from enum import Enum, unique

@unique
class GrindRarity(Enum):
    NORMAL = 1
    MAGIC = 2
    RARE = 3
    HERO = 4
    LEGEND = 5

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name


@unique
class GrindSet(Enum):
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
class GrindType(Enum):
    NORMAL = 1
    ANCIENT = 2


@unique
class GrindStat(Enum):
    HP_ADD = 1
    HP_MUL = 2
    ATK_ADD = 3
    ATK_MUL = 4
    DEF_ADD = 5
    DEF_MUL = 6
    SPD = 7


    def __str__(self):
        match self:
            case GrindStat.HP_ADD:
                return "HP"
            case GrindStat.HP_MUL:
                return "HP%"
            case GrindStat.ATK_ADD:
                return "ATK"
            case GrindStat.ATK_MUL:
                return "ATK%"
            case GrindStat.DEF_ADD:
                return "DEF"
            case GrindStat.DEF_MUL:
                return "DEF%"
            case GrindStat.SPD:
                return "SPD"

    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        if not isinstance(other, GrindStat):
            return NotImplemented
        return self.value == other.value
    
    def __lt__(self, other):
        if not isinstance(other, GrindStat):
            return NotImplemented
        return self.value < other.value
    
    def __le__(self, other):
        if not isinstance(other, GrindStat):
            return NotImplemented
        return self.value <= other.value
    
    def __ge__(self, other):
        if not isinstance(other, GrindStat):
            return NotImplemented
        return self.value >= other.value
    
    def __gt__(self, other):
        if not isinstance(other, GrindStat):
            return NotImplemented
        return self.value > other.value
    
    @property
    def is_additive(self) -> bool:
        """Check if the stat property is additive."""
        return self in {
            GrindStat.HP_ADD, GrindStat.ATK_ADD, GrindStat.DEF_ADD,
            GrindStat.SPD}
