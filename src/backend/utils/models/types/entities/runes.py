from typeguard import typechecked

from src.backend.utils.models.types.aliases.runes import *
from src.backend.utils.models.types.entity import Entity
from src.backend.utils.models.types.event import Event

class Rune(Entity):
    """
    Class definition for a rune object.

    Attributes:
        slot (RuneSlotEvent): The slot of the rune (1-6).
        grade (RuneGradeEvent): The grade rating of the rune (1-6).
        rarity (RuneRarityEvent): The rarity of the rune.
        set (RuneSetEvent): The set of the rune

        main_stat (RuneStatEvent): The main stat stat of the rune.
        main_value (RuneValueEvent): The main stat value of the rune

        prefix_stat (RuneStatEvent): The prefix stat stat.
        prefix_value (RuneValueEvent): The prefix stat value.

        innate_sub_stats (RuneSubStatEvent): Event over tuples of innate sub-stat stats.
        innate_sub_upraritys (RuneRollEvent): Event over tuples of innate sub-stat stat uprarity counts.
        innate_sub_values (RuneSubValueEvent): Event over tuples of innate sub-stat stat values.

        additional_sub_stats (RuneSubStatEvent): Event over tuples of additional sub-stat stats.
        additional_sub_values (RuneSubValueEvent): Event over tuples of additional sub-stat stat values.
    """
    def __init__(
            self,
            slot: RuneSlotEvent,
            grade: RuneGradeEvent,
            rarity: RuneRarityEvent,
            set: RuneSetEvent,
            main_stat: RuneStatEvent,
            main_value: RuneValueEvent,
            prefix_stat: RuneStatEvent,
            prefix_value: RuneValueEvent,
            innate_sub_stats: RuneSubStatEvent,
            innate_sub_upraritys: RuneRollEvent,
            innate_sub_values: RuneSubValueEvent,
            additional_sub_stats: RuneSubStatEvent,
            additional_sub_values: RuneSubValueEvent,
        ):
        events: dict[str, Event] = {
            "slot": slot,
            "grade": grade,
            "rarity": rarity,
            "set": set,
            "main_stat": main_stat,
            "main_value": main_value,
            "prefix_stat": prefix_stat,
            "prefix_value": prefix_value,
            "innate_sub_stats": innate_sub_stats,
            "innate_sub_upraritys": innate_sub_upraritys,
            "innate_sub_values": innate_sub_values,
            "additional_sub_stats": additional_sub_stats,
            "additional_sub_values": additional_sub_values
        }
        super().__init__(events)
    
    def __str__(self) -> str:
        return (f'''
SLOT {self._events["slot"].outcome} {'*' * self._events["grade"].outcome.value} {self._events["rarity"].outcome} {self._events["set"].outcome}
MAIN: {self._events["main_stat"].outcome} ({self._events["main_value"].outcome})
PREFIX: {self._events["prefix_stat"].outcome} ({self._events["prefix_value"].outcome})
SUBS: {self._events["innate_sub_values"].outcome | self._events["additional_sub_values"].outcome}
''')
