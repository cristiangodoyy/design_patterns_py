"""Build families of cars through one factory per manufacturer.

Pattern: Abstract Factory (creational).
Counterpart: ``cars_before_abstract_factory.py``.

Notes
-----
Why:
    - Each manufacturer is a concrete factory that makes a whole family
      of related products (economy, sport and luxury editions), so the
      client can never mix a Ford car with a GM one by accident.
    - The client depends only on ``AbsFactory`` and ``AbsCar``; it never
      names a concrete car class (dependency inversion).
    - A new manufacturer is a new factory class plus one entry in
      ``FACTORIES``; existing factories and the client do not change
      (open/closed).
    - The factory is chosen at runtime from a ``dict[Maker,
      AbsFactory]``, for example from configuration or user input.
      Each factory is created once and reused.

When to use:
    - The system must work with several families of related products
      and the products of one family are meant to be used together.
    - You want to swap the whole family at once (a manufacturer, a UI
      theme, a database vendor) without touching client code.

Trade-offs:
    - Adding a new kind of product (say, a pickup edition) is expensive:
      ``AbsFactory`` and every concrete factory must change.
    - More classes than a simple ``if/elif``; overkill for one family.

Related:
    - Each ``create_*`` method is a Factory Method.
    - Concrete factories are often Singletons; Builder can be used when
      a product needs a step-by-step assembly instead.

Roles::

    client --uses--> AbsFactory (AbstractFactory)
                         ^
             FordFactory | GeneralMotorsFactory (ConcreteFactory)
                         |
                      creates
                         v
                     AbsCar (AbstractProduct)
                         ^
        Fiesta | Mustang | LincolnMKS       <- Ford family
        Spark  | Camaro  | CadillacCTS      <- GM family
                  (ConcreteProduct)
"""

from abc import ABC, abstractmethod
from enum import StrEnum, auto


class Maker(StrEnum):
    """Car manufacturers that have a factory.

    Role in the pattern: key that selects the ConcreteFactory.
    """

    GM = auto()
    FORD = auto()


class AbsCar(ABC):
    """Interface shared by every car of every manufacturer.

    Role in the pattern: AbstractProduct.
    """

    def __init__(self, name: str) -> None:
        """Store the commercial name shared by every edition.

        Parameters
        ----------
        name : str
            Commercial name of the car model.
        """
        self._name = name

    @property
    def name(self) -> str:
        """Commercial name of the car model."""
        return self._name

    @abstractmethod
    def start(self) -> None:
        """Start the engine and announce it."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the engine and announce it."""


class FordFiesta(AbsCar):
    """Ford economy car.

    Role in the pattern: ConcreteProduct.
    """

    def __init__(self) -> None:
        """Create the car under its commercial name, "Ford Fiesta"."""
        super().__init__("Ford Fiesta")

    def start(self) -> None:
        """Announce that the Fiesta runs cheaply."""
        print(f"{self.name} running cheaply.")

    def stop(self) -> None:
        """Announce that the Fiesta shuts down."""
        print(f"{self.name} shutting down.")


class FordMustang(AbsCar):
    """Ford sport car.

    Role in the pattern: ConcreteProduct.
    """

    def __init__(self) -> None:
        """Create the car under its commercial name, "Ford Mustang"."""
        super().__init__("Ford Mustang")

    def start(self) -> None:
        """Announce that the Mustang roars to life."""
        print(f"{self.name} roaring and ready to go!")

    def stop(self) -> None:
        """Announce that the Mustang shuts down."""
        print(f"{self.name} shutting down.")


class LincolnMKS(AbsCar):
    """Ford luxury car.

    Role in the pattern: ConcreteProduct.
    """

    def __init__(self) -> None:
        """Create the car under its commercial name, "Lincoln MKS"."""
        super().__init__("Lincoln MKS")

    def start(self) -> None:
        """Announce that the Lincoln runs smoothly."""
        print(f"{self.name} running smoothly.")

    def stop(self) -> None:
        """Announce that the Lincoln shuts down."""
        print(f"{self.name} shutting down.")


class ChevySpark(AbsCar):
    """General Motors economy car.

    Role in the pattern: ConcreteProduct.
    """

    def __init__(self) -> None:
        """Create the car under its commercial name, "Chevy Spark"."""
        super().__init__("Chevy Spark")

    def start(self) -> None:
        """Announce that the Spark runs efficiently."""
        print(f"{self.name} running efficiently.")

    def stop(self) -> None:
        """Announce that the Spark shuts down."""
        print(f"{self.name} shutting down.")


