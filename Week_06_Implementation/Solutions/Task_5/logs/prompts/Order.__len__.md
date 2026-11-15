## Task
Implement the method `__len__` of class `Order` in file `playground/playground/orders.py`.
Description: Return the number of line items.

Current stub in the file:
```python
def __len__(self) -> int:
    pass
```

## Relevant code from the repository (top 5 retrieved chunks)
### 1. playground/playground/orders.py::OrderBuilder.__len__ (similarity 0.870)
```python
# file: playground/playground/orders.py
# class: OrderBuilder
# kind: method
    def __len__(self) -> int:
        """Return the number of recorded lines."""
        return len(self._lines)
```
### 2. playground/playground/orders.py::OrderLog.__len__ (similarity 0.759)
```python
# file: playground/playground/orders.py
# class: OrderLog
# kind: method
    def __len__(self) -> int:
        """Return the number of logged orders."""
        return len(self._orders)
```
### 3. playground/playground/orders.py::Order.items (similarity 0.743)
```python
# file: playground/playground/orders.py
# class: Order
# kind: method
    @property
    def items(self) -> Tuple[LineItem, ...]:
        """Return a tuple copy of the order's line items."""
        return tuple(self._items)
```
### 4. playground/playground/orders.py::Order.__iter__ (similarity 0.729)
```python
# file: playground/playground/orders.py
# class: Order
# kind: method
    def __iter__(self) -> Iterator[LineItem]:
        """Iterate over a tuple snapshot of the order's line items."""
        return iter(tuple(self._items))
```
### 5. playground/playground/orders.py::Order.total (similarity 0.684)
```python
# file: playground/playground/orders.py
# class: Order
# kind: method
    @property
    def total(self) -> Money:
        """Return the total price of all line items under this order's pricing."""
        return self._pricing.price(self._items)
```

## Requirements
- Keep the exact name, signature and decorators of the stub.
- Include this docstring: """Return the number of line items."""
- Use only names already imported or defined in the module; do not add imports.
- Follow the conventions visible in the retrieved code (attribute names, validation, exceptions).
- Return only the method in one ```python block.