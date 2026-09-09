from backend.utils.models.types.events import Event
import math
import pytest
import operator as op

from enum import IntEnum, unique
from src.backend.utils.models.types.entities import *

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

CoinTosses = tuple[CoinToss, ...]
DiceRolls = tuple[DiceRoll, ...]
CoinTossEntity = Entity[CoinTosses]
DiceRollEntity = Entity[DiceRolls]

@pytest.mark.unit
class TestCoinTossEntity:
    @pytest.fixture
    def coin_tosses(self) -> CoinTosses:
        return (CoinToss.HEADS, CoinToss.TAILS, CoinToss.HEADS)

    @pytest.fixture
    def three_unconditional_tosses(self) -> Event[CoinTosses]:
        return Event[CoinToss]([member for member in CoinToss]).intersect_self(3)
    
    @pytest.fixture
    def three_conditional_tosses(self) -> Event[CoinTosses]:
        event = Event[CoinToss]([member for member in CoinToss]).intersect_self(n=3).filter(
            lambda tosses: sum((toss == CoinToss.HEADS) for toss in tosses) >= 2
        )
        assert event is not None
        return event

    # --------------------
    # Entity.probability()
    # --------------------
    def test_probability_without_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](coin_tosses, three_unconditional_tosses)
        assert entity.probability == 0.125

    def test_probability_with_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses],
        three_conditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](coin_tosses, three_unconditional_tosses, three_conditional_tosses)
        assert entity.probability == 0.25

    def test_condition_probability_without_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](coin_tosses, three_unconditional_tosses)
        entity.condition()
        assert entity.probability == 1.0

    def test_unconditon_probability_with_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses],
        three_conditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](coin_tosses, three_unconditional_tosses, three_conditional_tosses)
        entity.uncondition()
        assert entity.probability == 0.125

    # ---------------
    # Entity.sorted()
    # ---------------
    def test_sorted_probability_without_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        assert entity.probability == 0.375

    def test_sorted_probability_with_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses],
        three_conditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses, 
            three_unconditional_tosses,
            three_conditional_tosses).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        assert entity.probability == 0.75

    def test_sorted_condition_probability_without_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        entity.condition()
        assert entity.probability == 1.0

    def test_sorted_unconditon_probability_with_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses],
        three_conditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses,
            three_conditional_tosses).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        entity.uncondition()
        assert entity.probability == 0.375

    # -------------------
    # Entity.to_counter()
    # -------------------
    def test_to_counter_probability_without_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).to_counter()
        assert entity.probability == 0.375

    def test_to_counter_probability_with_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses],
        three_conditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses, 
            three_unconditional_tosses,
            three_conditional_tosses).to_counter()
        assert entity.probability == 0.75

    def test_to_counter_condition_probability_without_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).to_counter()
        entity.condition()
        assert entity.probability == 1.0

    def test_to_counter_unconditon_probability_with_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses],
        three_conditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses,
            three_conditional_tosses).to_counter()
        entity.uncondition()
        assert entity.probability == 0.375

    # ---------------
    # Entity.reduce()
    # ---------------
    def test_reduce_count_heads_probability_without_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).reduce(
                op=lambda count, coin: count + int(coin == CoinToss.HEADS),
                initial=0
            )
        assert entity.probability == 0.375

    def test_reduce_count_heads_probability_with_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses],
        three_conditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses, 
            three_unconditional_tosses,
            three_conditional_tosses).reduce(
                op=lambda count, coin: count + int(coin == CoinToss.HEADS),
                initial=0
            )
        assert entity.probability == 0.75

    def test_reduce_count_heads_condition_probability_without_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).reduce(
                op=lambda count, coin: count + int(coin == CoinToss.HEADS),
                initial=0
            )
        entity.condition()
        assert entity.probability == 1.0

    def test_reduce_count_heads_unconditon_probability_with_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses],
        three_conditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses,
            three_conditional_tosses).reduce(
                op=lambda count, coin: count + int(coin == CoinToss.HEADS),
                initial=0
            )
        entity.uncondition()
        assert entity.probability == 0.375

    # ------------
    # Entity.map()
    # ------------
    def test_map_count_heads_probability_without_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).map(
                func=lambda tosses: sum(coin == CoinToss.HEADS for coin in tosses)
            )
        assert entity.probability == 0.375

    def test_map_count_heads_probability_with_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses],
        three_conditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses, 
            three_unconditional_tosses,
            three_conditional_tosses).map(
                func=lambda tosses: sum(coin == CoinToss.HEADS for coin in tosses)
            )
        assert entity.probability == 0.75

    def test_map_count_heads_condition_probability_without_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses).map(
                func=lambda tosses: sum(coin == CoinToss.HEADS for coin in tosses)
            )
        entity.condition()
        assert entity.probability == 1.0

    def test_map_count_heads_unconditon_probability_with_conditional_event(
        self,
        coin_tosses: CoinTosses,
        three_unconditional_tosses: Event[CoinTosses],
        three_conditional_tosses: Event[CoinTosses]
    ):
        entity = Entity[CoinTosses](
            coin_tosses,
            three_unconditional_tosses,
            three_conditional_tosses).map(
                func=lambda tosses: sum(coin == CoinToss.HEADS for coin in tosses)
            )
        entity.uncondition()
        assert entity.probability == 0.375


