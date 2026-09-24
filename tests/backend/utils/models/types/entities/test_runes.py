from backend.utils.models.enums.runes import *
from backend.utils.models.types.aliases.runes import *
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
        outcome = RuneGrade.RARE
        unconditional_distribution = RuneGradeDistribution(
            [member for member in RuneGrade]
        )
        return RuneGradeEvent(outcome, unconditional_distribution)

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
        outcome = RuneProperty.HP_ADD
        unconditional_distribution = RunePropertyDistribution(
            [RuneProperty.HP_ADD]
        )
        return RunePropertyEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def rune_main_value_event(self):
        outcome = 2400
        unconditional_distribution = RuneValueDistribution([2400])
        return RuneValueEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def no_rune_prefix_property_event(self):
        outcome = RuneProperty.NO_PROPERTY
        unconditional_distribution = RunePropertyDistribution(
            [member for member in RuneProperty]
        )
        unconditional_distribution.rebalance(RuneProperty.NO_PROPERTY, 0.9)
        return RunePropertyEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def rune_prefix_value_event(self):
        outcome = 0
        unconditional_distribution = RuneValueDistribution([0])
        return RuneValueEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def spd_hp_mul_innate_sub_property_event(self):
        outcome = tuple(sorted([RuneProperty.SPD, RuneProperty.HP_MUL]))
        distribution = RunePropertyDistribution([
            member for member in RuneProperty if member not in (RuneProperty.NO_PROPERTY, RuneProperty.HP_ADD)
        ])
        unconditional_distribution: RuneSubPropertyDistribution = distribution.sample_distribution(n=2, replace=False)
        return RuneSubPropertyEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def double_spd_innate_sub_upgrades_event(self):
        outcome = RuneRollCounts({RuneProperty.SPD: 3, RuneProperty.HP_MUL: 1})
        distribution = RunePropertyDistribution([
            RuneProperty.SPD, RuneProperty.HP_MUL]).intersect_self(n=2).to_counter()
        unconditional_distribution: RuneRollDistribution = distribution.map(
            lambda counter: counter + RuneRollCounts([RuneProperty.SPD, RuneProperty.HP_MUL]))
        return RuneRollEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def double_spd_innate_sub_values_event(self):
        outcome = RuneRollValues({RuneProperty.SPD: 18, RuneProperty.HP_MUL: 6})
        spd_value_distribution = RuneValueDistribution(range(4, 7)).intersect_self(3).map(sum)
        hp_mul_value_distribution = RuneValueDistribution(range(5, 9)).intersect_self(1).map(sum)
        unconditional_distribution: RuneSubValueDistribution = spd_value_distribution.intersect(hp_mul_value_distribution).map(
            lambda t: RuneRollValues({RuneProperty.SPD: t[0], RuneProperty.HP_MUL: t[1]})
        )
        conditional_distribution: RuneSubValueDistribution | None = unconditional_distribution.filter(
            lambda r: r[RuneProperty.SPD] >= 16
        )
        return RuneSubValueEvent(outcome, unconditional_distribution, conditional_distribution)

    @pytest.fixture
    def acc_res_additional_sub_property_event(self):
        outcome = tuple(sorted([RuneProperty.ACC, RuneProperty.RES]))
        distribution = RunePropertyDistribution([
            member for member in RuneProperty if member not in (RuneProperty.NO_PROPERTY, RuneProperty.HP_ADD)
        ])
        unconditional_distribution: RuneSubPropertyDistribution = distribution.sample_distribution(n=2, replace=False)
        return RuneSubPropertyEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def acc_res_additional_sub_values_event(self):
        outcome = RuneRollValues({RuneProperty.ACC: 7, RuneProperty.RES: 7})
        acc_value_distribution = RuneValueDistribution(range(4, 9))
        res_mul_value_distribution = RuneValueDistribution(range(4, 9))
        unconditional_distribution: RuneSubValueDistribution = acc_value_distribution.intersect(res_mul_value_distribution).map(
            lambda t: RuneRollValues({RuneProperty.ACC: t[0], RuneProperty.RES: t[1]})
        )
        conditional_distribution: RuneSubValueDistribution | None = unconditional_distribution.filter(
            lambda r: r[RuneProperty.ACC] + r[RuneProperty.RES] >= 14
        )
        return RuneSubValueEvent(outcome, unconditional_distribution, conditional_distribution)

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
            set=violent_rune_set_event,
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