class ChevyCamaro(AbsCar):
    """General Motors sport car.

    Role in the pattern: ConcreteProduct.
    """

    def __init__(self) -> None:
        """Create the car under its commercial name, "Chevy Camaro"."""
        super().__init__("Chevy Camaro")

    def start(self) -> None:
        """Announce that the Camaro's V8 starts."""
        print(f"{self.name} V8 sounding awesome!")

    def stop(self) -> None:
        """Announce that the Camaro shuts down."""
        print(f"{self.name} shutting down.")


class CadillacCTS(AbsCar):
    """General Motors luxury car.

    Role in the pattern: ConcreteProduct.
    """

    def __init__(self) -> None:
        """Create the car under its commercial name, "Cadillac CTS"."""
        super().__init__("Cadillac CTS")

    def start(self) -> None:
        """Announce that the Cadillac purrs luxuriously."""
        print(f"{self.name} purring luxuriously.")

    def stop(self) -> None:
        """Announce that the Cadillac shuts down."""
        print(f"{self.name} shutting down.")


class AbsFactory(ABC):
    """Make the economy, sport and luxury editions of one manufacturer.

    Every concrete factory produces one family; the client picks the
    family by picking the factory.

    Role in the pattern: AbstractFactory.
    """

    @abstractmethod
    def create_economy(self) -> AbsCar:
        """Return a new economy-edition car."""

    @abstractmethod
    def create_sport(self) -> AbsCar:
        """Return a new sport-edition car."""

    @abstractmethod
    def create_luxury(self) -> AbsCar:
        """Return a new luxury-edition car."""


class FordFactory(AbsFactory):
    """Make the Ford family of cars.

    Role in the pattern: ConcreteFactory.
    """

    def create_economy(self) -> AbsCar:
        """Return a Ford Fiesta, Ford's economy edition."""
        return FordFiesta()

    def create_sport(self) -> AbsCar:
        """Return a Ford Mustang, Ford's sport edition."""
        return FordMustang()

    def create_luxury(self) -> AbsCar:
        """Return a Lincoln MKS, Ford's luxury edition."""
        return LincolnMKS()


class GeneralMotorsFactory(AbsFactory):
    """Make the General Motors family of cars.

    Role in the pattern: ConcreteFactory.
    """

    def create_economy(self) -> AbsCar:
        """Return a Chevy Spark, GM's economy edition."""
        return ChevySpark()

    def create_sport(self) -> AbsCar:
        """Return a Chevy Camaro, GM's sport edition."""
        return ChevyCamaro()

    def create_luxury(self) -> AbsCar:
        """Return a Cadillac CTS, GM's luxury edition."""
        return CadillacCTS()


FACTORIES: dict[Maker, AbsFactory] = {
    Maker.FORD: FordFactory(),
    Maker.GM: GeneralMotorsFactory(),
}


def factory_for(maker: Maker | str) -> AbsFactory:
    """Return the factory for ``maker``, chosen at runtime.

    Parameters
    ----------
    maker : Maker or str
        Manufacturer, or its key as read from configuration, such as
        ``"ford"`` or ``"gm"``.

    Returns
    -------
    AbsFactory
        Shared factory that makes that manufacturer's family of cars.

    Raises
    ------
    ValueError
        If no factory is registered for ``maker``.
    """
    try:
        return FACTORIES[Maker(maker)]
    except ValueError as exc:
        known = ", ".join(sorted(FACTORIES))
        raise ValueError(
            f"Unknown maker {maker!r}; expected one of: {known}"
        ) from exc


def drive_lineup(factory: AbsFactory) -> None:
    """Start and stop every edition made by ``factory``.

    This is the client code: it only knows the abstract interfaces.

    Parameters
    ----------
    factory : AbsFactory
        Factory of the family to drive.
    """
    for car in (
        factory.create_economy(),
        factory.create_sport(),
        factory.create_luxury(),
    ):
        car.start()
        car.stop()


def client() -> None:
    """Drive the whole lineup of each manufacturer."""
    for maker in (Maker.FORD, Maker.GM):
        drive_lineup(factory_for(maker))


if __name__ == "__main__":
    client()
