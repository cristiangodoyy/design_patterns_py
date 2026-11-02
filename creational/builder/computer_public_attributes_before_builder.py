"""Configure a custom computer by setting public attributes.

Pattern: Builder (creational), problem side.
Counterpart: ``computer_with_builder.py``.
Step 2 of 5; previous: ``computer_long_constructor_before_builder.py``;
next: ``computer_encapsulated_before_builder.py``.

Notes
-----
Scenario:
    The same custom-computer shop as step 1. To get rid of the long
    constructor, ``Computer`` now only exposes its attributes and the
    client sets them one by one.

What goes wrong here:
    - It is a very common fix for parameter proliferation, and it works:
      the output is the same as in step 1. But it is not a good fix.
    - The client must know every component and assign it itself; nothing
      stops it from forgetting one, which silently leaves it empty.
    - There is no encapsulation: any code can change a component at any
      time, which makes maintenance harder than the original problem.

Roles::

    client ---> computer = Computer()
                computer.case = ...
                computer.mainboard = ...   (client assembles the parts)
                ...
"""


class Computer:
    """Custom computer whose components are plain public attributes."""

    def __init__(self) -> None:
        """Start with every component empty; the client must set each one."""
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


def client() -> None:
    """Configure one computer by assigning each attribute directly."""
    computer = Computer()
    computer.video_card = "GeForce"
    computer.case = "Coolermaster"
    computer.cpu = "Intel Core i9"
    computer.memory = "2 x 16GB"
    computer.hard_drive = "SSD 2TB"
    computer.mainboard = "MSI"
    computer.display()


if __name__ == "__main__":
    client()
