"""Make a logger a thread-safe singleton with a metaclass.

Pattern: Singleton (creational), metaclass variant.
Counterpart: ``logger_before_singleton.py``; sibling variants
``logger_with_classic_singleton.py``,
``logger_with_base_class_singleton.py`` and
``logger_with_monostate_singleton.py``.

Notes
-----
Why:
    - A metaclass is the class of a class: its ``__call__`` runs when
      someone writes ``Logger(...)``. Overriding it decides whether a
      new object is built at all.
    - The singleton rule lives entirely in ``SingletonMeta``; ``Logger``
      only declares ``metaclass=SingletonMeta`` and stays a plain
      logger (clean separation of concerns).
    - When the instance already exists, ``__call__`` returns it without
      calling ``__init__`` again. ``__init__`` runs exactly once, so
      arguments passed on later calls are silently ignored.
    - Thread-safe: creation is guarded by a ``threading.Lock`` with
      double-checked locking, so concurrent first calls still build a
      single instance.

When to use:
    - Several classes need the singleton rule and must keep their own
      ``__init__`` free of guards.
    - Instances may be requested from several threads.

Trade-offs:
    - Metaclasses are less familiar than inheritance and conflict with
      other metaclasses (e.g. ``ABCMeta``) unless combined.
    - Ignoring later constructor arguments can surprise callers; one
      ``threading.Lock`` is shared by all classes, so a singleton whose
      ``__init__`` builds another singleton would deadlock.
    - Still global state: tests must reset ``_instances`` to stay
      independent.

Related:
    - The base-class variant puts the same registry in the hierarchy.
    - Monostate (Borg) shares state instead of identity.

Roles::

    Logger(...) --> SingletonMeta.__call__   (metaclass, holds lock)
                        |  first call: type.__call__ -> __init__
                        |  later calls: return cached instance
                        v
                    the one Logger           (Singleton)
"""

import threading

from concurrent.futures import ThreadPoolExecutor
from typing import ClassVar


class SingletonMeta(type):
    """Metaclass that lets each of its classes build only one instance.

    Thread-safe.

    Role in the pattern: Singleton machinery (metaclass).
    """

    _instances: ClassVar[dict[type, object]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __call__[T](cls: type[T], *args: object, **kwargs: object) -> T:
        """Return the class's single instance, creating it once.

        Parameters
        ----------
        *args
            Forwarded to ``__init__`` on the first call only.
        **kwargs
            Forwarded to ``__init__`` on the first call only.

        Returns
        -------
        T
            The shared instance of ``cls``.
        """
        instance = SingletonMeta._instances.get(cls)
        if isinstance(instance, cls):  # fast path: no lock once built
            return instance
        with SingletonMeta._lock:
            # Check again: another thread may have built it while this
            # one was waiting for the lock.
            instance = SingletonMeta._instances.get(cls)
            if not isinstance(instance, cls):
                instance = type.__call__(cls, *args, **kwargs)
                SingletonMeta._instances[cls] = instance
        return instance


class Logger(metaclass=SingletonMeta):
    """Plain logger; the metaclass makes it a singleton.

    Thread-safe creation; ``__init__`` runs only once.

    Role in the pattern: Singleton.

    Parameters
    ----------
    name : str, default="app"
        Label of the log. Only the first call's value is used.
    """

    def __init__(self, name: str = "app") -> None:
        """Set up the buffer and its lock; the metaclass runs this once."""
        self.name = name
        self._records: list[str] = []
        self._records_lock = threading.Lock()

    def log(self, message: str) -> None:
        """Append ``message`` to the shared buffer, safely across threads."""
        with self._records_lock:
            self._records.append(f"[{self.name}] {message}")

    @property
    def records(self) -> list[str]:
        """Copy of every message logged so far, by anyone."""
        with self._records_lock:
            return list(self._records)


def client() -> None:
    """Build the logger from many threads, then show ignored arguments."""
    with ThreadPoolExecutor(max_workers=8) as pool:
        loggers = list(pool.map(lambda _: Logger(), range(32)))
    first = loggers[0]
    print(f"32 threads got one instance: {all(x is first for x in loggers)}")

    first.log("order 42: created")
    later = Logger("ignored")
    later.log("order 42: card charged")
    print(f"Logger() is Logger('ignored'): {later is first}")
    print(f"__init__ ran once, name is still {later.name!r}")
    print(f"Shared log: {later.records}")


if __name__ == "__main__":
    client()
