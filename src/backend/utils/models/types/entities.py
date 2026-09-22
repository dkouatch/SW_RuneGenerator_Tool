from __future__ import annotations

from functools import reduce
from typing import TypeVar, Hashable, Generic, Callable, overload, cast
from typeguard import typechecked

from src.backend.utils.models.types.events import Event
from src.backend.utils.models.types.general import *
from src.backend.utils.models.enums.stats import StatProperty
from src.backend.utils.models.enums.runes import RuneSlot, RuneSet, RuneStars
from src.backend.utils.models.enums.general import Grade, Upgrade

T = TypeVar('T', bound=Hashable)

# TODO: Dungeon class for representing drops where we template full rune event outcomes

@typechecked
class Entity(Generic[T]):
    """Class representing an entity which contains an value and its associated event.

    The value is an outcome and the associated event is CONDITIONAL on outcomes of some other event.
    i.e. For an Entity object with an outcome `a` and unconditional event `E` and some conditional
    event `F`, then

    - E = RandomVar(A)
    - F = RandomVar(A | B=b)
    - a \\in E and a \\in F
    - F is a subset of E

    Almost all entities are of the first form where you have a \\in E for a fixed event E.
    Only sub-property events may have the additional thing. Now is this necessary? Idk.

    Supports creating entities over None

    Attributes:
        outcome (T): The value of the entity, an outcome, which must be hashable.
        unconditional_event (Event[T]): The event associated with the entity, independent of some fixed choices within the value.
        conditional_event (Event[T] | None): The event associated with the entity, dependent of some fixed choices within the value.
        probability (float): The relevant probability of the entity according to whether it is fixed
        is_conditioned (bool): State of the entity
    """

    def __init__(self,
                 outcome: T,
                 unconditional_event: Event[T],
                 conditional_event: Event[T] | None = None) -> None:
        self._check_args(outcome, unconditional_event, conditional_event)
        self._outcome = outcome
        self._unconditional_event = unconditional_event
        self._conditional_event = conditional_event
        self._is_conditioned = conditional_event is not None  # By default, True if conditional event provided
        print(f"Created Entity over type {type(outcome)}")
    
    def _check_args(
        self,
        outcome: T,
        unconditional_event: Event[T],
        conditional_event: Event[T] | None) -> None:
        """Enforces the following constraints
        
        1. The outcome is possible in the unconditional event.
        2. If a conditional event exists, the outcome is possible.
        3. If a conditional event exists, the set of outcomes in the conditional event
           is a subset of outcomes in the unconditional event.

        Args:
            outcome (Optional[T]): Outcome value provided in initialization
            unconditional_event (Event[T]): Unconditional event provided in initialization
            conditional_event (Event[T] | None): Conditional event provided in intiialization
        Raises:
            AttributeError: does not adhere to the constraints
        """
        if outcome not in unconditional_event:
            raise AttributeError(f"Value {outcome} is not a possible outcome of the unconditional event.")
        if conditional_event is not None:
            if outcome not in conditional_event:
                raise AttributeError(f"Value {outcome} is not a possible outcome of the conditional event.")
            elif not conditional_event.outcomes.issubset(unconditional_event.outcomes):
                raise AttributeError("Set of outcomes in conditional event is not a subset of the set of outcomes in the unconditional event.")

    @property
    def outcome(self) -> T:
        """Returns the value of the entity."""
        return self._outcome
    
    @property
    def unconditional_event(self) -> Event[T]:
        """Returns the unconditional event associated with the entity."""
        return self._unconditional_event
    
    @property
    def conditional_event(self) -> Event[T] | None:
        """Returns the conditional event associated with the entity."""
        return self._conditional_event
    
    def condition(self) -> None:
        """Conditions the entity on the conditional event's probabilities, or to 1.0 if it does not exist."""
        self._is_conditioned = True
    
    def uncondition(self) -> None:
        """Unconditions the entity to switch to the unconditional event's probabilities."""
        self._is_conditioned = False
    
    @property
    def probability(self) -> float:
        """Returns the probability of the outcome."""
        if self._is_conditioned:
            if self.conditional_event is None:  # If no conditional event exists, returns probability of 1.0
                return 1.0
            else:
                return self.conditional_event[self.outcome]
        else:
            return self.unconditional_event[self.outcome]

    def sorted[V: SortableHashable](self: Entity[tuple[V, ...]]) -> Entity[tuple[V, ...]]:
        """Creates new entity where event outcomes that are previously unsorted tuples become sorted

        NOTE: Recall that sorted events should not be manipulated in the same manner as normal events

        Returns:
            Entity[tuple[SortableHashable, ...]]: New entity with sorted events and outcome
        """
        new_outcome = tuple(sorted(self.outcome))
        new_unconditional_event = self.unconditional_event.sorted()
        new_conditional_event = None if self.conditional_event is None else self.conditional_event.sorted()
        return Entity[tuple[V, ...]](new_outcome, new_unconditional_event, new_conditional_event) 
    
    def to_counter[V: Hashable](self: Entity[tuple[V, ...]]) -> Entity[HashableCounter[V]]:
        """Creates new entity where event outcomes that are tuples over type V
        are converted into counter objects over type V.

        E.g., `('apple', 'orange', 'banana', 'orange', 'apple') -> {'apple': 2, 'banana': 1, 'orange': 2}`

        Returns:
            Entity[HashableCounter[V]]: New entity of counter events and outcome instead of tuples
        """
        new_outcome = HashableCounter[V](self.outcome)
        new_unconditional_event = self.unconditional_event.to_counter()
        new_conditional_event = None if self.conditional_event is None else self.conditional_event.to_counter()
        return Entity[HashableCounter[V]](new_outcome, new_unconditional_event, new_conditional_event) 
    
    @overload
    def reduce[V: Hashable](
        self: Entity[tuple[V, ...]],
        op: Callable[[V, V], V]) -> Entity[V]: ...

    @overload
    def reduce[U: Hashable, V: Hashable](
        self: Entity[tuple[U, ...]],
        op: Callable[[V, U], V],
        initial: V) -> Entity[V]: ...
    
    def reduce[V: Hashable](
            self: Entity[tuple[Hashable, ...]],
            op,
            initial: V | None = None) -> Entity[V]:
        """Tries to reduce the entity if event outcomes are tuples using a folding function.
        Effectively folds sequences of smaller events into a meaningful, aggregate representation.

        The folding operation is left-associative:
        
        `f ( f ( ... f(z, 1) ...), n-1), n)`

        Args:
            op (Callable[[V, V], V] | Callable[[V, U], V]): Folding function to apply to the outcome and events
            initial (V | None): Initial folding value
        Returns:
            Entity[V]: A new entity with reduced events and outcome
        """
        new_outcome = (
            reduce(op, self.outcome) if initial is None 
            else reduce(op, self.outcome, initial))
        new_outcome = cast(V, new_outcome)

        new_unconditional_event = (
            self.unconditional_event.reduce(op) if initial is None
            else self.unconditional_event.reduce(op, initial))
        new_unconditional_event = cast(Event[V], new_unconditional_event)

        if self.conditional_event is None:
            new_conditional_event = None
        else:
            new_conditional_event = (
                self.conditional_event.reduce(op) if initial is None
                else self.conditional_event.reduce(op, initial))
            new_conditional_event = cast(Event[V], new_conditional_event)

        return Entity[V](new_outcome, new_unconditional_event, new_conditional_event)
    
    def map[V: Hashable](
            self,
            func: Callable[[T], V]) -> Entity[V]:
        """Maps the outcomes of the event to a new type using a mapping function

        Args:
            func (Callable[[T], V]): Function to apply to each outcome
        Returns:
            Event[V]: New event with mapped outcomes
        """
        new_outcome = func(self.outcome)
        new_unconditional_event = self.unconditional_event.map(func)
        new_conditional_event = None if self.conditional_event is None else self.conditional_event.map(func)
        return Entity[V](new_outcome, new_unconditional_event, new_conditional_event) 


ValueEntity = Entity[int]
SubValueEntity = Entity[tuple[int, ...]]
PropertyEntity = Entity[StatProperty]
SubPropertyEntity = Entity[tuple[StatProperty, ...]]
RuneStarsEntity = Entity[RuneStars]
RuneSlotEntity = Entity[RuneSlot]
RuneSetEntity = Entity[RuneSet]
GradeEntity = Entity[Grade]
UpgradeEntity = Entity[Upgrade]
