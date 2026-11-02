"""Arrange trips that share one itinerary skeleton.

Pattern: Template Method (behavioral).
Counterpart: ``travel_agency_before_template_method.py``.

Notes
-----
Why:
    - ``Trip.itinerary`` fixes the plan once: transport, three days, an
      optional excursion, then the return home.
    - The template method cannot be overridden (``@final`` for mypy,
      ``__init_subclass__`` at runtime); destinations only decide what
      each step means.
    - ``optional_excursion`` is a hook with an empty default, so only
      the destinations that offer one override it.
    - The agency works with any ``Trip`` and needs no branching.

When to use:
    - Several classes follow the same sequence of steps and differ only
      in how some of the steps are carried out.
    - You want subclasses to extend an algorithm only at well-defined
      points.

Trade-offs:
    - The skeleton is fixed by inheritance and cannot vary at runtime.
    - Each destination must implement every abstract step, even trivial
      ones.

Related:
    - Strategy swaps a whole algorithm by composition; Template Method
      keeps the algorithm and varies its steps by inheritance.
    - Builder also runs steps in order, but a director drives separate
      builder objects instead of an inherited skeleton.

Roles::

    TravelAgency (client) ---> Trip (AbstractClass)
                                 itinerary()  @final template method:
                                   set_transport -> day1 -> day2 -> day3
                                   -> optional_excursion (hook)
                                   -> return_home
                                      ^
                        VeniceTrip | MaldivesTrip (overrides the hook)
                               (ConcreteClass)
"""

from abc import ABC, abstractmethod
from typing import final


class Trip(ABC):
    """Skeleton of every three-day package.

    Role in the pattern: AbstractClass.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Reject subclasses that override the template method.

        ``@final`` is only checked by static type checkers; this hook
        enforces the same rule when the subclass is defined.

        Raises
        ------
        TypeError
            If the subclass defines ``itinerary``.
        """
        super().__init_subclass__(**kwargs)
        if "itinerary" in vars(cls):
            raise TypeError(
                f"{cls.__name__} must not override Trip.itinerary()"
            )

    @final
    def itinerary(self) -> None:
        """Run the steps of the trip in their fixed order.

        This is the template method; subclasses customise the steps,
        never the order.
        """
        self.set_transport()
        self.day1()
        self.day2()
        self.day3()
        self.optional_excursion()
        self.return_home()

    @abstractmethod
    def set_transport(self) -> None:
        """Describe how travellers get around."""

    @abstractmethod
    def day1(self) -> None:
        """Describe the first day."""

    @abstractmethod
    def day2(self) -> None:
        """Describe the second day."""

    @abstractmethod
    def day3(self) -> None:
        """Describe the third day."""

    def optional_excursion(self) -> None:
        """Add an extra activity before going home.

        This is a hook: the default does nothing, and subclasses
        override it only when they offer an excursion.
        """
        return

    @abstractmethod
    def return_home(self) -> None:
        """Describe the way back."""


class VeniceTrip(Trip):
    """Historical package; keeps the default hook.

    Role in the pattern: ConcreteClass.
    """

    def set_transport(self) -> None:
        """Get around Venice by boat along the Grand Canal."""
        print("Take a boat and find your way in the Grand Canal")

    def day1(self) -> None:
        """Visit St Mark's Basilica."""
        print("Visit St Mark's Basilica in St Mark's Square")

    def day2(self) -> None:
        """Visit the Doge's Palace."""
        print("Appreciate Doge's Palace")

    def day3(self) -> None:
        """Eat near the Rialto Bridge."""
        print("Enjoy the food near the Rialto Bridge")

    def return_home(self) -> None:
        """Buy souvenirs and travel back."""
        print("Get souvenirs for friends and get back")


class MaldivesTrip(Trip):
    """Beach package; overrides the ``optional_excursion`` hook.

    Role in the pattern: ConcreteClass.
    """

    def set_transport(self) -> None:
        """Get around the islands on foot."""
        print("On foot, on any island, wow!")

    def day1(self) -> None:
        """Watch the marine life of Banana Reef."""
        print("Enjoy the marine life of Banana Reef")

    def day2(self) -> None:
        """Do water sports and snorkelling."""
        print("Go for the water sports and snorkelling")

    def day3(self) -> None:
        """Relax on the beach."""
        print("Relax on the beach and enjoy the sun")

    def optional_excursion(self) -> None:
        """Add a sunset dolphin cruise (overrides the hook)."""
        print("Take a sunset cruise to watch the dolphins")

    def return_home(self) -> None:
        """Leave the beach, reluctantly."""
        print("Don't feel like leaving the beach...")


class TravelAgency:
    """Arrange any trip without knowing its concrete class.

    Role in the pattern: Client.
    """

    def arrange_trip(self, trip: Trip) -> None:
        """Print the itinerary of ``trip``."""
        trip.itinerary()


def client() -> None:
    """Arrange both packages through the same template method."""
    agency = TravelAgency()
    trips: list[Trip] = [VeniceTrip(), MaldivesTrip()]
    for trip in trips:
        print(f"== {type(trip).__name__}")
        agency.arrange_trip(trip)


if __name__ == "__main__":
    client()
