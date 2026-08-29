from __future__ import annotations

import numpy as np
import itertools
import operator

from functools import reduce
from typing import Generic, Protocol, Self, TypeVar, Callable, cast, overload, override, get_args
from typeguard import typechecked
from collections.abc import Sequence, Hashable

from src.backend.utils.models.enums.stats import StatProperty
from src.backend.utils.models.enums.runes import RuneSlot, RuneSet, RuneStars
from src.backend.utils.models.enums.general import Grade, Upgrade, HashableCounter

ERROR: float = 0.000001  # Tolerance for floating point comparisons
T = TypeVar(name='T', bound=Hashable)

# TODO: Add support for probability of getting < value or > value or between values or among values
# Specifically for ValueEvent

# TODO: Might not want to print full list of outcomes or probabilities in error messages

# TODO: Separate fancy functions from Event class

# TODO: Rewrite get_event_as_counter() as an application of reduce()

class SortableHashable(Hashable, Protocol):
    def __lt__(self, other: object, /) -> bool: ...


@typechecked
class Event(Generic[T]):
    """Generic event class for SW items that models Random Variables.

    The core field of this class is the `pdf : dict[T, float]` field
    that represents a probability density function for `outcomes : T`
    in the event.

    The class supports standard probability operations such as random
    sampling, event union and intersection, along with functional
    operations like reduce, map, and filtering.
    """

    def __init__(
            self,
            outcomes: Sequence[T],
            weights: Sequence[float | int] | None = None) -> None:
        """Primary constructor

        Note: weights are normalized

        Args:
            outcomes (Sequence[T]): list of event outcomes
            weights (Sequence[float | int] | None): weights of each outcome
        """
        self._check_args(outcomes, weights)
        if weights is None:
            probabilities = (1.0 / len(outcomes) for _ in outcomes)
        else:
            probabilities = (weight / sum(weights) for weight in weights)
        self._pdf: dict[T, float] = dict(zip(outcomes, probabilities))
        print(f"Created Event over type {type(next(iter(outcomes)))}")
    
    @classmethod
    def from_pdf(cls, pdf: dict[T, float | int]) -> Event[T]:
        """Secondary constructor

        Args:
            pdf (dict[T, float]): Designated probability density function
        Returns:
            Event[T]: event object
        """
        return cls(list(pdf.keys()), list(pdf.values()))
    
    def _check_args(
            self,
            outcomes: Sequence[T],
            weights: Sequence[float] | None) -> None:
        """Checks for the following constraints on object initialization:
        * Outcomes exist and are unique
        * Weights are strictly positive
        * Number of provided outcomes and weights match

        Args:
            outcomes (Sequence[T]): Outcomes provided in initialization
            weights (Sequence[float] | None): Weights provided in initialization
        Raises:
            AttributeError: does not adhere to one of the constraints
        """
        if len(outcomes) == 0:
            raise AttributeError("Must enter non-empty outcomes.")
        if len(outcomes) != len(set(outcomes)):
            raise AttributeError("Outcome values must be unique.")
        if weights:
            if len(outcomes) != len(weights):
                raise AttributeError(
                    f"Number of values in outcomes ({len(outcomes)}) and " +
                    f"weights ({len(weights)}) does not match."
                )
            elif not all(0 < weight for weight in weights):
                raise AttributeError("Not all weights are strictly positive.")

    @property
    def captured_type(self) -> type[T] | None:
        return type(next(iter(self.outcomes)))

    @property
    def outcomes(self) -> set[T]:
        return set(self.pdf.keys())
    
    @property
    def probabilities(self) -> tuple[float, ...]:
        return tuple(self.pdf.values())
    
    @property
    def pdf(self) -> dict[T, float]:
        return self._pdf
    
    def __contains__(self, outcome: T):
        return self[outcome] >= ERROR
    
    def __getitem__(self, outcome: T) -> float:
        return self.pdf.get(outcome, 0.0)
    
    def __iter__(self):
        return iter(self.pdf.items())
    
    def __copy__(self) -> Event[T]:
        return Event[T].from_pdf(self.pdf.copy())
    
    @override
    def __eq__(self, other: object) -> bool:
        """Equality function for Event Class

        Args:
            other (object)

        Returns:
            bool: True only if two events have same set of outcomes with equal probabilities
        """
        if isinstance(other, Event):
            if self.captured_type == other.captured_type:
                other_event: Event[T] = cast(Event[T], other)
                if self.outcomes != other_event.outcomes:
                    return False
                for outcome in self.outcomes:
                    if abs(self[outcome] - other_event[outcome]) >= ERROR:
                        return False
                return True
        return False
    
    @override
    def __hash__(self) -> int:
        """Hash function for Event class

        Returns:
            int: hash of the tuple of outcomes and probabilities
        """
        return hash((self.outcomes, self.probabilities))
    
    def __delitem__(self, key: T) -> None:
        """Delete Item function for the Event class

        If outcome exists, removes outcome and re-normalizes probabilities

        Args:
            key (T): Outcome to delete

        Raises:
            KeyError: Outcome does not exist
            ValueError: Attempt to delete event's only outcome
        """
        if key not in self.outcomes:
            raise KeyError(f"Outcome '{key}' not in event outcomes.")
        total = sum(self.probabilities)
        if total - self[key] <= ERROR:
            raise ValueError(f"Cannot delete the only outcome '{key}' in the event.")
        
        total -= self[key]
        del self.pdf[key]
        self._pdf = {
            outcome: prb / total for outcome, prb in self}
    
    def remove(self, outcomes: Sequence[T]) -> None:
        """Removes outcomes from the event

        Args:
            outcomes (Sequence[T]): Outcomes to remove
        Raises:
            KeyError: There exists outcomes that don't exist in the event
            ValueError: Input outcomes contains duplicate entries
            ValueError: Outcomes are all outcomes in the event
        """
        if len(set(outcomes)) != len(outcomes):
            raise ValueError(f"Outcomes {outcomes} contains duplicate entries.")
        elif self.outcomes == set(outcomes):
            raise ValueError("Request for all outcomes to be removed.")
        elif not self.outcomes.issuperset(outcomes):
            raise KeyError(f"Outcomes {set(outcomes).difference(self.outcomes)} do not exist in event.")

        for outcome in outcomes:
            if outcome in self.outcomes:
                del self[outcome]
    
    def rebalance(self, outcome: T, probability: float) -> None:
        """Rebalances the event around an outcome.
        
        Sets the probability of an outcome to a specific probability
        and renormalizes the rest of the outcomes according to the
        remaining probability.

        Args:
            outcome (T): Outcome to rebalance or to add to the event
            probability (float): New probability for the outcome
        Raises:
            KeyError: If outcome argument doesn't exist in the event
            ValueError: If the new probability is not in (0,1)
            ValueError: If event only has one outcome
        """
        if outcome not in self.outcomes:
            raise KeyError(f"Outcome '{outcome}' does not exist in this event.")
        elif not (0 < probability < 1):
            raise ValueError("Probability must be in (0,1).")
        
        other_outcomes = self.outcomes - {outcome}
        total = sum(self.probabilities) - self[outcome]
        if total <= ERROR:
            raise ValueError("Cannot rebalance an event with only one outcome.")
        constant = (1 - probability) / total

        for other_outcome in other_outcomes:
            self.pdf[other_outcome] *= constant
        self.pdf[outcome] = probability
    
    def intersect[V: Hashable](self, other: Event[V]) -> Event[tuple[T, V]]:
        """Returns the intersection of two events

        Effectively the cartesian product of `Event[T]` and `Event[V]`.

        Args:
            other (Event[V]): Other event to intersect with
        Returns:
            Event[(T, V)]: New event with outcomes as tuples of the two events' outcomes
        """
        new_pdf: dict[tuple[T, V], float] = {}
        for outcome1, prb1 in self:
            for outcome2, prb2 in other:
                new_pdf[(outcome1, outcome2)] = prb1 * prb2
        return Event[tuple[T, V]].from_pdf(new_pdf)
    
    def intersect_self(self, n: int) -> Event[tuple[T, ...]]:
        """Intersects the event with itself n times

        Args:
            n (int): Number of times to intersect with itself
        Raises:
            ValueError: n < 1
        Returns:
            Event[tuple[T, ...]]: New event with outcomes as tuples of the original event
        """
        if n < 1:
            raise ValueError("n must be a positive integer.")
        elif n == 1:
            this_new_pdf: dict[tuple[T], float] = {(outcome,): prb for outcome, prb in self}
            return Event[tuple[T]].from_pdf(this_new_pdf)
        else:
            new_outcomes = itertools.product(self.outcomes, repeat=n)
            new_pdf: dict[tuple[T, ...], float] = {}
            for new_outcome in new_outcomes:
                new_pdf[new_outcome] = reduce(
                    operator.mul,
                    (self[outcome] for outcome in new_outcome),
                    1.0)
            return Event[tuple[T, ...]].from_pdf(new_pdf)
    
    def sample(self, n: int=1, replace: bool=False) -> tuple[T, ...]:
        """Samples n outcomes from the event without replacement

        Args:
            n (int, optional): sample size. Defaults to 1.
            replace (bool, optional): whether to sample with replacement. Defaults to False.
        Raises:
            ValueError: n < 1
            ValueError: Sampling without replacement when n is greater than the number of outcomes
        Returns:
            tuple[T, ...]: tuple of sampled outcomes
        """
        # TODO: Add support for returning the probability of getting the sampled outcome
        if n < 1:
            raise ValueError("n must be a positive integer.")
        elif n > len(self.outcomes) and replace is False:
            raise ValueError(
                f"Cannot sample {n} outcomes without replacement from an " +
                f"event with only {len(self.outcomes)} unique outcomes.")

        outcomes = np.array(list(self.outcomes), dtype=object)
        probabilities = np.array(list(self.probabilities), dtype=float)
        if n == 1:
            sample: T = np.random.choice(outcomes, p=probabilities)
            return (sample,)
        else:
            samples = np.random.choice(outcomes, p=probabilities, size=n, replace=replace)
            samples = tuple[T, ...](samples)
            return samples
    
    def sample_event(self, n: int, replace: bool=False) -> Event[tuple[T, ...]]:
        """Choose n outcomes without replacement and returns a new event with those outcomes

        Args:
            n (int): sample size must be at least 1.
            replace (bool, optional): whether to sample with replacement. Defaults to False.
        Raises:
            ValueError: n < 1
            ValueError: Sampling without replacement when n is greater than the number of outcomes
        Returns:
            Event[tuple[T, ...]]: Event representing possibilities from sampling n outcomes
        """
        if n < 1:
            raise ValueError("n must be at least 1 to form a new event.")
        else:
            if replace:
                new_event = self.intersect_self(n)
                return new_event
            else:
                # TODO: Implement without replacement (choose n)
                if n > len(self.outcomes):
                    raise ValueError(
                        f"Cannot sample {n} outcomes without replacement from an " +
                        f"event with only {len(self.outcomes)} unique outcomes.")
                else:
                    new_outcomes = itertools.permutations(self.outcomes, n)
                    new_pdf: dict[tuple[T, ...], float] = {}
                    for new_outcome in new_outcomes:
                        base_prb = 1.0
                        new_prb = 1.0
                        for outcome in new_outcome:
                            new_prb *= self[outcome] / base_prb
                            base_prb -= self[outcome]
                        new_pdf[new_outcome] = new_prb
                    return Event[tuple[T, ...]].from_pdf(new_pdf)
    
    def sorted[V: SortableHashable](self: Event[tuple[V, ...]]) -> Event[tuple[V, ...]]:
        """Creates new event where outcomes that are previously unsorted tuples become sorted

        NOTE: A sorted event should not be manipulated in the same manner as normal events

        Returns:
            Event[tuple[SortableHashable, ...]]: Event of set outcomes instead of tuples
        """
        new_pdf: dict[tuple[V, ...], float] = {}
        for outcome, prb in self:
            s_outcome = tuple(sorted(outcome))
            if s_outcome in new_pdf.keys():
                new_pdf[s_outcome] += prb
            else:
                new_pdf[s_outcome] = prb
        return Event[tuple[V, ...]].from_pdf(new_pdf)
    
    def get_event_as_counter[V: Hashable](self: Event[tuple[V, ...]]) -> Event[HashableCounter[V]]:
        """Creates new event where outcomes that are tuples over type V
        are converted into counter objects over type V.

        E.g., `('apple', 'orange', 'banana', 'orange', 'apple') -> {'apple': 2, 'banana': 1, 'orange': 2}`

        Returns:
            Event[HashableCounter[V]]: Event of counter outcomes instead of tuples
        """
        new_pdf: dict[HashableCounter[V], float] = {}
        for outcome, prb in self:
            c_outcome: HashableCounter[V] = HashableCounter[V](outcome)
            if c_outcome in new_pdf.keys():
                new_pdf[c_outcome] += prb
            else:
                new_pdf[c_outcome] = prb
        return Event[HashableCounter[V]].from_pdf(new_pdf)
    
    def filter(self, func: Callable[[T], bool]) -> Event[T]:
        """Narrows the event outcomes using a predicate function

        Args:
            func (Callable[[T], bool]): Predicate function to filter outcomes
        Returns:
            Event[T]: New event with filtered outcomes
        """
        new_pdf: dict[T, float] = {outcome: prb for outcome, prb in self if func(outcome)}
        if len(new_pdf) == 0:
            raise ValueError("No outcomes satisfy the filter condition.")
        return Event[T].from_pdf(new_pdf)
    
    def filter_by_probability(self, func: Callable[[float], bool]) -> Event[T]:
        """Narrows the event outcomes by their corresponding probability using a predicate function

        Args:
            func (Callable[[float], bool]): Predicate function to filter probabilities

        Returns:
            Event[T]: New event with filtered outcomes
        """
        return self.filter(lambda outcome: func(self[outcome]))
    
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
        """Tries to reduce the event if outcomes are tuples using a folding function.
        Effectively folds sequences of smaller events into a meaningful, aggregate representation.

        The folding operation is left-associative:
        
        `f ( f ( ... f(z, 1) ...), n-1), n)`

        Args:
            op (Callable[[tuple[Hashable], V], V]): Folding function to apply to the outcomes
        Returns:
            Event[V]: None if event type is not a sequence, otherwise a new event with reduced outcomes
        """
        new_pdf: dict[V, float] = {}
        if initial is not None:
            for outcome, prb in self:
                if (s := reduce(op, outcome, initial)) in new_pdf.keys():
                    new_pdf[s] += prb
                else:
                    new_pdf[s] = prb
            return Event[V].from_pdf(new_pdf)
        else:
            for outcome, prb in self:
                outcome = cast(tuple[V, ...], outcome)
                if (s := reduce(op, outcome)) in new_pdf.keys():
                    new_pdf[s] += prb
                else:
                    new_pdf[s] = prb
            return Event[V].from_pdf(new_pdf)
    
    def map[V: Hashable](
            self,
            func: Callable[[T], V]) -> Event[V]:
        """Maps the outcomes of the event to a new type using a mapping function

        Args:
            func (Callable[[T], V]): Function to apply to each outcome
        Returns:
            Event[V]: New event with mapped outcomes
        """
        new_pdf: dict[V, float] = {}
        for outcome, prb in self:
            new_outcome = func(outcome)
            if new_outcome in new_pdf.keys():
                new_pdf[new_outcome] += prb
            else:
                new_pdf[new_outcome] = prb
        return Event[V].from_pdf(new_pdf)

# Type aliases for rune/artifact stat values and properties
ValueEvent = Event[int]
PropertyEvent = Event[StatProperty]
SubPropertyEvent = Event[tuple[StatProperty, ...]]
RuneSlotEvent = Event[RuneSlot]
RuneStarsEvent = Event[RuneStars]
RuneSetEvent = Event[RuneSet]
GradeEvent = Event[Grade]
UpgradeEvent = Event[Upgrade]
