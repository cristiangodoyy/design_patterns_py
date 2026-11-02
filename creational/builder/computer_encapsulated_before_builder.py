"""Configure a custom computer inside a dedicated class.

Pattern: Builder (creational), problem side.
Counterpart: ``computer_with_builder.py``.
Step 3 of 5; previous: ``computer_public_attributes_before_builder.py``;
next: ``computer_build_before_builder.py``.

Notes
-----
Scenario:
    The same custom-computer shop. Setting the attributes is now
    encapsulated in ``MyComputerBuilder``, so the client no longer
    assigns components itself.

What goes wrong here:
    - The client no longer assigns the components itself, but that
      exposes the next problem: build order. A computer cannot be
      assembled in any old way; there are definite steps to follow in
      sequence.
    - You cannot install the video card before the mainboard, and
      installing the hard drive first may obstruct other work. Here all
      components are set in one method, in arbitrary order, and nothing
      expresses or enforces the sequence.

Roles::

    client ---> MyComputerBuilder.build_computer()
                  sets every attribute of Computer, in any order
                MyComputerBuilder.get_computer() ---> Computer
"""


class Computer:
    """Custom computer whose components are set by a builder class."""

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
    """Encapsulate how the computer's components are set."""

    def __init__(self) -> None:
        """Start with an empty computer; ``build_computer`` replaces it."""
        self._computer = Computer()

    def get_computer(self) -> Computer:
        """Return the computer configured by the last build."""
        return self._computer

    def build_computer(self) -> None:
        """Configure a new computer, setting every component at once.

        The order of the assignments is arbitrary: nothing encodes the
        fact that the mainboard must be installed before the video card.
        """
        self._computer = Computer()
        self._computer.video_card = "GeForce"
        self._computer.case = "Coolermaster"
        self._computer.cpu = "Intel Core i9"
        self._computer.memory = "2 x 16GB"
        self._computer.hard_drive = "SSD 2TB"
        self._computer.mainboard = "MSI"


def client() -> None:
    """Build one computer through the encapsulating class."""
    builder = MyComputerBuilder()
    builder.build_computer()
    builder.get_computer().display()


if __name__ == "__main__":
    client()
