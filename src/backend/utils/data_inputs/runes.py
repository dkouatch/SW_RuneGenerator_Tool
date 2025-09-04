import src.backend.utils.events.runes as rune_events

from src.backend.utils.models.enums.runes import RuneSlot, RuneStars, RuneSet
from src.backend.utils.models.enums.general import Grade
from src.backend.utils.models.enums.stats import StatProperty
from src.backend.utils.models.types.entities import *
from src.backend.utils.models.types.events import *

# General Form of Functions
# 1. Create the event object representing all possible outcomes conditioned on previous choices.
# 2. If asking for user input is disabled, return a random sample from the event and fix it as an entity object.
# 3. If asking for user input is enabled, ask the user if they want to enter their own input.
# 3a. If they deny, execute step (2)
# 3b. Otherwise, prompt the user for input and validate it against the event.
# 4. Ask the user if they want to fix the choice.
# 4a. If so, fix it. If fixing the part of the outcomes that contain the user's choice.
# 5. Create the entity object containing the final outcome, event object dependent on fixed user choices, and 
#    event object independent of user choices.

def get_rune_slot(ask_input=False, default: Optional[RuneSlot] = None) -> RuneSlotEntity:
    """Get the rune slot from user input or return a default or random value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default or random value.
        default (RuneSlot, optional): Returned if ask_input is False
    Returns:
        RuneSlotEntity: The rune slot selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune slot."""
    event = PropertyEvent([
        RuneSlot.ONE, RuneSlot.TWO, RuneSlot.THREE,
        RuneSlot.FOUR, RuneSlot.FIVE, RuneSlot.SIX])
    if not ask_input:
        entity = RuneSlotEntity(default if default is not None else event.sample(), event)
        entity.fix()  # No fixed event provided because there is only one possible outcome
        return entity
    else:
        slot_input = int(input("Enter the rune slot (1-6): "))
        match slot_input:
            case 1:
                entity = RuneSlotEntity(RuneSlot.ONE, event)
            case 2:
                entity = RuneSlotEntity(RuneSlot.TWO, event)
            case 3:
                entity = RuneSlotEntity(RuneSlot.THREE, event)
            case 4:
                entity = RuneSlotEntity(RuneSlot.FOUR, event)
            case 5:
                entity = RuneSlotEntity(RuneSlot.FIVE, event)
            case 6:
                entity = RuneSlotEntity(RuneSlot.SIX, event)
            case _:
                raise ValueError("Invalid rune slot entered.")
        fix_input = str(input("Fix this slot? (y/n): ")).strip().lower()
        if fix_input == 'y':
            entity.fix()
        return entity

def get_rune_stars(ask_input=False, default: Optional[RuneStars] = None) -> RuneStarsEntity:
    """Get the rune star grade from user input or return a default or random value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default or random value.
        default (RuneStars, optional): Returned if ask_input is False
    Returns:
        RuneStarsEntity: The rune star grade selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune star grade.
    """
    event = RuneStarsEvent([
        RuneStars.ONE, RuneStars.TWO, RuneStars.THREE,
        RuneStars.FOUR, RuneStars.FIVE, RuneStars.SIX])
    if not ask_input:
        entity = RuneStarsEntity(default if default is not None else event.sample(), event)
        entity.fix()  # No fixed event provided because there is only one possible outcome
        return entity
    else:
        star_input = int(input("Enter the rune star grade (1-6): "))
        match star_input:
            case 1:
                entity = RuneStarsEntity(RuneStars.ONE, event)
            case 2:
                entity = RuneStarsEntity(RuneStars.TWO, event)
            case 3:
                entity = RuneStarsEntity(RuneStars.THREE, event)
            case 4:
                entity = RuneStarsEntity(RuneStars.FOUR, event)
            case 5:
                entity = RuneStarsEntity(RuneStars.FIVE, event)
            case 6:
                entity = RuneStarsEntity(RuneStars.SIX, event)
            case _:
                raise ValueError("Invalid rune slot entered.")
        fix_input = str(input("Fix this star grade? (y/n): ")).strip().lower()
        if fix_input == 'y':
            entity.fix()
        return entity

