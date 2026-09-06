# Starter Fixture-Set Template

A "fixture" (per Chapters 5, 6, and 9, and the Appendix E glossary) is a
real, historical example with a **known correct answer**, used to measure
an agent's actual accuracy instead of relying on a general impression of
its quality. Build this *before* you trust any agent's output — the book's
Chapter 5 demo and Day 4 of the "First 30 Days" plan (Chapter 14) both
insist on this order, not the reverse.

## How to use `fixture_set_template.json`

1. Copy it and rename it for the task you're evaluating
   (e.g. `pr_quality_fixtures.json`).
2. Fill in 3–5 real, historical examples per category you care about.
   `expected` should be the answer a careful human reviewer already agrees
   on — not a guess, and not something the agent itself produced.
3. Write a test (see `chapters/ch05_ci_triage_agent/test_triage_agent.py`
   for the pattern) that runs your agent against every fixture and asserts
   the output matches `expected` within whatever tolerance is appropriate
   (exact match for categories, a threshold for confidence scores, etc.).
4. Re-run this suite whenever you change a prompt, not just when something
   seems to have gone wrong. A rubric that was well-calibrated when you
   wrote it can drift out of alignment as your codebase or the underlying
   model changes (Chapter 13).

## A note on honesty

One good result from a fixture set is a demo. A measured track record
across the *whole* fixture set is evidence — that distinction is the whole
point of Chapter 6's promotion checklist. Don't declare an agent trustworthy
because it got the first three examples right; keep expanding the set with
genuinely difficult and adversarial cases as you find them.
