"""
Type aliases for gems by applying the Distribution and Event generic classes
onto supporting enum classes.
"""

from src.backend.utils.models.enums.gems import GemRarity, GemSet, GemStat
from src.backend.utils.models.types.distribution import Distribution
from src.backend.utils.models.types.event import Event
from src.backend.utils.models.types.general import HashableCounter, HashableDict

# -------------
# Distributions
# -------------
GemRarityDistribution = Distribution[GemRarity]
GemSetDistribution = Distribution[GemSet]
GemStatDistribution = Distribution[GemStat]
GemValueDistribution = Distribution[int]

# ------
# Events
# ------
GemRarityEvent = Event[GemRarity]
GemSetEvent = Event[GemSet]
GemStatEvent = Event[GemStat]
GemValueEvent = Event[int]
