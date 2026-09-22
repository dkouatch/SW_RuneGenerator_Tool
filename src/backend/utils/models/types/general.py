from __future__ import annotations

from collections import Counter
from collections.abc import Hashable, Iterable, Mapping
from typing import TypeVar, Protocol, overload

T = TypeVar('T', bound=Hashable)

class SortableHashable(Hashable, Protocol):
    def __lt__(self, other: object, /) -> bool: ...


class HashableDict(Mapping):
    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)
        self._frozenset = frozenset(self._data)

    def __hash__(self):
        return hash(self._frozenset)
    
    def __eq__(self, other):
        if isinstance(other, HashableDict):
            return self._frozenset == other._frozenset
        return NotImplemented
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)


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
        return NotImplemented
    
    def __iter__(self):
        return iter(self.counter)

    def __add__(self, other: HashableCounter[T]) -> HashableCounter[T]:
        new_counter = self.counter + other.counter
        return HashableCounter[T](new_counter)
    
    def __radd__(self, other: HashableCounter[T]):
        return self.__add__(other)
    
    def __or__(self, other: HashableCounter[T]):
        return self.counter | other.counter
    
    @classmethod
    def from_counter(cls, counter: Counter[T]):
        return cls(counter.elements())
    
    def elements(self):
        return self.counter.elements()

    def most_common(self, n: int | None=None):
        return self.counter.most_common(n)
    
    def subtract(self, **kwargs):
        return NotImplemented
    
    def total(self):
        return self.counter.total()
    
    def update(self, **kwargs):
        return NotImplemented
