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
        match self:
            case StatProperty.HP_ADD:
                return "HP"
            case StatProperty.HP_MUL:
                return "HP%"
            case StatProperty.ATK_ADD:
                return "ATK"
            case StatProperty.ATK_MUL:
                return "ATK%"
            case StatProperty.DEF_ADD:
                return "DEF"
            case StatProperty.DEF_MUL:
                return "DEF%"
            case StatProperty.SPD:
                return "SPD"
            case StatProperty.RES:
                return "RES"
            case StatProperty.ACC:
                return "ACC"
            case StatProperty.CR:
                return "CR"
            case StatProperty.CD:
                return "CD"
            case StatProperty.NO_PROPERTY:
                return "-"
    
    def __repr__(self):
        return str(self)
    
    def __bool__(self):
        return self != StatProperty.NO_PROPERTY
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        if not isinstance(other, StatProperty):
            return NotImplemented
        return self.value == other.value
    
    def __lt__(self, other):
        if not isinstance(other, StatProperty):
            return NotImplemented
        return self.value < other.value
    
    def __le__(self, other):
        if not isinstance(other, StatProperty):
            return NotImplemented
        return self.value <= other.value
    
    def __ge__(self, other):
        if not isinstance(other, StatProperty):
            return NotImplemented
        return self.value >= other.value
    
    def __gt__(self, other):
        if not isinstance(other, StatProperty):
            return NotImplemented
        return self.value > other.value
    
    @property
    def is_additive(self) -> bool:
        """Check if the stat property is additive."""
        return self in {
            StatProperty.HP_ADD, StatProperty.ATK_ADD, StatProperty.DEF_ADD,
            StatProperty.SPD}
    
    @property
    def prefix_descriptor(self) -> str:
        """Descriptor for the prefix stat property."""
        match self:
            case StatProperty.HP_ADD:
                return "Strong"
            case StatProperty.HP_MUL:
                return "Tenacious"
            case StatProperty.ATK_ADD:
                return "Ferocious"
            case StatProperty.ATK_MUL:
                return "Powerful"
            case StatProperty.DEF_ADD:
                return "Sturdy"
            case StatProperty.DEF_MUL:
                return "Durable"
            case StatProperty.SPD:
                return "Quick"
            case StatProperty.RES:
                return "Resistant"
            case StatProperty.ACC:
                return "Intricate"
            case StatProperty.CR:
                return "Mortal"
            case StatProperty.CD:
                return "Cruel"
            case StatProperty.NO_PROPERTY:
                return ""
