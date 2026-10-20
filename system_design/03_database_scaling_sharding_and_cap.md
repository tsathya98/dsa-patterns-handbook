# Database scaling, sharding, and the CAP theorem

> **Target:** System design interviews  
> **Core concept:** Choosing between SQL, NoSQL, and Distributed SQL, understanding storage engines (B+ Trees vs. LSM-Trees), scaling from read replicas to sharded clusters, and trading off consistency vs. availability.

## 1. Relational (SQL) vs. Non-Relational (NoSQL)

If both SQL and NoSQL support indexing and both support sharding, why do both exist?

The short answer: **SQL was built for a single computer in the 1970s and forced to scale later. NoSQL was built from day one to live across hundreds of machines.**

Because of that difference in origin, they force you to model data in opposite directions.

### The design shift: Schema-first vs. Query-first

#### SQL is Schema-First
In Postgres or MySQL, you design tables around entities and their real-world relationships. You make a `users` table, an `orders` table, and link them with foreign keys.

You do not need to know what queries your product manager will ask for six months from now. If marketing suddenly asks for *"all users over age 25 in Bangalore who bought shoes on a Sunday"*, you can write a SQL query with three `JOIN`s and `WHERE` clauses. The database engine calculates the answer on the fly. 

SQL gives you complete query flexibility at the cost of join overhead at massive scale.

#### NoSQL is Access-Pattern-First
In DynamoDB or Cassandra, you cannot do that. You must know your exact queries **before** you design the table.

If you are building an Instagram feed in DynamoDB, you look at your UI and say: *"I only need to do one thing: fetch posts for user X, sorted by timestamp."*

You set `user_id` as your partition key and `timestamp` as your sort key.

That one query runs in 5 milliseconds at any scale. But if someone asks: *"Can you search for posts containing the word 'coffee'?"*, DynamoDB cannot do it without scanning every single record across every server in the cluster. It will freeze your database and cost thousands of dollars.

In NoSQL, you give up ad-hoc queries to get guaranteed single-digit millisecond latency on a few predefined lookups.

### How sharding actually works under the hood

#### Sharding in SQL is bolted on
Postgres was designed to run on one server. When your data hits 20 TB and you have to split it across 10 database servers, Postgres does not do this naturally out of the box.

You have to bolt on external middleware like Vitess or Citus, or write manual routing logic in your application code.

Once you split SQL across 10 machines:
* **Cross-shard joins break:** A join between an order on Machine A and a user on Machine B means pulling data across the network, which kills latency.
* **Distributed transactions slow down:** Multi-table ACID transactions across different servers require two-phase commit (2PC) protocols that degrade write throughput.

Once you shard SQL, you lose the primary benefits that made SQL appealing in the first place.

#### Sharding in NoSQL is native
DynamoDB and Cassandra were designed around a hash ring.

When you write an item with partition key `user_123`, the database hashes that key: `hash("user_123")`. That hash points directly to Server 42.

The database routes the request to Server 42 in constant time $O(1)$. There are no cross-table joins or relational foreign keys to coordinate, because everything needed to answer that query is stored inside that one item or partition.

Whether you store 1,000 rows or 10 billion rows, DynamoDB gives you the exact same latency.

---

## 2. Storage engines: B+ Trees vs. LSM-Trees

This is a core follow-up topic for senior and staff interviewers.

```text
B+ Tree (SQL / In-Place Updates)            LSM-Tree (NoSQL / Append-Only Log)
┌─────────────────────────┐                  ┌───────────────────────────────┐
│ Page Directory / Nodes  │                  │ In-Memory MemTable (Fast RAM) │
│ [ 10 | 20 | 30 | 40 ]   │                  └──────────────┬────────────────┘
└────────────┬────────────┘                                 │ Flushes sequentially
             │ Random Disk Seeks                            ▼
             ▼                               ┌───────────────────────────────┐
┌─────────────────────────┐                  │ Immutable SSTables on Disk    │
│ Updated Page on Disk    │                  │ (Background Compaction)       │
└─────────────────────────┘                  └───────────────────────────────┘
```

