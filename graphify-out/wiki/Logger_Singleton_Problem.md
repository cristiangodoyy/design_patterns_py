# Logger Singleton Problem

> 16 nodes

## Key Concepts

- **Logger** (8 connections) — `creational/singleton/logger_before_singleton.py`
- **create_order()** (5 connections) — `creational/singleton/logger_before_singleton.py`
- **logger_before_singleton.py** (5 connections) — `creational/singleton/logger_before_singleton.py`
- **charge_card()** (4 connections) — `creational/singleton/logger_before_singleton.py`
- **client()** (4 connections) — `creational/singleton/logger_before_singleton.py`
- **.records()** (2 connections) — `creational/singleton/logger_before_singleton.py`
- **.__init__()** (2 connections) — `creational/singleton/logger_before_singleton.py`
- **.log()** (2 connections) — `creational/singleton/logger_before_singleton.py`
- **Let every module create its own logger and lose the full story. Pattern:…** (1 connections) — `creational/singleton/logger_before_singleton.py`
- **Logger that keeps its records in a private in-memory buffer. Not a singleton:…** (1 connections) — `creational/singleton/logger_before_singleton.py`
- **Start a new, empty buffer of this logger's own.** (1 connections) — `creational/singleton/logger_before_singleton.py`
- **Append ``message`` to this logger's buffer.** (1 connections) — `creational/singleton/logger_before_singleton.py`
- **Copy of the messages logged through this object.** (1 connections) — `creational/singleton/logger_before_singleton.py`
- **Order module: logs through a logger of its own.** (1 connections) — `creational/singleton/logger_before_singleton.py`
- **Payment module: logs through another, unrelated logger.** (1 connections) — `creational/singleton/logger_before_singleton.py`
- **Run one checkout and show that its log is split in two.** (1 connections) — `creational/singleton/logger_before_singleton.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `creational/singleton/logger_before_singleton.py`

## Audit Trail

- EXTRACTED: 20 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*