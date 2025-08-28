from src.backend.utils.models.types.entities import *

class RuneManager:
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
        innate_sub_properties (SubPropertyEntity): List of innate sub-stat properties.
        sub_stat_values (list[int]): List of sub-stat values.
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
            innate_sub_values: list[ValueEntity],
            additional_sub_properties: SubPropertyEntity,
            additional_sub_values: list[ValueEntity],
        ):
        self._slot = slot
        self._stars = stars
        self._default_grade = default_grade
        self._rune_set = rune_set
        self._main_property = main_property
        self._main_value = main_value
        self._prefix_property = prefix_property
        self._prefix_value = prefix_value
        self._innate_sub_properties = innate_sub_properties
        self._innate_sub_values = innate_sub_values
        self._additional_sub_properties = additional_sub_properties
        self._additional_sub_values = additional_sub_values

        self.rune = Rune(
            slot=self._slot.value,
            stars=self._stars.value,
            default_grade=self._default_grade.value,
            rune_set=self._rune_set.value,
            main_property=self._main_property.value,
            main_value=self._main_value.value,
            prefix_property=self._prefix_property.value,
            prefix_value=self._prefix_value.value,
            innate_sub_properties=self._innate_sub_properties.value,
            innate_sub_values=[v.value for v in self._innate_sub_values],
            additional_sub_properties=self._additional_sub_properties.value,
            additional_sub_values=[v.value for v in self._additional_sub_values],
        )

class Rune:
    """
    Class definition for a Rune object.
    """
    def __init__(
            self,
            slot: RuneSlot,
            stars: RuneStars,
            default_grade: Grade,
            rune_set: RuneSet,
            main_property: StatProperty,
            main_value: int,
            prefix_property: StatProperty,
            prefix_value: int,
            innate_sub_properties: tuple[StatProperty, ...],
            innate_sub_values: list[int],
            additional_sub_properties: tuple[StatProperty, ...],
            additional_sub_values: list[int],):
        self._slot = slot
        self._stars = stars
        self._default_grade = default_grade
        self._rune_set = rune_set
        self._main_property = main_property
        self._main_value = main_value
        self._prefix_property = prefix_property
        self._prefix_value = prefix_value
        self._innate_sub_properties = innate_sub_properties
        self._innate_sub_values = innate_sub_values
        self._additional_sub_properties = additional_sub_properties
        self._additional_sub_values = additional_sub_values
    
    def __str__(self):
        print(f"""
{self._stars}* {self._rune_set} {self._default_grade}
MAIN: {self._main_stat_property} -> {self._main_stat_value}
PREFIX: {self._prefix_stat_property} -> {self._prefix_stat_value}
SUBS: {list(zip(self._innate_sub_properties + self._additional_sub_properties, self._innate_sub_values + self._additional_sub_values))}
""")
