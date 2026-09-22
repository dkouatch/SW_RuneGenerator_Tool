import math
from typeguard import typechecked

from src.backend.utils.models.types.entities import *

class Rune:
    """
    Class definition for an immutable Rune object.

    Attributes:
        slot (RuneSlotEntity): The slot of the rune (1-6).
        stars (RuneStarsEntity): The star rating of the rune (1-6).
        default_grade (GradeEntity): The default grade of the rune.

        main_property (PropertyEntity): The main stat property of the rune.
        main_value (ValueEntity): The main stat value of the rune

        prefix_property (PropertyEntity): The prefix stat property.
        prefix_value (ValueEntity): The prefix stat value.

        innate_sub_properties (SubPropertyEntity): Entity over tuples of innate sub-stat properties.
        innate_sub_upgrades (UpgradeEntity): Entity over tuples of innate sub-stat property upgrade counts.
        innate_sub_values (SubValueEntity): Entity over tuples of innate sub-stat property values.

        additional_sub_properties (SubPropertyEntity): Entity over tuples of additional sub-stat properties.
        additional_sub_values (SubValueEntity): Entity over tuples of additional sub-stat property values.
    """
    def __init__(
            self,
            slot: RuneSlotEntity,
            stars: RuneStarsEntity,
            default_grade: GradeEntity,
            rune_set: RuneSetEntity,
            main_property: PropertyEntity,
            main_value: ValueEntity,
            prefix_property: PropertyEntity,
            prefix_value: ValueEntity,
            innate_sub_properties: SubPropertyEntity,
            innate_sub_upgrades: UpgradeEntity,
            innate_sub_values: SubValueEntity,
            additional_sub_properties: SubPropertyEntity,
            additional_sub_values: SubValueEntity,
        ):
        self._entities: dict[str, Entity] = {
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
    
    @property
    def entities(self) -> list[Entity]:
        return list(self._entities.values())

    @property
    def probability(self) -> int | float:
        return math.prod(entity.probability for entity in self.entities)
    
    @property
    def likelihood(self) -> int | float:
        return 1.0 / self.probability
    
    def uncondition(self, key: str) -> None:
        """Unconditions an entity by querying the internal dictionary.

        Args:
            key (str): Key (e.g, "stars", "slot", etc.)

        Raises:
            KeyError: Key does not exist in internal dictionary of Entity objects
        """
        if key not in self._entities.keys():
            raise KeyError(f"Key '{key}' does not exist.")
        self._entities[key].uncondition()
    
    def condition(self, key: str) -> None:
        """Conditions an entity by querying the internal dictionary.

        Args:
            key (str): Key (e.g, "stars", "slot", etc.)

        Raises:
            KeyError: Key does not exist in internal dictionary of Entity objects
        """
        if key not in self._entities.keys():
            raise KeyError(f"Key '{key}' does not exist.")
        self._entities[key].condition()
    
    def reset(self) -> None:
        """Unconditions all entities
        """
        for entity in self.entities:
            entity.uncondition()
    
    def condition_all(self) -> None:
        """Conditions all entities
        """
        for entity in self.entities:
            entity.condition()
    
    def __str__(self) -> str:
        return (f'''
{self._entities["stars"].outcome}* {self._entities["default_grade"].outcome} {self._entities["rune_set"].outcome}
MAIN: {self._entities["main_property"].outcome} ({self._entities["main_value"].outcome})
PREFIX: {self._entities["prefix_property"].outcome} ({self._entities["prefix_value"].outcome})
SUBS: {zip(self._entities["innate_sub_properties"].outcome + self._entities["additional_sub_properties"].outcome,
self._entities["innate_sub_values"].outcome + self._entities["additional_sub_values"].outcome)}
''')
