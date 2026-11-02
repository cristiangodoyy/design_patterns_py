"""Share one logger state across distinct objects (Monostate / Borg).

Pattern: Singleton (creational), Monostate (Borg) variant.
Counterpart: ``logger_before_singleton.py``; sibling variants
``logger_with_classic_singleton.py``,
``logger_with_base_class_singleton.py`` and
``logger_with_metaclass_singleton.py``.

Notes
-----
Why:
    - What callers usually need is one *state*, not one *object*. Here
      ``Logger()`` builds a new object every time, but every object's
      ``__dict__`` is the same dictionary, so they all see the same
      records.
    - ``__init_subclass__`` gives each subclass its own shared
      dictionary, so ``Logger`` and ``AuditLogger`` do not mix their
      state (one dictionary on the base class would merge them).
    - Callers keep the normal ``Logger()`` syntax and may even subclass
      it freely.

When to use:
    - Callers only need consistent shared state, not a single object
      identity (nothing relies on ``is`` or on identity-based caches).
    - You want singleton behaviour without controlling object creation.

Trade-offs:
    - ``a is b`` is ``False``, which surprises readers who expect a
      singleton; identity-based caches or ``is`` checks will not work.
    - ``__init__`` still runs on every call, so it must not reset state
      that already exists (``Logger.__init__`` checks first).
    - Not thread-safe: the first initialisation and the shared mutable
      state need a lock if several threads use the logger.
    - Classes with ``__slots__`` have no ``__dict__`` to share.

Related:
    - Classic, base-class and metaclass variants share identity.
    - Flyweight also shares state, but only the intrinsic part.

Roles::

    Logger() #1 ---+--> Logger._shared_state       (Monostate)
    Logger() #2 ---+
    AuditLogger()  ---> AuditLogger._shared_state  (separate state)
"""

from typing import ClassVar, Self


class Borg:
    """Base class whose instances of one subclass share one ``__dict__``.

    Not thread-safe. Meant to be subclassed, not instantiated directly.

    Role in the pattern: Monostate machinery.
    """

    _shared_state: ClassVar[dict[str, object]]

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Give each subclass its own shared state dictionary."""
        super().__init_subclass__(**kwargs)
        cls._shared_state = {}

    def __new__(cls, *args: object, **kwargs: object) -> Self:
        """Return a new object whose ``__dict__`` is the class's shared state.

        The arguments are accepted only so that ``Logger("app")`` reaches
        ``__init__``; they are not used here.
        """
        instance = super().__new__(cls)
        instance.__dict__ = cls._shared_state
        return instance


class Logger(Borg):
    """Logger whose instances are distinct but share their records.

    Not thread-safe.

    Role in the pattern: Monostate.

    Parameters
    ----------
    name : str, default="app"
        Label of the log. Only the first call's value is kept.
    """

    name: str
    _records: list[str]

    def __init__(self, name: str = "app") -> None:
        """Initialise the shared state once; later instances reuse it."""
        if "_records" in self.__dict__:
            return
        self.name = name
        self._records = []

    def log(self, message: str) -> None:
        """Append ``message`` to the state shared by all instances."""
        self._records.append(f"[{self.name}] {message}")

    @property
    def records(self) -> list[str]:
        """Copy of every message logged so far, by any instance."""
        return list(self._records)


class AuditLogger(Logger):
    """Security log with its own shared state, separate from ``Logger``.

    Not thread-safe.

    Role in the pattern: Monostate.
    """

    def __init__(self, name: str = "audit") -> None:
        """Initialise the audit state once, labelled "audit" by default.

        Parameters
        ----------
        name : str, default="audit"
            Label of the log. Only the first call's value is kept.
        """
        super().__init__(name)


def client() -> None:
    """Show distinct objects that share one state per class."""
    a, b = Logger(), Logger()
    a.log("order 42: created")
    b.log("order 42: card charged")
    print(f"a is b: {a is b}")
    print(f"a and b share state: {a.__dict__ is b.__dict__}")
    print(f"Records seen through a: {a.records}")

    audit = AuditLogger()
    audit.log("user ada: logged in")
    print(
        f"Logger and AuditLogger share state: {audit.__dict__ is a.__dict__}"
    )
    print(f"Audit records: {audit.records}")


if __name__ == "__main__":
    client()
