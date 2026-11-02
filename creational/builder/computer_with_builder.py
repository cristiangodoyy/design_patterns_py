"""Assemble custom computers with a Director and interchangeable builders.

Pattern: Builder (creational).
Counterpart: ``computer_build_before_builder.py``.
Step 5 of 5; previous: ``computer_build_before_builder.py``.

Notes
-----
Why:
    - The journey so far: step 1 had too many constructor parameters;
      step 2 exposed the attributes, which was worse; step 3 encapsulated
      them but had no build order; step 4 enforced the order with step
      methods but had to be copied for every new configuration.
    - Builder separates *how* a computer is assembled from *what* it is
      made of. ``Director`` owns the build sequence, the same for every
      computer; each concrete builder (``LenovoBuilder``, ``HPBuilder``)
      only decides which components go into each step.
    - ``AbsBuilder`` declares the build steps and keeps the product under
      construction, so a new configuration is a new builder class and
      neither the director nor the existing builders change
      (open/closed).
    - The client picks a builder, hands it to the director and receives
      the finished product; it never assembles parts itself.

When to use:
    - An object is assembled in several ordered steps, or has many
      optional parts that would otherwise need a long constructor.
    - The same construction process must create different
      representations of the product.

Trade-offs:
    - More classes (director, abstract builder, one builder per
      configuration); overkill for objects that a dataclass or keyword
      arguments describe well enough.
    - The product is incomplete until the director has finished; reading
      it earlier returns a half-built object.

Related:
    - Abstract Factory returns a product in one call; Builder assembles
      it step by step and returns it at the end.
    - Template Method also fixes a sequence of steps, but through
      inheritance in one class instead of a separate director.
    - Composite trees are often assembled with a builder.

Roles::

    client ---> Director ---uses---> AbsBuilder (Builder) ---> Computer
                build_computer()        ^                     (Product)
                                        |
                          LenovoBuilder | HPBuilder
                              (ConcreteBuilder)
"""

from abc import ABC, abstractmethod


class Computer:
    """Custom computer assembled by a builder.

    Role in the pattern: Product.
    """

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


class AbsBuilder(ABC):
    """Declare the build steps and hold the computer being built.

    Every concrete builder fills in the same steps with its own
    components; the order is the director's business.

    Role in the pattern: Builder.
    """

    def __init__(self) -> None:
        """Start with an empty computer to build on."""
        self._computer = Computer()

    def new_computer(self) -> None:
        """Start assembling a fresh, empty computer.

        The director calls this first, so every build starts clean and
        never reuses parts of a previous one.
        """
        self._computer = Computer()

    def get_computer(self) -> Computer:
        """Return the computer assembled so far (the GetResult step)."""
        return self._computer

    @abstractmethod
    def install_case(self) -> None:
        """Install the case every other part goes into."""

    @abstractmethod
    def build_mainboard(self) -> None:
        """Assemble the mainboard with its CPU and memory."""

    @abstractmethod
    def install_hard_drive(self) -> None:
        """Install the hard drive."""

    @abstractmethod
    def install_video_card(self) -> None:
        """Install the video card."""


class LenovoBuilder(AbsBuilder):
    """Build a high-end configuration.

    Role in the pattern: ConcreteBuilder.
    """

    def install_case(self) -> None:
        """Install the Coolermaster case."""
        self._computer.case = "Coolermaster"

    def build_mainboard(self) -> None:
        """Fit the MSI mainboard with an Intel Core i9 and 2 x 16GB."""
        self._computer.mainboard = "MSI"
        self._computer.cpu = "Intel Core i9"
        self._computer.memory = "2 x 16GB"

    def install_hard_drive(self) -> None:
        """Install the 2TB SSD."""
        self._computer.hard_drive = "SSD 2TB"

    def install_video_card(self) -> None:
        """Install the GeForce GTX video card."""
        self._computer.video_card = "GeForce GTX"


class HPBuilder(AbsBuilder):
    """Build a budget configuration.

    Role in the pattern: ConcreteBuilder.
    """

    def install_case(self) -> None:
        """Install the Corsair case."""
        self._computer.case = "Corsair"

    def build_mainboard(self) -> None:
        """Fit the ASUS mainboard with an AMD Ryzen 5 and 2 x 4GB."""
        self._computer.mainboard = "ASUS"
        self._computer.cpu = "AMD Ryzen 5"
        self._computer.memory = "2 x 4GB"

    def install_hard_drive(self) -> None:
        """Install the 1TB Seagate hard drive."""
        self._computer.hard_drive = "Seagate HD 1TB"

    def install_video_card(self) -> None:
        """Install the on-board video (no card)."""
        self._computer.video_card = "On board"


class Director:
    """Run the build steps of any builder in the required order.

    The director knows how to assemble a computer but not which parts
    to use: it calls each builder step in sequence and then hands back
    the finished product.

    Role in the pattern: Director.
    """

    def __init__(self, builder: AbsBuilder) -> None:
        """Use ``builder`` for every computer this director assembles.

        Parameters
        ----------
        builder : AbsBuilder
            Builder that decides which components go into each step.
        """
        self._builder = builder

    def build_computer(self) -> None:
        """Assemble a new computer, in the same order for any builder."""
        self._builder.new_computer()
        self._builder.install_case()
        self._builder.build_mainboard()
        self._builder.install_hard_drive()
        self._builder.install_video_card()

    def get_computer(self) -> Computer:
        """Return the finished computer from the builder."""
        return self._builder.get_computer()


def client() -> None:
    """Build one computer with each builder through the same director."""
    for builder in (LenovoBuilder(), HPBuilder()):
        director = Director(builder)
        director.build_computer()
        director.get_computer().display()


if __name__ == "__main__":
    client()
