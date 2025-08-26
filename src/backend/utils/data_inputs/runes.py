import src.backend.utils.events.runes as rune_events

from src.backend.utils.models.enums.runes import RuneSlot, RuneStars, RuneSet
from src.backend.utils.models.enums.general import Grade
from src.backend.utils.models.enums.stats import StatProperty
from src.backend.utils.models.types.entities import *

def get_rune_slot(ask_input=False) -> RuneSlotEntity:
    """Get the rune slot from user input or return a default value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default value.
    Returns:
        RuneSlotEntity: The rune slot selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune slot."""
    if not ask_input:
        return RuneSlotEntity(RuneSlot.ONE)
    slot_input = int(input("Enter the rune slot (1-6): "))
    match slot_input:
        case 1:
            return RuneSlotEntity(RuneSlot.ONE)
        case 2:
            return RuneSlotEntity(RuneSlot.TWO)
        case 3:
            return RuneSlotEntity(RuneSlot.THREE)
        case 4:
            return RuneSlotEntity(RuneSlot.FOUR)
        case 5:
            return RuneSlotEntity(RuneSlot.FIVE)
        case 6:
            return RuneSlotEntity(RuneSlot.SIX)
        case _:
            raise ValueError("Invalid rune slot entered.")

def get_rune_stars(ask_input=False) -> RuneStarsEntity:
    """Get the rune star grade from user input or return a default value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default value.
    Returns:
        RuneStarsEntity: The rune star grade selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune star grade.
    """
    if not ask_input:
        return RuneStarsEntity(RuneStars.ONE)
    star_input = int(input("Enter the rune star grade (1-6): "))
    match star_input:
        case 1:
            return RuneStarsEntity(RuneStars.ONE)
        case 2:
            return RuneStarsEntity(RuneStars.TWO)
        case 3:
            return RuneStarsEntity(RuneStars.THREE)
        case 4:
            return RuneStarsEntity(RuneStars.FOUR)
        case 5:
            return RuneStarsEntity(RuneStars.FIVE)
        case 6:
            return RuneStarsEntity(RuneStars.SIX)
        case _:
            raise ValueError("Invalid rune slot entered.")

def get_rune_type(ask_input=False) -> RuneSetEntity:
    """Get the rune type from user input or return a default value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default value.
    Returns:
        RuneSetEntity: The rune type selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune type.
    """
    if not ask_input:
        return RuneSetEntity(RuneSet.Energy)
    type_input = str(input("Enter the rune type (Violent, Swift, Despair, etc): ")).strip().lower()
    match type_input:
        case "violent":
            return RuneSetEntity(RuneSet.Violent)
        case "swift":
            return RuneSetEntity(RuneSet.Swift)
        case "despair":
            return RuneSetEntity(RuneSet.Despair)
        case "energy":
            return RuneSetEntity(RuneSet.Energy)
        case "fatal":
            return RuneSetEntity(RuneSet.Fatal)
        case "blade":
            return RuneSetEntity(RuneSet.Blade)
        case "rage":
            return RuneSetEntity(RuneSet.Rage)
        case "will":
            return RuneSetEntity(RuneSet.Will)
        case "nemesis":
            return RuneSetEntity(RuneSet.Nemesis)
        case "vampire":
            return RuneSetEntity(RuneSet.Vampire)
        case "shield":
            return RuneSetEntity(RuneSet.Shield)
        case "revenge":
            return RuneSetEntity(RuneSet.Revenge)
        case "fight":
            return RuneSetEntity(RuneSet.Fight)
        case "determination":
            return RuneSetEntity(RuneSet.Determination)
        case "enhance":
            return RuneSetEntity(RuneSet.Enhance)
        case "accuracy":
            return RuneSetEntity(RuneSet.Accuracy)
        case "tolerance":
            return RuneSetEntity(RuneSet.Tolerance)
        case _:
            raise ValueError("Invalid rune type entered.")

