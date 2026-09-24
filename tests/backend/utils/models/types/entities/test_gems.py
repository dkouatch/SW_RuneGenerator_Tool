from backend.utils.models.enums.gems import *
from backend.utils.models.types.aliases.gems import *
from backend.utils.models.types.entities.gems import Gem

import pytest

@pytest.mark.integration
class TestGem:
    @pytest.fixture
    def legend_grade_event(self):
        outcome = GemGrade.LEGEND
        unconditional_distribution = GemGradeDistribution(
            [member for member in GemGrade]
        )
        return GemGradeEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def rage_set_event(self):
        outcome = GemSet.RAGE
        unconditional_distribution = GemSetDistribution(
            [member for member in GemSet]
        )
        conditional_distribution = GemSetDistribution([
            GemSet.RAGE, GemSet.VAMPIRE, GemSet.NEMESIS, GemSet.WILL, GemSet.DESTROY
        ])
        return GemSetEvent(outcome, unconditional_distribution, conditional_distribution)

    @pytest.fixture
    def crit_dmg_gem_property_event(self):
        outcome = GemProperty.CD
        unconditional_distribution = GemPropertyDistribution(
            [member for member in GemProperty]
        )
        return GemPropertyEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def crit_dmg_gem_value_event(self):
        outcome = 8
        unconditional_distribution = GemValueDistribution(range(7, 11))
        return GemValueEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def gem(
        self,
        legend_grade_event,
        rage_set_event,
        crit_dmg_gem_property_event,
        crit_dmg_gem_value_event
        ) -> Gem:
        return Gem(
            grade=legend_grade_event,
            set=rage_set_event,
            property=crit_dmg_gem_property_event,
            value=crit_dmg_gem_value_event
        )
    
    def test_gem_init(self, gem):
        assert True