def get_rune_set(ask_input=False, default: Optional[RuneSet] = None) -> RuneSetEntity:
    """Get the rune type from user input or return a default or random value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default or random value.
        default (RuneSet, optional): Returned if ask_input is False
    Returns:
        RuneSetEntity: The rune type selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune type.
    """
    event = RuneSetEvent([
        RuneSet.ENERGY, RuneSet.GUARD, RuneSet.SWIFT,  RuneSet.FOCUS,
        RuneSet.ENDURE, RuneSet.FATAL, RuneSet.BLADE, RuneSet.RAGE,
        RuneSet.VIOLENT, RuneSet.WILL, RuneSet.NEMESIS, RuneSet.DESPAIR,
        RuneSet.REVENGE, RuneSet.DESTROY, RuneSet.SHIELD, RuneSet.VAMPIRE,
        RuneSet.SEAL, RuneSet.INTANGIBLE, RuneSet.FIGHT, RuneSet.DETERMINATION,
        RuneSet.ENHANCE, RuneSet.ACCURACY, RuneSet.TOLERANCE])
    if not ask_input:
        entity = RuneSetEntity(default if default is not None else event.sample(), event)
        entity.fix() # No fixed event provided because there is only one possible outcome
        return entity
    else:
        type_input = str(input("Enter the rune type (Violent, Swift, Despair, etc): ")).strip().lower()
        match type_input:
            case "violent":
                entity = RuneSetEntity(RuneSet.VIOLENT, event)
            case "swift":
                entity = RuneSetEntity(RuneSet.SWIFT, event)
            case "despair":
                entity = RuneSetEntity(RuneSet.DESPAIR, event)
            case "energy":
                entity = RuneSetEntity(RuneSet.ENERGY, event)
            case "fatal":
                entity = RuneSetEntity(RuneSet.FATAL, event)
            case "blade":
                entity = RuneSetEntity(RuneSet.BLADE, event)
            case "rage":
                entity = RuneSetEntity(RuneSet.RAGE, event)
            case "will":
                entity = RuneSetEntity(RuneSet.WILL, event)
            case "nemesis":
                entity = RuneSetEntity(RuneSet.NEMESIS, event)
            case "vampire":
                entity = RuneSetEntity(RuneSet.VAMPIRE, event)
            case "shield":
                entity = RuneSetEntity(RuneSet.SHIELD, event)
            case "revenge":
                entity = RuneSetEntity(RuneSet.REVENGE, event)
            case "fight":
                entity = RuneSetEntity(RuneSet.FIGHT, event)
            case "determination":
                entity = RuneSetEntity(RuneSet.DETERMINATION, event)
            case "enhance":
                entity = RuneSetEntity(RuneSet.ENHANCE, event)
            case "accuracy":
                entity = RuneSetEntity(RuneSet.ACCURACY, event)
            case "tolerance":
                entity = RuneSetEntity(RuneSet.TOLERANCE, event)
            case "guard":
                entity = RuneSetEntity(RuneSet.GUARD, event)
            case "destroy":
                entity = RuneSetEntity(RuneSet.DESTROY, event)
            case "endure":
                entity = RuneSetEntity(RuneSet.ENDURE, event)
            case "focus":
                entity = RuneSetEntity(RuneSet.FOCUS, event)
            case "intangible":
                entity = RuneSetEntity(RuneSet.INTANGIBLE, event)
            case "seal":
                entity = RuneSetEntity(RuneSet.SEAL, event)
            case _:
                raise ValueError("Invalid rune type entered.")
        fix_input = str(input("Fix this rune type? (y/n): ")).strip().lower()
        if fix_input == 'y':
            entity.fix()
        return entity
            