def get_rune_grade(ask_input=False) -> GradeEntity:
    """Get the rune grade from user input or return a default value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default value.
    Returns:
        GradeEntity: The rune grade selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune grade.
    """
    if not ask_input:
        return GradeEntity(Grade.HERO)
    grade_input = str(input("Enter the rune grade (Normal, Magic, Rare, Hero, Legend): ")).strip().lower()
    match grade_input:
        case "normal":
            return GradeEntity(Grade.NORMAL)
        case "magic":
            return GradeEntity(Grade.MAGIC)
        case "rare":
            return GradeEntity(Grade.RARE)
        case "hero":
            return GradeEntity(Grade.HERO)
        case "legend":
            return GradeEntity(Grade.LEGEND)
        case _:
            raise ValueError("Invalid rune grade entered.")

def get_rune_stage(grade: Grade) -> ValueEntity:
    """Get stage of rune based on its grade. Currently not customizable.
    Args:
        grade (Grade): rune grade
    Returns:
        ValueEntity: rune stage (0-12)
    Raises:
        ValueError: invalid rune grade
    """
    match grade:
        case Grade.NORMAL:
            return ValueEntity(0)
        case Grade.MAGIC:
            return ValueEntity(3)
        case Grade.RARE:
            return ValueEntity(6)
        case Grade.HERO:
            return ValueEntity(9)
        case Grade.LEGEND:
            return ValueEntity(12)

def get_main_stat_property(slot: RuneSlot, ask_input=False) -> PropertyEntity:
    """Get the main stat property for a rune slot from user input or return a random property.
    Args:
        slot (RuneSlot): The rune slot for which to get the main stat property.
        ask_input (bool): If True, prompt the user for input. If False, return None.
    Returns:
        PropertyEntity: The main stat property for the rune slot.
    Raises:
        ValueError: If the user input is not a valid main stat property.
    """
    event = rune_events.get_rune_main_stat_property_event(slot)
    if not ask_input:
        return PropertyEntity(event.sample(), event)
    else:
        answer = str(input("Enter a main stat property? (y/n): ")).strip().lower()
        if answer == 'y':
            stat_input = str(input("Enter the property (ATK+/HP+/DEF+, ATK%/HP%/DEF%, SPD, CR, CD, RES, ACC): ")).strip().lower()
            match stat_input:
                case "atk+":
                    return PropertyEntity(StatProperty.ATK_ADD, event)
                case "hp+":
                    return PropertyEntity(StatProperty.HP_ADD, event)
                case "def+":
                    return PropertyEntity(StatProperty.DEF_ADD, event)
                case "atk%":
                    return PropertyEntity(StatProperty.ATK_MUL, event)
                case "hp%":
                    return PropertyEntity(StatProperty.HP_MUL, event)
                case "def%":
                    return PropertyEntity(StatProperty.DEF_MUL, event)
                case "spd":
                    return PropertyEntity(StatProperty.SPD, event)
                case "cr":
                    return PropertyEntity(StatProperty.CR, event)
                case "cd":
                    return PropertyEntity(StatProperty.CD, event)
                case "res":
                    return PropertyEntity(StatProperty.RES, event)
                case "acc":
                    return PropertyEntity(StatProperty.ACC, event)
                case _:
                    raise ValueError("Invalid main stat property entered.")
        else:
            return PropertyEntity(event.sample(), event)

def get_prefix_property(slot: RuneSlot, main_property: StatProperty, ask_input=False) -> PropertyEntity:
    """Get the prefix stat property and value from user input or return a random value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a random value.
    Returns:
        PropertyEntity: The prefix stat property
    Raises:
        ValueError: If the user input is not a valid prefix stat property.
    """
    event = rune_events.get_rune_prefix_stat_property_event(slot, main_property)
    if not ask_input:
        return PropertyEntity(event.sample(), event)
    answer = str(input("Enter a prefix stat property? (y/n): ")).strip().lower()
    if answer == 'y':
        prop_input = str(input("Enter the prefix stat property (ATK+/HP+/DEF+, ATK%/HP%/DEF%, SPD, CR, CD, RES, ACC): ")).strip().lower()
        match prop_input:
            case "atk+":
                return PropertyEntity(StatProperty.ATK_ADD, event)
            case "hp+":
                return PropertyEntity(StatProperty.HP_ADD, event)
            case "def+":
                return PropertyEntity(StatProperty.DEF_ADD, event)
            case "atk%":
                return PropertyEntity(StatProperty.ATK_MUL, event)
            case "hp%":
                return PropertyEntity(StatProperty.HP_MUL, event)
            case "def%":
                return PropertyEntity(StatProperty.DEF_MUL, event)
            case "spd":
                return PropertyEntity(StatProperty.SPD, event)
            case "cr":
                return PropertyEntity(StatProperty.CR, event)
            case "cd":
                return PropertyEntity(StatProperty.CD, event)
            case "res":
                return PropertyEntity(StatProperty.RES, event)
            case "acc":
                return PropertyEntity(StatProperty.ACC, event)
            case _:
                raise ValueError("Invalid stat property entered.")
    else:
        return PropertyEntity(event.sample(), event)

