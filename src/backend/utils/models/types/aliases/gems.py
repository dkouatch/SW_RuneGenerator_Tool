"""
Type aliases for gems by applying the Distribution and Event generic classes
onto supporting enum classes.
"""

from src.backend.utils.models.enums.gems import GemGrade, GemSet, GemProperty
from src.backend.utils.models.types.distribution import Distribution
from src.backend.utils.models.types.event import Event
from src.backend.utils.models.types.general import HashableCounter, HashableDict

# -------------
# Distributions
# -------------
GemGradeDistribution = Distribution[GemGrade]
GemSetDistribution = Distribution[GemSet]
GemPropertyDistribution = Distribution[GemProperty]
GemValueDistribution = Distribution[int]

# ------
# Events
# ------
GemGradeEvent = Event[GemGrade]
GemSetEvent = Event[GemSet]
GemPropertyEvent = Event[GemProperty]
GemValueEvent = Event[int]
