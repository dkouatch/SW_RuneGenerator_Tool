from backend.utils.models.types.distribution import Distribution
import math
import pytest
import operator as op

from . import CoinToss, DiceRoll
from src.backend.utils.models.types.event import *

CoinTosses = tuple[CoinToss, ...]
DiceRolls = tuple[DiceRoll, ...]
CoinTossEvent = Event[CoinTosses]
DiceRollEvent = Event[DiceRolls]

@pytest.mark.unit
class TestCoinTossEvent:
    @pytest.fixture
    def coin_tosses(self) -> CoinTosses:
        return (CoinToss.HEADS, CoinToss.TAILS, CoinToss.HEADS)

    @pytest.fixture
    def three_unconditional_tosses(self) -> Distribution[CoinTosses]:
        return Distribution[CoinToss]([member for member in CoinToss]).intersect_self(3)
    
    @pytest.fixture
    def three_conditional_tosses(self) -> Distribution[CoinTosses]:
        distribution = Distribution[CoinToss]([member for member in CoinToss]).intersect_self(n=3).filter(
            lambda tosses: sum((toss == CoinToss.HEADS) for toss in tosses) >= 2
        )
        assert distribution is not None
        return distribution

    # -------------------
    # Event.probability()
    # -------------------
    def test_probability_without_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](coin_tosses, three_unconditional_tosses)
        assert event.probability == 0.125

    def test_probability_with_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses],
        three_conditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](coin_tosses, three_unconditional_tosses, three_conditional_tosses)
        assert event.probability == 0.25

    def test_condition_probability_without_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](coin_tosses, three_unconditional_tosses)
        event.condition()
        assert event.probability == 1.0

    def test_unconditon_probability_with_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses],
        three_conditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](coin_tosses, three_unconditional_tosses, three_conditional_tosses)
        event.uncondition()
        assert event.probability == 0.125

    # --------------
    # Event.sorted()
    # --------------
    def test_sorted_probability_without_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        assert event.probability == 0.375

    def test_sorted_probability_with_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses],
        three_conditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses, 
            three_unconditional_tosses,
            three_conditional_tosses).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        assert event.probability == 0.75

    def test_sorted_condition_probability_without_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        event.condition()
        assert event.probability == 1.0

    def test_sorted_unconditon_probability_with_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses],
        three_conditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses,
            three_conditional_tosses).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        event.uncondition()
        assert event.probability == 0.375

    # ------------------
    # Event.to_counter()
    # ------------------
    def test_to_counter_probability_without_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).to_counter()
        assert event.probability == 0.375

    def test_to_counter_probability_with_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses],
        three_conditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses, 
            three_unconditional_tosses,
            three_conditional_tosses).to_counter()
        assert event.probability == 0.75

    def test_to_counter_condition_probability_without_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).to_counter()
        event.condition()
        assert event.probability == 1.0

    def test_to_counter_unconditon_probability_with_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses],
        three_conditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses,
            three_conditional_tosses).to_counter()
        event.uncondition()
        assert event.probability == 0.375

    # --------------
    # Event.reduce()
    # --------------
    def test_reduce_count_heads_probability_without_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).reduce(
                op=lambda count, coin: count + int(coin == CoinToss.HEADS),
                initial=0
            )
        assert event.probability == 0.375

    def test_reduce_count_heads_probability_with_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses],
        three_conditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses, 
            three_unconditional_tosses,
            three_conditional_tosses).reduce(
                op=lambda count, coin: count + int(coin == CoinToss.HEADS),
                initial=0
            )
        assert event.probability == 0.75

    def test_reduce_count_heads_condition_probability_without_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).reduce(
                op=lambda count, coin: count + int(coin == CoinToss.HEADS),
                initial=0
            )
        event.condition()
        assert event.probability == 1.0

    def test_reduce_count_heads_unconditon_probability_with_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses],
        three_conditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses,
            three_conditional_tosses).reduce(
                op=lambda count, coin: count + int(coin == CoinToss.HEADS),
                initial=0
            )
        event.uncondition()
        assert event.probability == 0.375

    # -----------
    # Event.map()
    # -----------
    def test_map_count_heads_probability_without_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).map(
                func=lambda tosses: sum(coin == CoinToss.HEADS for coin in tosses)
            )
        assert event.probability == 0.375

    def test_map_count_heads_probability_with_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses],
        three_conditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses, 
            three_unconditional_tosses,
            three_conditional_tosses).map(
                func=lambda tosses: sum(coin == CoinToss.HEADS for coin in tosses)
            )
        assert event.probability == 0.75

    def test_map_count_heads_condition_probability_without_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).map(
                func=lambda tosses: sum(coin == CoinToss.HEADS for coin in tosses)
            )
        event.condition()
        assert event.probability == 1.0

    def test_map_count_heads_unconditon_probability_with_conditional_distribution(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Distribution[CoinTosses],
        three_conditional_tosses: Distribution[CoinTosses]
    ):
        event = Event[CoinTosses](
            coin_tosses,
            three_unconditional_tosses,
            three_conditional_tosses).map(
                func=lambda tosses: sum(coin == CoinToss.HEADS for coin in tosses)
            )
        event.uncondition()
        assert event.probability == 0.375


