# 🗄️ Database Scaling, Sharding & The CAP Theorem

> **Target:** System Design Interviews (FAANG)  
> **Key Focus:** Moving from a single database server to a globally distributed, partition-tolerant database cluster.

---

## 📈 1. The 3 Phases of Database Scaling

```text
Phase 1: Read/Write Separation (Replicas)    Phase 2: Database Sharding (Horizontal Partitioning)
┌──────────────┐                             ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Primary DB  │ (All Writes)                │   Shard 1    │   │   Shard 2    │   │   Shard 3    │
└──────┬───────┘                             │ Users A - H  │   │ Users I - P  │   │ Users Q - Z  │
       │ (Replication Stream)                └──────────────┘   └──────────────┘   └──────────────┘
       ▼
┌──────────────┬──────────────┐
│ Read Replica │ Read Replica │ (All Reads)
└──────────────┘──────────────┘
```

### Phase 1: Read/Write Split (Primary-Replica)
* **Writes** go strictly to the **Primary** node.
* **Reads** are distributed across multiple **Read Replicas** via a connection pool or proxy (e.g. ProxySQL / PgBouncer).
* **The Gotcha — Replication Lag:**
  * Changes take a few milliseconds to reach replicas asynchronously.
  * *Bug:* User updates profile $\to$ page reloads $\to$ read hits replica that hasn't received the write yet $\to$ user sees old data!
  * *Fix:* **Read-your-own-writes consistency:** Route reads for the updating user directly to the Primary for 5 seconds after a write.

### Phase 2: Sharding (Horizontal Partitioning)
When database disk size exceeds ~1–2 TB or write IOPS bottleneck a single machine, split data across independent nodes (**shards**).

---

## 🔑 2. Sharding Strategies & The Sharding Key

The choice of **Partition Key (Sharding Key)** dictates the entire architecture:

| Sharding Strategy | Mechanism | Pros | Cons / Traps |
| :--- | :--- | :--- | :--- |
| **Range-Based** | Shard by ID range (e.g. IDs 1–1M $\to$ Shard 1, 1M–2M $\to$ Shard 2). | Simple range queries (`WHERE id BETWEEN 50 AND 100`). | Severe **Hotspotting**! Newer IDs receive 100% of the write traffic. |
| **Hash-Based** | `shard_id = hash(key) % total_shards` | Uniform distribution of data and traffic across all nodes. | Adding/removing a shard invalidates almost all keys $\to$ massive data migration! |
| **Directory-Based** | Lookup service / table maps keys to specific shard IDs. | Extremely flexible; easy to rebalance individual shards. | Lookup service is a potential bottleneck and Single Point of Failure (SPOF). |

---

## ⭕ 3. Consistent Hashing: The Distributed Saver

Standard modular hashing (`hash(key) % N`) breaks whenever nodes are added or removed because almost every key remaps to a new node.

### How Consistent Hashing Works:
1. Map both **servers** and **keys** onto a circular 360° hash ring (0 to $2^{32}-1$).
2. To find where a key lives: hash the key $\to$ walk **clockwise** on the ring until you hit the first server node.

```text
               Server A (0°)
                 ┌────────┐
          Key 1 ─┤        │
                 ▼        ▼
       Server C ◄────────── Server B (120°)
       (240°)      Key 2
```

3. **When Server B fails or is removed:** Only keys between A and B need to migrate (to Server C). The rest of the keys remain completely untouched!
4. **Virtual Nodes (V-Nodes):**
   * *Problem:* Real servers might map unevenly on the ring (causing hotspotting).
   * *Fix:* Assign each physical machine 100–250 "virtual nodes" across the ring. This spreads load evenly and avoids cascades when a node dies.

---

## ⚖️ 4. The CAP Theorem & PACELC

In any distributed data store, network partitions (dropped packets, severed cables, datacenter outages) are **inevitable physical realities**.

```text
                       The CAP Theorem
                        Consistency
                            /\
                           /  \
                          /    \
                         /  CA  \   (Impossible on distributed networks!)
                        /________\
             Availability ------ Partition Tolerance
                  (AP)                (CP)
```

Because **Partition Tolerance (P)** is mandatory, you can only choose between:

* **CP (Consistency + Partition Tolerance):**
  * When a network partition occurs, the system rejects writes or returns errors rather than serving inconsistent/stale data.
  * *Examples:* Traditional SQL with 2PC, Google Cloud Spanner, Apache HBase, ZooKeeper.
  * *Use Cases:* Banking balances, stock trades, ticketing systems where double-booking is forbidden.
* **AP (Availability + Partition Tolerance):**
  * When a network partition occurs, all nodes remain available to read/write, returning whatever data they have (even if stale). Nodes reconcile conflicts later (**Eventual Consistency**).
  * *Examples:* Apache Cassandra, DynamoDB, CouchDB.
  * *Use Cases:* Social media feeds, YouTube view counts, shopping cart items.

### PACELC Extension (When there is NO partition):
* If **P**artition: choose **A**vailability or **C**onsistency.
* **E**lse (Normal Operation): choose **L**atency or **C**onsistency.
  * *Example:* DynamoDB/Cassandra choose **PA/EL** (favor Availability during partitions, favor Low Latency during normal operations).
  * *Example:* PostgreSQL/MongoDB choose **PC/EC** (favor Consistency always).
