from collections import Counter
from collections.abc import Hashable, Sequence
from enum import Enum, unique
from typing import TypeVar, Protocol

from src.backend.utils.models.enums.stats import StatProperty

T = TypeVar('T', bound=Hashable)

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

class HashableCounter[T]:
    def __init__(self, *args, **kwargs):
        self.counter = Counter[T](*args, **kwargs)
    
    def __hash__(self) -> int:
        return hash(frozenset(self.counter.items()))
    
    def __eq__(self, other):
        if isinstance(other, HashableCounter):
            return self.counter == other.counter
        elif isinstance(other, Counter):
            return self.counter == other
        else:
            return NotImplemented
    
    def __repr__(self):
        return f"HashableCounter({repr(self.counter)})"
    
    def __getitem__(self, key):
        return self.counter[key]
    
    def __setitem__(self, key, value):
        self.counter[key] = value
    
    def __iter__(self):
        return iter(self.counter)
    
    def __add__(self, other):
        if isinstance(other, HashableCounter):
            new_counter = self.counter + other.counter
            return HashableCounter[T](new_counter)
        elif isinstance(other, Counter):
            new_counter = self.counter + other
            return HashableCounter[T](new_counter)
        else:
            return NotImplemented
    
    def __radd__(self, other):
        if isinstance(other, HashableCounter):
            new_counter = self.counter + other.counter
            return HashableCounter[T](new_counter)
        elif isinstance(other, Counter):
            new_counter = self.counter + other
            return HashableCounter[T](new_counter)
        else:
            return NotImplemented

Upgrade = HashableCounter[StatProperty]
