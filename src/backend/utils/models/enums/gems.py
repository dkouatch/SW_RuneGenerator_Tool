from enum import Enum, unique

@unique
class GemGrade(Enum):
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
class GemSet(Enum):
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
class GemProperty(Enum):
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

    def __str__(self):
        match self:
            case GemProperty.HP_ADD:
                return "HP"
            case GemProperty.HP_MUL:
                return "HP%"
            case GemProperty.ATK_ADD:
                return "ATK"
            case GemProperty.ATK_MUL:
                return "ATK%"
            case GemProperty.DEF_ADD:
                return "DEF"
            case GemProperty.DEF_MUL:
                return "DEF%"
            case GemProperty.SPD:
                return "SPD"
            case GemProperty.RES:
                return "RES"
            case GemProperty.ACC:
                return "ACC"
            case GemProperty.CR:
                return "CR"
            case GemProperty.CD:
                return "CD"
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        if not isinstance(other, GemProperty):
            return NotImplemented
        return self.value == other.value
    
    def __lt__(self, other):
        if not isinstance(other, GemProperty):
            return NotImplemented
        return self.value < other.value
    
    def __le__(self, other):
        if not isinstance(other, GemProperty):
            return NotImplemented
        return self.value <= other.value
    
    def __ge__(self, other):
        if not isinstance(other, GemProperty):
            return NotImplemented
        return self.value >= other.value
    
    def __gt__(self, other):
        if not isinstance(other, GemProperty):
            return NotImplemented
        return self.value > other.value
    
    @property
    def is_additive(self) -> bool:
        """Check if the stat property is additive."""
        return self in {
            GemProperty.HP_ADD, GemProperty.ATK_ADD, GemProperty.DEF_ADD,
            GemProperty.SPD}