def get_rune_default_grade(ask_input=False, default: Optional[Grade] = None) -> GradeEntity:
    """Get the rune grade from user input or return a default or random value.
    Args:
        ask_input (bool): If True, prompt the user for input. If False, return a default or random value.
        default (Grade, optional): Returned if ask_input is False
    Returns:
        GradeEntity: The rune grade selected by the user or a default value.
    Raises:
        ValueError: If the user input is not a valid rune grade.
    """
    event = GradeEvent([
        Grade.NORMAL, Grade.MAGIC, Grade.RARE,
        Grade.HERO, Grade.LEGEND])
    if not ask_input:
        entity = GradeEntity(default if default is not None else event.sample(), event)
        entity.fix()
        return entity
    else:
        grade_input = str(input("Enter the rune grade (Normal, Magic, Rare, Hero, Legend): ")).strip().lower()
        match grade_input:
            case "normal":
                entity = GradeEntity(Grade.NORMAL, event)
            case "magic":
                entity = GradeEntity(Grade.MAGIC, event)
            case "rare":
                entity = GradeEntity(Grade.RARE, event)
            case "hero":
                entity = GradeEntity(Grade.HERO, event)
            case "legend":
                entity = GradeEntity(Grade.LEGEND, event)
            case _:
                raise ValueError("Invalid rune grade entered.")
        fix_input = str(input("Fix this rune grade? (y/n): ")).strip().lower()
        if fix_input == 'y':
            entity.fix()
        return entity

def get_rune_stage(grade: Grade) -> ValueEntity:
    """Get stage of rune based on its grade.
    Args:
        grade (Grade): rune grade
    Returns:
        ValueEntity: rune stage (0-12)
    Raises:
        ValueError: invalid rune grade
    """
    # TODO: Make this customizable
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

def get_main_property(
        slot: RuneSlot,
        ask_input=False,
        default: Optional[StatProperty] = None) -> PropertyEntity:
    """Get the main stat property for a rune slot from user input or return a default or random property.
    Args:
        slot (RuneSlot): The rune slot for which to get the main stat property.
        ask_input (bool): If True, prompt the user for input. If False, return None.
        default (StatProperty, optional): Returned if ask_input is False
    Returns:
        PropertyEntity: The main stat property for the rune slot.
    Raises:
        ValueError: If the user input is not a valid main stat property.
    """
    event = rune_events.get_rune_main_stat_property_event(slot)
    if not ask_input:
        entity = PropertyEntity(default if default is not None else event.sample(), event)
        entity.fix()
        return entity
    else:
        answer = str(input("Enter a main stat property? (y/n): ")).strip().lower()
        if answer == 'y':
            stat_input = str(input("Enter the property (ATK+/HP+/DEF+, ATK%/HP%/DEF%, SPD, CR, CD, RES, ACC): ")).strip().lower()
            match stat_input:
                case "atk+":
                    entity = PropertyEntity(StatProperty.ATK_ADD, event)
                case "hp+":
                    entity = PropertyEntity(StatProperty.HP_ADD, event)
                case "def+":
                    entity = PropertyEntity(StatProperty.DEF_ADD, event)
                case "atk%":
                    entity = PropertyEntity(StatProperty.ATK_MUL, event)
                case "hp%":
                    entity = PropertyEntity(StatProperty.HP_MUL, event)
                case "def%":
                    entity = PropertyEntity(StatProperty.DEF_MUL, event)
                case "spd":
                    entity = PropertyEntity(StatProperty.SPD, event)
                case "cr":
                    entity = PropertyEntity(StatProperty.CR, event)
                case "cd":
                    entity = PropertyEntity(StatProperty.CD, event)
                case "res":
                    entity = PropertyEntity(StatProperty.RES, event)
                case "acc":
                    entity = PropertyEntity(StatProperty.ACC, event)
                case _:
                    entity = ValueError("Invalid main stat property entered.")
            fix_input = str(input("Fix this main stat property? (y/n): ")).strip().lower()
            if fix_input == 'y':
                entity.fix()
            return entity
        else:
            entity = PropertyEntity(event.sample(), event)
            entity.fix()
            return entity

def get_main_value(stars: RuneStars, stage: int, main_property: StatProperty) -> ValueEntity:
    """Get the main stat value from user input or return a default or random value.
    Args:
        stars (RuneStars): The star rating of the rune (1-6).
        stage (int): The current upgrade stage of the rune (0-12).
        main_property (StatProperty): The main stat property of the rune.
    Returns:
        ValueEntity: The main stat value.
    """
    # NOTE: Main values are deterministic and not probabilistic
    event = rune_events.get_rune_main_stat_value_event(stars, stage, main_property)
    return ValueEntity(event.sample(), event)

