# 🤝 Distributed Coordination, Exactly-Once & Concurrency Guide

> **Target:** FAANG System Design Interviews (L4–L6)  
> **Core Idea:** Once you have more than one server or more than one database, networks will drop packets, machines will freeze mid-operation, and two users will click "Save" at the exact same millisecond. Here is how production systems keep data correct.

---

## 🎯 1. Doing Things Exactly Once

In a distributed system, you never know if a timeout means *"the request failed before reaching the server"* or *"the server succeeded, and only the reply got lost."*

### 1. Idempotency
* **What goes wrong:** A user clicks "Pay \$50", their Wi-Fi blips, the app retries automatically, and their credit card gets charged \$100.
* **Real-World Example:** Stripe payment retries or a background worker retrying a webhook after a `504 Gateway Timeout`.
* **The Fix:** **Idempotency Keys.** The client generates a unique UUID (`idempotency_key: "req_98a7"`) and sends it in the header. The server saves that key + the response in a DB table. If the same key arrives again, the server skips execution and **replays the saved response**.

### 2. Delivery Guarantees
* **What goes wrong:**
  * *At-most-once:* Fire and forget—fast, but drops messages if a worker crashes.
  * *At-least-once:* Retries until acknowledged—never loses data, but sends duplicates.
  * *Exactly-once:* Mathematically impossible over a network without coordination at the receiver.
* **The Fix:** **At-Least-Once Delivery + Idempotent Consumer.** Let the queue retry freely, and make the consumer check an idempotency table or `UPSERT` by primary key so duplicates are harmless.

### 3. The Dual-Write Problem & Transactional Outbox
* **What goes wrong:** Your code saves an order to Postgres, and on the next line publishes an `"OrderCreated"` event to Kafka. If the server crashes between line 1 and line 2, the database has the order, but Kafka never hears about it—your system is now permanently out of sync!

```text
❌ Broken Dual Write:                     ✅ Transactional Outbox Pattern:
App ──1. INSERT order──> [ Postgres ]     App ──1. BEGIN TX ──────────────────┐
 │  (App crashes here! 💥)                                                    ▼
 └───2. Publish (NEVER HAPPENS)           [ Postgres: orders table + outbox table ] (COMMIT!)
                                                              │
                                                     2. Polls & Publishes
                                                              ▼
                                                    [ Outbox Relay ] ──> [ Kafka ]
```

* **The Fix:** **Transactional Outbox Pattern.** Inside a **single local database transaction**, `INSERT` into the `orders` table AND `INSERT` the event payload into an `outbox` table. Commit both atomically. A separate background worker (or Debezium CDC) reads rows from the `outbox` table and publishes them to Kafka until acknowledged.

### 4. Saga Pattern
* **What goes wrong:** One business workflow spans 3 separate microservices (e.g., Book Flight $\to$ Book Hotel $\to$ Charge Card). You can't wrap 3 separate databases in one SQL transaction. What if Flight and Hotel succeed, but the Credit Card declines?
* **Real-World Example:** Booking a vacation bundle across Airline, Hotel, and Payment services, or publishing a report that spans both a Report Service and a Dashboard Service.
* **The Fix:** **A Chain of Local Steps + Compensating ("Undo") Actions.** If Step 3 (`Charge Card`) fails, the Saga runs backward executing explicit undo steps: `Cancel Hotel` $\to$ `Cancel Flight`.

### 5. Two-Phase Commit (2PC)
* **What goes wrong:** You try to make 3 databases commit at the exact same moment using a central coordinator (Phase 1: *"Are you all ready?"* $\to$ Phase 2: *"Commit now!"*).
* **Why interviewers hate it at scale:** Every database holds row locks while waiting for the coordinator. If the coordinator crashes mid-protocol, all databases stay locked and blocked! Use **Sagas** or **Outbox** instead whenever possible.

### 6. Poison Message (Poison Pill)
* **What goes wrong:** A malformed message lands in your queue (e.g., unexpected `null` field that triggers a `NullPointerException`). The worker crashes, the message goes back to the queue, the next worker picks it up and crashes too—stuck in an infinite crash loop forever.
* **The Fix:** **Max Receive Count + Dead-Letter Queue (DLQ).** Track delivery attempts; after $N$ failures (e.g., 3 tries), move the message aside into a DLQ and alert an engineer so healthy messages keep flowing.

---

## 🧭 2. Coordinating Several Machines

When you run 5 replicas of an orchestrator or cron scheduler, how do they agree on who is in charge without stepping on each other?

### 1. Leader Election
* **What goes wrong:** You run 3 replicas of a billing service for high availability. At midnight, all 3 wake up and run the daily billing job, charging every customer 3 times.
* **The Fix:** Elect **one single Leader** using a coordination service (`etcd`, `ZooKeeper`, `Consul`) or a database advisory lock. Only the leader executes scheduled singleton tasks; followers stand by in case the leader dies.

### 2. Lease (Time-Bounded Lock)
* **What goes wrong:** Worker A grabs a lock to process a job, and then Worker A's hardware catches fire. If the lock never expires, no other worker can ever touch that job again.
* **The Fix:** **Acquire a Lease with a TTL** (e.g., 30 seconds). While Worker A is alive, it sends a heartbeat every 10 seconds to renew the lease. If Worker A dies, the lease expires after 30 seconds and Worker B takes over.

