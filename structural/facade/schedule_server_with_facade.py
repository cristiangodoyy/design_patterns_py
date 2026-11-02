"""Start and stop a schedule server through a two-method facade.

Pattern: Facade (structural).
Counterpart: ``schedule_server_before_facade.py``.

Notes
-----
Why:
    - The facade hides the startup and shutdown sequences of five
      subsystem classes behind ``start_server()`` and
      ``stop_server()``.
    - The correct order of the steps, which spans several classes,
      lives in exactly one place.
    - Most clients depend only on a small, stable interface, so the
      subsystems can be renamed, split or extended without breaking
      them.
    - The subsystems are not hidden away: the few clients that need
      fine-grained control can still use them directly.

When to use:
    - You want a simple interface to a complex subsystem. Subsystems
      tend to grow into many small classes as they evolve; a facade
      gives most clients a default view that is good enough.
    - There are many dependencies between clients and the classes that
      implement an abstraction; a facade decouples them.
    - You want to layer subsystems: each layer exposes a facade as its
      entry point, and layers talk to each other only through it.

Trade-offs:
    - The facade can grow into a god object if it absorbs unrelated
      responsibilities; prefer several focused facades over one global
      facade when clients use different subsets of the subsystem.
    - It adds one more class; it does not encapsulate the subsystem,
      it only simplifies access to it.

Related:
    - Adapter can also wrap several classes, but it converts an
      interface into the one the client expects; Facade defines a new,
      simpler interface.
    - Mediator also centralises collaboration, but its colleagues know
      about it; subsystem classes are unaware of the facade.
    - A facade is often a Singleton, and Abstract Factory can create
      subsystem objects for it.

Roles::

    client ---> ScheduleServerFacade (Facade)
                  start_server() / stop_server()
                        |
                        +--> Bootloader
                        +--> ExecutionContext
                        +--> ListenerRegistry     (Subsystem classes)
                        +--> SystemObjects
                        +--> ProcessManager
"""


class Bootloader:
    """Boot sequence and final power-off of the server.

    Role in the pattern: Subsystem class; unaware of the facade.
    """

    def start_booting(self) -> None:
        """Begin the boot sequence (first step of startup)."""
        print("Starting to boot")

    def read_system_config_file(self) -> None:
        """Load the system configuration files."""
        print("Reading system config files")

    def init(self) -> None:
        """Initialise the server core."""
        print("Initializing")

    def destroy(self) -> None:
        """Tear down the server core."""
        print("Destroying")

    def shutdown(self) -> None:
        """Power the server off (last step of shutdown)."""
        print("Shutting down")


class ExecutionContext:
    """Runtime context shared by the scheduled jobs.

    Role in the pattern: Subsystem class; unaware of the facade.
    """

    def initialize_context(self) -> None:
        """Create the context the scheduled jobs run in."""
        print("Initializing context")

    def destroy_context(self) -> None:
        """Release the jobs' execution context."""
        print("Destroying context")


class ListenerRegistry:
    """Event listeners that trigger the scheduled jobs.

    Role in the pattern: Subsystem class; unaware of the facade.
    """

    def initialize_listeners(self) -> None:
        """Register the listeners that trigger the jobs."""
        print("Initializing listeners")

    def destroy_listeners(self) -> None:
        """Unregister the job listeners."""
        print("Destroying listeners")


class SystemObjects:
    """Long-lived objects the jobs work with.

    Role in the pattern: Subsystem class; unaware of the facade.
    """

    def create_system_objects(self) -> None:
        """Create the long-lived objects the jobs use."""
        print("Creating system objects")

    def destroy_system_objects(self) -> None:
        """Destroy the long-lived system objects."""
        print("Destroying system objects")


class ProcessManager:
    """Worker processes that run the jobs.

    Role in the pattern: Subsystem class; unaware of the facade.
    """

    def release_processes(self) -> None:
        """Release the worker processes (first step of shutdown)."""
        print("Releasing processes")


class ScheduleServerFacade:
    """Client-facing entry point with just ``start`` and ``stop``.

    Role in the pattern: Facade. It forwards each request to the right
    subsystem in the right order, so most clients only need these two
    methods.
    """

    def __init__(
        self,
        bootloader: Bootloader,
        context: ExecutionContext,
        listeners: ListenerRegistry,
        system_objects: SystemObjects,
        processes: ProcessManager,
    ) -> None:
        """Keep the subsystems the facade coordinates.

        Parameters
        ----------
        bootloader : Bootloader
            Boot sequence and final power-off.
        context : ExecutionContext
            Runtime context of the jobs.
        listeners : ListenerRegistry
            Listeners that trigger the jobs.
        system_objects : SystemObjects
            Long-lived objects the jobs use.
        processes : ProcessManager
            Worker processes that run the jobs.
        """
        self._bootloader = bootloader
        self._context = context
        self._listeners = listeners
        self._system_objects = system_objects
        self._processes = processes

    def start_server(self) -> None:
        """Boot and initialise the server in the required order."""
        self._bootloader.start_booting()
        self._bootloader.read_system_config_file()
        self._bootloader.init()
        self._context.initialize_context()
        self._listeners.initialize_listeners()
        self._system_objects.create_system_objects()

    def stop_server(self) -> None:
        """Release resources and shut the server down safely."""
        self._processes.release_processes()
        self._bootloader.destroy()
        self._system_objects.destroy_system_objects()
        self._listeners.destroy_listeners()
        self._context.destroy_context()
        self._bootloader.shutdown()


def client() -> None:
    """Run the server through the facade: two calls instead of twelve."""
    facade = ScheduleServerFacade(
        Bootloader(),
        ExecutionContext(),
        ListenerRegistry(),
        SystemObjects(),
        ProcessManager(),
    )

    facade.start_server()
    print("Start working")
    print("After work done")
    facade.stop_server()


if __name__ == "__main__":
    client()
