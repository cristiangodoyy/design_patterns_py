"""Publish support-desk KPIs to a hard-coded list of displays.

Pattern: Observer (behavioral), problem side.
Counterpart: ``kpi_dashboard_with_observer.py``.

Notes
-----
Scenario:
    A support center tracks three key performance indicators (open
    tickets, tickets opened in the last hour and tickets closed in the
    last hour). Every time new values arrive, two displays must be
    refreshed: one shows the values as reported, the other forecasts
    the open tickets for the next hour.

What goes wrong here:
    - ``Dashboard`` knows every consumer and calls each one itself, so
      the source of the data is coupled to the code that shows it.
    - Open/closed: a new display means one more private method and one
      more call in ``publish``; the class is never closed.
    - Consumers cannot be added or removed at runtime; the list is
      fixed when the class is written.
    - ``_print_current`` branches on the KPI name, so a new indicator
      also means editing the ``if/elif`` chain.

Roles::

    client ---> Dashboard.publish(kpis)
                  _print_current(kpis)    (consumer 1, hard-coded)
                  _print_forecast(kpis)   (consumer 2, hard-coded)
"""

from collections.abc import Sequence
from enum import StrEnum, auto
from typing import NamedTuple


class KPIName(StrEnum):
    """Indicators reported by the support center."""

    NEW = auto()
    OPEN = auto()
    CLOSED = auto()


class KPI(NamedTuple):
    """One named indicator value."""

    name: KPIName
    value: int


class Dashboard:
    """Publish KPIs to a fixed, hard-coded list of consumers."""

    def publish(self, kpis: Sequence[KPI]) -> None:
        """Send ``kpis`` to every consumer known to this class.

        Each new consumer needs one more call here and one more private
        method below, so the class is never closed for modification.

        Parameters
        ----------
        kpis : Sequence of KPI
            Latest values of every indicator.
        """
        self._print_current(kpis)
        self._print_forecast(kpis)

    def _print_current(self, kpis: Sequence[KPI]) -> None:
        """Print every KPI exactly as reported, one line per indicator.

        This is consumer 1, hard-coded into the dashboard. It branches on
        ``kpi.name``, so a new indicator also means a new ``elif`` here.

        Parameters
        ----------
        kpis : Sequence of KPI
            Latest values of every indicator.
        """
        for kpi in kpis:
            if kpi.name == KPIName.OPEN:
                print(f"Current open tickets: {kpi.value}")
            elif kpi.name == KPIName.NEW:
                print(f"New tickets in last hour: {kpi.value}")
            elif kpi.name == KPIName.CLOSED:
                print(f"Tickets closed in last hour: {kpi.value}")
        print("*****")

    def _print_forecast(self, kpis: Sequence[KPI]) -> None:
        """Print the open tickets expected in the next hour.

        This is consumer 2, also hard-coded: open + new - closed, never
        below zero.

        Parameters
        ----------
        kpis : Sequence of KPI
            Latest values; must include the open, new and closed indicators.
        """
        values = {kpi.name: kpi.value for kpi in kpis}
        expected_open = max(
            0,
            values[KPIName.OPEN]
            + values[KPIName.NEW]
            - values[KPIName.CLOSED],
        )
        print(f"Forecast open tickets in next hour: {expected_open}")
        print("*****")


def client() -> None:
    """Publish one round of KPI values."""
    kpis = [
        KPI(KPIName.OPEN, 25),
        KPI(KPIName.NEW, 5),
        KPI(KPIName.CLOSED, 10),
    ]
    Dashboard().publish(kpis)


if __name__ == "__main__":
    client()
