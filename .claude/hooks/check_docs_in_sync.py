"""Claude Code PostToolUse hook: keep the docs in sync with the examples.

After Claude edits an example (.py inside a pattern folder under creational/,
structural/ or behavioral/) or a Markdown doc, run
tests/unit/test_docs_in_sync.py. On failure, exit with code 2 so the test
output is sent back to Claude, which then updates the README of the
pattern, README.md, PATTERNS.md or the module docstrings in the same turn.
"""

import json
import subprocess
import sys

from pathlib import PurePath

CATEGORIES = {"creational", "structural", "behavioral"}


def _is_watched(file_path: str) -> bool:
    path = PurePath(file_path.replace("\\", "/"))
    if path.suffix == ".md":
        return True
    # Examples live in <category>/<pattern>/<example>.py.
    return (
        path.suffix == ".py"
        and len(path.parents) > 1
        and path.parents[1].name in CATEGORIES
    )


def client() -> int:
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input", {})
    file_path = str(tool_input.get("file_path", ""))
    if not _is_watched(file_path):
        return 0

    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--no-header",
            "-p",
            "no:cacheprovider",
            "tests/unit/test_docs_in_sync.py",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return 0

    failures = [
        line
        for line in result.stdout.splitlines()
        if line.startswith("E ") or "AssertionError" in line
    ]
    # stderr + exit code 2 is how a hook sends its message back to Claude.
    sys.stderr.write(
        "The documentation is out of sync with the examples. Update the "
        "README of the pattern (or README.md / PATTERNS.md, or the module "
        "docstring of the example):\n"
        + "\n".join(failures or result.stdout.splitlines()[-20:])
        + "\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(client())
