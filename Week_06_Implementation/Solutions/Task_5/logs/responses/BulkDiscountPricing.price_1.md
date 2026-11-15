```python
def price(self, items: Sequence[LineItem]) -> Money:
    """Return the base price, less the discount if the quantity qualifies."""
    base_price = self._base.price(items)
    total_quantity = sum(item.quantity for item in items)
    if total_quantity >= self._threshold and self._percent_off:
        discount = (base_price * self._percent_off) // 100
        return base_price - discount
    return base_price
```