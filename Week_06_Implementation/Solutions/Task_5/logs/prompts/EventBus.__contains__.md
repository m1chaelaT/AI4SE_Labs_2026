## Task
Implement the method `__contains__` of class `EventBus` in file `playground/playground/events.py`.
Description: Return whether any handlers are registered for ``event_type``.

Current stub in the file:
```python
def __contains__(self, event_type: object) -> bool:
    pass
```

## Relevant code from the repository (top 5 retrieved chunks)
### 1. playground/playground/events.py::EventBus.__init__ (similarity 0.751)
```python
# file: playground/playground/events.py
# class: EventBus
# kind: method
    def __init__(self) -> None:
        """Initialise an empty handler registry."""
        self._handlers: Dict[EventType, List[Callable[..., None]]] = {}
```
### 2. playground/tests/test_events.py::EventBusContainsTests (similarity 0.714)
```python
# file: playground/tests/test_events.py
# kind: class
class EventBusContainsTests(unittest.TestCase):
    # methods:
    #   def test_contains_false_without_handlers(self) -> None:
    #   def test_contains_true_with_handler(self) -> None:
    #   def test_contains_false_after_all_unsubscribed(self) -> None:
    #   def test_contains_non_event_type_is_false(self) -> None:
```
### 3. playground/playground/events.py::EventBus.subscribe (similarity 0.712)
```python
# file: playground/playground/events.py
# class: EventBus
# kind: method
    def subscribe(self, event_type: EventType, handler: Callable[..., None]) -> None:
        """Register ``handler`` to be called when ``event_type`` is published."""
        if not isinstance(event_type, EventType):
            raise TypeError("event_type must be EventType")
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._handlers.setdefault(event_type, []).append(handler)
```
### 4. playground/playground/simulation.py::Simulation.bus (similarity 0.703)
```python
# file: playground/playground/simulation.py
# class: Simulation
# kind: method
    @property
    def bus(self) -> EventBus:
        """Return the event bus."""
        return self._bus
```
### 5. playground/tests/test_events.py::EventBusContainsTests.test_contains_non_event_type_is_false (similarity 0.688)
```python
# file: playground/tests/test_events.py
# class: EventBusContainsTests
# kind: test
    def test_contains_non_event_type_is_false(self) -> None:
        self.assertNotIn("ORDER_SHIPPED", EventBus())
        self.assertNotIn(4, EventBus())
```

## Requirements
- Keep the exact name, signature and decorators of the stub.
- Include this docstring: """Return whether any handlers are registered for ``event_type``."""
- Use only names already imported or defined in the module; do not add imports.
- Follow the conventions visible in the retrieved code (attribute names, validation, exceptions).
- Return only the method in one ```python block.