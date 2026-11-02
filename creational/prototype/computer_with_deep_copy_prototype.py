"""Clone configured computers with ``copy.deepcopy`` (deep prototype).

Pattern: Prototype (creational).
Counterpart: ``computer_before_prototype.py``; sibling variants
``computer_with_shallow_copy_prototype.py`` and
``computer_with_registry_prototype.py``.

Notes
-----
Why:
    - The client gets a new, fully configured computer by asking an
      existing one to ``clone()`` itself; it no longer repeats every
      constructor argument or even needs the concrete class.
    - ``copy.deepcopy`` copies the whole object graph, so the clone's
      ``MainBoard`` is a new object: changing it leaves the original
      untouched (the shallow variant's surprise is gone).
    - ``deepcopy`` keeps a memo of the objects it has already copied, so
      shared references and reference cycles are reproduced in the copy
      instead of causing infinite recursion.

When to use:
    - New objects are small variations of a configured one, and
      building them from scratch is verbose or expensive.
    - The prototype owns mutable parts (lists, dicts, nested objects)
      that each clone must be free to change independently.

Trade-offs:
    - It may copy too much: large or intentionally shared parts (a
      cache, a parent, a read-only catalog) are duplicated too.
    - Some objects cannot be copied at all: open files, sockets, locks
      and database connections raise ``TypeError`` or yield a broken
      copy.
    - Both are fixed by defining ``__deepcopy__(self, memo)`` on the
      class to choose what is copied, what is shared and what is
      recreated.
    - Slower than a shallow copy because it walks the whole graph.

Related:
    - Factory Method and Abstract Factory create objects from classes;
      Prototype creates them from configured instances.
    - Memento also copies state, but to restore it later, not to spawn
      new objects.

Roles::

    Client ---> AbsPrototype.clone()          (Prototype)
                      ^
                 AbsComputer
                      ^
              Laptop | Tower                  (ConcretePrototype)
                         |
                     MainBoard   <-- copied, one per tower
"""

import copy

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self


class AbsPrototype(ABC):
    """Object that can produce a copy of itself.

    Role in the pattern: Prototype.
    """

    @abstractmethod
    def clone(self) -> Self:
        """Return a new object configured like this one."""


class AbsComputer(AbsPrototype):
    """Computer that can be cloned and described.

    Role in the pattern: Prototype (domain interface).
    """

    model: str

    @abstractmethod
    def describe(self) -> str:
        """Return a printable spec sheet of the computer."""


def _spec_sheet(model: str, rows: list[tuple[str, str]]) -> str:
    """Return a printable spec sheet: a title line plus one aligned row each.

    Parameters
    ----------
    model : str
        Model name shown in the title.
    rows : list of tuple of (str, str)
        Label and value of each component, in display order.

    Returns
    -------
    str
        The spec sheet, one line per row.
    """
    lines = [f"Custom computer: {model}"]
    lines += [f"    {label:>10}: {value}" for label, value in rows]
    return "\n".join(lines)


@dataclass
class MainBoard:
    """Mutable part fitted inside a tower.

    Role in the pattern: component copied together with its tower.
    """

    manufacturer: str
    model: str


@dataclass
class Laptop(AbsComputer):
    """Laptop cloned with a deep copy, like every computer in this file.

    Role in the pattern: ConcretePrototype.
    """

    model: str
    processor: str
    memory: str
    hard_drive: str
    graphics: str
    screen: str

    def clone(self) -> Self:
        """Return a deep copy that shares no mutable state."""
        return copy.deepcopy(self)

    def describe(self) -> str:
        """Return the laptop's spec sheet, screen included."""
        return _spec_sheet(
            self.model,
            [
                ("Processor", self.processor),
                ("Memory", self.memory),
                ("Hard drive", self.hard_drive),
                ("Graphics", self.graphics),
                ("Screen", self.screen),
            ],
        )


@dataclass
class Tower(AbsComputer):
    """Desktop tower that owns a mutable ``MainBoard``.

    Role in the pattern: ConcretePrototype.
    """

    model: str
    mainboard: MainBoard
    processor: str
    memory: str
    hard_drive: str
    graphics: str
    monitor: str

    def clone(self) -> Self:
        """Return a deep copy with its own ``MainBoard``.

        ``copy.deepcopy`` recursively copies every attribute, using a
        memo so that objects referenced twice, or in a cycle, are copied
        only once.
        """
        return copy.deepcopy(self)

    def describe(self) -> str:
        """Return the tower's spec sheet, mainboard and monitor included."""
        board = f"{self.mainboard.manufacturer} {self.mainboard.model}"
        return _spec_sheet(
            self.model,
            [
                ("Mainboard", board),
                ("Processor", self.processor),
                ("Memory", self.memory),
                ("Hard drive", self.hard_drive),
                ("Graphics", self.graphics),
                ("Monitor", self.monitor),
            ],
        )


def client() -> None:
    """Clone a laptop and a tower, then customise each clone."""
    laptop = Laptop(
        model="L1",
        processor="Intel",
        memory="32GB",
        hard_drive="2TB SSD",
        graphics="onboard",
        screen="1920x1080",
    )
    laptop_clone = laptop.clone()
    laptop_clone.model = "L2"
    laptop_clone.processor = "AMD"
    print(laptop.describe())
    print(laptop_clone.describe())

    tower = Tower(
        model="T1",
        mainboard=MainBoard(manufacturer="ASUS", model="Game"),
        processor="AMD",
        memory="32GB",
        hard_drive="2TB SSD",
        graphics="onboard",
        monitor="1920x1080",
    )
    tower_clone = tower.clone()
    tower_clone.model = "T2"
    tower_clone.mainboard.model = "Business"
    print(tower.describe())
    print(tower_clone.describe())
    shared = tower_clone.mainboard is tower.mainboard
    print(f"T2 shares T1's MainBoard object: {shared}")
    print(f"T1's mainboard is still {tower.mainboard.model!r}.")


if __name__ == "__main__":
    client()
