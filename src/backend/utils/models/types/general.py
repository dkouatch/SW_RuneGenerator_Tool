from collections import Counter
from collections.abc import Hashable
from typing import TypeVar, Protocol

T = TypeVar('T', bound=Hashable)

class SortableHashable(Hashable, Protocol):
    def __lt__(self, other: object, /) -> bool: ...


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