@pytest.mark.unit
class TestDiceRollEntity:
    @pytest.fixture
    def dice_rolls(self) -> DiceRolls:
        return (DiceRoll.THREE, DiceRoll.FIVE, DiceRoll.TWO)

    @pytest.fixture
    def three_unconditional_rolls(self) -> Event[DiceRolls]:
        return Event[DiceRoll]([member for member in DiceRoll]).intersect_self(3)

    @pytest.fixture
    def three_conditional_rolls(self) -> Event[DiceRolls]:
        event = Event[DiceRoll]([member for member in DiceRoll]).intersect_self(n=3).filter(
            lambda rolls: sum(int(roll) for roll in rolls) >= 6
        )
        assert event is not None
        return event

    # --------------------
    # Entity.probability()
    # --------------------
    def test_probability_without_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](dice_rolls, three_unconditional_rolls)
        assert math.isclose(entity.probability, 1/216)

    def test_probability_with_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls],
        three_conditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](dice_rolls, three_unconditional_rolls, three_conditional_rolls)
        assert math.isclose(entity.probability, 1/206)

    def test_condition_probability_without_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](dice_rolls, three_unconditional_rolls)
        entity.condition()
        assert entity.probability == 1.0

    def test_unconditon_probability_with_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls],
        three_conditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](dice_rolls, three_unconditional_rolls, three_conditional_rolls)
        entity.uncondition()
        assert math.isclose(entity.probability, 1/216)

    # ---------------
    # Entity.sorted()
    # ---------------
    def test_sorted_probability_without_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        assert math.isclose(entity.probability, 1/36)

    def test_sorted_probability_with_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls],
        three_conditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls, 
            three_unconditional_rolls,
            three_conditional_rolls).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        assert math.isclose(entity.probability, 3/103)

    def test_sorted_condition_probability_without_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        entity.condition()
        assert entity.probability == 1.0

    def test_sorted_unconditon_probability_with_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls],
        three_conditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls,
            three_conditional_rolls).sorted()  # pyright: ignore[reportAttributeAccessIssue]
        entity.uncondition()
        assert math.isclose(entity.probability, 1/36)

    # -------------------
    # Entity.to_counter()
    # -------------------
    def test_to_counter_probability_without_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).to_counter()
        assert math.isclose(entity.probability, 1/36)

    def test_to_counter_probability_with_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls],
        three_conditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls, 
            three_unconditional_rolls,
            three_conditional_rolls).to_counter()
        assert math.isclose(entity.probability, 3/103)

    def test_to_counter_condition_probability_without_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).to_counter()
        entity.condition()
        assert entity.probability == 1.0

    def test_to_counter_unconditon_probability_with_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls],
        three_conditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls,
            three_conditional_rolls).to_counter()
        entity.uncondition()
        assert math.isclose(entity.probability, 1/36)

    # ---------------
    # Entity.reduce()
    # ---------------
    def test_reduce_count_twos_probability_without_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).reduce(
                op=lambda count, roll: count + int(roll == DiceRoll.TWO),
                initial=0
            )
        assert math.isclose(entity.probability, 25/72)

    def test_reduce_count_twos_probability_with_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls],
        three_conditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls, 
            three_unconditional_rolls,
            three_conditional_rolls).reduce(
                op=lambda count, roll: count + int(roll == DiceRoll.TWO),
                initial=0
            )
        assert math.isclose(entity.probability, 36/103)

    def test_reduce_count_twos_condition_probability_without_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).reduce(
                op=lambda count, roll: count + int(roll == DiceRoll.TWO),
                initial=0
            )
        entity.condition()
        assert entity.probability == 1.0

    def test_reduce_count_twos_unconditon_probability_with_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls],
        three_conditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls,
            three_conditional_rolls).reduce(
                op=lambda count, roll: count + int(roll == DiceRoll.TWO),
                initial=0
            )
        entity.uncondition()
        assert math.isclose(entity.probability, 25/72)

    # ------------
    # Entity.map()
    # ------------
    def test_map_count_twos_probability_without_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).map(
                func=lambda rolls: sum((roll == DiceRoll.TWO) for roll in rolls)
            )
        assert math.isclose(entity.probability, 25/72)

    def test_map_count_twos_probability_with_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls],
        three_conditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls, 
            three_unconditional_rolls,
            three_conditional_rolls).map(
                func=lambda rolls: sum((roll == DiceRoll.TWO) for roll in rolls)
            )
        assert math.isclose(entity.probability, 36/103)

    def test_map_count_twos_condition_probability_without_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls).map(
                func=lambda rolls: sum((roll == DiceRoll.TWO) for roll in rolls)
            )
        entity.condition()
        assert entity.probability == 1.0

    def test_map_count_twos_unconditon_probability_with_conditional_event(
        self,
        dice_rolls: DiceRolls,
        three_unconditional_rolls: Event[DiceRolls],
        three_conditional_rolls: Event[DiceRolls]
    ):
        entity = Entity[DiceRolls](
            dice_rolls,
            three_unconditional_rolls,
            three_conditional_rolls).map(
                func=lambda rolls: sum((roll == DiceRoll.TWO) for roll in rolls)
            )
        entity.uncondition()
        assert math.isclose(entity.probability, 25/72)


