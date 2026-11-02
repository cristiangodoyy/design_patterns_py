"""Add car options at runtime by wrapping cars in decorators.

Pattern: Decorator (structural).
Counterpart: ``cars_before_decorator.py``.

Notes
-----
Why:
    - Each option is a decorator: an ``AbsCar`` that wraps another
      ``AbsCar`` and adds its own description and cost to the wrapped
      car's. Options stack in any order, one per category (paint,
      engine, upholstery).
    - Adding responsibilities happens per object, at runtime, without
      editing the trim classes or subclassing every combination.
    - 3 trims plus 6 options is 9 classes instead of one subclass per
      combination, and each option's cost lives in exactly one place.
    - Costs are integer cents, so adding options never accumulates
      floating-point rounding errors.

When to use:
    - You need to add responsibilities to individual objects
      dynamically and transparently, without affecting other objects.
    - Extending by subclassing is impractical because independent
      options would cause a subclass explosion.

Trade-offs:
    - Many small, similar-looking objects; a deep wrapper stack can be
      hard to debug.
    - Combination rules that subclassing enforced by construction (a
      car has one engine) must now be checked at runtime: wrapping a
      second option of the same category raises ``ValueError``.
    - A decorated car is not identical to the wrapped one, so code that
      relies on object identity or concrete type breaks.
    - Order can matter when decorators do more than add up values.

Related:
    - Adapter changes an object's interface; Decorator keeps it.
    - Composite also builds recursive structures, but with many
      children; a decorator has exactly one.
    - Strategy changes an object's guts; Decorator changes its skin.

Roles::

    AbsCar (Component)
      ^                  ^
    Economy | Luxury    AbsDecorator (Decorator) ---wraps---> AbsCar
    | Sport               ^
    (ConcreteComponent)  Black | Red | Inline4Cyl | V6 | Leather | Vinyl
                         (ConcreteDecorator, one category each)
"""

from abc import ABC, abstractmethod
from enum import StrEnum, auto
from typing import ClassVar


class OptionCategory(StrEnum):
    """Kinds of options; a car takes at most one option of each.

    Role in the pattern: rule data checked by the Decorator.
    """

    PAINT = auto()
    ENGINE = auto()
    UPHOLSTERY = auto()


class AbsCar(ABC):
    """Car that can describe itself and report its cost.

    Role in the pattern: Component.
    """

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description, including every option."""

    @property
    @abstractmethod
    def cost(self) -> int:
        """Total cost in US cents, including every option."""

    @property
    def categories(self) -> frozenset[OptionCategory]:
        """Option categories already fitted; a bare trim has none."""
        return frozenset()


class Economy(AbsCar):
    """Economy trim.

    Role in the pattern: ConcreteComponent.
    """

    @property
    def description(self) -> str:
        """The trim's name, ``"Economy"``."""
        return "Economy"

    @property
    def cost(self) -> int:
        """Base cost of the economy trim, in cents."""
        return 1_200_000


class Luxury(AbsCar):
    """Luxury trim.

    Role in the pattern: ConcreteComponent.
    """

    @property
    def description(self) -> str:
        """The trim's name, ``"Luxury"``."""
        return "Luxury"

    @property
    def cost(self) -> int:
        """Base cost of the luxury trim, in cents."""
        return 1_800_000


class Sport(AbsCar):
    """Sport trim.

    Role in the pattern: ConcreteComponent.
    """

    @property
    def description(self) -> str:
        """The trim's name, ``"Sport"``."""
        return "Sport"

    @property
    def cost(self) -> int:
        """Base cost of the sport trim, in cents."""
        return 1_500_000


