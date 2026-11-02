"""Add student and corporate discounts by subclassing every combination.

Pattern: Bridge (structural), problem side.
Counterpart: ``subscription_discount_with_bridge.py``.
Step 2 of 3: discounts are added with more subclasses.

Notes
-----
Scenario:
    A new requirement arrives: a 10% discount for students and a 20%
    discount for corporate customers, on both annual and monthly
    subscriptions. Continuing with subclassing, each billing period
    gets one subclass per discount.

What goes wrong here:
    - Two independent dimensions (billing period and discount) share
      one hierarchy, so the classes multiply: 2 periods x 2 discounts
      means four new classes on top of the original two.
    - Another requirement, say a limited-time offer that doubles the
      subscription period for the same price, would need six more
      classes, doubling what is already too many.
    - The discount rules are duplicated: ``AnnualStudent`` and
      ``MonthlyStudent`` both hard-code the same 10%.
    - The discount is fixed at class-definition time; it cannot be
      chosen or changed per subscription at runtime.

Roles::

    Subscription (abstract: price, expiration)
        ^                         ^
      Annual                    Monthly
        ^        ^                ^         ^
    AnnualStudent AnnualCorporate MonthlyStudent MonthlyCorporate
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
    """Subscription of one subscriber, enrolled on a given date."""

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
    """Monthly subscription: $50, expires in a month."""

    @property
    def price(self) -> int:
        """Monthly price: $50, in cents."""
        return 5_000

    @property
    def expiration(self) -> date:
        """One month after the enrollment date."""
        return add_months(self._enrolled, 1)


class AnnualStudent(Annual):
    """Annual subscription with the 10% student discount."""

    @property
    def price(self) -> int:
        """Annual price minus the 10% student discount."""
        return super().price * 90 // 100


class AnnualCorporate(Annual):
    """Annual subscription with the 20% corporate discount."""

    @property
    def price(self) -> int:
        """Annual price minus the 20% corporate discount."""
        return super().price * 80 // 100


class MonthlyStudent(Monthly):
    """Monthly subscription with the 10% student discount (duplicated)."""

    @property
    def price(self) -> int:
        """Monthly price minus the 10% student discount, again."""
        return super().price * 90 // 100


class MonthlyCorporate(Monthly):
    """Monthly subscription with the 20% corporate discount (duplicated)."""

    @property
    def price(self) -> int:
        """Monthly price minus the 20% corporate discount, again."""
        return super().price * 80 // 100


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
    """Build every period and discount combination and print them."""
    subscriptions = (
        Monthly("Fred", ENROLLED),
        MonthlyStudent("Ted", ENROLLED),
        MonthlyCorporate("Bob", ENROLLED),
        Annual("Wilma", ENROLLED),
        AnnualStudent("Carol", ENROLLED),
        AnnualCorporate("Alice", ENROLLED),
    )
    for line in describe(subscriptions):
        print(line)


if __name__ == "__main__":
    client()
