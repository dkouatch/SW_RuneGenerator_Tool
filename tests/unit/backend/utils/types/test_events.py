import pytest
import operator as op

from enum import Enum, unique
from src.backend.utils.types.events import Event, ValueEvent, PropertyEvent
from src.backend.utils.enums.stats import StatProperty

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
            probabilities=[0.5, 0.5])

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
    def test_coin_one_and_two_union_outcomes(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent):
        coins = coin_one.union(coin_two)
        assert coins.outcomes == set((CoinToss.HEADS, CoinToss.TAILS))
    
    @pytest.mark.functional
    def test_coin_one_and_two_union_densities(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent):
        coins = coin_one.union(coin_two)
        assert coins.densities == (1, 1)
    
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
            probabilities=[1/6] * 6)
    
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
