# Testing and Validation Rules

## Test impact policy

Behavior changes require tests.

Add or update tests when changing:

- Business logic.
- Public APIs.
- Data models.
- Validation rules.
- Error handling.
- Persistence behavior.
- Agent/node routing.
- Evaluation logic.
- Security-sensitive behavior.
- Bug fixes.

Do not add tests only for trivial formatting, comments, or mechanical renames unless risk justifies it.

## Test location

Follow existing repository conventions.

Common preferred layout:

```text
tests/
  unit/
  integration/
  contract/
  e2e/
```

or colocated tests if the repo already uses that pattern.

Do not introduce a new test layout without a reason.

## Pytest markers

Use existing markers. If the repo has no marker policy, prefer:

- `unit`: fast, deterministic, no network, no external services.
- `integration`: may touch local containers, databases, or service adapters.
- `contract`: public API stability tests (imports, exception hierarchy, schema shape).
- `slow`: expensive or long-running.
- `e2e`: full workflow tests.

Do not mark tests as integration to avoid making them deterministic.

## Validation ladder

Run the narrowest relevant command first.

Preferred order:

```bash
uv run pytest path/to/test_file.py -q
uv run pytest -m unit -q
uv run ruff check .
uv run mypy .
uv run pre-commit run --all-files
```

For formatting-only changes:

```bash
uv run ruff check .
uv run ruff format --check .
```

For type-only changes:

```bash
uv run mypy .
```

For dependency/config changes:

```bash
uv sync --locked
uv run pytest -m unit -q
```

Only run broad suites after narrow checks pass.

## Determinism

Tests should be deterministic.

Avoid:

- Real network calls.
- Real credentials.
- Wall-clock dependence.
- Order dependence.
- Randomness without fixed seeds.
- LLM calls in unit tests.
- External services in unit tests.

Use fakes, fixtures, snapshots, local test doubles, or recorded fixtures where appropriate.

## Property-based tests

Use Hypothesis when it materially improves confidence, especially for:

- Normalization.
- Fuzzy matching.
- Parsers.
- OData/SQL compilers.
- Clustering/deduplication.
- Schema round-trips.
- Boundary conditions.

Keep property tests targeted and fast.

## LLM and agent tests

For LLM/agent workflows:

- Separate deterministic unit tests from live-model evaluations.
- Use frozen model outputs or fixtures for unit tests.
- Use explicit evaluator cases for behavior assessment.
- Do not let the agent evaluate itself as the only quality gate.
- Prefer externally defined expected outcomes.
- Record prompt/template versions when relevant.

## Snapshot tests

Do not update snapshots blindly.

Only update snapshots when:

- The changed output is intended.
- The reason is documented.
- The diff was inspected.

## Failure reporting

When tests fail, report:

- Command run.
- Failure category.
- Whether failure appears related to the change.
- Files likely involved.
- Next recommended command or patch.

Never state that the code is validated if validation failed, was skipped, or was not run.

## Test naming

Test names should communicate the unit under test, the scenario, and the expected outcome.

A test name should include:

- The method or behavior being tested.
- The scenario or context being evaluated.
- The expected result when that scenario is executed.

Prefer `given_when_then`-style phrasing when it improves clarity.

## Test grouping

Prefer class-based grouping when multiple tests target the same unit.

- Name the class `Test<Thing>`.
- Do not define `__init__`.
- Prefix methods with `test_`.

Use standalone functions only when:

- There is exactly one meaningful test for the unit.
- A one-off regression test would be less readable inside a class.

## Test structure

Structure tests with explicit Arrange, Act, Assert sections.

- Separate setup, execution, and assertions visibly.
- Use a single act per test.
- Split tests that require multiple acts into independent cases.

## Test scope and focus

Each test validates one behavior, not one method.

- Multiple tests per method are expected when each covers a distinct behavior.
- Keep tests complete and concise.
- Do not combine unrelated behaviors in a single test.
- Split complex or conditional scenarios into smaller tests instead of branching inside one.

## Assertion clarity

Assertion failures should communicate intent.

- State the expected outcome, the actual result, and the relevant parameters.
- Do not rely on generic messages that obscure why the test failed.

## Avoid brittle tests

Tests should only change when system requirements change.

Avoid:

- Hard-coded values such as expected error messages.
- Assertions on internal object usage within a public method, such as specific log messages.
- Coupling to implementation details outside the public API.

Test against the public API only.