def get_prefix_property(
        slot: RuneSlot,
        main_property: StatProperty,
        ask_input=False,
        default: Optional[StatProperty] = None) -> PropertyEntity:
    """Get the prefix stat property and value from user input or return a default or random value.
    Args:
        slot (RuneSlot): The rune slot
        main_property (StatProperty): The rune's main property
        ask_input (bool): If True, prompt the user for input. If False, return a default or random value.
        default (StatProperty, optional): Returned if ask_input is False
    Returns:
        PropertyEntity: The prefix stat property
    Raises:
        ValueError: If the user input is not a valid prefix stat property.
    """
    event = rune_events.get_rune_prefix_stat_property_event(slot, main_property)
    if not ask_input:
        entity = PropertyEntity(default if default is not None else event.sample(), event)
        entity.fix()
        return entity
    else:
        answer = str(input("Enter a prefix stat property? (y/n): ")).strip().lower()
        if answer == 'y':
            prop_input = str(input("Enter the prefix stat property (ATK+/HP+/DEF+, ATK%/HP%/DEF%, SPD, CR, CD, RES, ACC): ")).strip().lower()
            match prop_input:
                case "atk+":
                    entity = PropertyEntity(StatProperty.ATK_ADD, event)
                case "hp+":
                    entity = PropertyEntity(StatProperty.HP_ADD, event)
                case "def+":
                    entity = PropertyEntity(StatProperty.DEF_ADD, event)
                case "atk%":
                    entity = PropertyEntity(StatProperty.ATK_MUL, event)
                case "hp%":
                    entity = PropertyEntity(StatProperty.HP_MUL, event)
                case "def%":
                    entity = PropertyEntity(StatProperty.DEF_MUL, event)
                case "spd":
                    entity = PropertyEntity(StatProperty.SPD, event)
                case "cr":
                    entity = PropertyEntity(StatProperty.CR, event)
                case "cd":
                    entity = PropertyEntity(StatProperty.CD, event)
                case "res":
                    entity = PropertyEntity(StatProperty.RES, event)
                case "acc":
                    entity = PropertyEntity(StatProperty.ACC, event)
                case _:
                    raise ValueError("Invalid stat property entered.")
            fix_input = str(input("Fix this prefix stat property? (y/n): ")).strip().lower()
            if fix_input == 'y':
                entity.fix()
            return entity
        else:
            return PropertyEntity(event.sample(), event)

def get_prefix_value(
        stars: RuneStars,
        prefix_property: StatProperty,
        ask_input=False,
        default: Optional[int] = None) -> ValueEntity:
    """Get the prefix stat value from user input or return a random value.
    Args:
        stars (RuneStars): The rune star grade
        prefix_property (StatProperty): The rune prefix property
        ask_input (bool): If True, prompt the user for input. If False, return a default or random value.
        default (int, optional): Returned if ask_input is False
    Returns:
        ValueEntity: The prefix stat value.
    Raises:
        ValueError: If the user input is not a valid prefix stat property.
    """
    if prefix_property == StatProperty.NO_PROPERTY:
        return ValueEntity(None)
    value_event = rune_events.get_rune_prefix_stat_value_event(stars, prefix_property)
    if not ask_input:
        entity = ValueEntity(default if default is not None else value_event.sample(), value_event)
        entity.fix()
        return entity
    else:
        answer = str(input("Enter a prefix stat value? (y/n): ")).strip().lower()
        if answer == 'y':
            value = int(input("Enter the prefix stat value: "))
            entity = ValueEntity(value, value_event)
            fix_input = str(input("Fix this prefix stat value? (y/n): ")).strip().lower()
            if fix_input == 'y':
                entity.fix()
            return entity
        else:
            return ValueEntity(value_event.sample(), value_event)

