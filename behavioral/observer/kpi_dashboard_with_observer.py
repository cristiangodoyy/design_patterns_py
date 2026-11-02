"""Refresh KPI displays by letting them observe the KPI source.

Pattern: Observer (behavioral).
Counterpart: ``kpi_dashboard_before_observer.py``.

Notes
-----
Why:
    - ``KPIs`` (the subject) no longer knows which displays exist: it
      keeps a list of ``Observer`` objects and notifies all of them
      whenever its values change.
    - Displays attach and detach themselves at runtime; a new display
      is a new observer class, and neither the subject nor the other
      displays change (open/closed).
    - Pull model: ``notify`` only says "something changed", and each
      observer reads the values it needs from the subject.

When to use:
    - A change in one object must be reflected in others, and you do
      not know in advance how many there are or which ones.
    - The object that changes should not be coupled to the objects
      that react to the change.

Trade-offs:
    - Observers are notified in attach order, and a slow or failing
      observer delays or breaks the ones after it.
    - With the pull model each observer depends on the subject's
      concrete interface; the push model sends the data instead, at
      the cost of a fixed ``update`` signature.
    - Forgetting to detach keeps observers alive (lapsed listener).

Related:
    - Mediator also decouples senders from receivers, but centralises
      the logic in one object.
    - Model-View-Controller uses Observer between model and views.

Roles::

    Subject (Subject) ---notifies---> Observer (Observer)
       ^                                  ^
    KPIs (ConcreteSubject)            KPIObserver (pull-model base)
       ^                                  ^
       +--------pulls values------  CurrentKPIs | ForecastKPIs
                                     (ConcreteObserver)
"""

from abc import ABC, abstractmethod
from typing import Protocol


class KPISource(Protocol):
    """Read-only view of the KPI values an observer pulls.

    Observers depend on this shape, not on the concrete ``KPIs`` class,
    so any object that exposes the three values can be observed.

    Role in the pattern: Subject interface (read side).
    """

    @property
    def open_tickets(self) -> int:
        """Tickets currently open."""
        ...

    @property
    def closed_tickets(self) -> int:
        """Tickets closed in the last hour."""
        ...

    @property
    def new_tickets(self) -> int:
        """Tickets opened in the last hour."""
        ...


class Observer(ABC):
    """Anything that wants to hear about subject changes.

    Role in the pattern: Observer.
    """

    @abstractmethod
    def update(self) -> None:
        """React to a change in the observed subject."""


class Subject:
    """Keep a list of observers and notify them of changes.

    Each instance owns its own list, so two subjects never share
    observers. A list (not a set) keeps notification order
    deterministic: observers are called in attach order.

    Role in the pattern: Subject.
    """

    def __init__(self) -> None:
        """Start with no observers attached."""
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Register ``observer``; attaching it twice has no effect."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Unregister ``observer``.

        Raises
        ------
        ValueError
            If ``observer`` is not attached.
        """
        if observer not in self._observers:
            raise ValueError(f"{type(observer).__name__} is not attached")
        self._observers.remove(observer)

    def notify(self) -> None:
        """Call ``update()`` on every attached observer, in attach order.

        It iterates over a copy, so an observer may detach itself (or
        others) while being notified.
        """
        for observer in list(self._observers):
            observer.update()


class KPIs(Subject):
    """Source of the support-desk key performance indicators.

    Role in the pattern: ConcreteSubject.
    """

    def __init__(self) -> None:
        """Start with every indicator at zero and no observers."""
        super().__init__()
        self._open_tickets = 0
        self._closed_tickets = 0
        self._new_tickets = 0

    @property
    def open_tickets(self) -> int:
        """Tickets currently open."""
        return self._open_tickets

    @property
    def closed_tickets(self) -> int:
        """Tickets closed in the last hour."""
        return self._closed_tickets

    @property
    def new_tickets(self) -> int:
        """Tickets opened in the last hour."""
        return self._new_tickets

    def set_kpis(
        self, open_tickets: int, closed_tickets: int, new_tickets: int
    ) -> None:
        """Store new values and notify every attached observer."""
        self._open_tickets = open_tickets
        self._closed_tickets = closed_tickets
        self._new_tickets = new_tickets
        self.notify()


class KPIObserver(Observer):
    """Base display that pulls the latest values before rendering them.

    Subclasses only implement ``display()``; the pull logic lives here
    once.

    Role in the pattern: Observer (pull-model base for KPI displays).
    """

    def __init__(self, kpis: KPISource) -> None:
        """Remember the source to pull from; values start at zero.

        Parameters
        ----------
        kpis : KPISource
            Source whose values are read on every ``update()``.
        """
        self._kpis = kpis
        self._open_tickets = 0
        self._closed_tickets = 0
        self._new_tickets = 0

    def update(self) -> None:
        """Pull the latest values from the subject, then display them."""
        self._open_tickets = self._kpis.open_tickets
        self._closed_tickets = self._kpis.closed_tickets
        self._new_tickets = self._kpis.new_tickets
        self.display()

    @abstractmethod
    def display(self) -> None:
        """Render the values pulled by the last ``update()``."""


class CurrentKPIs(KPIObserver):
    """Show the KPIs exactly as reported.

    Role in the pattern: ConcreteObserver.
    """

    def display(self) -> None:
        """Print the three indicators as reported."""
        print(f"Current open tickets: {self._open_tickets}")
        print(f"New tickets in last hour: {self._new_tickets}")
        print(f"Tickets closed in last hour: {self._closed_tickets}")
        print("*****")


class ForecastKPIs(KPIObserver):
    """Project open tickets one hour ahead, assuming rates stay the same.

    Role in the pattern: ConcreteObserver.
    """

    def expected_open_tickets(self) -> int:
        """Return open + new - closed, never below zero."""
        return max(
            0, self._open_tickets + self._new_tickets - self._closed_tickets
        )

    def display(self) -> None:
        """Print the forecast of open tickets for the next hour."""
        print(
            "Forecast open tickets in next hour: "
            f"{self.expected_open_tickets()}"
        )
        print("*****")


def client() -> None:
    """Attach two displays, publish values, then detach one."""
    kpis = KPIs()
    current = CurrentKPIs(kpis)
    forecast = ForecastKPIs(kpis)
    kpis.attach(current)
    kpis.attach(forecast)

    kpis.set_kpis(open_tickets=25, closed_tickets=10, new_tickets=5)
    kpis.set_kpis(open_tickets=100, closed_tickets=50, new_tickets=30)

    print("Detaching the forecast display")
    kpis.detach(forecast)
    kpis.set_kpis(open_tickets=50, closed_tickets=10, new_tickets=20)


if __name__ == "__main__":
    client()