@pytest.mark.unit
class TestDiceRollEvent:
    @pytest.fixture
    def dice_rolls(self) -> DiceRolls:
        return (DiceRoll.THREE, DiceRoll.FIVE, DiceRoll.TWO)

    @pytest.fixture
    def three_unconditional_rolls(self) -> Distribution[DiceRolls]:
        return Distribution[DiceRoll]([member for member in DiceRoll]).intersect_self(3)

    @pytest.fixture
    def three_conditional_rolls(self) -> Distribution[DiceRolls]:
        distribution = Distribution[DiceRoll]([member for member in DiceRoll]).intersect_self(n=3).filter(
            lambda rolls: sum(int(roll) for roll in rolls) >= 6
        )
        assert distribution is not None
        return distribution

    # -------------------
    # Event.probability()
    # -------------------
    def test_probability_without_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](dice_rolls, three_unconditional_rolls)
        assert math.isclose(event.probability, 1/216)

    def test_probability_with_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls],
        three_conditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](dice_rolls, three_unconditional_rolls, three_conditional_rolls)
        assert math.isclose(event.probability, 1/206)

    def test_condition_probability_without_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](dice_rolls, three_unconditional_rolls)
        event.condition()
        assert event.probability == 1.0

    def test_unconditon_probability_with_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls],
        three_conditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](dice_rolls, three_unconditional_rolls, three_conditional_rolls)
        event.uncondition()
        assert math.isclose(event.probability, 1/216)

    # --------------
    # Event.sorted()
    # --------------
    def test_sorted_probability_without_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        assert math.isclose(event.probability, 1/36)

    def test_sorted_probability_with_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls],
        three_conditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls, 
            three_unconditional_rolls,
            three_conditional_rolls).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        assert math.isclose(event.probability, 3/103)

    def test_sorted_condition_probability_without_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        event.condition()
        assert event.probability == 1.0

    def test_sorted_unconditon_probability_with_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls],
        three_conditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls,
            three_conditional_rolls).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        event.uncondition()
        assert math.isclose(event.probability, 1/36)

    # ------------------
    # Event.to_counter()
    # ------------------
    def test_to_counter_probability_without_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).to_counter()
        assert math.isclose(event.probability, 1/36)

    def test_to_counter_probability_with_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls],
        three_conditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls, 
            three_unconditional_rolls,
            three_conditional_rolls).to_counter()
        assert math.isclose(event.probability, 3/103)

    def test_to_counter_condition_probability_without_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).to_counter()
        event.condition()
        assert event.probability == 1.0

    def test_to_counter_unconditon_probability_with_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls],
        three_conditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls,
            three_conditional_rolls).to_counter()
        event.uncondition()
        assert math.isclose(event.probability, 1/36)

    # --------------
    # Event.reduce()
    # --------------
    def test_reduce_count_twos_probability_without_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).reduce(
                op=lambda count, roll: count + int(roll == DiceRoll.TWO),
                initial=0
            )
        assert math.isclose(event.probability, 25/72)

    def test_reduce_count_twos_probability_with_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls],
        three_conditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls, 
            three_unconditional_rolls,
            three_conditional_rolls).reduce(
                op=lambda count, roll: count + int(roll == DiceRoll.TWO),
                initial=0
            )
        assert math.isclose(event.probability, 36/103)

    def test_reduce_count_twos_condition_probability_without_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).reduce(
                op=lambda count, roll: count + int(roll == DiceRoll.TWO),
                initial=0
            )
        event.condition()
        assert event.probability == 1.0

    def test_reduce_count_twos_unconditon_probability_with_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls],
        three_conditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls,
            three_conditional_rolls).reduce(
                op=lambda count, roll: count + int(roll == DiceRoll.TWO),
                initial=0
            )
        event.uncondition()
        assert math.isclose(event.probability, 25/72)

    # -----------
    # Event.map()
    # -----------
    def test_map_count_twos_probability_without_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).map(
                func=lambda rolls: sum((roll == DiceRoll.TWO) for roll in rolls)
            )
        assert math.isclose(event.probability, 25/72)

    def test_map_count_twos_probability_with_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls],
        three_conditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls, 
            three_unconditional_rolls,
            three_conditional_rolls).map(
                func=lambda rolls: sum((roll == DiceRoll.TWO) for roll in rolls)
            )
        assert math.isclose(event.probability, 36/103)

    def test_map_count_twos_condition_probability_without_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).map(
                func=lambda rolls: sum((roll == DiceRoll.TWO) for roll in rolls)
            )
        event.condition()
        assert event.probability == 1.0

    def test_map_count_twos_unconditon_probability_with_conditional_distribution(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Distribution[DiceRolls],
        three_conditional_rolls: Distribution[DiceRolls]
    ):
        event = Event[DiceRolls](
            dice_rolls,
            three_unconditional_rolls,
            three_conditional_rolls).map(
                func=lambda rolls: sum((roll == DiceRoll.TWO) for roll in rolls)
            )
        event.uncondition()
        assert math.isclose(event.probability, 25/72)


