## Task
Implement the method `transition` of class `OrderStateMachine` in file `playground/playground/orders.py`.
Description: Return ``target`` if the transition is allowed, else raise.

Current stub in the file:
```python
def transition(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
    pass
```

## Relevant code from the repository (top 5 retrieved chunks)
### 1. playground/playground/orders.py::OrderStateMachine.can_transition (similarity 0.878)
```python
# file: playground/playground/orders.py
# class: OrderStateMachine
# kind: method
    def can_transition(self, source: OrderStatus, target: OrderStatus) -> bool:
        """Return whether ``target`` is reachable from ``source``."""
        return target in OrderStateMachine.allowed_from(source)
```
### 2. playground/playground/orders.py::Order.advance (similarity 0.813)
```python
# file: playground/playground/orders.py
# class: Order
# kind: method
    def advance(self, target: OrderStatus) -> None:
        """Transition the order to ``target`` status, raising if not allowed."""
        new_status = self._machine.transition(self._status, target)
        self._status = new_status
```
### 3. playground/playground/orders.py::OrderStateMachine.__call__ (similarity 0.773)
```python
# file: playground/playground/orders.py
# class: OrderStateMachine
# kind: method
    def __call__(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
        """Convenience alias for :meth:`transition`."""
        return self.transition(source, target)
```
### 4. playground/playground/orders.py::OrderStateMachine (similarity 0.750)
```python
# file: playground/playground/orders.py
# kind: class
class OrderStateMachine:
    """Legal OrderStatus transitions, data-driven via TRANSITIONS."""

    TRANSITIONS: Dict[OrderStatus, FrozenSet[OrderStatus]] = {
        OrderStatus.NEW: frozenset({OrderStatus.RESERVED, OrderStatus.CANCELLED}),
        OrderStatus.RESERVED: frozenset({OrderStatus.SHIPPED, OrderStatus.CANCELLED}),
        OrderStatus.SHIPPED: frozenset(),
        OrderStatus.CANCELLED: frozenset(),
    }
    # methods:
    #   def allowed_from(status: OrderStatus) -> FrozenSet[OrderStatus]:
    #   def can_transition(self, source: OrderStatus, target: OrderStatus) -> bool:
    #   def transition(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
    #   def __call__(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
```
### 5. playground/playground/orders.py::OrderStateMachine.allowed_from (similarity 0.733)
```python
# file: playground/playground/orders.py
# class: OrderStateMachine
# kind: method
    @staticmethod
    def allowed_from(status: OrderStatus) -> FrozenSet[OrderStatus]:
        """Return the set of statuses reachable from ``status``."""
        if not isinstance(status, OrderStatus):
            raise TypeError("status must be OrderStatus")
        return OrderStateMachine.TRANSITIONS[status]
```

## Requirements
- Keep the exact name, signature and decorators of the stub.
- Include this docstring: """Return ``target`` if the transition is allowed, else raise."""
- Use only names already imported or defined in the module; do not add imports.
- Follow the conventions visible in the retrieved code (attribute names, validation, exceptions).
- Return only the method in one ```python block.