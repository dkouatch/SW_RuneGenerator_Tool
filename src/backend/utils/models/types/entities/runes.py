from typeguard import typechecked

from src.backend.utils.models.types.aliases.runes import *
from src.backend.utils.models.types.entity import Entity
from src.backend.utils.models.types.event import Event

class Rune(Entity):
    """
    Class definition for an immutable Rune object.

    Attributes:
        slot (RuneSlotEvent): The slot of the rune (1-6).
        stars (RuneStarsEvent): The star rating of the rune (1-6).
        default_grade (RuneGradeEvent): The default grade of the rune.

        main_property (RunePropertyEvent): The main stat property of the rune.
        main_value (RuneValueEvent): The main stat value of the rune

        prefix_property (RunePropertyEvent): The prefix stat property.
        prefix_value (RuneValueEvent): The prefix stat value.

        innate_sub_properties (RuneSubPropertyEvent): Event over tuples of innate sub-stat properties.
        innate_sub_upgrades (RuneRollEvent): Event over tuples of innate sub-stat property upgrade counts.
        innate_sub_values (RuneSubValueEvent): Event over tuples of innate sub-stat property values.

        additional_sub_properties (RuneSubPropertyEvent): Event over tuples of additional sub-stat properties.
        additional_sub_values (RuneSubValueEvent): Event over tuples of additional sub-stat property values.
    """
    def __init__(
            self,
            slot: RuneSlotEvent,
            stars: RuneStarsEvent,
            default_grade: RuneGradeEvent,
            rune_set: RuneSetEvent,
            main_property: RunePropertyEvent,
            main_value: RuneValueEvent,
            prefix_property: RunePropertyEvent,
            prefix_value: RuneValueEvent,
            innate_sub_properties: RuneSubPropertyEvent,
            innate_sub_upgrades: RuneRollEvent,
            innate_sub_values: RuneSubValueEvent,
            additional_sub_properties: RuneSubPropertyEvent,
            additional_sub_values: RuneSubValueEvent,
        ):
        events: dict[str, Event] = {
            "slot": slot,
            "stars": stars,
            "default_grade": default_grade,
            "rune_set": rune_set,
            "main_property": main_property,
            "main_value": main_value,
            "prefix_property": prefix_property,
            "prefix_value": prefix_value,
            "innate_sub_properties": innate_sub_properties,
            "innate_sub_upgrades": innate_sub_upgrades,
            "innate_sub_values": innate_sub_values,
            "additional_sub_properties": additional_sub_properties,
            "additional_sub_values": additional_sub_values
        }
        super().__init__(events)
    
    def __str__(self) -> str:
        return (f'''
SLOT {self._events["slot"].outcome} {'*' * self._events["stars"].outcome.value} {self._events["default_grade"].outcome} {self._events["rune_set"].outcome}
MAIN: {self._events["main_property"].outcome} ({self._events["main_value"].outcome})
PREFIX: {self._events["prefix_property"].outcome} ({self._events["prefix_value"].outcome})
SUBS: {self._events["innate_sub_values"].outcome | self._events["additional_sub_values"].outcome}
''')