* **SQL (Postgres, MySQL InnoDB) uses B+ Trees:**
  B-Trees keep data organized on disk so range queries (`WHERE age BETWEEN 20 AND 30`) and point lookups are fast. But whenever you write or update data, the database has to update nodes in place across random disk blocks. Under write-heavy workloads, random I/O saturates disk bandwidth.
* **NoSQL (Cassandra, ScyllaDB, RocksDB) uses LSM-Trees:**
  When a write arrives, the database writes it sequentially to an append-only Write-Ahead Log (WAL) on disk and inserts it into an in-memory sorted structure (MemTable). It never performs random disk seeks for updates. When the MemTable fills, it flushes to disk as an immutable Sorted String Table (SSTable). Background threads periodically merge and deduplicate SSTables (compaction). This allows LSM-Trees to absorb millions of writes per second (e.g. sensor data, chat messages, metrics).

---

## 3. The Serverless Postgres reality vs. Distributed SQL

A common misconception in system design interviews is assuming that Serverless Postgres provides horizontal write scaling.

### What Serverless Postgres actually does
Platforms like AWS Aurora Serverless v2 and Neon decouple **Compute** from **Storage**:
1. **Shared distributed storage:** The storage layer auto-expands across availability zones without managing disk partitions.
2. **Stateless compute:** The database engine runs on independent compute nodes.

This enables two specific capabilities:
* **Dynamic vertical scaling:** CPU and RAM scale from 2 GB to 64 GB without restarting the database.
* **Horizontal read scaling:** You can spin up read replicas quickly because they connect directly to the shared storage layer without copying data disks.

### The catch: The single writer bottleneck
**All write traffic still funnels through one primary writer node.**
* If your application pushes 50,000 writes per second, Serverless Postgres will scale up that single machine's CPU and memory.
* Once that single writer hits its hardware, connection, or lock queue limits, writes will bottleneck. You cannot add a second writer node to share write throughput in standard Serverless Postgres.

### True Distributed SQL (Spanner, CockroachDB, YugabyteDB)
If you require a relational database that distributes both reads and writes horizontally across multiple nodes, you need Distributed SQL.

These engines partition data across nodes while maintaining multi-node ACID transactions using consensus protocols (Paxos or Raft):
* **The trade-off:** Write latency increases from ~1-2 ms (single-node Postgres) to 15-30 ms because nodes must complete cross-network round trips to reach consensus before committing.

---

## 4. Database selection decision matrix

| Feature | Relational (PostgreSQL / MySQL) | Distributed SQL (Spanner / CockroachDB) | NoSQL (DynamoDB / Cassandra) |
| :--- | :--- | :--- | :--- |
| **Data model** | Tables, strict schemas, foreign keys | Tables, strict schemas, foreign keys | Key-value, document, wide-column |
| **Query style** | Complex declarative SQL with multi-table `JOIN`s | SQL with distributed joins | Primary key and hash/range lookups. Zero joins. |
| **Scaling writes** | Vertical only (single primary node) | Horizontal (distributed consensus) | Horizontal (hash ring partitioning) |
| **Scaling reads** | Horizontal (read replicas) | Horizontal (any node) | Horizontal (any node) |
| **Transactions** | Strong ACID on single node | Distributed ACID (Paxos/Raft) | Single-row ACID, eventual consistency across nodes |
| **Write latency** | Ultra-low (1-3 ms local write) | Medium (15-30 ms consensus round trips) | Ultra-low (2-5 ms append/hash write) |
| **Best suited for** | Financial ledgers, e-commerce checkout, relational data | Global inventory, financial ledgers needing horizontal scale | High-throughput telemetry, chat feeds, clickstream, user sessions |

---

## 5. Phases of database scaling

