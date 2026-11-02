"""Start and stop a schedule server by calling every subsystem step.

Pattern: Facade (structural), problem side.
Counterpart: ``schedule_server_with_facade.py``.

Notes
-----
Scenario:
    A company ships a Schedule Server that runs jobs (sending e-mails or
    SMS, reading or writing files, transferring files) at their
    scheduled time. Internally the server is made of several
    subsystems: a bootloader, an execution context, event listeners,
    the system objects and the job processes. The server works well,
    but customers complain that starting and stopping it is far too
    complicated: they must drive five classes through twelve low-level
    calls in exactly the right order.

What goes wrong here:
    - Every client repeats the same startup and shutdown sequences, so
      the knowledge of the correct order is duplicated everywhere.
    - Calling the steps in the wrong order, or forgetting one, leaves
      the server half initialised or leaks resources.
    - Clients are coupled to every subsystem class and every internal
      operation: renaming, splitting or adding a step breaks all of
      them.
    - Most clients only want "start" and "stop"; the low-level interface
      is a burden they never asked for.

Roles::

    client ---> Bootloader.start_booting()
           ---> Bootloader.read_system_config_file()
           ---> Bootloader.init()
           ---> ExecutionContext.initialize_context()
           ---> ...            (5 classes, 12 calls, order matters)
           ---> Bootloader.shutdown()
"""


class Bootloader:
    """Boot sequence and final power-off of the server."""

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
    """Runtime context shared by the scheduled jobs."""

    def initialize_context(self) -> None:
        """Create the context the scheduled jobs run in."""
        print("Initializing context")

    def destroy_context(self) -> None:
        """Release the jobs' execution context."""
        print("Destroying context")


class ListenerRegistry:
    """Event listeners that trigger the scheduled jobs."""

    def initialize_listeners(self) -> None:
        """Register the listeners that trigger the jobs."""
        print("Initializing listeners")

    def destroy_listeners(self) -> None:
        """Unregister the job listeners."""
        print("Destroying listeners")


class SystemObjects:
    """Long-lived objects the jobs work with."""

    def create_system_objects(self) -> None:
        """Create the long-lived objects the jobs use."""
        print("Creating system objects")

    def destroy_system_objects(self) -> None:
        """Destroy the long-lived system objects."""
        print("Destroying system objects")


class ProcessManager:
    """Worker processes that run the jobs."""

    def release_processes(self) -> None:
        """Release the worker processes (first step of shutdown)."""
        print("Releasing processes")


def client() -> None:
    """Run the server the hard way: the client orchestrates every step."""
    bootloader = Bootloader()
    context = ExecutionContext()
    listeners = ListenerRegistry()
    system_objects = SystemObjects()
    processes = ProcessManager()

    bootloader.start_booting()
    bootloader.read_system_config_file()
    bootloader.init()
    context.initialize_context()
    listeners.initialize_listeners()
    system_objects.create_system_objects()

    print("Start working")
    print("After work done")

    processes.release_processes()
    bootloader.destroy()
    system_objects.destroy_system_objects()
    listeners.destroy_listeners()
    context.destroy_context()
    bootloader.shutdown()


if __name__ == "__main__":
    client()
