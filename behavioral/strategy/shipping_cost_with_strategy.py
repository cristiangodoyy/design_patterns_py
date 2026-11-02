"""Calculate shipping cost with interchangeable strategy objects.

Pattern: Strategy (behavioral).
Counterpart: ``shipping_cost_before_strategy.py``.

Notes
-----
Why:
    - Each shipping algorithm lives in its own class, so ``Order`` only
      describes the order (single responsibility).
    - New shippers are new classes; ``ShippingCost`` never changes
      (open/closed).
    - The context depends on the ``AbsStrategy`` abstraction, not on
      concrete algorithms (dependency inversion).

When to use:
    - Several interchangeable algorithms solve the same task.
    - The algorithm must be chosen, or swapped, at runtime.
    - You see a long ``if/elif`` chain that selects behavior by a type
      code.

Trade-offs:
    - More classes; overkill when there are two fixed branches that will
      never grow.
    - Clients must know which strategy to pick.

Related:
    - State also delegates to an object, but states replace themselves;
      a strategy is chosen from outside.
    - Template Method varies steps through inheritance; Strategy varies
      the whole algorithm through composition.

Roles::

    ShippingCost (Context) ----> AbsStrategy (Strategy)
                                       ^
                 FedExStrategy | UPSStrategy | PostalStrategy
                              (ConcreteStrategy)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    """Order to be shipped; it no longer knows how it travels.

    Role in the pattern: data passed to every strategy.
    """

    customer: str


class AbsStrategy(ABC):
    """Contract shared by every shipping algorithm.

    Role in the pattern: Strategy.
    """

    @abstractmethod
    def calculate(self, order: Order) -> int:
        """Return the shipping cost for ``order``.

        Parameters
        ----------
        order : Order
            Order being shipped.

        Returns
        -------
        int
            Cost in US cents.
        """


class FedExStrategy(AbsStrategy):
    """FedEx flat rate.

    Role in the pattern: ConcreteStrategy.
    """

    def calculate(self, order: Order) -> int:
        """Return the FedEx flat rate, whatever the order."""
        return 300


class UPSStrategy(AbsStrategy):
    """UPS flat rate.

    Role in the pattern: ConcreteStrategy.
    """

    def calculate(self, order: Order) -> int:
        """Return the UPS flat rate, whatever the order."""
        return 400


class PostalStrategy(AbsStrategy):
    """Postal service flat rate.

    Role in the pattern: ConcreteStrategy.
    """

    def calculate(self, order: Order) -> int:
        """Return the postal flat rate, whatever the order."""
        return 500


class ShippingCost:
    """Compute costs by delegating to the injected strategy.

    Role in the pattern: Context.
    """

    def __init__(self, strategy: AbsStrategy) -> None:
        """Use ``strategy`` until it is replaced.

        Parameters
        ----------
        strategy : AbsStrategy
            Shipping algorithm to delegate to.
        """
        self._strategy = strategy

    @property
    def strategy(self) -> AbsStrategy:
        """Algorithm currently used; it can be replaced at runtime."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbsStrategy) -> None:
        """Replace the algorithm used by the next calculations."""
        self._strategy = strategy

    def shipping_cost(self, order: Order) -> int:
        """Delegate the calculation to the current strategy."""
        return self._strategy.calculate(order)


def format_cents(cents: int) -> str:
    """Return ``cents`` formatted as dollars, for example ``$5.20``."""
    return f"${cents // 100}.{cents % 100:02d}"


def client() -> None:
    """Compute one order's cost with each strategy, swapped at runtime."""
    order = Order("Ada")
    strategies: tuple[AbsStrategy, ...] = (
        FedExStrategy(),
        UPSStrategy(),
        PostalStrategy(),
    )
    calculator = ShippingCost(strategies[0])
    for strategy in strategies:
        calculator.strategy = strategy
        cost = calculator.shipping_cost(order)
        print(f"{type(strategy).__name__}: {format_cents(cost)}")


if __name__ == "__main__":
    client()
