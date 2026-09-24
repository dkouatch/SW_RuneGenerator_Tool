import operator

from src.backend.utils.models.enums.runes import *
from src.backend.utils.models.types.aliases.runes import *

# ------
# VALUES
# ------
def get_rune_main_value_distribution(
        grade: RuneGrade,
        stage: int,
        main_stat: RuneStat) -> RuneValueDistribution:
    """
    Returns the distribution for value of a rune's main stat based on its stat, grade, and stage.

    Args:
        grade (RuneGrade): star-grade of rune (1-6)
        stage (int): upgrade stage (0-15)
        main_stat (RuneStat): rune main stat
    
    Returns:
        RuneValueDistribution: distribution object for values
    
    Raises:
        ValueError: invalid star, main_stat, or stage value
    """
    # Implementation to retrieve the range for the main stat
    match grade:
        case RuneGrade.ONE_STAR:
            match main_stat:
                case RuneStat.HP_ADD:
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
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
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
                case (RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL |
                      RuneStat.SPD | RuneStat.RES | RuneStat.ACC | RuneStat.CR):
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
                case RuneStat.CD:
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
                    raise ValueError(f"Unknown stat: {main_stat}")
        case RuneGrade.TWO_STAR:
            match main_stat:
                case RuneStat.HP_ADD:
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
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
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
                case (RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL |
                      RuneStat.RES | RuneStat.ACC | RuneStat.CR | RuneStat.SPD):
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
                case RuneStat.CD:
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
                    raise ValueError(f"Unknown stat: {main_stat}")
        case RuneGrade.THREE_STAR:
            match main_stat:
                case RuneStat.HP_ADD:
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
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
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
                case (RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL |
                      RuneStat.RES | RuneStat.RES):
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
                case RuneStat.SPD:
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
                case RuneStat.CR:
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
                case RuneStat.CD:
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
                    raise ValueError(f"Unknown stat: {main_stat}")
        case RuneGrade.FOUR_STAR:
            match main_stat:
                case RuneStat.HP_ADD:
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
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
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
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
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
                case RuneStat.SPD:
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
                case RuneStat.RES | RuneStat.ACC:
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
                case RuneStat.CR:
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
                case RuneStat.CD:
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
                    raise ValueError(f"Unknown stat: {main_stat}")
        case RuneGrade.FIVE_STAR:
            match main_stat:
                case RuneStat.HP_ADD:
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
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
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
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
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
                case RuneStat.SPD:
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
                case RuneStat.RES | RuneStat.ACC:
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
                case RuneStat.CR:
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
                case RuneStat.CD:
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
                    raise ValueError(f"Unknown stat: {main_stat}")
        case RuneGrade.SIX_STAR:
            match main_stat:
                case RuneStat.HP_ADD:
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
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
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
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
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
                case RuneStat.SPD:
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
                case RuneStat.RES | RuneStat.ACC:
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
                case RuneStat.CR:
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
                case RuneStat.CD:
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
                    raise ValueError(f"Unknown stat: {main_stat}")
    

