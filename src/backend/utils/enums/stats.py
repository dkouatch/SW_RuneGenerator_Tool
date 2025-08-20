from enum import Enum, unique

@unique
class StatProperty(Enum):
    HP_ADD = 1
    HP_MUL = 2
    ATK_ADD = 3
    ATK_MUL = 4
    DEF_ADD = 5
    DEF_MUL = 6
    SPD = 7
    RES = 8
    ACC = 9
    CR = 10
    CD = 11
    NO_PROPERTY = 12

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
