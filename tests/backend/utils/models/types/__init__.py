from enum import IntEnum, unique

@unique
class CoinToss(IntEnum):
    HEADS = 1
    TAILS = 2


@unique
class DiceRoll(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6