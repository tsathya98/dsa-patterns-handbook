# Low-Level Design & Design Patterns Cheat Sheet

> **Full Detailed Guides:**
> - [Python LLD: Classes, OOP Foundations, and SOLID](../system-design/08_python_lld_classes_and_oop_foundations.md)
> - [Python Design Patterns Reference Guide](../system-design/09_python_design_patterns_reference.md)
> - [17 Canonical LLD Problems Catalog](../system-design/10_low_level_design_problems_catalog.md)

---

## 1. Quick Decision Matrix: Which Pattern When?

| Symptom / Requirement in Interview | Recommended Pattern | Python Implementation Tip | Classic Interview Problem |
| :--- | :--- | :--- | :--- |
| Algorithm or formula changes based on type/config | **Strategy** | `ABC` with `@abstractmethod`, inject via constructor | Parking Lot Pricing, Rate Limiter |
| Method behavior changes based on object lifecycle mode | **State** | Replace `if state == ...` with State classes calling `context.set_state()` | Vending Machine, ATM, Elevator |
| One event triggers actions across multiple unknown services | **Observer** | Maintain `_observers: List[Observer]` with `attach()` and `notify()` | Notification Service, Splitwise |
| Need undo, redo, queued tasks, or operation logs | **Command** | Command class with `execute()` and `undo()` | Text Editor, Chess Engine |
| Request passes through a chain of rules or filters | **Chain of Responsibility** | Handler class with `self.next_handler` and `handle()` | Logging Framework, ATM Note Dispenser |
| External SDK or API has incompatible method names or formats | **Adapter** | Wrapper class inheriting your domain `ABC` and delegating to SDK | Payment Gateway (Stripe / PayPal) |
| Need cross-cutting concerns (retry, rate limit, logging) | **Decorator** | Wrap target class with identical interface, adding behavior | Notification Channel Retries |
| Complex multi-class subsystem needs a simple API | **Facade** | Unified orchestrator class exposing 3 to 5 high-level methods | Parking Lot Controller, In-Memory FS |
| Complex object with 5+ optional constructor parameters | **Builder** | Builder class with fluent chaining `with_x()` returning `self` | Movie Ticket Booking, Order Creation |
| Need to instantiate subclasses without hardcoding classes | **Factory Method** | Static or class method returning instance based on input type | Vehicle Factory, Notification Sender Factory |

---

## 2. Python OOP Interview Essentials

### Method Types Cheat Sheet
* **Instance method (`def func(self):`)**: Operates on specific instance data. Use for core entity behavior.
* **Class method (`@classmethod def from_x(cls):`)**: Alternative constructor or class-level registry tracker.
* **Static method (`@staticmethod def validate():`)**: Pure utility function; does not touch instance or class state.

### Property Accessor Template
```python
class Account:
    def __init__(self, balance: float):
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
```

### Abstract Base Class (ABC) Contract Template
```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: int) -> bool:
        pass
```

---

## 3. SOLID Principles in 10 Seconds

* **S (Single Responsibility):** 1 class = 1 job. Don't mix inventory, payment, and UI in one class.
* **O (Open / Closed):** Add new features by adding new classes (Strategy), never by editing existing tested logic.
* **L (Liskov Substitution):** Subclasses must fulfill base class contracts without raising unexpected exceptions.
* **I (Interface Segregation):** Small, focused interfaces are better than one fat interface with unused methods.
* **D (Dependency Inversion):** High-level services depend on abstractions (`ABC`), not concrete vendor SDKs.

---

## 4. Top 17 Problems Quick Map

| Category | Canonical Problems | Target Time | Primary Patterns |
| :--- | :--- | :--- | :--- |
| **Games** | Tic Tac Toe, Snake and Ladder, Chess | 40 to 90 min | Strategy, Observer, Command |
| **Hardware & Devices** | Vending Machine, ATM, Elevator System | 50 to 75 min | State, Chain of Responsibility, Strategy |
| **E-Commerce & Booking** | Movie Ticket Booking, Payment Gateway, Parking Lot | 60 to 80 min | Builder, Adapter, Facade, Strategy |
| **Developer Tools** | Logging Framework, Rate Limiter, In-Memory File System, LRU Cache, Text Editor | 45 to 55 min | Chain of Responsibility, Composite, Strategy, Command |
| **Fintech & Collaboration** | Splitwise, Chat Room, Notification Service | 50 to 60 min | Observer, Mediator, Decorator, Strategy |
