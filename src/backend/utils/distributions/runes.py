import operator

from src.backend.utils.models.enums.runes import *
from src.backend.utils.models.types.aliases.runes import *

# ------
# VALUES
# ------
def get_rune_main_value_distribution(
        stars: RuneStars,
        stage: int,
        main_property: RuneProperty) -> RuneValueDistribution:
    """
    Returns the distribution for value of a rune's main stat based on its property, stars, and stage.

    Args:
        stars (RuneStars): number of stars of rune (1-6)
        stage (int): upgrade stage (0-15)
        main_property (RuneProperty): rune main property
    
    Returns:
        RuneValueDistribution: distribution object for values
    
    Raises:
        ValueError: invalid star, main_property, or stage value
    """
    # Implementation to retrieve the range for the main stat
    match stars:
        case RuneStars.ONE:
            match main_property:
                case RuneProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            40, 85, 150,
                            195, 240, 285,
                            330, 375, 420,
                            465, 510, 555,
                            600, 645, 690,
                            804
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            3, 6, 9,
                            12, 15, 18,
                            21, 24, 27,
                            30, 33, 36,
                            39, 42, 45,
                            54
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case (RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL |
                      RuneProperty.SPD | RuneProperty.RES | RuneProperty.ACC | RuneProperty.CR):
                    if 0 <= stage and stage <= 15:
                        values = [
                            1, 2, 3,
                            4, 5, 6,
                            7, 8, 9,
                            10, 11, 12,
                            13, 14, 15,
                            18
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.CD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            2, 3, 4,
                            5, 6, 7,
                            8, 9, 10,
                            11, 12, 13,
                            14, 15, 16,
                            19
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_property}")
        case RuneStars.TWO:
            match main_property:
                case RuneProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            70, 130, 190,
                            250, 310, 370,
                            430, 490, 550,
                            610, 670, 730,
                            790, 850, 910,
                            1092
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            5, 9, 13,
                            17, 21, 25,
                            29, 33, 37,
                            41, 45, 49,
                            53, 57, 61,
                            73
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case (RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL |
                      RuneProperty.RES | RuneProperty.ACC | RuneProperty.CR | RuneProperty.SPD):
                    if 0 <= stage and stage <= 15:
                        values = [
                            2, 3, 4,
                            5, 6, 7,
                            8, 9, 10,
                            11, 12, 13,
                            14, 15, 16,
                            19
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.CD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            3, 5, 7,
                            9, 11, 13,
                            15, 17, 19,
                            21, 23, 25,
                            27, 29, 31,
                            37
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_property}")
        case RuneStars.THREE:
            match main_property:
                case RuneProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            100, 175, 250,
                            325, 400, 475,
                            550, 625, 700,
                            775, 850, 925,
                            1000, 1075, 1150,
                            1380
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            7, 12, 17,
                            22, 27, 32,
                            37, 42, 47,
                            52, 57, 62,
                            67, 72, 77,
                            92
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case (RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL |
                      RuneProperty.RES | RuneProperty.RES):
                    if 0 <= stage and stage <= 15:
                        values = [
                            4, 6, 8,
                            10, 12, 14,
                            16, 18, 20,
                            22, 24, 26,
                            28, 30, 32,
                            38
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.SPD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            3, 4, 6,
                            7, 8, 10,
                            11, 12, 14,
                            15, 16, 18,
                            19, 20, 22,
                            25
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.CR:
                    if 0 <= stage and stage <= 15:
                        values = [
                            3, 5, 7,
                            9, 11, 13,
                            15, 17, 19,
                            21, 23, 25,
                            27, 29, 31,
                            37
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.CD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            4, 6, 8,
                            11, 13, 15,
                            17, 20, 22,
                            24, 26, 29,
                            31, 33, 35,
                            43
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_property}")
        case RuneStars.FOUR:
            match main_property:
                case RuneProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            160, 250, 340,
                            430, 520, 610,
                            700, 790, 880,
                            970, 1060, 1150,
                            1240, 1330, 1420,
                            1704
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            10, 16, 22,
                            28, 34, 40,
                            46, 52, 58,
                            64, 70, 76,
                            82, 88, 94,
                            112
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    if 0 <= stage and stage <= 15:
                        values = [
                            5, 7, 9,
                            11, 14, 16,
                            18, 20, 22,
                            24, 26, 29,
                            31, 33, 35,
                            43
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.SPD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            4, 5, 7,
                            8, 10, 11,
                            13, 14, 16,
                            17, 19, 20,
                            22, 23, 25,
                            30
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.RES | RuneProperty.ACC:
                    if 0 <= stage and stage <= 15:
                        values = [
                            6, 8, 10,
                            12, 15, 17,
                            19, 21, 23,
                            25, 27, 30,
                            32, 34, 36,
                            44
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.CR:
                    if 0 <= stage and stage <= 15:
                        values = [
                            4, 6, 8,
                            10, 13, 15,
                            17, 19, 21,
                            23, 25, 28,
                            30, 32, 34,
                            42
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.CD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            6, 9, 12,
                            15, 18, 21,
                            24, 27, 30,
                            33, 36, 39,
                            42, 45, 48,
                            54
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_property}")
        case RuneStars.FIVE:
            match main_property:
                case RuneProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            270, 375, 480,
                            585, 690, 795,
                            900, 1005, 1110,
                            1215, 1320, 1425,
                            1530, 1635, 1740,
                            2088
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            15, 22, 29,
                            36, 43, 50,
                            57, 64, 71,
                            78, 85, 92,
                            99, 106, 113,
                            135
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    if 0 <= stage and stage <= 15:
                        values = [
                            8, 10, 13,
                            15, 18, 20,
                            23, 25, 28,
                            30, 32, 35,
                            37, 40, 42,
                            51
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.SPD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            5, 7, 9,
                            11, 13, 15,
                            17, 19, 21,
                            23, 25, 27,
                            29, 31, 33,
                            39
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.RES | RuneProperty.ACC:
                    if 0 <= stage and stage <= 15:
                        values = [
                            9, 11, 14,
                            16, 19, 21,
                            24, 26, 29,
                            31, 33, 36,
                            38, 41, 43,
                            51
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.CR:
                    if 0 <= stage and stage <= 15:
                        values = [
                            5, 7, 10,
                            12, 15, 17,
                            20, 22, 25,
                            27, 29, 32,
                            34, 37, 39,
                            47
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.CD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            8, 11, 15,
                            18, 21, 25,
                            28, 31, 35,
                            38, 41, 45,
                            48, 51, 55,
                            65
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_property}")
        case RuneStars.SIX:
            match main_property:
                case RuneProperty.HP_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            360, 460, 600,
                            720, 840, 960,
                            1080, 1200, 1320,
                            1440, 1560, 1680,
                            1800, 1920, 2040,
                            2448,
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            22, 30, 38,
                            46, 54, 62,
                            70, 78, 86,
                            94, 102, 110,
                            118, 126, 134,
                            160
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    if 0 <= stage and stage <= 15:
                        values = [
                            11, 14, 17,
                            20, 23, 26,
                            29, 32, 35,
                            38, 41, 44,
                            47, 50, 53,
                            63
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.SPD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            7, 9, 11,
                            13, 15, 17,
                            19, 21, 23,
                            25, 27, 29,
                            31, 33, 35,
                            42
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.RES | RuneProperty.ACC:
                    if 0 <= stage and stage <= 15:
                        values = [
                            12, 15, 18,
                            21, 24, 27,
                            30, 33, 36,
                            39, 42, 45,
                            48, 51, 54,
                            64
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.CR:
                    if 0 <= stage and stage <= 15:
                        values = [
                            7, 10, 13,
                            16, 19, 22,
                            25, 28, 31,
                            34, 37, 40,
                            43, 46, 49,
                            58
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case RuneProperty.CD:
                    if 0 <= stage and stage <= 15:
                        values = [
                            11, 14, 17,
                            20, 23, 26,
                            29, 32, 35,
                            38, 41, 44,
                            47, 50, 53,
                            63
                        ]
                        return RuneValueDistribution([values[stage]])
                    else:
                        raise ValueError(f"Invalid stage: {stage}")
                case _:
                    raise ValueError(f"Unknown property: {main_property}")
    

def get_rune_prefix_value_distribution(
        stars: RuneStars,
        prefix_property: RuneProperty) -> RuneValueDistribution:
    """
    Returns the distribution for a rune's prefix stat value based on its stars and property.

    Args:
        stars (RuneStars): Number of stars of rune (1-6)
        prefix_property (RuneProperty): Rune prefix property
    
    Returns:
        RuneValueDistribution: distribution object for values
    
    Raises:
        ValueError: If the stars or prefix property are invalid
    """
    # Implementation to retrieve the range for the prefix stat
    match stars:
        case RuneStars.ONE:
            match prefix_property:
                case RuneProperty.NO_PROPERTY:
                    return RuneValueDistribution([0])
                case RuneProperty.HP_ADD:
                    return RuneValueDistribution(range(15, 61))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    return RuneValueDistribution(range(1, 5))
                case (RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL |
                      RuneProperty.CR | RuneProperty.CD | RuneProperty.RES | RuneProperty.ACC):
                    return RuneValueDistribution(range(1, 3))
                case RuneProperty.SPD:
                    return RuneValueDistribution([1])
        case RuneStars.TWO:
            match prefix_property:
                case RuneProperty.NO_PROPERTY:
                    return RuneValueDistribution([0])
                case RuneProperty.HP_ADD:
                    return RuneValueDistribution(range(30, 106))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    return RuneValueDistribution(range(2, 6))
                case (RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL |
                      RuneProperty.CR | RuneProperty.CD | RuneProperty.RES | RuneProperty.ACC):
                    return RuneValueDistribution(range(1, 4))
                case RuneProperty.SPD:
                    return RuneValueDistribution(range(1, 3))
        case RuneStars.THREE:
            match prefix_property:
                case RuneProperty.NO_PROPERTY:
                    return RuneValueDistribution([0])
                case RuneProperty.HP_ADD:
                    return RuneValueDistribution(range(45, 166))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    return RuneValueDistribution(range(3, 9))
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    return RuneValueDistribution(range(2, 6))
                case RuneProperty.SPD | RuneProperty.CR:
                    return RuneValueDistribution(range(1, 4))
                case RuneProperty.RES | RuneProperty.ACC | RuneProperty.CD:
                    return RuneValueDistribution(range(2, 5))
        case RuneStars.FOUR:
            match prefix_property:
                case RuneProperty.NO_PROPERTY:
                    return RuneValueDistribution([0])
                case RuneProperty.HP_ADD:
                    return RuneValueDistribution(range(60, 226))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    return RuneValueDistribution(range(4, 11))
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    return RuneValueDistribution(range(3, 7))
                case RuneProperty.SPD | RuneProperty.CR:
                    return RuneValueDistribution(range(2, 5))
                case RuneProperty.RES | RuneProperty.ACC | RuneProperty.CD:
                    return RuneValueDistribution(range(2, 6))
        case RuneStars.FIVE:
            match prefix_property:
                case RuneProperty.NO_PROPERTY:
                    return RuneValueDistribution([0])
                case RuneProperty.HP_ADD:
                    return RuneValueDistribution(range(90, 301))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    return RuneValueDistribution(range(8, 16))
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    return RuneValueDistribution(range(4, 8))
                case RuneProperty.SPD | RuneProperty.CR | RuneProperty.CD:
                    return RuneValueDistribution(range(3, 6))
                case RuneProperty.RES | RuneProperty.ACC:
                    return RuneValueDistribution(range(3, 8))
        case RuneStars.SIX:
            match prefix_property:
                case RuneProperty.NO_PROPERTY:
                    return RuneValueDistribution([0])
                case RuneProperty.HP_ADD:
                    return RuneValueDistribution(range(135, 376))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    return RuneValueDistribution(range(10, 21))
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    return RuneValueDistribution(range(5, 9))
                case RuneProperty.SPD | RuneProperty.CR:
                    return RuneValueDistribution(range(4, 7))
                case RuneProperty.RES | RuneProperty.ACC:
                    return RuneValueDistribution(range(4, 9))
                case RuneProperty.CD:
                    return RuneValueDistribution(range(4, 8))

def get_rune_sub_value_distribution(
        stars: RuneStars,
        sub_property: RuneProperty,
        num_upgrades: int = 0) -> RuneValueDistribution:
    """
    Returns the distribution for a rune's substat value based on its stars and property.

    This returned distribution is used for calculating innate and additional substat values.

    Args:
        stars (RuneStars): Number of stars of rune (1-6)
        sub_property (RuneProperty): Rune substat property
        num_upgrades (int, optional): Number of times the substat has been upgraded (0-4)
    
    Returns:
        RuneValueDistribution: distribution object for values
    
    Raises:
        ValueError: If the stars or sub property are invalid
    """
    # Implementation to retrieve the range for the sub stat
    match stars:
        case RuneStars.ONE:
            match sub_property:
                case RuneProperty.NO_PROPERTY:
                    distribution = RuneValueDistribution([0])
                case RuneProperty.HP_ADD:
                    distribution = RuneValueDistribution(range(15, 61))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    distribution = RuneValueDistribution(range(1, 5))
                case (RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL |
                      RuneProperty.CR | RuneProperty.CD | RuneProperty.RES | RuneProperty.ACC):
                    distribution = RuneValueDistribution(range(1, 3))
                case RuneProperty.SPD:
                    distribution = RuneValueDistribution([1])
        case RuneStars.TWO:
            match sub_property:
                case RuneProperty.NO_PROPERTY:
                    distribution = RuneValueDistribution([0])
                case RuneProperty.HP_ADD:
                    distribution = RuneValueDistribution(range(30, 106))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    distribution = RuneValueDistribution(range(2, 6))
                case (RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL |
                      RuneProperty.CR | RuneProperty.CD | RuneProperty.RES | RuneProperty.ACC):
                    distribution = RuneValueDistribution(range(1, 4))
                case RuneProperty.SPD:
                    distribution = RuneValueDistribution(range(1, 3))
        case RuneStars.THREE:
            match sub_property:
                case RuneProperty.NO_PROPERTY:
                    distribution = RuneValueDistribution([0])
                case RuneProperty.HP_ADD:
                    distribution = RuneValueDistribution(range(45, 166))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    distribution = RuneValueDistribution(range(3, 9))
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    distribution = RuneValueDistribution(range(2, 6))
                case RuneProperty.SPD | RuneProperty.CR:
                    distribution = RuneValueDistribution(range(1, 4))
                case RuneProperty.RES | RuneProperty.ACC | RuneProperty.CD:
                    distribution = RuneValueDistribution(range(2, 5))
        case RuneStars.FOUR:
            match sub_property:
                case RuneProperty.HP_ADD:
                    distribution = RuneValueDistribution(range(60, 226))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    distribution = RuneValueDistribution(range(4, 11))
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    distribution = RuneValueDistribution(range(3, 7))
                case RuneProperty.SPD | RuneProperty.CR:
                    distribution = RuneValueDistribution(range(2, 5))
                case RuneProperty.RES | RuneProperty.ACC | RuneProperty.CD:
                    distribution = RuneValueDistribution(range(2, 6))
                case _:
                    raise ValueError(f"Invalid property: {sub_property}")
        case RuneStars.FIVE:
            match sub_property:
                case RuneProperty.HP_ADD:
                    distribution = RuneValueDistribution(range(90, 301))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    distribution = RuneValueDistribution(range(8, 16))
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    distribution = RuneValueDistribution(range(4, 8))
                case RuneProperty.SPD | RuneProperty.CR | RuneProperty.CD:
                    distribution = RuneValueDistribution(range(3, 6))
                case RuneProperty.RES | RuneProperty.ACC:
                    distribution = RuneValueDistribution(range(3, 8))
                case _:
                    raise ValueError(f"Invalid property: {sub_property}")
        case RuneStars.SIX:
            match sub_property:
                case RuneProperty.NO_PROPERTY:
                    distribution = RuneValueDistribution([0])
                case RuneProperty.HP_ADD:
                    distribution = RuneValueDistribution(range(135, 376))
                case RuneProperty.ATK_ADD | RuneProperty.DEF_ADD:
                    distribution = RuneValueDistribution(range(10, 21))
                case RuneProperty.HP_MUL | RuneProperty.ATK_MUL | RuneProperty.DEF_MUL:
                    distribution = RuneValueDistribution(range(5, 9))
                case RuneProperty.SPD | RuneProperty.CR:
                    distribution = RuneValueDistribution(range(4, 7))
                case RuneProperty.RES | RuneProperty.ACC:
                    distribution = RuneValueDistribution(range(4, 9))
                case RuneProperty.CD:
                    distribution = RuneValueDistribution(range(4, 8))
    if num_upgrades <= 0 or num_upgrades > 5:
        raise ValueError(f"Invalid number of upgrades: {num_upgrades}")
    else:
        intersect_distribution = distribution.intersect_self(num_upgrades)
        return intersect_distribution.reduce(operator.add)

# ----------
# PROPERTIES
# ----------
def get_rune_main_property_distribution(slot: RuneSlot) -> RunePropertyDistribution:
    """
    Returns a valid main property for a rune based on its slot.

    Args:
        slot (RuneSlot): rune slot (1-6)
    
    Returns:
        RunePropertyDistribution: distribution object for properties
    
    Raises:
        ValueError: incorrect slot
    """
    match slot:
        case RuneSlot.ONE:
            return RunePropertyDistribution([RuneProperty.ATK_ADD])
        case RuneSlot.TWO:
            return RunePropertyDistribution([
                RuneProperty.HP_MUL, RuneProperty.ATK_MUL, RuneProperty.DEF_MUL,
                RuneProperty.HP_ADD, RuneProperty.ATK_ADD, RuneProperty.DEF_ADD,
                RuneProperty.SPD
            ])
        case RuneSlot.THREE:
            return RunePropertyDistribution([RuneProperty.DEF_ADD])
        case RuneSlot.FOUR:
            return RunePropertyDistribution([
                RuneProperty.HP_MUL, RuneProperty.ATK_MUL, RuneProperty.DEF_MUL,
                RuneProperty.HP_ADD, RuneProperty.ATK_ADD, RuneProperty.DEF_ADD,
                RuneProperty.CR, RuneProperty.CD
            ])
        case RuneSlot.FIVE:
            return RunePropertyDistribution([RuneProperty.HP_ADD])
        case RuneSlot.SIX:
            return RunePropertyDistribution([
                RuneProperty.HP_MUL, RuneProperty.ATK_MUL, RuneProperty.DEF_MUL,
                RuneProperty.HP_ADD, RuneProperty.ATK_ADD, RuneProperty.DEF_ADD,
                RuneProperty.RES, RuneProperty.ACC
            ])

def get_rune_prefix_property_distribution(
        slot: RuneSlot,
        main_property: RuneProperty) -> RunePropertyDistribution:
    """
    Returns a valid prefix property for a rune based its main property and slot.

    Args:
        slot (RuneSlot): rune slot (1-6)
        main_property (RuneProperty): rune main property
    
    Returns:
        RunePropertyDistribution: distribution object for properties
    
    Raises:
        ValueError: invalid slot
    """
    props = [
        RuneProperty.HP_ADD, RuneProperty.HP_MUL,
        RuneProperty.ATK_ADD, RuneProperty.ATK_MUL,
        RuneProperty.DEF_ADD, RuneProperty.DEF_MUL,
        RuneProperty.RES, RuneProperty.ACC,
        RuneProperty.CR, RuneProperty.CD,
        RuneProperty.SPD, RuneProperty.NO_PROPERTY 
    ]
    distribution = RunePropertyDistribution(props)
    match slot:
        case RuneSlot.ONE:
            distribution.remove([RuneProperty.DEF_ADD, RuneProperty.DEF_MUL, RuneProperty.ATK_ADD])
        case RuneSlot.THREE:
            distribution.remove([RuneProperty.ATK_ADD, RuneProperty.ATK_MUL, RuneProperty.DEF_ADD])
        case RuneSlot.FIVE:
            distribution.remove([RuneProperty.HP_ADD])
        case RuneSlot.TWO | RuneSlot.FOUR | RuneSlot.SIX:
            distribution.remove([main_property])
    distribution.rebalance(RuneProperty.NO_PROPERTY, 0.75)
    return distribution

def get_rune_sub_properties_distribution(
        slot: RuneSlot,
        main_property: RuneProperty,
        prefix_property: RuneProperty,
        num_sub_props: int | None = None,
        exclude_sub_properties: list[RuneProperty] = []) -> RunePropertyDistribution | RuneSubPropertyDistribution:
    """
    Returns a valid sub property for a rune based its main and prefix properties and slot

    Args:
        slot (RuneSlot): rune slot (1-6)
        main_property (RuneProperty): rune main property
        prefix_property (RuneProperty): rune prefix property
        num_sub_props (int | None, optional): number of sub properties to sample (w/o replacement) on the rune (1-4)
        exclude_sub_properties (list[RuneProperty], optional): list of sub properties to exclude from selection. Defaults to [].
    
    Returns:
        RunePropertyDistribution | RuneSubPropertyDistribution: distribution object for properties

    Raises:
        ValueError: invalid slot
    """
    props = [
        RuneProperty.HP_ADD, RuneProperty.ATK_ADD, RuneProperty.DEF_ADD,
        RuneProperty.HP_MUL, RuneProperty.ATK_MUL, RuneProperty.DEF_MUL,
        RuneProperty.RES, RuneProperty.ACC, RuneProperty.CR, RuneProperty.CD,
        RuneProperty.SPD, 
    ]
    props.remove(main_property)
    if prefix_property:
        props.remove(prefix_property)
    match slot:
        case RuneSlot.ONE:
            props.remove(RuneProperty.DEF_ADD)
            props.remove(RuneProperty.DEF_MUL)
        case RuneSlot.THREE:
            props.remove(RuneProperty.ATK_ADD)
            props.remove(RuneProperty.ATK_MUL)
        case RuneSlot.TWO | RuneSlot.FOUR | RuneSlot.FIVE | RuneSlot.SIX:
            pass
    for sub_prop in exclude_sub_properties:
        if sub_prop in props:
            props.remove(sub_prop)
    prop_distribution = RunePropertyDistribution(props)
    if num_sub_props is None:
        # Distribution of all possible properties
        return prop_distribution
    elif num_sub_props == 0:
        return RunePropertyDistribution([RuneProperty.NO_PROPERTY])
    else:
        # Distribution of all possible properties of sample size num_sub_props
        return prop_distribution.sample_distribution(num_sub_props, replace=False)

def get_rune_sub_roll_counts_distribution(
        sub_properties: list[RuneProperty]
) -> RuneRollDistribution:
    num_upgrades = len(sub_properties)
    selections = RunePropertyDistribution(sub_properties).sample_distribution(num_upgrades, replace=True).to_counter()
    return selections.map(
            lambda counter: counter + RuneRollCounts(sub_properties))
