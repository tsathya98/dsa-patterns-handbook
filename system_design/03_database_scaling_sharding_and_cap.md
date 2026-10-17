# Database scaling, sharding, and the CAP theorem

> **Target:** System design interviews  
> **Core concept:** Scaling a database from a single node to read replicas and horizontally partitioned shards, and trading off consistency vs. availability during network partitions.

## 1. Phases of database scaling

```text
Phase 1: Read/Write Separation (Replicas)    Phase 2: Database Sharding (Horizontal Partitioning)
┌──────────────┐                             ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Primary DB  │ (All Writes)                │   Shard 1    │   │   Shard 2    │   │   Shard 3    │
└──────┬───────┘                             │ Users A - H  │   │ Users I - P  │   │ Users Q - Z  │
       │ (Replication Stream)                └──────────────┘   └──────────────┘   └──────────────┘
       ▼
┌──────────────┬──────────────┐
│ Read Replica │ Read Replica │ (All Reads)
└──────────────┴──────────────┘
```

### Phase 1: Read/write split (primary-replica replication)
* **Writes** go only to the **primary** node.
* **Reads** fan out across **read replicas**, typically behind a connection pooler like PgBouncer or ProxySQL.
* **Replication lag:**
  * With asynchronous replication, the primary commits a write and returns to the client before replicas apply the WAL/binlog event (often a few milliseconds to seconds later).
  * *Symptom:* A user edits their profile, the browser reloads immediately, the `GET` request hits a lagging replica, and the user sees their old profile.
  * *Fix (read-your-own-writes):* Pin reads for the acting user to the primary node for a short window after they perform a write, or pass the last written log sequence number (LSN) and wait until the replica catches up to that LSN.

### Phase 2: Horizontal sharding
When write throughput saturates a single primary node's disk IOPS or a table grows past a few terabytes, split rows across independent database shards so each shard holds a subset of the data.

## 2. Sharding strategies and partition keys

Your choice of **shard key (partition key)** determines whether traffic spreads evenly or piles onto a single hot node:

| Strategy | How it routes | Pros | Cons and traps |
| :--- | :--- | :--- | :--- |
| **Range-based** | Partition by contiguous key ranges (for example, `user_id` 1-1M on Shard 1, 1M-2M on Shard 2, or by month). | Efficient range scans (`WHERE created_at BETWEEN ...`). | **Hot shards:** If keys are monotonically increasing (timestamps or auto-increment IDs), the newest shard takes 100% of writes. |
| **Hash-based** | `shard_id = hash(key) % num_shards` | Spreads reads and writes evenly across shards. | Range queries must scatter-gather across all shards; naive `% N` hashing moves almost all keys when `num_shards` changes. |
| **Directory-based** | A lookup service maps each partition key or tenant ID to its current physical shard. | Can move individual heavy tenants to dedicated shards without changing hash math. | Extra lookup hop (if not cached on clients), and the directory table itself must be highly available. |

## 3. Consistent hashing

With naive modular hashing (`hash(key) % N`), changing $N$ from $4$ to $5$ remaps ~80% of keys to different shards, triggering massive data migration or cache misses.

### How consistent hashing works
1. Hash both **nodes** and **keys** onto a circular integer ring $[0, 2^{32}-1]$.
2. To route a key, compute `hash(key)` and walk clockwise around the ring until you hit the first node.

```text
               Server A (0°)
                 ┌────────┐
          Key 1 ─┤        │
                 ▼        ▼
       Server C ◄────────── Server B (120°)
       (240°)      Key 2
```

3. **Adding or removing a node:** If Server B goes down, only the keys sitting on the arc between Server A and Server B shift clockwise to Server C. On average, adding or removing a node in an $N$-node ring moves only $1/N$ of the keys.
4. **Virtual nodes (vnodes):**
   * With only 3 physical points on the ring, random placement leaves uneven arc sizes and skewed load.
   * Assigning 100 to 256 virtual node tokens per physical machine interleaves ranges evenly around the ring and spreads a failed machine's load across all surviving machines instead of dumping it onto a single neighbor.

## 4. CAP theorem and PACELC

In a distributed system across multiple machines or availability zones, network partitions (dropped packets, switch failures, split links) will happen.

```text
                       The CAP Theorem
                        Consistency
                            /\
                           /  \
                          /    \
                         /  CA  \   (Single-node / no network partition)
                        /________\
             Availability ------ Partition Tolerance
                  (AP)                (CP)
```

Because **Partition Tolerance (P)** is required whenever nodes communicate over a network, a partitioned system has to choose how to behave when nodes cannot reach each other:

* **CP (Consistency + Partition Tolerance):**
  * During a partition, nodes on the minority side (or nodes that cannot reach a quorum) reject writes and linearizable reads rather than returning stale or conflicting state.
  * *Examples:* Raft/Paxos state machines (etcd, ZooKeeper, Consul), Google Cloud Spanner, single-primary relational databases with synchronous quorum replication.
  * *Use cases:* Bank ledgers, inventory deduction, seat reservation, distributed locks.
* **AP (Availability + Partition Tolerance):**
  * During a partition, isolated nodes keep accepting reads and writes locally and reconcile conflicts after the network heals (eventual consistency via LWW, vector clocks, or CRDTs).
  * *Examples:* DynamoDB (default eventual reads), Apache Cassandra, Riak.
  * *Use cases:* Shopping carts, social media likes/view counters, DNS propagation.

### PACELC theorem (including normal operation)
CAP only describes what happens during a partition. PACELC adds what the system trades off when the network is healthy:
* **If Partition (P):** choose **Availability (A)** or **Consistency (C)**.
* **Else (E, normal operation):** choose **Latency (L)** or **Consistency (C)**.
  * *PA/EL systems (Cassandra, DynamoDB eventual reads):* Stay available during partitions and return fast local reads/writes without waiting for all replicas during normal operation.
  * *PC/EC systems (Spanner, synchronous quorum SQL):* Require quorum agreement both during partitions and on normal reads/writes, trading higher latency for strong consistency.
