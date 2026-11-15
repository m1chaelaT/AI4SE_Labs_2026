## Task
Implement the method `__contains__` of class `InventoryLedger` in file `playground/playground/inventory.py`.
Description: Return whether ``sku`` normalises to a SKU with positive on-hand stock.

Current stub in the file:
```python
def __contains__(self, sku: object) -> bool:
    pass
```

## Relevant code from the repository (top 5 retrieved chunks)
### 1. playground/playground/inventory.py::InventoryLedger.available (similarity 0.844)
```python
# file: playground/playground/inventory.py
# class: InventoryLedger
# kind: method
    def available(self, sku: str) -> int:
        """Return on-hand minus reserved for ``sku``."""
        sku = self._require_sku(sku)
        return self._on_hand.get(sku, 0) - self._reserved.get(sku, 0)
```
### 2. playground/playground/inventory.py::InventoryLedger.__iter__ (similarity 0.787)
```python
# file: playground/playground/inventory.py
# class: InventoryLedger
# kind: method
    def __iter__(self) -> Iterator[str]:
        """Iterate over SKUs with positive on-hand stock, in sorted order."""
        for sku in sorted(k for k, v in self._on_hand.items() if v > 0):
            yield sku
```
### 3. playground/playground/inventory.py::InventoryLedger._require_sku (similarity 0.787)
```python
# file: playground/playground/inventory.py
# class: InventoryLedger
# kind: method
    def _require_sku(self, sku: str) -> str:
        """Normalise ``sku`` and raise ``UnknownSKUError`` if it is unregistered."""
        sku = normalize_sku(sku)
        if sku not in self._product_repo:
            raise UnknownSKUError(sku)
        return sku
```
### 4. playground/playground/inventory.py::InventoryLedger.__len__ (similarity 0.769)
```python
# file: playground/playground/inventory.py
# class: InventoryLedger
# kind: method
    def __len__(self) -> int:
        """Return the number of SKUs with positive on-hand stock."""
        return sum(1 for qty in self._on_hand.values() if qty > 0)
```
### 5. playground/playground/inventory.py::InventoryLedger.release (similarity 0.768)
```python
# file: playground/playground/inventory.py
# class: InventoryLedger
# kind: method
    def release(self, sku: str, quantity: int) -> None:
        """Release ``quantity`` previously reserved for ``sku``."""
        quantity = ensure_positive_int(quantity, "quantity")
        sku = self._require_sku(sku)
        reserved = self._reserved.get(sku, 0)
        if quantity > reserved:
            raise InvalidTransitionError(reserved, quantity)
        self._reserved[sku] = reserved - quantity
```

## Requirements
- Keep the exact name, signature and decorators of the stub.
- Include this docstring: """Return whether ``sku`` normalises to a SKU with positive on-hand stock."""
- Use only names already imported or defined in the module; do not add imports.
- Follow the conventions visible in the retrieved code (attribute names, validation, exceptions).
- Return only the method in one ```python block.