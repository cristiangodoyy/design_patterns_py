"""Drive a computer's power states by branching on a status code.

Pattern: State (behavioral), problem side.
Counterpart: ``state_power_with_state.py``.

Notes
-----
Scenario:
    A computer can be off, on, suspended or hibernated. The power
    button, ``suspend`` and ``hibernate`` do different things, or are
    not allowed at all, depending on the current status.

What goes wrong here:
    - Every action is an ``if/elif`` chain over ``PowerStatus``; the
      behavior of one state is scattered across all the methods.
    - Open/closed: a new state (say, "rebooting") means editing every
      action method and hoping no branch is forgotten.
    - The transition rules are implicit in the branches; nothing shows
      in one place what a state allows.

Roles::

    Computer.power_button() / suspend() / hibernate()
      if OFF -> ...  elif ON -> ...  elif SUSPENDED/HIBERNATED -> ...
      (one branch per status, repeated in every action)
"""

from enum import StrEnum, auto


class PowerStatus(StrEnum):
    """Power states the computer can be in."""

    OFF = auto()
    ON = auto()
    SUSPENDED = auto()
    HIBERNATED = auto()


class InvalidTransitionError(ValueError):
    """Raised when an action is not allowed in the current state."""


class Computer:
    """Computer whose behavior branches on a status code."""

    def __init__(self, model: str = "HP") -> None:
        """Create a computer that starts powered off.

        Parameters
        ----------
        model : str, default="HP"
            Model name; informative only.
        """
        self.model = model
        self._status = PowerStatus.OFF

    @property
    def status(self) -> PowerStatus:
        """Current power status."""
        return self._status

    def power_button(self) -> None:
        """Turn on, turn off, or wake up, depending on the status."""
        if self._status == PowerStatus.OFF:
            self._change(PowerStatus.ON)
        elif self._status == PowerStatus.ON:
            self._change(PowerStatus.OFF)
        elif self._status in (PowerStatus.SUSPENDED, PowerStatus.HIBERNATED):
            self._change(PowerStatus.ON)

    def suspend(self) -> None:
        """Suspend the computer; only allowed while it is on.

        Raises
        ------
        InvalidTransitionError
            If the computer is not on.
        """
        if self._status == PowerStatus.ON:
            self._change(PowerStatus.SUSPENDED)
        else:
            raise InvalidTransitionError(
                f"Cannot suspend while {self._status}"
            )

    def hibernate(self) -> None:
        """Hibernate the computer; only allowed while it is on.

        Raises
        ------
        InvalidTransitionError
            If the computer is not on.
        """
        if self._status == PowerStatus.ON:
            self._change(PowerStatus.HIBERNATED)
        else:
            raise InvalidTransitionError(
                f"Cannot hibernate while {self._status}"
            )

    def _change(self, status: PowerStatus) -> None:
        """Print the transition and store ``status`` as the new status."""
        print(f"{self._status} -> {status}")
        self._status = status


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
    print(f"Final status: {computer.status}")


if __name__ == "__main__":
    client()
