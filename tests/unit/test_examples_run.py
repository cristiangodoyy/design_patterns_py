"""Smoke test: every example module runs as a script without errors."""

import runpy

from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[2]
CATEGORIES = ("creational", "structural", "behavioral")
EXAMPLES = sorted(
    path
    for category in CATEGORIES
    for path in (ROOT / category).glob("*/*.py")
    if path.stem != "__init__"
)


@pytest.mark.parametrize(
    "example",
    EXAMPLES,
    ids=[str(p.relative_to(ROOT)) for p in EXAMPLES],
)
def test_example_runs(example: Path) -> None:
    # run_path executes the file as a script without touching sys.modules,
    # so examples that reuse class names never clash with each other.
    runpy.run_path(str(example), run_name="__main__")
