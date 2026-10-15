# 🏗️ System Design Foundations: Production Infrastructure & Protocols

> **Reference Source:** [Hayk Simonyan – System Design Explained (APIs, Databases, Caching, Load Balancing & Production Infra)](https://www.youtube.com/watch?v=oYxTTirKY8M)  
> **Target:** FAANG System Design Interview Foundations  
> **Key Focus:** Architectural trade-offs, scalability patterns, communication protocols, and security.

---

## 🧭 System Evolution: From 1 User to 10 Million Users

Every scalable system in production evolves across 4 standard architectural phases:

```text
Phase 1: Monolithic Single Box          Phase 2: Decoupled Database
┌─────────────────────────┐             ┌──────────────┐      ┌──────────────┐
│  Client ──> [ App + DB ]│             │ App Server   │ ───> │ Database (DB)│
└─────────────────────────┘             └──────────────┘      └──────────────┘
(Fails: CPU/RAM contention, SPOF)        (Better: Independent resource scaling)

Phase 3: Horizontally Scaled Stateless Tier
                  ┌───> [ App Server 1 ] ──┐
[ Client ] ──> [ LB ] ─┼───> [ App Server 2 ] ──┼───> [ Primary DB ] (Writes)
                  └───> [ App Server 3 ] ──┘         │ (Replication)
                                                     ▼
                                              [ Read Replicas ] (Reads)

Phase 4: Full Production Enterprise Infrastructure
[ Client ] ──> [ DNS / Route 53 ]
                   │
                   ▼
             [ CDN / Edge ] ── (Static Assets / Cached Reads)
                   │
                   ▼
        [ API Gateway / Reverse Proxy ] ── (SSL Termination, Rate Limiting, Auth)
                   │
                   ▼
          [ Layer 7 Load Balancer ]
          ┌────────┴────────┐
          ▼                 ▼
   [ Web Service A ]  [ Web Service B ]
          │                 │
     (Sub-ms Read)     (Async Event)
          ▼                 ▼
   [ Redis Cache ]    [ Message Queue / Kafka ]
          │                 │
          ▼                 ▼
   [ Primary DB (SQL) ] [ Async Background Workers ]
          │
     (Replication)
          ▼
   [ Read Replicas ] + [ Analytical DB / Data Warehouse ]
```

---

## 🗄️ 1. Databases: The Core Storage Paradigms

Never say "I will just use a database." FAANG interviewers test whether you can justify **which** database fits the access pattern:

| Database Type | Core Tech Examples | Ideal Access Pattern & Use Cases | Trade-offs & Limitations |
| :--- | :--- | :--- | :--- |
| **Relational (SQL)** | PostgreSQL, MySQL | Strong ACID transactions, relational joins, financial/payment data, ecommerce orders. | Hard to shard horizontally across nodes; distributed joins are slow. |
| **Document (NoSQL)** | MongoDB, DynamoDB | Nested semi-structured data, rapid prototyping, catalog management, user profiles. | Weaker transactional guarantees across documents; data duplication. |
| **Key-Value** | Redis, Memcached | Ultra-low latency (<1 ms) lookups by key, session storage, rate limiting, leaderboards. | Limited query capabilities (cannot easily query by value or range). |
| **Wide-Column** | Apache Cassandra, ScyllaDB | Heavy write throughput, time-series events, sensor/IoT logs, massive petabyte scale. | Eventual consistency; complex data modeling; no joins. |
| **Graph** | Neo4j, AWS Neptune | Complex interconnected relationships, social friend graphs, fraud detection networks. | Difficult to partition across clusters; niche query syntax (Cypher). |

---

## ⚖️ 2. Scaling: Vertical vs. Horizontal

```text
Vertical Scaling (Scale UP):             Horizontal Scaling (Scale OUT):
┌───────────┐     ┌───────────────┐     ┌─────────┐   ┌─────────┐   ┌─────────┐
│ Small Box │ ──> │ Monster EC2   │     │ Node 1  │ + │ Node 2  │ + │ Node 3  │
│ 4 vCPU    │     │ 128 vCPU/4TB  │     └─────────┘   └─────────┘   └─────────┘
└───────────┘     └───────────────┘     (Behind a Load Balancer)
```

- **Vertical Scaling (Scale Up):**
  - **Pros:** Zero architectural changes, no distributed network latency, single point of configuration.
  - **Cons:** Hard physical hardware ceiling; cost curve grows exponentially; guaranteed downtime/SPOF.
- **Horizontal Scaling (Scale Out):**
  - **Pros:** Virtually infinite elasticity; high availability (if one node dies, others handle traffic); cost-efficient commodity hardware.
  - **Cons:** Requires **stateless application servers** (sessions stored in Redis/DB, not in local memory); distributed consensus overhead.

---

## 🔀 3. Load Balancing & Traffic Routing

A Load Balancer distributes incoming network traffic across multiple healthy backend servers.

### L4 vs. L7 Load Balancing:
* **Layer 4 (Transport Layer - TCP/UDP):**
  * Routes traffic purely based on IP address and Port (e.g., AWS NLB).
  * Does **not** inspect HTTP packet contents.
  * **Ultra-fast & lightweight**, handles millions of requests/sec with minimal CPU overhead.
* **Layer 7 (Application Layer - HTTP/HTTPS):**
  * Inspects URLs, HTTP headers, paths, and cookies (e.g., AWS ALB, NGINX, HAProxy).
  * Enables **smart routing**:
    * `/api/v1/users` $\to$ User Service.
    * `/api/v1/video` $\to$ Streaming Service.
  * Handles SSL/TLS Termination and header injection.

### Load Balancing Routing Algorithms:
1. **Round Robin:** Equal distribution in sequential order. (Assumes all servers have equal capacity).
2. **Weighted Round Robin:** Sends more requests to servers with higher CPU/memory specs.
3. **Least Connections:** Sends traffic to the server currently handling the fewest active connections. (Best for long-lived sessions).
4. **Least Response Time:** Routes to the server with the lowest latency and fewest connections.
5. **IP Hash / Consistent Hashing:** Hashes client IP to ensure the same client always reaches the same server (session affinity / sticky sessions).

### Health Checks & Eliminating SPOF:
* **Active Health Checks:** Load balancer sends periodic heartbeat probes (e.g., `GET /healthz` every 5 seconds). If a server fails 3 consecutive checks, it is evicted from the rotation.
* **Passive Health Checks:** Load balancer detects connection drops on real client requests and temporarily pauses routing to that node.
* **Eliminating the LB as a SPOF:** Use **Active-Passive Load Balancers** with floating Virtual IP (VIP) via VRRP / Keepalived, or **Active-Active** using DNS Anycast.

---

## 🌐 4. Networking & Protocols

### Transport Layer: TCP vs. UDP
```text
TCP: 3-Way Handshake (Reliable, Ordered)     UDP: Fire & Forget (Fast, Unchecked)
Client              Server                  Client              Server
  │─── SYN ──────────>│                       │─── Datagram 1 ───>│
  │<── SYN-ACK ───────│                       │─── Datagram 2 ───>│ (Lost in transit!)
  │─── ACK ──────────>│                       │─── Datagram 3 ───>│
  │─── Data Stream ──>│
```

* **TCP (Transmission Control Protocol):**
  * Guarantees delivery, packet ordering, and error-checking via ACK packets and retransmissions.
  * Includes congestion control and flow control.
  * *Used for:* HTTP/HTTPS, Web, Database connections, File transfers (SSH, FTP), Email (SMTP).
* **UDP (User Datagram Protocol):**
  * Connectionless, lightweight, zero handshake latency. No retransmissions if packets drop.
  * *Used for:* Live video streaming (WebRTC), online multiplayer gaming, DNS lookups, VoIP.

---

## 🔌 5. API Paradigms: REST vs. GraphQL vs. gRPC

| Feature | REST | GraphQL | gRPC |
| :--- | :--- | :--- | :--- |
| **Protocol / Transport** | HTTP 1.1 / HTTP 2 | HTTP 1.1 / HTTP 2 | HTTP 2 (Multiplexing) |
| **Payload Format** | JSON, XML | JSON | Protocol Buffers (Binary) |
| **Schema & Typing** | Optional (OpenAPI/Swagger) | Strict Schema Definition (SDL) | Strict (`.proto` files) |
| **Data Fetching** | Fixed endpoints per resource. Risks **over-fetching** or **under-fetching**. | Client queries **exact** fields needed in 1 request. | Remote method invocation; compact binary streams. |
| **Caching** | Native HTTP caching (ETags, CDN, `Cache-Control`). | Difficult at CDN layer (uses single `POST /graphql`). | Handled at application layer. |
| **Best Used For** | Public-facing APIs, standard web applications. | Complex frontends with varied mobile/web UI data needs. | High-throughput internal **microservice-to-microservice** communication. |

---

## ⚡ 6. Real-Time Communication Patterns

When the server needs to push updates to the client:

```text
Short Polling:          Long Polling:           Server-Sent Events:     WebSockets:
(Repeated Pings)        (Held Connection)       (Unidirectional Stream) (Full-Duplex Pipe)

Client   Server         Client   Server         Client   Server         Client   Server
  │─Data?─>│              │─Data?─>│              │──Connect─>│           │<═ Handshake ═>│
  │<─No────│              │   :    │              │<─Event 1──│           │<══ Msg A ════>│
  │        │ (wait)       │ (wait) │              │<─Event 2──│           │<══ Msg B ════>│
  │─Data?─>│              │   :    │              │<─Event 3──│           │<══ Msg C ════>│
  │<─Yes───│              │<─Data──│              (HTTP Stream)           (Bidirectional)
```

1. **Short Polling:** Client fires requests every $N$ seconds. Wasteful of bandwidth and CPU.
2. **Long Polling:** Server holds request open until new data is available. Re-establishes connection after every response.
3. **Server-Sent Events (SSE):** Persistent unidirectional connection (Server $\to$ Client) over standard HTTP. Ideal for live stock tickers, system alerts, and AI streaming responses (e.g. ChatGPT tokens).
4. **WebSockets:** Persistent, bidirectional full-duplex TCP connection. Low framing overhead (2 bytes). Ideal for chat applications, multiplayer games, and collaborative whiteboards.

---

## 🔐 7. Authentication & Authorization

### Authentication (AuthN: "Who are you?")
* **Session-Based Authentication (Stateful):**
  * User logs in $\to$ Server creates a session in memory/Redis and returns a `Set-Cookie: session_id=xyz`.
  * *Pros:* Easy to instantly invalidate/revoke sessions.
  * *Cons:* Requires central shared cache (Redis) as server fleet scales horizontally.
* **Token-Based Authentication / JWT (Stateless):**
  * Server signs a JSON Web Token (`Header.Payload.Signature`) using a secret key (HMAC) or private key (RSA).
  * Client sends token in `Authorization: Bearer <token>`.
  * *Pros:* Zero database lookups for verification; perfectly horizontally scalable.
  * *Cons:* Cannot be revoked before expiry without maintaining a centralized token denylist.
* **OAuth 2.0 & OpenID Connect (OIDC):**
  * Delegated identity standard ("Log in with Google / GitHub"). Allows third-party apps to access resources without exposing passwords.

### Authorization (AuthZ: "What are you allowed to do?")
* **RBAC (Role-Based Access Control):** Permissions assigned to roles (Admin, Editor, Viewer). Simple, predictable.
* **ABAC (Attribute-Based Access Control):** Evaluates attributes of the user, resource, action, and environment (e.g. *"Allow access IF user department == 'Finance' AND time < 6 PM AND IP is inside VPN"*).

---

## 🛡️ 8. Production Security & Edge Defence

* **TLS / HTTPS:** Encrypts data in transit. Asymmetric cryptography (RSA/ECDSA) establishes shared symmetric session keys (AES).
* **Rate Limiting:** Protects against brute-force attacks and noisy neighbors. Implemented via Token Bucket or Sliding Window algorithms at the API Gateway / Cloudflare layer.
* **CORS (Cross-Origin Resource Sharing):** Browser enforcement mechanism preventing malicious scripts on one origin from accessing APIs on another without explicit `Access-Control-Allow-Origin` headers.
* **CSRF (Cross-Site Request Forgery):** Attacker tricks a victim into executing unwanted actions on an authenticated app. Mitigated by `SameSite=Lax/Strict` cookie attributes and Anti-CSRF verification tokens.
* **DDoS Mitigation:** Absorbed at the edge using Anycast networks (Cloudflare, AWS Shield), CDN caching, SYN cookies, and scrubbing centers.
