"""Record collider events that share immutable particle-type objects.

Pattern: Flyweight (structural).
Counterpart: ``collider_events_before_flyweight.py``.

Notes
-----
Why:
    - The state of an event is split in two. Intrinsic state (particle
      name, mass, charge) is identical for many events, so it lives in
      a frozen ``ParticleType`` shared by all of them.
    - Extrinsic state (position, time, energy) varies per event and is
      kept in ``Event``, which only references the shared flyweight.
      Both versions use ``__slots__``, so the memory saved, measured by
      ``total_size``, comes from sharing alone.
    - ``FlyweightFactory`` caches flyweights by key, so asking twice for
      the same particle returns the very same object.

When to use:
    - An application creates a huge number of similar objects and
      memory is a real constraint.
    - Most of each object's state can be made extrinsic and moved out.
    - Once the extrinsic state is removed, many objects collapse into a
      few shared ones, and object identity does not matter to clients.

Trade-offs:
    - More moving parts: a factory, a cache and the split of state.
    - Shared objects must be immutable; a mutation would leak into
      every event that references them.
    - The cache lives as long as the factory and is never evicted here.

Related:
    - Factory Method / Singleton: the factory is often a single shared
      instance that controls creation.
    - Composite leaves are often implemented as flyweights.
    - Prototype copies objects; Flyweight shares them instead.

Roles::

    FlyweightFactory (FlyweightFactory) --caches--> ParticleType
                                                     (Flyweight,
    Event (client-side extrinsic state) --refers-->  intrinsic state)
      x_m, y_m, t_ns, energy_mev
"""

import math
import sys

from collections.abc import Iterable
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

RAW_PARTICLES = ("electron,0.511,-1", "muon,105.66,-1", "proton,938.27,1")


@dataclass(frozen=True, slots=True)
class ParticleType:
    """Immutable data shared by every event of one particle type.

    Role in the pattern: Flyweight (intrinsic state).
    """

    name: str
    mass_mev: float
    charge: int


class FlyweightFactory:
    """Create particle types on demand and hand out cached instances.

    Role in the pattern: FlyweightFactory.
    """

    CATALOG: Final = MappingProxyType(
        {
            "electron": (0.511, -1),
            "muon": (105.66, -1),
            "proton": (938.27, 1),
        }
    )

    def __init__(self) -> None:
        """Start with an empty cache; flyweights are created on demand."""
        self._flyweights: dict[str, ParticleType] = {}

    def get_flyweight(self, name: str) -> ParticleType:
        """Return the shared ``ParticleType`` for ``name``.

        The first request creates the flyweight; later requests return
        the cached object, so identity is preserved.

        Parameters
        ----------
        name : str
            Particle name, one of ``CATALOG``.

        Returns
        -------
        ParticleType
            Shared, immutable particle data.

        Raises
        ------
        ValueError
            If the particle is not in the catalog.
        """
        if name not in self._flyweights:
            if name not in self.CATALOG:
                raise ValueError(f"Unknown particle {name!r}")
            mass_mev, charge = self.CATALOG[name]
            self._flyweights[name] = ParticleType(name, mass_mev, charge)
        return self._flyweights[name]

    @property
    def count(self) -> int:
        """Number of distinct flyweights created so far."""
        return len(self._flyweights)


class Event:
    """One detector hit: extrinsic state plus a shared particle type.

    Role in the pattern: Client-side context holding extrinsic state.
    """

    __slots__ = ("particle", "x_m", "y_m", "t_ns", "energy_mev")

    def __init__(
        self,
        particle: ParticleType,
        x_m: float,
        y_m: float,
        t_ns: float,
        energy_mev: float,
    ) -> None:
        """Store the shared particle and this hit's measurements.

        Parameters
        ----------
        particle : ParticleType
            Shared flyweight with the particle's intrinsic state.
        x_m : float
            Horizontal distance from the collision point, in metres.
        y_m : float
            Vertical distance from the collision point, in metres.
        t_ns : float
            Time of the hit, in nanoseconds.
        energy_mev : float
            Measured kinetic energy, in MeV.
        """
        self.particle = particle
        self.x_m = x_m
        self.y_m = y_m
        self.t_ns = t_ns
        self.energy_mev = energy_mev

    def transverse_speed(self) -> float:
        """Return the speed from the collision point to the hit, in m/s."""
        return math.hypot(self.x_m, self.y_m) / (self.t_ns * 1e-9)

    def lorentz_factor(self) -> float:
        """Return gamma, combining shared mass and per-event energy."""
        return 1.0 + self.energy_mev / self.particle.mass_mev


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


def parse_event(factory: FlyweightFactory, record: str) -> Event:
    """Build an ``Event`` whose particle data comes from ``factory``.

    The mass and charge in ``record`` are ignored: the shared
    flyweight is the single source of truth for them.
    """
    name, _mass, _charge, x_m, y_m, t_ns, energy = record.split(",")
    return Event(
        particle=factory.get_flyweight(name),
        x_m=float(x_m),
        y_m=float(y_m),
        t_ns=float(t_ns),
        energy_mev=float(energy),
    )


def generate_events(factory: FlyweightFactory, count: int) -> list[Event]:
    """Parse ``count`` events from the deterministic record stream."""
    return [parse_event(factory, raw_record(index)) for index in range(count)]


def total_size(objects: Iterable[object]) -> int:
    """Return the bytes used by ``objects`` and everything they reference.

    Each distinct object is counted once, so a flyweight shared by many
    events is counted a single time.

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
    """Create a batch of events and report how much state is shared."""
    factory = FlyweightFactory()
    events = generate_events(factory, 1_000)

    first = events[1]
    print(f"First muon speed: {first.transverse_speed():.3e} m/s")
    print(f"First muon gamma: {first.lorentz_factor():.3f}")

    shared = factory.get_flyweight("muon") is first.particle
    print(f"Events: {len(events)}")
    print(f"Flyweights created: {factory.count}")
    print(f"Muon events share one flyweight: {shared}")
    print(f"Approximate total: {total_size(events)} bytes")


if __name__ == "__main__":
    client()
