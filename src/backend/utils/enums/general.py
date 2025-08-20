from enum import Enum, unique

@unique
class Grade(Enum):
    NORMAL = 1
    MAGIC = 2
    RARE = 3
    HERO = 4
    LEGEND = 5

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
