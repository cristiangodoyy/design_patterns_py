"""Let every module create its own logger and lose the full story.

Pattern: Singleton (creational), problem side.
Counterpart: ``logger_with_classic_singleton.py``,
``logger_with_base_class_singleton.py``,
``logger_with_metaclass_singleton.py`` and
``logger_with_monostate_singleton.py``.

Notes
-----
Scenario:
    An online shop records what happens during checkout. The order
    module and the payment module both need to log, and an operator
    later reads "the log" to understand what happened to an order.

What goes wrong here:
    - Each module calls ``Logger()`` and gets its own object with its
      own buffer, so the lines of one checkout end up split across two
      places and their relative order is lost.
    - Whoever reads one logger sees half the story; nothing in the code
      says there is a second buffer to look at.
    - With a real file handle the problem is worse: two handles opened
      in write mode on the same file truncate and overwrite each other.
    - Passing one logger to every function would fix it, but every
      signature on the call path then has to carry it.

Roles::

    order module   ---> Logger()  #1 ---> buffer A: "order created", ...
    payment module ---> Logger()  #2 ---> buffer B: "card charged", ...
                        (two objects, the log is split)
"""


class Logger:
    """Logger that keeps its records in a private in-memory buffer.

    Not a singleton: every ``Logger()`` call creates a new, empty buffer.
    Thread safety is not the issue here: nothing is shared at all.
    """

    def __init__(self) -> None:
        """Start a new, empty buffer of this logger's own."""
        self._records: list[str] = []

    def log(self, message: str) -> None:
        """Append ``message`` to this logger's buffer."""
        self._records.append(message)

    @property
    def records(self) -> list[str]:
        """Copy of the messages logged through this object."""
        return list(self._records)


def create_order(order_id: int) -> None:
    """Order module: logs through a logger of its own."""
    logger = Logger()
    logger.log(f"order {order_id}: created")
    charge_card(order_id)
    logger.log(f"order {order_id}: confirmed")
    print(f"Order module log:   {logger.records}")


def charge_card(order_id: int) -> None:
    """Payment module: logs through another, unrelated logger."""
    logger = Logger()
    logger.log(f"order {order_id}: card charged")
    print(f"Payment module log: {logger.records}")


def client() -> None:
    """Run one checkout and show that its log is split in two."""
    create_order(42)
    first, second = Logger(), Logger()
    print(f"Logger() is Logger(): {first is second}")


if __name__ == "__main__":
    client()
