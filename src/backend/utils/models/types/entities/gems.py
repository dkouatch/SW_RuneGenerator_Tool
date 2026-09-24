from typeguard import typechecked

from src.backend.utils.models.types.aliases.gems import *
from src.backend.utils.models.types.entity import Entity
from src.backend.utils.models.types.event import Event

class Gem(Entity):
    """
    Class definition for a gem object.

    Attributes:
        grade (GemGradeEvent): The default grade of the gem.
        set (GemSetEvent): The set of the gem.
        property (GemPropertyEvent): The stat property of the gem.
        value (GemValueEvent): The main stat value of the gem
    """
    def __init__(
            self,
            grade: GemGradeEvent,
            set: GemSetEvent,
            property: GemPropertyEvent,
            value: GemValueEvent
        ):
        events: dict[str, Event] = {
            "grade": grade,
            "set": set,
            "property": property,
            "value": value
        }
        super().__init__(events)
