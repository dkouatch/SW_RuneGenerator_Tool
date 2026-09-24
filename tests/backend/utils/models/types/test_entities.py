import pytest
from math import isclose

from . import CoinToss, DiceRoll
from src.backend.utils.models.types.distribution import Distribution
from src.backend.utils.models.types.event import Event
from src.backend.utils.models.types.entity import Entity

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
        entity = GameEntity(
            coin_toss_event,
            dice_roll_event
        )
        entity.reset()
        return entity
    
    # -------------
    # Entity.events
    # -------------
    def test_game_entity_events(
        self,
        coin_toss_event: CoinTossEvent,
        dice_roll_event: DiceRollEvent,
        game_entity: GameEntity
    ):
        assert game_entity.events == [coin_toss_event, dice_roll_event]

    # ------------------
    # Entity.probability
    # ------------------
    def test_game_entity_unconditional_probability(
        self,
        game_entity: GameEntity
    ):
        assert isclose(
            game_entity.probability,
            1 / (8 * 216)
        )

    def test_game_entity_conditional_probability(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition_all()
        assert isclose(
            game_entity.probability,
            1 / (4 * 206)
        )

    def test_game_entity_reunconditioned_probability(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition_all()
        game_entity.reset()
        assert isclose(
            game_entity.probability,
            1 / (8 * 216)
        )

    # -----------------
    # Entity.likelihood
    # -----------------
    def test_game_entity_unconditional_likelihood(
        self,
        game_entity: GameEntity
    ):
        assert isclose(
            game_entity.likelihood,
            8 * 216
        )

    def test_game_entity_conditional_likelihood(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition_all()
        assert isclose(
            game_entity.likelihood,
            4 * 206
        )

    def test_game_entity_reunconditioned_likelihood(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition_all()
        game_entity.reset()
        assert isclose(
            game_entity.likelihood,
            8 * 216
        )

    # --------------
    # Entity.query()
    # --------------
    def test_game_entity_query_coins_unconditional(
        self,
        game_entity: GameEntity
    ):
        assert game_entity.query("coins") == (
            (CoinToss.HEADS, CoinToss.TAILS, CoinToss.HEADS),
            0.125
        )

    def test_game_entity_query_coins_conditional(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition("coins")
        assert game_entity.query("coins") == (
            (CoinToss.HEADS, CoinToss.TAILS, CoinToss.HEADS),
            0.25
        )

    def test_game_entity_query_dice_unconditional(
        self,
        game_entity: GameEntity
    ):
        outcome, probability = game_entity.query("dice")
        assert (
            outcome == (DiceRoll.THREE, DiceRoll.FIVE, DiceRoll.TWO)
            and isclose(probability, 1/216)
        )

    def test_game_entity_query_dice_conditional(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition("dice")
        outcome, probability = game_entity.query("dice")
        assert (
            outcome == (DiceRoll.THREE, DiceRoll.FIVE, DiceRoll.TWO)
            and isclose(probability, 1/206)
        )

    # --------------------
    # Entity.uncondition()
    # --------------------
    def test_game_entity_probability_uncondition_coins_only(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition_all()
        game_entity.uncondition("coins")
        assert isclose(
            game_entity.probability,
            1 / (8 * 206)
        )

    def test_game_entity_probability_uncondition_dice_only(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition_all()
        game_entity.uncondition("dice")
        assert isclose(
            game_entity.probability,
            1 / (4 * 216)
        )

    # ------------------
    # Entity.condition()
    # ------------------
    def test_game_entity_probability_condition_coins_only(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition("coins")
        assert isclose(
            game_entity.probability,
            1 / (4 * 216)
        )

    def test_game_entity_probability_condition_dice_only(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition("dice")
        assert isclose(
            game_entity.probability,
            1 / (8 * 206)
        )

    def test_game_entity_probability_recondition_coins_only(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition(
            "coins",
            lambda x: False)
        assert isclose(
            game_entity.probability,
            1/216
        )

    def test_game_entity_probability_recondition_dice_only(
        self,
        game_entity: GameEntity
    ):
        game_entity.condition(
            "dice",
            lambda x: False)
        assert isclose(
            game_entity.probability,
            1/8
        )