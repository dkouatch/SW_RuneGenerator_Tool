from typeguard import typechecked

from src.backend.utils.models.types.aliases.grinds import *
from src.backend.utils.models.types.entity import Entity
from src.backend.utils.models.types.event import Event

class Grind(Entity):
    """
    Class definition for a grind object.

    Attributes:
        grade (GrindGradeEvent): The default grade of the grind.
        set (GrindSetEvent): The set of the grind.
        property (GrindPropertyEvent): The stat property of the grind.
        value (GrindValueEvent): The main stat value of the grind
    """
    def __init__(
            self,
            grade: GrindGradeEvent,
            set: GrindSetEvent,
            property: GrindPropertyEvent,
            value: GrindValueEvent
        ):
        events: dict[str, Event] = {
            "grade": grade,
            "set": set,
            "property": property,
            "value": value
        }
        super().__init__(events)
