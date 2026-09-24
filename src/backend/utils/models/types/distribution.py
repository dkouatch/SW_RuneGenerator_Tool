from __future__ import annotations

import math
import numpy as np
import itertools
import operator

from functools import reduce
from typing import Generic, TypeVar, Callable, cast, overload, override
from typeguard import typechecked
from collections.abc import Sequence, Hashable, Iterable

from src.backend.utils.models.types.general import *

T = TypeVar(name='T', bound=Hashable)

# TODO: Set up distribution / set of outcomes for each dungeon rune set (don't forget intangible)

@typechecked
class Distribution(Generic[T]):
    """Generic distribution class for SW items that models Random Variables.

    The core field of this class is the `pdf : dict[T, float]` field
    that represents a probability density function for `outcomes : T`
    in the distribution.

    The class supports standard probability operations such as random
    sampling, distribution union and intersection, along with functional
    operations like reduce, map, and filtering.
    """

    def __init__(
        self,
        outcomes: Sequence[T],
        weights: Sequence[float | int] | None = None) -> None:
        """Primary constructor

        Note: weights are normalized

        Args:
            outcomes (Sequence[T]): list of distribution outcomes
            weights (Sequence[float | int] | None): weights of each outcome
        """
        self._check_args(outcomes, weights)
        if weights is None:
            probabilities = (1.0 / len(outcomes) for _ in outcomes)
        else:
            probabilities = (weight / sum(weights) for weight in weights)
        self._pdf: dict[T, float] = dict(zip(outcomes, probabilities))
        print(f"Created Distribution over type {type(next(iter(outcomes)))}")
    
    @classmethod
    def from_pdf(cls, pdf: dict[T, float | int]) -> Distribution[T]:
        """Secondary constructor

        Args:
            pdf (dict[T, float]): Designated probability density function
        Returns:
            Distribution[T]: distribution object
        """
        return cls(list(pdf.keys()), list(pdf.values()))
    
    def _check_args(
            self,
            outcomes: Sequence[T],
            weights: Sequence[float] | None) -> None:
        """Checks for the following constraints on object initialization:
        1. Outcomes exist and are unique
        2. Weights are strictly positive
        3. Number of provided outcomes and weights match

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
        return self[outcome] > 0 and not math.isclose(self[outcome], 0)
    
    def __getitem__(self, outcome: T) -> float:
        return self.pdf.get(outcome, 0.0)
    
    def __iter__(self):
        return iter(self.pdf.items())
    
    def __copy__(self) -> Distribution[T]:
        return Distribution[T].from_pdf(self.pdf.copy())
    
    @override
    def __eq__(self, other: object):
        """Equality function for Distribution Class

        Args:
            other (object)
        Returns:
            bool: True only if two distributions have same set of outcomes with equal probabilities
        """
        if isinstance(other, Distribution):
            if self.captured_type == other.captured_type:
                other_distribution: Distribution[T] = cast(Distribution[T], other)
                if self.outcomes != other_distribution.outcomes:
                    return False
                for outcome in self.outcomes:
                    if not math.isclose(self[outcome], other_distribution[outcome]):
                        return False
                return True
        return NotImplemented
    
    @override
    def __hash__(self) -> int:
        return hash((self.outcomes, self.probabilities))
    
    def __delitem__(self, key: T) -> None:
        """Delete Item function for the Distribution class

        If outcome exists, removes outcome and re-normalizes probabilities

        Args:
            key (T): Outcome to delete

        Raises:
            KeyError: Outcome does not exist
            ValueError: Attempt to delete distribution's only outcome
        """
        if key not in self.outcomes:
            raise KeyError(f"Outcome '{key}' not in distribution outcomes.")
        total = sum(self.probabilities)
        if total - self[key] <= 0 or math.isclose(total, self[key]):
            raise ValueError(f"Cannot delete the only outcome '{key}' in the distribution.")
        
        total -= self[key]
        del self.pdf[key]
        self._pdf = {
            outcome: prb / total for outcome, prb in self}
    
    def remove(self, outcomes: Sequence[T]) -> None:
        """Removes outcomes from the distribution

        Args:
            outcomes (Sequence[T]): Outcomes to remove
        Raises:
            KeyError: There exists outcomes that don't exist in the distribution
            ValueError: Input outcomes contains duplicate entries
            ValueError: Outcomes are all outcomes in the distribution
        """
        if len(set(outcomes)) != len(outcomes):
            raise ValueError("Provided outcomes contains duplicates.")
        elif self.outcomes == set(outcomes):
            raise ValueError("Request for all outcomes to be removed.")
        elif not self.outcomes.issuperset(outcomes):
            raise KeyError("Subset of provided outcomes do not exist in distribution.")

        for outcome in outcomes:
            if outcome in self.outcomes:
                del self[outcome]
    
    def rebalance(self, outcome: T, probability: float) -> None:
        """Rebalances the distribution around an outcome.
        
        Sets the probability of an outcome to a specific probability
        and renormalizes the rest of the outcomes according to the
        remaining probability.

        Args:
            outcome (T): Outcome to rebalance or to add to the distribution
            probability (float): New probability for the outcome
        Raises:
            KeyError: If outcome argument doesn't exist in the distribution
            ValueError: If the new probability is not in (0,1)
            ValueError: If distribution only has one outcome
        """
        if outcome not in self.outcomes:
            raise KeyError(f"Outcome '{outcome}' does not exist in this distribution.")
        elif not (0 < probability < 1):
            raise ValueError("Probability must be in (0,1).")
        
        other_outcomes = self.outcomes - {outcome}
        total = sum(self.probabilities) - self[outcome]
        if total <= 0 or math.isclose(total, 0):
            raise ValueError("Cannot rebalance an distribution with only one outcome.")
        constant = (1 - probability) / total

        for other_outcome in other_outcomes:
            self.pdf[other_outcome] *= constant
        self.pdf[outcome] = probability
    
    def intersect[V: Hashable](self, other: Distribution[V]) -> Distribution[tuple[T, V]]:
        """Returns the intersection of two distributions

        Effectively the cartesian product of `Distribution[T]` and `Distribution[V]`.

        Args:
            other (Distribution[V]): Other distribution to intersect with
        Returns:
            Distribution[(T, V)]: New distribution with outcomes as tuples of the two distributions' outcomes
        """
        new_pdf: dict[tuple[T, V], float] = {}
        for outcome1, prb1 in self:
            for outcome2, prb2 in other:
                new_pdf[(outcome1, outcome2)] = prb1 * prb2
        return Distribution[tuple[T, V]].from_pdf(new_pdf)
    
    def intersect_self(self, n: int) -> Distribution[tuple[T, ...]]:
        """Intersects the distribution with itself n times

        Args:
            n (int): Number of times to intersect with itself
        Raises:
            ValueError: n < 1
        Returns:
            Distribution[tuple[T, ...]]: New distribution with outcomes as tuples of the original distribution
        """
        if n < 1:
            raise ValueError("n must be a positive integer.")
        elif n == 1:
            this_new_pdf: dict[tuple[T], float] = {(outcome,): prb for outcome, prb in self}
            return Distribution[tuple[T]].from_pdf(this_new_pdf)
        else:
            new_outcomes = itertools.product(self.outcomes, repeat=n)
            new_pdf: dict[tuple[T, ...], float] = {}
            for new_outcome in new_outcomes:
                new_pdf[new_outcome] = reduce(
                    operator.mul,
                    (self[outcome] for outcome in new_outcome),
                    1.0)
            return Distribution[tuple[T, ...]].from_pdf(new_pdf)
    
    def sample(self, n: int=1, replace: bool=False) -> tuple[T, ...]:
        """Samples n outcomes from the distribution without replacement

        Args:
            n (int, optional): sample size. Defaults to 1.
            replace (bool, optional): whether to sample with replacement. Defaults to False.
        Raises:
            ValueError: n < 1
            ValueError: Sampling without replacement when n is greater than the number of outcomes
        Returns:
            tuple[T, ...]: tuple of sampled outcomes
        """
        if n < 1:
            raise ValueError("n must be a positive integer.")
        elif n > len(self.outcomes) and replace is False:
            raise ValueError(
                f"Cannot sample {n} outcomes without replacement from an " +
                f"distribution with only {len(self.outcomes)} unique outcomes.")

        outcomes = np.array(list(self.outcomes), dtype=object)
        probabilities = np.array(list(self.probabilities), dtype=float)
        if n == 1:
            sample: T = np.random.choice(outcomes, p=probabilities)
            return (sample,)
        else:
            samples = np.random.choice(outcomes, p=probabilities, size=n, replace=replace)
            samples = tuple[T, ...](samples)
            return samples
    
    def sample_distribution(self, n: int, replace: bool=False) -> Distribution[tuple[T, ...]]:
        """Choose n outcomes without replacement and returns a new distribution with those outcomes

        Args:
            n (int): sample size must be at least 1.
            replace (bool, optional): whether to sample with replacement. Defaults to False.
        Raises:
            ValueError: n < 1
            ValueError: Sampling without replacement when n is greater than the number of outcomes
        Returns:
            Distribution[tuple[T, ...]]: Distribution representing possibilities from sampling n outcomes
        """
        if n < 1:
            raise ValueError("n must be at least 1 to form a new distribution.")
        else:
            if replace:
                new_distribution = self.intersect_self(n)
                return new_distribution
            else:
                # TODO: Implement without replacement (choose n)
                if n > len(self.outcomes):
                    raise ValueError(
                        f"Cannot sample {n} outcomes without replacement from an " +
                        f"distribution with only {len(self.outcomes)} unique outcomes.")
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
                    return Distribution[tuple[T, ...]].from_pdf(new_pdf)
    
    def sorted[V: SortableHashable](self: Distribution[tuple[V, ...]]) -> Distribution[tuple[V, ...]]:
        """Creates new distribution where outcomes that are previously unsorted tuples become sorted

        NOTE: A sorted distribution should not be manipulated in the same manner as normal distributions

        Returns:
            Distribution[tuple[SortableHashable, ...]]: Distribution of set outcomes instead of tuples
        """
        new_pdf: dict[tuple[V, ...], float] = {}
        for outcome, prb in self:
            s_outcome = tuple(sorted(outcome))
            if s_outcome in new_pdf.keys():
                new_pdf[s_outcome] += prb
            else:
                new_pdf[s_outcome] = prb
        return Distribution[tuple[V, ...]].from_pdf(new_pdf)
    
    def to_counter[V: Hashable](self: Distribution[tuple[V, ...]]) -> Distribution[HashableCounter[V]]:
        """Creates new distribution where outcomes that are tuples over type V
        are converted into counter objects over type V.

        E.g., `('apple', 'orange', 'banana', 'orange', 'apple') -> {'apple': 2, 'banana': 1, 'orange': 2}`

        Returns:
            Distribution[HashableCounter[V]]: Distribution of counter outcomes instead of tuples
        """
        new_pdf: dict[HashableCounter[V], float] = {}
        for outcome, prb in self:
            c_outcome: HashableCounter[V] = HashableCounter[V](outcome)
            if c_outcome in new_pdf.keys():
                new_pdf[c_outcome] += prb
            else:
                new_pdf[c_outcome] = prb
        return Distribution[HashableCounter[V]].from_pdf(new_pdf)
    
    def filter(self, func: Callable[[T], bool]) -> Distribution[T] | None:
        """Narrows the distribution outcomes using a predicate function

        Args:
            func (Callable[[T], bool]): Predicate function to filter outcomes
        Returns:
            None: No outcome matches the filter
            Distribution[T]: New distribution with filtered outcomes
        """
        new_pdf: dict[T, float] = {outcome: prb for outcome, prb in self if func(outcome)}
        return None if not new_pdf else Distribution[T].from_pdf(new_pdf)
    
    def filter_by_probability(self, func: Callable[[float], bool]) -> Distribution[T] | None:
        """Narrows the distribution outcomes by their corresponding probability using a predicate function

        Args:
            func (Callable[[float], bool]): Predicate function to filter probabilities
        Returns:
            None: No outcome probability matches the filter
            Distribution[T]: New distribution with filtered outcomes
        """
        return self.filter(lambda outcome: func(self[outcome]))
    
    def query(self, func: Callable[[T], bool]) -> float:
        """Returns probability based on querying of the distribution

        Args:
            func (Callable[[T], bool]): Query of interest
        Returns:
            float: Probability of query occurring
        """
        return sum(prb for outcome, prb in self if func(outcome))
    
    @overload
    def reduce[V: Hashable](
        self: Distribution[tuple[V, ...]],
        op: Callable[[V, V], V]) -> Distribution[V]: ...

    @overload
    def reduce[U: Hashable, V: Hashable](
        self: Distribution[tuple[U, ...]],
        op: Callable[[V, U], V],
        initial: V) -> Distribution[V]: ...
    
    def reduce[V: Hashable](
            self: Distribution[tuple[Hashable, ...]],
            op,
            initial: V | None = None) -> Distribution[V]:
        """Tries to reduce the distribution if outcomes are tuples using a folding function.
        Effectively folds sequences of smaller distributions into a meaningful, aggregate representation.

        The folding operation is left-associative:
        
        `f ( f ( ... f(z, 1) ...), n-1), n)`

        Args:
            op (Callable[[V, V], V] | Callable[[V, U], V]): Folding function to apply to the outcomes
            initial (V | None): Initial folding value
        Returns:
            Distribution[V]: None if distribution type is not a sequence, otherwise a new distribution with reduced outcomes
        """
        new_pdf: dict[V, float] = {}
        if initial is not None:
            for outcome, prb in self:
                if (s := reduce(op, outcome, initial)) in new_pdf.keys():
                    new_pdf[s] += prb
                else:
                    new_pdf[s] = prb
            return Distribution[V].from_pdf(new_pdf)
        else:
            for outcome, prb in self:
                outcome = cast(tuple[V, ...], outcome)
                if (s := reduce(op, outcome)) in new_pdf.keys():
                    new_pdf[s] += prb
                else:
                    new_pdf[s] = prb
            return Distribution[V].from_pdf(new_pdf)
    
    def map[V: Hashable](
            self,
            func: Callable[[T], V]) -> Distribution[V]:
        """Maps the outcomes of the distribution to a new type using a mapping function

        Args:
            func (Callable[[T], V]): Function to apply to each outcome
        Returns:
            Distribution[V]: New distribution with mapped outcomes
        """
        new_pdf: dict[V, float] = {}
        for outcome, prb in self:
            new_outcome = func(outcome)
            if new_outcome in new_pdf.keys():
                new_pdf[new_outcome] += prb
            else:
                new_pdf[new_outcome] = prb
        return Distribution[V].from_pdf(new_pdf)


def intersect_over(distributions: Iterable[Distribution]) -> Distribution[tuple]:
    """Returns the intersection of an arbitrary number of distributions

    Effectively the cartesian product of all these distributions

    Args:
        distributions (Iterable[Distribution]): Some iterable sequence of distributions
    Returns:
        Distribution[tuple]: New distribution with outcomes as tuples over combined distribution oucomes
    Raises:
        ValueError: distributions arg has size/len 0
    """
    if (num_distributions := len(list(distributions))) == 0:
        raise ValueError("Cannot intersect over no distributions")
    new_pdf: dict[tuple, float] = {}
    num_outcomes_per_distribution = [len(distribution.outcomes) for distribution in distributions]
    outcome_index_per_distribution = {i: 0 for i in range(num_distributions)}
    distribution_list = list(distributions)

    def dfs(distribution_index, outcomes_list, outcomes_prb):
        # Leaf node: have iterated through all distributions
        if distribution_index >= num_distributions:
            new_pdf[tuple(outcomes_list)] = outcomes_prb
            return
        # Non-leaf node: iterate through outcomes of this distribution
        for outcome, prb in distribution_list[distribution_index]:
            dfs(distribution_index + 1, outcomes_list + [outcome], outcomes_prb * prb)
    dfs(0, [], 1.0)
    return Distribution[tuple].from_pdf(new_pdf)
