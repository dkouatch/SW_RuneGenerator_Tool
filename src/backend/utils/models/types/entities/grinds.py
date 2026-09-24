from typeguard import typechecked

from src.backend.utils.models.types.aliases.grinds import *
from src.backend.utils.models.types.entity import Entity
from src.backend.utils.models.types.event import Event

class Grind(Entity):
    """
    Class definition for a grind object.

    Attributes:
        rarity (GrindRarityEvent): The default rarity of the grind.
        set (GrindSetEvent): The set of the grind.
        stat (GrindStatEvent): The stat of the grind.
        value (GrindValueEvent): The value of the grind
    """
    def __init__(
            self,
            rarity: GrindRarityEvent,
            set: GrindSetEvent,
            stat: GrindStatEvent,
            value: GrindValueEvent
        ):
        events: dict[str, Event] = {
            "rarity": rarity,
            "set": set,
            "stat": stat,
            "value": value
        }
        super().__init__(events)
