"""Build and run programs through one fixed compilation skeleton.

Pattern: Template Method (behavioral).
Counterpart: ``compiler_before_template_method.py``.

Notes
-----
Why:
    - ``Compiler.compile_and_run`` defines the pipeline once; subclasses
      only fill in the steps that differ.
    - The template method cannot be overridden, so no subclass can
      reorder or skip steps: ``@final`` lets mypy reject it statically,
      and ``__init_subclass__`` rejects it at runtime with
      ``TypeError``.
    - ``optimize`` is a hook: an optional step with an empty default
      that only the compilers needing it override.
    - Clients use one entry point for every compiler.

When to use:
    - Several classes share the same algorithm skeleton but differ in
      some of its steps.
    - You want to control exactly where subclasses may extend an
      algorithm (abstract steps and hooks), and nowhere else.
    - You see duplicated step sequences across sibling classes.

Trade-offs:
    - Inheritance-based: the skeleton is fixed at class definition and
      cannot be changed at runtime.
    - Subclasses are coupled to the base class; many small abstract
      steps make the contract hard to follow.

Related:
    - Strategy varies the whole algorithm through composition; Template
      Method varies parts of it through inheritance.
    - Factory Method is often one of the steps of a template method.

Roles::

    Compiler (AbstractClass)
      compile_and_run()  @final template method:
        collect_source() -> compile_to_object() -> optimize() -> run()
                                                   (hook)
              ^                         ^
        IOSCompiler            AndroidCompiler (overrides the hook)
                  (ConcreteClass)
"""

from abc import ABC, abstractmethod
from typing import final


class Compiler(ABC):
    """Skeleton shared by every compiler.

    Role in the pattern: AbstractClass.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Reject subclasses that override the template method.

        ``@final`` is only checked by static type checkers; this hook
        enforces the same rule when the subclass is defined.

        Raises
        ------
        TypeError
            If the subclass defines ``compile_and_run``.
        """
        super().__init_subclass__(**kwargs)
        if "compile_and_run" in vars(cls):
            raise TypeError(
                f"{cls.__name__} must not override Compiler.compile_and_run()"
            )

    @final
    def compile_and_run(self) -> None:
        """Run the pipeline: collect, compile, optimize, run.

        This is the template method; subclasses customise the steps,
        never the order.
        """
        self.collect_source()
        self.compile_to_object()
        self.optimize()
        self.run()

    @abstractmethod
    def collect_source(self) -> None:
        """Gather the source files to compile."""

    @abstractmethod
    def compile_to_object(self) -> None:
        """Translate the sources into an executable form."""

    def optimize(self) -> None:
        """Run an optional step between compiling and running.

        This is a hook: the default does nothing, and subclasses
        override it only when they need it.
        """
        return

    @abstractmethod
    def run(self) -> None:
        """Execute the compiled program."""


class IOSCompiler(Compiler):
    """Compile Swift code for iOS; keeps the default hook.

    Role in the pattern: ConcreteClass.
    """

    def collect_source(self) -> None:
        """Gather the Swift sources."""
        print("Collecting Swift source code")

    def compile_to_object(self) -> None:
        """Compile the Swift sources to LLVM bitcode."""
        print("Compiling Swift code to LLVM bitcode")

    def run(self) -> None:
        """Run the program on the iOS runtime."""
        print("Program running on the iOS runtime")


class AndroidCompiler(Compiler):
    """Compile Kotlin code for Android; overrides the ``optimize`` hook.

    Role in the pattern: ConcreteClass.
    """

    def collect_source(self) -> None:
        """Gather the Kotlin sources."""
        print("Collecting Kotlin source code")

    def compile_to_object(self) -> None:
        """Compile the Kotlin sources to DEX bytecode."""
        print("Compiling Kotlin code to DEX bytecode")

    def optimize(self) -> None:
        """Shrink the DEX bytecode before running (overrides the hook)."""
        print("Shrinking DEX bytecode")

    def run(self) -> None:
        """Run the program on the Android runtime."""
        print("Program running on the Android runtime")


def client() -> None:
    """Build both apps through the same template method."""
    compilers: list[Compiler] = [IOSCompiler(), AndroidCompiler()]
    for compiler in compilers:
        print(f"== {type(compiler).__name__}")
        compiler.compile_and_run()


if __name__ == "__main__":
    client()
