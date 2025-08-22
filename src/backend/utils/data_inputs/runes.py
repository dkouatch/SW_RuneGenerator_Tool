from typing import Optional

from src.backend.utils.models.enums.runes import RuneSlot, RuneStars, RuneSet
from src.backend.utils.models.enums.general import Grade
from src.backend.utils.models.enums.stats import StatProperty

def get_rune_slot(ask_input=True) -> RuneSlot:
    """Get the rune slot from user input or return a default value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default value.
    Returns:
        RuneSlot: The rune slot selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune slot."""
    if not ask_input:
        return RuneSlot.ONE
    slot_input = int(input("Enter the rune slot (1-6): "))
    match slot_input:
        case 1:
            return RuneSlot.ONE
        case 2:
            return RuneSlot.TWO
        case 3:
            return RuneSlot.THREE
        case 4:
            return RuneSlot.FOUR
        case 5:
            return RuneSlot.FIVE
        case 6:
            return RuneSlot.SIX
        case _:
            raise ValueError("Invalid rune slot entered.")

def get_rune_stars(ask_input=True) -> RuneStars:
    """Get the rune star grade from user input or return a default value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default value.
    Returns:
        RuneStars: The rune star grade selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune star grade.
    """
    if not ask_input:
        return RuneStars.ONE
    star_input = int(input("Enter the rune star grade (1-6): "))
    match star_input:
        case 1:
            return RuneStars.ONE
        case 2:
            return RuneStars.TWO
        case 3:
            return RuneStars.THREE
        case 4:
            return RuneStars.FOUR
        case 5:
            return RuneStars.FIVE
        case 6:
            return RuneStars.SIX
        case _:
            raise ValueError("Invalid rune slot entered.")

def get_rune_type(ask_input=True) -> RuneSet:
    """Get the rune type from user input or return a default value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default value.
    Returns:
        RuneSet: The rune type selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune type.
    """
    if not ask_input:
        return RuneSet.Energy
    type_input = str(input("Enter the rune type (Violent, Swift, Despair, etc): ")).strip().lower()
    match type_input:
        case "violent":
            return RuneSet.Violent
        case "swift":
            return RuneSet.Swift
        case "despair":
            return RuneSet.Despair
        case "energy":
            return RuneSet.Energy
        case "fatal":
            return RuneSet.Fatal
        case "blade":
            return RuneSet.Blade
        case "rage":
            return RuneSet.Rage
        case "will":
            return RuneSet.Will
        case "nemesis":
            return RuneSet.Nemesis
        case "vampire":
            return RuneSet.Vampire
        case "shield":
            return RuneSet.Shield
        case "revenge":
            return RuneSet.Revenge
        case "fight":
            return RuneSet.Fight
        case "determination":
            return RuneSet.Determination
        case "enhance":
            return RuneSet.Enhance
        case "accuracy":
            return RuneSet.Accuracy
        case "tolerance":
            return RuneSet.Tolerance
        case _:
            raise ValueError("Invalid rune type entered.")

def get_rune_grade(ask_input=True) -> Grade:
    """Get the rune grade from user input or return a default value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default value.
    Returns:
        Grade: The rune grade selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune grade.
    """
    if not ask_input:
        return Grade.HERO
    grade_input = str(input("Enter the rune grade (Normal, Magic, Rare, Hero, Legend): ")).strip().lower()
    match grade_input:
        case "normal":
            return Grade.NORMAL
        case "magic":
            return Grade.MAGIC
        case "rare":
            return Grade.RARE
        case "hero":
            return Grade.HERO
        case "legend":
            return Grade.LEGEND
        case _:
            raise ValueError("Invalid rune grade entered.")

def get_main_stat(slot: RuneSlot, ask_input=True) -> Optional[StatProperty]:
    """Get the main stat property for a rune slot from user input or return a default value or None.
    Args:
        slot (RuneSlot): The rune slot for which to get the main stat property.
        ask_input (bool): If True, prompt the user for input. If False, return None.
    Returns:
        Optional[StatProperty]: The main stat property for the rune slot or None if not applicable.
    Raises:
        ValueError: If the user input is not a valid main stat property.
    """
    if slot in [RuneSlot.ONE, RuneSlot.THREE, RuneSlot.FIVE]:
        return None
    else:
        if not ask_input:
            return StatProperty.HP_MUL
        answer = str(input("Enter a main stat property? (y/n): ")).strip().lower()
        if answer == 'y':
            stat_input = str(input("Enter the property (ATK+/HP+/DEF+, ATK%/HP%/DEF%, SPD, CR, CD, RES, ACC): ")).strip().lower()
            match stat_input:
                case "atk+":
                    return StatProperty.ATK_ADD
                case "hp+":
                    return StatProperty.HP_ADD
                case "def+":
                    return StatProperty.DEF_ADD
                case "atk%":
                    return StatProperty.ATK_MUL
                case "hp%":
                    return StatProperty.HP_MUL
                case "def%":
                    return StatProperty.DEF_MUL
                case "spd":
                    return StatProperty.SPD
                case "cr":
                    return StatProperty.CR
                case "cd":
                    return StatProperty.CD
                case "res":
                    return StatProperty.RES
                case "acc":
                    return StatProperty.ACC
                case _:
                    raise ValueError("Invalid main stat property entered.")
        else:
            return None

def get_prefix_stat(ask_input=True) -> tuple[Optional[StatProperty], Optional[int]]:
    """Get the prefix stat property and value from user input or return a default value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default value.
    Returns:
        tuple[Optional[StatProperty], Optional[int]]: A tuple containing the prefix stat property and value.
    Raises:
        ValueError: If the user input is not a valid prefix stat property.
    """
    if not ask_input:
        return StatProperty.ACC, 7
    answer = str(input("Enter a prefix stat property? (y/n): ")).strip().lower()
    if answer == 'y':
        prop_input = str(input("Enter the prefix stat property (ATK+/HP+/DEF+, ATK%/HP%/DEF%, SPD, CR, CD, RES, ACC): ")).strip().lower()
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
                raise ValueError("Invalid stat property entered.")
        
        answer = str(input("Enter a prefix stat value? (y/n): ")).strip().lower()
        if answer == 'y':
            value_input = int(input("Enter the prefix stat value: "))
        else:
            value_input = None
        return prop_input, value_input
    else:
        prop_input, value_input = (None, None)
    return prop_input, value_input

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

def get_sub_stats(grade: Grade, ask_input=True) -> tuple[list[StatProperty], list[int]]:
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
