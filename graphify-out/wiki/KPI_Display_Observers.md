# KPI Display Observers

> 10 nodes

## Key Concepts

- **client()** (6 connections) — `behavioral/observer/kpi_dashboard_with_observer.py`
- **CurrentKPIs** (5 connections) — `behavioral/observer/kpi_dashboard_with_observer.py`
- **.set_kpis()** (4 connections) — `behavioral/observer/kpi_dashboard_with_observer.py`
- **.notify()** (3 connections) — `behavioral/observer/kpi_dashboard_with_observer.py`
- **.display()** (2 connections) — `behavioral/observer/kpi_dashboard_with_observer.py`
- **Call ``update()`` on every attached observer, in attach order. It iterates over…** (1 connections) — `behavioral/observer/kpi_dashboard_with_observer.py`
- **Store new values and notify every attached observer.** (1 connections) — `behavioral/observer/kpi_dashboard_with_observer.py`
- **Show the KPIs exactly as reported. Role in the pattern: ConcreteObserver.** (1 connections) — `behavioral/observer/kpi_dashboard_with_observer.py`
- **Print the three indicators as reported.** (1 connections) — `behavioral/observer/kpi_dashboard_with_observer.py`
- **Attach two displays, publish values, then detach one.** (1 connections) — `behavioral/observer/kpi_dashboard_with_observer.py`

## Relationships

- [KPI Dashboard Observer Solution](KPI_Dashboard_Observer_Solution.md) (3 shared connections)
- [KPI Classes](KPI_Classes.md) (2 shared connections)
- [KPI Observer Base](KPI_Observer_Base.md) (1 shared connections)
- [Forecast KPIs](Forecast_KPIs.md) (1 shared connections)

## Source Files

- `behavioral/observer/kpi_dashboard_with_observer.py`

## Audit Trail

- EXTRACTED: 15 (94%)
- INFERRED: 1 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*