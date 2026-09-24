"""
Type aliases for grinds by applying the Distribution and Event generic classes
onto supporting enum classes.
"""

from src.backend.utils.models.enums.grinds import GrindRarity, GrindSet, GrindStat
from src.backend.utils.models.types.distribution import Distribution
from src.backend.utils.models.types.event import Event
from src.backend.utils.models.types.general import HashableCounter, HashableDict

# -------------
# Distributions
# -------------
GrindRarityDistribution = Distribution[GrindRarity]
GrindSetDistribution = Distribution[GrindSet]
GrindStatDistribution = Distribution[GrindStat]
GrindValueDistribution = Distribution[int]

# ------
# Events
# ------
GrindRarityEvent = Event[GrindRarity]
GrindSetEvent = Event[GrindSet]
GrindStatEvent = Event[GrindStat]
GrindValueEvent = Event[int]
