## Task
Implement the method `can_afford` of class `Customer` in file `playground/playground/models.py`.
Description: Return True if ``balance + total`` does not exceed the credit limit.

Current stub in the file:
```python
def can_afford(self, total: Money) -> bool:
    pass
```

## Relevant code from the repository (top 5 retrieved chunks)
### 1. playground/playground/models.py::Customer.charge (similarity 0.814)
```python
# file: playground/playground/models.py
# class: Customer
# kind: method
    def charge(self, total: Money) -> None:
        """Increase the balance by ``total``, raising if the limit would be exceeded."""
        if not self.can_afford(total):
            raise ValueError("credit limit exceeded")
        self._balance = self._balance + total
```
### 2. playground/playground/models.py::Customer (similarity 0.750)
```python
# file: playground/playground/models.py
# kind: class
class Customer(Entity):
    """Buyer with a credit limit. Balance is the amount owed."""
    # methods:
    #   def __init__(self, customer_id: str, name: str, credit_limit: Money = Money(0)) -> None:
    #   def customer_id(self) -> str:
    #   def name(self) -> str:
    #   def credit_limit(self) -> Money:
    #   def balance(self) -> Money:
    #   def identity(self) -> str:
    #   def can_afford(self, total: Money) -> bool:
    #   def charge(self, total: Money) -> None:
```
### 3. playground/playground/models.py::Customer.credit_limit (similarity 0.738)
```python
# file: playground/playground/models.py
# class: Customer
# kind: method
    @property
    def credit_limit(self) -> Money:
        """Return the credit limit."""
        return self._credit_limit
```
### 4. playground/playground/models.py::Customer.balance (similarity 0.709)
```python
# file: playground/playground/models.py
# class: Customer
# kind: method
    @property
    def balance(self) -> Money:
        """Return the current outstanding balance."""
        return self._balance
```
### 5. playground/tests/test_models.py::CustomerTests.test_can_afford_accounts_for_existing_balance (similarity 0.683)
```python
# file: playground/tests/test_models.py
# class: CustomerTests
# kind: test
    def test_can_afford_accounts_for_existing_balance(self) -> None:
        c = Customer("C-1", "A", Money(1000))
        c.charge(Money(600))
        self.assertTrue(c.can_afford(Money(400)))
        self.assertFalse(c.can_afford(Money(401)))
```

## Requirements
- Keep the exact name, signature and decorators of the stub.
- Include this docstring: """Return True if ``balance + total`` does not exceed the credit limit."""
- Use only names already imported or defined in the module; do not add imports.
- Follow the conventions visible in the retrieved code (attribute names, validation, exceptions).
- Return only the method in one ```python block.