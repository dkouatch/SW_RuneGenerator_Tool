from backend.utils.models.enums.gems import *
from backend.utils.models.types.aliases.gems import *
from backend.utils.models.types.entities.gems import Gem

import pytest

@pytest.mark.integration
class TestGem:
    @pytest.fixture
    def legend_rarity_event(self):
        outcome = GemRarity.LEGEND
        unconditional_distribution = GemRarityDistribution(
            [member for member in GemRarity]
        )
        return GemRarityEvent(outcome, unconditional_distribution)

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
    def crit_dmg_gem_stat_event(self):
        outcome = GemStat.CD
        unconditional_distribution = GemStatDistribution(
            [member for member in GemStat]
        )
        return GemStatEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def crit_dmg_gem_value_event(self):
        outcome = 8
        unconditional_distribution = GemValueDistribution(range(7, 11))
        return GemValueEvent(outcome, unconditional_distribution)

    @pytest.fixture
    def gem(
        self,
        legend_rarity_event,
        rage_set_event,
        crit_dmg_gem_stat_event,
        crit_dmg_gem_value_event
        ) -> Gem:
        return Gem(
            rarity=legend_rarity_event,
            set=rage_set_event,
            stat=crit_dmg_gem_stat_event,
            value=crit_dmg_gem_value_event
        )
    
    def test_gem_init(self, gem):
        assert True
