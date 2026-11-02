"""Drive a computer's power states with one object per state.

Pattern: State (behavioral).
Counterpart: ``state_power_before_state.py``.

Notes
-----
Why:
    - Each power state is a class that implements every action for
      that state, so the behavior of one state lives in one place.
    - Each action returns the next state; ``Computer`` (the context)
      just delegates and swaps its current state, with no branching.
    - Actions a state does not override are rejected by the base
      class, so the allowed transitions are explicit per state.
    - A new state is a new class; existing states only change if they
      can transition to it (open/closed).

When to use:
    - An object's behavior depends on its state and must change at
      runtime when the state changes.
    - Methods have large conditionals over the same status code.

Trade-offs:
    - More classes; overkill for two states with trivial behavior.
    - States know their successors, so they are coupled to each other.

Related:
    - Strategy has the same shape, but a strategy is chosen from
      outside and does not replace itself.
    - States without fields can be shared as Singletons or Flyweights.

Roles::

    Computer (Context) ---current state---> ComputerState (State)
                                               ^
                              Off | On | Suspended | Hibernated
                                       (ConcreteState)
"""

from abc import ABC, abstractmethod


class InvalidTransitionError(ValueError):
    """Raised when an action is not allowed in the current state.

    Role in the pattern: error raised by a State that rejects an action.
    """


class ComputerState(ABC):
    """Behavior of the computer in one power state.

    Each action returns the next state. Actions a state does not
    override are rejected.

    Role in the pattern: State.
    """

    @property
    def name(self) -> str:
        """Human-readable name of the state."""
        return type(self).__name__

    @property
    @abstractmethod
    def on_enter(self) -> str:
        """Message shown when the computer enters this state."""

    @abstractmethod
    def power_button(self) -> "ComputerState":
        """Return the state reached by pressing the power button."""

    def suspend(self) -> "ComputerState":
        """Return the state reached by suspending.

        Raises
        ------
        InvalidTransitionError
            Unless a concrete state allows it.
        """
        raise InvalidTransitionError(f"Cannot suspend while {self.name}")

    def hibernate(self) -> "ComputerState":
        """Return the state reached by hibernating.

        Raises
        ------
        InvalidTransitionError
            Unless a concrete state allows it.
        """
        raise InvalidTransitionError(f"Cannot hibernate while {self.name}")

    def __str__(self) -> str:
        """Return the state's name, used when printing transitions."""
        return self.name


class Off(ComputerState):
    """Computer is powered down.

    Role in the pattern: ConcreteState.
    """

    @property
    def on_enter(self) -> str:
        """Message for a computer that has just been powered off."""
        return "Powered off"

    def power_button(self) -> ComputerState:
        """Turn the computer on."""
        return On()


class On(ComputerState):
    """Computer is powered up and running.

    Role in the pattern: ConcreteState.
    """

    @property
    def on_enter(self) -> str:
        """Message for a computer that has just started running."""
        return "Up and running"

    def power_button(self) -> ComputerState:
        """Turn the computer off."""
        return Off()

    def suspend(self) -> ComputerState:
        """Go to sleep, keeping the memory powered."""
        return Suspended()

    def hibernate(self) -> ComputerState:
        """Save the memory to disk and power down."""
        return Hibernated()


class Suspended(ComputerState):
    """Computer is sleeping with its memory powered.

    Role in the pattern: ConcreteState.
    """

    @property
    def on_enter(self) -> str:
        """Message for a computer that has just gone to sleep."""
        return "Sleeping, memory kept powered"

    def power_button(self) -> ComputerState:
        """Wake up and resume running."""
        return On()


class Hibernated(ComputerState):
    """Computer saved its memory to disk and powered down.

    Role in the pattern: ConcreteState.
    """

    @property
    def on_enter(self) -> str:
        """Message for a computer that has just hibernated."""
        return "Memory saved to disk"

    def power_button(self) -> ComputerState:
        """Restore the memory from disk and resume running."""
        return On()


class Computer:
    """Computer that delegates every action to its current state.

    Role in the pattern: Context.
    """

    def __init__(self, model: str = "HP") -> None:
        """Create a computer that starts in the ``Off`` state.

        Parameters
        ----------
        model : str, default="HP"
            Model name; informative only.
        """
        self.model = model
        self._state: ComputerState = Off()

    @property
    def state(self) -> ComputerState:
        """Current power state."""
        return self._state

    def power_button(self) -> None:
        """Press the power button."""
        self._change(self._state.power_button())

    def suspend(self) -> None:
        """Suspend the computer.

        Raises
        ------
        InvalidTransitionError
            If the current state does not allow it; the state is kept.
        """
        self._change(self._state.suspend())

    def hibernate(self) -> None:
        """Hibernate the computer.

        Raises
        ------
        InvalidTransitionError
            If the current state does not allow it; the state is kept.
        """
        self._change(self._state.hibernate())

    def _change(self, state: ComputerState) -> None:
        """Print the transition and make ``state`` the current state."""
        print(f"{self._state} -> {state}: {state.on_enter}")
        self._state = state


def client() -> None:
    """Drive the computer through valid and invalid transitions."""
    computer = Computer()
    computer.power_button()
    computer.power_button()
    computer.power_button()
    computer.suspend()
    try:
        computer.hibernate()
    except InvalidTransitionError as error:
        print(f"Rejected: {error}")
    computer.power_button()
    computer.power_button()
    print(f"Final state: {computer.state}")


if __name__ == "__main__":
    client()
