# Chapter 5 — Agentic AI for CI/CD Failure Triage

Builds on `ci-fundamentals-demo` from Chapter 2. This is a Level 0 agent
that reads a pytest failure log and honestly reports its own uncertainty —
the first agent in the book that's promoted, in Chapter 6, toward Level 1.

## Setup

1. Add `calculate_average` (see `app_additions.py`) to
   `ci-fundamentals-demo/app.py`.
2. Add the tests in `test_app_additions.py` to `test_app.py`.
3. Run `pytest -v > failure_log.txt 2>&1` locally — you'll get a
   `ZeroDivisionError` because the function never checks for an empty list.
4. Run the agent:

```bash
python triage_agent.py
```

You should get something close to:

```json
{
  "category": "test_logic",
  "evidence": "ZeroDivisionError: division by zero",
  "diagnosis": "calculate_average does not handle an empty list input, causing a division by zero when sum(numbers) is divided by len(numbers) which is 0.",
  "confidence": 0.95,
  "suggested_fix": "Add a check for an empty list at the start of calculate_average and return 0 or raise a clear error."
}
```

`fixtures/zero_division_log.txt` and `test_triage_agent.py` give you a real,
historical example with a known correct answer — the ground-truth "fixture"
this book insists you build *before* trusting any agent's output.

## Break It

Add the deliberately flawed `test_calculate_average_timing_sensitive` test
from `test_app_additions.py`, which fails intermittently for timing reasons
unrelated to `calculate_average` itself. Feed its failure log to the agent.
It will often confidently report `category: "test_logic"` with a
specific-sounding diagnosis about the function being slow — when the real
category is `"flaky"`, and the real fix is deleting or rewriting the test,
not touching `calculate_average` at all.

## Fix It / Guardrails

- **`validate_triage`** enforces the confidence threshold in code rather
  than trusting the prompt: a low-confidence result can't carry a suggested
  fix through untouched.
- **`triage_with_consistency_check`** runs the triage twice and treats a
  disagreement between runs as `"unknown"` rather than picking one answer
  arbitrarily.
- **`triage_failure_with_cost`** logs token usage on every call — instrument
  cost from day one, not after the first surprising bill.

A model's self-reported confidence is itself a probabilistic claim. Enforce
thresholds in code; don't trust the prompt to be obeyed.

## Exercise

Extend `TRIAGE_RUBRIC` to add a new category relevant to a pipeline you
actually work with, and validate it against a real failure log from that
pipeline.
