"""Model annual and monthly subscriptions with a small class hierarchy.

Pattern: Bridge (structural), problem side.
Counterpart: ``subscription_discount_with_bridge.py``.
Step 1 of 3: two subscription types, each with its own price.

Notes
-----
Scenario:
    There are two kinds of subscribers, annual and monthly. An annual
    subscription costs $250 and expires in a year; a monthly one costs
    $50 and expires in a month. Each subclass fixes its price and
    computes its expiration from the enrollment date.

What goes wrong here:
    - Nothing yet: two classes for two variants is perfectly fine.
    - But price and billing period are fused into the same hierarchy.
      As soon as a second, independent dimension appears (discounts in
      step 2), every combination will need its own subclass.

Roles::

    Subscription (abstract: price, expiration)
        ^              ^
      Annual        Monthly
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


class Subscription(ABC):
    """Subscription of one subscriber, enrolled on a given date.

    Subclasses must provide the price and compute the expiration date
    from the enrollment date.
    """

    def __init__(self, subscriber: str, enrolled: date) -> None:
        """Store who subscribed and when.

        Parameters
        ----------
        subscriber : str
            Name of the subscriber.
        enrolled : date
            Date the subscription started.
        """
        self._subscriber = subscriber
        self._enrolled = enrolled

    @property
    def subscriber(self) -> str:
        """Name of the subscriber."""
        return self._subscriber

    @property
    def enrolled(self) -> date:
        """Date the subscription started."""
        return self._enrolled

    @property
    @abstractmethod
    def price(self) -> int:
        """Price of the subscription in US cents."""

    @property
    @abstractmethod
    def expiration(self) -> date:
        """Date the subscription expires."""


class Annual(Subscription):
    """Annual subscription: $250, expires in a year."""

    @property
    def price(self) -> int:
        """Annual price: $250, in cents."""
        return 25_000

    @property
    def expiration(self) -> date:
        """One year after the enrollment date."""
        return add_months(self._enrolled, 12)


class Monthly(Subscription):
    """Monthly subscription: $50, expires in a month.

    It looks much like ``Annual`` except for the price and the
    expiration calculation.
    """

    @property
    def price(self) -> int:
        """Monthly price: $50, in cents."""
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
        Subscriber, cost and expiration of each subscription.
    """
    return [
        f"Subscriber: {sub.subscriber}; Cost: {format_cents(sub.price)}; "
        f"Expiration: {sub.expiration.isoformat()}"
        for sub in subscriptions
    ]


def client() -> None:
    """Build one subscription of each type and print them."""
    subscriptions = (Monthly("Bob", ENROLLED), Annual("Carol", ENROLLED))
    for line in describe(subscriptions):
        print(line)


if __name__ == "__main__":
    client()
