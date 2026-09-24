from typeguard import typechecked

from src.backend.utils.models.types.aliases.gems import *
from src.backend.utils.models.types.entity import Entity
from src.backend.utils.models.types.event import Event

class Gem(Entity):
    """
    Class definition for a gem object.

    Attributes:
        rarity (GemRarityEvent): The default rarity of the gem.
        set (GemSetEvent): The set of the gem.
        stat (GemStatEvent): The stat of the gem.
        value (GemValueEvent): The value of the gem
    """
    def __init__(
            self,
            rarity: GemRarityEvent,
            set: GemSetEvent,
            stat: GemStatEvent,
            value: GemValueEvent
        ):
        events: dict[str, Event] = {
            "rarity": rarity,
            "set": set,
            "stat": stat,
            "value": value
        }
        super().__init__(events)
