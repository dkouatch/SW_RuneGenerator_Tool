from backend.utils.models.types.distribution import Distribution


import pytest
from enum import IntEnum, unique

from src.backend.utils.models.types.distribution import Distribution
from src.backend.utils.models.types.event import Event
from src.backend.utils.models.types.entity import Entity

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
CoinTossEvent = Event[CoinTosses]
DiceRollEvent = Event[DiceRolls]


class GameEntity(Entity):
    def __init__(
        self,
        coin_tosses: CoinTossEvent,
        dice_rolls: DiceRollEvent):
        super().__init__({
            "coins": coin_tosses,
            "dice": dice_rolls
        })


@pytest.mark.unit
class TestEntity:
    @pytest.fixture
    def coin_toss_event(self) -> CoinTossEvent:
        outcome: CoinTosses = (CoinToss.HEADS, CoinToss.TAILS, CoinToss.HEADS)
        three_unconditional_tosses: Distribution[CoinTosses] = Distribution[CoinToss](
            [member for member in CoinToss]).intersect_self(3)
        three_conditional_tosses: Distribution[CoinTosses] | None= three_unconditional_tosses.filter(
            lambda tosses: sum((toss == CoinToss.HEADS) for toss in tosses) >= 2
        )
        return CoinTossEvent(
            outcome,
            three_unconditional_tosses,
            three_conditional_tosses
        )

    @pytest.fixture
    def dice_roll_event(self) -> DiceRollEvent:
        outcome: DiceRolls = (DiceRoll.THREE, DiceRoll.FIVE, DiceRoll.TWO)
        three_unconditional_rolls: Distribution[DiceRolls] = Distribution[DiceRoll](
            [member for member in DiceRoll]).intersect_self(3)
        three_conditional_rolls = three_unconditional_rolls.filter(
            lambda rolls: sum(int(roll) for roll in rolls) >= 6
        )
        return DiceRollEvent(
            outcome,
            three_unconditional_rolls,
            three_conditional_rolls
        )
    
    @pytest.fixture
    def game_entity(
        self,
        coin_toss_event,
        dice_roll_event
    ) -> GameEntity:
        return GameEntity(
            coin_toss_event,
            dice_roll_event
        )
