"""
Type aliases for grinds by applying the Distribution and Event generic classes
onto supporting enum classes.
"""

from src.backend.utils.models.enums.grinds import GrindGrade, GrindSet, GrindProperty
from src.backend.utils.models.types.distribution import Distribution
from src.backend.utils.models.types.event import Event
from src.backend.utils.models.types.general import HashableCounter, HashableDict

# -------------
# Distributions
# -------------
GrindGradeDistribution = Distribution[GrindGrade]
GrindSetDistribution = Distribution[GrindSet]
GrindPropertyDistribution = Distribution[GrindProperty]
GrindValueDistribution = Distribution[int]

# ------
# Events
# ------
GrindGradeEvent = Event[GrindGrade]
GrindSetEvent = Event[GrindSet]
GrindPropertyEvent = Event[GrindProperty]
GrindValueEvent = Event[int]
