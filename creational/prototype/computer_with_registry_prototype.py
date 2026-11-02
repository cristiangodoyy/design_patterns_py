"""Clone pre-configured computers by name from a prototype registry.

Pattern: Prototype (creational), registry (prototype manager) variant.
Counterpart: ``computer_before_prototype.py``; sibling variants
``computer_with_shallow_copy_prototype.py`` and
``computer_with_deep_copy_prototype.py``.

Notes
-----
Why:
    - Clients ask for "a gaming-tower" by name and receive a fresh,
      fully configured copy; they never see the concrete classes or the
      constructor arguments.
    - The catalogue of prototypes can grow at runtime (``register``)
      without touching any client code.
    - The registry validates what goes in, so every stored object is
      guaranteed to support ``clone()``.

When to use:
    - The set of available configurations is dynamic (loaded from
      settings, plugins or user presets).
    - Many clients need copies of the same few configured objects.

Trade-offs:
    - Names are strings: a typo is only detected at runtime, so the
      registry raises a ``KeyError`` that lists the known names.
    - Clones are deep copies (see the deep-copy variant for the cost of
      copying too much or copying uncopyable resources).
    - The registry is one more object to create, fill and pass around.

Related:
    - Abstract Factory can be implemented as a registry of prototypes,
      one per product.
    - Flyweight also keeps a keyed pool, but hands out the *shared*
      object instead of a copy.

Roles::

    Client ---> PrototypeManager.clone(name)     (prototype manager)
                       |
                       v  prototype.clone()
                 AbsPrototype                    (Prototype)
                       ^
                  AbsComputer
                       ^
               Laptop | Tower                    (ConcretePrototype)
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
    """Laptop preset stored in the registry.

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
    """Tower preset stored in the registry.

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
        """Return a deep copy with its own ``MainBoard``."""
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


class PrototypeManager[P: AbsPrototype]:
    """Keep named prototypes and hand out clones of them.

    The registry wraps a private dictionary instead of subclassing
    ``dict``: subclassing would expose ``update``, ``|=``, ``setdefault``
    and friends, which bypass any validation added to ``__setitem__``.

    Role in the pattern: prototype manager (registry).

    Parameters
    ----------
    kind : type of AbsPrototype
        Prototype type accepted by ``register`` and returned by
        ``clone``, e.g. ``AbsComputer``.
    """

    def __init__(self, kind: type[P]) -> None:
        """Start empty; ``register`` accepts only instances of ``kind``."""
        self._kind = kind
        self._prototypes: dict[str, P] = {}

    def register(self, name: str, prototype: object) -> None:
        """Store ``prototype`` under ``name``, replacing any previous one.

        Parameters
        ----------
        name : str
            Key clients will use to ask for clones.
        prototype : object
            Configured instance to copy from. It is checked at runtime,
            so callers that bypass static typing cannot slip in an
            object without ``clone()``.

        Raises
        ------
        TypeError
            If ``prototype`` is not an instance of the registry's kind.
        """
        if not isinstance(prototype, self._kind):
            raise TypeError(
                f"Cannot register {name!r}: expected an instance of "
                f"{self._kind.__name__}, got {type(prototype).__name__}."
            )
        self._prototypes[name] = prototype

    def clone(self, name: str) -> P:
        """Return a fresh clone of the prototype stored as ``name``.

        The copy is whatever the prototype's ``clone()`` returns; every
        preset in this module clones itself with a deep copy.

        Parameters
        ----------
        name : str
            Name used when the prototype was registered.

        Returns
        -------
        P
            New object equal to, but independent from, the prototype.

        Raises
        ------
        KeyError
            If no prototype was registered under ``name``.
        """
        try:
            prototype = self._prototypes[name]
        except KeyError:
            known = ", ".join(self.names()) or "none"
            raise KeyError(
                f"No prototype named {name!r}. Registered names: {known}. "
                "Call register() first."
            ) from None
        return prototype.clone()

    def names(self) -> list[str]:
        """Return the registered names in alphabetical order."""
        return sorted(self._prototypes)

    def __contains__(self, name: object) -> bool:
        """Return whether a prototype is registered under ``name``."""
        return name in self._prototypes


def client() -> None:
    """Fill a registry with presets, clone them and customise the clones."""
    manager = PrototypeManager(AbsComputer)
    manager.register(
        "office-laptop",
        Laptop(
            model="L1",
            processor="Intel",
            memory="32GB",
            hard_drive="2TB SSD",
            graphics="onboard",
            screen="1920x1080",
        ),
    )
    manager.register(
        "gaming-tower",
        Tower(
            model="T1",
            mainboard=MainBoard(manufacturer="ASUS", model="Game"),
            processor="AMD",
            memory="32GB",
            hard_drive="2TB SSD",
            graphics="onboard",
            monitor="1920x1080",
        ),
    )
    print(f"Presets: {', '.join(manager.names())}")

    laptop = manager.clone("office-laptop")
    laptop.model = "L2"
    print(laptop.describe())

    tower = manager.clone("gaming-tower")
    tower.model = "T2"
    print(tower.describe())
    print("Preset untouched:")
    print(manager.clone("gaming-tower").describe())

    try:
        manager.clone("server")
    except KeyError as error:
        print(f"KeyError: {error.args[0]}")
    try:
        manager.register("toaster", "not a computer")
    except TypeError as error:
        print(f"TypeError: {error}")


if __name__ == "__main__":
    client()
