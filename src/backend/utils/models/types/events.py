from __future__ import annotations

import numpy as np
import itertools
import operator

from functools import reduce
from typing import Iterable, Optional, TypeVar, Hashable, Callable, TypeGuard

from src.backend.utils.models.enums.stats import StatProperty
from src.backend.utils.models.enums.runes import RuneSlot, RuneSet, RuneStars
from src.backend.utils.models.enums.general import Grade, Upgrade, HashableCounter

T = TypeVar('T', bound=Hashable)
V = TypeVar('V', bound=Hashable)
ERROR = 0.0001  # Tolerance for floating point comparisons

class Event[T]:
    """Generic event class for SW items that models Random Variables.

    Contains underlying probability density function and supports
    random outcome selection, event unions, and event intersections.
    """

    def __init__(
            self,
            outcomes: Iterable[T],
            weights: Optional[Iterable[float | int]] = None):
        """Primary constructor

        Args:
            outcomes (Iterable[T]): list of event outcomes
            weights (Optional[Iterable[float  |  int]]): weights of each outcome
        """
        self._check_args(outcomes, weights)
        if weights is None:
            probabilities = (1.0 / len(outcomes) for _ in outcomes)
        else:
            probabilities = (weight / sum(weights) for weight in weights)
        self._pdf = dict(zip(outcomes, probabilities))
        print(f"Created Event over type {type(list(outcomes)[0])}")
    
    @classmethod
    def from_pdf(cls, pdf: dict[T, float]) -> Event[T]:
        """Secondary constructor

        Args:
            pdf (dict[T, float]): Designated probability density function
        Returns:
            Event[T]: event object
        """
        return cls(pdf.keys(), pdf.values())
    
    def _check_args(
            self,
            outcomes: Iterable[T],
            weights: Optional[Iterable[float]]) -> None:
        """Checks for the following constraints on object initialization:
        1. Outcomes exist and are unique
        2. Weights are strictly positive

        Args:
            outcomes (Iterable[T]): Outcomes provided in initialization
            weights (Optional[Iterable[float]]): Weights provided in initialization
        Raises:
            AttributeError: does not adhere to one of the constraints
        """
        if len(outcomes) == 0:
            raise AttributeError("Must enter non-empty outcomes.")
        if len(outcomes) != len(set(outcomes)):
            raise AttributeError("outcomes values must be unique.")
        if weights:
            if len(outcomes) != len(weights):
                raise AttributeError(
                    f"Number of values in outcomes ({len(outcomes)}) and " 
                    f"weights ({len(weights)}) does not match."
                )
            elif not all(0 < weight for weight in weights):
                raise AttributeError("Not all weights are strictly positive.")
    
    @property
    def outcomes(self) -> set[T]:
        return set(self.pdf.keys())
    
    @property
    def probabilities(self) -> list[float]:
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
        return Event.from_pdf(self.pdf.copy())
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return False
        else:
            return self.pdf == other.pdf 
    
    def __delitem__(self, key: T) -> None:
        if key not in self.outcomes:
            raise KeyError(f"Outcome {key} not in event outcomes.")
        total = sum(self.probabilities)
        if total - self[key] <= ERROR:
            raise ValueError("Cannot delete the only outcome in the event.")
        
        total -= self[key]
        del self.pdf[key]
        self._pdf = {
            outcome: prb / total for outcome, prb in self}
    
    def remove(self, outcomes: Iterable[T]) -> None:
        """Removes outcomes from the event
        Args:
            outcomes (Iterable[T]): Outcomes to remove
        """
        for outcome in outcomes:
            if outcome in self.outcomes:
                del self[outcome]
    
    def rebalance(self, outcome: T, probability: float) -> None:
        """Rebalances the event by setting the probability of an outcome to a new value

        Args:
            outcome (T): Outcome to rebalance or to add to the event
            probability (float): New probability for the outcome
        Raises:
            ValueError: if the new probability is not in (0,1)
        """
        if not (0 < probability < 1):
            raise ValueError("Probability must be in (0,1).")
        
        other_outcomes = self.outcomes - {outcome}
        total = sum(self.probabilities) - self[outcome]
        if total <= ERROR:
            raise ValueError("Cannot rebalance an event with only one outcome.")
        constant = (1 - probability) / total

        for other_outcome in other_outcomes:
            self.pdf[other_outcome] *= constant
        self.pdf[outcome] = probability
    
    def _is_tuple_of_hashables(self) -> TypeGuard[tuple[Hashable]]:
        """Checks if the event outcomes are sequences of hashable types"""
        return all(
            isinstance(outcome, tuple)
            and all(isinstance(value, Hashable) for value in outcome)
            for outcome in self.outcomes)
    
    def intersect(self, other: Event[V]) -> Event[(T, V)]:
        """Returns the intersection of two events
        Args:
            other (Event[V]): Other event to intersect with
        Returns:
            Event[(T, V)]: New event with outcomes as tuples of the two events' outcomes
        """
        new_pdf = {}
        for outcome1, prb1 in self:
            for outcome2, prb2 in other:
                new_pdf[(outcome1, outcome2)] = prb1 * prb2
        return Event.from_pdf(new_pdf)
    
    def intersect_self(self, n: int) -> Event[tuple[T, ...]]:
        """Intersects the event with itself n times
        Args:
            n (int): Number of times to intersect with itself
        Raises:
            ValueError: n is nonpositive
        Returns:
            Event[tuple[T, ...]]: New event with outcomes as tuples of the original event
        """
        if n < 1:
            raise ValueError("n must be a positive integer.")
        elif n == 1:
            return self
        else:
            new_outcomes = itertools.combinations_with_replacement(self.outcomes, n)
            new_pdf = {}
            for new_outcome in new_outcomes:
                new_pdf[new_outcome] = reduce(
                    operator.mul,
                    (self[outcome] for outcome in new_outcome),
                    1.0)
            return Event.from_pdf(new_pdf)
    
    def sample(self, n: int = 1, replace=False) -> T | np.ndarray[T]:
        """Samples n outcomes from the event without replacement

        Args:
            n (int, optional): sample size. Defaults to 1.
            replace (bool, optional): whether to sample with replacement. Defaults to False.

        Raises:
            ValueError: n is nonpositive or greater than the number of unique outcomes

        Returns:
            T: _description_
        """
        # TODO: Add support for returning the probability of getting the sampled outcome
        if n < 1:
            raise ValueError("n must be a positive integer.")
        elif n > len(self.outcomes) and replace is False:
            raise ValueError(
                f"Cannot sample {n} outcomes without replacement from an "
                f"event with only {len(self.outcomes)} unique outcomes.")
        samples = np.random.choice(list(self.outcomes), p=self.probabilities, size=n, replace=replace)
        if n == 1:
            return samples[0]
        else:
            return tuple(samples)
    
    def sample_event(self, n: int, replace=False) -> Event[tuple[T, ...]] | None:
        """Choose n outcomes without replacement and returns a new event with those outcomes
        Args:
            n (int): sample size must be at least 1.
            replace (bool, optional): whether to sample with replacement. Defaults to False.
        """
        if n < 1:
            raise ValueError("n must be at least 1 to form a new event.")
        elif n == 1:
            new_pdf = {tuple([outcome]): prb for outcome, prb in self}
            return Event.from_pdf(new_pdf)
        else:
            if replace:
                new_event = self.intersect_self(n)
                return new_event
            else:
                # TODO: Implement without replacement (choose n)
                if n > len(self.outcomes):
                    raise ValueError(
                        f"Cannot sample {n} outcomes without replacement from an "
                        f"event with only {len(self.outcomes)} unique outcomes.")
                else:
                    new_outcomes = itertools.permutations(self.outcomes, n)
                    new_pdf = {}
                    for new_outcome in new_outcomes:
                        base_prb = 1.0
                        new_prb = 1.0
                        for outcome in new_outcome:
                            new_prb *= self[outcome] / base_prb
                            base_prb -= self[outcome]
                        new_pdf[new_outcome] = new_prb
                    return Event.from_pdf(new_pdf)
    
    def sorted(self) -> Optional[Event]:
        """Creates new event where outcomes are sorted tuples instead of tuples

        NOTE: A sorted event should not be manipulated in the same manner as normal events

        Returns:
            Event[Set]: Event of set outcomes instead of tuples
        """
        if self._is_tuple_of_hashables():
            new_pdf = {}
            for outcome, prb in self:
                s_outcome = tuple(sorted(outcome))
                if s_outcome in new_pdf.keys():
                    new_pdf[s_outcome] += prb
                else:
                    new_pdf[s_outcome] = prb
            return Event.from_pdf(new_pdf)
        else:
            print("Not sorted")
    
    def get_event_as_counter(self) -> Optional[Event[HashableCounter]]:
        """Creates new event where outcomes are counter objects instead of tuples
        Returns:
            Optional[Event[Counter]]: Event of counter outcomes instead of tuples
        """
        if self._is_tuple_of_hashables():
            new_pdf = {}
            for outcome, prb in self:
                c_outcome = HashableCounter(outcome)
                if c_outcome in new_pdf.keys():
                    new_pdf[c_outcome] += prb
                else:
                    new_pdf[c_outcome] = prb
            return Event.from_pdf(new_pdf)
        else:
            print("No counter created.")
    
    def filter(self, func: Callable[[T], bool]) -> Event[T]:
        """Filters the event outcomes using a predicate function
        Args:
            func (Callable[[T], bool]): Predicate function to filter outcomes
        Returns:
            Event[T]: New event with filtered outcomes
        """
        new_pdf = {outcome: prb for outcome, prb in self if func(outcome)}
        if len(new_pdf) == 0:
            raise ValueError("No outcomes satisfy the filter condition.")
        return Event.from_pdf(new_pdf)
    
    def reduce(
            self,
            op : Callable[[tuple[Hashable], V], V]) -> Optional[Event[V]]:
        """Tries to reduce the event if it is a sequence of smaller events using a folding function
        Args:
            op (Callable[[tuple[Hashable], V], V]): Folding function to apply to the outcomes
        Returns:
            Optional[Event[V]]: None if event type is not a sequence, otherwise a new event with reduced outcomes
        """
        if self._is_tuple_of_hashables():
            new_pdf = {}
            for outcome, prb1 in self:
                if (s := reduce(op, outcome)) in new_pdf.keys():
                    new_pdf[s] += prb1
                else:
                    new_pdf[s] = prb1
            return Event.from_pdf(new_pdf)
    
    def map(
            self,
            func: Callable[[T], V]) -> Event[V]:
        """Maps the outcomes of the event to a new type using a function

        Args:
            func (Callable[[T], V]): Function to apply to each outcome
        Returns:
            Event[V]: New event with mapped outcomes
        """
        new_pdf = {}
        for outcome, prb in self:
            new_outcome = func(outcome)
            if new_outcome in new_pdf.keys():
                new_pdf[new_outcome] += prb
            else:
                new_pdf[new_outcome] = prb
        return Event.from_pdf(new_pdf)
    
    # TODO: Add support for probability of getting < value or > value or between values or among values

# Type aliases for rune/artifact stat values and properties
ValueEvent = Event[int]
PropertyEvent = Event[StatProperty]
SubPropertyEvent = Event[tuple[StatProperty, ...]]
RuneSlotEvent = Event[RuneSlot]
RuneStarsEvent = Event[RuneStars]
RuneSetEvent = Event[RuneSet]
GradeEvent = Event[Grade]
UpgradeEvent = Event[Upgrade]
