## Task
Implement the method `is_terminal` of class `OrderStatus` in file `playground/playground/enums.py`.
Description: True when the status ends further transitions.

Current stub in the file:
```python
@property
def is_terminal(self) -> bool:
    pass
```

## Relevant code from the repository (top 5 retrieved chunks)
### 1. playground/playground/enums.py::OrderStatus (similarity 0.810)
```python
# file: playground/playground/enums.py
# kind: class
class OrderStatus(Enum):
    """Lifecycle stages for an order."""

    NEW = "new"
    RESERVED = "reserved"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"
    # methods:
    #   def is_terminal(self) -> bool:
```
### 2. playground/tests/test_enums.py::OrderStatusTests.test_cancelled_is_terminal (similarity 0.698)
```python
# file: playground/tests/test_enums.py
# class: OrderStatusTests
# kind: test
    def test_cancelled_is_terminal(self) -> None:
        self.assertIs(OrderStatus.CANCELLED.is_terminal, True)
```
### 3. playground/playground/orders.py::Order.advance (similarity 0.694)
```python
# file: playground/playground/orders.py
# class: Order
# kind: method
    def advance(self, target: OrderStatus) -> None:
        """Transition the order to ``target`` status, raising if not allowed."""
        new_status = self._machine.transition(self._status, target)
        self._status = new_status
```
### 4. playground/tests/test_enums.py::OrderStatusTests.test_new_is_not_terminal (similarity 0.687)
```python
# file: playground/tests/test_enums.py
# class: OrderStatusTests
# kind: test
    def test_new_is_not_terminal(self) -> None:
        self.assertIs(OrderStatus.NEW.is_terminal, False)
```
### 5. playground/playground/orders.py::Order.status (similarity 0.672)
```python
# file: playground/playground/orders.py
# class: Order
# kind: method
    @property
    def status(self) -> OrderStatus:
        """Return the current order status."""
        return self._status
```

## Requirements
- Keep the exact name, signature and decorators of the stub.
- Include this docstring: """True when the status ends further transitions."""
- Use only names already imported or defined in the module; do not add imports.
- Follow the conventions visible in the retrieved code (attribute names, validation, exceptions).
- Return only the method in one ```python block.