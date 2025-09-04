from enum import Enum, unique

@unique
class RuneSlot(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6

    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)

@unique
class RuneStars(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)

@unique
class RuneSet(Enum):
    ENERGY = 1
    GUARD = 2
    SWIFT = 3
    FOCUS = 4
    ENDURE = 5
    FATAL = 6
    BLADE = 7
    RAGE = 8
    VIOLENT = 9
    WILL = 10
    NEMESIS = 11
    DESPAIR = 12
    REVENGE = 13
    DESTROY = 14
    SHIELD = 15
    VAMPIRE = 16
    SEAL = 17
    INTANGIBLE = 18
    FIGHT = 19
    DETERMINATION = 20
    ENHANCE = 21
    ACCURACY = 22
    TOLERANCE = 23

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

@unique
class RuneType(Enum):
    NORMAL = 1
    ANCIENT = 2
