"""Calculate shipping cost by branching on the order's shipper.

Pattern: Strategy (behavioral), problem side.
Counterpart: ``shipping_cost_with_strategy.py``.

Notes
-----
Scenario:
    An online shop ships orders with FedEx, UPS or the postal service,
    and each company charges differently. The cost calculator must
    return the right price for every order.

What goes wrong here:
    - ``Order`` stores which shipper it uses, mixing what is ordered
      with how it travels (single responsibility).
    - ``ShippingCost`` branches on the shipper with an ``if`` chain;
      a new shipper means a new branch and a new helper method
      (open/closed).
    - Every algorithm lives in the same class, so they cannot be
      tested, reused or swapped independently.

Roles::

    ShippingCost.shipping_cost(order)
      if FEDEX  -> _fedex_cost()
      if UPS    -> _ups_cost()
      if POSTAL -> _postal_cost()   (edit for every new shipper)
"""

from enum import StrEnum, auto


class Shipper(StrEnum):
    """Shipping companies known to the calculator."""

    FEDEX = auto()
    UPS = auto()
    POSTAL = auto()


class Order:
    """Order that also knows how it will be shipped.

    Holding the shipper here mixes two responsibilities: what is being
    ordered and how it travels.
    """

    def __init__(self, customer: str, shipper: Shipper) -> None:
        """Store who placed the order and which company ships it.

        Parameters
        ----------
        customer : str
            Name of the customer.
        shipper : Shipper
            Shipping company; it selects the branch in ``ShippingCost``.
        """
        self._customer = customer
        self._shipper = shipper

    @property
    def customer(self) -> str:
        """Name of the customer who placed the order."""
        return self._customer

    @property
    def shipper(self) -> Shipper:
        """Shipping company chosen for the order."""
        return self._shipper


class ShippingCost:
    """Compute costs by branching on the order's shipper."""

    def shipping_cost(self, order: Order) -> int:
        """Return the shipping cost for ``order``.

        Adding a shipper requires a new branch here and a new helper
        method below, so this class is never closed for modification.

        Parameters
        ----------
        order : Order
            Order whose shipper selects the branch.

        Returns
        -------
        int
            Cost in US cents.

        Raises
        ------
        ValueError
            If the shipper has no branch yet.
        """
        if order.shipper == Shipper.FEDEX:
            return self._fedex_cost(order)
        if order.shipper == Shipper.UPS:
            return self._ups_cost(order)
        if order.shipper == Shipper.POSTAL:
            return self._postal_cost(order)
        raise ValueError(f"Invalid shipper {order.shipper}")

    def _fedex_cost(self, order: Order) -> int:
        """Return the FedEx flat rate in cents."""
        return 300

    def _ups_cost(self, order: Order) -> int:
        """Return the UPS flat rate in cents."""
        return 400

    def _postal_cost(self, order: Order) -> int:
        """Return the postal service flat rate in cents."""
        return 500


def format_cents(cents: int) -> str:
    """Return ``cents`` formatted as dollars, for example ``$5.20``."""
    return f"${cents // 100}.{cents % 100:02d}"


def client() -> None:
    """Compute the cost of one order per shipper."""
    calculator = ShippingCost()
    for shipper in Shipper:
        order = Order("Ada", shipper)
        cost = calculator.shipping_cost(order)
        print(f"{shipper}: {format_cents(cost)}")


if __name__ == "__main__":
    client()