def get_rune_prefix_value_distribution(
        grade: RuneGrade,
        prefix_stat: RuneStat) -> RuneValueDistribution:
    """
    Returns the distribution for a rune's prefix stat value based on its grade and stat.

    Args:
        grade (RuneGrade): Star-grade of rune (1-6)
        prefix_stat (RuneStat): Rune prefix stat
    
    Returns:
        RuneValueDistribution: distribution object for values
    
    Raises:
        ValueError: If the grade or prefix stat are invalid
    """
    # Implementation to retrieve the range for the prefix stat
    match grade:
        case RuneGrade.ONE_STAR:
            match prefix_stat:
                case RuneStat.NONE:
                    return RuneValueDistribution([0])
                case RuneStat.HP_ADD:
                    return RuneValueDistribution(range(15, 61))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    return RuneValueDistribution(range(1, 5))
                case (RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL |
                      RuneStat.CR | RuneStat.CD | RuneStat.RES | RuneStat.ACC):
                    return RuneValueDistribution(range(1, 3))
                case RuneStat.SPD:
                    return RuneValueDistribution([1])
        case RuneGrade.TWO_STAR:
            match prefix_stat:
                case RuneStat.NONE:
                    return RuneValueDistribution([0])
                case RuneStat.HP_ADD:
                    return RuneValueDistribution(range(30, 106))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    return RuneValueDistribution(range(2, 6))
                case (RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL |
                      RuneStat.CR | RuneStat.CD | RuneStat.RES | RuneStat.ACC):
                    return RuneValueDistribution(range(1, 4))
                case RuneStat.SPD:
                    return RuneValueDistribution(range(1, 3))
        case RuneGrade.THREE_STAR:
            match prefix_stat:
                case RuneStat.NONE:
                    return RuneValueDistribution([0])
                case RuneStat.HP_ADD:
                    return RuneValueDistribution(range(45, 166))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    return RuneValueDistribution(range(3, 9))
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
                    return RuneValueDistribution(range(2, 6))
                case RuneStat.SPD | RuneStat.CR:
                    return RuneValueDistribution(range(1, 4))
                case RuneStat.RES | RuneStat.ACC | RuneStat.CD:
                    return RuneValueDistribution(range(2, 5))
        case RuneGrade.FOUR_STAR:
            match prefix_stat:
                case RuneStat.NONE:
                    return RuneValueDistribution([0])
                case RuneStat.HP_ADD:
                    return RuneValueDistribution(range(60, 226))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    return RuneValueDistribution(range(4, 11))
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
                    return RuneValueDistribution(range(3, 7))
                case RuneStat.SPD | RuneStat.CR:
                    return RuneValueDistribution(range(2, 5))
                case RuneStat.RES | RuneStat.ACC | RuneStat.CD:
                    return RuneValueDistribution(range(2, 6))
        case RuneGrade.FIVE_STAR:
            match prefix_stat:
                case RuneStat.NONE:
                    return RuneValueDistribution([0])
                case RuneStat.HP_ADD:
                    return RuneValueDistribution(range(90, 301))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    return RuneValueDistribution(range(8, 16))
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
                    return RuneValueDistribution(range(4, 8))
                case RuneStat.SPD | RuneStat.CR | RuneStat.CD:
                    return RuneValueDistribution(range(3, 6))
                case RuneStat.RES | RuneStat.ACC:
                    return RuneValueDistribution(range(3, 8))
        case RuneGrade.SIX_STAR:
            match prefix_stat:
                case RuneStat.NONE:
                    return RuneValueDistribution([0])
                case RuneStat.HP_ADD:
                    return RuneValueDistribution(range(135, 376))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    return RuneValueDistribution(range(10, 21))
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
                    return RuneValueDistribution(range(5, 9))
                case RuneStat.SPD | RuneStat.CR:
                    return RuneValueDistribution(range(4, 7))
                case RuneStat.RES | RuneStat.ACC:
                    return RuneValueDistribution(range(4, 9))
                case RuneStat.CD:
                    return RuneValueDistribution(range(4, 8))

