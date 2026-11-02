"""Create cars through one factory class per car type.

Pattern: Factory Method (creational).
Counterpart: ``cars_before_factory.py``.
Step 3 of 3; previous: ``cars_with_simple_factory.py``.

Notes
-----
Why:
    - The simple factory of step 2 is limited to one factory that
      creates every product the same way. What if we need more factories
      for flexibility? The classic factory pattern is what we need.
    - ``AbsFactory`` declares the factory method ``create_auto``; there
      is one concrete factory per product type, and each one decides how
      its car is created. Implementations can vary freely, and a complex
      factory might even use other patterns, such as Builder.
    - ``AbsFactory.drive_new_car`` works with whatever car the subclass
      creates, so the creator's logic never names a concrete car.
    - The client picks a factory by name from a
      ``dict[str, type[AbsFactory]]``; no ``eval`` and no module
      introspection are needed.

When to use:
    - A class cannot anticipate which product class it must create, and
      wants its subclasses to decide.
    - Each product needs its own creation logic (configuration, naming,
      validation) rather than a bare constructor call.

Trade-offs:
    - One factory class per product type: many small classes.
    - An unknown factory name raises ``ValueError`` instead of returning
      a null object, so the caller must handle it; the error message
      lists the valid names.

Related:
    - Simple Factory (step 2) centralises creation in one class.
    - Abstract Factory groups several factory methods that create a
      family of related products.
    - Template Method: ``drive_new_car`` is a template method whose
      variable step is the factory method.

Roles::

    client ---> load_factory(name) ---> AbsFactory (Creator)
                                          create_auto()  <- factory method
                                          drive_new_car()
                                             ^
                 ChevyFactory | FordFactory | JeepFactory (ConcreteCreator)
                                    | creates
                                    v
          AbsAuto (Product) <- ChevyVolt | FordFusion | JeepSahara
                                       (ConcreteProduct)
"""

from abc import ABC, abstractmethod


class AbsAuto(ABC):
    """Interface every car must implement.

    Role in the pattern: Product.
    """

    def __init__(self, name: str) -> None:
        """Store the commercial name chosen by the factory.

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
        """Start the car and announce it."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the car and announce it."""


class ChevyVolt(AbsAuto):
    """Chevrolet electric car.

    Role in the pattern: ConcreteProduct.
    """

    def start(self) -> None:
        """Announce that the electric Volt starts."""
        print(f"{self.name} running with shocking power!")

    def stop(self) -> None:
        """Announce that the Volt shuts down."""
        print(f"{self.name} shutting down.")


class FordFusion(AbsAuto):
    """Ford mid-size sedan.

    Role in the pattern: ConcreteProduct.
    """

    def start(self) -> None:
        """Announce that the Fusion runs smoothly."""
        print(f"{self.name} running smoothly.")

    def stop(self) -> None:
        """Announce that the Fusion shuts down."""
        print(f"{self.name} shutting down.")


class JeepSahara(AbsAuto):
    """Jeep off-road vehicle.

    Role in the pattern: ConcreteProduct.
    """

    def start(self) -> None:
        """Announce that the Sahara runs ruggedly."""
        print(f"{self.name} running ruggedly.")

    def stop(self) -> None:
        """Announce that the Sahara shuts down."""
        print(f"{self.name} shutting down.")


class AbsFactory(ABC):
    """Declare the factory method that creates one type of car.

    Role in the pattern: Creator.
    """

    @abstractmethod
    def create_auto(self) -> AbsAuto:
        """Return a new car; each concrete factory decides which one."""

    def drive_new_car(self) -> AbsAuto:
        """Create a car with the factory method, then start and stop it.

        Returns
        -------
        AbsAuto
            The car that was driven.
        """
        car = self.create_auto()
        car.start()
        car.stop()
        return car


class ChevyFactory(AbsFactory):
    """Create Chevy Volt cars.

    Role in the pattern: ConcreteCreator.
    """

    def create_auto(self) -> AbsAuto:
        """Return a Chevy Volt with its commercial name."""
        return ChevyVolt("Chevy Volt")


class FordFactory(AbsFactory):
    """Create Ford Fusion cars.

    Role in the pattern: ConcreteCreator.
    """

    def create_auto(self) -> AbsAuto:
        """Return a Ford Fusion with its commercial name."""
        return FordFusion("Ford Fusion")


class JeepFactory(AbsFactory):
    """Create Jeep Sahara cars.

    Role in the pattern: ConcreteCreator.
    """

    def create_auto(self) -> AbsAuto:
        """Return a Jeep Sahara with its commercial name."""
        return JeepSahara("Jeep Sahara")


FACTORIES: dict[str, type[AbsFactory]] = {
    "chevy": ChevyFactory,
    "ford": FordFactory,
    "jeep": JeepFactory,
}


def load_factory(factory_name: str) -> AbsFactory:
    """Find and instantiate the factory registered as ``factory_name``.

    Parameters
    ----------
    factory_name : str
        Key of the factory in ``FACTORIES``, for example ``"ford"``.

    Returns
    -------
    AbsFactory
        A new instance of the matching factory.

    Raises
    ------
    ValueError
        If no factory is registered under ``factory_name``.
    """
    factory_class = FACTORIES.get(factory_name)
    if factory_class is None:
        known = ", ".join(sorted(FACTORIES))
        raise ValueError(
            f"Unknown factory {factory_name!r}; expected one of: {known}"
        )
    return factory_class()


def client() -> None:
    """Test-drive one car from each factory, then ask for an unknown one."""
    for factory_name in FACTORIES:
        load_factory(factory_name).drive_new_car()
    try:
        load_factory("tesla")
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    client()
