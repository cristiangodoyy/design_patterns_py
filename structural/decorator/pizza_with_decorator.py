"""Add extra toppings to pizzas at runtime with decorators.

Pattern: Decorator (structural).
Counterpart: ``pizza_before_decorator.py``.

Notes
-----
Why:
    - A pizzeria needs a calculator for extra toppings: a customer can
      ask for more toppings on any pizza, and each one adds to the
      description and the price. That is adding a responsibility to an
      object at runtime, which is what Decorator is for.
    - Each topping wraps an ``AbsPizza`` and is an ``AbsPizza``, so
      toppings stack in any combination without a class per
      combination.
    - Prices are integer cents, so adding toppings never accumulates
      floating-point rounding errors.

When to use:
    - Responsibilities must be added to, or removed from, individual
      objects dynamically.
    - Independent extensions would otherwise cause a subclass explosion.

Trade-offs:
    - Many small objects; the final pizza is a chain of wrappers.
    - Code that checks the concrete type (``isinstance(p, VeganPizza)``)
      no longer works once the pizza is decorated; ask the pizza
      instead (``is_vegan()``), which every decorator forwards.
    - Rules the subclass hierarchy enforced by construction (no
      chicken on a vegan pizza) must now be checked at runtime:
      ``Chicken`` raises ``ValueError`` on a vegan pizza.

Related:
    - Composite shares the recursive structure, with many children.
    - Chain of Responsibility also links wrappers, but each link may
      stop the request; a decorator always forwards it.

Roles::

    AbsPizza (Component)
      ^                       ^
    VeganPizza | NonVeganPizza   PizzaDecorator (Decorator) --> AbsPizza
    (ConcreteComponent)            ^
                             Tomatoes | Chicken | ExtraCheese
                             (ConcreteDecorator)
"""

from abc import ABC, abstractmethod


class AbsPizza(ABC):
    """Pizza that can describe itself and report its price.

    Role in the pattern: Component.
    """

    @abstractmethod
    def get_description(self) -> str:
        """Return the description, including every topping."""

    @abstractmethod
    def get_price(self) -> int:
        """Return the total price in cents, including every topping."""

    @abstractmethod
    def is_vegan(self) -> bool:
        """Return whether the pizza, toppings included, is vegan."""


class VeganPizza(AbsPizza):
    """Plain vegan pizza.

    Role in the pattern: ConcreteComponent.
    """

    def get_description(self) -> str:
        """Return the base description of a vegan pizza."""
        return "Vegan pizza"

    def get_price(self) -> int:
        """Return the vegan pizza's base price in cents."""
        return 23000

    def is_vegan(self) -> bool:
        """Return ``True``: the base has no animal products."""
        return True


class NonVeganPizza(AbsPizza):
    """Plain non-vegan pizza.

    Role in the pattern: ConcreteComponent.
    """

    def get_description(self) -> str:
        """Return the base description of a non-vegan pizza."""
        return "Non-vegan pizza"

    def get_price(self) -> int:
        """Return the non-vegan pizza's base price in cents."""
        return 35000

    def is_vegan(self) -> bool:
        """Return ``False``."""
        return False


class PizzaDecorator(AbsPizza):
    """Topping that wraps another pizza.

    Role in the pattern: Decorator.

    By default it forwards both calls to the wrapped pizza unchanged;
    concrete toppings extend the results.
    """

    def __init__(self, pizza: AbsPizza) -> None:
        """Wrap ``pizza``, which may itself be decorated.

        Parameters
        ----------
        pizza : AbsPizza
            Pizza to wrap.
        """
        self._pizza = pizza

    def get_description(self) -> str:
        """Return the wrapped pizza's description, unchanged."""
        return self._pizza.get_description()

    def get_price(self) -> int:
        """Return the wrapped pizza's price, unchanged."""
        return self._pizza.get_price()

    def is_vegan(self) -> bool:
        """Return whether the wrapped pizza is vegan."""
        return self._pizza.is_vegan()


class Tomatoes(PizzaDecorator):
    """Extra tomatoes.

    Role in the pattern: ConcreteDecorator.
    """

    def get_description(self) -> str:
        """Return the wrapped description plus tomatoes."""
        return f"{super().get_description()}, tomatoes"

    def get_price(self) -> int:
        """Return the wrapped price plus the tomatoes, in cents."""
        return super().get_price() + 520


class Chicken(PizzaDecorator):
    """Extra chicken; only allowed on non-vegan pizzas.

    Role in the pattern: ConcreteDecorator.

    Parameters
    ----------
    pizza : AbsPizza
        Pizza to wrap.

    Raises
    ------
    ValueError
        If ``pizza`` is vegan.
    """

    def __init__(self, pizza: AbsPizza) -> None:
        """Wrap ``pizza`` unless it is vegan."""
        if pizza.is_vegan():
            raise ValueError(
                f"Cannot add chicken to {pizza.get_description()!r}"
            )
        super().__init__(pizza)

    def get_description(self) -> str:
        """Return the wrapped description plus chicken."""
        return f"{super().get_description()}, chicken"

    def get_price(self) -> int:
        """Return the wrapped price plus the chicken, in cents."""
        return super().get_price() + 2072


class ExtraCheese(PizzaDecorator):
    """Extra cheese.

    Role in the pattern: ConcreteDecorator.
    """

    def get_description(self) -> str:
        """Return the wrapped description plus extra cheese."""
        return f"{super().get_description()}, extra cheese"

    def get_price(self) -> int:
        """Return the wrapped price plus the extra cheese, in cents."""
        return super().get_price() + 300


def format_cents(cents: int) -> str:
    """Return ``cents`` formatted as dollars, for example ``$5.20``."""
    return f"${cents // 100}.{cents % 100:02d}"


def describe(pizza: AbsPizza) -> str:
    """Return a printable line with the pizza's description and price."""
    return f"{pizza.get_description()}: {format_cents(pizza.get_price())}"


def client() -> None:
    """Print a few pizzas with toppings stacked at runtime."""
    pizzas = (
        VeganPizza(),
        Tomatoes(VeganPizza()),
        ExtraCheese(Tomatoes(VeganPizza())),
        Chicken(NonVeganPizza()),
        Tomatoes(Chicken(Chicken(NonVeganPizza()))),
    )
    for pizza in pizzas:
        print(describe(pizza))

    try:
        Chicken(VeganPizza())
    except ValueError as error:
        print(f"Rejected: {error}")


if __name__ == "__main__":
    client()
