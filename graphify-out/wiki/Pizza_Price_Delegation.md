# Pizza Price Delegation

> 6 nodes

## Key Concepts

- **.get_price()** (5 connections) — `structural/decorator/pizza_with_decorator.py`
- **.get_price()** (3 connections) — `structural/decorator/pizza_with_decorator.py`
- **.get_price()** (3 connections) — `structural/decorator/pizza_with_decorator.py`
- **Return the wrapped pizza's price, unchanged.** (1 connections) — `structural/decorator/pizza_with_decorator.py`
- **Return the wrapped price plus the chicken, in cents.** (1 connections) — `structural/decorator/pizza_with_decorator.py`
- **Return the wrapped price plus the extra cheese, in cents.** (1 connections) — `structural/decorator/pizza_with_decorator.py`

## Relationships

- [Pizza Decorator Toppings](Pizza_Decorator_Toppings.md) (2 shared connections)
- [Extra Cheese Decorator](Extra_Cheese_Decorator.md) (1 shared connections)
- [Pizza Decorator Wrappers](Pizza_Decorator_Wrappers.md) (1 shared connections)

## Source Files

- `structural/decorator/pizza_with_decorator.py`

## Audit Trail

- EXTRACTED: 9 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*