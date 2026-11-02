"""Print customers, vendors and employees through object adapters.

Pattern: Adapter (structural).
Counterpart: ``customers_vendors_before_adapter.py``.
Step 4 of 4: adapters wrap an adaptee instance (composition).

Notes
-----
Why:
    - Each adapter holds a ``Vendor`` or an ``Employee`` and exposes it
      behind the ``Addressable`` interface the client expects, so the
      client loops over one interface with no type checks.
    - The adaptees stay untouched: the translation from ``number`` and
      ``street`` (and ``city``) to one ``address`` lives in the adapter.
    - New kinds of entities get a new adapter; the client is closed for
      modification (open/closed).
    - ``Addressable`` is a ``Protocol``: customers and adapters satisfy
      it structurally, without inheriting from it.

When to use:
    - You must reuse existing classes (legacy or third-party code) whose
      interfaces do not match the one your code expects.
    - You want to adapt any instance of the adaptee, including its
      subclasses, without inheriting from it.

Trade-offs:
    - One more indirection and one more class per incompatible type.
    - These adapters are one-way: they make a vendor look like a
      customer, not the other way around. A two-way adapter would have
      to implement both interfaces.

Related:
    - The class adapter (step 3) uses multiple inheritance instead.
    - Decorator also wraps an object but keeps its interface.
    - Facade defines a new, simpler interface over a subsystem.

Roles::

    describe(entities) ----> Addressable (Target)
                               ^            ^              ^
                         Customer    VendorAdapter   EmployeeAdapter
                                     (Adapter)       (Adapter)
                                         | has-a          | has-a
                                         v                v
                                     Vendor (Adaptee)  Employee (Adaptee)
"""

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol


class Addressable(Protocol):
    """Interface the client code works against.

    Role in the pattern: Target.
    """

    @property
    def name(self) -> str:
        """Display name of the entity."""
        ...

    @property
    def address(self) -> str:
        """Full address as one string, house number first."""
        ...


@dataclass(frozen=True)
class Customer:
    """Customer that already matches ``Addressable`` structurally.

    Role in the pattern: concrete Target (needs no adaptation).
    """

    name: str
    address: str


@dataclass(frozen=True)
class Vendor:
    """Vendor whose address is split into house number and street.

    Role in the pattern: Adaptee.
    """

    name: str
    number: int
    street: str


@dataclass(frozen=True)
class Employee:
    """Employee whose address also carries the city.

    Role in the pattern: Adaptee.
    """

    name: str
    number: int
    street: str
    city: str


class VendorAdapter:
    """Expose a wrapped ``Vendor`` through the ``Addressable`` interface.

    Role in the pattern: Adapter (object adapter).
    """

    def __init__(self, vendor: Vendor) -> None:
        """Wrap ``vendor`` without changing it.

        Parameters
        ----------
        vendor : Vendor
            Adaptee exposed through the ``Addressable`` interface.
        """
        self._vendor = vendor

    @property
    def name(self) -> str:
        """The wrapped vendor's name, unchanged."""
        return self._vendor.name

    @property
    def address(self) -> str:
        """House number and street joined into one address."""
        return f"{self._vendor.number} {self._vendor.street}"


class EmployeeAdapter:
    """Expose a wrapped ``Employee`` through the ``Addressable`` interface.

    Role in the pattern: Adapter (object adapter).
    """

    def __init__(self, employee: Employee) -> None:
        """Wrap ``employee`` without changing it.

        Parameters
        ----------
        employee : Employee
            Adaptee exposed through the ``Addressable`` interface.
        """
        self._employee = employee

    @property
    def name(self) -> str:
        """The wrapped employee's name, unchanged."""
        return self._employee.name

    @property
    def address(self) -> str:
        """House number, street and city joined into one address."""
        employee = self._employee
        return f"{employee.number} {employee.street}, {employee.city}"


ENTITIES: tuple[Addressable, ...] = (
    Customer("Pizza Love", "33 Pepperoni Lane"),
    Customer("Sweet Tooth", "42 Chocolate Ave."),
    VendorAdapter(Vendor("Dough Factory", 1, "Semolina Court")),
    VendorAdapter(Vendor("Cocoa World", 53, "Tropical Blvd.")),
    EmployeeAdapter(Employee("Ada Lovelace", 12, "Analytical St.", "London")),
)


def describe(entities: Iterable[Addressable]) -> list[str]:
    """Return one printable line per entity.

    Parameters
    ----------
    entities : Iterable of Addressable
        Customers or adapters; anything with ``name`` and ``address``.

    Returns
    -------
    list of str
        ``"Name: ...; Address: ..."`` lines, in input order.
    """
    return [
        f"Name: {entity.name}; Address: {entity.address}"
        for entity in entities
    ]


def client() -> None:
    """Print customers and adapted vendors and employees together."""
    for line in describe(ENTITIES):
        print(line)


if __name__ == "__main__":
    client()
