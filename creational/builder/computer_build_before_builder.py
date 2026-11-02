"""Configure a custom computer through ordered build steps.

Pattern: Builder (creational), problem side.
Counterpart: ``computer_with_builder.py``.
Step 4 of 5; previous: ``computer_encapsulated_before_builder.py``;
next: ``computer_with_builder.py``.

Notes
-----
Scenario:
    The same custom-computer shop. This time the build order is
    enforced: ``MyComputerBuilder`` enhances step 3's version by
    splitting the assembly into one method per step and calling them in
    the correct order. The mainboard is assembled in its own step
    (mainboard, CPU and memory) and then installed into the case.

What goes wrong here:
    - The steps look great until the shop wants a different product.
      A second configuration means copying the whole class and changing
      the values: the build order and the step methods are duplicated.
    - The sequence of steps (how to assemble) and the components chosen
      (what to assemble) live in the same class, so they cannot vary
      independently.

Roles::

    client ---> MyComputerBuilder.build_computer()
                  install_case() -> build_mainboard()
                  -> install_hard_drive() -> install_video_card()
                MyComputerBuilder.get_computer() ---> Computer
                (copy the whole class for every new configuration)
"""


class Computer:
    """Custom computer assembled step by step."""

    def __init__(self) -> None:
        """Start with every component empty; the build fills them in."""
        self.case: str = ""
        self.mainboard: str = ""
        self.cpu: str = ""
        self.memory: str = ""
        self.hard_drive: str = ""
        self.video_card: str = ""

    def display(self) -> None:
        """Print the computer's components, one per line."""
        print("Custom Computer:")
        print(f"\t{'Case':>10}: {self.case}")
        print(f"\t{'Mainboard':>10}: {self.mainboard}")
        print(f"\t{'CPU':>10}: {self.cpu}")
        print(f"\t{'Memory':>10}: {self.memory}")
        print(f"\t{'Hard drive':>10}: {self.hard_drive}")
        print(f"\t{'Video card':>10}: {self.video_card}")


class MyComputerBuilder:
    """Assemble one fixed computer configuration in the correct order."""

    def __init__(self) -> None:
        """Start with an empty computer; ``build_computer`` replaces it."""
        self._computer = Computer()

    def get_computer(self) -> Computer:
        """Return the computer assembled by the last build."""
        return self._computer

    def build_computer(self) -> None:
        """Assemble a new computer by running each step in sequence."""
        self._computer = Computer()
        self.install_case()
        self.build_mainboard()
        self.install_hard_drive()
        self.install_video_card()

    def install_case(self) -> None:
        """Install the case every other part goes into."""
        self._computer.case = "Coolermaster N300"

    def build_mainboard(self) -> None:
        """Assemble the mainboard with its CPU and memory."""
        self._computer.mainboard = "MSI 970"
        self._computer.cpu = "Intel Core i7-4770"
        self._computer.memory = "Corsair Vengeance 16GB"

    def install_hard_drive(self) -> None:
        """Install the hard drive once the mainboard is in place."""
        self._computer.hard_drive = "Seagate 4TB"

    def install_video_card(self) -> None:
        """Install the video card into the mainboard."""
        self._computer.video_card = "GeForce GTX 1070"


def client() -> None:
    """Build one computer by running the ordered steps."""
    builder = MyComputerBuilder()
    builder.build_computer()
    builder.get_computer().display()


if __name__ == "__main__":
    client()
