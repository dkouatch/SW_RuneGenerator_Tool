from backend.utils.models.enums.general import Grade, Upgrade, Roll
from backend.utils.models.enums.stats import StatProperty
from backend.utils.models.enums.runes import RuneSet, RuneSlot, RuneStars

from backend.utils.models.types.distribution import GradeDistribution, RuneSetDistribution, RuneSlotDistribution, RuneStarsDistribution, PropertyDistribution, ValueDistribution, SubPropertyDistribution, UpgradeDistribution, SubValueDistribution
from backend.utils.models.types.event import GradeEvent, RuneSetEvent, RuneSlotEvent, RuneStarsEvent, PropertyEvent, ValueEvent, SubPropertyEvent, UpgradeEvent, SubValueEvent

from backend.utils.models.types.entities.runes import Rune

import pytest

@pytest.mark.integration
class TestRune:
    @pytest.fixture
    def slot_five_event(self):
        outcome = RuneSlot.FIVE
        unconditional_distribution: RuneSlotDistribution = RuneSlotDistribution(
            [member for member in RuneSlot]
        )
        return RuneSlotEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def six_star_event(self):
        outcome = RuneStars.SIX
        unconditional_distribution = RuneStarsDistribution(
            [member for member in RuneStars]
        )
        return RuneStarsEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def rare_grade_event(self):
        outcome = Grade.RARE
        unconditional_distribution = GradeDistribution(
            [member for member in Grade]
        )
        return GradeEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def violent_rune_set_event(self):
        outcome = RuneSet.VIOLENT
        unconditional_distribution = RuneSetDistribution(
            [member for member in RuneSet]
        )
        conditional_distribution = RuneSetDistribution([
            RuneSet.REVENGE, RuneSet.FOCUS, RuneSet.ENDURE, RuneSet.VIOLENT, RuneSet.GUARD
        ])
        return RuneSetEvent(outcome, unconditional_distribution, conditional_distribution)

    @pytest.fixture
    def hp_add_rune_main_property_event(self):
        outcome = StatProperty.HP_ADD
        unconditional_distribution = PropertyDistribution(
            [StatProperty.HP_ADD]
        )
        return PropertyEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def rune_main_value_event(self):
        outcome = 2400
        unconditional_distribution = ValueDistribution([2400])
        return ValueEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def no_rune_prefix_property_event(self):
        outcome = StatProperty.NO_PROPERTY
        unconditional_distribution = PropertyDistribution(
            [member for member in StatProperty]
        )
        unconditional_distribution.rebalance(StatProperty.NO_PROPERTY, 0.9)
        return PropertyEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def rune_prefix_value_event(self):
        outcome = 0
        unconditional_distribution = ValueDistribution([0])
        return ValueEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def spd_hp_mul_innate_sub_property_event(self):
        outcome = tuple(sorted([StatProperty.SPD, StatProperty.HP_MUL]))
        distribution = PropertyDistribution([
            member for member in StatProperty if member not in (StatProperty.NO_PROPERTY, StatProperty.HP_ADD)
        ])
        unconditional_distribution: SubPropertyDistribution = distribution.sample_distribution(n=2, replace=False)
        return SubPropertyEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def double_spd_innate_sub_upgrades_event(self):
        outcome = Upgrade({StatProperty.SPD: 3, StatProperty.HP_MUL: 1})
        distribution = PropertyDistribution([
            StatProperty.SPD, StatProperty.HP_MUL]).intersect_self(n=2).to_counter()
        unconditional_distribution: UpgradeDistribution = distribution.map(
            lambda counter: counter + Upgrade([StatProperty.SPD, StatProperty.HP_MUL]))
        return UpgradeEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def double_spd_innate_sub_values_event(self):
        outcome = Roll({StatProperty.SPD: 18, StatProperty.HP_MUL: 6})
        spd_value_distribution = ValueDistribution(range(4, 7)).intersect_self(3).map(sum)
        hp_mul_value_distribution = ValueDistribution(range(5, 9)).intersect_self(1).map(sum)
        unconditional_distribution: SubValueDistribution = spd_value_distribution.intersect(hp_mul_value_distribution).map(
            lambda t: Roll({StatProperty.SPD: t[0], StatProperty.HP_MUL: t[1]})
        )
        conditional_distribution: SubValueDistribution | None = unconditional_distribution.filter(
            lambda r: r[StatProperty.SPD] >= 16
        )
        return SubValueEvent(outcome, unconditional_distribution, conditional_distribution)

    @pytest.fixture
    def acc_res_additional_sub_property_event(self):
        outcome = tuple(sorted([StatProperty.ACC, StatProperty.RES]))
        distribution = PropertyDistribution([
            member for member in StatProperty if member not in (StatProperty.NO_PROPERTY, StatProperty.HP_ADD)
        ])
        unconditional_distribution: SubPropertyDistribution = distribution.sample_distribution(n=2, replace=False)
        return SubPropertyEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def acc_res_additional_sub_values_event(self):
        outcome = Roll({StatProperty.ACC: 7, StatProperty.RES: 7})
        acc_value_distribution = ValueDistribution(range(4, 9))
        res_mul_value_distribution = ValueDistribution(range(4, 9))
        unconditional_distribution: SubValueDistribution = acc_value_distribution.intersect(res_mul_value_distribution).map(
            lambda t: Roll({StatProperty.ACC: t[0], StatProperty.RES: t[1]})
        )
        conditional_distribution: SubValueDistribution | None = unconditional_distribution.filter(
            lambda r: r[StatProperty.ACC] + r[StatProperty.RES] >= 14
        )
        return SubValueEvent(outcome, unconditional_distribution, conditional_distribution)

    @pytest.fixture
    def rune(
        self,
        slot_five_event,
        six_star_event,
        rare_grade_event,
        violent_rune_set_event,
        hp_add_rune_main_property_event,
        rune_main_value_event,
        no_rune_prefix_property_event,
        rune_prefix_value_event,
        spd_hp_mul_innate_sub_property_event,
        double_spd_innate_sub_upgrades_event,
        double_spd_innate_sub_values_event,
        acc_res_additional_sub_property_event,
        acc_res_additional_sub_values_event
        ) -> Rune:
        return Rune(
            slot=slot_five_event,
            stars=six_star_event,
            default_grade=rare_grade_event,
            rune_set=violent_rune_set_event,
            main_property=hp_add_rune_main_property_event,
            main_value=rune_main_value_event,
            prefix_property=no_rune_prefix_property_event,
            prefix_value=rune_prefix_value_event,
            innate_sub_properties=spd_hp_mul_innate_sub_property_event,
            innate_sub_upgrades=double_spd_innate_sub_upgrades_event,
            innate_sub_values=double_spd_innate_sub_values_event,
            additional_sub_properties=acc_res_additional_sub_property_event,
            additional_sub_values=acc_res_additional_sub_values_event
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
