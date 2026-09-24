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
    def six_star_grade_event(self):
        outcome = RuneGrade.SIX_STAR
        unconditional_distribution = RuneGradeDistribution(
            [member for member in RuneGrade]
        )
        return RuneGradeEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def rare_rarity_event(self):
        outcome = RuneRarity.RARE
        unconditional_distribution = RuneRarityDistribution(
            [member for member in RuneRarity]
        )
        return RuneRarityEvent(outcome, unconditional_distribution)

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
    def hp_add_rune_main_stat_event(self):
        outcome = RuneStat.HP_ADD
        unconditional_distribution = RuneStatDistribution(
            [RuneStat.HP_ADD]
        )
        return RuneStatEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def rune_main_value_event(self):
        outcome = 2400
        unconditional_distribution = RuneValueDistribution([2400])
        return RuneValueEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def no_rune_prefix_stat_event(self):
        outcome = RuneStat.NONE
        unconditional_distribution = RuneStatDistribution(
            [member for member in RuneStat]
        )
        unconditional_distribution.rebalance(RuneStat.NONE, 0.9)
        return RuneStatEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def rune_prefix_value_event(self):
        outcome = 0
        unconditional_distribution = RuneValueDistribution([0])
        return RuneValueEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def spd_hp_mul_innate_sub_stat_event(self):
        outcome = tuple(sorted([RuneStat.SPD, RuneStat.HP_MUL]))
        distribution = RuneStatDistribution([
            member for member in RuneStat if member not in (RuneStat.NONE, RuneStat.HP_ADD)
        ])
        unconditional_distribution: RuneSubStatDistribution = distribution.sample_distribution(n=2, replace=False)
        return RuneSubStatEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def double_spd_innate_sub_upraritys_event(self):
        outcome = RuneRollCounts({RuneStat.SPD: 3, RuneStat.HP_MUL: 1})
        distribution = RuneStatDistribution([
            RuneStat.SPD, RuneStat.HP_MUL]).intersect_self(n=2).to_counter()
        unconditional_distribution: RuneRollDistribution = distribution.map(
            lambda counter: counter + RuneRollCounts([RuneStat.SPD, RuneStat.HP_MUL]))
        return RuneRollEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def double_spd_innate_sub_values_event(self):
        outcome = RuneRollValues({RuneStat.SPD: 18, RuneStat.HP_MUL: 6})
        spd_value_distribution = RuneValueDistribution(range(4, 7)).intersect_self(3).map(sum)
        hp_mul_value_distribution = RuneValueDistribution(range(5, 9)).intersect_self(1).map(sum)
        unconditional_distribution: RuneSubValueDistribution = spd_value_distribution.intersect(hp_mul_value_distribution).map(
            lambda t: RuneRollValues({RuneStat.SPD: t[0], RuneStat.HP_MUL: t[1]})
        )
        conditional_distribution: RuneSubValueDistribution | None = unconditional_distribution.filter(
            lambda r: r[RuneStat.SPD] >= 16
        )
        return RuneSubValueEvent(outcome, unconditional_distribution, conditional_distribution)

    @pytest.fixture
    def acc_res_additional_sub_stat_event(self):
        outcome = tuple(sorted([RuneStat.ACC, RuneStat.RES]))
        distribution = RuneStatDistribution([
            member for member in RuneStat if member not in (RuneStat.NONE, RuneStat.HP_ADD)
        ])
        unconditional_distribution: RuneSubStatDistribution = distribution.sample_distribution(n=2, replace=False)
        return RuneSubStatEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def acc_res_additional_sub_values_event(self):
        outcome = RuneRollValues({RuneStat.ACC: 7, RuneStat.RES: 7})
        acc_value_distribution = RuneValueDistribution(range(4, 9))
        res_mul_value_distribution = RuneValueDistribution(range(4, 9))
        unconditional_distribution: RuneSubValueDistribution = acc_value_distribution.intersect(res_mul_value_distribution).map(
            lambda t: RuneRollValues({RuneStat.ACC: t[0], RuneStat.RES: t[1]})
        )
        conditional_distribution: RuneSubValueDistribution | None = unconditional_distribution.filter(
            lambda r: r[RuneStat.ACC] + r[RuneStat.RES] >= 14
        )
        return RuneSubValueEvent(outcome, unconditional_distribution, conditional_distribution)

    @pytest.fixture
    def rune(
        self,
        slot_five_event,
        six_star_grade_event,
        rare_rarity_event,
        violent_rune_set_event,
        hp_add_rune_main_stat_event,
        rune_main_value_event,
        no_rune_prefix_stat_event,
        rune_prefix_value_event,
        spd_hp_mul_innate_sub_stat_event,
        double_spd_innate_sub_upraritys_event,
        double_spd_innate_sub_values_event,
        acc_res_additional_sub_stat_event,
        acc_res_additional_sub_values_event
        ) -> Rune:
        return Rune(
            slot=slot_five_event,
            grade=six_star_grade_event,
            rarity=rare_rarity_event,
            set=violent_rune_set_event,
            main_stat=hp_add_rune_main_stat_event,
            main_value=rune_main_value_event,
            prefix_stat=no_rune_prefix_stat_event,
            prefix_value=rune_prefix_value_event,
            innate_sub_stats=spd_hp_mul_innate_sub_stat_event,
            innate_sub_upraritys=double_spd_innate_sub_upraritys_event,
            innate_sub_values=double_spd_innate_sub_values_event,
            additional_sub_stats=acc_res_additional_sub_stat_event,
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
