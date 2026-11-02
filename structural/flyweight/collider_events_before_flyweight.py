"""Record collider events that each carry a full copy of particle data.

Pattern: Flyweight (structural), problem side.
Counterpart: ``collider_events_with_flyweight.py``.

Notes
-----
Scenario:
    A particle detector records thousands of hits per second. Each hit
    arrives as one text record with the particle data and its own
    position, time and measured energy. Only a handful of particle
    types exist (electron, muon, proton), and their mass and charge
    never change.

What goes wrong here:
    - Every ``Event`` is parsed from its own record, so it owns its own
      ``str`` for the particle name and its own ``float`` for the mass:
      constant data is duplicated once per event.
    - ``Event`` already uses ``__slots__``, exactly like the flyweight
      version, so the memory difference measured by ``total_size``
      comes from the duplicated particle data alone.
    - Nothing guarantees consistency: two events of the "same" particle
      could end up with different masses after a typo or an update.

Roles::

    Event(name, mass, charge, x, y, t, energy)   x 1000
          ^^^^^^^^^^^^^^^^^^^^
          identical values, but a separate copy in every event
"""

import math
import sys

from collections.abc import Iterable

RAW_PARTICLES = ("electron,0.511,-1", "muon,105.66,-1", "proton,938.27,1")


class Event:
    """One detector hit that keeps its own copy of the particle data."""

    __slots__ = (
        "particle_name",
        "mass_mev",
        "charge",
        "x_m",
        "y_m",
        "t_ns",
        "energy_mev",
    )

    def __init__(
        self,
        particle_name: str,
        mass_mev: float,
        charge: int,
        x_m: float,
        y_m: float,
        t_ns: float,
        energy_mev: float,
    ) -> None:
        """Store the particle data and the measurements of one hit.

        Parameters
        ----------
        particle_name : str
            Name of the particle, copied into every event.
        mass_mev : float
            Rest mass in MeV, copied into every event.
        charge : int
            Electric charge, copied into every event.
        x_m : float
            Horizontal distance from the collision point, in metres.
        y_m : float
            Vertical distance from the collision point, in metres.
        t_ns : float
            Time of the hit, in nanoseconds.
        energy_mev : float
            Measured kinetic energy, in MeV.
        """
        self.particle_name = particle_name
        self.mass_mev = mass_mev
        self.charge = charge
        self.x_m = x_m
        self.y_m = y_m
        self.t_ns = t_ns
        self.energy_mev = energy_mev

    def transverse_speed(self) -> float:
        """Return the speed from the collision point to the hit, in m/s."""
        return math.hypot(self.x_m, self.y_m) / (self.t_ns * 1e-9)

    def lorentz_factor(self) -> float:
        """Return gamma, treating ``energy_mev`` as kinetic energy."""
        return 1.0 + self.energy_mev / self.mass_mev


def raw_record(index: int) -> str:
    """Return the deterministic detector record number ``index``.

    Parameters
    ----------
    index : int
        Position of the record in the stream.

    Returns
    -------
    str
        Comma-separated particle data followed by the measurements.
    """
    particle = RAW_PARTICLES[index % len(RAW_PARTICLES)]
    x_m = 0.3 + 0.2 * (index % 4)
    y_m = 0.1 * (index % 5)
    t_ns = 4.0 + 0.5 * (index % 7)
    energy_mev = 50.0 + 25.0 * (index % 9)
    return f"{particle},{x_m},{y_m},{t_ns},{energy_mev}"


def parse_event(record: str) -> Event:
    """Build an ``Event`` that owns every value parsed from ``record``."""
    name, mass, charge, x_m, y_m, t_ns, energy = record.split(",")
    return Event(
        particle_name=name,
        mass_mev=float(mass),
        charge=int(charge),
        x_m=float(x_m),
        y_m=float(y_m),
        t_ns=float(t_ns),
        energy_mev=float(energy),
    )


def generate_events(count: int) -> list[Event]:
    """Parse ``count`` events from the deterministic record stream."""
    return [parse_event(raw_record(index)) for index in range(count)]


def total_size(objects: Iterable[object]) -> int:
    """Return the bytes used by ``objects`` and everything they reference.

    Each distinct object is counted once, so shared objects are not
    counted again for every event that refers to them.

    Parameters
    ----------
    objects : Iterable of object
        Root objects to measure, such as a list of events.

    Returns
    -------
    int
        Approximate total size in bytes, as reported by
        ``sys.getsizeof``.
    """
    seen: set[int] = set()
    pending = list(objects)
    size = 0
    while pending:
        obj = pending.pop()
        if id(obj) in seen:
            continue
        seen.add(id(obj))
        size += sys.getsizeof(obj)
        for slot in getattr(type(obj), "__slots__", ()):
            pending.append(getattr(obj, slot))
    return size


def client() -> None:
    """Create a batch of events and report the memory they need."""
    events = generate_events(1_000)

    first = events[1]
    print(f"First muon speed: {first.transverse_speed():.3e} m/s")
    print(f"First muon gamma: {first.lorentz_factor():.3f}")

    print(f"Events: {len(events)}")
    print(f"Particle records stored: {len(events)} (one per event)")
    print(f"Approximate total: {total_size(events)} bytes")


if __name__ == "__main__":
    client()
