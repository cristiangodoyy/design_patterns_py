"""Combine subscription periods and discounts through a bridge.

Pattern: Bridge (structural).
Counterpart: ``subscription_discount_before_bridge.py``.
Step 3 of 3: the discount becomes a separate, injected hierarchy.

Notes
-----
Why:
    - Billing period and discount vary independently, so each gets its
      own hierarchy: ``Subscription`` (abstraction) and ``Discount``
      (implementor). The subscription holds a discount instance, and
      that reference is the "bridge" between them.
    - Classes now grow additively, not multiplicatively: 2 periods plus
      3 discounts is 5 classes, and a new discount is one new class
      that works with every period.
    - The discount is injected per subscription, so it is chosen at
      runtime (dependency injection) and can be tested in isolation.

When to use:
    - A class hierarchy is growing in two (or more) independent
      dimensions and every combination needs its own subclass.
    - You want to choose or switch an implementation at runtime.
    - Abstraction and implementation should evolve separately.

Trade-offs:
    - More indirection and more types for a design with only one real
      combination.
    - The implementor interface must be general enough for every
      refined abstraction; changing it touches both sides.

Related:
    - Strategy has the same shape; Bridge is about splitting a whole
      hierarchy, Strategy about swapping one algorithm.
    - Adapter makes existing, unrelated classes fit after the fact;
      Bridge is designed up front.
    - Abstract Factory can create matching abstraction/implementor
      pairs.

Roles::

    Subscription (Abstraction) ---has-a---> Discount (Implementor)
         ^                                      ^
    Annual | Monthly             NoDiscount | StudentDiscount
    (RefinedAbstraction)           | CorporateDiscount
                                   (ConcreteImplementor)
"""

import calendar

from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import date


def add_months(start: date, months: int) -> date:
    """Return ``start`` moved forward by ``months`` calendar months.

    When the target month is shorter, the day is clamped to its last
    day (January 31 plus one month is the end of February).

    Parameters
    ----------
    start : date
        Date to move from.
    months : int
        Number of months to add; may be negative.

    Returns
    -------
    date
        The shifted date.
    """
    month_index = start.month - 1 + months
    year = start.year + month_index // 12
    month = month_index % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(start.day, last_day))


class Discount(ABC):
    """Rule that turns a base price into the price actually charged.

    Prices are integer cents; percentage discounts round down to the
    nearest cent.

    Role in the pattern: Implementor.
    """

    @abstractmethod
    def apply(self, price: int) -> int:
        """Return ``price`` after this discount.

        Parameters
        ----------
        price : int
            Base price in US cents.

        Returns
        -------
        int
            Discounted price in US cents.
        """


class NoDiscount(Discount):
    """Charge the full base price.

    Role in the pattern: ConcreteImplementor.
    """

    def apply(self, price: int) -> int:
        """Return ``price`` unchanged."""
        return price


class StudentDiscount(Discount):
    """Take 10% off for students.

    Role in the pattern: ConcreteImplementor.
    """

    def apply(self, price: int) -> int:
        """Return 90% of ``price``, rounded down to the cent."""
        return price * 90 // 100


class CorporateDiscount(Discount):
    """Take 20% off for corporate customers.

    Role in the pattern: ConcreteImplementor.
    """

    def apply(self, price: int) -> int:
        """Return 80% of ``price``, rounded down to the cent."""
        return price * 80 // 100


class Subscription(ABC):
    """Subscription whose final price is delegated to a discount.

    Role in the pattern: Abstraction.

    Subclasses decide the billing period (base price and expiration);
    the injected ``Discount`` decides how much of it is charged.
    """

    def __init__(
        self, subscriber: str, enrolled: date, discount: Discount
    ) -> None:
        """Store who subscribed, when, and which discount applies.

        Parameters
        ----------
        subscriber : str
            Name of the subscriber.
        enrolled : date
            Date the subscription started.
        discount : Discount
            Rule applied to the base price; the bridge to the other hierarchy.
        """
        self._subscriber = subscriber
        self._enrolled = enrolled
        self._discount = discount

    @property
    def subscriber(self) -> str:
        """Name of the subscriber."""
        return self._subscriber

    @property
    def enrolled(self) -> date:
        """Date the subscription started."""
        return self._enrolled

    @property
    def discount(self) -> Discount:
        """Discount applied to the base price."""
        return self._discount

    @property
    @abstractmethod
    def base_price(self) -> int:
        """Undiscounted price of the billing period in US cents."""

    @property
    @abstractmethod
    def expiration(self) -> date:
        """Date the subscription expires, computed from ``enrolled``."""

    @property
    def price(self) -> int:
        """Price charged: the base price after the discount."""
        return self._discount.apply(self.base_price)


class Annual(Subscription):
    """Annual subscription: $250 base, expires in a year.

    Role in the pattern: RefinedAbstraction.
    """

    @property
    def base_price(self) -> int:
        """Undiscounted annual price: $250, in cents."""
        return 25_000

    @property
    def expiration(self) -> date:
        """One year after the enrollment date."""
        return add_months(self._enrolled, 12)


class Monthly(Subscription):
    """Monthly subscription: $50 base, expires in a month.

    Role in the pattern: RefinedAbstraction.
    """

    @property
    def base_price(self) -> int:
        """Undiscounted monthly price: $50, in cents."""
        return 5_000

    @property
    def expiration(self) -> date:
        """One month after the enrollment date."""
        return add_months(self._enrolled, 1)


ENROLLED = date(2024, 1, 31)


def format_cents(cents: int) -> str:
    """Return ``cents`` formatted as dollars, for example ``$5.20``."""
    return f"${cents // 100}.{cents % 100:02d}"


def describe(subscriptions: Iterable[Subscription]) -> list[str]:
    """Return one printable line per subscription.

    Parameters
    ----------
    subscriptions : Iterable of Subscription
        Subscriptions to describe.

    Returns
    -------
    list of str
        Subscriber, discount, cost and expiration of each subscription.
    """
    return [
        f"Subscriber: {sub.subscriber}; "
        f"Discount: {type(sub.discount).__name__}; "
        f"Cost: {format_cents(sub.price)}; "
        f"Expiration: {sub.expiration.isoformat()}"
        for sub in subscriptions
    ]


def client() -> None:
    """Pair each period with different injected discounts and print."""
    subscriptions = (
        Monthly("Ted", ENROLLED, StudentDiscount()),
        Monthly("Bob", ENROLLED, CorporateDiscount()),
        Annual("Alice", ENROLLED, CorporateDiscount()),
        Annual("Wilma", ENROLLED, NoDiscount()),
    )
    for line in describe(subscriptions):
        print(line)


if __name__ == "__main__":
    client()
