from typing import TypeVar, Hashable, Optional

from src.backend.utils.models.types.events import Event
from src.backend.utils.models.enums.stats import StatProperty
from src.backend.utils.models.enums.runes import RuneSlot, RuneSet, RuneStars
from src.backend.utils.models.enums.general import Grade

T = TypeVar('T', bound=Hashable)

class Entity[T]:
    """Class representing an entity which contains an value and its associated event.

    The value is an outcome and the associated event is CONDITIONAL on outcomes of some other event.
    i.e. For an Entity object with an outcome `a` and event `E`, then

    - E = RandomVar(A | B=b, C=c)
    - a \\in E

    Attributes:
        value (T): The value of the entity, which must be hashable.
        event (Optional[Event[T]]): The event associated with the entity, if any.
        is_fixed (bool): Indicates if the entity is fixed, meaning it has no associated event
                         or ignores the event's probabilities.
    """

    def __init__(self, value: T, event: Optional[Event[T]] = None):
        self._check_args(value, event)
        self._value = value
        self._event = event
        self._is_fixed = event is None
        self._check_args(value, event)
    
    def _check_args(self, value, event) -> None:
        """Checks for the following constraints on object initialization:
        1. The value is a possible outcome of the event

        Args:
            value (T): Value provided in initialization
            event (Event[T]): Event provided in initialization
        Raises:
            AttributeError: does not adhere to one of the constraints"""
        if value not in event:
            raise AttributeError(f"Value {value} is not a possible outcome of event")

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
RuneStarsEntity = Entity[RuneStars]
RuneSlotEntity = Entity[RuneSlot]
RuneSetEntity = Entity[RuneSet]
GradeEntity = Entity[Grade]
