"""Configure a custom computer through one long constructor.

Pattern: Builder (creational), problem side.
Counterpart: ``computer_with_builder.py``.
Step 1 of 5; next: ``computer_public_attributes_before_builder.py``.

Notes
-----
Scenario:
    A shop assembles custom computers. Each computer is made of a case,
    a mainboard, a CPU, memory, a hard drive and a video card, and the
    list of components tends to grow as the shop adds new features.

What goes wrong here:
    - Long parameter list: the constructor takes one argument per
      component. Calls are hard to read and maintain, and nothing tells
      you which parameters are mandatory and which are optional.
    - Every new component makes the signature longer and forces every
      caller to change; constructors tend to grow like this as a
      project matures without refactoring.
    - The builder pattern is good at handling exactly this kind of
      issue; the next steps walk towards it.

Roles::

    client ---> Computer(case, mainboard, cpu, memory,
                         hard_drive, video_card)   (one call, six args)
"""


class Computer:
    """Custom computer configured entirely through its constructor."""

    def __init__(
        self,
        case: str,
        mainboard: str,
        cpu: str,
        memory: str,
        hard_drive: str,
        video_card: str,
    ) -> None:
        """Store every component; all six are required.

        Parameters
        ----------
        case : str
            Case every other part goes into.
        mainboard : str
            Mainboard model.
        cpu : str
            Processor fitted on the mainboard.
        memory : str
            Installed memory.
        hard_drive : str
            Storage device.
        video_card : str
            Graphics card.
        """
        self.case = case
        self.mainboard = mainboard
        self.cpu = cpu
        self.memory = memory
        self.hard_drive = hard_drive
        self.video_card = video_card

    def display(self) -> None:
        """Print the computer's components, one per line."""
        print("Custom Computer:")
        print(f"\t{'Case':>10}: {self.case}")
        print(f"\t{'Mainboard':>10}: {self.mainboard}")
        print(f"\t{'CPU':>10}: {self.cpu}")
        print(f"\t{'Memory':>10}: {self.memory}")
        print(f"\t{'Hard drive':>10}: {self.hard_drive}")
        print(f"\t{'Video card':>10}: {self.video_card}")


def client() -> None:
    """Configure one computer through the long constructor."""
    computer = Computer(
        case="Coolermaster",
        mainboard="MSI",
        cpu="Intel Core i9",
        memory="2 x 16GB",
        hard_drive="SSD 2TB",
        video_card="GeForce",
    )
    computer.display()


if __name__ == "__main__":
    client()
