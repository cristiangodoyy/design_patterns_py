"""Arrange trips whose itineraries are each written out by hand.

Pattern: Template Method (behavioral), problem side.
Counterpart: ``travel_agency_with_template_method.py``.

Notes
-----
Scenario:
    A travel agency sells three-day packages. Every package follows
    the same plan: get there, spend three days, then go back home. Only
    the details of each step change from destination to destination.

What goes wrong here:
    - Each trip writes the whole sequence again under its own method
      name, so the shared plan exists only by convention.
    - Changing the plan (say, adding a free day) means editing every
      trip class and hoping they stay consistent.
    - The agency must branch on the trip kind to know which method to
      call, so every new destination edits the agency too.

Roles::

    TravelAgency.arrange_trip(kind)
        if HISTORICAL -> VeniceTrip.plan()        transport, days, home
        elif BEACH    -> MaldivesTrip.organize()  transport, days, home
                       (same skeleton, copied by hand)
"""

from enum import StrEnum, auto


class TripKind(StrEnum):
    """Packages the agency sells."""

    HISTORICAL = auto()
    BEACH = auto()


class VeniceTrip:
    """Historical package with its own copy of the itinerary."""

    def plan(self) -> None:
        """Print the whole Venice itinerary, written out by hand."""
        print("Take a boat and find your way in the Grand Canal")
        print("Visit St Mark's Basilica in St Mark's Square")
        print("Appreciate Doge's Palace")
        print("Enjoy the food near the Rialto Bridge")
        print("Get souvenirs for friends and get back")


class MaldivesTrip:
    """Beach package with a second copy of the itinerary."""

    def organize(self) -> None:
        """Print the whole Maldives itinerary, copied by hand.

        Same skeleton as ``VeniceTrip.plan`` under another method name.
        """
        print("On foot, on any island, wow!")
        print("Enjoy the marine life of Banana Reef")
        print("Go for the water sports and snorkelling")
        print("Relax on the beach and enjoy the sun")
        print("Don't feel like leaving the beach...")


class TravelAgency:
    """Agency that must know every trip class and its method name."""

    def arrange_trip(self, kind: TripKind) -> None:
        """Print the itinerary of the requested package.

        Raises
        ------
        ValueError
            If the agency has no branch for ``kind`` yet.
        """
        if kind == TripKind.HISTORICAL:
            VeniceTrip().plan()
        elif kind == TripKind.BEACH:
            MaldivesTrip().organize()
        else:
            raise ValueError(f"Unknown trip kind {kind}")


def client() -> None:
    """Arrange every package the agency sells."""
    agency = TravelAgency()
    for kind in TripKind:
        print(f"== {kind}")
        agency.arrange_trip(kind)


if __name__ == "__main__":
    client()
