"""Share one logger through ``__new__`` or a lazy ``instance()`` method.

Pattern: Singleton (creational), classic variant.
Counterpart: ``logger_before_singleton.py``; sibling variants
``logger_with_base_class_singleton.py``,
``logger_with_metaclass_singleton.py`` and
``logger_with_monostate_singleton.py``.

Notes
-----
Why:
    - Every module that needs to log gets the *same* object, so all
      records of one checkout land in one buffer, in order.
    - Nobody has to pass the logger through every function signature.
    - Two classic spellings are shown:

      * ``Logger`` overrides ``__new__``: ``Logger()`` itself returns
        the shared object, so callers cannot get it wrong.
      * ``LazyLogger`` follows the GoF book: an explicit
        ``instance()`` class method creates the object on first use
        (lazy instantiation) and returns it afterwards.

When to use:
    - Exactly one instance must exist (a log sink, a configuration, a
      hardware handle) and many unrelated modules need to reach it.
    - The single class is final; for reusable machinery see the
      base-class and metaclass variants.

Trade-offs:
    - Not thread-safe: both spellings use check-then-create, so two
      threads arriving together can each build an instance. See the
      metaclass variant for a locked version.
    - ``LazyLogger`` relies on a convention: ``LazyLogger()`` still
      builds a fresh, unshared object.
    - A singleton is global state in disguise: it hides dependencies
      and leaks state between tests unless they reset it.

Related:
    - Monostate (Borg) shares state instead of identity.
    - Abstract Factory, Builder and Facade objects are often singletons.

Roles::

    module A ---+--> Logger()              --> the one Logger
    module B ---+    LazyLogger.instance() --> the one LazyLogger
                                               (Singleton)
"""

from typing import ClassVar, final


@final
class Logger:
    """Logger whose constructor always returns the same object.

    The instance is created on the first ``Logger()`` call and stored on
    the class. Not thread-safe.

    Role in the pattern: Singleton.
    """

    _instance: ClassVar["Logger | None"] = None
    _records: list[str]

    def __new__(cls) -> "Logger":
        """Return the shared logger, creating it and its buffer once."""
        if cls._instance is None:
            instance = super().__new__(cls)
            # State lives here, not in __init__: Python calls __init__
            # on every Logger() call, which would wipe the records.
            instance._records = []
            cls._instance = instance
        return cls._instance

    def log(self, message: str) -> None:
        """Append ``message`` to the shared buffer."""
        self._records.append(message)

    @property
    def records(self) -> list[str]:
        """Copy of every message logged so far, by anyone."""
        return list(self._records)


@final
class LazyLogger:
    """Logger reached through an explicit, lazy ``instance()`` method.

    Nothing is built until the first ``instance()`` call. Not
    thread-safe, and ``LazyLogger()`` bypasses the singleton.

    Role in the pattern: Singleton.
    """

    _instance: ClassVar["LazyLogger | None"] = None

    def __init__(self) -> None:
        """Start an empty buffer; call ``instance()`` to get the shared one."""
        self._records: list[str] = []

    @classmethod
    def instance(cls) -> "LazyLogger":
        """Return the shared logger, creating it on the first call."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def log(self, message: str) -> None:
        """Append ``message`` to this logger's buffer."""
        self._records.append(message)

    @property
    def records(self) -> list[str]:
        """Copy of every message logged through this object."""
        return list(self._records)


def client() -> None:
    """Log from two places and show that both reach the same object."""
    orders, payments = Logger(), Logger()
    orders.log("order 42: created")
    payments.log("order 42: card charged")
    print(f"Logger() is Logger(): {orders is payments}")
    print(f"Shared log: {orders.records}")

    print(f"LazyLogger built yet: {LazyLogger._instance is not None}")
    first, second = LazyLogger.instance(), LazyLogger.instance()
    print(f"LazyLogger built yet: {LazyLogger._instance is not None}")
    print(f"instance() is instance(): {first is second}")
    print(f"LazyLogger() is instance(): {LazyLogger() is first}")


if __name__ == "__main__":
    client()
