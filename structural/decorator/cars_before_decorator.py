"""Model car trims with a plain class hierarchy, before adding options.

Pattern: Decorator (structural), problem side.
Counterpart: ``cars_with_decorator.py``.

Notes
-----
Scenario:
    A dealer sells three trims: economy, luxury and sport. Each trim
    is a subclass of ``AbsCar`` with its own description and cost.
    Customers now want options on top of any trim: paint color, engine
    and upholstery, each adding to the description and the cost.

What goes wrong here:
    - With inheritance, every combination of options is a new class:
      ``EconomyBlackV6Leather``, ``SportRedInline4Vinyl``... With 3
      trims, 2 colors, 2 engines and 2 upholsteries that is already
      3 x 2 x 2 x 2 = 24 subclasses, and each new option doubles it.
    - The cost of an option (say, black paint) is repeated in every
      class that includes it.
    - Options are fixed when the class is written; they cannot be added
      to an existing car object at runtime.

Roles::

    AbsCar (description, cost)
      ^         ^         ^
    Economy   Luxury    Sport     (+ one subclass per option combination)
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable


class AbsCar(ABC):
    """Car that can describe itself and report its cost."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of the car."""

    @property
    @abstractmethod
    def cost(self) -> int:
        """Cost of the car in US cents."""


class Economy(AbsCar):
    """Economy trim."""

    @property
    def description(self) -> str:
        """The trim's name, ``"Economy"``."""
        return "Economy"

    @property
    def cost(self) -> int:
        """Base cost of the economy trim, in cents."""
        return 1_200_000


class Luxury(AbsCar):
    """Luxury trim."""

    @property
    def description(self) -> str:
        """The trim's name, ``"Luxury"``."""
        return "Luxury"

    @property
    def cost(self) -> int:
        """Base cost of the luxury trim, in cents."""
        return 1_800_000


class Sport(AbsCar):
    """Sport trim."""

    @property
    def description(self) -> str:
        """The trim's name, ``"Sport"``."""
        return "Sport"

    @property
    def cost(self) -> int:
        """Base cost of the sport trim, in cents."""
        return 1_500_000


def format_cents(cents: int) -> str:
    """Return ``cents`` formatted as dollars, for example ``$5.20``."""
    return f"${cents // 100}.{cents % 100:02d}"


def describe(cars: Iterable[AbsCar]) -> list[str]:
    """Return one printable line per car.

    Parameters
    ----------
    cars : Iterable of AbsCar
        Cars to describe.

    Returns
    -------
    list of str
        Description and cost of each car.
    """
    return [
        f"Description: {car.description}; Cost: {format_cents(car.cost)}"
        for car in cars
    ]


def client() -> None:
    """Print each trim without any options."""
    for line in describe((Economy(), Luxury(), Sport())):
        print(line)


if __name__ == "__main__":
    client()
