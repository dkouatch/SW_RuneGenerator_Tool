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
    Energy = 1
    Guard = 2
    Swift = 3
    Focus = 4
    Endure = 5
    Fatal = 6
    Blade = 7
    Rage = 8
    Violent = 9
    Will = 10
    Nemesis = 11
    Despair = 12
    Revenge = 13
    Destroy = 14
    Shield = 15
    Vampire = 16
    Seal = 17
    Intangible = 18
    Fight = 19
    Determination = 20
    Enhance = 21
    Accuracy = 22
    Tolerance = 23

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

@unique
class RuneType(Enum):
    NORMAL = 1
    ANCIENT = 2
