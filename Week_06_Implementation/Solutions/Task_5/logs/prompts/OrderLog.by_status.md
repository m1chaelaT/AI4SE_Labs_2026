## Task
Implement the method `by_status` of class `OrderLog` in file `playground/playground/orders.py`.
Description: Yield orders whose status matches ``status``.

Current stub in the file:
```python
def by_status(self, status: OrderStatus) -> Iterator[Order]:
    pass
```

## Relevant code from the repository (top 5 retrieved chunks)
### 1. playground/playground/orders.py::Order.status (similarity 0.820)
```python
# file: playground/playground/orders.py
# class: Order
# kind: method
    @property
    def status(self) -> OrderStatus:
        """Return the current order status."""
        return self._status
```
### 2. playground/playground/orders.py::OrderLog (similarity 0.721)
```python
# file: playground/playground/orders.py
# kind: class
class OrderLog:
    """Ordered, deduplicated record of orders; iterable."""
    # methods:
    #   def __init__(self) -> None:
    #   def record(self, order: Order) -> None:
    #   def by_status(self, status: OrderStatus) -> Iterator[Order]:
    #   def __getitem__(self, index: int) -> Order:
    #   def __len__(self) -> int:
    #   def __iter__(self) -> Iterator[Order]:
```
### 3. playground/playground/orders.py::OrderLog.__init__ (similarity 0.716)
```python
# file: playground/playground/orders.py
# class: OrderLog
# kind: method
    def __init__(self) -> None:
        """Create an empty order log."""
        self._orders: List[Order] = []
```
### 4. playground/playground/orders.py::OrderLog.__iter__ (similarity 0.713)
```python
# file: playground/playground/orders.py
# class: OrderLog
# kind: method
    def __iter__(self) -> Iterator[Order]:
        """Iterate over the logged orders."""
        yield from list(self._orders)
```
### 5. playground/playground/orders.py::OrderLog.__getitem__ (similarity 0.707)
```python
# file: playground/playground/orders.py
# class: OrderLog
# kind: method
    def __getitem__(self, index: int) -> Order:
        """Return the order at ``index``."""
        return self._orders[index]
```

## Requirements
- Keep the exact name, signature and decorators of the stub.
- Include this docstring: """Yield orders whose status matches ``status``."""
- Use only names already imported or defined in the module; do not add imports.
- Follow the conventions visible in the retrieved code (attribute names, validation, exceptions).
- Return only the method in one ```python block.