# Distributed coordination, transactions, and concurrency control

> **Target:** System design interviews (L4 to L6)  
> **Core concept:** Once state spans multiple servers or databases, packets drop, processes pause during GC, and concurrent requests race on the same rows. This guide covers idempotency, cross-service transactions, leader election with fencing tokens, and database locking.

## 1. Idempotency and cross-service transactions

When an RPC times out over a network, the caller cannot tell whether the request dropped before reaching the server or succeeded on the server and dropped on the way back.

### 1. Idempotency keys
* **Problem:** A user clicks "Pay \$50", their mobile connection drops before the HTTP response returns, the client retries, and the user gets charged \$100.
* **Fix:** The client generates a UUID (`Idempotency-Key: req_98a7`) for the payment attempt and sends it in the request header. The server stores the key and its final response in an `idempotency_keys` table inside the same database transaction as the ledger write. If a retry arrives with the same key, the server returns the stored response without charging the card again.

### 2. Delivery guarantees
* **At-most-once:** Send once and never retry. Fast, but drops events on failure.
* **At-least-once:** Retry until acknowledged. Prevents data loss, but delivers duplicates whenever ACKs are lost or workers crash mid-flight.
* **Effectively-once:** Combine **at-least-once delivery** with an **idempotent consumer** (deduplicating by `event_id` or using deterministic `UPSERT` keys).

### 3. Dual-write problem and the transactional outbox pattern
* **Problem:** An application writes a row to Postgres and on the next line publishes an `OrderCreated` event to Kafka. If the process crashes between the database commit and the Kafka publish (or if Kafka is temporarily unreachable), the database has the order but downstream consumers never receive the event.

```text
Broken Dual Write:                        Transactional Outbox Pattern:
App ──1. INSERT order──> [ Postgres ]     App ──1. BEGIN TX ──────────────────┐
 │  (App crashes here)                                                        ▼
 └───2. Publish (Never happens)                [ Postgres: orders + outbox ] (COMMIT)
                                                              │
                                                     2. Tail WAL / poll outbox
                                                              ▼
                                                    [ Outbox Relay ] ──> [ Kafka ]
```

* **Fix (Transactional Outbox):** Within a **single local SQL transaction**, `INSERT` the order into `orders` and `INSERT` the event payload into an `outbox` table, then `COMMIT`. A separate relay process (either polling the `outbox` table or tailing the Postgres WAL via Debezium CDC) publishes pending outbox rows to Kafka and marks them sent once Kafka acknowledges them.

* **Transactional outbox 4-step sequence:**
  * **1. Atomic local commit:** Within a single DB transaction, insert the entity into `orders` and the event into an `outbox` table, then commit.
  * **2. Change data capture (CDC):** A background relay (Debezium tailing the WAL log or scheduled poller) reads unpublished outbox rows.
  * **3. At-least-once publish:** The relay publishes the event to Kafka and updates the outbox row status to published upon broker ACK.
  * **4. Idempotent consumption:** Consumers deduplicate messages via message ID before processing to prevent duplicate side-effects.


### 4. Saga pattern
* **Problem:** A checkout workflow spans three separate services with their own databases: `ReserveInventory` $\to$ `ChargeCard` $\to$ `CreateShipment`. You cannot hold a single ACID database transaction across three independent microservices.
* **Fix:** Model the workflow as a **Saga**, which is a sequence of local transactions paired with explicit **compensating actions** (undo steps). If `ChargeCard` fails at Step 2, the Saga orchestrator executes the compensating action for Step 1 (`ReleaseInventory`) to return the system to a consistent state. Both forward steps and compensating steps must be idempotent.

### 5. Two-Phase Commit (2PC)
* **How it works:** A coordinator asks all participating databases to prepare and lock rows (Phase 1: Voting), and once all vote `YES`, tells all of them to commit (Phase 2: Commit).
* **Trade-offs:** 2PC is a blocking protocol. All participants hold row locks across network round trips, and if the coordinator crashes after Phase 1, participants remain blocked holding locks until the coordinator recovers. Prefer **Transactional Outbox** or **Sagas** across microservices; reserve 2PC or Paxos-backed distributed transactions (like Spanner) for storage engines designed around them.

### 6. Poison pill messages
* **Problem:** A corrupted or unexpected message payload triggers an unhandled exception in a consumer worker. The worker crashes, the message visibility timeout expires, the broker redelivers the same message to another worker, and the entire consumer fleet enters a crash loop.
* **Fix:** Configure a maximum delivery count (for example, `maxReceiveCount = 5`) and route messages that exceed it to a **Dead Letter Queue (DLQ)** with alerting so healthy messages continue processing.

## 2. Distributed coordination and consensus

### 1. Leader election
* **Problem:** You run 3 replicas of a scheduler service for high availability, and at midnight all 3 replicas fire the same daily billing job.
* **Fix:** Elect a single active leader using a consensus store (`etcd`, `ZooKeeper`, `Consul`) or a database lease table so only the leader schedules singleton jobs while followers stand by.

