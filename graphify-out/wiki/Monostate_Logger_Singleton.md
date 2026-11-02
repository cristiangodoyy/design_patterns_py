# Monostate Logger Singleton

> 22 nodes

## Key Concepts

- **Logger** (8 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **logger_with_monostate_singleton.py** (6 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **AuditLogger** (5 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Borg** (5 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **client()** (4 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **.__init__()** (3 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **.__init__()** (3 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **.records()** (2 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **.__init_subclass__()** (2 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **.__new__()** (2 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **.log()** (2 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Share one logger state across distinct objects (Monostate / Borg). Pattern:…** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Append ``message`` to the state shared by all instances.** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Copy of every message logged so far, by any instance.** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Security log with its own shared state, separate from ``Logger``. Not thread-…** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Initialise the audit state once, labelled "audit" by default. Parameters…** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Show distinct objects that share one state per class.** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Base class whose instances of one subclass share one ``__dict__``. Not thread-…** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Give each subclass its own shared state dictionary.** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Return a new object whose ``__dict__`` is the class's shared state. The…** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Logger whose instances are distinct but share their records. Not thread-safe.…** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`
- **Initialise the shared state once; later instances reuse it.** (1 connections) — `creational/singleton/logger_with_monostate_singleton.py`

## Relationships

- [Classic Lazy Singleton](Classic_Lazy_Singleton.md) (1 shared connections)

## Source Files

- `creational/singleton/logger_with_monostate_singleton.py`

## Audit Trail

- EXTRACTED: 27 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*