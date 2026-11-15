## Task
Implement the method `stock_report` of class `Warehouse` in file `playground/playground/inventory.py`.
Description: Return a mapping of SKU to available quantity.

Current stub in the file:
```python
def stock_report(self) -> Dict[str, int]:
    pass
```

## Relevant code from the repository (top 5 retrieved chunks)
### 1. playground/playground/inventory.py::Warehouse.receive (similarity 0.758)
```python
# file: playground/playground/inventory.py
# class: Warehouse
# kind: method
    def receive(self, sku: str, quantity: int) -> int:
        """Add stock to the warehouse ledger; return the new on-hand total."""
        return self._ledger.add_stock(sku, quantity)
```
### 2. playground/playground/inventory.py::Warehouse (similarity 0.713)
```python
# file: playground/playground/inventory.py
# kind: class
class Warehouse(Entity):
    """Named location owning an :class:`InventoryLedger`."""
    # methods:
    #   def __init__(self, warehouse_id: str, name: str, ledger: InventoryLedger) -> None:
    #   def identity(self) -> str:
    #   def ledger(self) -> InventoryLedger:
    #   def receive(self, sku: str, quantity: int) -> int:
    #   def stock_report(self) -> Dict[str, int]:
    #   def __repr__(self) -> str:
```
### 3. playground/playground/inventory.py::inventory (similarity 0.709)
```python
# file: playground/playground/inventory.py
# kind: module
"""Inventory ledger and warehouse location."""

from __future__ import annotations

from typing import Dict, Iterator

from .base import Entity, Repository
from .exceptions import InvalidTransitionError, OutOfStockError, UnknownSKUError
from .util import ensure_positive_int, normalize_sku
```
### 4. playground/playground/inventory.py::Warehouse.__repr__ (similarity 0.699)
```python
# file: playground/playground/inventory.py
# class: Warehouse
# kind: method
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Warehouse({self._warehouse_id!r}, {self._name!r})"
```
### 5. playground/playground/inventory.py::InventoryLedger.available (similarity 0.680)
```python
# file: playground/playground/inventory.py
# class: InventoryLedger
# kind: method
    def available(self, sku: str) -> int:
        """Return on-hand minus reserved for ``sku``."""
        sku = self._require_sku(sku)
        return self._on_hand.get(sku, 0) - self._reserved.get(sku, 0)
```

## Requirements
- Keep the exact name, signature and decorators of the stub.
- Include this docstring: """Return a mapping of SKU to available quantity."""
- Use only names already imported or defined in the module; do not add imports.
- Follow the conventions visible in the retrieved code (attribute names, validation, exceptions).
- Return only the method in one ```python block.