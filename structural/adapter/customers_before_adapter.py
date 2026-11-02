"""Print customer names and addresses: the program before any vendors.

Pattern: Adapter (structural), problem side.
Counterpart: ``customers_vendors_with_object_adapter.py``.
Step 1 of 4: the original program, which only knows about customers.

Notes
-----
Scenario:
    A program prints the names and addresses of ``Customer`` objects.
    Users like it and soon ask for it to work with vendors too: after
    all, vendors also have a name and an address.

What goes wrong here:
    - Nothing is broken yet, but ``describe`` is written against the
      ``Customer`` interface: ``name`` plus a single ``address`` string.
    - The vendor API (next step) stores the address as a separate
      ``number`` and ``street``, so it cannot be passed in as is.
    - Copying the program into a vendor-only version would violate
      "don't repeat yourself"; step 2 tries conditional logic instead.

Roles::

    describe(customers) ---> Customer.name
                             Customer.address
"""

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    """Customer with a single, combined address string."""

    name: str
    address: str


CUSTOMERS = (
    Customer("Pizza Love", "33 Pepperoni Lane"),
    Customer("Happy and Green", "25 Kale St."),
    Customer("Sweet Tooth", "42 Chocolate Ave."),
)


def describe(customers: Iterable[Customer]) -> list[str]:
    """Return one printable line per customer.

    Parameters
    ----------
    customers : Iterable of Customer
        Customers to describe.

    Returns
    -------
    list of str
        ``"Name: ...; Address: ..."`` lines, in input order.
    """
    return [
        f"Name: {customer.name}; Address: {customer.address}"
        for customer in customers
    ]


def client() -> None:
    """Print every known customer."""
    for line in describe(CUSTOMERS):
        print(line)


if __name__ == "__main__":
    client()
