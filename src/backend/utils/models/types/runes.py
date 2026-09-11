import math
from typeguard import typechecked

from src.backend.utils.models.types.entities import *

@typechecked
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
        innate_sub_values (list[ValueEntity]): Entity over tuples of innate sub-stat property values.

        additional_sub_properties (SubPropertyEntity): Entity over tuples of additional sub-stat properties.
        additional_sub_values (list[ValueEntity]): Entity over tuples of additional sub-stat property values.
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
            innate_sub_values: list[ValueEntity],
            additional_sub_properties: SubPropertyEntity,
            additional_sub_values: list[ValueEntity],
        ):
        self._entities: dict[str, Entity | list[Entity]] = {
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
        entities: list[Entity] = []
        for value in self._entities.values():
            if isinstance(value, list):
                value = cast(list[Entity], value)
                entities += value
            elif isinstance(value, Entity):
                entities.append(value)
        return entities

    @property
    def probability(self) -> int | float:
        return math.prod(entity.probability for entity in self.entities)
    
    @property
    def likelihood(self) -> int | float:
        return 1.0 / self.probability
    
    def uncondition(self, key: str, index: int | None=None) -> None:
        """Unconditions an entity by querying the internal dictionary.

        Args:
            key (str): Key (e.g, "stars", "slot", etc.)
            index (int | None, optional): Index for keys that are lists of entites. Defaults to None.

        Raises:
            KeyError: Keys the wrong type, list[Entity] instead of Entity, vice versa
            KeyError: Index is out of bounds for the queried list of Entity objects
        """
        if index is None:
            if not isinstance((entity := self._entities[key]), Entity):
                raise KeyError(f"Key '{key}' has type 'list[Entity]' instead of 'Entity'.")
            entity.uncondition()
        else:
            if not isinstance((entity_list := self._entities[key]), list):
                raise KeyError(f"Key '{key}' has type 'Entity' instead of 'list[Entity]'.")
            elif index >= (length:= len(entity_list)):
                raise KeyError(f"Index {index} is out of bounds for entity list of length {length}.")
            entity = cast(Entity, entity_list[index])
            entity.uncondition()
    
    def condition(self, key: str, index: int | None=None) -> None:
        """Conditions an entity by querying the internal dictionary.

        Args:
            key (str): Key (e.g, "stars", "slot", etc.)
            index (int | None, optional): Index for keys that are lists of entites. Defaults to None.

        Raises:
            KeyError: Keys the wrong type, list[Entity] instead of Entity, vice versa
            KeyError: Index is out of bounds for the queried list of Entity objects
        """
        if index is None:
            if not isinstance((entity := self._entities[key]), Entity):
                raise KeyError(f"Key '{key}' has type 'list[Entity]' instead of 'Entity'.")
            entity.condition()
        else:
            if not isinstance((entity_list := self._entities[key]), list):
                raise KeyError(f"Key '{key}' has type 'Entity' instead of 'list[Entity]'.")
            elif index >= (length:= len(entity_list)):
                raise KeyError(f"Index {index} is out of bounds for entity list of length {length}.")
            entity = cast(Entity, entity_list[index])
            entity.condition()
    
    def reset(self) -> None:
        """Unconditions all entities
        """
        for entity in self.entities:
            entity.uncondition()


"""
    def __str__(self):
        return (f'''
{self._stars}* {self._rune_set} {self._default_grade}
MAIN: {self._main_property} -> {self._main_value}
PREFIX: {self._prefix_property} -> {self._prefix_value}
SUBS: {list(zip(self._innate_sub_properties + self._additional_sub_properties, self._innate_sub_values + self._additional_sub_values))}
''')
"""