### 3. Fencing Token (The Zombie Leader Fix)
* **What goes wrong:** Lease alone has a fatal flaw! Imagine Worker 1 holds a 30-second lease, then hits a **45-second Garbage Collection (GC) pause** (it freezes right before writing to storage). Meanwhile, the lease expires, and Worker 2 gets the new lease and writes fresh data. Suddenly, Worker 1 unfreezes from GC and blindly overwrites Worker 2's fresh data with old data!

```text
Worker 1 (Zombie):  [Gets Lease #33] ──(Frozen in 45s GC Pause...)──────────> Writes with Token #33 ❌ (Rejected!)
Worker 2 (New):                         [Gets Lease #34] ──> Writes with Token #34 ✅ (Storage sets min_token = 34)
```

* **The Fix:** **Monotonically Increasing Fencing Tokens (`fence_generation_num`).** Every time a lease is granted, the lock service increments a counter (`33`, `34`, `35`...). Workers must pass this number with every write. The database checks: `IF token < last_seen_token THEN REJECT`. When Zombie Worker 1 wakes up with Token `#33`, storage rejects it because it has already seen Token `#34`!

### 4. Split Brain
* **What goes wrong:** A network cable between Datacenter East and Datacenter West gets cut. Neither side can ping the other, so *both* sides assume the other died and *both* elect their own Primary database—accepting conflicting writes that corrupt data.
* **The Fix:** **Quorum (Majority Vote: $\lfloor N/2 \rfloor + 1$).** If you have 5 nodes and the network splits into `3 nodes` vs `2 nodes`, only the side with `3 nodes` (the majority) is allowed to elect a leader and accept writes. The `2-node` side automatically steps down. (Always use an **odd number** of consensus nodes: 3 or 5!).

### 5. Consensus (Raft / Paxos)
* **What goes wrong:** How do multiple machines agree on a single truth (who the leader is, or what order transactions happened) even when nodes crash or packets drop?
* **The Fix:** Consensus algorithms like **Raft** or **Paxos** (built into `etcd`, `CockroachDB`, `Spanner`, and `Kafka KRaft`), which use quorum voting so any committed entry is guaranteed to survive node failures.

### 6. Clock Skew
* **What goes wrong:** You resolve conflicting edits using "Last Write Wins" (`LWW`) based on each server's local wall-clock (`System.currentTimeMillis()`). But Server A's NTP clock is 200ms ahead of Server B's clock! Server B writes *later* in real life, but its timestamp looks *earlier*, so its update is silently thrown away.
* **The Fix:** Never trust physical wall-clock timestamps across machines for ordering. Use **database-generated monotonically increasing version numbers**, **Lamport logical clocks**, or **Google TrueTime**.

---

## 🔒 3. Data Consistency & Concurrent Edits

### 1. Lost Update Problem (Optimistic Concurrency Control)
* **What goes wrong:** Alice and Bob both open the same shared report (Version 1) at 10:00 AM. Alice edits the title and saves at 10:01 AM. Bob edits a paragraph and saves at 10:02 AM—unaware of Alice's save, Bob's payload overwrites the whole document and **erases Alice's work**.
* **The Fix:** **Optimistic Concurrency Control (OCC).** Attach a `version` number (or `ETag` / `snapshot_token`) to every row:
  ```sql
  UPDATE reports 
  SET content = 'Bob edit', version = 2 
  WHERE id = 100 AND version = 1;
  ```
  * Since Alice already bumped `version` to `2`, Bob's `WHERE version = 1` matches **0 rows**!
  * The server returns `412 Precondition Failed` (or `409 Conflict`), telling Bob to refresh and merge his changes.

### 2. Pessimistic Locking
* **What goes wrong:** When contention is super high (e.g., 500 people trying to buy the last concert seat or transfer money from the same account), optimistic retries fail 99% of the time.
* **The Fix:** **Lock the row upfront before editing (`SELECT * FROM seats WHERE id = 5 FOR UPDATE`).** No other transaction can modify or lock that row until you `COMMIT`.
* **Trade-off:** Safe against lost updates, but slows down throughput and risks **Deadlocks** if Transaction 1 locks Row A then wants Row B, while Transaction 2 locks Row B then wants Row A.

---

## 🧠 Quick Self-Check Challenge

> **Question:** Two orchestrator replicas both think they own the curation run for the same Dashboard. Which **two concepts** from Section 2 stop them from both writing, and what does each one do?

<details>
<summary><b>💡 Click to Reveal the Answer</b></summary>

1. **Lease (Time-Bounded Lock):** Ensures only one orchestrator replica can acquire ownership of the curation run at a time, and automatically releases ownership if that replica crashes and stops sending heartbeats.
2. **Fencing Token (`fence_generation_num`):** Protects against a "zombie" replica whose lease expired while it was frozen (e.g., during a GC pause or network lag). Each lease hands out an increasing number (`#1`, `#2`...). When the delayed replica wakes up and tries to write with old token `#1`, the storage layer rejects it because it has already seen token `#2`!

</details>
