import src.backend.utils.data_inputs.runes as runes_input

from src.backend.utils.models.types.runes import RuneManager
from src.backend.utils.models.enums.general import Upgrade
from src.backend.utils.data_inputs.templates import *

def create_rune(ask_input: bool = True) -> None:
    """Creates a Rune object either from user input or randomly generated.

    Args:
        ask_input (bool, optional): If True, prompts user for input. Defaults to True.

    Returns:
        Rune: The created Rune object.
    """
    # Get basic rune attributes
    slot = runes_input.get_rune_slot(ask_input)
    stars = runes_input.get_rune_stars(ask_input)
    default_grade = runes_input.get_rune_default_grade(ask_input)
    rune_set = runes_input.get_rune_set(ask_input)
    stage = runes_input.get_rune_stage(default_grade.value)

    # Get main property
    main_property = runes_input.get_main_property(slot.value, ask_input)
    main_value = runes_input.get_main_value(
        stars.value, stage.value, main_property.value)

    # Get prefix property
    prefix_property = runes_input.get_prefix_property(
        slot.value, main_property.value, ask_input)
    prefix_value = runes_input.get_prefix_value(
        stars.value, prefix_property.value, ask_input)

    # Get sub properties
    innate_sub_properties = runes_input.get_innate_sub_properties(
        slot.value, default_grade.value, main_property.value, prefix_property.value, ask_input=ask_input)
    innate_sub_upgrades = runes_input.get_innate_sub_upgrades(
        innate_sub_properties.value, ask_input)
    innate_sub_values = runes_input.get_sub_values(
        stars.value, innate_sub_properties.value,
        innate_sub_upgrades.value, ask_input)
    additional_sub_properties = runes_input.get_additional_sub_properties(
        slot.value, default_grade.value, main_property.value, prefix_property.value, innate_sub_properties.value, ask_input)
    additional_sub_values = runes_input.get_sub_values(
        stars.value, additional_sub_properties.value,
        Upgrade({prop: 0 for prop in additional_sub_properties.value}))

    rune_manager = RuneManager(
        slot,
        stars,
        default_grade,
        rune_set,
        main_property,
        main_value,
        prefix_property,
        prefix_value,
        innate_sub_properties,
        innate_sub_upgrades,
        innate_sub_values,
        additional_sub_properties,
        additional_sub_values
    )
    print(f"""Created rune with probability {rune_manager.probability} (1 in {rune_manager.likelihood}):
          {rune_manager.rune}""")

def create_rune_from_template(template: dict) -> None:
    # Get basic rune attributes
    slot = runes_input.get_rune_slot(default=template["slot"])
    stars = runes_input.get_rune_stars(default=template["stars"])
    default_grade = runes_input.get_rune_default_grade(default=template["default_grade"])
    rune_set = runes_input.get_rune_set(default=template["rune_set"])
    stage = runes_input.get_rune_stage(default_grade.value)

    # Get main property
    main_property = runes_input.get_main_property(slot.value, default=template["main_property"])
    main_value = runes_input.get_main_value(
        stars.value, stage.value, main_property.value)

    # Get prefix property
    prefix_property = runes_input.get_prefix_property(
        slot.value, main_property.value, default=template["prefix_property"])
    prefix_value = runes_input.get_prefix_value(
        stars.value, prefix_property.value, default=template["prefix_value"])

    # Get sub properties
    innate_sub_properties = runes_input.get_innate_sub_properties(
        slot.value, default_grade.value, main_property.value,
        prefix_property.value, default=template["innate_sub_properties"])
    innate_sub_upgrades = runes_input.get_innate_sub_upgrades(
        list(innate_sub_properties.value), default=template["innate_sub_upgrades"])
    innate_sub_values = runes_input.get_sub_values(
        stars.value, innate_sub_properties.value,
        innate_sub_upgrades.value, default=template["innate_sub_values"])
    additional_sub_properties = runes_input.get_additional_sub_properties(
        slot.value, default_grade.value, main_property.value,
        prefix_property.value, list(innate_sub_properties.value),
        default=template["additional_sub_properties"])
    additional_sub_values = runes_input.get_sub_values(
        stars.value, additional_sub_properties.value,
        None if additional_sub_properties.value is None else Upgrade({prop: 0 for prop in additional_sub_properties.value}),
        default=template["additional_sub_values"])

    rune_manager = RuneManager(
        slot,
        stars,
        default_grade,
        rune_set,
        main_property,
        main_value,
        prefix_property,
        prefix_value,
        innate_sub_properties,
        innate_sub_upgrades,
        innate_sub_values,
        additional_sub_properties,
        additional_sub_values
    )
    rune_manager.unfix_all()
    print(f"""Created rune with probability {rune_manager.probability} (1 in {rune_manager.likelihood}):
          {rune_manager.rune}""")


if __name__ == "__main__":
    create_rune_from_template(NORMAL_SLOT_ONE_NO_PREFIX_RUNE)
    create_rune_from_template(MAGIC_SLOT_TWO_WITH_PREFIX_RUNE)
    create_rune_from_template(RARE_SLOT_FIVE_NO_PREFIX_RUNE)
    create_rune_from_template(HERO_SLOT_FOUR_NO_PREFIX_RUNE)
    create_rune_from_template(LEGEND_SLOT_SIX_WITH_PREFIX_RUNE)

    # create_rune()
