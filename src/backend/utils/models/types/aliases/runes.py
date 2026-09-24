"""
Type aliases for runes by applying the Distribution and Event generic classes
onto supporting enum classes.
"""

from src.backend.utils.models.enums.runes import RuneGrade, RuneSlot, RuneSet, RuneStars, RuneProperty
from src.backend.utils.models.types.distribution import Distribution
from src.backend.utils.models.types.event import Event
from src.backend.utils.models.types.general import HashableCounter, HashableDict


RuneRollCounts = HashableCounter[RuneProperty]  # E.g. 2 rolls into SPD
RuneRollValues = HashableDict[RuneProperty, int]  # E.g. rolled 18 SPD

# -------------
# Distributions
# -------------
RuneGradeDistribution = Distribution[RuneGrade]
RuneSlotDistribution = Distribution[RuneSlot]
RuneStarsDistribution = Distribution[RuneStars]
RuneSetDistribution = Distribution[RuneSet]

RunePropertyDistribution = Distribution[RuneProperty]
RuneSubPropertyDistribution = Distribution[tuple[RuneProperty, ...]]

RuneRollDistribution = Distribution[RuneRollCounts]

RuneValueDistribution = Distribution[int]
RuneSubValueDistribution = Distribution[RuneRollValues]


# ------
# Events
# ------
RuneGradeEvent = Event[RuneGrade]
RuneSlotEvent = Event[RuneSlot]
RuneStarsEvent = Event[RuneStars]
RuneSetEvent = Event[RuneSet]

RunePropertyEvent = Event[RuneProperty]
RuneSubPropertyEvent = Event[tuple[RuneProperty, ...]]

RuneRollEvent = Event[RuneRollCounts]

RuneValueEvent = Event[int]
RuneSubValueEvent = Event[RuneRollValues]