def get_prefix_stat_value(stars: RuneStars, prefix_stat_property: StatProperty, ask_input=False) -> ValueEntity:
    """Get the prefix stat value from user input or return a random value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default value.
    Returns:
        ValueEntity: The prefix stat value.
    Raises:
        ValueError: If the user input is not a valid prefix stat property.
    """
    value_event = rune_events.get_rune_prefix_stat_value_event(stars, prefix_stat_property)
    if not ask_input:
        return ValueEntity(value_event.sample(), value_event)
    answer = str(input("Enter a prefix stat value? (y/n): ")).strip().lower()
    if answer == 'y':
        value = int(input("Enter the prefix stat value: "))
        return ValueEntity(value, value_event)
    else:
        return ValueEntity(value_event.sample(), value_event)

def get_sub_stat(count: int):
    """Get the sub-stat property and value from user input.
    Args:
        count (int): The count of the sub-stat being entered (1, 2, etc.).
    Returns:
        tuple[StatProperty, int]: A tuple containing the sub-stat property and value.
    Raises:
        ValueError: If the user input is not a valid sub-stat property.
    """
    prop_input = str(input(f"Enter property for sub-stat {count} (ATK+/HP+/DEF+, ATK%/HP%/DEF%, SPD, CR, CD, RES, ACC):")).strip().lower()
    match prop_input:
        case "atk+":
            prop_input = StatProperty.ATK_ADD
        case "hp+":
            prop_input = StatProperty.HP_ADD
        case "def+":
            prop_input = StatProperty.DEF_ADD
        case "atk%":
            prop_input = StatProperty.ATK_MUL
        case "hp%":
            prop_input = StatProperty.HP_MUL
        case "def%":
            prop_input = StatProperty.DEF_MUL
        case "spd":
            prop_input = StatProperty.SPD
        case "cr":
            prop_input = StatProperty.CR
        case "cd":
            prop_input = StatProperty.CD
        case "res":
            prop_input = StatProperty.RES
        case "acc":
            prop_input = StatProperty.ACC
        case _:
            raise ValueError("Invalid main stat property entered.")
    
    value_input = int(input("Enter the sub-stat value: "))
    return prop_input, value_input

def get_sub_stats(grade: Grade, ask_input=False) -> tuple[list[StatProperty], list[int]]:
    """Get the sub-stat properties and values based on the rune grade.
    Args:
        grade (Grade): The rune grade for which to get the sub-stat properties and values.
        ask_input (bool): If True, prompt the user for input. If False, return default values.
    Returns:
        tuple[list[StatProperty], list[int]]: A tuple containing lists of sub-stat properties and values.
    Raises:
        ValueError: If the user input is not a valid rune grade.
    """
    if not ask_input:
        return [], []
    match grade:
        case Grade.NORMAL:
            num_input = 0
        case Grade.MAGIC:
            num_input = 1
        case Grade.RARE:
            num_input = 2
        case Grade.HERO:
            num_input = 3
        case Grade.LEGEND:
            num_input = 4
        case _:
            raise ValueError("Invalid rune grade entered.")

    sub_stat_properties = []
    sub_stat_values = []

    for i in range(num_input):
        prop, value = get_sub_stat(i+1)
        sub_stat_properties.append(prop)
        sub_stat_values.append(value)

    return sub_stat_properties, sub_stat_values
