"""
Type aliases for runes by applying the Distribution and Event generic classes
onto supporting enum classes.
"""

from src.backend.utils.models.enums.runes import *
from src.backend.utils.models.types.distribution import Distribution
from src.backend.utils.models.types.event import Event
from src.backend.utils.models.types.general import HashableCounter, HashableDict


RuneRollCounts = HashableCounter[RuneStat]  # E.g. 2 rolls into SPD
RuneRollValues = HashableDict[RuneStat, int]  # E.g. rolled 18 SPD

# -------------
# Distributions
# -------------
RuneRarityDistribution = Distribution[RuneRarity]
RuneSlotDistribution = Distribution[RuneSlot]
RuneGradeDistribution = Distribution[RuneGrade]
RuneSetDistribution = Distribution[RuneSet]

RuneStatDistribution = Distribution[RuneStat]
RuneSubStatDistribution = Distribution[tuple[RuneStat, ...]]

RuneRollDistribution = Distribution[RuneRollCounts]

RuneValueDistribution = Distribution[int]
RuneSubValueDistribution = Distribution[RuneRollValues]


# ------
# Events
# ------
RuneRarityEvent = Event[RuneRarity]
RuneSlotEvent = Event[RuneSlot]
RuneGradeEvent = Event[RuneGrade]
RuneSetEvent = Event[RuneSet]

RuneStatEvent = Event[RuneStat]
RuneSubStatEvent = Event[tuple[RuneStat, ...]]

RuneRollEvent = Event[RuneRollCounts]

RuneValueEvent = Event[int]
RuneSubValueEvent = Event[RuneRollValues]

