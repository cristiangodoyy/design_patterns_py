## Project Context

This is a python project: a reference catalogue of GoF design pattern
examples, grouped in `creational/`, `structural/` and `behavioral/`. Each
pattern folder has at least one "before" version (the problem, without the
pattern) and one "with" version (the pattern applied); some patterns walk
through several steps or compare variants.

When creating or modifying classes, follow the rules and templates in
PATTERNS.md and the "Design-pattern examples" section of
`.claude/python.md`. Read README.md for the repository map and each pattern
folder's README.md for the reasoning and the caveats of each example.

Every example module has a numpydoc module docstring with `Pattern:`,
`Counterpart:`, `Notes` (Scenario / What goes wrong in "before" files; Why /
When to use / Trade-offs / Related in "with" files) and `Roles::`. Every
class of a "with" file declares its `Role in the pattern` in its docstring.

The tests in `tests/unit/` are the executable version of the guide: a smoke
test that runs every example, a test that runs each snippet of PATTERNS.md,
and `tests/unit/test_docs_in_sync.py`, which checks that every example file
and class is documented. A PostToolUse hook (`.claude/settings.json`) runs
it after each edit: if it reports a failure, update the README of the
pattern (or README.md / PATTERNS.md, or the module docstring) before
finishing.

## Repository assumptions

- Python is the primary implementation language.
- Use `uv` as the package and command runner.
- Use `pytest` for tests.
- Use `ruff` for linting and formatting policy.
- Use `mypy` (strict) for type checking: every example must be fully typed.
- Keep the examples dependency-free and self-contained: they illustrate
  design patterns, not libraries, and never import from another example.
- Keep money as `int` cents.
- Keep the file naming scheme: `<example>_before_<pattern>.py` and
  `<example>_with_<variant>_<pattern>.py`.

## Validation command preference

Prefer commands in this order, depending on the affected code:

```bash
uv run --group tests pytest path/to/test_file.py -q
uv run --group tests pytest -m unit -q
uv run --group linters ruff check .
uv run --group linters ruff format --check .
uv run --group linters mypy .
```

## graphify

This project has a knowledge graph at .docs/ with god nodes, community structure, and cross-file relationships.

Rules:
- When .docs/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If .docs/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read .docs/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed .docs/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.
