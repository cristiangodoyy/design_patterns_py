# Logger Records

> 8 nodes

## Key Concepts

- **Logger** (6 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **.records()** (2 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **.log()** (2 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **.__new__()** (2 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Logger whose constructor always returns the same object. The instance is…** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Return the shared logger, creating it and its buffer once.** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Append ``message`` to the shared buffer.** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Copy of every message logged so far, by anyone.** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`

## Relationships

- [Classic Lazy Singleton](Classic_Lazy_Singleton.md) (2 shared connections)

## Source Files

- `creational/singleton/logger_with_classic_singleton.py`

## Audit Trail

- EXTRACTED: 9 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*