### 2. Leases (time-bounded locks)
* **Problem:** If a worker acquires a lock with no expiration and then loses power, no other worker can ever acquire the lock.
* **Fix:** Grant locks as **leases with a TTL** (for example, 15 seconds). The lock holder sends periodic heartbeats every 5 seconds to extend the lease while working; if the holder crashes, the lease expires and another node takes over.

### 3. Fencing tokens (preventing zombie writes)
* **Problem:** Leases alone do not protect storage from a paused leader. Suppose Worker 1 holds a 15-second lease, pauses for 30 seconds in a stop-the-world GC pause right before sending a write, and meanwhile its lease expires and Worker 2 acquires the lease and writes new state. When Worker 1 wakes up from GC, it finishes sending its delayed write and overwrites Worker 2's data.

```text
Worker 1 (Paused):  [Gets Lease, Token #33] ──(30s GC Pause...)──────────> Writes with Token #33 (Rejected)
Worker 2 (New):                               [Gets Lease, Token #34] ──> Writes with Token #34 (Accepted, min_token = 34)
```

* **Fix:** Issue a **monotonically increasing fencing token** (`33`, `34`, `35`...) every time a lease is acquired. The worker passes its fencing token on every write to the storage system, and the storage system rejects any write carrying a token smaller than the highest token it has already processed (`WHERE fencing_token >= current_fencing_token`).

### 4. Split brain and quorums
* **Problem:** A network link between two availability zones drops. Both sides think the other side crashed, and both sides promote a primary database node, accepting conflicting writes that diverge.
* **Fix:** Require a **majority quorum ($\lfloor N/2 \rfloor + 1$)** of nodes to elect a leader or commit a write. In a 5-node cluster split into 3 nodes vs. 2 nodes, only the 3-node partition has a majority ($\ge 3$) and can continue accepting writes; the 2-node partition steps down. Deploy consensus clusters with an odd number of nodes (3 or 5).

### 5. Consensus protocols (Raft and Paxos)
* **Role:** Consensus algorithms (`Raft` in etcd, CockroachDB, and Kafka KRaft; `Paxos` in Spanner) replicate a state machine log across a quorum of nodes so that leadership election and log commits remain linearizable across node crashes and network partitions.

### 6. Clock skew
* **Problem:** Physical wall clocks (`time.time()` synced via NTP) drift by tens of milliseconds across machines. If you resolve concurrent writes across nodes using wall-clock Last-Write-Wins (LWW), a machine whose clock is 100ms fast will overwrite later writes from a machine with an accurate clock.
* **Fix:** Order events using monotonic version counters in the database, Lamport/vector logical clocks, or bounded-uncertainty hardware clocks (Google TrueTime).

## 3. Database concurrency control: optimistic vs. pessimistic locking

### 1. Lost updates and Optimistic Concurrency Control (OCC)
* **Problem:** Alice and Bob both read Version 1 of a document at 10:00. Alice saves her edit at 10:01, and Bob saves his edit at 10:02, blindly overwriting Alice's changes.
* **Fix (OCC / compare-and-swap):** Include a `version` column (or `ETag`) on the row and check it in the `WHERE` clause on update:
  ```sql
  UPDATE reports
  SET content = 'Bob edit', version = 2
  WHERE id = 100 AND version = 1;
  ```
  Because Alice already incremented `version` to `2`, Bob's update affects `0` rows. The application detects `rows_affected == 0` and returns `HTTP 409 Conflict` or `412 Precondition Failed` so Bob's client can fetch the latest version and merge.

### 2. Pessimistic locking (`SELECT ... FOR UPDATE`)
* **When to use:** When contention on the same row is high (such as deducting inventory or transferring account balances) and optimistic retries would thrash.
* **Fix:** Acquire an exclusive row lock inside the transaction before reading and modifying:
  ```sql
  BEGIN;
  SELECT balance FROM accounts WHERE id = 42 FOR UPDATE;
  UPDATE accounts SET balance = balance - 100 WHERE id = 42;
  COMMIT;
  ```
* **Trade-offs:** Prevents concurrent transactions from modifying the locked row until `COMMIT`, but holds database locks longer and can deadlock if two transactions lock multiple rows in opposite orders (prevent deadlocks by always locking row IDs in ascending order).

## 4. Self-check question

> **Question:** Two scheduler replicas both believe they own the same background curation job. Which two mechanisms from Section 2 prevent both of them from corrupting state in the database, and what role does each play?

<details>
<summary><b>Click to reveal answer</b></summary>

1. **Lease (time-bounded lock):** Ensures only one replica holds active ownership at a time, and automatically releases ownership after the TTL expires if the holder crashes and stops heartbeating.
2. **Fencing token:** Protects the database against a delayed or GC-paused former leader whose lease expired while it was frozen. Each lease acquisition increments the token (`#33` $\to$ `#34`), and the database rejects any write carrying an older token than the highest token it has already recorded.

</details>
