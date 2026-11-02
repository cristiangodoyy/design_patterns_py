"""Make loggers singletons by inheriting from a reusable base class.

Pattern: Singleton (creational), base-class variant.
Counterpart: ``logger_before_singleton.py``; sibling variants
``logger_with_classic_singleton.py``,
``logger_with_metaclass_singleton.py`` and
``logger_with_monostate_singleton.py``.

Notes
-----
Why:
    - The "only one instance" logic is written once in ``Singleton``
      and reused by every class that inherits from it.
    - Instances are keyed by the concrete class, so each subclass gets
      its own single instance: ``Logger()`` and ``AuditLogger()`` are
      two different objects, each shared by all of its callers.

When to use:
    - Several unrelated classes must each have exactly one instance.
    - You prefer plain inheritance over a metaclass.

Trade-offs:
    - Python calls ``__init__`` on *every* ``Logger()`` call, even when
      ``__new__`` returns the existing object. Without a guard, the
      second call would reset the state; ``Logger.__init__`` therefore
      returns early once initialised, and later arguments are ignored.
    - Not thread-safe: two threads can both miss the lookup and create
      two instances. See the metaclass variant for a locked version.
    - The singleton logic leaks into the class hierarchy, and each
      subclass must remember the ``__init__`` guard.

Related:
    - The metaclass variant moves the same registry out of the
      hierarchy and skips ``__init__`` on repeated calls for free.
    - Monostate (Borg) shares state instead of identity.

Roles::

    Singleton.__new__ --> _instances[cls]       (reusable machinery)
         ^
       Logger            --> one Logger         (Singleton)
         ^
       AuditLogger       --> one AuditLogger    (Singleton)
"""

from typing import ClassVar, Self


class Singleton:
    """Base class that keeps one instance per concrete subclass.

    Not thread-safe.

    Role in the pattern: reusable Singleton machinery.
    """

    _instances: ClassVar[dict[type, object]] = {}
    _initialized: bool = False

    def __new__(cls, *args: object, **kwargs: object) -> Self:
        """Return the existing instance of ``cls``, creating it on first use.

        The arguments are accepted only so that ``Logger("app")`` reaches
        ``__init__``; they are not used here.
        """
        # Look up the concrete class, so subclasses do not share one
        # instance; ``isinstance`` also narrows the stored object.
        instance = Singleton._instances.get(cls)
        if not isinstance(instance, cls):
            instance = super().__new__(cls)
            Singleton._instances[cls] = instance
        return instance


class Logger(Singleton):
    """Application logger; one instance per class.

    Role in the pattern: Singleton.

    Parameters
    ----------
    name : str, default="app"
        Label of the log. Only the first call's value is kept.
    """

    def __init__(self, name: str = "app") -> None:
        """Initialise the shared state once; later calls change nothing."""
        if self._initialized:
            return
        self._initialized = True
        self.name = name
        self._records: list[str] = []

    def log(self, message: str) -> None:
        """Append ``message`` to the shared buffer."""
        self._records.append(f"[{self.name}] {message}")

    @property
    def records(self) -> list[str]:
        """Copy of every message logged so far, by anyone."""
        return list(self._records)


class AuditLogger(Logger):
    """Separate log for security events, with its own single instance.

    Role in the pattern: Singleton.
    """

    def __init__(self, name: str = "audit") -> None:
        """Initialise the audit log once, labelled "audit" by default.

        Parameters
        ----------
        name : str, default="audit"
            Label of the log. Only the first call's value is kept.
        """
        super().__init__(name)


def client() -> None:
    """Show one shared instance per class and a guarded ``__init__``."""
    logger = Logger()
    logger.log("order 42: created")
    again = Logger("ignored")
    again.log("order 42: card charged")
    print(f"Logger() is Logger('ignored'): {logger is again}")
    print(f"Name kept from the first call: {again.name!r}")
    print(f"Records survived the second call: {again.records}")

    audit = AuditLogger()
    audit.log("user ada: logged in")
    print(f"AuditLogger() is AuditLogger(): {audit is AuditLogger()}")
    print(f"Logger() is AuditLogger(): {logger is audit}")
    print(f"Audit records: {audit.records}")


if __name__ == "__main__":
    client()
