# Chapter 4 — What Is an AI Agent, Really?

A Level 0 (suggest-only) review agent: perceive (read the staged diff) →
decide (ask an LLM against a rubric) → observe (print to your terminal).
Nothing is posted anywhere; a human reads every suggestion.

## Setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install anthropic   # or your LLM provider's SDK — the pattern is identical
export ANTHROPIC_API_KEY="your-key-here"
```

## Run it

```bash
git add .
python review_agent.py
```

## Break It

Imagine the rubric asked for a `line_number` field instead of `line_hint`,
and `display_suggestions` printed it directly as "see line 47." Run that
version against a real diff a few times — the LLM's line numbers are
frequently off by a few lines, especially across multiple hunks or renamed
files. It isn't lying; it's producing a plausible, fluent continuation, and a
precise-looking integer is exactly the kind of claim you need to verify
rather than trust.

## Fix It / Guardrail

1. **Prefer verifiable references over precise-looking guesses.** That's why
   this agent asks for `line_hint` (a quoted snippet you can search for)
   instead of `line_number` (an integer the model has to count correctly).
2. **`validate_suggestions`** is the deterministic check wrapped around the
   probabilistic output: if `line_hint` isn't a real substring of the diff,
   the suggestion is dropped and flagged, not trusted.

A Level 0 agent's output is a draft, never a verdict. Structure in an output
(JSON, schemas) guarantees parseability, not correctness.

## Exercise

Run the agent against a diff with an intentional bug (reuse the
`apply_discount` bug from `ch03_first_ai_workflow` if you still have that
repo). Did it catch the issue? If it printed something confidently wrong,
use the validation habits above to figure out why.
