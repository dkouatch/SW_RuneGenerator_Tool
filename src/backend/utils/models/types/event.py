from __future__ import annotations

from functools import reduce
from typing import TypeVar, Hashable, Generic, Callable, overload, cast, overload
from typeguard import typechecked

from src.backend.utils.models.types.distribution import Distribution
from src.backend.utils.models.types.general import *

T = TypeVar('T', bound=Hashable)

# TODO: Dungeon class for representing drops where we template full rune distribution outcomes

class Event(Generic[T]):
    """Class representing an event which contains an value and its associated distribution.

    The value is an outcome and the associated distribution is CONDITIONAL on outcomes of some other distribution.
    i.e. For an Event object with an outcome `a` and unconditional distribution `X1` and some conditional
    distribution `X2`, then

    - X1 = RandomVar(A)
    - X2 = RandomVar(A | B=b)
    - a \\in X1 and a \\in X2
    - X2 is a subset of X1

    Almost all events are of the first form where you have a \\in E for a fixed distribution E.
    Only sub-property distributions may have the additional thing. Now is this necessary? Idk.

    Attributes:
        outcome (T): The value of the event, an outcome, which must be hashable.
        unconditional_distribution (Distribution[T]): The distribution associated with the event, independent of some fixed choices within the value.
        conditional_distribution (Distribution[T] | None): The distribution associated with the event, dependent of some fixed choices within the value.
        probability (float): The relevant probability of the event according to whether it is fixed
        is_conditioned (bool): State of the event
    """

    def __init__(self,
                 outcome: T,
                 unconditional_distribution: Distribution[T],
                 conditional_distribution: Distribution[T] | None = None) -> None:
        self._check_args(outcome, unconditional_distribution, conditional_distribution)
        self._outcome = outcome
        self._unconditional_distribution = unconditional_distribution
        self._conditional_distribution = conditional_distribution
        self._is_conditioned = conditional_distribution is not None  # By default, True if conditional distribution provided
        print(f"Created Event over type {type(outcome)}")
    
    def _check_args(
        self,
        outcome: T,
        unconditional_distribution: Distribution[T],
        conditional_distribution: Distribution[T] | None) -> None:
        """Enforces the following constraints
        
        1. The outcome is possible in the unconditional distribution.
        2. If a conditional distribution exists, the outcome is possible.
        3. If a conditional distribution exists, the set of outcomes in the conditional distribution
           is a subset of outcomes in the unconditional distribution.

        Args:
            outcome (Optional[T]): Outcome value provided in initialization
            unconditional_distribution (Distribution[T]): Unconditional distribution provided in initialization
            conditional_distribution (Distribution[T] | None): Conditional distribution provided in intiialization
        Raises:
            AttributeError: does not adhere to the constraints
        """
        if outcome not in unconditional_distribution:
            raise AttributeError(f"Value {outcome} is not a possible outcome of the unconditional distribution.")
        if conditional_distribution is not None:
            if outcome not in conditional_distribution:
                raise AttributeError(f"Value {outcome} is not a possible outcome of the conditional distribution.")
            elif not conditional_distribution.outcomes.issubset(unconditional_distribution.outcomes):
                raise AttributeError("Set of outcomes in conditional distribution is not a subset of the set of outcomes in the unconditional distribution.")

    @property
    def outcome(self) -> T:
        """Returns the value of the event."""
        return self._outcome
    
    @property
    def unconditional_distribution(self) -> Distribution[T]:
        """Returns the unconditional distribution associated with the event."""
        return self._unconditional_distribution
    
    @property
    def conditional_distribution(self) -> Distribution[T] | None:
        """Returns the conditional distribution associated with the event."""
        return self._conditional_distribution
    
    @overload
    def condition(self) -> None: ...

    @overload
    def condition(self, f: Callable[[T], bool]) -> None: ...
    
    def condition(
        self,
        f: Callable[[T], bool] | None = None) -> None:
        """Conditions the event on the existing conditional distribution's probabilities, 
        applies predicate function on the unconditional distribution to generate a new 
        conditional distribution, or conditions to 1.0 if it a conditional distribution 
        does not exist.
        
        Args:
            f: (Callable[[T], bool] | None): predicate function
        """
        self._is_conditioned = True
        if f is not None:
            self._conditional_distribution = self.unconditional_distribution.filter(f)
    
    def uncondition(self) -> None:
        """Unconditions the event to switch to the unconditional distribution's probabilities."""
        self._is_conditioned = False
    
    @property
    def probability(self) -> float:
        """Returns the probability of the outcome."""
        if self._is_conditioned:
            if self.conditional_distribution is None:  # If no conditional distribution exists, returns probability of 1.0
                return 1.0
            else:
                return self.conditional_distribution[self.outcome]
        else:
            return self.unconditional_distribution[self.outcome]

    def sorted[V: SortableHashable](self: Event[tuple[V, ...]]) -> Event[tuple[V, ...]]:
        """Creates new event where distribution outcomes that are previously unsorted tuples become sorted

        NOTE: Recall that sorted distributions should not be manipulated in the same manner as normal distributions

        Returns:
            Event[tuple[SortableHashable, ...]]: New event with sorted distributions and outcome
        """
        new_outcome = tuple(sorted(self.outcome))
        new_unconditional_distribution = self.unconditional_distribution.sorted()
        new_conditional_distribution = None if self.conditional_distribution is None else self.conditional_distribution.sorted()
        return Event[tuple[V, ...]](new_outcome, new_unconditional_distribution, new_conditional_distribution) 
    
    def to_counter[V: Hashable](self: Event[tuple[V, ...]]) -> Event[HashableCounter[V]]:
        """Creates new event where distribution outcomes that are tuples over type V
        are converted into counter objects over type V.

        E.g., `('apple', 'orange', 'banana', 'orange', 'apple') -> {'apple': 2, 'banana': 1, 'orange': 2}`

        Returns:
            Event[HashableCounter[V]]: New event of counter distributions and outcome instead of tuples
        """
        new_outcome = HashableCounter[V](self.outcome)
        new_unconditional_distribution = self.unconditional_distribution.to_counter()
        new_conditional_distribution = None if self.conditional_distribution is None else self.conditional_distribution.to_counter()
        return Event[HashableCounter[V]](new_outcome, new_unconditional_distribution, new_conditional_distribution) 
    
    @overload
    def reduce[V: Hashable](
        self: Event[tuple[V, ...]],
        op: Callable[[V, V], V]) -> Event[V]: ...

    @overload
    def reduce[U: Hashable, V: Hashable](
        self: Event[tuple[U, ...]],
        op: Callable[[V, U], V],
        initial: V) -> Event[V]: ...
    
    def reduce[V: Hashable](
            self: Event[tuple[Hashable, ...]],
            op,
            initial: V | None = None) -> Event[V]:
        """Tries to reduce the event if distribution outcomes are tuples using a folding function.
        Effectively folds sequences of smaller distributions into a meaningful, aggregate representation.

        The folding operation is left-associative:
        
        `f ( f ( ... f(z, 1) ...), n-1), n)`

        Args:
            op (Callable[[V, V], V] | Callable[[V, U], V]): Folding function to apply to the outcome and distributions
            initial (V | None): Initial folding value
        Returns:
            Event[V]: A new event with reduced distributions and outcome
        """
        new_outcome = (
            reduce(op, self.outcome) if initial is None 
            else reduce(op, self.outcome, initial))
        new_outcome = cast(V, new_outcome)

        new_unconditional_distribution = (
            self.unconditional_distribution.reduce(op) if initial is None
            else self.unconditional_distribution.reduce(op, initial))
        new_unconditional_distribution = cast(Distribution[V], new_unconditional_distribution)

        if self.conditional_distribution is None:
            new_conditional_distribution = None
        else:
            new_conditional_distribution = (
                self.conditional_distribution.reduce(op) if initial is None
                else self.conditional_distribution.reduce(op, initial))
            new_conditional_distribution = cast(Distribution[V], new_conditional_distribution)

        return Event[V](new_outcome, new_unconditional_distribution, new_conditional_distribution)
    
    def map[V: Hashable](
            self,
            func: Callable[[T], V]) -> Event[V]:
        """Maps the outcomes of the distribution to a new type using a mapping function

        Args:
            func (Callable[[T], V]): Function to apply to each outcome
        Returns:
            Distribution[V]: New distribution with mapped outcomes
        """
        new_outcome = func(self.outcome)
        new_unconditional_distribution = self.unconditional_distribution.map(func)
        new_conditional_distribution = None if self.conditional_distribution is None else self.conditional_distribution.map(func)
        return Event[V](new_outcome, new_unconditional_distribution, new_conditional_distribution)