@pytest.mark.unit
class TestBadEntities:
    # ----------------
    # Event.__init__()
    # ----------------
    def test_outcome_not_in_unconditional_distribution(self):
        unconditional_distribution = Distribution[int](range(4))
        with pytest.raises(AttributeError):
            Event[int](4, unconditional_distribution)

    def test_outcome_not_in_conditional_distribution(self):
        unconditional_distribution = Distribution[int](range(4))
        conditional_distribution = unconditional_distribution.filter(lambda x: x < 3)
        with pytest.raises(AttributeError):
            Event[int](3, unconditional_distribution, conditional_distribution)

    def test_conditional_outcomes_not_in_unconditional_outcomes(self):
        unconditional_distribution = Distribution[int](range(4))
        conditional_distribution = Distribution[int](range(3, 7))
        with pytest.raises(AttributeError):
            Event[int](3, unconditional_distribution, conditional_distribution)

    @pytest.mark.skip("Cannot enforce strict type-checking over generic classes in Python.")
    def test_outcome_unconditional_distribution_type_mismatch(self):
        unconditional_distribution = Distribution[str](['a', 'b', 'c'])
        with pytest.raises(AttributeError):
            Event[int](3, unconditional_distribution)  #pyright: ignore[reportArgumentType]

    @pytest.mark.skip("Cannot enforce strict type-checking over generic classes in Python.")
    def test_outcome_conditional_distribution_type_mismatch(self):
        unconditional_distribution = Distribution[int](range(4))
        conditional_distribution = Distribution[str](['a', 'b', 'c'])
        with pytest.raises(AttributeError):
            Event[int](3, unconditional_distribution, conditional_distribution)  #pyright: ignore[reportArgumentType]

    # --------------
    # Event.sorted()
    # --------------
    def test_unsortable(self):
        event = Event[int](
            0,
            Distribution[int]([0, 1]))
        with pytest.raises(TypeError):
            event.sorted()  # pyright: ignore[reportAttributeAccessIssue]

    # ------------------
    # Event.to_counter()
    # ------------------
    def test_uncounterable(self):
        event = Event[int](
            0,
            Distribution[int]([0, 1]))
        with pytest.raises(TypeError):
            event.to_counter()  # pyright: ignore[reportAttributeAccessIssue]

    # --------------
    # Event.reduce()
    # --------------
    def test_reduce_op_wrong_type(self):
        event = Event[int](
            0,
            Distribution[int]([0, 1]))
        with pytest.raises(TypeError):
            event.reduce(op.add)  # pyright: ignore[reportAttributeAccessIssue]
    
    def test_reduce_initial_wrong_type(self):
        event = Event[tuple[int, ...]](
            (0, 1),
            Distribution[tuple[int, ...]]([(0, 1), (2, 1)]))
        with pytest.raises(TypeError):
            event.reduce(op.add, 'a')  # pyright: ignore[reportArgumentType]

    # -----------
    # Event.map()
    # -----------
    def test_map_func_wrong_type(self):
        event = Event[str](
            'a',
            Distribution[str](['a', 'b']))
        with pytest.raises(TypeError):
            event.map(lambda x: x + 0)  # pyright: ignore[reportOperatorIssue]
