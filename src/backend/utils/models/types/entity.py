import math
from typeguard import typechecked
from typing import Any

from src.backend.utils.models.types.event import *
from abc import ABC

class Entity(ABC):
    def __init__(self, events):
        self._events: dict[str, Event] = events

    @property
    def events(self) -> list[Event]:
        return list(self._events.values())

    @property
    def probability(self) -> int | float:
        return math.prod(event.probability for event in self.events)
    
    @property
    def likelihood(self) -> int | float:
        return 1.0 / self.probability
    
    def query(self, key: str) -> tuple:
        """Queries the outcome and probability of an event from the internal dictionary.

        Args:
            key (str): Key (e.g, "stars", "slot", etc.)
        Returns:
            (outcome, probability)
        Raises:
            KeyError: Key does not exist in internal dictionary of Event objects
        """
        if key not in self._events.keys():
            raise KeyError(f"Key '{key}' does not exist.")
        event = self._events[key]
        return event.outcome, event.probability
    
    def uncondition(self, key: str) -> None:
        """Unconditions an event by querying the internal dictionary.

        Args:
            key (str): Key (e.g, "stars", "slot", etc.)
        Raises:
            KeyError: Key does not exist in internal dictionary of Event objects
        """
        if key not in self._events.keys():
            raise KeyError(f"Key '{key}' does not exist.")
        self._events[key].uncondition()
    
    def condition(self, key: str, f: Callable[[Any], bool] | None=None) -> None:
        """Conditions an event by querying the internal dictionary.

        Args:
            key (str): Key (e.g, "stars", "slot", etc.)
        Raises:
            KeyError: Key does not exist in internal dictionary of Event objects
        """
        if key not in self._events.keys():
            raise KeyError(f"Key '{key}' does not exist.")
        self._events[key].condition(f)  # pyright: ignore[reportArgumentType]
    
    def reset(self) -> None:
        """Unconditions all events
        """
        for event in self.events:
            event.uncondition()
    
    def condition_all(self) -> None:
        """Conditions all events
        """
        for event in self.events:
            event.condition()
