from enum import Enum, unique

@unique
class RuneGrade(Enum):
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


from enum import Enum, unique

@unique
class RuneProperty(Enum):
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
        match self:
            case RuneProperty.HP_ADD:
                return "HP"
            case RuneProperty.HP_MUL:
                return "HP%"
            case RuneProperty.ATK_ADD:
                return "ATK"
            case RuneProperty.ATK_MUL:
                return "ATK%"
            case RuneProperty.DEF_ADD:
                return "DEF"
            case RuneProperty.DEF_MUL:
                return "DEF%"
            case RuneProperty.SPD:
                return "SPD"
            case RuneProperty.RES:
                return "RES"
            case RuneProperty.ACC:
                return "ACC"
            case RuneProperty.CR:
                return "CR"
            case RuneProperty.CD:
                return "CD"
            case RuneProperty.NO_PROPERTY:
                return "-"
    
    def __repr__(self):
        return str(self)
    
    def __bool__(self):
        return self != RuneProperty.NO_PROPERTY
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        if not isinstance(other, RuneProperty):
            return NotImplemented
        return self.value == other.value
    
    def __lt__(self, other):
        if not isinstance(other, RuneProperty):
            return NotImplemented
        return self.value < other.value
    
    def __le__(self, other):
        if not isinstance(other, RuneProperty):
            return NotImplemented
        return self.value <= other.value
    
    def __ge__(self, other):
        if not isinstance(other, RuneProperty):
            return NotImplemented
        return self.value >= other.value
    
    def __gt__(self, other):
        if not isinstance(other, RuneProperty):
            return NotImplemented
        return self.value > other.value
    
    @property
    def is_additive(self) -> bool:
        """Check if the stat property is additive."""
        return self in {
            RuneProperty.HP_ADD, RuneProperty.ATK_ADD, RuneProperty.DEF_ADD,
            RuneProperty.SPD}
    
    @property
    def prefix_descriptor(self) -> str:
        """Descriptor for the prefix stat property."""
        match self:
            case RuneProperty.HP_ADD:
                return "Strong"
            case RuneProperty.HP_MUL:
                return "Tenacious"
            case RuneProperty.ATK_ADD:
                return "Ferocious"
            case RuneProperty.ATK_MUL:
                return "Powerful"
            case RuneProperty.DEF_ADD:
                return "Sturdy"
            case RuneProperty.DEF_MUL:
                return "Durable"
            case RuneProperty.SPD:
                return "Quick"
            case RuneProperty.RES:
                return "Resistant"
            case RuneProperty.ACC:
                return "Intricate"
            case RuneProperty.CR:
                return "Mortal"
            case RuneProperty.CD:
                return "Cruel"
            case RuneProperty.NO_PROPERTY:
                return ""
