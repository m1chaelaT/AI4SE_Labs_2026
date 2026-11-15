```python
def __contains__(self, sku: object) -> bool:
    """Return whether ``sku`` normalises to a SKU with positive on-hand stock."""
    try:
        sku_norm = normalize_sku(sku)
    except Exception:
        return False
    if sku_norm not in self._product_repo:
        return False
    return self._on_hand.get(sku_norm, 0) > 0
```