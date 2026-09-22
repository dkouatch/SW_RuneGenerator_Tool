from backend.utils.models.enums.general import Grade, Upgrade, Roll
from backend.utils.models.enums.stats import StatProperty
from backend.utils.models.enums.runes import RuneSet, RuneSlot, RuneStars

from backend.utils.models.types.events import GradeEvent, RuneSetEvent, RuneSlotEvent, RuneStarsEvent, PropertyEvent, ValueEvent, SubPropertyEvent, UpgradeEvent, SubValueEvent
from backend.utils.models.types.entities import GradeEntity, RuneSetEntity, RuneSlotEntity, RuneStarsEntity, PropertyEntity, ValueEntity, SubPropertyEntity, UpgradeEntity, SubValueEntity

from backend.utils.models.types.runes import Rune

import pytest

@pytest.mark.integration
class TestRune:
    @pytest.fixture
    def slot_five_entity(self):
        outcome = RuneSlot.FIVE
        unconditional_event: RuneSlotEvent = RuneSlotEvent(
            [member for member in RuneSlot]
        )
        return RuneSlotEntity(outcome, unconditional_event)

    @pytest.fixture
    def six_star_entity(self):
        outcome = RuneStars.SIX
        unconditional_event = RuneStarsEvent(
            [member for member in RuneStars]
        )
        return RuneStarsEntity(outcome, unconditional_event)

    @pytest.fixture
    def rare_grade_entity(self):
        outcome = Grade.RARE
        unconditional_event = GradeEvent(
            [member for member in Grade]
        )
        return GradeEntity(outcome, unconditional_event)

    @pytest.fixture
    def violent_rune_set_entity(self):
        outcome = RuneSet.VIOLENT
        unconditional_event = RuneSetEvent(
            [member for member in RuneSet]
        )
        conditional_event = RuneSetEvent([
            RuneSet.REVENGE, RuneSet.FOCUS, RuneSet.ENDURE, RuneSet.VIOLENT, RuneSet.GUARD
        ])
        return RuneSetEntity(outcome, unconditional_event, conditional_event)

    @pytest.fixture
    def hp_add_rune_main_property_entity(self):
        outcome = StatProperty.HP_ADD
        unconditional_event = PropertyEvent(
            [StatProperty.HP_ADD]
        )
        return PropertyEntity(outcome, unconditional_event)

    @pytest.fixture
    def rune_main_value_entity(self):
        outcome = 2400
        unconditional_event = ValueEvent([2400])
        return ValueEntity(outcome, unconditional_event)

    @pytest.fixture
    def no_rune_prefix_property_entity(self):
        outcome = StatProperty.NO_PROPERTY
        unconditional_event = PropertyEvent(
            [member for member in StatProperty]
        )
        unconditional_event.rebalance(StatProperty.NO_PROPERTY, 0.9)
        return PropertyEntity(outcome, unconditional_event)

    @pytest.fixture
    def rune_prefix_value_entity(self):
        outcome = 0
        unconditional_event = ValueEvent([0])
        return ValueEntity(outcome, unconditional_event)

    @pytest.fixture
    def spd_hp_mul_innate_sub_property_entity(self):
        outcome = tuple(sorted([StatProperty.SPD, StatProperty.HP_MUL]))
        event = PropertyEvent([
            member for member in StatProperty if member not in (StatProperty.NO_PROPERTY, StatProperty.HP_ADD)
        ])
        unconditional_event: SubPropertyEvent = event.sample_event(n=2, replace=False)
        return SubPropertyEntity(outcome, unconditional_event)

    @pytest.fixture
    def double_spd_innate_sub_upgrades_entity(self):
        outcome = Upgrade({StatProperty.SPD: 3, StatProperty.HP_MUL: 1})
        event = PropertyEvent([
            StatProperty.SPD, StatProperty.HP_MUL]).intersect_self(n=2).to_counter()
        unconditional_event: UpgradeEvent = event.map(
            lambda counter: counter + Upgrade([StatProperty.SPD, StatProperty.HP_MUL]))
        return UpgradeEntity(outcome, unconditional_event)

    @pytest.fixture
    def double_spd_innate_sub_values_entity(self):
        outcome = Roll({StatProperty.SPD: 18, StatProperty.HP_MUL: 6})
        spd_value_event = ValueEvent(range(4, 7)).intersect_self(3).map(sum)
        hp_mul_value_event = ValueEvent(range(5, 9)).intersect_self(1).map(sum)
        unconditional_event: SubValueEvent = spd_value_event.intersect(hp_mul_value_event).map(
            lambda t: Roll({StatProperty.SPD: t[0], StatProperty.HP_MUL: t[1]})
        )
        conditional_event: SubValueEvent | None = unconditional_event.filter(
            lambda r: r[StatProperty.SPD] >= 16
        )
        return SubValueEntity(outcome, unconditional_event, conditional_event)

    @pytest.fixture
    def acc_res_additional_sub_property_entity(self):
        outcome = tuple(sorted([StatProperty.ACC, StatProperty.RES]))
        event = PropertyEvent([
            member for member in StatProperty if member not in (StatProperty.NO_PROPERTY, StatProperty.HP_ADD)
        ])
        unconditional_event: SubPropertyEvent = event.sample_event(n=2, replace=False)
        return SubPropertyEntity(outcome, unconditional_event)

    @pytest.fixture
    def acc_res_additional_sub_values_entity(self):
        outcome = Roll({StatProperty.ACC: 7, StatProperty.RES: 7})
        acc_value_event = ValueEvent(range(4, 9))
        res_mul_value_event = ValueEvent(range(4, 9))
        unconditional_event: SubValueEvent = acc_value_event.intersect(res_mul_value_event).map(
            lambda t: Roll({StatProperty.ACC: t[0], StatProperty.RES: t[1]})
        )
        conditional_event: SubValueEvent | None = unconditional_event.filter(
            lambda r: r[StatProperty.ACC] + r[StatProperty.RES] >= 14
        )
        return SubValueEntity(outcome, unconditional_event, conditional_event)

    @pytest.fixture
    def rune(
        self,
        slot_five_entity,
        six_star_entity,
        rare_grade_entity,
        violent_rune_set_entity,
        hp_add_rune_main_property_entity,
        rune_main_value_entity,
        no_rune_prefix_property_entity,
        rune_prefix_value_entity,
        spd_hp_mul_innate_sub_property_entity,
        double_spd_innate_sub_upgrades_entity,
        double_spd_innate_sub_values_entity,
        acc_res_additional_sub_property_entity,
        acc_res_additional_sub_values_entity
        ) -> Rune:
        return Rune(
            slot=slot_five_entity,
            stars=six_star_entity,
            default_grade=rare_grade_entity,
            rune_set=violent_rune_set_entity,
            main_property=hp_add_rune_main_property_entity,
            main_value=rune_main_value_entity,
            prefix_property=no_rune_prefix_property_entity,
            prefix_value=rune_prefix_value_entity,
            innate_sub_properties=spd_hp_mul_innate_sub_property_entity,
            innate_sub_upgrades=double_spd_innate_sub_upgrades_entity,
            innate_sub_values=double_spd_innate_sub_values_entity,
            additional_sub_properties=acc_res_additional_sub_property_entity,
            additional_sub_values=acc_res_additional_sub_values_entity
        )
    
    def test_rune_init(self, rune):
        assert True
    
    def test_rune_str(self, rune):
        assert str(rune) == f"""
SLOT 5 ****** RARE VIOLENT
MAIN: HP (2400)
PREFIX: - (0)
SUBS: {{SPD: 18, HP%: 6, ACC: 7, RES: 7}}
"""
