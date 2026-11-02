"""Create cars by name through one factory with an explicit registry.

Pattern: Simple Factory (creational).
Counterpart: ``cars_before_factory.py``.
Step 2 of 3; previous: ``cars_before_factory.py``;
next: ``cars_with_factory_method.py``.

Notes
-----
Why:
    - ``AutoFactory`` encapsulates class instantiation: it maps each car
      name to its class and returns a new instance, so the long
      ``if/elif`` chain of step 1 is gone.
    - Open/closed: adding a car is a new ``AbsAuto`` subclass plus one
      ``register`` call where the factory is assembled
      (``default_auto_factory``); ``AutoFactory`` itself never changes.
    - Dependency inversion: the client depends on the ``AbsAuto``
      abstraction and only knows car *names*; it never imports or
      instantiates a concrete car class.
    - Unknown names return a ``NullCar`` (Null Object), so the client
      never has to test for ``None``. ``NullCar`` is deliberately not
      registered: it is the fallback, not a model you can order.
    - The registry belongs to each factory instance, so two factories
      never share or leak registrations.

When to use:
    - The class to instantiate is chosen at runtime from a key such as a
      name read from configuration, a command line or a request.
    - You want one place that knows how to create every product.

Trade-offs:
    - We are limited to one factory: every product is created the same
      way, by calling its class with no arguments. When products need
      different creation logic, use a Factory Method (step 3).
    - Someone still has to register every class; forgetting it means
      the name silently produces a ``NullCar``.

Related:
    - Null Object provides the safe default for unknown names.
    - Factory Method adds one factory per product type.
    - Prototype can replace the registry of classes with a registry of
      ready-made instances to clone.

Roles::

    client ---> AutoFactory.create_instance(name) ---> AbsAuto (Product)
                  _autos: dict[str, type[AbsAuto]]        ^
                  unknown name -> NullCar      ChevyVolt | FordFusion |
                                               JeepSahara | NullCar
                                                 (ConcreteProduct)
"""

from abc import ABC, abstractmethod


class AbsAuto(ABC):
    """Interface every car must implement.

    Role in the pattern: Product.
    """

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
        print("Chevy Volt running with shocking power!")

    def stop(self) -> None:
        """Announce that the Volt shuts down."""
        print("Chevy Volt shutting down.")


class FordFusion(AbsAuto):
    """Ford mid-size sedan.

    Role in the pattern: ConcreteProduct.
    """

    def start(self) -> None:
        """Announce that the Fusion runs smoothly."""
        print("Ford Fusion running smoothly.")

    def stop(self) -> None:
        """Announce that the Fusion shuts down."""
        print("Ford Fusion shutting down.")


class JeepSahara(AbsAuto):
    """Jeep off-road vehicle.

    Role in the pattern: ConcreteProduct.
    """

    def start(self) -> None:
        """Announce that the Sahara runs ruggedly."""
        print("Jeep Sahara running ruggedly.")

    def stop(self) -> None:
        """Announce that the Sahara shuts down."""
        print("Jeep Sahara shutting down.")


class NullCar(AbsAuto):
    """Stand-in returned for unknown names (Null Object).

    It implements every required method, so callers never have to check
    for a missing car at runtime.

    Role in the pattern: ConcreteProduct (null object).
    """

    def __init__(self, car_name: str) -> None:
        """Remember the requested name to report it later.

        Parameters
        ----------
        car_name : str
            Name that is not registered in the factory.
        """
        self._car_name = car_name

    @property
    def car_name(self) -> str:
        """Name that was requested but is not registered."""
        return self._car_name

    def start(self) -> None:
        """Report that the unknown car cannot start."""
        print(f'Cannot start unknown car "{self._car_name}".')

    def stop(self) -> None:
        """Report that the unknown car cannot stop."""
        print(f'Cannot stop unknown car "{self._car_name}".')


class AutoFactory:
    """Create and return an instance of the requested car class.

    Role in the pattern: Factory.
    """

    def __init__(self) -> None:
        """Start with an empty registry; ``register`` fills it."""
        self._autos: dict[str, type[AbsAuto]] = {}

    def register(self, car_name: str, auto_class: type[AbsAuto]) -> None:
        """Make ``auto_class`` available under ``car_name``.

        Parameters
        ----------
        car_name : str
            Name clients will use to ask for the car.
        auto_class : type of AbsAuto
            Car class instantiated, with no arguments, on each request.
        """
        self._autos[car_name] = auto_class

    def create_instance(self, car_name: str) -> AbsAuto:
        """Return a new car for ``car_name``.

        Parameters
        ----------
        car_name : str
            Registered name of the desired car.

        Returns
        -------
        AbsAuto
            A new instance of the registered class, or a ``NullCar``
            when the name is unknown.
        """
        auto_class = self._autos.get(car_name)
        if auto_class is None:
            return NullCar(car_name)
        return auto_class()


def default_auto_factory() -> AutoFactory:
    """Return a factory that knows every car model in this module.

    This is the single place to touch when a new model is added.

    Returns
    -------
    AutoFactory
        Factory with ``ChevyVolt``, ``FordFusion`` and ``JeepSahara``
        registered as ``"chevy"``, ``"ford"`` and ``"jeep"``.
    """
    factory = AutoFactory()
    factory.register("chevy", ChevyVolt)
    factory.register("ford", FordFusion)
    factory.register("jeep", JeepSahara)
    return factory


def client() -> None:
    """Ask the factory for every known car plus an unknown one."""
    factory = default_auto_factory()
    for car_name in ("chevy", "ford", "jeep", "tesla"):
        car = factory.create_instance(car_name)
        car.start()
        car.stop()


if __name__ == "__main__":
    client()
