# Schedule Server Facade Problem

> 38 nodes

## Key Concepts

- **Bootloader** (8 connections) — `structural/facade/schedule_server_before_facade.py`
- **client()** (7 connections) — `structural/facade/schedule_server_before_facade.py`
- **schedule_server_before_facade.py** (7 connections) — `structural/facade/schedule_server_before_facade.py`
- **ExecutionContext** (5 connections) — `structural/facade/schedule_server_before_facade.py`
- **ListenerRegistry** (5 connections) — `structural/facade/schedule_server_before_facade.py`
- **SystemObjects** (5 connections) — `structural/facade/schedule_server_before_facade.py`
- **ProcessManager** (4 connections) — `structural/facade/schedule_server_before_facade.py`
- **.destroy()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.init()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.read_system_config_file()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.shutdown()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.start_booting()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.destroy_context()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.initialize_context()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.destroy_listeners()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.initialize_listeners()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.release_processes()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.create_system_objects()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **.destroy_system_objects()** (2 connections) — `structural/facade/schedule_server_before_facade.py`
- **Start and stop a schedule server by calling every subsystem step. Pattern:…** (1 connections) — `structural/facade/schedule_server_before_facade.py`
- **Worker processes that run the jobs.** (1 connections) — `structural/facade/schedule_server_before_facade.py`
- **Release the worker processes (first step of shutdown).** (1 connections) — `structural/facade/schedule_server_before_facade.py`
- **Run the server the hard way: the client orchestrates every step.** (1 connections) — `structural/facade/schedule_server_before_facade.py`
- **Boot sequence and final power-off of the server.** (1 connections) — `structural/facade/schedule_server_before_facade.py`
- **Begin the boot sequence (first step of startup).** (1 connections) — `structural/facade/schedule_server_before_facade.py`
- *... and 13 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `structural/facade/schedule_server_before_facade.py`

## Audit Trail

- EXTRACTED: 42 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*