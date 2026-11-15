## Task
Implement the method `__bool__` of class `Money` in file `playground/playground/models.py`.
Description: Return True when the amount is non-zero.

Current stub in the file:
```python
def __bool__(self) -> bool:
    pass
```

## Relevant code from the repository (top 5 retrieved chunks)
### 1. playground/playground/models.py::Money.__eq__ (similarity 0.825)
```python
# file: playground/playground/models.py
# class: Money
# kind: method
    def __eq__(self, other: object) -> bool:
        """Return True if ``other`` is Money with equal cents."""
        if not isinstance(other, Money):
            return NotImplemented
        return self._cents == other._cents
```
### 2. playground/playground/models.py::Money.__le__ (similarity 0.820)
```python
# file: playground/playground/models.py
# class: Money
# kind: method
    def __le__(self, other: Money) -> bool:
        """Return True if ``self`` is less than or equal to ``other``."""
        if not isinstance(other, Money):
            return NotImplemented
        return self._cents <= other._cents
```
### 3. playground/playground/models.py::Money.__lt__ (similarity 0.817)
```python
# file: playground/playground/models.py
# class: Money
# kind: method
    def __lt__(self, other: Money) -> bool:
        """Return True if ``self`` is strictly less than ``other``."""
        if not isinstance(other, Money):
            return NotImplemented
        return self._cents < other._cents
```
### 4. playground/playground/models.py::Money.__mul__ (similarity 0.781)
```python
# file: playground/playground/models.py
# class: Money
# kind: method
    def __mul__(self, factor: int) -> Money:
        """Return ``self`` multiplied by a non-negative integer."""
        if isinstance(factor, bool) or not isinstance(factor, int):
            raise TypeError("factor must be int")
        if factor < 0:
            raise ValueError("factor cannot be negative")
        return Money(self._cents * factor)
```
### 5. playground/tests/test_models.py::MoneyMiscTests.test_bool_false_for_zero (similarity 0.776)
```python
# file: playground/tests/test_models.py
# class: MoneyMiscTests
# kind: test
    def test_bool_false_for_zero(self) -> None:
        self.assertFalse(bool(Money(0)))
```

## Requirements
- Keep the exact name, signature and decorators of the stub.
- Include this docstring: """Return True when the amount is non-zero."""
- Use only names already imported or defined in the module; do not add imports.
- Follow the conventions visible in the retrieved code (attribute names, validation, exceptions).
- Return only the method in one ```python block.