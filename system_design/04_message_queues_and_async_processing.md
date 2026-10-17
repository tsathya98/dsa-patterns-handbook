# Message queues and event-driven architecture

> **Target:** System design interviews  
> **Core concept:** Decoupling producers from consumers with an asynchronous queue or log to smooth traffic spikes, isolate downstream failures, and scale background workers independently.

## 1. Synchronous vs. asynchronous processing

```text
Synchronous (Blocking): Cascading Failure Risk
User ──> [ Web Server ] ──> [ Payment API ] ──> [ Email Service ] ──> [ Warehouse API ]
(Latency = 50ms + 200ms + 300ms + 400ms = ~950ms. If Email crashes, checkout fails.)

Asynchronous (Decoupled): Fast Response and Fault Isolation
User ──> [ Web Server ] ──> [ Payment API ] ──> [ Message Queue / Kafka ]
            │                                             │
            ▼ (Returns 200 OK in ~250ms)                  ├──> [ Email Worker ]
                                                          └──> [ Warehouse Worker ]
```

### Why put a queue between services
1. **Decoupling:** The checkout service publishes an `OrderPlaced` event without caring whether 1 or 10 downstream services consume it.
2. **Load leveling (buffering):** If traffic spikes $10\times$ during a flash sale, the queue buffers incoming jobs in memory/disk while workers drain them at a steady rate that does not overwhelm the database.
3. **Fault isolation:** If the email provider goes down for 20 minutes, checkout stays up and queued email jobs process once the worker recovers.
4. **Independent scaling:** You can autoscale worker pods based on queue lag without touching the web tier.

## 2. Traditional message brokers (RabbitMQ, SQS) vs. event logs (Kafka, Kinesis)

| Feature | Message broker (RabbitMQ, AWS SQS) | Distributed commit log (Apache Kafka, AWS Kinesis) |
| :--- | :--- | :--- |
| **Delivery model** | Push (RabbitMQ) or point-to-point poll (SQS); tracks per-message ACK state. | Pull; consumers track their own integer offset in an append-only log. |
| **Message retention** | Deleted from the queue as soon as the consumer acknowledges it. | Retained on disk for a configured window (for example, 7 days) or indefinitely via compaction. |
| **Replayability** | No replay once ACKed. | Consumers can rewind their offset to replay historical events or bootstrap a new service. |
| **Ordering** | Best-effort (standard SQS) or strict FIFO per message group (SQS FIFO / single RabbitMQ consumer). | Strict ordering guaranteed **within each partition**. |
| **Throughput** | Tens of thousands of messages/sec per broker. | Hundreds of thousands to millions of events/sec via sequential disk I/O and `sendfile` zero-copy. |
| **Best fit** | Task queues, delayed jobs, per-message routing rules, long-running background work. | High-throughput event pipelines, CDC streams, audit logs, multiple independent consumer groups. |

## 3. Kafka mechanics: topics, partitions, and consumer groups

```text
               Topic: "user-orders" (Partition key: user_id)
        ┌──────────────────────────────────────────────┐
        │ Partition 0: [Msg 0][Msg 1][Msg 2][Msg 3]... │ ──> Consumer A
        ├──────────────────────────────────────────────┤
        │ Partition 1: [Msg 0][Msg 1][Msg 2]...        │ ──> Consumer B  (Consumer Group 1)
        ├──────────────────────────────────────────────┤
        │ Partition 2: [Msg 0][Msg 1][Msg 2][Msg 3]... │ ──> Consumer C
        └──────────────────────────────────────────────┘
```

* **Topic:** Named logical stream of events (such as `user-orders`).
* **Partition:** Ordered, immutable append-only log file. Partitions are the unit of parallelism in Kafka.
* **Partition key:** `hash(partition_key) % num_partitions`. Using `user_id` or `order_id` as the partition key routes all events for that entity to the same partition in exact order.
* **Consumer group:** Within a single consumer group, **each partition is assigned to at most one consumer instance at a time**. If a topic has 6 partitions, a consumer group can have at most 6 active consumers (any 7th consumer sits idle as a warm standby).

## 4. Delivery semantics and idempotency

When networks drop packets or workers crash mid-job, message delivery falls into three categories:

### Delivery guarantees
* **At-most-once:** Producer fires and forgets, or consumer commits offset before processing. Fast, but messages can be lost on crash.
* **At-least-once:** Producer retries until broker ACKs, and consumer commits offset only after processing finishes. No messages are lost, **but messages can be delivered more than once**.
* **Effectively-once:** Combine **at-least-once delivery** with an **idempotent consumer**.

### Designing an idempotent consumer
An operation is idempotent if applying it multiple times has the exact same effect as applying it once.

Because distributed queues almost always run in at-least-once mode, every state-changing consumer should be idempotent:
1. Producer attaches a deterministic or UUID `event_id` / `idempotency_key` to the message payload.
2. Consumer starts a local database transaction:
   * `INSERT INTO processed_events (event_id) VALUES (:id)` (with a `UNIQUE` constraint).
   * Apply the business state change (for example, credit account or update order status) in the same transaction.
3. If the unique constraint fails, the event was already processed, so the consumer skips the work and acknowledges the message.

## 5. Retries, exponential backoff, and dead letter queues (DLQ)

When a consumer fails to process a message (because a downstream API timed out or the payload hit a bug):

```text
Message ──> [ Primary Queue ] ──> Consumer (Fails)
                                      │
                                      ▼ (Exponential backoff + jitter: 1s, 2s, 4s, 8s)
                                 [ Retry Queue ]
                                      │ (Exceeds max_retries = 5)
                                      ▼
                           [ Dead Letter Queue (DLQ) ]
                                      │
                                      ▼
                         (Alert on-call / inspect & replay)
```

1. **Exponential backoff with jitter:** Wait $2^{\text{attempt}} + \text{random\_jitter}$ seconds between retries so recovering downstream services do not get hammered by synchronized retry waves.
2. **Dead letter queue (DLQ):** If a malformed message ("poison pill") fails after $N$ retries, move it to a separate DLQ and advance the consumer offset so one bad message does not block the entire partition behind it.