class AbsDecorator(AbsCar):
    """Car option that wraps another car.

    Role in the pattern: Decorator.

    It keeps a reference to the wrapped component and has the same
    interface, so a decorated car can be wrapped again. By default it
    forwards every call unchanged; concrete options extend the results.

    Parameters
    ----------
    car : AbsCar
        Car to wrap, possibly already decorated.

    Raises
    ------
    ValueError
        If ``car`` already has an option of this decorator's category.
    """

    category: ClassVar[OptionCategory]

    def __init__(self, car: AbsCar) -> None:
        """Wrap ``car`` after checking its option categories."""
        if self.category in car.categories:
            raise ValueError(
                f"Cannot add {type(self).__name__}: {car.description!r} "
                f"already has one {self.category} option"
            )
        self._car = car

    @property
    def car(self) -> AbsCar:
        """The wrapped car, which may itself be decorated."""
        return self._car

    @property
    def description(self) -> str:
        """The wrapped car's description, unchanged."""
        return self._car.description

    @property
    def cost(self) -> int:
        """The wrapped car's cost, unchanged."""
        return self._car.cost

    @property
    def categories(self) -> frozenset[OptionCategory]:
        """The wrapped car's categories plus this option's."""
        return self._car.categories | {self.category}


class Black(AbsDecorator):
    """Midnight black paint.

    Role in the pattern: ConcreteDecorator.
    """

    category = OptionCategory.PAINT

    @property
    def description(self) -> str:
        """The wrapped car's description plus the midnight black paint."""
        return f"{super().description}, midnight black"

    @property
    def cost(self) -> int:
        """The wrapped car's cost plus the midnight black paint, in cents."""
        return super().cost + 180_000


class Red(AbsDecorator):
    """Ferrari red paint.

    Role in the pattern: ConcreteDecorator.
    """

    category = OptionCategory.PAINT

    @property
    def description(self) -> str:
        """The wrapped car's description plus the Ferrari red paint."""
        return f"{super().description}, Ferrari red"

    @property
    def cost(self) -> int:
        """The wrapped car's cost plus the Ferrari red paint, in cents."""
        return super().cost + 120_000


class Inline4Cyl(AbsDecorator):
    """Inline four-cylinder engine.

    Role in the pattern: ConcreteDecorator.
    """

    category = OptionCategory.ENGINE

    @property
    def description(self) -> str:
        """The wrapped car's description plus the inline-4 engine."""
        return f"{super().description}, inline 4 cylinder"

    @property
    def cost(self) -> int:
        """The wrapped car's cost plus the inline-4 engine, in cents."""
        return super().cost + 50_000


class V6(AbsDecorator):
    """V6 engine.

    Role in the pattern: ConcreteDecorator.
    """

    category = OptionCategory.ENGINE

    @property
    def description(self) -> str:
        """The wrapped car's description plus the V6 engine."""
        return f"{super().description}, V6"

    @property
    def cost(self) -> int:
        """The wrapped car's cost plus the V6 engine, in cents."""
        return super().cost + 220_000


class Leather(AbsDecorator):
    """Top-grain leather upholstery.

    Role in the pattern: ConcreteDecorator.
    """

    category = OptionCategory.UPHOLSTERY

    @property
    def description(self) -> str:
        """The wrapped car's description plus the leather upholstery."""
        return f"{super().description}, top-grain leather"

    @property
    def cost(self) -> int:
        """The wrapped car's cost plus the leather upholstery, in cents."""
        return super().cost + 270_000


class Vinyl(AbsDecorator):
    """Vinyl upholstery.

    Role in the pattern: ConcreteDecorator.
    """

    category = OptionCategory.UPHOLSTERY

    @property
    def description(self) -> str:
        """The wrapped car's description plus the vinyl upholstery."""
        return f"{super().description}, vinyl upholstery"

    @property
    def cost(self) -> int:
        """The wrapped car's cost plus the vinyl upholstery, in cents."""
        return super().cost + 50_000


def format_cents(cents: int) -> str:
    """Return ``cents`` formatted as dollars, for example ``$5.20``."""
    return f"${cents // 100}.{cents % 100:02d}"


def describe(car: AbsCar) -> str:
    """Return a printable line with the car's description and cost."""
    return f"Description: {car.description}; Cost: {format_cents(car.cost)}"


def client() -> None:
    """Wrap cars in options one at a time and print each stage."""
    car: AbsCar = Economy()
    print(describe(car))
    for option in (Inline4Cyl, Vinyl, Black):
        car = option(car)
        print(describe(car))

    print(describe(Red(Leather(V6(Sport())))))
    print(describe(Black(Leather(Luxury()))))

    try:
        V6(Inline4Cyl(Economy()))
    except ValueError as error:
        print(f"Rejected: {error}")


if __name__ == "__main__":
    client()
