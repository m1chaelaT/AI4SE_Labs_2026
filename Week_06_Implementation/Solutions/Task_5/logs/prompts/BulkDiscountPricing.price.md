## Task
Implement the method `price` of class `BulkDiscountPricing` in file `playground/playground/pricing.py`.
Description: Return the base price, less the discount if the quantity qualifies.

Current stub in the file:
```python
def price(self, items: Sequence[LineItem]) -> Money:
    pass
```

## Relevant code from the repository (top 5 retrieved chunks)
### 1. playground/playground/pricing.py::BulkDiscountPricing.__repr__ (similarity 0.797)
```python
# file: playground/playground/pricing.py
# class: BulkDiscountPricing
# kind: method
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"BulkDiscountPricing(threshold={self._threshold}, percent_off={self._percent_off})"
```
### 2. playground/playground/pricing.py::BulkDiscountPricing.percent_off (similarity 0.773)
```python
# file: playground/playground/pricing.py
# class: BulkDiscountPricing
# kind: method
    @property
    def percent_off(self) -> int:
        """Return the discount percentage."""
        return self._percent_off
```
### 3. playground/playground/pricing.py::BulkDiscountPricing.threshold (similarity 0.762)
```python
# file: playground/playground/pricing.py
# class: BulkDiscountPricing
# kind: method
    @property
    def threshold(self) -> int:
        """Return the qualifying total quantity."""
        return self._threshold
```
### 4. playground/playground/pricing.py::BulkDiscountPricing (similarity 0.752)
```python
# file: playground/playground/pricing.py
# kind: class
class BulkDiscountPricing(PricingStrategy):
    """Wraps another strategy; applies a percent discount when total quantity meets a threshold."""
    # methods:
    #   def __init__(self, base: PricingStrategy, threshold: int, percent_off: int) -> None:
    #   def threshold(self) -> int:
    #   def percent_off(self) -> int:
    #   def price(self, items: Sequence[LineItem]) -> Money:
    #   def __repr__(self) -> str:
```
### 5. playground/playground/pricing.py::BulkDiscountPricing.__init__ (similarity 0.724)
```python
# file: playground/playground/pricing.py
# class: BulkDiscountPricing
# kind: method
    def __init__(self, base: PricingStrategy, threshold: int, percent_off: int) -> None:
        """Create a strategy that discounts ``base`` totals above ``threshold`` quantity."""
        if not isinstance(base, PricingStrategy):
            raise TypeError("base must be PricingStrategy")
        threshold = ensure_positive_int(threshold, "threshold")
        if isinstance(percent_off, bool) or not isinstance(percent_off, int):
            raise TypeError("percent_off must be int")
        if percent_off < 0 or percent_off > 100:
            raise ValueError("percent_off must be 0..100")
        self._base = base
        self._threshold = threshold
        self._percent_off = percent_off
```

## Requirements
- Keep the exact name, signature and decorators of the stub.
- Include this docstring: """Return the base price, less the discount if the quantity qualifies."""
- Use only names already imported or defined in the module; do not add imports.
- Follow the conventions visible in the retrieved code (attribute names, validation, exceptions).
- Return only the method in one ```python block.