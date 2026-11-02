"""The documentation stays in sync with the example modules.

If one of these tests fails after changing an example, update the README of
the pattern folder, the main README.md, PATTERNS.md or the module docstring
of the example, as the message says.
"""

import ast
import re

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
EXAMPLE_IDS = [str(p.relative_to(ROOT)) for p in EXAMPLES]
PATTERN_DIRS = sorted({path.parent for path in EXAMPLES})
PATTERN_IDS = [str(p.relative_to(ROOT)) for p in PATTERN_DIRS]
# Sections every module docstring must have; see any example for the layout.
REQUIRED_SECTIONS = ("Pattern:", "Counterpart:", "Notes\n-----", "Roles::")
FILE_REFERENCE = re.compile(r"``([A-Za-z0-9_]+\.py)``")
# Names that shadow Python built-ins: the templates must not use them.
FORBIDDEN_NAMES = {"id", "type"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _tree(example: Path) -> ast.Module:
    return ast.parse(_read(example))


def _module_docstring(example: Path) -> str:
    return ast.get_docstring(_tree(example)) or ""


def _public_classes(example: Path) -> list[str]:
    return [
        node.name
        for node in _tree(example).body
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
    ]


@pytest.mark.parametrize("example", EXAMPLES, ids=EXAMPLE_IDS)
def test_example_is_linked_in_the_main_readme(example: Path) -> None:
    link = f"({example.relative_to(ROOT).as_posix()})"

    assert link in _read(ROOT / "README.md"), (
        f"{example.relative_to(ROOT)} is not linked in the repository map "
        "of README.md"
    )


@pytest.mark.parametrize("pattern_dir", PATTERN_DIRS, ids=PATTERN_IDS)
def test_pattern_readme_is_linked_in_the_main_readme(
    pattern_dir: Path,
) -> None:
    link = f"({pattern_dir.relative_to(ROOT).as_posix()}/README.md)"

    assert link in _read(ROOT / "README.md"), (
        f"{pattern_dir.relative_to(ROOT)}/README.md is not linked in the "
        "repository map of README.md"
    )


@pytest.mark.parametrize("example", EXAMPLES, ids=EXAMPLE_IDS)
def test_example_is_linked_in_its_readme(example: Path) -> None:
    readme = example.parent / "README.md"

    assert readme.exists(), f"{example.parent.relative_to(ROOT)} has no README"
    assert f"({example.name})" in _read(readme), (
        f"{example.name} is not linked in the 'Archivos' table of "
        f"{example.parent.relative_to(ROOT)}/README.md"
    )


@pytest.mark.parametrize("example", EXAMPLES, ids=EXAMPLE_IDS)
def test_example_classes_are_documented(example: Path) -> None:
    readme = _read(example.parent / "README.md")

    missing = [
        name
        for name in _public_classes(example)
        if not re.search(rf"\b{name}\b", readme)
    ]

    assert not missing, (
        f"Classes of {example.name} not mentioned in "
        f"{example.parent.relative_to(ROOT)}/README.md: {', '.join(missing)}"
    )


@pytest.mark.parametrize("example", EXAMPLES, ids=EXAMPLE_IDS)
def test_module_docstring_has_required_sections(example: Path) -> None:
    docstring = _module_docstring(example)

    missing = [name for name in REQUIRED_SECTIONS if name not in docstring]

    assert not missing, (
        f"Module docstring of {example.name} lacks: {', '.join(missing)}"
    )


@pytest.mark.parametrize("example", EXAMPLES, ids=EXAMPLE_IDS)
def test_referenced_files_exist(example: Path) -> None:
    referenced = set(FILE_REFERENCE.findall(_module_docstring(example)))

    missing = sorted(
        name for name in referenced if not (example.parent / name).exists()
    )

    assert not missing, (
        f"{example.name} references files that do not exist in "
        f"{example.parent.relative_to(ROOT)}/: {', '.join(missing)}"
    )


@pytest.mark.parametrize(
    "example",
    [path for path in EXAMPLES if "_with_" in path.name],
    ids=[pid for pid in EXAMPLE_IDS if "_with_" in pid],
)
def test_pattern_classes_declare_their_role(example: Path) -> None:
    missing = [
        node.name
        for node in _tree(example).body
        if isinstance(node, ast.ClassDef)
        and not node.name.startswith("_")
        and "Role in the pattern" not in (ast.get_docstring(node) or "")
    ]

    assert not missing, (
        f"Classes of {example.name} without 'Role in the pattern' in "
        f"their docstring: {', '.join(missing)}"
    )


@pytest.mark.parametrize("pattern_dir", PATTERN_DIRS, ids=PATTERN_IDS)
def test_pattern_readme_links_to_patterns_md(pattern_dir: Path) -> None:
    readme = _read(pattern_dir / "README.md")

    assert "PATTERNS.md#" in readme, (
        f"{pattern_dir.relative_to(ROOT)}/README.md does not link its "
        "template in PATTERNS.md"
    )


def _python_blocks(markdown: str) -> list[str]:
    return re.findall(r"```python\n(.*?)```", markdown, re.DOTALL)


def _patterns_sections() -> list[tuple[str, Path, list[str]]]:
    """Return (heading, pattern folder, python blocks) per PATTERNS.md entry.

    Each pattern section ends with an "Ejemplo completo" link to its folder.
    """
    sections = re.split(r"^### ", _read(ROOT / "PATTERNS.md"), flags=re.M)
    result = []
    for section in sections[1:]:
        heading = section.splitlines()[0]
        link = re.search(r"\]\(([\w/]+)/README\.md\)", section)
        assert link, f"PATTERNS.md section {heading!r} has no example link"
        result.append((heading, ROOT / link.group(1), _python_blocks(section)))
    return result


PATTERNS_SECTIONS = _patterns_sections()


def _module_definitions(
    pattern_dir: Path,
) -> tuple[dict[str, set[str]], set[str]]:
    """Return {class: method and attribute names} and the module functions."""
    classes: dict[str, set[str]] = {}
    functions: set[str] = set()
    for example in pattern_dir.glob("*.py"):
        for node in _tree(example).body:
            if isinstance(node, ast.ClassDef):
                classes.setdefault(node.name, set()).update(
                    _member_names(node)
                )
            elif isinstance(node, ast.FunctionDef):
                functions.add(node.name)
    return classes, functions


def _member_names(node: ast.ClassDef) -> set[str]:
    names: set[str] = set()
    for member in node.body:
        if isinstance(member, ast.FunctionDef):
            names.add(member.name)
    return names


@pytest.mark.parametrize(
    ("heading", "pattern_dir", "blocks"),
    PATTERNS_SECTIONS,
    ids=[heading for heading, _, _ in PATTERNS_SECTIONS],
)
def test_patterns_template_follows_its_examples(
    heading: str, pattern_dir: Path, blocks: list[str]
) -> None:
    classes, functions = _module_definitions(pattern_dir)
    unknown: list[str] = []
    for block in blocks:
        for node in ast.parse(block).body:
            if isinstance(node, ast.ClassDef):
                if node.name not in classes:
                    unknown.append(f"class {node.name}")
                    continue
                unknown += [
                    f"{node.name}.{name}"
                    for name in sorted(_member_names(node))
                    if name not in classes[node.name]
                ]
            elif isinstance(node, ast.FunctionDef):
                if not node.name.startswith("test_") and (
                    node.name not in functions
                ):
                    unknown.append(f"def {node.name}")

    assert blocks, f"PATTERNS.md section {heading!r} has no template"
    assert not unknown, (
        f"The {heading} template in PATTERNS.md uses names that do not "
        f"exist in {pattern_dir.relative_to(ROOT)}/: {', '.join(unknown)}"
    )


@pytest.mark.parametrize("pattern_dir", PATTERN_DIRS, ids=PATTERN_IDS)
def test_readme_snippets_are_copied_from_the_examples(
    pattern_dir: Path,
) -> None:
    source_lines = {
        line.strip()
        for example in pattern_dir.glob("*.py")
        for line in _read(example).splitlines()
    }
    readme = _read(pattern_dir / "README.md")

    missing = [
        line.strip()
        for block in _python_blocks(readme)
        for line in block.splitlines()
        if line.strip() not in {"", "..."} and line.strip() not in source_lines
    ]

    assert not missing, (
        f"Code in {pattern_dir.relative_to(ROOT)}/README.md that is not "
        f"in its examples: {missing}"
    )


def test_patterns_templates_do_not_shadow_builtins() -> None:
    snippets = re.findall(
        r"```python\n(.*?)```", _read(ROOT / "PATTERNS.md"), re.DOTALL
    )
    offending: set[str] = set()
    for snippet in snippets:
        for node in ast.walk(ast.parse(snippet)):
            if isinstance(node, ast.AnnAssign) and isinstance(
                node.target, ast.Name
            ):
                offending.add(node.target.id)
            elif isinstance(node, ast.arg):
                offending.add(node.arg)
            elif isinstance(node, ast.Attribute):
                offending.add(node.attr)

    assert not offending & FORBIDDEN_NAMES, (
        "PATTERNS.md templates use names that shadow built-ins: "
        f"{', '.join(sorted(offending & FORBIDDEN_NAMES))}"
    )
