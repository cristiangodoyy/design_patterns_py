"""Clone configured computers with ``copy.copy`` (shallow prototype).

Pattern: Prototype (creational).
Counterpart: ``computer_before_prototype.py``; sibling variants
``computer_with_deep_copy_prototype.py`` and
``computer_with_registry_prototype.py``.

Notes
-----
Why:
    - The client gets a new, fully configured computer by asking an
      existing one to ``clone()`` itself; it no longer repeats every
      constructor argument or even needs the concrete class.
    - ``copy.copy`` is the cheapest clone: it creates a new object and
      fills it with *references* to the original's attributes.

When to use:
    - New objects are small variations of a configured one, and
      building them from scratch is verbose or expensive.
    - Every attribute is immutable (``str``, ``int``, tuples), so sharing
      references is harmless. ``Laptop`` is such a case.

Trade-offs:
    - Mutable parts are shared, not copied. ``Tower`` holds a
      ``MainBoard`` object, so changing the clone's board also changes
      the original's. The demo prints this surprise; the deep-copy
      variant removes it.
    - Each concrete class must implement ``clone()``.

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
                     MainBoard   <-- shared by original and clone
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

    Role in the pattern: component that a shallow copy shares.
    """

    manufacturer: str
    model: str


@dataclass
class Laptop(AbsComputer):
    """Laptop made only of immutable strings, so shallow copy is safe.

    Role in the pattern: ConcretePrototype.
    """

    model: str
    processor: str
    memory: str
    hard_drive: str
    graphics: str
    screen: str

    def clone(self) -> Self:
        """Return a shallow copy; every attribute is an immutable str."""
        return copy.copy(self)

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
        """Return a shallow copy.

        The new tower gets its own attributes, but ``mainboard`` still
        points to the original's ``MainBoard`` object.
        """
        return copy.copy(self)

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
    """Clone a laptop safely, then show a tower clone sharing its board."""
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
    tower_clone.mainboard.model = "Business"  # meant for T2 only
    print(tower.describe())
    print(tower_clone.describe())
    shared = tower_clone.mainboard is tower.mainboard
    print(f"T2 shares T1's MainBoard object: {shared}")
    print(
        f"Surprise: T1's mainboard is now {tower.mainboard.model!r}, "
        "although only T2 was changed."
    )


if __name__ == "__main__":
    client()
