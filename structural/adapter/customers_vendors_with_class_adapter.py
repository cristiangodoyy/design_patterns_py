"""Print customers and vendors through a class adapter (inheritance).

Pattern: Adapter (structural).
Counterpart: ``customers_vendors_before_adapter.py``.
Step 3 of 4: the adapter inherits from both the target and the adaptee.

Notes
-----
Why:
    - The adapter lets objects with incompatible interfaces collaborate:
      it translates calls the client makes into calls the adaptee
      understands.
    - ``VendorAdapter`` *is a* ``Vendor`` (it reuses the vendor's state
      and ``name``) and *is an* ``Addressable`` (it adds the combined
      ``address`` the client expects), via multiple inheritance.
    - The client goes back to one loop over one interface; it never
      checks which kind of entity it received (open/closed).

When to use:
    - You must reuse an existing class (often legacy or third-party
      code) whose interface does not match the one your code expects.
    - You can subclass the adaptee and only need to adapt that one
      class, not a whole family of subclasses.

Trade-offs:
    - The adapter is bound to one concrete adaptee class at definition
      time; an object adapter (step 4) can wrap any instance instead.
    - Multiple inheritance couples the adapter to the adaptee's
      internals and makes attribute resolution order matter.

Related:
    - The object adapter achieves the same with composition.
    - Bridge separates abstraction from implementation up front;
      Adapter makes unrelated classes work together after the fact.
    - Decorator keeps the interface and adds behavior; Adapter changes
      the interface.

Roles::

    describe(entities) ----> Addressable (Target)
                               ^          ^
                        Customer      VendorAdapter (Adapter)
                                          |  inherits
                                          v
                                        Vendor (Adaptee)
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass


class Addressable(ABC):
    """Interface the client code works against.

    ``name`` is a plain attribute every target must provide; only the
    combined ``address`` has to be computed.

    Role in the pattern: Target.
    """

    name: str

    @property
    @abstractmethod
    def address(self) -> str:
        """Full address as one string, house number first."""


class Customer(Addressable):
    """Customer that already speaks the target interface.

    Role in the pattern: concrete Target (needs no adaptation).
    """

    def __init__(self, name: str, address: str) -> None:
        """Store the customer's name and its combined address.

        Parameters
        ----------
        name : str
            Display name of the customer.
        address : str
            Full address, house number first.
        """
        self.name = name
        self._address = address

    @property
    def address(self) -> str:
        """The address exactly as the customer stores it."""
        return self._address


@dataclass(frozen=True)
class Vendor:
    """Vendor whose address is split into house number and street.

    Role in the pattern: Adaptee. It is exactly the class of step 2;
    the adapter reuses it as is.
    """

    name: str
    number: int
    street: str


class VendorAdapter(Vendor, Addressable):
    """Vendor that also looks like an ``Addressable`` to the client.

    Role in the pattern: Adapter (class adapter).

    It inherits ``__init__`` and the ``name`` field from ``Vendor`` and
    only adds the ``address`` the target is missing. ``Vendor`` is
    listed first so its generated ``__init__`` is found first in the
    method resolution order.
    """

    @property
    def address(self) -> str:
        """Build the combined address from the vendor's own parts."""
        return f"{self.number} {self.street}"


ENTITIES: tuple[Addressable, ...] = (
    Customer("Pizza Love", "33 Pepperoni Lane"),
    Customer("Happy and Green", "25 Kale St."),
    Customer("Sweet Tooth", "42 Chocolate Ave."),
    VendorAdapter("Dough Factory", 1, "Semolina Court"),
    VendorAdapter("Farm Produce", 14, "Country Rd."),
    VendorAdapter("Cocoa World", 53, "Tropical Blvd."),
)


def describe(entities: Iterable[Addressable]) -> list[str]:
    """Return one printable line per entity.

    The client only knows the target interface; it cannot tell a
    customer from an adapted vendor.

    Parameters
    ----------
    entities : Iterable of Addressable
        Customers, adapted vendors or any other target implementation.

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
    """Print customers and adapted vendors with the same client."""
    for line in describe(ENTITIES):
        print(line)


if __name__ == "__main__":
    client()