def get_sub_property(exclude_sub_properties: list[StatProperty], count: int) -> tuple[StatProperty, bool]:
    """Get the sub-stat property from user input.
    Args:
        exclude_sub_properties (list[StatProperty]): list of sub properties already selected by user
        count (int): The count of the sub-stat being entered (1, 2, etc.).
    Returns:
        PropertyEntity: the sub-stat property.
    Raises:
        ValueError: If the user input is not a valid sub-stat property or has already been selected
    """
    prop_input = str(input(f"Enter property for sub-stat {count} (ATK+/HP+/DEF+, ATK%/HP%/DEF%, SPD, CR, CD, RES, ACC):")).strip().lower()
    match prop_input:
        case "atk+":
            prop = StatProperty.ATK_ADD
        case "hp+":
            prop = StatProperty.HP_ADD
        case "def+":
            prop = StatProperty.DEF_ADD
        case "atk%":
            prop = StatProperty.ATK_MUL
        case "hp%":
            prop = StatProperty.HP_MUL
        case "def%":
            prop = StatProperty.DEF_MUL
        case "spd":
            prop = StatProperty.SPD
        case "cr":
            prop = StatProperty.CR
        case "cd":
            prop = StatProperty.CD
        case "res":
            prop = StatProperty.RES
        case "acc":
            prop = StatProperty.ACC
        case _:
            raise ValueError("Invalid main stat property entered.")
    
    if prop in exclude_sub_properties:
        raise ValueError(f"Chosen property {prop} has already been previously selected (see {exclude_sub_properties})")
    
    fix_input = str(input(f"Fix this choice of sub-stat property {prop}? (y/n): ")).strip().lower()
    return prop, fix_input == 'y'

def get_innate_sub_properties(
        slot: RuneSlot,
        grade: Grade,
        main_property: StatProperty,
        prefix_property: StatProperty,
        ask_input=False,
        default: Optional[Iterable[StatProperty]] = None) -> SubPropertyEntity:
    """Get the sub-stat properties and values based on the rune grade.
    Args:
        slot (RuneSlot): The slot of the rune (1-6).
        grade (Grade): The rune grade for which to get the sub-stat properties and values.
        main_property (StatProperty): The main stat property of the rune.
        prefix_property (StatProperty): The prefix stat property of the rune.
        innate_sub_properties (list[StatProperty], optional): List of innate sub-stat properties. Defaults to [].
        ask_input (bool): If True, prompt the user for input. If False, return default or random values.
        default (Iterable[StatProperty], optional): Returned if ask_input is False
    Returns:
        SubPropertyEntity: A tuple containing lists of sub-stat properties.
    Raises:
        ValueError: If the user input is not a valid rune grade or invalid number of sub properties.
    """
    match grade:
        case Grade.NORMAL:
            num_sub_props = 0
        case Grade.MAGIC:
            num_sub_props = 1
        case Grade.RARE:
            num_sub_props = 2
        case Grade.HERO:
            num_sub_props = 3
        case Grade.LEGEND:
            num_sub_props = 4
        case _:
            raise ValueError("Invalid rune grade entered.")
    
    if num_sub_props == 0:
        return SubPropertyEntity(())
    
    # Event representing all possible selections of sub properties
    unfixed_props_event = rune_events.get_rune_sub_stat_properties_event(
        slot, main_property, prefix_property,
        num_sub_props=num_sub_props)
    unfixed_props_event = unfixed_props_event.sorted()
    
    if not ask_input:
        entity = SubPropertyEntity(tuple(sorted(default)) if default is not None else unfixed_props_event.sample(), unfixed_props_event)
        entity.fix()
        return entity
    else:
        user_selections = {}
        count = int(input(f"How many innate sub stats do you want to manually enter? (max of {num_sub_props}): "))
        if count < 0 or count > num_sub_props:
            raise ValueError(f"Invalid number of sub stats entered: {count}")

        for i in range(count):  # Get each user requested sub property
            prop, fix = get_sub_property(list(user_selections.keys()), i+1)
            user_selections[prop] = fix
        manual_sub_properties = tuple(user_selections.keys())
        if len(manual_sub_properties) != len(set(manual_sub_properties)):
            raise ValueError(f"Duplicate sub property entries: {manual_sub_properties}")
        
        fixed_sub_props = {prop for prop, is_fixed in user_selections.items() if is_fixed} 
        if len(fixed_sub_props) == 0:     
            fixed_props_event = None 
        else:
            fixed_props_event = unfixed_props_event.filter(
            lambda props: fixed_sub_props.issubset(set(props))
        )

        # Still have random sub_properties left to generate
        if num_sub_props - count > 0:
            random_sub_properties = rune_events.get_rune_sub_stat_properties_event(
                slot, main_property, prefix_property, exclude_sub_properties=manual_sub_properties
            ).sample(n=num_sub_props-count, replace=False)
            if not isinstance(random_sub_properties, tuple):
                random_sub_properties = (random_sub_properties,)
        else:
            random_sub_properties = ()

        sub_properties = tuple(sorted(manual_sub_properties + random_sub_properties))
        entity = SubPropertyEntity(sub_properties, unfixed_props_event, fixed_props_event)
        entity.fix()
        return entity

