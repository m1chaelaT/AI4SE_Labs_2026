```python
def stock_report(self) -> Dict[str, int]:
    """Return a mapping of SKU to available quantity."""
    ledger = self._ledger
    # collect all SKUs that appear either on-hand or reserved
    skus = set(getattr(ledger, "_on_hand", {}).keys()) | set(getattr(ledger, "_reserved", {}).keys())
    return {sku: ledger.available(sku) for sku in skus}
```