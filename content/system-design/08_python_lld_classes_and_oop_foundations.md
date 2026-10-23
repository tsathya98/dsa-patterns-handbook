# Python LLD: Classes, OOP Foundations, and SOLID Principles

> **Reference Articles & Repositories:**
> - [Python LLD Interview: Classes - Building Blocks of Object-Oriented Power](https://medium.com/python-interview-preparation/python-lld-interview-classes-building-blocks-of-object-oriented-power-b019fd164886)
> - [GOAT Engineer: Low-Level Design in Python](https://github.com/abhaypaswan/lld-python)

Low-Level Design (LLD) and Machine Coding interviews evaluate whether you can translate ambiguous domain requirements into clean, modular, extensible, and testable code within 45 to 60 minutes.

In Python, writing good LLD code requires mastering Python-specific OOP building blocks: class vs instance attributes, method decorators (`@classmethod`, `@staticmethod`, `@property`), formal interfaces via Abstract Base Classes (`abc`), magic (dunder) methods, dataclasses, and SOLID principles.

---

## 1. Class vs. instance attributes (State management)

Confusion between class variables and instance variables is a frequent bug in LLD interviews:

```python
class ParkingSpot:
    # Class variable: shared across ALL parking spot instances
    total_spots_created = 0

    def __init__(self, spot_id: str, spot_type: str):
        # Instance variables: unique to THIS specific instance
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.vehicle = None
        ParkingSpot.total_spots_created += 1
```

### The mutable class variable trap
Never put mutable collections (lists, dicts, sets) at the class level unless intentionally designing a shared registry:

```python
# BUG: All accounts share the exact same transactions list in memory!
class BadAccount:
    transactions = []  # Shared across all instances!

# CORRECT: Initialize per-instance state inside __init__
class GoodAccount:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.transactions = []  # Unique to this account instance
```

---

## 2. The three method types

Python provides three distinct method types, each serving a specific architectural role in LLD:

| Method Type | Decorator | First Arg | Access Level | Primary LLD Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Instance method** | None | `self` | Instance and class state | Mutate state, execute domain actions (e.g. `park_vehicle()`, `dispense()`). |
| **Class method** | `@classmethod` | `cls` | Class state, no instance state | Factory constructors, parsing payloads, tracking global registries. |
| **Static method** | `@staticmethod` | None | No state access | Pure utility functions, domain validation rules, math formulas. |

### Concrete code example

```python
from datetime import datetime

class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: str):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.entry_time = datetime.now()

    # 1. Instance method: operates on this specific vehicle
    def calculate_duration_hours(self) -> float:
        delta = datetime.now() - self.entry_time
        return max(1.0, delta.total_seconds() / 3600.0)

    # 2. Class method: alternative constructor / factory method
    @classmethod
    def from_csv_line(cls, csv_line: str) -> "Vehicle":
        plate, vtype = csv_line.strip().split(",")
        return cls(license_plate=plate, vehicle_type=vtype)

    # 3. Static method: pure utility / validation check
    @staticmethod
    def is_valid_license_plate(plate: str) -> bool:
        return len(plate) >= 4 and plate.isalnum()
```

---

## 3. Encapsulation and `@property` accessors

Python does not have `private` keywords like Java or C++. Instead, it uses naming conventions and `@property` decorators:

* `variable`: Public attribute (accessible everywhere).
* `_variable`: Protected attribute (internal convention; please do not touch outside class or subclasses).
* `__variable`: Private attribute with name-mangling (Python renames it to `_ClassName__variable` to prevent accidental subclass collisions).

### Using `@property` for validation and invariants

```python
class BankAccount:
    def __init__(self, account_id: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self._balance = initial_balance

    @property
    def balance(self) -> float:
        """Getter: read-only access to balance."""
        return self._balance

    @balance.setter
    def balance(self, new_balance: float):
        """Setter: enforces domain invariants."""
        if new_balance < 0:
            raise ValueError("Balance cannot drop below zero")
        self._balance = new_balance
```

---

## 4. Abstract Base Classes (ABCs): defining contracts

In LLD, an interface defines a contract that multiple implementations must fulfill (Strategy pattern, Factory pattern, State pattern). Python's standard library provides the `abc` module:

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Abstract interface defining the payment contract."""

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Process the transaction. Must return True on success, False on failure."""
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Refund a previous transaction."""
        pass

class StripePaymentProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Charged ${amount:.2f} via Stripe API")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"Refunded transaction {transaction_id} via Stripe API")
        return True
```

If a subclass forgets to implement any `@abstractmethod`, Python raises `TypeError: Can't instantiate abstract class` at object creation time, catching design oversights immediately.

---

## 5. Dunder (Magic) methods that matter in LLD

Implementing these core magic methods makes your classes behave natively and cleanly in tests and logs:

| Dunder Method | Purpose | Why it matters in LLD interviews |
| :--- | :--- | :--- |
| `__repr__` | Unambiguous developer string representation | Debugging and logging state during test runs. |
| `__str__` | User-facing readable string | Clean console output for CLI demos. |
| `__eq__` | Equality comparison based on attributes | Asserting entity equality in pytest (`assert order1 == order2`). |
| `__hash__` | Hash computation | Allows using objects as keys in `dict` or elements in `set`. |
| `__len__` | Returns container length | Makes custom collections (e.g. `Deck`, `FileSystem`) work with `len()`. |

```python
class Item:
    def __init__(self, item_id: str, name: str, price_cents: int):
        self.item_id = item_id
        self.name = name
        self.price_cents = price_cents

    def __repr__(self) -> str:
        return f"Item(id={self.item_id!r}, name={self.name!r}, price={self.price_cents})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return False
        return self.item_id == other.item_id

    def __hash__(self) -> int:
        return hash(self.item_id)
```

---

## 6. Dataclasses: rapid domain modeling

In time-constrained 45-minute interviews, writing boilerplate `__init__`, `__repr__`, and `__eq__` by hand wastes 10 minutes. Python's `@dataclass` generates them automatically:

```python
from dataclasses import dataclass, field
from typing import List
from enum import Enum

class VehicleSize(Enum):
    MOTORCYCLE = 1
    COMPACT = 2
    LARGE = 3

@dataclass
class Ticket:
    ticket_id: str
    vehicle_plate: str
    spot_id: str
    issued_at: float
    paid: bool = False
    fee_cents: int = 0
```

---

## 7. SOLID principles in Python LLD

The 5 SOLID principles guide how you divide classes during machine coding:

### 1. Single Responsibility Principle (SRP)
* **Rule:** A class should have only one reason to change.
* **LLD Application:** In a Vending Machine, separate the `InventoryManager` (tracks item stock) from the `CashSlot` (validates coins/bills) and the `VendingStateMachine` (manages user state). Do not put all three in one mega-class.

### 2. Open / Closed Principle (OCP)
* **Rule:** Open for extension, closed for modification.
* **LLD Application:** Use the Strategy pattern. In a Parking Lot pricing engine, define `PricingStrategy(ABC)` with implementations `HourlyPricing`, `FlatRatePricing`, and `SurgePricing`. Adding a new discount strategy never touches existing pricing classes.

### 3. Liskov Substitution Principle (LSP)
* **Rule:** Subtypes must be substitutable for their base types without breaking caller expectations.
* **LLD Application:** If `Vehicle` defines `get_spot_size() -> VehicleSize`, every subclass (`Car`, `Truck`, `Motorcycle`) must return a valid `VehicleSize` without throwing unexpected errors or requiring `if isinstance(v, Truck):` checks in the parking manager.

### 4. Interface Segregation Principle (ISP)
* **Rule:** Clients should not be forced to depend on methods they do not use.
* **LLD Application:** Rather than creating one massive `SmartDevice(ABC)` with `print()`, `scan()`, `fax()`, split into smaller ABCs: `Printer(ABC)`, `Scanner(ABC)`. A basic inkjet implements only `Printer`.

### 5. Dependency Inversion Principle (DIP)
* **Rule:** High-level modules should depend on abstractions, not on concrete implementations.
* **LLD Application:** In a Notification Service, `NotificationService` depends on `NotificationSender(ABC)`, not directly on `TwilioSMSClient`. You inject `TwilioSMSClient` or `SendGridEmailClient` via the constructor (Dependency Injection).

---

## 8. Five-step LLD machine coding framework

Follow this strict step-by-step framework to complete any machine coding round within 45 minutes:

* **1. Clarify requirements & scope (5 min):** Confirm actors, primary use cases, edge cases, and in-memory vs persisted constraints.
* **2. Define core entities & enums (5 min):** List domain objects as dataclasses or standard classes (`User`, `Vehicle`, `Spot`, `State`).
* **3. Define interfaces & patterns (10 min):** Identify which design pattern handles the primary variation (State for lifecycle, Strategy for algorithms, Observer for notifications).
* **4. Implement core logic & demo runner (20 min):** Build out the manager/controller class and a runnable `main.py` demonstrating the happy path and edge cases.
* **5. Discuss follow-ups & concurrency (5 min):** Explain how you would add thread locks (`threading.Lock`), database transactions, or distributed caching.