def get_additional_sub_properties(
        slot: RuneSlot,
        grade: Grade,
        main_property: StatProperty,
        prefix_property: StatProperty,
        innate_sub_properties: list[StatProperty],
        ask_input=False,
        default: Optional[Iterable[StatProperty]] = None) -> SubPropertyEntity:
    """Get the sub-stat properties and values based on the rune grade.
    Args:
        slot (RuneSlot): The slot of the rune (1-6).
        grade (Grade): The rune grade for which to get the sub-stat properties and values.
        main_property (StatProperty): The main stat property of the rune.
        prefix_property (StatProperty): The prefix stat property of the rune.
        innate_sub_properties (list[StatProperty], optional): List of innate sub-stat properties. Defaults to [].
        ask_input (bool): If True, prompt the user for input. If False, return default or random values.
        default (Iterable[StatProperty], optional): Returned if ask_input is False
    Returns:
        SubPropertyEntity: A tuple containing lists of sub-stat properties.
    Raises:
        ValueError: If the user input is not a valid rune grade or invalid number of sub properties.
    """
    match grade:
        case Grade.NORMAL:
            num_sub_props = 4
        case Grade.MAGIC:
            num_sub_props = 3
        case Grade.RARE:
            num_sub_props = 2
        case Grade.HERO:
            num_sub_props = 1
        case Grade.LEGEND:
            num_sub_props = 0
        case _:
            raise ValueError("Invalid rune grade entered.")
    
    if num_sub_props == 0:
        return SubPropertyEntity(())
    
    # Event representing all possible selections of sub properties
    unfixed_props_event = rune_events.get_rune_sub_stat_properties_event(
        slot, main_property, prefix_property,
        num_sub_props=num_sub_props,
        exclude_sub_properties=innate_sub_properties)
    unfixed_props_event = unfixed_props_event.sorted()
    
    if not ask_input:
        entity = SubPropertyEntity(tuple(sorted(default)) if default is not None else unfixed_props_event.sample(), unfixed_props_event)
        entity.fix()
        return entity
    else:
        user_selections = {}
        count = int(input(f"How many additional sub stats do you want to manually enter? (max of {num_sub_props}): "))
        if count < 0 or count > num_sub_props:
            raise ValueError(f"Invalid number of sub stats entered: {count}")

        for i in range(count):  # Get each user requested sub property
            prop, fix = get_sub_property(list(user_selections.keys()), i+1)
            user_selections[prop] = fix
        manual_sub_properties = tuple(user_selections.keys())
        if len(manual_sub_properties) != len(set(manual_sub_properties)):
            raise ValueError(f"Duplicate sub property entries: {manual_sub_properties}")
        
        fixed_sub_props = {prop for prop, is_fixed in user_selections.items() if is_fixed}      
        if len(fixed_sub_props) == 0:     
            fixed_props_event = None 
        else:
            fixed_props_event = unfixed_props_event.filter(
            lambda props: fixed_sub_props.issubset(set(props))
        )

        # Still have random sub_properties left to generate
        if num_sub_props - count > 0:
            random_sub_properties = rune_events.get_rune_sub_stat_properties_event(
                slot, main_property, prefix_property, exclude_sub_properties=innate_sub_properties+manual_sub_properties
            ).sample(n=num_sub_props-count, replace=False)
            if not isinstance(random_sub_properties, tuple):
                random_sub_properties = (random_sub_properties,)
        else:
            random_sub_properties = ()

        sub_properties = tuple(sorted(manual_sub_properties + random_sub_properties))
        entity = SubPropertyEntity(sub_properties, unfixed_props_event, fixed_props_event)
        entity.fix()
        return entity

