from __future__ import annotations

import random
from functools import reduce
from typing import Iterable, Optional, TypeVar, Hashable, Union, Sequence, Callable

from src.utils.enums.stats import StatProperty

T = TypeVar('T', bound=Hashable)
V = TypeVar('V', bound=Hashable)

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
            elif abs(sum(probabilities) - 1) > 0.0001:
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
        for outcome1, prb1 in self.pdf.items():
            for outcome2, prb2 in other.pdf.items():
                new_pdf[(outcome1, outcome2)] = prb1 * prb2
        return Event.from_pdf(new_pdf)
    
    def rand(self) -> T:
        return random.choices(self.pdf.keys(), weights=self.pdf.values())
    
    def reduce(
            self,
            op : Callable[[Hashable, Hashable], Hashable]) -> Optional[Event[Hashable]]:
        """Tries to reduce the event if it is a sequence of smaller events using a folding function

        Args:
            op (Callable[[Hashable, Hashable], Hashable]): Folding function to apply to the outcomes
        Returns:
            Optional[Event[Hashable]]: None if event type is not a sequence, otherwise a new event with reduced outcomes
        """
        if isinstance(T, tuple[Hashable]):
            new_pdf = {}
            for outcome, prb1 in self.pdf.items():
                if (s := reduce(op, outcome)) in new_pdf.keys():
                    new_pdf[s] += prb1
                else:
                    new_pdf[s] = prb1
            return Event.from_pdf(new_pdf)


class UnionEvent:
    """Event class that represents the union of multiple events

    Supports union operations and provides cumulative distribution function (CDF) for the union of events.
    """
    def __init__(self, events: Iterable[Event]):
        self._cdf = {}
        for event in events:
            for outcome, prb in event.pdf.items():
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
    
    def union(self, other: UnionEvent):
        """Unions this event with another UnionEvent
        Args:
            other (UnionEvent): Another UnionEvent to union with
        """
        for outcome, density in other.cdf:
            if outcome in self.cdf.keys():
                self.cdf[outcome] += density
            else:
                self.cdf[outcome] = density

# Type aliases for rune/artifact stat values and properties
ValueEvent = Union[Event[int], Event[Sequence[int]]]
PropertyEvent = Union[Event[StatProperty], Event[Sequence[StatProperty]]]
