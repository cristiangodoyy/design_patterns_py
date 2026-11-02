"""Print customers and vendors by branching on which kind was requested.

Pattern: Adapter (structural), problem side.
Counterpart: ``customers_vendors_with_object_adapter.py``.
Step 2 of 4: vendors are added with conditional logic in the client.

Notes
-----
Scenario:
    Users want the customer report to work with vendors as well.
    Unfortunately the vendor API differs: a ``Customer`` has one
    combined ``address`` while a ``Vendor`` splits it into ``number``
    and ``street``. This version teaches the client about both.

What goes wrong here:
    - The client must check which kind of list it received and format
      each kind differently: type-checking branches are a smell.
    - Open/closed: government customers or foreign vendors would mean
      breaking open ``describe`` again to add one more branch.
    - Knowledge of the vendor's address layout leaks into the client
      instead of living next to the vendor.

Roles::

    describe(kind)
      if "customers" -> Customer.name, Customer.address
      elif "vendors" -> Vendor.name, Vendor.number + Vendor.street
      else           -> ValueError (edit the client for every new kind)
"""

from dataclasses import dataclass
from typing import Literal

type EntityKind = Literal["customers", "vendors"]


@dataclass(frozen=True)
class Customer:
    """Customer with a single, combined address string."""

    name: str
    address: str


@dataclass(frozen=True)
class Vendor:
    """Vendor whose address is split into house number and street.

    This is the incompatible interface the client has to cope with.
    """

    name: str
    number: int
    street: str


CUSTOMERS = (
    Customer("Pizza Love", "33 Pepperoni Lane"),
    Customer("Happy and Green", "25 Kale St."),
    Customer("Sweet Tooth", "42 Chocolate Ave."),
)

VENDORS = (
    Vendor("Dough Factory", 1, "Semolina Court"),
    Vendor("Farm Produce", 14, "Country Rd."),
    Vendor("Cocoa World", 53, "Tropical Blvd."),
)


def describe(kind: EntityKind) -> list[str]:
    """Return one printable line per entity of the requested kind.

    The client has to know every entity type and how each one stores
    its address.

    Parameters
    ----------
    kind : {"customers", "vendors"}
        Which list to describe.

    Returns
    -------
    list of str
        ``"Name: ...; Address: ..."`` lines, in list order.

    Raises
    ------
    ValueError
        If ``kind`` has no branch yet.
    """
    if kind == "customers":
        return [
            f"Name: {customer.name}; Address: {customer.address}"
            for customer in CUSTOMERS
        ]
    if kind == "vendors":
        return [
            f"Name: {vendor.name}; Address: {vendor.number} {vendor.street}"
            for vendor in VENDORS
        ]
    raise ValueError(f"Incorrect type: {kind}")


def client() -> None:
    """Print customers and then vendors through the branching client."""
    kinds: tuple[EntityKind, ...] = ("customers", "vendors")
    for kind in kinds:
        print(f"-- {kind}")
        for line in describe(kind):
            print(line)


if __name__ == "__main__":
    client()
