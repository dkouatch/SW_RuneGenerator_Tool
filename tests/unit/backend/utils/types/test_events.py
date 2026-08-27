from src.backend.utils.models.types.events import Event

import pytest
import operator as op

from enum import Enum, unique
from src.backend.utils.models.types.events import *
from src.backend.utils.models.enums.stats import StatProperty

@unique
class CoinToss(Enum):
    HEADS = 1
    TAILS = 2

@unique
class DiceRoll(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6

CoinTossEvent = Event[CoinToss]
DiceRollEvent = Event[DiceRoll]

class TestCoinTossEvent:
    @pytest.fixture
    def coin_one(self) -> CoinTossEvent:
        return CoinTossEvent([CoinToss.HEADS, CoinToss.TAILS])
    
    @pytest.fixture
    def coin_two(self) -> CoinTossEvent:
        return CoinTossEvent(
            outcomes=[CoinToss.HEADS, CoinToss.TAILS],
            weights=[0.5, 0.5])

    @pytest.fixture
    def coin_biased(self) -> CoinTossEvent:
        return CoinTossEvent.from_pdf(
            {CoinToss.HEADS: 0.9, CoinToss.TAILS: 0.1})

    @pytest.mark.functional
    def test_coin_one_probabilities(self, coin_one: CoinTossEvent):
        assert coin_one.probabilities == (0.5, 0.5)
    
    @pytest.mark.functional
    def test_coin_two_probabilities(self, coin_two: CoinTossEvent):
        assert coin_two.probabilities == (0.5, 0.5)
    
    @pytest.mark.functional
    def test_coin_biased_probabilities(self, coin_biased: CoinTossEvent):
        assert coin_biased.probabilities == (0.9, 0.1)
    
    @pytest.mark.functional
    def test_coin_one_sample_all(self, coin_one: CoinTossEvent):
        assert set(coin_one.sample(n=2)) == coin_one.outcomes
    
    @pytest.mark.functional
    def test_coin_two_sample_all(self, coin_two: CoinTossEvent):
        assert set(coin_two.sample(n=2)) == coin_two.outcomes
    
    @pytest.mark.functional
    def test_coin_biased_sample_all(self, coin_biased: CoinTossEvent):
        assert set(coin_biased.sample(n=2)) == coin_biased.outcomes
    
    @pytest.mark.functional
    def test_coin_one_and_two_intersect_outcomes(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent):
        coins = coin_one.intersect(coin_two)
        assert coins.outcomes == set([
            (CoinToss.HEADS, CoinToss.HEADS),
            (CoinToss.HEADS, CoinToss.TAILS),
            (CoinToss.TAILS, CoinToss.HEADS),
            (CoinToss.TAILS, CoinToss.TAILS)])
    
    @pytest.mark.functional
    def test_coin_one_and_two_intersect_probabilities(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent):
        coins = coin_one.intersect(coin_two)
        assert coins.probabilities == (1/4, 1/4, 1/4, 1/4)
    
    @pytest.mark.functional
    def test_coin_one_remove_heads(
        self,
        coin_one: CoinTossEvent
    ):
        coin_one.remove([CoinToss.HEADS])
        assert coin_one == CoinTossEvent([CoinToss.TAILS])
    
    @pytest.mark.functional
    def test_coin_one_readd_heads(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent
    ):
        coin_one.rebalance(CoinToss.HEADS, 0.5)
        assert coin_one == coin_two
    
    @pytest.mark.functional
    def test_coin_one_remove_all(
        self,
        coin_one: CoinTossEvent
    ):
        with pytest.raises(ValueError):
            coin_one.remove([CoinToss.HEADS, CoinToss.TAILS])
    
    @pytest.mark.functional
    def test_coin_one_bias(
        self,
        coin_one: CoinTossEvent,
        coin_biased: CoinTossEvent
    ):
        coin_one.rebalance(CoinToss.HEADS, 0.9)
        assert coin_one == coin_biased
    
    @pytest.mark.functional
    def test_coin_one_unbias(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent
    ):
        coin_one.rebalance(CoinToss.HEADS, 0.5)
        assert coin_one == coin_two


class TestDiceRollEvent:
    @pytest.fixture
    def die_one(self) -> DiceRollEvent:
        return DiceRollEvent([DiceRoll.ONE, DiceRoll.TWO, DiceRoll.THREE,
                              DiceRoll.FOUR, DiceRoll.FIVE, DiceRoll.SIX])
    
    @pytest.fixture
    def die_two(self) -> DiceRollEvent:
        return DiceRollEvent(
            outcomes=[DiceRoll.ONE, DiceRoll.TWO, DiceRoll.THREE,
                      DiceRoll.FOUR, DiceRoll.FIVE, DiceRoll.SIX],
            weights=[1/6] * 6)
    
    @pytest.fixture
    def die_biased(self) -> DiceRollEvent:
        return DiceRollEvent.from_pdf(
            {DiceRoll.ONE: 0.1, DiceRoll.TWO: 0.1, DiceRoll.THREE: 0.1,
             DiceRoll.FOUR: 0.1, DiceRoll.FIVE: 0.1, DiceRoll.SIX: 0.5})

    @pytest.mark.functional
    def test_die_one_probabilities(self, die_one: DiceRollEvent):
        assert die_one.probabilities == (1/6, 1/6, 1/6, 1/6, 1/6, 1/6)
    
    @pytest.mark.functional
    def test_die_two_probabilities(self, die_two: DiceRollEvent):
        assert die_two.probabilities == (1/6, 1/6, 1/6, 1/6, 1/6, 1/6)
    
    @pytest.mark.functional
    def test_die_biased_probabilities(self, die_biased: DiceRollEvent):
        assert die_biased.probabilities == (0.1, 0.1, 0.1, 0.1, 0.1, 0.5)
    
    @pytest.mark.functional
    def test_die_one_sample_all(self, die_one: DiceRollEvent):
        assert set(die_one.sample(n=6)) == die_one.outcomes
    
    @pytest.mark.functional
    def test_die_two_sample_all(self, die_two: DiceRollEvent):
        assert set(die_two.sample(n=6)) == die_two.outcomes
    
    @pytest.mark.functional
    def test_die_biased_sample_all(self, die_biased: DiceRollEvent):
        assert set(die_biased.sample(n=6)) == die_biased.outcomes
    
    @pytest.mark.functional
    def test_die_one_remove_one(
        self,
        die_one: DiceRollEvent
    ):
        die_one.remove([DiceRoll.ONE])
        assert die_one == DiceRollEvent([
            DiceRoll.TWO, DiceRoll.THREE, DiceRoll.FOUR,
            DiceRoll.FIVE, DiceRoll.SIX
        ])
    
    @pytest.mark.functional
    def test_die_one_readd_one(
        self,
        die_one: DiceRollEvent,
        die_two: DiceRollEvent
    ):
        die_one.rebalance(DiceRoll.ONE, 1.0 / 6)
        assert die_one == die_two
    
    @pytest.mark.functional
    def test_die_one_remove_all(
        self,
        die_one: DiceRollEvent
    ):
        with pytest.raises(ValueError):
            die_one.remove([
                DiceRoll.ONE, DiceRoll.TWO,
                DiceRoll.THREE, DiceRoll.FOUR,
                DiceRoll.FIVE, DiceRoll.SIX])
    
    @pytest.mark.functional
    def test_die_one_bias(
        self,
        die_one: DiceRollEvent,
        die_biased: DiceRollEvent
    ):
        die_one.rebalance(DiceRoll.SIX, 0.5)
        assert die_one == die_biased
    
    @pytest.mark.functional
    def test_die_one_unbias(
        self,
        die_one: DiceRollEvent,
        die_two: DiceRollEvent
    ):
        die_one.rebalance(DiceRoll.SIX, 1.0 / 6)
        assert die_one == die_two


class TestBadEvents:
    @pytest.mark.functional
    def test_instantiate_no_outcomes(self):
        try:
            Event[int]([])
        except AttributeError as e:
            assert str(e) == "Must enter non-empty outcomes."
            return
        assert False

    @pytest.mark.functional
    def test_instantiate_duplicate_outcomes(self):
        try:
            Event[int]([0, 1, 1])
        except AttributeError as e:
            assert str(e) == "Outcome values must be unique."
            return
        assert False
    
    @pytest.mark.functional
    def test_instantiate_few_outcomes(self):
        try:
            Event[int]([0], [0.4, 0.6])
        except AttributeError as e:
            assert str(e) == "Number of values in outcomes (1) and weights (2) does not match."
            return
        assert False
    
    @pytest.mark.functional
    def test_instantiate_many_outcomes(self):
        try:
            Event[int]([0, 1], [1])
        except AttributeError as e:
            assert str(e) == "Number of values in outcomes (2) and weights (1) does not match."
            return
        assert False

    @pytest.mark.functional
    def test_instantiate_zero_weight(self):
        try:
            Event[int]([0, 1], [0.5, 0])
        except AttributeError as e:
            assert str(e) == "Not all weights are strictly positive."
            return
        assert False

    @pytest.mark.functional
    def test_instantiate_negative_weight(self):
        try:
            Event[int]([0, 1], [0.5, -0.5])
        except AttributeError as e:
            assert str(e) == "Not all weights are strictly positive."
            return
        assert False
    
    @pytest.mark.functional
    def test_delete_nonexistent_outcome(self):
        event = Event[int]([0])
        try:
            del event[1]
        except KeyError as e:
            assert str(e) == '"Outcome \'1\' not in event outcomes."'
            return
        assert False
    
    @pytest.mark.functional
    def test_delete_all_outcomes(self):
        event = Event[int]([0])
        try:
            del event[0]
        except ValueError as e:
            assert str(e) == "Cannot delete the only outcome '0' in the event."
            return
        assert False

    @pytest.mark.functional
    def test_remove_duplicate_outcomes(self):
        event = Event[int]([0, 1])
        try:
            event.remove([1, 1])
        except ValueError as e:
            assert str(e) == "Outcomes [1, 1] contains duplicate entries."
            return
        assert False

    @pytest.mark.functional
    def test_remove_nonexistent_outcome(self):
        event = Event[int]([0])
        try:
            event.remove([1])
        except KeyError as e:
            assert str(e) == "'Outcomes {1} do not exist in event.'"
            return
        assert False
    
    @pytest.mark.functional
    def test_remove_nonexistent_outcome_superset(self):
        event = Event[int]([0, 1])
        try:
            event.remove([1, 2])
        except KeyError as e:
            assert str(e) == "'Outcomes {2} do not exist in event.'"
            return
        assert False
    
    @pytest.mark.functional
    def test_remove_all_outcomes(self):
        event = Event[int]([0, 1])
        try:
            event.remove([0, 1])
        except ValueError as e:
            assert str(e) == "Request for all outcomes to be removed."
            return
        assert False
    
    @pytest.mark.functional
    def test_rebalance_non_probability_negative(self):
        event = Event[int]([0, 1])
        try:
            event.rebalance(0, -1)
        except ValueError as e:
            assert str(e) == "Probability must be in (0,1)."
            return
        assert False
    
    @pytest.mark.functional
    def test_rebalance_non_probability_zero(self):
        event = Event[int]([0, 1])
        try:
            event.rebalance(0, 0)
        except ValueError as e:
            assert str(e) == "Probability must be in (0,1)."
            return
        assert False
    
    @pytest.mark.functional
    def test_rebalance_non_probability_positive(self):
        event = Event[int]([0, 1])
        try:
            event.rebalance(0, 1)
        except ValueError as e:
            assert str(e) == "Probability must be in (0,1)."
            return
        assert False
    
    @pytest.mark.functional
    def test_intersect_zero(self):
        event = Event[int]([0, 1])
        try:
            event.intersect_self(0)
        except ValueError as e:
            assert str(e) == "n must be a positive integer."
            return
        assert False
    
    @pytest.mark.functional
    def test_intersect_negative(self):
        event = Event[int]([0, 1])
        try:
            event.intersect_self(-1)
        except ValueError as e:
            assert str(e) == "n must be a positive integer."
            return
        assert False
    
    @pytest.mark.functional
    def test_sample_zero(self):
        event = Event[int]([0, 1])
        try:
            event.sample(0)
        except ValueError as e:
            assert str(e) == "n must be a positive integer."
            return
        assert False
    
    @pytest.mark.functional
    def test_sample_negative(self):
        event = Event[int]([0, 1])
        try:
            event.sample(-1)
        except ValueError as e:
            assert str(e) == "n must be a positive integer."
            return
        assert False
    
    @pytest.mark.functional
    def test_sample_too_many(self):
        event = Event[int]([0, 1])
        try:
            event.sample(3, replace=False)
        except ValueError as e:
            assert str(e) == "Cannot sample 3 outcomes without replacement from an event with only 2 unique outcomes."
            return
        assert False
    
    @pytest.mark.functional
    def test_sample_event_zero(self):
        event = Event[int]([0, 1])
        try:
            event.sample_event(0)
        except ValueError as e:
            assert str(e) == "n must be at least 1 to form a new event."
            return
        assert False
    
    @pytest.mark.functional
    def test_sample_event_negative(self):
        event = Event[int]([0, 1])
        try:
            event.sample_event(-1)
        except ValueError as e:
            assert str(e) == "n must be at least 1 to form a new event."
            return
        assert False
    
    @pytest.mark.functional
    def test_sample_event_too_many(self):
        event = Event[int]([0, 1])
        try:
            event.sample_event(3, replace=False)
        except ValueError as e:
            assert str(e) == "Cannot sample 3 outcomes without replacement from an event with only 2 unique outcomes."
            return
        assert False
    
    @pytest.mark.functional
    def test_unsortable(self):
        event = Event[int]([0, 1])
        with pytest.raises(TypeError):
            event.sorted()  # pyright: ignore[reportAttributeAccessIssue]
    
    @pytest.mark.functional
    def test_uncounterable(self):
        event = Event[int]([0, 1])
        with pytest.raises(TypeError):
            event.get_event_as_counter()  # pyright: ignore[reportAttributeAccessIssue]
    
    @pytest.mark.functional
    def test_filter_type_mismatch(self):
        event = Event[str](['a', 'b'])
        with pytest.raises(TypeError):
            event.filter(lambda x: x < 0)  # pyright: ignore[reportOperatorIssue]
    
    @pytest.mark.functional
    def test_reduce_op_wrong_type(self):
        event = Event[int]([0, 1])
        with pytest.raises(TypeError):
            event.reduce(op.add)  # pyright: ignore[reportAttributeAccessIssue]
    
    @pytest.mark.functional
    def test_reduce_initial_wrong_type(self):
        event = Event[tuple[int, ...]]([(0, 1), (2, 1)])
        with pytest.raises(TypeError):
            event.reduce(op.add, 'a')  # pyright: ignore[reportArgumentType]
    
    @pytest.mark.functional
    @pytest.mark.skip(reason="Cannot perform strict type-checking over generic classes in Python.")
    def test_event_instantiation_type_mismatch(self):
        with pytest.raises(TypeError):
            event = Event[str]([0, 1])  # pyright: ignore[reportArgumentType]


class TestValueEvent:
    @pytest.fixture
    def value_one(self) -> ValueEvent:
        return ValueEvent([0, 1, 2])
    
    @pytest.fixture
    def value_two(self) -> ValueEvent:
        return ValueEvent([0, 1, 2])
    
    @pytest.fixture
    def value_combined(self) -> ValueEvent:
        return ValueEvent.from_pdf({0: 1/9, 1: 2/9, 2: 3/9, 3: 2/9, 4: 1/9})
      
    @pytest.mark.unit
    def test_values_reduced(
        self,
        value_one: ValueEvent,
        value_two: ValueEvent,
        value_combined: ValueEvent):
        reduced = value_one.intersect(value_two).reduce(op.add)
        assert reduced == value_combined


class TestPropertyEvent:
    pass


class TestSubPropertyEvent:
    pass


class TestRuneSlotEvent:
    pass


class TestRuneStarsEvent:
    pass


class TestRuneSetEvent:
    pass


class TestGradeEvent:
    pass


class TestUpgradeEvent:
    pass