def get_innate_sub_upgrades(
        sub_properties: Optional[list[StatProperty]],
        ask_input: bool = False,
        default: Optional[dict[StatProperty, int]] = None
) -> list[ValueEntity]:
    """_summary_

    Args:
        sub_properties (list[StatProperty]): _description_
        ask_input (bool, optional): _description_. Defaults to False.
        default (Optional[list[int]], optional): _description_. Defaults to None.
    """
    if len(sub_properties) == 0:
        return UpgradeEntity(None)

    counter_event = rune_events.get_rune_sub_upgrades_event(sub_properties)
    if not ask_input:
        entity = UpgradeEntity(Upgrade({prop: upgrade for prop, upgrade in default.items() if upgrade != 0}) if default is not None else counter_event.sample(), counter_event)
        entity.fix()
        return entity
    else:
        num_available_upgrades = len(sub_properties)
        user_upgrades = Upgrade({prop: 0 for prop in sub_properties})  # Represent user-selected upgrades
        fixed_upgrades = Upgrade()  # Represent fixed user-selected upgrades
        for prop in sub_properties:
            if num_available_upgrades > 0:
                answer = str(input(f"Enter number of upgrades for sub property {prop}? (y/n) ")).strip().lower()
                if answer == 'y':
                    count = int(input(f"Enter number of upgrades for sub property {prop} (0-{num_available_upgrades})"))
                    if 0 <= count <= num_available_upgrades:
                        user_upgrades[prop] = count
                        fix_answer = str(input("Fix this selection? (y/n) ")).strip().lower()
                        if fix_answer == 'y':
                            fixed_upgrades[prop] = count
                        num_available_upgrades -= count
                    else:
                        raise ValueError(f"Invalid number of upgrades {count} requested for {prop}. Can only choose between 0 and {num_available_upgrades} inclusive.")
                    
        # TODO: More expressive relationship other than == (<, <=, etc.)
        if len(fixed_upgrades == 0):
            fixed_counter_event = None
        else:
            fixed_counter_event = counter_event.filter(
                lambda counter: all(
                    count == counter[upgrade]
                    for upgrade, count in fixed_upgrades))

        if num_available_upgrades > 0:  # Get remaining random upgrades
            random_upgrades = Upgrade(PropertyEvent(sub_properties).sample(num_available_upgrades, replace=False))
        else:
            random_upgrades = Upgrade()
        all_upgrades = user_upgrades + random_upgrades
        return UpgradeEntity(all_upgrades, counter_event, fixed_counter_event)

def get_sub_value(
        stars: RuneStars,
        sub_property: StatProperty,
        num_upgrades: int,
        ask_input: bool = False,
        default: Optional[int] = None
) -> ValueEntity:
    value_event = rune_events.get_rune_sub_stat_value_event(stars, sub_property, num_upgrades)
    if not ask_input:
        entity = ValueEntity(default if default is not None else value_event.sample(), value_event)
        entity.fix()
        return entity
    else:
        answer = str(input(f"Enter value for sub property {sub_property}? (y/n) ")).strip().lower()
        if answer == 'y':
            value = int(input(f"Enter value for sub property {sub_property} (+{num_upgrades}) "))
            fix_answer = str(input("Fix this selection? (y/n) ")).strip().lower()
            if fix_answer == 'y':
                return ValueEntity(value, value_event, ValueEvent([value]))
            else:
                return ValueEntity(value, value_event)
        else:
            return ValueEntity(value_event.sample(), value_event)

def get_sub_values(
        stars: RuneStars,
        sub_properties: Iterable[StatProperty],
        upgrades: Optional[Upgrade],
        ask_input: bool = False,
        default: Optional[dict[StatProperty, int]] = None
) -> list[ValueEntity]:
    if upgrades is None:
        return []
    else:
        print(upgrades)
        entities = [get_sub_value(stars, sub_property, upgrades[sub_property], ask_input, default[sub_property] if default is not None else None)
                    for sub_property in sub_properties]
        return entities



