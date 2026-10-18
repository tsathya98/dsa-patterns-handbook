# Low-Level Design (LLD) Problems Catalog

> **Source Repository & Test Suites:** [GOAT Engineer: Low-Level Design in Python](https://github.com/abhaypaswan/lld-python)

In top-tier engineering interviews (Google, Meta, Uber, Stripe, Amazon), Low-Level Design (LLD) and Machine Coding rounds test whether you can design, structure, and implement a production-grade object-oriented application within 45 to 60 minutes.

Below is the canonical catalog of 17 standard LLD problems, indexed by difficulty, core design patterns, and typical interview time targets.

---

## The 17 Canonical LLD Problems

| # | Problem | Difficulty | Design Patterns Used | Target Time | Core Engineering Focus |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Design Tic Tac Toe** | 🟢 Easy | Strategy, Observer | 40 min | $O(1)$ win detection via line counters instead of matrix scans; bot difficulty strategy. |
| **2** | **Snake and Ladder** | 🟢 Easy | Strategy | 45 min | Turn-based state transitions; pluggable fair vs crooked dice; preventing snake loops. |
| **3** | **Design Splitwise** | 🟡 Medium | Strategy, Observer | 60 min | Exact cent-precision arithmetic; 4 split strategies (Equal, Exact, Percentage, Share); group balance minimization. |
| **4** | **Design a Chat Room** | 🟡 Medium | Mediator, Observer, Facade | 50 min | Decoupling peer-to-peer messaging via a central hub; presence tracking and message histories. |
| **5** | **Design a Logging Framework** | 🟡 Medium | Chain of Responsibility, Strategy, Singleton | 45 min | Multi-target log dispatching where handlers do not short-circuit; level filtering. |
| **6** | **Design a Notification Service** | 🟡 Medium | Decorator, Observer, Factory Method, Strategy | 55 min | Channel fanning (Email, SMS, Push, Slack); composable retry, rate limit, and deduplication decorators. |
| **7** | **Design a Parking Lot** | 🟡 Medium | Strategy, Factory Method, Command, Facade | 60 min | Pluggable spot allocation and pricing strategies; vehicle size matching; clean CLI console. |
| **8** | **Design a Rate Limiter** | 🟡 Medium | Strategy | 50 min | Token Bucket, Fixed Window, Sliding Window Log, and Sliding Window Counter implementations. |
| **9** | **Design a Text Editor with Undo** | 🟡 Medium | Command, Memento, Composite, Facade | 55 min | Reversible edits via command pattern with undo/redo stacks; gap buffer or piece table. |
| **10** | **Design a Vending Machine** | 🟡 Medium | State | 50 min | Explicit state transitions (`Idle`, `HasMoney`, `Dispensing`, `SoldOut`); atomic money and change invariant. |
| **11** | **Design an ATM** | 🟡 Medium | State, Chain of Responsibility | 60 min | State-guarded card and PIN workflows; denomination chain note dispenser planning before payout. |
| **12** | **Design an In-Memory File System** | 🟡 Medium | Composite, Visitor, Iterator, Facade | 55 min | Tree hierarchy for files and directories; operations (search, disk usage) via visitors without bloating nodes. |
| **13** | **Design an LRU Cache** | 🟡 Medium | Strategy, Template Method | 45 min | $\mathcal{O}(1)$ get and put via hash map + doubly linked list; swappable eviction policies (LRU, LFU, FIFO). |
| **14** | **Design Chess** | 🔴 Hard | Strategy, Command, Template Method, Observer | 90 min | Move validation per piece; undoable move commands; check and checkmate detection via temporary state evaluation. |
| **15** | **Design a Movie Ticket Booking System** | 🔴 Hard | Builder, Repository, Proxy, Strategy, Facade | 80 min | Preventing double booking via expiring seat locks; caching proxies; clean booking builders. |
| **16** | **Design a Payment Gateway** | 🔴 Hard | Adapter, Abstract Factory, Strategy, Facade | 70 min | Incompatible bank SDK adapters; regional abstract factories; idempotent transaction tracking. |
| **17** | **Design an Elevator System** | 🔴 Hard | Strategy, State, Observer | 75 min | Bank of elevator cars running the LOOK algorithm; optimal car dispatching strategy; door and motion state machine. |

---

## Blueprints for the Top 5 Interview Questions

### 1. Design a Parking Lot

#### Requirements
* Multi-floor parking garage supporting Motorcycles, Cars, and Buses.
* Spot types: Compact, Large, Handicapped, Electric.
* Spot allocation strategy: Nearest to entrance, or Random.
* Fee calculation: Hourly rate with different multipliers per vehicle size.

#### Core Entity Hierarchy
* `Vehicle(ABC)` -> `Motorcycle`, `Car`, `Bus`
* `ParkingSpot(ABC)` -> `CompactSpot`, `LargeSpot`, `HandicappedSpot`
* `ParkingFloor`: Manages a list of spots and spot status.
* `ParkingLot`: Singleton or Facade orchestrating floors, ticket issuance, and departures.
* `AllocationStrategy(ABC)` -> `NearestFirstStrategy`, `RandomStrategy`
* `PricingStrategy(ABC)` -> `HourlyPricingStrategy`, `FlatRateStrategy`

#### Key Invariant
* A large vehicle (like a Bus) can only fit in a Large spot or multiple adjacent spots. A Car can fit in Compact or Large spots.

---

### 2. Design a Vending Machine

#### Requirements
* Accepts coins and bills of standard denominations.
* User selects an item code. If balance is sufficient, dispenses item and returns change.
* If user cancels, refunds the inserted amount.
* Machine must not dispense if it cannot provide exact change.

#### State Machine Diagram
```text
           ┌──────────────────────┐
           │      IdleState       │
           └──────────┬───────────┘
                      │ insert_money()
                      ▼
           ┌──────────────────────┐
           │    HasMoneyState     │
           └────┬────────────┬────┘
cancel() / refund │            │ select_item() [valid & paid]
                  ▼            ▼
           ┌──────────┐  ┌──────────────────────┐
           │  Idle    │  │   DispensingState    │
           └──────────┘  └──────────┬───────────┘
                                    │ dispense_complete()
                                    ▼
                         [ Return Change & Go to Idle ]
```

#### Key Invariant
* Money transaction atomicity: Never deduct inventory until payment is completely confirmed, and never accept payment if change cannot be made.

---

### 3. Design Splitwise

#### Requirements
* Users can create shared expenses within groups or directly between friends.
* Four split types supported:
  * **Equal:** Split evenly among $n$ participants.
  * **Exact:** Specific monetary amounts per participant (must sum to total).
  * **Percent:** Specific percentage per participant (must sum to 100%).
  * **Shares:** Ratio-based division.
* Balance simplification: Minimize the total number of transactions required to settle up all group debts.

#### Algorithm Steps for Balance Simplification:
* **1. Calculate net balances:** For each participant, compute `net = total_paid - total_owed`.
* **2. Separate debtors and creditors:** Group people into `debtors` (`net < 0`) and `creditors` (`net > 0`).
* **3. Greedy settlement:** Match the largest debtor with the largest creditor. Transfer the minimum of `abs(debt)` and `credit`. Update both balances.
* **4. Repeat until settled:** At most $n - 1$ payments will fully resolve all group debts.

---

### 4. Design a Rate Limiter

#### Requirements
* Reject client requests that exceed a specified threshold within a time window (e.g. 100 requests per minute per API key).
* Support pluggable rate-limiting algorithms.

#### Algorithm Comparison
* **Token Bucket:** Refills tokens at a constant rate up to bucket capacity. Handles bursts smoothly; memory is $\mathcal{O}(1)$ per user.
* **Fixed Window Counter:** Divides time into fixed windows. Suffers from the boundary burst problem (can receive $2\times$ limit around window borders).
* **Sliding Window Log:** Stores exact timestamp of every request in a deque. Perfectly accurate, but uses $\mathcal{O}(k)$ memory per user where $k$ is request count.
* **Sliding Window Counter:** Approximates sliding window by weighting the count of the previous window with the elapsed percentage of the current window. Low memory and smooth boundary handling.

---

### 5. Design a Movie Ticket Booking System

#### Requirements
* Users browse movies, cinemas, shows, and select specific seats.
* Temporary seat hold: Once a user selects a seat, hold it exclusively for 10 minutes while payment completes.
* Prevent double-booking under high concurrent load.

#### Concurrency & Locking Strategy
* **Optimistic locking:** Use a version number on the `Seat` entity. Fails fast if another transaction updated the seat version concurrently.
* **Pessimistic locking / Expiring Redis locks:** Acquire a timed distributed lock on `lock:show:{show_id}:seat:{seat_id}` with a 10-minute TTL. Release explicitly upon booking completion or let it expire on abandonment.

---

## 45-Minute Machine Coding Blueprint

When an interviewer presents an LLD prompt, execute according to this exact timeline:

* **00:00 to 05:00 (Clarify & Scope):** Write down assumptions in comments. List in-scope vs out-of-scope features. Define core user operations.
* **05:00 to 12:00 (Domain Entities & Enums):** Define data models and enums using Python `@dataclass`. Ensure attributes have clear types.
* **12:00 to 20:00 (Interfaces & Patterns):** Define the Abstract Base Classes (`abc.ABC`) for the main variation point (Strategy, State, or Factory).
* **20:00 to 35:00 (Core Service & Logic):** Implement the orchestrating service/facade and write the primary business workflows.
* **35:00 to 42:00 (Runnable Demo / Tests):** Create a clean `if __name__ == '__main__':` block demonstrating the happy path, edge cases, and error handling.
* **42:00 to 45:00 (Follow-ups & Concurrency):** Discuss thread safety (`threading.Lock`), persistence layers, and horizontal scalability.
