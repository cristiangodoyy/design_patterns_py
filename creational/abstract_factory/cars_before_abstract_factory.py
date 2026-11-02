"""Pick a car from nested if/elif chains over maker and edition.

Pattern: Abstract Factory (creational), problem side.
Counterpart: ``cars_with_abstract_factory.py``.

Notes
-----
Scenario:
    A dealership sells cars from two manufacturers, Ford and General
    Motors, and each manufacturer offers an economy, a sport and a
    luxury edition. The client must hand out the right car for every
    maker/edition combination.

What goes wrong here:
    - The client knows every concrete car class; ``Car`` is just the
      union of all of them, so it grows with each new model.
    - Open/closed: a new maker or a new edition means editing the nested
      ``if/elif`` chain in ``make_car``.
    - Nothing groups the cars by family, so the client can mix a Ford
      economy car with a GM luxury car by mistake.
    - Dependency inversion: the client depends on implementations, not
      on an abstraction of "a car" or "a manufacturer".

Roles::

    make_car(maker, edition)
      if GM:   Spark | Camaro | CadillacCTS
      if FORD: Fiesta | Mustang | LincolnMKS
      (client instantiates every concrete class itself)
"""

from enum import StrEnum, auto


class Maker(StrEnum):
    """Car manufacturers known to the client."""

    GM = auto()
    FORD = auto()


class Edition(StrEnum):
    """Editions every manufacturer offers."""

    ECONOMY = auto()
    SPORT = auto()
    LUXURY = auto()


class FordFiesta:
    """Ford economy car."""

    def start(self) -> None:
        """Announce that the Fiesta runs cheaply."""
        print("Ford Fiesta running cheaply.")

    def stop(self) -> None:
        """Announce that the Fiesta shuts down."""
        print("Ford Fiesta shutting down.")


class FordMustang:
    """Ford sport car."""

    def start(self) -> None:
        """Announce that the Mustang roars to life."""
        print("Ford Mustang roaring and ready to go!")

    def stop(self) -> None:
        """Announce that the Mustang shuts down."""
        print("Ford Mustang shutting down.")


class LincolnMKS:
    """Ford luxury car."""

    def start(self) -> None:
        """Announce that the Lincoln runs smoothly."""
        print("Lincoln MKS running smoothly.")

    def stop(self) -> None:
        """Announce that the Lincoln shuts down."""
        print("Lincoln MKS shutting down.")


class ChevySpark:
    """General Motors economy car."""

    def start(self) -> None:
        """Announce that the Spark runs efficiently."""
        print("Chevy Spark running efficiently.")

    def stop(self) -> None:
        """Announce that the Spark shuts down."""
        print("Chevy Spark shutting down.")


class ChevyCamaro:
    """General Motors sport car."""

    def start(self) -> None:
        """Announce that the Camaro's V8 starts."""
        print("Chevy Camaro V8 sounding awesome!")

    def stop(self) -> None:
        """Announce that the Camaro shuts down."""
        print("Chevy Camaro shutting down.")


class CadillacCTS:
    """General Motors luxury car."""

    def start(self) -> None:
        """Announce that the Cadillac purrs luxuriously."""
        print("Cadillac CTS purring luxuriously.")

    def stop(self) -> None:
        """Announce that the Cadillac shuts down."""
        print("Cadillac CTS shutting down.")


# The only "common type" is the list of every concrete class: adding a
# model means editing this alias as well as ``make_car``.
type Car = (
    FordFiesta
    | FordMustang
    | LincolnMKS
    | ChevySpark
    | ChevyCamaro
    | CadillacCTS
)


def make_car(maker: Maker, edition: Edition) -> Car:
    """Instantiate the concrete car for ``maker`` and ``edition``.

    Parameters
    ----------
    maker : Maker
        Manufacturer that builds the car.
    edition : Edition
        Edition requested by the customer.

    Returns
    -------
    Car
        A new instance of the matching concrete class.

    Raises
    ------
    ValueError
        If the combination has no branch yet.
    """
    if maker == Maker.GM:
        if edition == Edition.ECONOMY:
            return ChevySpark()
        if edition == Edition.SPORT:
            return ChevyCamaro()
        if edition == Edition.LUXURY:
            return CadillacCTS()
    if maker == Maker.FORD:
        if edition == Edition.ECONOMY:
            return FordFiesta()
        if edition == Edition.SPORT:
            return FordMustang()
        if edition == Edition.LUXURY:
            return LincolnMKS()
    raise ValueError(f"Unknown car: maker={maker}, edition={edition}")


def client() -> None:
    """Start and stop one car per maker/edition combination."""
    for maker in Maker:
        for edition in Edition:
            car = make_car(maker, edition)
            car.start()
            car.stop()


if __name__ == "__main__":
    client()
