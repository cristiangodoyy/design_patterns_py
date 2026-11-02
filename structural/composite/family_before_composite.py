"""Find the oldest person across a family and a list of singles.

Pattern: Composite (structural), problem side.
Counterpart: ``family_with_composite.py``.

Notes
-----
Scenario:
    People can belong to a family or stay single, and we want the
    oldest person among all of them. ``Family`` is a collection of
    ``Person`` objects; singles are just a plain list.

What goes wrong here:
    - Individuals and groups have different interfaces, so the client
      must treat each structure differently and repeats the same search
      loop for the family and for the singles.
    - Groups cannot contain other groups: a family of families, or a
      family plus a loner, needs yet another loop in the client.
    - The client also has to seed the search with a sentinel
      (``date.max``) and deal with "nobody found" itself.

Roles::

    find_oldest(family, singles)
      for member in Family   -> compare birthdate   (loop 1)
      for person in singles  -> compare birthdate   (loop 2, duplicated)
"""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import date

REFERENCE_DATE = date(2025, 1, 1)


@dataclass(frozen=True)
class Person:
    """Person with a name and a birthdate."""

    name: str
    birthdate: date


class Family(Iterable[Person]):
    """Group of people that can be iterated, but only one level deep."""

    def __init__(self, members: Iterable[Person]) -> None:
        """Store the members of the family.

        Parameters
        ----------
        members : Iterable of Person
            People in the family; families cannot be nested.
        """
        self._members = list(members)

    def __iter__(self) -> Iterator[Person]:
        """Iterate over the members, one level deep."""
        return iter(self._members)


def age_on(birthdate: date, reference: date) -> tuple[int, int]:
    """Return the age at ``reference`` as whole years and months.

    Parameters
    ----------
    birthdate : date
        Date of birth.
    reference : date
        Date the age is measured on; injected to keep results fixed.

    Returns
    -------
    tuple of (int, int)
        Completed years and the remaining completed months.
    """
    months = (reference.year - birthdate.year) * 12
    months += reference.month - birthdate.month
    if reference.day < birthdate.day:
        months -= 1
    return divmod(months, 12)


def find_oldest(family: Family, singles: Iterable[Person]) -> Person:
    """Return the oldest person in ``family`` or ``singles``.

    The same search is written twice because the two groups are
    different kinds of object.

    Parameters
    ----------
    family : Family
        People who belong to the family.
    singles : Iterable of Person
        People who belong to no family.

    Returns
    -------
    Person
        The person with the earliest birthdate.

    Raises
    ------
    ValueError
        If both groups are empty.
    """
    oldest: Person | None = None
    earliest_date = date.max

    for member in family:
        if member.birthdate < earliest_date:
            oldest = member
            earliest_date = member.birthdate

    for single in singles:
        if single.birthdate < earliest_date:
            oldest = single
            earliest_date = single.birthdate

    if oldest is None:
        raise ValueError("Cannot find the oldest person of empty groups")
    return oldest


def client() -> None:
    """Print the oldest person among a family and some singles."""
    family = Family(
        [
            Person("Trillian", date(1970, 3, 14)),
            Person("Arthur", date(1965, 7, 4)),
            Person("Ford", date(1995, 2, 2)),
            Person("Zaphod", date(1997, 5, 1)),
            Person("Douglas", date(1999, 4, 2)),
        ]
    )
    singles = [
        Person("Marvin", date(1991, 1, 1)),
        Person("Slarti", date(1993, 9, 9)),
    ]

    oldest = find_oldest(family, singles)
    years, months = age_on(oldest.birthdate, REFERENCE_DATE)
    print(f"Oldest person: {oldest.name}; Age: {years} years, {months} months")


if __name__ == "__main__":
    client()
