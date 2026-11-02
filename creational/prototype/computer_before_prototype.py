"""Build every computer variant by hand from constructor arguments.

Pattern: Prototype (creational), problem side.
Counterpart: ``computer_with_shallow_copy_prototype.py``,
``computer_with_deep_copy_prototype.py`` and
``computer_with_registry_prototype.py``.

Notes
-----
Scenario:
    A shop sells a carefully configured gaming tower. Customers order
    small variations of it: the same machine with another model name,
    or with a business mainboard instead of the gaming one.

What goes wrong here:
    - The client must know the concrete ``Tower`` class and every one of
      its seven constructor arguments, including the nested
      ``MainBoard``, just to get "the same, but slightly different".
    - The configuration is repeated at every call site; when ``Tower``
      gains a field, every hand-written copy must be edited, and the
      ones that are forgotten silently drift from the original.
    - Copying field by field is easy to get wrong: reuse
      ``original.mainboard`` instead of building a new board and the
      two towers secretly share one object.
    - If building a configured object were expensive (probing hardware,
      loading drivers), that cost would be paid again for every
      variation.

Roles::

    Client ---> Tower(model, MainBoard(...), processor, memory,
                      hard_drive, graphics, monitor)
    Client ---> Tower(...the same seven arguments, typed again...)
"""

from dataclasses import dataclass


@dataclass
class MainBoard:
    """Mainboard fitted inside a tower."""

    manufacturer: str
    model: str


@dataclass
class Tower:
    """Desktop tower whose every variant is built from scratch."""

    model: str
    mainboard: MainBoard
    processor: str
    memory: str
    hard_drive: str
    graphics: str
    monitor: str

    def describe(self) -> str:
        """Return a printable spec sheet of the tower."""
        board = f"{self.mainboard.manufacturer} {self.mainboard.model}"
        rows = [
            ("Mainboard", board),
            ("Processor", self.processor),
            ("Memory", self.memory),
            ("Hard drive", self.hard_drive),
            ("Graphics", self.graphics),
            ("Monitor", self.monitor),
        ]
        lines = [f"Custom computer: {self.model}"]
        lines += [f"    {label:>10}: {value}" for label, value in rows]
        return "\n".join(lines)


def client() -> None:
    """Order two variations of a tower by repeating its configuration."""
    original = Tower(
        model="T1",
        mainboard=MainBoard(manufacturer="ASUS", model="Game"),
        processor="AMD",
        memory="32GB",
        hard_drive="2TB SSD",
        graphics="onboard",
        monitor="1920x1080",
    )
    # Variation 1: every argument typed again, only the model differs.
    renamed = Tower(
        model="T2",
        mainboard=MainBoard(manufacturer="ASUS", model="Game"),
        processor="AMD",
        memory="32GB",
        hard_drive="2TB SSD",
        graphics="onboard",
        monitor="1920x1080",
    )
    # Variation 2: copied field by field, nested board included.
    business = Tower(
        model="T3",
        mainboard=MainBoard(
            manufacturer=original.mainboard.manufacturer,
            model="Business",
        ),
        processor=original.processor,
        memory=original.memory,
        hard_drive=original.hard_drive,
        graphics=original.graphics,
        monitor=original.monitor,
    )
    for tower in (original, renamed, business):
        print(tower.describe())
    print("Each variation repeated all 7 constructor arguments.")


if __name__ == "__main__":
    client()
