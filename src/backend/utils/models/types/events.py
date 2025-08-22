from __future__ import annotations

import numpy as np
from functools import reduce
from typing import Iterable, Optional, TypeVar, Hashable, Union, Sequence, Callable, TypeGuard

from backend.utils.enums.stats import StatProperty

T = TypeVar('T', bound=Hashable)
V = TypeVar('V', bound=Hashable)
ERROR = 0.0001  # Tolerance for floating point comparisons

class Event[T]:
    """Generic event class for SW items

    Contains underlying probability density function and supports
    random outcome selection, event unions, and event intersections.
    """

    def __init__(
            self,
            outcomes: Iterable[T],
            probabilities: Optional[Iterable[float | int]] = None):
        """Primary constructor

        Args:
            outcomes (Iterable[T]): list of event outcomes
            probabilities (Optional[Iterable[float  |  int]]): probabilities of each outcome
        """
        self._check_args(outcomes, probabilities)
        if probabilities is None:
            probabilities = (1.0 / len(outcomes) for _ in outcomes)
        self._pdf = dict(zip(outcomes, probabilities))
    
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
            probabilities: Optional[Iterable[float]]) -> None:
        """Checks for the following constraints on object initialization:
        1. Outcomes exist and are unique
        2. Probabilities are in [0,1] and sum to 1 (with some error allowed)

        Args:
            outcomes (Iterable[T]): Outcomes provided in initialization
            probabilities (Optional[Iterable[float]]): Probabilities provided in initialization
        Raises:
            AttributeError: does not adhere to one of the constraints
        """
        if len(outcomes) == 0:
            raise AttributeError("Must enter non-empty outcomes.")
        if len(outcomes) != len(set(outcomes)):
            raise AttributeError("outcomes values must be unique.")
        if probabilities:
            if len(outcomes) != len(probabilities):
                raise AttributeError(
                    f"Number of values in outcomes ({len(outcomes)}) and " 
                    f"probabilities ({len(probabilities)}) does not match."
                )
            elif not all(0 <= prb <= 1 for prb in probabilities):
                raise AttributeError("Not all probabilities are in [0,1]")
            elif abs(sum(probabilities) - 1) > ERROR:
                raise AttributeError(f"Probabilities do not sum to 1 but to {sum(probabilities)} instead")
    
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
        return outcome in self.pdf.keys()
    
    def __getitem__(self, outcome: T) -> float:
        return self.pdf.get(outcome, 0.0)
    
    def __iter__(self):
        return iter(self.pdf.items())
    
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
        self.pdf = {
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
    
    def union(self, other: Event[V]) -> UnionEvent:
        return UnionEvent([self, other])
    
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
        return np.random.choice(list(self.outcomes), p=self.probabilities, size=n, replace=replace)
    
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


class UnionEvent:
    """Event class that represents the union of multiple events

    Supports union operations and provides cumulative distribution function (CDF) for the union of events.
    """
    def __init__(self, events: Iterable[Event]):
        self._cdf = {}
        for event in events:
            for outcome, prb in event:
                if outcome in self.cdf.keys():
                    self._cdf[outcome] += prb
                else:
                    self._cdf[outcome] = prb
        self.events = events
    
    @property
    def outcomes(self) -> set[Event]:
        return set(self.cdf.keys())
    
    @property
    def densities(self) -> list[float]:
        return tuple(self.cdf.values())
    
    @property
    def cdf(self) -> dict[Event, float]:
        return self._cdf
    
    def __contains__(self, outcome: T):
        return outcome in self.pdf.keys()
    
    def __getitem__(self, outcome: Event) -> float:
        return self.cdf.get(outcome, 0.0)
    
    def __iter__(self):
        return iter(self.cdf.items())
    
    def union(self, other: UnionEvent):
        """Unions this event with another UnionEvent
        Args:
            other (UnionEvent): Another UnionEvent to union with
        """
        for outcome, density in other:
            if outcome in self.cdf.keys():
                self.cdf[outcome] += density
            else:
                self.cdf[outcome] = density

# Type aliases for rune/artifact stat values and properties
ValueEvent = Event[int]
PropertyEvent = Event[StatProperty]
