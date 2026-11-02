"""Build and run programs with compilers that each repeat the pipeline.

Pattern: Template Method (behavioral), problem side.
Counterpart: ``compiler_with_template_method.py``.

Notes
-----
Scenario:
    A toolchain builds mobile apps for iOS and Android. Both compilers
    go through the same pipeline: collect the sources, compile them to
    an intermediate form, then run the program. Android also shrinks
    its bytecode before running.

What goes wrong here:
    - The step sequence is copied into every compiler; changing the
      pipeline means editing every class and keeping them in sync.
    - Nothing enforces the order: a new compiler can skip a step or
      run them in the wrong order without anyone noticing.
    - There is no common entry point, so clients must know each
      compiler's own method name.

Roles::

    IOSCompiler.build()              AndroidCompiler.compile_and_run()
      collect -> compile -> run        collect -> compile -> shrink -> run
      (same skeleton, written twice, free to drift apart)
"""


class IOSCompiler:
    """Compile Swift code, with its own copy of the pipeline."""

    def build(self) -> None:
        """Collect, compile and run, in an order fixed only by habit."""
        print("Collecting Swift source code")
        print("Compiling Swift code to LLVM bitcode")
        print("Program running on the iOS runtime")


class AndroidCompiler:
    """Compile Kotlin code, with a second copy of the pipeline."""

    def compile_and_run(self) -> None:
        """Repeat the same pipeline plus an extra shrinking step."""
        print("Collecting Kotlin source code")
        print("Compiling Kotlin code to DEX bytecode")
        print("Shrinking DEX bytecode")
        print("Program running on the Android runtime")


def client() -> None:
    """Build both apps; note the client must know two method names."""
    IOSCompiler().build()
    AndroidCompiler().compile_and_run()


if __name__ == "__main__":
    client()
