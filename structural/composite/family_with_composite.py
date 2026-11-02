"""Find the oldest person in trees of people nested to any depth.

Pattern: Composite (structural).
Counterpart: ``family_before_composite.py``.

Notes
-----
Why:
    - ``Person`` (leaf) and ``Tree`` (composite) share the ``Component``
      interface, so the client asks any node for ``get_oldest()``
      without knowing whether it is one person or a whole group.
    - A ``Tree`` replaces the old ``Family`` and can hold people or
      other trees at any depth, in any combination.
    - A person is the oldest of its own one-node tree, so it simply
      returns itself; a tree asks each member and keeps the earliest
      birthdate. The recursion replaces the duplicated client loops.
    - ``NullPerson`` is a Null Object: a pseudo person born on
      ``date.max``. It is the default of the ``min()`` search, so it
      is what an empty tree returns instead of ``None``, and it never
      wins a comparison against a real person.

When to use:
    - You need to represent part-whole hierarchies of objects.
    - Clients should treat individual objects and compositions of
      objects uniformly.

Trade-offs:
    - The common interface can become too general: it is hard to
      restrict which components a composite may contain.
    - Operations that only make sense for leaves (here ``birthdate``)
      need a separate contract (``Individual``).

Related:
    - Iterator traverses composites; Visitor adds operations to them.
    - Decorator has a similar recursive structure but a single child.
    - Null Object, used here for the empty result.

Roles::

    client ---> Component.get_oldest()
                   ^                 ^
             Individual            Tree (Composite)
             ^        ^              | members: Component, any depth
    Person (Leaf)  NullPerson        +--> Person | Tree | ...
                   (Null Object)
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from datetime import date

REFERENCE_DATE = date(2025, 1, 1)


class Component(ABC):
    """Anything that can report its oldest person.

    Role in the pattern: Component.
    """

    @abstractmethod
    def get_oldest(self) -> "Individual":
        """Return the oldest individual in this node.

        Returns
        -------
        Individual
            The individual with the earliest birthdate, or a
            ``NullPerson`` when the node holds nobody.
        """


class Individual(Component):
    """Contract shared by real and null people.

    Role in the pattern: Leaf interface.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name of the individual."""

    @property
    @abstractmethod
    def birthdate(self) -> date:
        """Date of birth used to compare ages."""

    @property
    @abstractmethod
    def is_null(self) -> bool:
        """Whether this individual stands for nobody.

        Check it before computing an age: a null individual's
        ``birthdate`` is a sentinel, not a real date.
        """

    def get_oldest(self) -> "Individual":
        """Return ``self``: a lone individual is its own oldest member."""
        return self


class Person(Individual):
    """Person with a name and a birthdate.

    Role in the pattern: Leaf.
    """

    def __init__(self, name: str, birthdate: date) -> None:
        """Store the person's name and birthdate.

        Parameters
        ----------
        name : str
            Display name.
        birthdate : date
            Date of birth used to compare ages.
        """
        self._name = name
        self._birthdate = birthdate

    @property
    def name(self) -> str:
        """The name given at construction."""
        return self._name

    @property
    def birthdate(self) -> date:
        """The birthdate given at construction."""
        return self._birthdate

    @property
    def is_null(self) -> bool:
        """Always ``False``: a ``Person`` is a real individual."""
        return False


class NullPerson(Individual):
    """Pseudo person with the latest possible birthdate.

    Role in the pattern: Null Object (leaf that stands for nobody).
    """

    @property
    def name(self) -> str:
        """Always ``"nobody"``."""
        return "nobody"

    @property
    def birthdate(self) -> date:
        """Always ``date.max``, so it never wins a comparison."""
        return date.max

    @property
    def is_null(self) -> bool:
        """Always ``True``: there is no real person behind this object."""
        return True


class Tree(Component, Iterable[Component]):
    """Group of people or other trees, nested to any depth.

    Role in the pattern: Composite.
    """

    def __init__(self, members: Iterable[Component]) -> None:
        """Store the members of the tree.

        Parameters
        ----------
        members : Iterable of Component
            People or other trees, nested to any depth.
        """
        self._members = list(members)

    def __iter__(self) -> Iterator[Component]:
        """Iterate over the direct members of this tree."""
        return iter(self._members)

    def get_oldest(self) -> Individual:
        """Return the oldest individual among all nested members.

        Returns
        -------
        Individual
            The oldest member found recursively, or ``NullPerson`` when
            the tree is empty.
        """
        return min(
            (member.get_oldest() for member in self),
            key=lambda individual: individual.birthdate,
            default=NullPerson(),
        )


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


def client() -> None:
    """Build trees in several combinations and print each oldest."""
    hitchhikers = Tree(
        [
            Person("Trillian", date(1970, 3, 14)),
            Person("Arthur", date(1965, 7, 4)),
            Person("Ford", date(1995, 2, 2)),
            Person("Zaphod", date(1997, 5, 1)),
            Person("Douglas", date(1999, 4, 2)),
        ]
    )
    singles = Tree(
        [
            Person("Marvin", date(1991, 1, 1)),
            Person("Slarti", date(1993, 9, 9)),
        ]
    )
    loner = Person("Dirk", date(1990, 6, 6))

    tree1 = Tree([hitchhikers])
    tree2 = Tree([singles, loner])
    tree3 = Tree([tree1, tree2])

    for tree in (tree1, tree2, tree3):
        oldest = tree.get_oldest()
        years, months = age_on(oldest.birthdate, REFERENCE_DATE)
        print(
            f"Oldest person: {oldest.name}; "
            f"Age: {years} years, {months} months"
        )
    nobody = Tree([]).get_oldest()
    print(
        f"Oldest person in an empty tree: {nobody.name}; "
        f"is_null: {nobody.is_null}"
    )


if __name__ == "__main__":
    client()
