from src.backend.utils.models.types.events import Event

import pytest
import operator as op

from enum import IntEnum, unique
from src.backend.utils.models.types.events import *
from src.backend.utils.models.enums.stats import StatProperty

@unique
class CoinToss(IntEnum):
    HEADS = 1
    TAILS = 2

@unique
class DiceRoll(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6

CoinTossEvent = Event[CoinToss]
DiceRollEvent = Event[DiceRoll]

@pytest.mark.unit
class TestCoinTossEvent:
    @pytest.fixture
    def coin_one(self) -> CoinTossEvent:
        return CoinTossEvent([CoinToss.HEADS, CoinToss.TAILS])
    
    @pytest.fixture
    def coin_two(self) -> CoinTossEvent:
        return CoinTossEvent(
            outcomes=[CoinToss.TAILS, CoinToss.HEADS],
            weights=[0.5, 0.5])

    @pytest.fixture
    def coin_biased(self) -> CoinTossEvent:
        return CoinTossEvent.from_pdf(
            {CoinToss.HEADS: 0.9, CoinToss.TAILS: 0.1})
    
    # --------------
    # Event.outcomes
    # --------------
    def test_coin_one_outcomes(self, coin_one: CoinTossEvent):
        assert coin_one.outcomes == {CoinToss.HEADS, CoinToss.TAILS}
    
    def test_coin_two_outcomes(self, coin_two: CoinTossEvent):
        assert coin_two.outcomes == {CoinToss.HEADS, CoinToss.TAILS}
    
    def test_coin_biased_outcomes(self, coin_biased: CoinTossEvent):
        assert coin_biased.outcomes == {CoinToss.HEADS, CoinToss.TAILS}

    # -------------------
    # Event.probabilities
    # -------------------
    def test_coin_one_probabilities(self, coin_one: CoinTossEvent):
        assert coin_one.probabilities == (0.5, 0.5)
    
    def test_coin_two_probabilities(self, coin_two: CoinTossEvent):
        assert coin_two.probabilities == (0.5, 0.5)
    
    def test_coin_biased_probabilities(self, coin_biased: CoinTossEvent):
        assert coin_biased.probabilities == (0.9, 0.1)
    
    # --------------
    # Event.remove()
    # --------------
    def test_coin_one_remove_heads(
        self,
        coin_one: CoinTossEvent
    ):
        coin_one.remove([CoinToss.HEADS])
        assert coin_one == CoinTossEvent([CoinToss.TAILS])
    
    def test_coin_one_remove_all(
        self,
        coin_one: CoinTossEvent
    ):
        with pytest.raises(ValueError):
            coin_one.remove([CoinToss.HEADS, CoinToss.TAILS])
    
    # --------------
    # Event.rebalance()
    # --------------
    def test_coin_one_bias(
        self,
        coin_one: CoinTossEvent,
        coin_biased: CoinTossEvent
    ):
        coin_one.rebalance(CoinToss.HEADS, 0.9)
        assert coin_one == coin_biased
    
    def test_coin_biased_unbias(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent,
        coin_biased: CoinTossEvent
    ):
        coin_biased.rebalance(CoinToss.HEADS, 0.5)
        assert coin_biased == coin_one
        assert coin_biased == coin_two
    
    # -----------------
    # Event.intersect()
    # -----------------
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
    
    def test_coin_one_and_two_intersect_probabilities(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent):
        coins = coin_one.intersect(coin_two)
        assert coins.probabilities == (1/4, 1/4, 1/4, 1/4)
    
    def test_coin_one_and_two_intersect_commutative(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent):
        assert coin_one.intersect(coin_two) == coin_two.intersect(coin_one)
    
    # ----------------------
    # Event.intersect_self()
    # ----------------------
    def test_coin_one_intersect_self_once(
        self,
        coin_one: CoinTossEvent
    ):
        coin_one_intersected = coin_one.intersect_self(1)
        truth_coin = Event[tuple[CoinToss]](
            outcomes=[(CoinToss.HEADS,), (CoinToss.TAILS,)])
        assert coin_one_intersected == truth_coin
    
    def test_coin_two_intersect_self_once(
        self,
        coin_two: CoinTossEvent
    ):
        coin_two_intersected = coin_two.intersect_self(1)
        truth_coin = Event[tuple[CoinToss]](
            outcomes=[(CoinToss.HEADS,), (CoinToss.TAILS,)])
        assert coin_two_intersected == truth_coin
    
    def test_coin_one_intersect_self_twice(
        self,
        coin_one: CoinTossEvent
    ):
        coin_one_intersected = coin_one.intersect_self(2)
        truth_coin = Event[tuple[CoinToss, CoinToss]].from_pdf({
            (CoinToss.HEADS, CoinToss.HEADS): 0.25,
            (CoinToss.HEADS, CoinToss.TAILS): 0.25,
            (CoinToss.TAILS, CoinToss.HEADS): 0.25,
            (CoinToss.TAILS, CoinToss.TAILS): 0.25})
        assert coin_one_intersected == truth_coin

    def test_coin_two_intersect_self_twice(
        self,
        coin_two: CoinTossEvent
    ):
        coin_two_intersected = coin_two.intersect_self(2)
        truth_coin = Event[tuple[CoinToss, CoinToss]].from_pdf({
            (CoinToss.HEADS, CoinToss.HEADS): 0.25,
            (CoinToss.HEADS, CoinToss.TAILS): 0.25,
            (CoinToss.TAILS, CoinToss.HEADS): 0.25,
            (CoinToss.TAILS, CoinToss.TAILS): 0.25})
        assert coin_two_intersected == truth_coin

    # --------------
    # Event.sample()
    # --------------
    def test_coin_one_sample_all(self, coin_one: CoinTossEvent):
        assert set(coin_one.sample(n=2)) == coin_one.outcomes
    
    def test_coin_two_sample_all(self, coin_two: CoinTossEvent):
        assert set(coin_two.sample(n=2)) == coin_two.outcomes
    
    def test_coin_biased_sample_all(self, coin_biased: CoinTossEvent):
        assert set(coin_biased.sample(n=2)) == coin_biased.outcomes
    
    # --------------------
    # Event.sample_event()
    # --------------------
    def test_coin_one_sample_one_event(
        self,
        coin_one: CoinTossEvent
    ):
        coin_one_sampled = coin_one.sample_event(1)
        truth_coin = Event[tuple[CoinToss]](
            outcomes=[(CoinToss.HEADS,), (CoinToss.TAILS,)])
        assert coin_one_sampled == truth_coin
    
    def test_coin_two_sample_one_event(
        self,
        coin_two: CoinTossEvent
    ):
        coin_two_sampled = coin_two.sample_event(1)
        truth_coin = Event[tuple[CoinToss]](
            outcomes=[(CoinToss.HEADS,), (CoinToss.TAILS,)])
        assert coin_two_sampled == truth_coin
    
    def test_coin_one_sample_two_events(
        self,
        coin_one: CoinTossEvent
    ):
        coin_one_sampled = coin_one.sample_event(2, replace=True)
        truth_coin = Event[tuple[CoinToss, CoinToss]].from_pdf({
            (CoinToss.HEADS, CoinToss.HEADS): 0.25,
            (CoinToss.HEADS, CoinToss.TAILS): 0.25,
            (CoinToss.TAILS, CoinToss.HEADS): 0.25,
            (CoinToss.TAILS, CoinToss.TAILS): 0.25})
        assert coin_one_sampled == truth_coin

    def test_coin_two_sample_two_events(
        self,
        coin_two: CoinTossEvent
    ):
        coin_two_sampled = coin_two.sample_event(n=2, replace=True)
        truth_coin = Event[tuple[CoinToss, CoinToss]].from_pdf({
            (CoinToss.HEADS, CoinToss.HEADS): 0.25,
            (CoinToss.HEADS, CoinToss.TAILS): 0.25,
            (CoinToss.TAILS, CoinToss.HEADS): 0.25,
            (CoinToss.TAILS, CoinToss.TAILS): 0.25})
        assert coin_two_sampled == truth_coin
    
    def test_coin_biased_sample_two_events_without_replacement(
        self,
        coin_biased: CoinTossEvent
    ):
        coin_biased_sampled = coin_biased.sample_event(n=2, replace=False)
        print(coin_biased_sampled._pdf)
        assert coin_biased_sampled == Event[tuple[CoinToss, CoinToss]].from_pdf({
            (CoinToss.HEADS, CoinToss.TAILS): 0.9,
            (CoinToss.TAILS, CoinToss.HEADS): 0.1,
        })

    
    # --------------
    # Event.sorted()
    # --------------
    def test_coin_explicitly_sorted(self):
        coin_flips = Event[tuple[CoinToss, CoinToss]]([
            (CoinToss.HEADS, CoinToss.TAILS),
            (CoinToss.TAILS, CoinToss.HEADS),
            (CoinToss.TAILS, CoinToss.TAILS)
        ])
        assert (
            coin_flips.sorted() ==  # pyright: ignore[reportAttributeAccessIssue]
            Event[tuple[CoinToss, CoinToss]].from_pdf({
                (CoinToss.HEADS, CoinToss.TAILS): 2/3,
                (CoinToss.TAILS, CoinToss.TAILS): 1/3
            })
        )

    def test_coin_one_intersect_and_sort(
        self,
        coin_one: CoinTossEvent):
        coin_intersected = coin_one.intersect_self(n=3)
        assert (
            coin_intersected.sorted() ==  # pyright: ignore[reportAttributeAccessIssue]
            Event[tuple[CoinToss, CoinToss, CoinToss]].from_pdf({
                (CoinToss.HEADS, CoinToss.HEADS, CoinToss.HEADS): 0.125,
                (CoinToss.HEADS, CoinToss.HEADS, CoinToss.TAILS): 0.375,
                (CoinToss.HEADS, CoinToss.TAILS, CoinToss.TAILS): 0.375,
                (CoinToss.TAILS, CoinToss.TAILS, CoinToss.TAILS): 0.125
            })
        )

    def test_coin_biased_intersect_and_sort(
        self,
        coin_biased: CoinTossEvent):
        coin_intersected = coin_biased.intersect_self(n=3)
        assert (
            coin_intersected.sorted() ==  # pyright: ignore[reportAttributeAccessIssue]
            Event[tuple[CoinToss, CoinToss, CoinToss]].from_pdf({
                (CoinToss.HEADS, CoinToss.HEADS, CoinToss.HEADS): 0.729,
                (CoinToss.HEADS, CoinToss.HEADS, CoinToss.TAILS): 0.243,
                (CoinToss.HEADS, CoinToss.TAILS, CoinToss.TAILS): 0.027,
                (CoinToss.TAILS, CoinToss.TAILS, CoinToss.TAILS): 0.001
            })
        )
    
    def test_coin_two_sample_without_replacement_and_sort(
        self,
        coin_two: CoinTossEvent):
        coin_sampled = coin_two.sample_event(n=2, replace=False)
        assert (
            coin_sampled.sorted() ==  # pyright: ignore[reportAttributeAccessIssue]
            Event[tuple[CoinToss, CoinToss]]([(CoinToss.HEADS, CoinToss.TAILS)])
        )

    # ----------------------------
    # Event.get_event_as_counter()
    # ----------------------------
    def test_coin_explicitly_countered(self):
        coin_flips = Event[tuple[CoinToss, CoinToss]]([
            (CoinToss.HEADS, CoinToss.TAILS),
            (CoinToss.TAILS, CoinToss.HEADS),
            (CoinToss.TAILS, CoinToss.TAILS)
        ])
        assert (
            coin_flips.get_event_as_counter() ==
            Event[HashableCounter[CoinToss]].from_pdf({
                HashableCounter[CoinToss]({CoinToss.HEADS: 1, CoinToss.TAILS: 1}): 2/3,
                HashableCounter[CoinToss]({CoinToss.TAILS: 2}): 1/3
            })
        )

    def test_coin_two_intersect_and_counter(
        self,
        coin_two: CoinTossEvent):
        coin_intersected = coin_two.intersect_self(n=3)
        assert (
            coin_intersected.get_event_as_counter() ==
            Event[HashableCounter[CoinToss]].from_pdf({
                HashableCounter[CoinToss]({CoinToss.HEADS: 3}): 0.125,
                HashableCounter[CoinToss]({CoinToss.HEADS: 2, CoinToss.TAILS: 1}): 0.375,
                HashableCounter[CoinToss]({CoinToss.HEADS: 1, CoinToss.TAILS: 2}): 0.375,
                HashableCounter[CoinToss]({CoinToss.TAILS: 3}): 0.125
            })
        )

    def test_coin_biased_intersect_and_counter(
        self,
        coin_biased: CoinTossEvent):
        coin_intersected = coin_biased.intersect_self(n=3)
        assert (
            coin_intersected.get_event_as_counter() ==
            Event[HashableCounter[CoinToss]].from_pdf({
                HashableCounter[CoinToss]({CoinToss.HEADS: 3}): 0.729,
                HashableCounter[CoinToss]({CoinToss.HEADS: 2, CoinToss.TAILS: 1}): 0.243,
                HashableCounter[CoinToss]({CoinToss.HEADS: 1, CoinToss.TAILS: 2}): 0.027,
                HashableCounter[CoinToss]({CoinToss.TAILS: 3}): 0.001
            })
        )
    
    def test_coin_one_sample_without_replacement_and_counter(
        self,
        coin_one: CoinTossEvent):
        coin_sampled = coin_one.sample_event(n=2, replace=False)
        assert (
            coin_sampled.get_event_as_counter() == 
            Event[HashableCounter[CoinToss]]([
                HashableCounter[CoinToss]({CoinToss.HEADS: 1, CoinToss.TAILS: 1})
            ])
        )

    # --------------
    # Event.filter()
    # --------------
    def test_coin_one_filter_heads(
        self,
        coin_one: CoinTossEvent
    ):
        assert (
            coin_one.filter(lambda outcome: outcome is CoinToss.HEADS) ==
            CoinTossEvent([CoinToss.HEADS])
        )
    
    def test_coin_two_filter_tails(
        self,
        coin_two: CoinTossEvent
    ):
        assert (
            coin_two.filter(lambda outcome: outcome is CoinToss.TAILS) ==
            CoinTossEvent([CoinToss.TAILS])
        )
    
    def test_coin_biased_no_filter(
        self,
        coin_biased: CoinTossEvent
    ):
        assert coin_biased.filter(lambda _: True) == coin_biased

    # -----------------------------
    # Event.filter_by_probability()
    # -----------------------------
    def test_coin_biased_filter_small_probabilities(
        self,
        coin_biased: CoinTossEvent
    ):
        assert (
            coin_biased.filter_by_probability(lambda p: p < 0.5) ==
            CoinTossEvent([CoinToss.TAILS])
        )

    def test_coin_biased_filter_large_probabilities(
        self,
        coin_biased: CoinTossEvent
    ):
        assert (
            coin_biased.filter_by_probability(lambda p: p > 0.5) ==
            CoinTossEvent([CoinToss.HEADS])
        )
    
    def test_coin_biased_filter_no_probabilities(
        self,
        coin_biased: CoinTossEvent
    ):
        assert coin_biased.filter_by_probability(lambda p: p > 0) == coin_biased

    # --------------
    # Event.reduce()
    # --------------
    def test_coin_one_two_intersect_and_reduce_to_count_heads(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent
    ):
        coin_intersected = coin_one.intersect(coin_two)
        assert (
            coin_intersected.reduce(
                op=lambda count, coin: count + int(coin is CoinToss.HEADS),
                initial=0
            ) ==
            Event[int].from_pdf({
                0: 0.25, 1: 0.5, 2: 0.25
            })
        )

    def test_coin_one_two_intersect_and_reduce_to_count_tails(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent
    ):
        coin_intersected = coin_one.intersect(coin_two)
        assert (
            coin_intersected.reduce(
                op=lambda count, coin: count + int(coin is CoinToss.TAILS),
                initial=0
            ) ==
            Event[int].from_pdf({
                0: 0.25, 1: 0.5, 2: 0.25
            })
        )

    def test_coin_biased_intersect_self_and_reduce_to_count_heads(
        self,
        coin_biased: CoinTossEvent
    ):
        coin_intersected = coin_biased.intersect_self(3)
        assert (
            coin_intersected.reduce(
                op=lambda count, coin: count + int(coin is CoinToss.HEADS),
                initial=0
            ) ==
            Event[int].from_pdf({
                0: 0.001, 1: 0.027, 2: 0.243, 3: 0.729
            })
        )

    def test_coin_biased_intersect_self_and_reduce_to_count_tails(
        self,
        coin_biased: CoinTossEvent
    ):
        coin_intersected = coin_biased.intersect_self(3)
        assert (
            coin_intersected.reduce(
                op=lambda count, coin: count + int(coin is CoinToss.TAILS),
                initial=0
            ) ==
            Event[int].from_pdf({
                0: 0.729, 1: 0.243, 2: 0.027, 3: 0.001
            })
        )

    # -----------
    # Event.map()
    # -----------
    def test_coin_one_two_intersect_and_map_to_count_heads(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent
    ):
        coin_intersected = coin_one.intersect(coin_two)
        assert (
            coin_intersected.map(
                lambda outcome: sum (coin is CoinToss.HEADS for coin in outcome)
            ) ==
            Event[int].from_pdf({
                0: 0.25, 1: 0.5, 2: 0.25
            })
        )

    def test_coin_one_two_intersect_and_map_to_count_tails(
        self,
        coin_one: CoinTossEvent,
        coin_two: CoinTossEvent
    ):
        coin_intersected = coin_one.intersect(coin_two)
        assert (
            coin_intersected.map(
                lambda outcome: sum (coin is CoinToss.TAILS for coin in outcome)
            ) ==
            Event[int].from_pdf({
                0: 0.25, 1: 0.5, 2: 0.25
            })
        )

    def test_coin_biased_intersect_self_and_map_to_count_heads(
        self,
        coin_biased: CoinTossEvent
    ):
        coin_intersected = coin_biased.intersect_self(3)
        assert (
            coin_intersected.map(
                lambda outcome: sum (coin is CoinToss.HEADS for coin in outcome)
            ) ==
            Event[int].from_pdf({
                0: 0.001, 1: 0.027, 2: 0.243, 3: 0.729
            })
        )

    def test_coin_biased_intersect_self_and_map_to_count_tails(
        self,
        coin_biased: CoinTossEvent
    ):
        coin_intersected = coin_biased.intersect_self(3)
        assert (
            coin_intersected.map(
                lambda outcome: sum (coin is CoinToss.TAILS for coin in outcome)
            ) ==
            Event[int].from_pdf({
                0: 0.729, 1: 0.243, 2: 0.027, 3: 0.001
            })
        )

    def test_coin_biased_map_to_flip_probabilities(
        self,
        coin_biased: CoinTossEvent
    ):
        assert (
            coin_biased.map(
                lambda coin: CoinToss.HEADS if coin is CoinToss.TAILS else CoinToss.TAILS
            ) ==
            CoinTossEvent.from_pdf({
                CoinToss.HEADS: 0.1, CoinToss.TAILS: 0.9
            })
        )


@pytest.mark.unit
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

    # --------------
    # Event.outcomes
    # --------------
    def test_die_one_outcomes(self, die_one: DiceRollEvent):
        assert die_one.outcomes == {
            DiceRoll.ONE, DiceRoll.TWO, DiceRoll.THREE,
            DiceRoll.FOUR, DiceRoll.FIVE, DiceRoll.SIX}
    
    def test_die_two_outcomes(self, die_two: DiceRollEvent):
        assert die_two.outcomes == {
            DiceRoll.ONE, DiceRoll.TWO, DiceRoll.THREE,
            DiceRoll.FOUR, DiceRoll.FIVE, DiceRoll.SIX}
    
    def test_die_biased_outcomes(self, die_biased: DiceRollEvent):
        assert die_biased.outcomes == {
            DiceRoll.ONE, DiceRoll.TWO, DiceRoll.THREE,
            DiceRoll.FOUR, DiceRoll.FIVE, DiceRoll.SIX}

    # -------------------
    # Event.probabilities
    # -------------------
    def test_die_one_probabilities(self, die_one: DiceRollEvent):
        assert die_one.probabilities == (1/6, 1/6, 1/6, 1/6, 1/6, 1/6)
    
    def test_die_two_probabilities(self, die_two: DiceRollEvent):
        assert die_two.probabilities == (1/6, 1/6, 1/6, 1/6, 1/6, 1/6)
    
    def test_die_biased_probabilities(self, die_biased: DiceRollEvent):
        assert die_biased.probabilities == (0.1, 0.1, 0.1, 0.1, 0.1, 0.5)

    # --------------
    # Event.remove()
    # --------------
    def test_die_one_remove_one(
        self,
        die_one: DiceRollEvent
    ):
        die_one.remove([DiceRoll.ONE])
        assert die_one == DiceRollEvent([
            DiceRoll.TWO, DiceRoll.THREE, DiceRoll.FOUR,
            DiceRoll.FIVE, DiceRoll.SIX
        ])
    
    def test_die_one_remove_all(
        self,
        die_one: DiceRollEvent
    ):
        with pytest.raises(ValueError):
            die_one.remove([
                DiceRoll.ONE, DiceRoll.TWO,
                DiceRoll.THREE, DiceRoll.FOUR,
                DiceRoll.FIVE, DiceRoll.SIX])

    # -----------------
    # Event.rebalance()
    # -----------------
    def test_die_one_bias(
        self,
        die_one: DiceRollEvent,
        die_biased: DiceRollEvent
    ):
        die_one.rebalance(DiceRoll.SIX, 0.5)
        assert die_one == die_biased
    
    def test_die_one_unbias(
        self,
        die_one: DiceRollEvent,
        die_two: DiceRollEvent
    ):
        die_one.rebalance(DiceRoll.SIX, 1.0 / 6)
        assert die_one == die_two

    # -----------------
    # Event.intersect()
    # -----------------
    def test_dice_one_and_two_intersect_outcomes(
        self,
        die_one: DiceRollEvent,
        die_two: DiceRollEvent):
        dice = die_one.intersect(die_two)
        assert dice.outcomes == set([
            (DiceRoll.ONE, DiceRoll.ONE), (DiceRoll.ONE, DiceRoll.TWO), (DiceRoll.ONE, DiceRoll.THREE), (DiceRoll.ONE, DiceRoll.FOUR), (DiceRoll.ONE, DiceRoll.FIVE), (DiceRoll.ONE, DiceRoll.SIX), 
            (DiceRoll.TWO, DiceRoll.ONE), (DiceRoll.TWO, DiceRoll.TWO), (DiceRoll.TWO, DiceRoll.THREE), (DiceRoll.TWO, DiceRoll.FOUR), (DiceRoll.TWO, DiceRoll.FIVE), (DiceRoll.TWO, DiceRoll.SIX), 
            (DiceRoll.THREE, DiceRoll.ONE), (DiceRoll.THREE, DiceRoll.TWO), (DiceRoll.THREE, DiceRoll.THREE), (DiceRoll.THREE, DiceRoll.FOUR), (DiceRoll.THREE, DiceRoll.FIVE), (DiceRoll.THREE, DiceRoll.SIX), 
            (DiceRoll.FOUR, DiceRoll.ONE), (DiceRoll.FOUR, DiceRoll.TWO), (DiceRoll.FOUR, DiceRoll.THREE), (DiceRoll.FOUR, DiceRoll.FOUR), (DiceRoll.FOUR, DiceRoll.FIVE), (DiceRoll.FOUR, DiceRoll.SIX), 
            (DiceRoll.FIVE, DiceRoll.ONE), (DiceRoll.FIVE, DiceRoll.TWO), (DiceRoll.FIVE, DiceRoll.THREE), (DiceRoll.FIVE, DiceRoll.FOUR), (DiceRoll.FIVE, DiceRoll.FIVE), (DiceRoll.FIVE, DiceRoll.SIX), 
            (DiceRoll.SIX, DiceRoll.ONE), (DiceRoll.SIX, DiceRoll.TWO), (DiceRoll.SIX, DiceRoll.THREE), (DiceRoll.SIX, DiceRoll.FOUR), (DiceRoll.SIX, DiceRoll.FIVE), (DiceRoll.SIX, DiceRoll.SIX)])
    
    def test_dice_one_and_two_intersect_probabilities(
        self,
        die_one: DiceRollEvent,
        die_two: DiceRollEvent):
        dice = die_one.intersect(die_two)
        assert dice.probabilities == (1.0/36,) * 36
    
    def test_dice_one_and_two_intersect_commutative(
        self,
        die_one: DiceRollEvent,
        die_two: DiceRollEvent):
        assert die_one.intersect(die_two) == die_two.intersect(die_one)


    # ----------------------
    # Event.intersect_self()
    # ----------------------

    # --------------
    # Event.sample()
    # --------------
    def test_die_one_sample_all(self, die_one: DiceRollEvent):
        assert set(die_one.sample(n=6)) == die_one.outcomes
    
    def test_die_two_sample_all(self, die_two: DiceRollEvent):
        assert set(die_two.sample(n=6)) == die_two.outcomes
    
    def test_die_biased_sample_all(self, die_biased: DiceRollEvent):
        assert set(die_biased.sample(n=6)) == die_biased.outcomes

    # --------------------
    # Event.sample_event()
    # --------------------
    @pytest.mark.skip(reason="Not ready")
    def test_dice_one_sample_one_event(self):
        pass

    @pytest.mark.skip(reason="Not ready")
    def test_dice_two_sample_one_event(self):
        pass

    @pytest.mark.skip(reason="Not ready")
    def test_dice_one_sample_two_events(self):
        pass

    @pytest.mark.skip(reason="Not ready")
    def test_dice_two_sample_two_events(self):
        pass

    # --------------
    # Event.sorted()
    # --------------

    # ----------------------------
    # Event.get_event_as_counter()
    # ----------------------------

    # --------------
    # Event.filter()
    # --------------

    # -----------------------------
    # Event.filter_by_probability()
    # -----------------------------

    # --------------
    # Event.reduce()
    # --------------

    # -----------
    # Event.map()
    # -----------


@pytest.mark.unit
class TestBadEvents:
    # --------------
    # Event.outcomes
    # --------------
    def test_instantiate_no_outcomes(self):
        try:
            Event[int]([])
        except AttributeError as e:
            assert str(e) == "Must enter non-empty outcomes."
            return
        assert False

    def test_instantiate_duplicate_outcomes(self):
        try:
            Event[int]([0, 1, 1])
        except AttributeError as e:
            assert str(e) == "Outcome values must be unique."
            return
        assert False
    
    def test_instantiate_few_outcomes(self):
        try:
            Event[int]([0], [0.4, 0.6])
        except AttributeError as e:
            assert str(e) == "Number of values in outcomes (1) and weights (2) does not match."
            return
        assert False
    
    def test_instantiate_many_outcomes(self):
        try:
            Event[int]([0, 1], [1])
        except AttributeError as e:
            assert str(e) == "Number of values in outcomes (2) and weights (1) does not match."
            return
        assert False

    # @pytest.mark.skip(reason="Cannot perform strict type-checking over generic classes in Python.")
    def test_instantiate_outcomes_wrong_type(self):
        # with pytest.raises(TypeError):
            event = Event[str]([0, 1])  # pyright: ignore[reportArgumentType]

    # -------------------
    # Event.probabilities
    # -------------------
    def test_instantiate_zero_weight(self):
        try:
            Event[int]([0, 1], [0.5, 0])
        except AttributeError as e:
            assert str(e) == "Not all weights are strictly positive."
            return
        assert False

    def test_instantiate_negative_weight(self):
        try:
            Event[int]([0, 1], [0.5, -0.5])
        except AttributeError as e:
            assert str(e) == "Not all weights are strictly positive."
            return
        assert False

    # -------------------
    # Event.__delitem__()
    # -------------------
    def test_delete_nonexistent_outcome(self):
        event = Event[int]([0])
        try:
            del event[1]
        except KeyError as e:
            assert str(e) == '"Outcome \'1\' not in event outcomes."'
            return
        assert False
    
    def test_delete_all_outcomes(self):
        event = Event[int]([0])
        try:
            del event[0]
        except ValueError as e:
            assert str(e) == "Cannot delete the only outcome '0' in the event."
            return
        assert False

    def test_remove_duplicate_outcomes(self):
        event = Event[int]([0, 1])
        try:
            event.remove([1, 1])
        except ValueError as e:
            assert str(e) == "Outcomes [1, 1] contains duplicate entries."
            return
        assert False

    # --------------
    # Event.remove()
    # --------------
    def test_remove_nonexistent_outcome(self):
        event = Event[int]([0])
        try:
            event.remove([1])
        except KeyError as e:
            assert str(e) == "'Outcomes {1} do not exist in event.'"
            return
        assert False
    
    def test_remove_nonexistent_outcome_superset(self):
        event = Event[int]([0, 1])
        try:
            event.remove([1, 2])
        except KeyError as e:
            assert str(e) == "'Outcomes {2} do not exist in event.'"
            return
        assert False
    
    def test_remove_all_outcomes(self):
        event = Event[int]([0, 1])
        try:
            event.remove([0, 1])
        except ValueError as e:
            assert str(e) == "Request for all outcomes to be removed."
            return
        assert False

    # -----------------
    # Event.rebalance()
    # -----------------
    def test_rebalance_outcome_does_not_exist(self):
        event = Event[int]([0])
        try:
            event.rebalance(2, 0.5)
        except KeyError as e:
            assert str(e) == "\"Outcome '2' does not exist in this event.\""
            return
        assert False

    def test_rebalance_non_probability_negative(self):
        event = Event[int]([0, 1])
        try:
            event.rebalance(0, -1)
        except ValueError as e:
            assert str(e) == "Probability must be in (0,1)."
            return
        assert False
    
    def test_rebalance_non_probability_zero(self):
        event = Event[int]([0, 1])
        try:
            event.rebalance(0, 0)
        except ValueError as e:
            assert str(e) == "Probability must be in (0,1)."
            return
        assert False
    
    def test_rebalance_non_probability_positive(self):
        event = Event[int]([0, 1])
        try:
            event.rebalance(0, 1)
        except ValueError as e:
            assert str(e) == "Probability must be in (0,1)."
            return
        assert False

    # ----------------------
    # Event.intersect_self()
    # ----------------------
    def test_intersect_zero(self):
        event = Event[int]([0, 1])
        try:
            event.intersect_self(0)
        except ValueError as e:
            assert str(e) == "n must be a positive integer."
            return
        assert False
    
    def test_intersect_negative(self):
        event = Event[int]([0, 1])
        try:
            event.intersect_self(-1)
        except ValueError as e:
            assert str(e) == "n must be a positive integer."
            return
        assert False

    # --------------
    # Event.sample()
    # --------------
    def test_sample_zero(self):
        event = Event[int]([0, 1])
        try:
            event.sample(0)
        except ValueError as e:
            assert str(e) == "n must be a positive integer."
            return
        assert False
    
    def test_sample_negative(self):
        event = Event[int]([0, 1])
        try:
            event.sample(-1)
        except ValueError as e:
            assert str(e) == "n must be a positive integer."
            return
        assert False
    
    def test_sample_too_many(self):
        event = Event[int]([0, 1])
        try:
            event.sample(3, replace=False)
        except ValueError as e:
            assert str(e) == "Cannot sample 3 outcomes without replacement from an event with only 2 unique outcomes."
            return
        assert False

    # --------------------
    # Event.sample_event()
    # --------------------
    def test_sample_event_zero(self):
        event = Event[int]([0, 1])
        try:
            event.sample_event(0)
        except ValueError as e:
            assert str(e) == "n must be at least 1 to form a new event."
            return
        assert False
    
    def test_sample_event_negative(self):
        event = Event[int]([0, 1])
        try:
            event.sample_event(-1)
        except ValueError as e:
            assert str(e) == "n must be at least 1 to form a new event."
            return
        assert False
    
    def test_sample_event_too_many(self):
        event = Event[int]([0, 1])
        try:
            event.sample_event(3, replace=False)
        except ValueError as e:
            assert str(e) == "Cannot sample 3 outcomes without replacement from an event with only 2 unique outcomes."
            return
        assert False

    # --------------
    # Event.sorted()
    # --------------
    def test_unsortable(self):
        event = Event[int]([0, 1])
        with pytest.raises(TypeError):
            event.sorted()  # pyright: ignore[reportAttributeAccessIssue]

    # ----------------------------
    # Event.get_event_as_counter()
    # ----------------------------
    def test_uncounterable(self):
        event = Event[int]([0, 1])
        with pytest.raises(TypeError):
            event.get_event_as_counter()  # pyright: ignore[reportAttributeAccessIssue]

    # --------------
    # Event.filter()
    # --------------
    def test_filter_type_mismatch(self):
        event = Event[str](['a', 'b'])
        with pytest.raises(TypeError):
            event.filter(lambda x: x < 0)  # pyright: ignore[reportOperatorIssue]

    # -----------------------------
    # Event.filter_by_probability()
    # -----------------------------

    # --------------
    # Event.reduce()
    # --------------
    def test_reduce_op_wrong_type(self):
        event = Event[int]([0, 1])
        with pytest.raises(TypeError):
            event.reduce(op.add)  # pyright: ignore[reportAttributeAccessIssue]
    
    def test_reduce_initial_wrong_type(self):
        event = Event[tuple[int, ...]]([(0, 1), (2, 1)])
        with pytest.raises(TypeError):
            event.reduce(op.add, 'a')  # pyright: ignore[reportArgumentType]


@pytest.mark.unit
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

    def test_values_reduced(
        self,
        value_one: ValueEvent,
        value_two: ValueEvent,
        value_combined: ValueEvent):
        reduced = value_one.intersect(value_two).reduce(op.add)
        assert reduced == value_combined


@pytest.mark.unit
class TestPropertyEvent:
    pass


@pytest.mark.unit
class TestSubPropertyEvent:
    pass


@pytest.mark.unit
class TestRuneSlotEvent:
    pass


@pytest.mark.unit
class TestRuneStarsEvent:
    pass


@pytest.mark.unit
class TestRuneSetEvent:
    pass


@pytest.mark.unit
class TestGradeEvent:
    pass


@pytest.mark.unit
class TestUpgradeEvent:
    pass