```text
Phase 1: Read/Write Split (Replicas)          Phase 2: Database Sharding (Horizontal Partitioning)
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
  * With asynchronous replication, the primary commits a write and returns to the client before replicas apply the WAL/binlog event (often milliseconds to seconds later).
  * *Symptom:* A user edits their profile, the page reloads, the `GET` request hits a lagging replica, and the user sees their old profile.
  * *Fix (read-your-own-writes):* Pin reads for the acting user to the primary node for a short window (e.g. 5 seconds) after they perform a write, or pass the last written log sequence number (LSN) and wait until the replica catches up to that LSN.

### Phase 2: Horizontal sharding
When write throughput saturates a single primary node's disk IOPS or a table grows past several terabytes, split rows across independent database shards so each shard holds a subset of the data.

---

## 6. Sharding strategies and partition keys

Your choice of **shard key (partition key)** determines whether traffic spreads evenly or piles onto a single hot node:

| Strategy | How it routes | Pros | Cons and traps |
| :--- | :--- | :--- | :--- |
| **Range-based** | Partition by contiguous key ranges (e.g. `user_id` 1-1M on Shard 1, 1M-2M on Shard 2, or by month). | Efficient range scans (`WHERE created_at BETWEEN ...`). | **Hot shards:** If keys are monotonically increasing (timestamps or auto-increment IDs), the newest shard takes 100% of writes. |
| **Hash-based** | `shard_id = hash(key) % num_shards` | Spreads reads and writes evenly across shards. | Range queries must scatter-gather across all shards; naive modular hashing moves almost all keys when `num_shards` changes. |
| **Directory-based** | A lookup service maps each partition key or tenant ID to its current physical shard. | Can move individual heavy tenants to dedicated shards without changing hash math. | Extra lookup hop (if not cached on clients), and the directory table itself must be highly available. |

---

## 7. Consistent hashing

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

---

## 8. CAP theorem and PACELC

In a distributed system across multiple machines or availability zones, network partitions (dropped packets, switch failures, split links) will happen.

```text
                       The CAP Theorem
                        Consistency
                            /\
                           /  \
                          /    \
                         /  CA  \   (Single-node only; no network partition)
                        /________\
             Availability ------ Partition Tolerance
                  (AP)                (CP)
```

Because **Partition Tolerance (P)** is mandatory whenever nodes communicate over an unreliable network, a partitioned system must choose how to behave when nodes cannot reach each other:

* **CP (Consistency + Partition Tolerance):**
  * During a network partition, nodes on the minority side (or nodes that cannot form a quorum) reject writes and linearizable reads rather than returning stale or conflicting state.
  * *Examples:* Raft/Paxos state machines (etcd, ZooKeeper, Consul), Google Cloud Spanner, single-primary relational databases with synchronous quorum replication.
  * *Use cases:* Financial balances, inventory counts, seat reservations, distributed locks.
* **AP (Availability + Partition Tolerance):**
  * During a partition, isolated nodes keep accepting reads and writes locally and reconcile conflicting writes after the network heals (eventual consistency via Last-Write-Wins, vector clocks, or CRDTs).
  * *Examples:* DynamoDB (default eventual reads), Apache Cassandra, Couchbase.
  * *Use cases:* Shopping carts, social media likes/view counters, DNS propagation.

### PACELC theorem (including normal operation)
CAP only describes what happens during a network partition. PACELC explains what the system trades off when the network is healthy:
* **If Partition (P):** choose **Availability (A)** or **Consistency (C)**.
* **Else (E, normal operation):** choose **Latency (L)** or **Consistency (C)**.
  * *PA/EL systems (Cassandra, DynamoDB eventual reads):* Stay available during partitions and return fast local reads/writes without waiting for all replicas during normal operation.
  * *PC/EC systems (Spanner, synchronous quorum SQL):* Require quorum agreement both during partitions and on normal reads/writes, trading higher latency for strict linearizability.
