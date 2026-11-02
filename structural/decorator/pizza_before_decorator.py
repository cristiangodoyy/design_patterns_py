"""Price pizzas with extra toppings using one subclass per combination.

Pattern: Decorator (structural), problem side.
Counterpart: ``pizza_with_decorator.py``.

Notes
-----
Scenario:
    A pizzeria sells vegan and non-vegan pizzas, and customers can ask
    for extra tomatoes or extra chicken. Each topping adds to the
    description and the price. Here every combination is a subclass.

What goes wrong here:
    - Subclass explosion: 2 bases and 2 toppings already need 6
      classes, and each new topping roughly doubles the count.
    - Duplication: the "add tomatoes" logic is repeated in every class
      that has tomatoes; changing its price means editing them all.
    - Combinations are fixed when the class is written: a pizza object
      cannot get an extra topping at runtime, and "double chicken"
      needs yet another class.

Roles::

    AbsPizza
      ^                        ^
    VeganPizza               NonVeganPizza
      ^                        ^
    VeganPizzaWithTomatoes   NonVeganPizzaWithTomatoes
                             NonVeganPizzaWithChicken
                               ^
                             NonVeganPizzaWithChickenAndTomatoes
"""

from abc import ABC, abstractmethod


class AbsPizza(ABC):
    """Pizza that can describe itself and report its price."""

    @abstractmethod
    def get_description(self) -> str:
        """Return the description, including every topping."""

    @abstractmethod
    def get_price(self) -> int:
        """Return the total price in cents, including every topping."""


class VeganPizza(AbsPizza):
    """Plain vegan pizza."""

    def get_description(self) -> str:
        """Return the base description of a vegan pizza."""
        return "Vegan pizza"

    def get_price(self) -> int:
        """Return the vegan pizza's base price in cents."""
        return 23000


class NonVeganPizza(AbsPizza):
    """Plain non-vegan pizza."""

    def get_description(self) -> str:
        """Return the base description of a non-vegan pizza."""
        return "Non-vegan pizza"

    def get_price(self) -> int:
        """Return the non-vegan pizza's base price in cents."""
        return 35000


class VeganPizzaWithTomatoes(VeganPizza):
    """Vegan pizza with extra tomatoes."""

    def get_description(self) -> str:
        """Return the vegan description plus tomatoes."""
        return f"{super().get_description()}, tomatoes"

    def get_price(self) -> int:
        """Return the vegan price plus the tomatoes, in cents."""
        return super().get_price() + 520


class NonVeganPizzaWithTomatoes(NonVeganPizza):
    """Non-vegan pizza with extra tomatoes (tomato logic duplicated)."""

    def get_description(self) -> str:
        """Return the non-vegan description plus tomatoes."""
        return f"{super().get_description()}, tomatoes"

    def get_price(self) -> int:
        """Return the non-vegan price plus the tomatoes."""
        return super().get_price() + 520


class NonVeganPizzaWithChicken(NonVeganPizza):
    """Non-vegan pizza with extra chicken."""

    def get_description(self) -> str:
        """Return the non-vegan description plus chicken."""
        return f"{super().get_description()}, chicken"

    def get_price(self) -> int:
        """Return the non-vegan price plus the chicken, in cents."""
        return super().get_price() + 2072


class NonVeganPizzaWithChickenAndTomatoes(NonVeganPizzaWithChicken):
    """Chicken pizza with extra tomatoes (tomato logic duplicated again)."""

    def get_description(self) -> str:
        """Return the chicken pizza's description plus tomatoes."""
        return f"{super().get_description()}, tomatoes"

    def get_price(self) -> int:
        """Return the chicken pizza's price plus the tomatoes."""
        return super().get_price() + 520


def format_cents(cents: int) -> str:
    """Return ``cents`` formatted as dollars, for example ``$5.20``."""
    return f"${cents // 100}.{cents % 100:02d}"


def describe(pizza: AbsPizza) -> str:
    """Return a printable line with the pizza's description and price."""
    return f"{pizza.get_description()}: {format_cents(pizza.get_price())}"


def client() -> None:
    """Print one pizza of every predefined combination."""
    pizzas = (
        VeganPizza(),
        VeganPizzaWithTomatoes(),
        NonVeganPizza(),
        NonVeganPizzaWithTomatoes(),
        NonVeganPizzaWithChicken(),
        NonVeganPizzaWithChickenAndTomatoes(),
    )
    for pizza in pizzas:
        print(describe(pizza))


if __name__ == "__main__":
    client()