@pytest.mark.unit
class TestBadEntities:
    # -----------------
    # Entity.__init__()
    # -----------------
    def test_outcome_not_in_unconditional_event(self):
        unconditional_event = Event[int](range(4))
        with pytest.raises(AttributeError):
            Entity[int](4, unconditional_event)

    def test_outcome_not_in_conditional_event(self):
        unconditional_event = Event[int](range(4))
        conditional_event = unconditional_event.filter(lambda x: x < 3)
        with pytest.raises(AttributeError):
            Entity[int](3, unconditional_event, conditional_event)

    def test_conditional_outcomes_not_in_unconditional_outcomes(self):
        unconditional_event = Event[int](range(4))
        conditional_event = Event[int](range(3, 7))
        with pytest.raises(AttributeError):
            Entity[int](3, unconditional_event, conditional_event)

    @pytest.mark.skip("Cannot enforce strict type-checking over generic classes in Python.")
    def test_outcome_unconditional_event_type_mismatch(self):
        unconditional_event = Event[str](['a', 'b', 'c'])
        with pytest.raises(AttributeError):
            Entity[int](3, unconditional_event)  #pyright: ignore[reportArgumentType]

    @pytest.mark.skip("Cannot enforce strict type-checking over generic classes in Python.")
    def test_outcome_conditional_event_type_mismatch(self):
        unconditional_event = Event[int](range(4))
        conditional_event = Event[str](['a', 'b', 'c'])
        with pytest.raises(AttributeError):
            Entity[int](3, unconditional_event, conditional_event)  #pyright: ignore[reportArgumentType]

    # ---------------
    # Entity.sorted()
    # ---------------
    def test_unsortable(self):
        entity = Entity[int](
            0,
            Event[int]([0, 1]))
        with pytest.raises(TypeError):
            entity.sorted()  # pyright: ignore[reportAttributeAccessIssue]

    # -------------------
    # Entity.to_counter()
    # -------------------
    def test_uncounterable(self):
        entity = Entity[int](
            0,
            Event[int]([0, 1]))
        with pytest.raises(TypeError):
            entity.to_counter()  # pyright: ignore[reportAttributeAccessIssue]

    # ---------------
    # Entity.reduce()
    # ---------------
    def test_reduce_op_wrong_type(self):
        entity = Entity[int](
            0,
            Event[int]([0, 1]))
        with pytest.raises(TypeError):
            entity.reduce(op.add)  # pyright: ignore[reportAttributeAccessIssue]
    
    def test_reduce_initial_wrong_type(self):
        entity = Entity[tuple[int, ...]](
            (0, 1),
            Event[tuple[int, ...]]([(0, 1), (2, 1)]))
        with pytest.raises(TypeError):
            entity.reduce(op.add, 'a')  # pyright: ignore[reportArgumentType]

    # ------------
    # Entity.map()
    # ------------
    def test_map_func_wrong_type(self):
        entity = Entity[str](
            'a',
            Event[str](['a', 'b']))
        with pytest.raises(TypeError):
            entity.map(lambda x: x + 0)  # pyright: ignore[reportOperatorIssue]
