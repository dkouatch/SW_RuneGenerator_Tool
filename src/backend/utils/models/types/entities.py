from typing import TypeVar, Hashable, Optional

from src.backend.utils.models.types.events import Event
from src.backend.utils.models.enums.stats import StatProperty

T = TypeVar('T', bound=Hashable)

class Entity[T]:
    """Class representing an entity which contains an value and its associated event.
    
    Attributes:
        value (T): The value of the entity, which must be hashable.
        event (Optional[Event[T]]): The event associated with the entity, if any.
        is_fixed (bool): Indicates if the entity is fixed, meaning it has no associated event
                         or ignores the event's probabilities.
    """

    def __init__(self, value: T, event: Optional[Event[T]] = None):
        self._value = value
        self._event = event
        self._is_fixed = event is None
    
    @property
    def value(self) -> T:
        """Returns the value of the entity."""
        return self._value
    
    @property
    def event(self) -> Optional[Event[T]]:
        """Returns the event associated with the entity."""
        return self._event
    
    @property
    def probability(self) -> float:
        """Returns the probability of the value."""
        if self.is_fixed:
            return 1.0
        return self.event[self.value]

ValueEntity = Entity[int]
PropertyEntity = Entity[StatProperty]