def get_rune_sub_value_distribution(
        grade: RuneGrade,
        sub_stat: RuneStat,
        num_upgrades: int = 0) -> RuneValueDistribution:
    """
    Returns the distribution for a rune's substat value based on its grade and stat.

    This returned distribution is used for calculating innate and additional substat values.

    Args:
        grade (RuneGrade): Star-grade of rune (1-6)
        sub_stat (RuneStat): Rune substat stat
        num_upgrades (int, optional): Number of times the substat has been upgraded (0-4)
    
    Returns:
        RuneValueDistribution: distribution object for values
    
    Raises:
        ValueError: If the grade or sub stat are invalid
    """
    # Implementation to retrieve the range for the sub stat
    match grade:
        case RuneGrade.ONE_STAR:
            match sub_stat:
                case RuneStat.NONE:
                    distribution = RuneValueDistribution([0])
                case RuneStat.HP_ADD:
                    distribution = RuneValueDistribution(range(15, 61))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    distribution = RuneValueDistribution(range(1, 5))
                case (RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL |
                      RuneStat.CR | RuneStat.CD | RuneStat.RES | RuneStat.ACC):
                    distribution = RuneValueDistribution(range(1, 3))
                case RuneStat.SPD:
                    distribution = RuneValueDistribution([1])
        case RuneGrade.TWO_STAR:
            match sub_stat:
                case RuneStat.NONE:
                    distribution = RuneValueDistribution([0])
                case RuneStat.HP_ADD:
                    distribution = RuneValueDistribution(range(30, 106))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    distribution = RuneValueDistribution(range(2, 6))
                case (RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL |
                      RuneStat.CR | RuneStat.CD | RuneStat.RES | RuneStat.ACC):
                    distribution = RuneValueDistribution(range(1, 4))
                case RuneStat.SPD:
                    distribution = RuneValueDistribution(range(1, 3))
        case RuneGrade.THREE_STAR:
            match sub_stat:
                case RuneStat.NONE:
                    distribution = RuneValueDistribution([0])
                case RuneStat.HP_ADD:
                    distribution = RuneValueDistribution(range(45, 166))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    distribution = RuneValueDistribution(range(3, 9))
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
                    distribution = RuneValueDistribution(range(2, 6))
                case RuneStat.SPD | RuneStat.CR:
                    distribution = RuneValueDistribution(range(1, 4))
                case RuneStat.RES | RuneStat.ACC | RuneStat.CD:
                    distribution = RuneValueDistribution(range(2, 5))
        case RuneGrade.FOUR_STAR:
            match sub_stat:
                case RuneStat.HP_ADD:
                    distribution = RuneValueDistribution(range(60, 226))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    distribution = RuneValueDistribution(range(4, 11))
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
                    distribution = RuneValueDistribution(range(3, 7))
                case RuneStat.SPD | RuneStat.CR:
                    distribution = RuneValueDistribution(range(2, 5))
                case RuneStat.RES | RuneStat.ACC | RuneStat.CD:
                    distribution = RuneValueDistribution(range(2, 6))
                case _:
                    raise ValueError(f"Invalid stat: {sub_stat}")
        case RuneGrade.FIVE_STAR:
            match sub_stat:
                case RuneStat.HP_ADD:
                    distribution = RuneValueDistribution(range(90, 301))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    distribution = RuneValueDistribution(range(8, 16))
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
                    distribution = RuneValueDistribution(range(4, 8))
                case RuneStat.SPD | RuneStat.CR | RuneStat.CD:
                    distribution = RuneValueDistribution(range(3, 6))
                case RuneStat.RES | RuneStat.ACC:
                    distribution = RuneValueDistribution(range(3, 8))
                case _:
                    raise ValueError(f"Invalid stat: {sub_stat}")
        case RuneGrade.SIX_STAR:
            match sub_stat:
                case RuneStat.NONE:
                    distribution = RuneValueDistribution([0])
                case RuneStat.HP_ADD:
                    distribution = RuneValueDistribution(range(135, 376))
                case RuneStat.ATK_ADD | RuneStat.DEF_ADD:
                    distribution = RuneValueDistribution(range(10, 21))
                case RuneStat.HP_MUL | RuneStat.ATK_MUL | RuneStat.DEF_MUL:
                    distribution = RuneValueDistribution(range(5, 9))
                case RuneStat.SPD | RuneStat.CR:
                    distribution = RuneValueDistribution(range(4, 7))
                case RuneStat.RES | RuneStat.ACC:
                    distribution = RuneValueDistribution(range(4, 9))
                case RuneStat.CD:
                    distribution = RuneValueDistribution(range(4, 8))
    if num_upgrades <= 0 or num_upgrades > 5:
        raise ValueError(f"Invalid number of upgrades: {num_upgrades}")
    else:
        intersect_distribution = distribution.intersect_self(num_upgrades)
        return intersect_distribution.reduce(operator.add)

# ----------
# PROPERTIES
# ----------
def get_rune_main_stat_distribution(slot: RuneSlot) -> RuneStatDistribution:
    """
    Returns a valid main stat for a rune based on its slot.

    Args:
        slot (RuneSlot): rune slot (1-6)
    
    Returns:
        RuneStatDistribution: distribution object for stats
    
    Raises:
        ValueError: incorrect slot
    """
    match slot:
        case RuneSlot.ONE:
            return RuneStatDistribution([RuneStat.ATK_ADD])
        case RuneSlot.TWO:
            return RuneStatDistribution([
                RuneStat.HP_MUL, RuneStat.ATK_MUL, RuneStat.DEF_MUL,
                RuneStat.HP_ADD, RuneStat.ATK_ADD, RuneStat.DEF_ADD,
                RuneStat.SPD
            ])
        case RuneSlot.THREE:
            return RuneStatDistribution([RuneStat.DEF_ADD])
        case RuneSlot.FOUR:
            return RuneStatDistribution([
                RuneStat.HP_MUL, RuneStat.ATK_MUL, RuneStat.DEF_MUL,
                RuneStat.HP_ADD, RuneStat.ATK_ADD, RuneStat.DEF_ADD,
                RuneStat.CR, RuneStat.CD
            ])
        case RuneSlot.FIVE:
            return RuneStatDistribution([RuneStat.HP_ADD])
        case RuneSlot.SIX:
            return RuneStatDistribution([
                RuneStat.HP_MUL, RuneStat.ATK_MUL, RuneStat.DEF_MUL,
                RuneStat.HP_ADD, RuneStat.ATK_ADD, RuneStat.DEF_ADD,
                RuneStat.RES, RuneStat.ACC
            ])

