# ⚡ System Design Fundamentals – 60-Second Cheat Sheet

> **Quick Reference:** Core architectural components, 3-second triggers, and interview trade-offs.

---

## ⚡ 1. The 3-Second Technology Decision Table

| When You Need To... | Choose This | Why? (The Interview Justification) |
| :--- | :--- | :--- |
| **Store relational / ACID financial data** | **PostgreSQL / MySQL** | Strong transactional integrity, foreign key constraints, schema validation. |
| **Cache hot data / sub-millisecond reads** | **Redis** | In-memory key-value data structure store, atomic operations, TTL eviction. |
| **Handle massive write-heavy timeseries/logs** | **Apache Cassandra / ScyllaDB** | Masterless architecture, append-only commit logs, horizontal partition scaling. |
| **Model complex connections (friends, fraud)** | **Neo4j** | Graph traversal avoids expensive multi-table recursive relational joins. |
| **Route traffic by HTTP path (`/api/users`)** | **Layer 7 Load Balancer (ALB)** | Application-aware, inspects HTTP headers, cookies, URL paths, terminates SSL. |
| **Route high-throughput raw TCP/UDP streams** | **Layer 4 Load Balancer (NLB)** | Packet-level routing by IP & Port, ultra-low latency, handles millions of QPS. |
| **Stream LLM tokens or real-time stock alerts** | **Server-Sent Events (SSE)** | Unidirectional server $\to$ client over HTTP, automatic browser reconnection. |
| **Real-time 2-way chat or multiplayer gaming** | **WebSockets** | Full-duplex persistent bidirectional TCP pipe, minimal 2-byte frame overhead. |
| **Internal service-to-service RPC calls** | **gRPC (Protobuf)** | Compact binary serialization, multiplexed over HTTP/2, auto-generated SDKs. |
| **Public-facing web/mobile client API** | **REST or GraphQL** | REST for simple cacheable resources; GraphQL when mobile UI needs flexible queries without over-fetching. |
| **Stateless cross-service authentication** | **JWT (JSON Web Tokens)** | Self-contained, cryptographic signature verification without DB lookups. |
| **Instant session revocation (banking logout)** | **Redis-backed Sessions** | Server stores state; deleting session key from Redis instantly terminates access. |

---

## 📊 2. Network Protocols Comparison

```text
Latency / Overhead:    UDP  <  TCP  <  HTTP/1.1  <  HTTP/2  <  HTTP/3 (QUIC)
Reliability:           UDP: Low (lossy)  |  TCP / HTTP: High (guaranteed delivery)
```

* **TCP:** 3-way handshake (`SYN` $\to$ `SYN-ACK` $\to$ `ACK`), in-order delivery, flow & congestion control.
* **UDP:** No handshake, fire-and-forget, zero connection state. Drops packets gracefully.
* **HTTP/1.1:** One request per TCP connection at a time (head-of-line blocking).
* **HTTP/2:** Multiplexes multiple requests/responses over a single TCP connection; binary framing.
* **HTTP/3:** Uses QUIC protocol over UDP; eliminates TCP head-of-line blocking across lost packets.

---

## 🛡️ 3. High Availability & Reliability Checklist

- [ ] **No SPOF (Single Point of Failure):** Every component has a redundant active/passive backup.
- [ ] **Stateless App Tier:** Servers store zero local state; sessions live in Redis, file uploads go to S3.
- [ ] **Database Read/Write Split:** Writes go to Primary (Leader); reads distributed across Read Replicas.
- [ ] **Multi-AZ Deployment:** Nodes spread across multiple availability zones in case a data center loses power.
- [ ] **Rate Limiting at Edge:** Shield backends from DDoS and abusive scraping via Token Bucket algorithms.
- [ ] **Graceful Degradation / Circuit Breaker:** If downstream microservice fails, return cached or fallback response instead of crashing.
