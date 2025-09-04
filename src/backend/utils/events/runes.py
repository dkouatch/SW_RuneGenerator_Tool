import operator
from typing import Optional

from src.backend.utils.models.enums.runes import RuneStars, RuneSlot
from src.backend.utils.models.enums.stats import StatProperty
from src.backend.utils.models.types.events import *

# VALUES
def get_rune_main_stat_value_event(
        stars: RuneStars,
        stage: int,
        main_stat_property: StatProperty) -> ValueEvent:
    """
    Returns the event for value of a rune's main stat based on its property, stars, and stage

    Args:
        stars (RuneStars): number of stars of rune (1-6)
        main_stat_property (StatProperty): rune main property
    
    Returns:
        ValueEvent: event object for values
    
    Raises:
        ValueError: invalid star, main_stat_property, or stage value
    """
    # Implementation to retrieve the range for the main stat
    match stars:
        case RuneStars.ONE:
            match main_stat_property:
                case StatProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            40, 85, 150,
                            195, 240, 285,
                            330, 375, 420,
                            465, 510, 555,
                            600, 645, 690,
                            804
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            3, 6, 9,
                            12, 15, 18,
                            21, 24, 27,
                            30, 33, 36,
                            39, 42, 45,
                            54
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case (StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL |
                      StatProperty.SPD | StatProperty.RES | StatProperty.ACC | StatProperty.CR):
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            1, 2, 3,
                            4, 5, 6,
                            7, 8, 9,
                            10, 11, 12,
                            13, 14, 15,
                            18
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.CD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            2, 3, 4,
                            5, 6, 7,
                            8, 9, 10,
                            11, 12, 13,
                            14, 15, 16,
                            19
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_stat_property}")
        case RuneStars.TWO:
            match main_stat_property:
                case StatProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            70, 130, 190,
                            250, 310, 370,
                            430, 490, 550,
                            610, 670, 730,
                            790, 850, 910,
                            1092
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            5, 9, 13,
                            17, 21, 25,
                            29, 33, 37,
                            41, 45, 49,
                            53, 57, 61,
                            73
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case (StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL |
                      StatProperty.RES | StatProperty.ACC | StatProperty.CR | StatProperty.SPD):
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            2, 3, 4,
                            5, 6, 7,
                            8, 9, 10,
                            11, 12, 13,
                            14, 15, 16,
                            19
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.CD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            3, 5, 7,
                            9, 11, 13,
                            15, 17, 19,
                            21, 23, 25,
                            27, 29, 31,
                            37
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_stat_property}")
        case RuneStars.THREE:
            match main_stat_property:
                case StatProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            100, 175, 250,
                            325, 400, 475,
                            550, 625, 700,
                            775, 850, 925,
                            1000, 1075, 1150,
                            1380
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            7, 12, 17,
                            22, 27, 32,
                            37, 42, 47,
                            52, 57, 62,
                            67, 72, 77,
                            92
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case (StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL |
                      StatProperty.RES | StatProperty.RES):
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            4, 6, 8,
                            10, 12, 14,
                            16, 18, 20,
                            22, 24, 26,
                            28, 30, 32,
                            38
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.SPD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            3, 4, 6,
                            7, 8, 10,
                            11, 12, 14,
                            15, 16, 18,
                            19, 20, 22,
                            25
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.CR:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            3, 5, 7,
                            9, 11, 13,
                            15, 17, 19,
                            21, 23, 25,
                            27, 29, 31,
                            37
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.CD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            4, 6, 8,
                            11, 13, 15,
                            17, 20, 22,
                            24, 26, 29,
                            31, 33, 35,
                            43
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_stat_property}")
        case RuneStars.FOUR:
            match main_stat_property:
                case StatProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            160, 250, 340,
                            430, 520, 610,
                            700, 790, 880,
                            970, 1060, 1150,
                            1240, 1330, 1420,
                            1704
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            10, 16, 22,
                            28, 34, 40,
                            46, 52, 58,
                            64, 70, 76,
                            82, 88, 94,
                            112
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            5, 7, 9,
                            11, 14, 16,
                            18, 20, 22,
                            24, 26, 29,
                            31, 33, 35,
                            43
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.SPD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            4, 5, 7,
                            8, 10, 11,
                            13, 14, 16,
                            17, 19, 20,
                            22, 23, 25,
                            30
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.RES | StatProperty.ACC:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            6, 8, 10,
                            12, 15, 17,
                            19, 21, 23,
                            25, 27, 30,
                            32, 34, 36,
                            44
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.CR:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            4, 6, 8,
                            10, 13, 15,
                            17, 19, 21,
                            23, 25, 28,
                            30, 32, 34,
                            42
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.CD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            6, 9, 12,
                            15, 18, 21,
                            24, 27, 30,
                            33, 36, 39,
                            42, 45, 48,
                            54
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_stat_property}")
        case RuneStars.FIVE:
            match main_stat_property:
                case StatProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            270, 375, 480,
                            585, 690, 795,
                            900, 1005, 1110,
                            1215, 1320, 1425,
                            1530, 1635, 1740,
                            2088
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            15, 22, 29,
                            36, 43, 50,
                            57, 64, 71,
                            78, 85, 92,
                            99, 106, 113,
                            135
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            8, 10, 13,
                            15, 18, 20,
                            23, 25, 28,
                            30, 32, 35,
                            37, 40, 42,
                            51
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.SPD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            5, 7, 9,
                            11, 13, 15,
                            17, 19, 21,
                            23, 25, 27,
                            29, 31, 33,
                            39
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.RES | StatProperty.ACC:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            9, 11, 14,
                            16, 19, 21,
                            24, 26, 29,
                            31, 33, 36,
                            38, 41, 43,
                            51
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.CR:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            5, 7, 10,
                            12, 15, 17,
                            20, 22, 25,
                            27, 29, 32,
                            34, 37, 39,
                            47
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.CD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            8, 11, 15,
                            18, 21, 25,
                            28, 31, 35,
                            38, 41, 45,
                            48, 51, 55,
                            65
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_stat_property}")
        case RuneStars.SIX:
            match main_stat_property:
                case StatProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            360, 460, 600,
                            720, 840, 960,
                            1080, 1200, 1320,
                            1440, 1560, 1680,
                            1800, 1920, 2040,
                            2448,
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            22, 30, 38,
                            46, 54, 62,
                            70, 78, 86,
                            94, 102, 110,
                            118, 126, 134,
                            160
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            11, 14, 17,
                            20, 23, 26,
                            29, 32, 35,
                            38, 41, 44,
                            47, 50, 53,
                            63
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.SPD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            7, 9, 11,
                            13, 15, 17,
                            19, 21, 23,
                            25, 27, 29,
                            31, 33, 35,
                            42
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.RES | StatProperty.ACC:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            12, 15, 18,
                            21, 24, 27,
                            30, 33, 36,
                            39, 42, 45,
                            48, 51, 54,
                            64
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.CR:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            7, 10, 13,
                            16, 19, 22,
                            25, 28, 31,
                            34, 37, 40,
                            43, 46, 49,
                            58
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case StatProperty.CD:
                    if 0 <= stage and stage <= 15:
                        stat_values = [
                            11, 14, 17,
                            20, 23, 26,
                            29, 32, 35,
                            38, 41, 44,
                            47, 50, 53,
                            63
                        ]
                        return ValueEvent([stat_values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_stat_property}")
    

def get_rune_prefix_stat_value_event(
        stars: RuneStars,
        prefix_stat_property: StatProperty) -> ValueEvent:
    """
    Returns the event for a rune's prefix stat based on its stars and property

    Args:
        stars (RuneStars): Number of stars of rune (1-6)
        prefix_stat_property (StatProperty): Rune prefix property
    
    Returns:
        ValueEvent: event object for values
    
    Raises:
        ValueError: If the stars or prefix property are invalid
    """
    # Implementation to retrieve the range for the prefix stat
    match stars:
        case RuneStars.ONE:
            match prefix_stat_property:
                case StatProperty.NO_PROPERTY:
                    return ValueEvent([0])
                case StatProperty.HP_ADD:
                    return ValueEvent(range(15, 61))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    return ValueEvent(range(1, 5))
                case (StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL |
                      StatProperty.CR | StatProperty.CD | StatProperty.RES | StatProperty.ACC):
                    return ValueEvent(range(1, 3))
                case StatProperty.SPD:
                    return ValueEvent([1])
                case _:
                    raise ValueError(f"Unknown property: {prefix_stat_property}")
        case RuneStars.TWO:
            match prefix_stat_property:
                case StatProperty.NO_PROPERTY:
                    return ValueEvent([0])
                case StatProperty.HP_ADD:
                    return ValueEvent(range(30, 106))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    return ValueEvent(range(2, 6))
                case (StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL |
                      StatProperty.CR | StatProperty.CD | StatProperty.RES | StatProperty.ACC):
                    return ValueEvent(range(1, 4))
                case StatProperty.SPD:
                    return ValueEvent(range(1, 3))
                case _:
                    raise ValueError(f"Unknown property: {prefix_stat_property}")
        case RuneStars.THREE:
            match prefix_stat_property:
                case StatProperty.NO_PROPERTY:
                    return ValueEvent([0])
                case StatProperty.HP_ADD:
                    return ValueEvent(range(45, 166))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    return ValueEvent(range(3, 9))
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    return ValueEvent(range(2, 6))
                case StatProperty.SPD | StatProperty.CR:
                    return ValueEvent(range(1, 4))
                case StatProperty.RES | StatProperty.ACC | StatProperty.CD:
                    return ValueEvent(range(2, 5))

                case _:
                    raise ValueError(f"Unknown property: {prefix_stat_property}")
        case RuneStars.FOUR:
            match prefix_stat_property:
                case StatProperty.NO_PROPERTY:
                    return ValueEvent([0])
                case StatProperty.HP_ADD:
                    return ValueEvent(range(60, 226))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    return ValueEvent(range(4, 11))
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    return ValueEvent(range(3, 7))
                case StatProperty.SPD | StatProperty.CR:
                    return ValueEvent(range(2, 5))
                case StatProperty.RES | StatProperty.ACC | StatProperty.CD:
                    return ValueEvent(range(2, 6))
                case _:
                    raise ValueError(f"Unknown property: {prefix_stat_property}")
        case RuneStars.FIVE:
            match prefix_stat_property:
                case StatProperty.NO_PROPERTY:
                    return ValueEvent([0])
                case StatProperty.HP_ADD:
                    return ValueEvent(range(90, 301))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    return ValueEvent(range(8, 16))
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    return ValueEvent(range(4, 8))
                case StatProperty.SPD | StatProperty.CR | StatProperty.CD:
                    return ValueEvent(range(3, 6))
                case StatProperty.RES | StatProperty.ACC:
                    return ValueEvent(range(3, 8))
                case _:
                    raise ValueError(f"Unknown property: {prefix_stat_property}")
        case RuneStars.SIX:
            match prefix_stat_property:
                case StatProperty.NO_PROPERTY:
                    return ValueEvent([0])
                case StatProperty.HP_ADD:
                    return ValueEvent(range(135, 376))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    return ValueEvent(range(10, 21))
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    return ValueEvent(range(5, 9))
                case StatProperty.SPD | StatProperty.CR:
                    return ValueEvent(range(4, 7))
                case StatProperty.RES | StatProperty.ACC:
                    return ValueEvent(range(4, 9))
                case StatProperty.CD:
                    return ValueEvent(range(4, 8))
                case _:
                    raise ValueError(f"Unknown property: {prefix_stat_property}")
        case _:
            raise ValueError(f"Unknown stars: {stars}")

def get_rune_sub_stat_value_event(
        stars: RuneStars,
        sub_stat_property: StatProperty,
        num_upgrades: int = 0) -> ValueEvent:
    """
    Returns the event for a rune's substat based on its stars and property

    Args:
        stars (RuneStars): Number of stars of rune (1-6)
        sub_stat_property (StatProperty): Rune substat property
        num_upgrades (int, optional): Number of times the substat has been upgraded (0-4)
    
    Returns:
        ValueEvent: event object for values
    
    Raises:
        ValueError: If the stars or sub property are invalid
    """
    # Implementation to retrieve the range for the sub stat
    match stars:
        case RuneStars.ONE:
            match sub_stat_property:
                case StatProperty.NO_PROPERTY:
                    event = ValueEvent([0])
                case StatProperty.HP_ADD:
                    event = ValueEvent(range(15, 61))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    event = ValueEvent(range(1, 5))
                case (StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL |
                      StatProperty.CR | StatProperty.CD | StatProperty.RES | StatProperty.ACC):
                    event = ValueEvent(range(1, 3))
                case StatProperty.SPD:
                    event = ValueEvent([1])
                case _:
                    raise ValueError(f"Invalid property: {sub_stat_property}")
        case RuneStars.TWO:
            match sub_stat_property:
                case StatProperty.NO_PROPERTY:
                    event = ValueEvent([0])
                case StatProperty.HP_ADD:
                    event = ValueEvent(range(30, 106))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    event = ValueEvent(range(2, 6))
                case (StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL |
                      StatProperty.CR | StatProperty.CD | StatProperty.RES | StatProperty.ACC):
                    event = ValueEvent(range(1, 4))
                case StatProperty.SPD:
                    event = ValueEvent(range(1, 3))
                case _:
                    raise ValueError(f"Invalid property: {sub_stat_property}")
        case RuneStars.THREE:
            match sub_stat_property:
                case StatProperty.NO_PROPERTY:
                    event = ValueEvent([0])
                case StatProperty.HP_ADD:
                    event = ValueEvent(range(45, 166))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    event = ValueEvent(range(3, 9))
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    event = ValueEvent(range(2, 6))
                case StatProperty.SPD | StatProperty.CR:
                    event = ValueEvent(range(1, 4))
                case StatProperty.RES | StatProperty.ACC | StatProperty.CD:
                    event = ValueEvent(range(2, 5))

                case _:
                    raise ValueError(f"Invalid property: {sub_stat_property}")
        case RuneStars.FOUR:
            match sub_stat_property:
                case StatProperty.HP_ADD:
                    event = ValueEvent(range(60, 226))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    event = ValueEvent(range(4, 11))
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    event = ValueEvent(range(3, 7))
                case StatProperty.SPD | StatProperty.CR:
                    event = ValueEvent(range(2, 5))
                case StatProperty.RES | StatProperty.ACC | StatProperty.CD:
                    event = ValueEvent(range(2, 6))
                case _:
                    raise ValueError(f"Invalid property: {sub_stat_property}")
        case RuneStars.FIVE:
            match sub_stat_property:
                case StatProperty.HP_ADD:
                    event = ValueEvent(range(90, 301))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    event = ValueEvent(range(8, 16))
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    event = ValueEvent(range(4, 8))
                case StatProperty.SPD | StatProperty.CR | StatProperty.CD:
                    event = ValueEvent(range(3, 6))
                case StatProperty.RES | StatProperty.ACC:
                    event = ValueEvent(range(3, 8))
                case _:
                    raise ValueError(f"Invalid property: {sub_stat_property}")
        case RuneStars.SIX:
            match sub_stat_property:
                case StatProperty.NO_PROPERTY:
                    event = ValueEvent([0])
                case StatProperty.HP_ADD:
                    event = ValueEvent(range(135, 376))
                case StatProperty.ATK_ADD | StatProperty.DEF_ADD:
                    event = ValueEvent(range(10, 21))
                case StatProperty.HP_MUL | StatProperty.ATK_MUL | StatProperty.DEF_MUL:
                    event = ValueEvent(range(5, 9))
                case StatProperty.SPD | StatProperty.CR:
                    event = ValueEvent(range(4, 7))
                case StatProperty.RES | StatProperty.ACC:
                    event = ValueEvent(range(4, 9))
                case StatProperty.CD:
                    event = ValueEvent(range(4, 8))
                case _:
                    raise ValueError(f"Invalid property: {sub_stat_property}")
        case _:
            raise ValueError(f"Unknown stars: {stars}")
    if num_upgrades < 0 or num_upgrades > 4:
        raise ValueError(f"Invalid number of upgrades: {num_upgrades}")
    elif num_upgrades == 0:
        return event
    else:
        intersect_event = event.intersect_self(num_upgrades+1)
        return intersect_event.reduce(operator.add)


# PROPERTIES
def get_rune_main_stat_property_event(slot: RuneSlot) -> PropertyEvent:
    """
    Returns a valid main property for a rune based its slot

    Args:
        slot (RuneSlot): rune slot (1-6)
    
    Returns:
        PropertyEvent: event object for properties
    
    Raises:
        ValueError: incorrect slot
    """
    match slot:
        case RuneSlot.ONE:
            return PropertyEvent([StatProperty.ATK_ADD])
        case RuneSlot.TWO:
            return PropertyEvent([
                StatProperty.HP_MUL, StatProperty.ATK_MUL, StatProperty.DEF_MUL,
                StatProperty.HP_ADD, StatProperty.ATK_ADD, StatProperty.DEF_ADD,
                StatProperty.SPD
            ])
        case RuneSlot.THREE:
            return PropertyEvent([StatProperty.DEF_ADD])
        case RuneSlot.FOUR:
            return PropertyEvent([
                StatProperty.HP_MUL, StatProperty.ATK_MUL, StatProperty.DEF_MUL,
                StatProperty.HP_ADD, StatProperty.ATK_ADD, StatProperty.DEF_ADD,
                StatProperty.CR, StatProperty.CD
            ])
        case RuneSlot.FIVE:
            return PropertyEvent([StatProperty.HP_ADD])
        case RuneSlot.SIX:
            return PropertyEvent([
                StatProperty.HP_MUL, StatProperty.ATK_MUL, StatProperty.DEF_MUL,
                StatProperty.HP_ADD, StatProperty.ATK_ADD, StatProperty.DEF_ADD,
                StatProperty.RES, StatProperty.ACC
            ])
        case _:
            raise ValueError(f"Unknown rune slot: {slot}")

def get_rune_prefix_stat_property_event(
        slot: RuneSlot,
        main_stat_property: StatProperty) -> PropertyEvent:
    """
    Returns a valid prefix property for a rune based its main property and slot

    Args:
        slot (RuneSlot): rune slot (1-6)
        main_stat_property (StatProperty): rune main property
    
    Returns:
        PropertyEvent: event object for properties
    
    Raises:
        ValueError: invalid slot
    """
    props = [
        StatProperty.HP_ADD, StatProperty.HP_MUL,
        StatProperty.ATK_ADD, StatProperty.ATK_MUL,
        StatProperty.DEF_ADD, StatProperty.DEF_MUL,
        StatProperty.RES, StatProperty.ACC,
        StatProperty.CR, StatProperty.CD,
        StatProperty.SPD, StatProperty.NO_PROPERTY 
    ]
    event = PropertyEvent(props)
    match slot:
        case RuneSlot.ONE:
            event.remove([StatProperty.DEF_ADD, StatProperty.DEF_MUL, StatProperty.ATK_ADD])
        case RuneSlot.THREE:
            event.remove([StatProperty.ATK_ADD, StatProperty.ATK_MUL, StatProperty.DEF_ADD])
        case RuneSlot.FIVE:
            event.remove([StatProperty.HP_ADD])
        case RuneSlot.TWO | RuneSlot.FOUR | RuneSlot.SIX:
            event.remove([main_stat_property])
        case _:
            raise ValueError(f"Unknown rune slot: {slot}")
    event.rebalance(StatProperty.NO_PROPERTY, 0.9)
    return event

def get_rune_sub_stat_properties_event(
        slot: RuneSlot,
        main_stat_property: StatProperty,
        prefix_property: StatProperty,
        num_sub_props: Optional[int] = None,
        exclude_sub_properties: list[StatProperty] = []) -> PropertyEvent | SubPropertyEvent:
    """
    Returns a valid sub property for a rune based its main and prefix properties and slot

    Args:
        slot (RuneSlot): rune slot (1-6)
        main_stat_property (StatProperty): rune main property
        prefix_property (StatProperty): rune prefix property
        num_sub_props (int): number of sub properties to sample on the rune (1-4)
        exclude_sub_properties (list[StatProperty], optional): list of sub properties to exclude from selection. Defaults to [].
    
    Returns:
        PropertyEvent | SubPropertyEvent: event object for properties

    Raises:
        ValueError: invalid slot
    """
    props = [
        StatProperty.HP_ADD, StatProperty.ATK_ADD, StatProperty.DEF_ADD,
        StatProperty.HP_MUL, StatProperty.ATK_MUL, StatProperty.DEF_MUL,
        StatProperty.RES, StatProperty.ACC, StatProperty.CR, StatProperty.CD,
        StatProperty.SPD, 
    ]
    props.remove(main_stat_property)
    if prefix_property:
        props.remove(prefix_property)
    match slot:
        case RuneSlot.ONE:
            props.remove(StatProperty.DEF_ADD)
            props.remove(StatProperty.DEF_MUL)
        case RuneSlot.THREE:
            props.remove(StatProperty.ATK_ADD)
            props.remove(StatProperty.ATK_MUL)
        case RuneSlot.TWO | RuneSlot.FOUR | RuneSlot.FIVE | RuneSlot.SIX:
            pass
        case _:
            raise ValueError(f"Unknown rune slot: {slot}")
    for sub_prop in exclude_sub_properties:
        if sub_prop in props:
            props.remove(sub_prop)
    prop_event = PropertyEvent(props)
    if num_sub_props is None:
        # Event of all possible properties
        return prop_event
    elif num_sub_props == 0:
        return PropertyEvent([StatProperty.NO_PROPERTY])
    else:
        # Event of all possible properties of sample size num_sub_props
        return prop_event.sample_event(num_sub_props, replace=False)

def get_rune_sub_upgrades_event(
        sub_properties: list[StatProperty]
) -> UpgradeEvent:
    num_upgrades = len(sub_properties)
    selections = PropertyEvent(sub_properties).sample_event(num_upgrades, replace=True)
    return selections.get_event_as_counter()

