# Classic Lazy Singleton

> 15 nodes

## Key Concepts

- **typing** (16 connections)
- **LazyLogger** (7 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **client()** (5 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **logger_with_classic_singleton.py** (5 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **.instance()** (3 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **.records()** (2 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **.__init__()** (2 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **.log()** (2 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Share one logger through ``__new__`` or a lazy ``instance()`` method. Pattern:…** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Return the shared logger, creating it on the first call.** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Append ``message`` to this logger's buffer.** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Copy of every message logged through this object.** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Log from two places and show that both reach the same object.** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Logger reached through an explicit, lazy ``instance()`` method. Nothing is…** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`
- **Start an empty buffer; call ``instance()`` to get the shared one.** (1 connections) — `creational/singleton/logger_with_classic_singleton.py`

## Relationships

- [Logger Records](Logger_Records.md) (2 shared connections)
- [KPI Dashboard Observer Problem](KPI_Dashboard_Observer_Problem.md) (1 shared connections)
- [KPI Dashboard Observer Solution](KPI_Dashboard_Observer_Solution.md) (1 shared connections)
- [Compiler Template Method](Compiler_Template_Method.md) (1 shared connections)
- [Travel Template Problem](Travel_Template_Problem.md) (1 shared connections)
- [Deep Copy Prototype](Deep_Copy_Prototype.md) (1 shared connections)
- [Computer Registry Prototype](Computer_Registry_Prototype.md) (1 shared connections)
- [Shallow Copy Prototype](Shallow_Copy_Prototype.md) (1 shared connections)
- [Base Class Singleton](Base_Class_Singleton.md) (1 shared connections)
- [Metaclass Singleton Logger](Metaclass_Singleton_Logger.md) (1 shared connections)
- [Monostate Logger Singleton](Monostate_Logger_Singleton.md) (1 shared connections)
- [Customer Adapter Entities](Customer_Adapter_Entities.md) (1 shared connections)

## Source Files

- `creational/singleton/logger_with_classic_singleton.py`

## Audit Trail

- EXTRACTED: 33 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*