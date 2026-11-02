"""The Python snippets of PATTERNS.md run, so the guide does not go stale."""

import re

from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

PATTERNS = Path(__file__).resolve().parents[2] / "PATTERNS.md"
SNIPPETS = re.findall(
    r"```python\n(.*?)```", PATTERNS.read_text(encoding="utf-8"), re.DOTALL
)


def test_patterns_has_snippets() -> None:
    assert SNIPPETS


@pytest.mark.parametrize("index", range(len(SNIPPETS)))
def test_snippet_runs(index: int) -> None:
    # Each template is self-contained (one per pattern), so it runs in a
    # fresh namespace: templates reuse names such as Observer or Subject.
    namespace: dict[str, object] = {"__name__": f"patterns_snippet_{index}"}
    exec(SNIPPETS[index], namespace)  # noqa: S102

    for name, value in list(namespace.items()):
        if name.startswith("test_") and callable(value):
            value()
