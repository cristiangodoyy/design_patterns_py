"""Create a car model by name with a brute-force if/elif chain.

Pattern: Factory (creational), problem side.
Counterpart: ``cars_with_simple_factory.py``.
Step 1 of 3; next: ``cars_with_simple_factory.py``.

Notes
-----
Scenario:
    A program must support several car models (a Chevy Volt, a Ford
    Fusion and a Jeep Sahara) but does not know which one it needs until
    runtime. ``get_car`` receives the desired model's name, which may come
    from a command-line argument, a desktop or web form, or a database.
    Each car implements ``start`` and ``stop``, which just print messages.

    Unknown names return a ``NullCar``: an example of the Null Object
    pattern, a dummy instance that still implements every required method
    so callers never have to test for ``None`` at runtime.

What goes wrong here:
    - Take note of the long ``if/elif/else`` chain. When you see one, or
      are tempted to write one, there might be a better way; the factory
      pattern offers a solution for exactly this issue.
    - Open/closed: a class or function should be open for extension but
      closed for modification. Adding a car model means opening this
      module and editing ``get_car``. Imagine you started using code
      someone designed only to find out later that they had changed it;
      you would be frustrated, and rightly so.
    - Dependency inversion: the program instantiates the car classes
      directly, so it depends on their implementations; ``Car`` is just
      the union of every concrete class.

Roles::

    client ---> get_car(name)
                  if "chevy" -> ChevyVolt()
                  elif "ford" -> FordFusion()
                  elif "jeep" -> JeepSahara()
                  else        -> NullCar(name)   (edit for every new car)
"""


class ChevyVolt:
    """Chevrolet electric car."""

    def start(self) -> None:
        """Announce that the electric Volt starts."""
        print("Chevy Volt running with shocking power!")

    def stop(self) -> None:
        """Announce that the Volt shuts down."""
        print("Chevy Volt shutting down.")


class FordFusion:
    """Ford mid-size sedan."""

    def start(self) -> None:
        """Announce that the Fusion runs smoothly."""
        print("Ford Fusion running smoothly.")

    def stop(self) -> None:
        """Announce that the Fusion shuts down."""
        print("Ford Fusion shutting down.")


class JeepSahara:
    """Jeep off-road vehicle."""

    def start(self) -> None:
        """Announce that the Sahara runs ruggedly."""
        print("Jeep Sahara running ruggedly.")

    def stop(self) -> None:
        """Announce that the Sahara shuts down."""
        print("Jeep Sahara shutting down.")


class NullCar:
    """Stand-in for an unknown model (Null Object).

    It accepts the requested name and reports it as unknown when started,
    so callers can treat it like any other car.
    """

    def __init__(self, car_name: str) -> None:
        """Remember the requested name to report it later.

        Parameters
        ----------
        car_name : str
            Name that matched no known model.
        """
        self._car_name = car_name

    def start(self) -> None:
        """Report that the requested car is unknown."""
        print(f'Unknown car "{self._car_name}".')

    def stop(self) -> None:
        """Do nothing: there is no engine to stop."""


type Car = ChevyVolt | FordFusion | JeepSahara | NullCar


def get_car(car_name: str) -> Car:
    """Instantiate the car class that matches ``car_name``.

    Parameters
    ----------
    car_name : str
        Name of the desired car, for example ``"chevy"``.

    Returns
    -------
    Car
        A new instance of the matching class, or a ``NullCar`` when the
        name is unknown.
    """
    if car_name == "chevy":
        return ChevyVolt()
    if car_name == "ford":
        return FordFusion()
    if car_name == "jeep":
        return JeepSahara()
    return NullCar(car_name)


def client() -> None:
    """Start and stop every supported car plus an unsupported one."""
    for car_name in ("chevy", "ford", "jeep", "tesla"):
        car = get_car(car_name)
        car.start()
        car.stop()


if __name__ == "__main__":
    client()
