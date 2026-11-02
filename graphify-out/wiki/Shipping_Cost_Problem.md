# Shipping Cost Problem

> 27 nodes

## Key Concepts

- **Order** (10 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **ShippingCost** (7 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **.shipping_cost()** (7 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **shipping_cost_before_strategy.py** (7 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Shipper** (5 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **client()** (5 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **.shipper()** (4 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **._fedex_cost()** (4 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **._postal_cost()** (4 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **._ups_cost()** (4 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **format_cents()** (3 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **.__init__()** (3 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **.customer()** (2 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **StrEnum** (1 connections)
- **Calculate shipping cost by branching on the order's shipper. Pattern: Strategy…** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Return the FedEx flat rate in cents.** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Return the UPS flat rate in cents.** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Return the postal service flat rate in cents.** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Return ``cents`` formatted as dollars, for example ``$5.20``.** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Compute the cost of one order per shipper.** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Shipping companies known to the calculator.** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Order that also knows how it will be shipped. Holding the shipper here mixes…** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Store who placed the order and which company ships it. Parameters ----------…** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Name of the customer who placed the order.** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- **Shipping company chosen for the order.** (1 connections) — `behavioral/strategy/shipping_cost_before_strategy.py`
- *... and 2 more nodes in this community*

## Relationships

- [Computer State Problem](Computer_State_Problem.md) (1 shared connections)

## Source Files

- `behavioral/strategy/shipping_cost_before_strategy.py`

## Audit Trail

- EXTRACTED: 39 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*