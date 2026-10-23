# Python Design Patterns for Low-Level Design (LLD)

> **Source & Worked Implementations:** [GOAT Engineer: Low-Level Design in Python](https://github.com/abhaypaswan/lld-python)

Design patterns are reusable architectural shapes that solve recurring object-oriented problems. In LLD and machine coding interviews, using the right pattern demonstrates clean architectural thinking, eliminates monolithic `if/elif` chains, and makes systems testable and extensible.

Below are the core design patterns categorized by Creational, Structural, and Behavioral types, with Python implementations, selection triggers, and interview mistakes to avoid.

---

## I. Behavioral patterns (The core of LLD interviews)

Behavioral patterns represent over 70% of pattern choices in machine coding rounds because real-world systems center on workflows, lifecycles, and event reactions.

### 1. Strategy pattern
Make an algorithm interchangeable behind a shared interface.

* **Reach for it when:** There is more than one reasonable way to execute a calculation or algorithm, chosen at runtime or configuration time rather than hardcoded in an `if/elif` cascade.
* **The usual mistake:** Evaluating an `if/else` inside every method call. A true Strategy is selected once and injected into the client class via constructor or setter.
* **Canonical interview problems:**
  * **Parking Lot:** Spot allocation strategy (Nearest, Random, Best-Fit) and pricing strategy (Hourly, Flat, Surge).
  * **Rate Limiter:** Token Bucket, Fixed Window, Sliding Window Log, Sliding Window Counter.
  * **Tic Tac Toe:** Bot move strategy (Random, Minimax).

```python
from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, hours: float) -> float:
        pass

class HourlyPricingStrategy(PricingStrategy):
    def __init__(self, hourly_rate: float):
        self.hourly_rate = hourly_rate

    def calculate_fee(self, hours: float) -> float:
        return hours * self.hourly_rate

class SurgePricingStrategy(PricingStrategy):
    def __init__(self, base_rate: float, multiplier: float):
        self.base_rate = base_rate
        self.multiplier = multiplier

    def calculate_fee(self, hours: float) -> float:
        return hours * self.base_rate * self.multiplier

# Usage via Dependency Injection:
class ParkingGarage:
    def __init__(self, pricing_strategy: PricingStrategy):
        self.pricing_strategy = pricing_strategy

    def exit_vehicle(self, hours: float) -> float:
        return self.pricing_strategy.calculate_fee(hours)
```

---

### 2. State pattern
Put state-specific behavior into dedicated state classes so transitions replace massive conditional logic.

* **Reach for it when:** The same method must perform completely different actions (or be explicitly rejected) depending on the object's current lifecycle state.
* **The usual mistake:** Keeping state as a string or enum flag checked at the top of every method with `if self.state == State.WAITING_FOR_MONEY:`. Adding a new state forces you to edit every existing method.
* **Canonical interview problems:**
  * **Vending Machine:** `IdleState`, `HasMoneyState`, `DispensingState`, `SoldOutState`.
  * **ATM:** `NoCardState`, `CardInsertedState`, `PinVerifiedState`, `DispensingCashState`.
  * **Elevator System:** `IdleState`, `MovingUpState`, `MovingDownState`, `MaintenanceState`.

```python
from abc import ABC, abstractmethod

class VendingMachineState(ABC):
    @abstractmethod
    def insert_money(self, context: "VendingMachine", amount: int):
        pass

    @abstractmethod
    def select_item(self, context: "VendingMachine", code: str):
        pass

    @abstractmethod
    def dispense(self, context: "VendingMachine"):
        pass

class IdleState(VendingMachineState):
    def insert_money(self, context: "VendingMachine", amount: int):
        context.collected_cents += amount
        print(f"Collected {amount} cents. Transitioning to HasMoneyState.")
        context.set_state(context.has_money_state)

    def select_item(self, context: "VendingMachine", code: str):
        print("Please insert money before selecting an item.")

    def dispense(self, context: "VendingMachine"):
        print("Cannot dispense without money and item selection.")

class VendingMachine:
    def __init__(self):
        self.collected_cents = 0
        self.idle_state = IdleState()
        # Initialize other states...
        self.current_state: VendingMachineState = self.idle_state

    def set_state(self, state: VendingMachineState):
        self.current_state = state

    def insert_money(self, amount: int):
        self.current_state.insert_money(self, amount)
```

---

### 3. Observer pattern
Define a one-to-many subscription model so multiple objects automatically receive updates when state changes.

* **Reach for it when:** State changes in one object require updates across an unknown or extensible list of other objects without tight coupling.
* **The usual mistake:** Hardcoding direct method calls on dependent services inside the subject class.
* **Canonical interview problems:**
  * **Notification Service:** Broadcasting alerts across Email, SMS, Slack, and Mobile Push.
  * **Splitwise:** Notifying group members when an expense is logged or balances settle.
  * **Chat Room:** Broadcasting messages to connected clients in a channel.

```python
from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: dict):
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(event_type, data)
```

---

### 4. Command pattern
Encapsulate a request as a standalone object, enabling parameterized actions, operation queues, and undo/redo capabilities.

* **Reach for it when:** You need to queue operations, log audit trails, delay execution, or provide reversible actions (undo/redo).
* **The usual mistake:** Storing only raw data payloads in an undo stack rather than fully executable command objects with their own `execute()` and `undo()` methods.
* **Canonical interview problems:**
  * **Text Editor:** `InsertTextCommand`, `DeleteTextCommand` with full undo stack.
  * **Chess Engine:** Move execution where every move command can be undone to support search backtracking.
  * **Parking Lot Console:** Pluggable CLI commands (`ParkCommand`, `ExitCommand`, `StatusCommand`).

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class InsertTextCommand(Command):
    def __init__(self, editor: "TextEditor", text: str):
        self.editor = editor
        self.text = text
        self.position = len(editor.content)

    def execute(self):
        self.editor.insert_at(self.position, self.text)

    def undo(self):
        self.editor.delete_range(self.position, len(self.text))
```

---

### 5. Chain of Responsibility
Pass a request along a sequence of potential handlers until handled, or allow every handler to inspect and process it.

* **Reach for it when:** Multiple handlers could process a request, and you want to decouple the sender from the specific handler order.
* **The usual mistake:** Forcing the chain to stop at the first handler when the problem domain requires all handlers to process (such as multi-target logging or validation rules).
* **Canonical interview problems:**
  * **Logging Framework:** Chain of handlers (DebugHandler -> InfoHandler -> ErrorHandler -> FileHandler).
  * **ATM Cash Dispenser:** Dispenser chain for denominations ($100 note handler -> $50 note handler -> $20 note handler).

```python
from abc import ABC, abstractmethod
from typing import Optional

class CashDispenser(ABC):
    def __init__(self, denomination: int):
        self.denomination = denomination
        self.next_dispenser: Optional["CashDispenser"] = None

    def set_next(self, next_dispenser: "CashDispenser") -> "CashDispenser":
        self.next_dispenser = next_dispenser
        return next_dispenser

    def dispense(self, amount: int):
        notes = amount // self.denomination
        remainder = amount % self.denomination
        if notes > 0:
            print(f"Dispensing {notes} x ${self.denomination} note(s)")
        if remainder > 0 and self.next_dispenser:
            self.next_dispenser.dispense(remainder)
        elif remainder > 0:
            raise ValueError(f"Cannot dispense remaining amount: ${remainder}")
```

---

## II. Creational patterns

Creational patterns abstract the instantiation process, making systems independent of how their objects are created, composed, and represented.

### 6. Factory Method and Abstract Factory
* **Factory Method:** Lets subclasses decide which class to instantiate. Use when a class cannot anticipate the class of objects it must create (e.g. `VehicleFactory.create_vehicle("car")`).
* **Abstract Factory:** Creates families of related objects without specifying concrete classes.
* **Canonical interview problems:**
  * **Payment Gateway:** Regional factories producing consistent payment processors, tax rules, and receipt generators (`USPaymentFactory`, `EUPaymentFactory`).
  * **Notification Service:** Factory producing channel senders based on subscriber preferences.

### 7. Builder pattern
Separate the construction of a complex object from its representation, allowing the same construction process to create different representations.

* **Reach for it when:** An object requires many constructor parameters, many of which are optional or have sensible defaults. Prevents telescoping constructor anti-patterns.
* **Canonical interview problems:**
  * **Movie Ticket Booking:** Constructing complex `Booking` objects with seat selection, meal add-ons, promo codes, and payment options.

```python
class BookingBuilder:
    def __init__(self, user_id: str, show_id: str):
        self.user_id = user_id
        self.show_id = show_id
        self.seats = []
        self.promo_code = None
        self.meals = []

    def with_seats(self, seats: list) -> "BookingBuilder":
        self.seats = seats
        return self

    def with_promo(self, code: str) -> "BookingBuilder":
        self.promo_code = code
        return self

    def build(self) -> "Booking":
        if not self.seats:
            raise ValueError("Cannot create a booking without seats")
        return Booking(self.user_id, self.show_id, self.seats, self.promo_code, self.meals)
```

---

## III. Structural patterns

Structural patterns ease the design by identifying simple ways to realize relationships among entities.

### 8. Adapter pattern
Convert the interface of an existing class into another interface clients expect, enabling classes with incompatible interfaces to work together.

* **Reach for it when:** You integrate a third-party SDK, legacy module, or external service whose method names, units, or parameters do not match your domain contract.
* **Canonical interview problems:**
  * **Payment Gateway:** Wrapping Stripe, PayPal, and Razorpay SDKs behind a unified `PaymentProcessor(ABC)` contract.

### 9. Decorator pattern
Attach additional responsibilities to an object dynamically without modifying its underlying class.

* **Reach for it when:** You need cross-cutting concerns (retries, rate limiting, logging, encryption) that can wrap around multiple services without subclass proliferation.
* **Canonical interview problems:**
  * **Notification Service:** Wrapping notification channels with retry logic, deduplication, and rate limiting decorators.

### 10. Facade pattern
Provide a simplified, unified high-level interface to a complex subsystem.

* **Reach for it when:** Callers need to interact with a system composed of dozens of internal classes without needing to understand the underlying coordination.
* **Canonical interview problems:**
  * **Parking Lot System:** `ParkingLotFacade` exposing simple methods `park()`, `exit()`, `get_status()`, hiding the interaction between `SpotManager`, `PricingEngine`, and `TicketRepository`.
