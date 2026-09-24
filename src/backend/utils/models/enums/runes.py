from enum import Enum, unique

@unique
class RuneRarity(Enum):
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
class RuneGrade(Enum):
    ONE_STAR = 1
    TWO_STAR = 2
    THREE_STAR = 3
    FOUR_STAR = 4
    FIVE_STAR = 5
    SIX_STAR = 6

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


@unique
class RuneStat(Enum):
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
    NONE = 12

    def __str__(self):
        match self:
            case RuneStat.HP_ADD:
                return "HP"
            case RuneStat.HP_MUL:
                return "HP%"
            case RuneStat.ATK_ADD:
                return "ATK"
            case RuneStat.ATK_MUL:
                return "ATK%"
            case RuneStat.DEF_ADD:
                return "DEF"
            case RuneStat.DEF_MUL:
                return "DEF%"
            case RuneStat.SPD:
                return "SPD"
            case RuneStat.RES:
                return "RES"
            case RuneStat.ACC:
                return "ACC"
            case RuneStat.CR:
                return "CR"
            case RuneStat.CD:
                return "CD"
            case RuneStat.NONE:
                return "-"
    
    def __repr__(self):
        return str(self)
    
    def __bool__(self):
        return self != RuneStat.NONE
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        if not isinstance(other, RuneStat):
            return NotImplemented
        return self.value == other.value
    
    def __lt__(self, other):
        if not isinstance(other, RuneStat):
            return NotImplemented
        return self.value < other.value
    
    def __le__(self, other):
        if not isinstance(other, RuneStat):
            return NotImplemented
        return self.value <= other.value
    
    def __ge__(self, other):
        if not isinstance(other, RuneStat):
            return NotImplemented
        return self.value >= other.value
    
    def __gt__(self, other):
        if not isinstance(other, RuneStat):
            return NotImplemented
        return self.value > other.value
    
    @property
    def is_additive(self) -> bool:
        """Check if the stat property is additive."""
        return self in {
            RuneStat.HP_ADD, RuneStat.ATK_ADD, RuneStat.DEF_ADD,
            RuneStat.SPD}
    
    @property
    def prefix_descriptor(self) -> str:
        """Descriptor for the prefix stat property."""
        match self:
            case RuneStat.HP_ADD:
                return "Strong"
            case RuneStat.HP_MUL:
                return "Tenacious"
            case RuneStat.ATK_ADD:
                return "Ferocious"
            case RuneStat.ATK_MUL:
                return "Powerful"
            case RuneStat.DEF_ADD:
                return "Sturdy"
            case RuneStat.DEF_MUL:
                return "Durable"
            case RuneStat.SPD:
                return "Quick"
            case RuneStat.RES:
                return "Resistant"
            case RuneStat.ACC:
                return "Intricate"
            case RuneStat.CR:
                return "Mortal"
            case RuneStat.CD:
                return "Cruel"
            case RuneStat.NONE:
                return ""
