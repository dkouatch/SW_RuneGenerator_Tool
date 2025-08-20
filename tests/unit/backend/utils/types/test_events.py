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
    def coin_one(self):
        return CoinTossEvent([CoinToss.HEADS, CoinToss.TAILS])
    
    @pytest.fixture
    def coin_two(self):
        return CoinTossEvent(
            outcomes=[CoinToss.HEADS, CoinToss.TAILS],
            probabilities=[0.5, 0.5])

    @pytest.fixture
    def coin_biased(self):
        return CoinTossEvent.from_pdf(
            {CoinToss.HEADS: 0.9, CoinToss.TAILS: 0.1})

    @pytest.mark.functional
    def test_coin_one_probabilities(self, coin_one):
        assert coin_one.probabilities == (0.5, 0.5)
    
    @pytest.mark.functional
    def test_coin_two_probabilities(self, coin_two):
        assert coin_two.probabilities == (0.5, 0.5)
    
    @pytest.mark.functional
    def test_coin_biased_probabilities(self, coin_biased):
        assert coin_biased.probabilities == (0.9, 0.1)
    
    @pytest.mark.functional
    def test_coin_one_and_two_union_outcomes(self, coin_one, coin_two):
        coins = coin_one.union(coin_two)
        assert coins.outcomes == set((CoinToss.HEADS, CoinToss.TAILS))
    
    @pytest.mark.functional
    def test_coin_one_and_two_union_densities(self, coin_one, coin_two):
        coins = coin_one.union(coin_two)
        assert coins.densities == (1, 1)
    
    @pytest.mark.functional
    def test_coin_one_and_two_intersect_outcomes(self, coin_one, coin_two):
        coins = coin_one.intersect(coin_two)
        assert coins.outcomes == set([
            (CoinToss.HEADS, CoinToss.HEADS),
            (CoinToss.HEADS, CoinToss.TAILS),
            (CoinToss.TAILS, CoinToss.HEADS),
            (CoinToss.TAILS, CoinToss.TAILS)])
    
    @pytest.mark.functional
    def test_coin_one_and_two_intersect_probabilities(self, coin_one, coin_two):
        coins = coin_one.intersect(coin_two)
        assert coins.probabilities == (1/4, 1/4, 1/4, 1/4)


class TestDiceRollEvent:
    @pytest.fixture
    def die_one(self):
        return DiceRollEvent([DiceRoll.ONE, DiceRoll.TWO, DiceRoll.THREE,
                              DiceRoll.FOUR, DiceRoll.FIVE, DiceRoll.SIX])
    
    @pytest.fixture
    def die_two(self):
        return DiceRollEvent(
            outcomes=[DiceRoll.ONE, DiceRoll.TWO, DiceRoll.THREE,
                      DiceRoll.FOUR, DiceRoll.FIVE, DiceRoll.SIX],
            probabilities=[1/6] * 6)
    
    @pytest.fixture
    def die_biased(self):
        return DiceRollEvent.from_pdf(
            {DiceRoll.ONE: 0.1, DiceRoll.TWO: 0.1, DiceRoll.THREE: 0.1,
             DiceRoll.FOUR: 0.1, DiceRoll.FIVE: 0.1, DiceRoll.SIX: 0.5})

    @pytest.mark.functional
    def test_die_one_probabilities(self, die_one):
        assert die_one.probabilities == (1/6, 1/6, 1/6, 1/6, 1/6, 1/6)
    
    @pytest.mark.functional
    def test_die_two_probabilities(self, die_two):
        assert die_two.probabilities == (1/6, 1/6, 1/6, 1/6, 1/6, 1/6)
    
    @pytest.mark.functional
    def test_die_biased_probabilities(self, die_biased):
        assert die_biased.probabilities == (0.1, 0.1, 0.1, 0.1, 0.1, 0.5)


class TestValueEvent:
    @pytest.fixture
    def value_one(self) -> ValueEvent:
        return Event[int]([0, 1, 2])
    
    @pytest.fixture
    def value_two(self) -> ValueEvent:
        return Event[int]([0, 1, 2])
    
    @pytest.fixture
    def value_combined(self) -> ValueEvent:
        return Event[int].from_pdf({0: 1/9, 1: 2/9, 2: 3/9, 3: 2/9, 4: 1/9})
    
    @pytest.mark.unit
    def test_values_reduced(self, value_one, value_two, value_combined):
        reduced = value_one.intersect(value_two).reduce(op.add)
        assert reduced == value_combined

class TestPropertyEvent:
    pass
