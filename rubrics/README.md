# Rubric Template Library

Every rubric used in the book, in one place, so you can adapt them to your
own stack without hunting through chapter code.

| File | From | Purpose |
|---|---|---|
| `review_rubric.py` | Chapter 4 | General code-diff review, verifiable-reference pattern |
| `triage_rubric.py` | Chapter 5 | CI/CD failure categorization with honest confidence |
| `pr_quality_rubric.py` | Chapter 6 | PR quality checks, hardened against prompt injection |
| `incident_memory_rubric.py` | Chapter 7 | Incident triage that distinguishes verified/unverified memory |
| `multi_agent_prompts.py` | Chapter 9 | Investigator / Diagnostician / Communicator pipeline prompts |

## How to adapt a rubric

1. **Keep the "return ONLY JSON" instruction and the exact field names** —
   downstream code parses these rubrics' output as structured data. If you
   change a field name, update every function that reads it.
2. **Keep any `CRITICAL` / data-vs-instruction paragraph.** These are the
   book's prompt-injection defenses (Chapter 6, Chapter 8). Removing them
   to "clean up" a rubric reopens the exact vulnerability those chapters
   walk through.
3. **Ask for verifiable references, not precise-looking guesses**, the same
   way `review_rubric.py` asks for a quoted `line_hint` instead of a
   `line_number`. If you add a new field, ask: can the model state this
   reliably, or does it only sound authoritative?
4. **Treat every rubric as a draft**, the same way this book treats every
   AI-generated output: a useful starting point that still needs your own
   review, your own fixtures, and your own judgment before you trust it
   with anything real.