def get_rune_prefix_stat_distribution(
        slot: RuneSlot,
        main_stat: RuneStat) -> RuneStatDistribution:
    """
    Returns a valid prefix stat for a rune based its main stat and slot.

    Args:
        slot (RuneSlot): rune slot (1-6)
        main_stat (RuneStat): rune main stat
    
    Returns:
        RuneStatDistribution: distribution object for stats
    
    Raises:
        ValueError: invalid slot
    """
    props = [
        RuneStat.HP_ADD, RuneStat.HP_MUL,
        RuneStat.ATK_ADD, RuneStat.ATK_MUL,
        RuneStat.DEF_ADD, RuneStat.DEF_MUL,
        RuneStat.RES, RuneStat.ACC,
        RuneStat.CR, RuneStat.CD,
        RuneStat.SPD, RuneStat.NONE 
    ]
    distribution = RuneStatDistribution(props)
    match slot:
        case RuneSlot.ONE:
            distribution.remove([RuneStat.DEF_ADD, RuneStat.DEF_MUL, RuneStat.ATK_ADD])
        case RuneSlot.THREE:
            distribution.remove([RuneStat.ATK_ADD, RuneStat.ATK_MUL, RuneStat.DEF_ADD])
        case RuneSlot.FIVE:
            distribution.remove([RuneStat.HP_ADD])
        case RuneSlot.TWO | RuneSlot.FOUR | RuneSlot.SIX:
            distribution.remove([main_stat])
    distribution.rebalance(RuneStat.NONE, 0.75)
    return distribution

def get_rune_sub_stats_distribution(
        slot: RuneSlot,
        main_stat: RuneStat,
        prefix_stat: RuneStat,
        num_sub_props: int | None = None,
        exclude_sub_stats: list[RuneStat] = []) -> RuneStatDistribution | RuneSubStatDistribution:
    """
    Returns a valid sub stat for a rune based its main and prefix stats and slot

    Args:
        slot (RuneSlot): rune slot (1-6)
        main_stat (RuneStat): rune main stat
        prefix_stat (RuneStat): rune prefix stat
        num_sub_props (int | None, optional): number of sub stats to sample (w/o replacement) on the rune (1-4)
        exclude_sub_stats (list[RuneStat], optional): list of sub stats to exclude from selection. Defaults to [].
    
    Returns:
        RuneStatDistribution | RuneSubStatDistribution: distribution object for stats

    Raises:
        ValueError: invalid slot
    """
    props = [
        RuneStat.HP_ADD, RuneStat.ATK_ADD, RuneStat.DEF_ADD,
        RuneStat.HP_MUL, RuneStat.ATK_MUL, RuneStat.DEF_MUL,
        RuneStat.RES, RuneStat.ACC, RuneStat.CR, RuneStat.CD,
        RuneStat.SPD, 
    ]
    props.remove(main_stat)
    if prefix_stat:
        props.remove(prefix_stat)
    match slot:
        case RuneSlot.ONE:
            props.remove(RuneStat.DEF_ADD)
            props.remove(RuneStat.DEF_MUL)
        case RuneSlot.THREE:
            props.remove(RuneStat.ATK_ADD)
            props.remove(RuneStat.ATK_MUL)
        case RuneSlot.TWO | RuneSlot.FOUR | RuneSlot.FIVE | RuneSlot.SIX:
            pass
    for sub_prop in exclude_sub_stats:
        if sub_prop in props:
            props.remove(sub_prop)
    prop_distribution = RuneStatDistribution(props)
    if num_sub_props is None:
        # Distribution of all possible stats
        return prop_distribution
    elif num_sub_props == 0:
        return RuneStatDistribution([RuneStat.NONE])
    else:
        # Distribution of all possible stats of sample size num_sub_props
        return prop_distribution.sample_distribution(num_sub_props, replace=False)

def get_rune_sub_roll_counts_distribution(
        sub_stats: list[RuneStat]
) -> RuneRollDistribution:
    num_upgrades = len(sub_stats)
    selections = RuneStatDistribution(sub_stats).sample_distribution(num_upgrades, replace=True).to_counter()
    return selections.map(
            lambda counter: counter + RuneRollCounts(sub_stats))
