from backend.utils.models.enums.grinds import *
from backend.utils.models.types.aliases.grinds import *
from backend.utils.models.types.entities.grinds import Grind

import pytest

@pytest.mark.integration
class TestGrind:
    @pytest.fixture
    def rare_grade_event(self):
        outcome = GrindGrade.HERO
        unconditional_distribution = GrindGradeDistribution(
            [member for member in GrindGrade]
        )
        return GrindGradeEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def swift_set_event(self):
        outcome = GrindSet.SWIFT
        unconditional_distribution = GrindSetDistribution(
            [member for member in GrindSet]
        )
        conditional_distribution = GrindSetDistribution([
            GrindSet.SWIFT, GrindSet.DESPAIR, GrindSet.BLADE, GrindSet.FATAL, GrindSet.ENERGY
        ])
        return GrindSetEvent(outcome, unconditional_distribution, conditional_distribution)

    @pytest.fixture
    def def_mul_grind_property_event(self):
        outcome = GrindProperty.DEF_MUL
        unconditional_distribution = GrindPropertyDistribution(
            [member for member in GrindProperty]
        )
        return GrindPropertyEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def def_mul_grind_value_event(self):
        outcome = 18
        unconditional_distribution = GrindValueDistribution(range(12, 23))
        return GrindValueEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def grind(
        self,
        rare_grade_event,
        swift_set_event,
        def_mul_grind_property_event,
        def_mul_grind_value_event
        ) -> Grind:
        return Grind(
            grade=rare_grade_event,
            set=swift_set_event,
            property=def_mul_grind_property_event,
            value=def_mul_grind_value_event
        )
    
    def test_grind_init(self, grind):
        assert True
