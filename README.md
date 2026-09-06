# Agentic AI Engineering for Junior Devs — Companion Repository

Companion code for *Agentic AI Engineering for Junior Devs: A Practical
Guide to Building, Securing, and Scaling AI Agents in DevOps Workflows* by
Simon Marcus.

As the book puts it in Chapter 14:

> "Everything built across these fourteen chapters — every agent, every
> rubric, every guardrail function — is meant to be a starting point you
> adapt, not a museum piece you admire."

Treat everything here the way the book teaches you to treat any
AI-generated output: a useful starting point that still needs your own
review, your own fixtures, and your own judgment before you trust it with
anything real.

## What's in this repository

- **`chapters/`** — full, runnable source code for every demo in Chapters
  2 through 12, one folder per chapter, each with its own README covering
  the Concept → Demo → Break It → Fix It → Guardrail → Checkpoint shape
  the book uses throughout.
- **`rubrics/`** — a standalone rubric template library (review, triage,
  PR-quality, and incident-memory rubrics, plus the Chapter 9 multi-agent
  prompt set) you can adapt to your own stack.
- **`checklists/`** — the consolidated production-readiness checklist
  (Chapter 13), the guardrail checklist by chapter (Appendix B), and the
  full progressive-autonomy reference table (Appendix A).
- **`fixtures/`** — a starter fixture-set template for building your own
  ground-truth evaluation set, per the pattern used in Chapters 5, 6, and 9.
- **`appendix/`** — tool-agnostic setup notes for teams not using GitHub
  Actions or Terraform (Appendix C), and a cost/token budgeting worksheet
  extending Chapter 10's `BudgetTracker` (Appendix D).

## Chapter map

| Folder | Chapter | What it builds |
|---|---|---|
| `chapters/ch02_fundamentals_refresher` | 2 | Git/CI/CD/IaC fundamentals demo — no AI yet, on purpose |
| `chapters/ch03_first_ai_workflow` | 3 | The `apply_discount` bug: why a green CI check isn't proof of correctness |
| `chapters/ch04_review_agent` | 4 | A Level 0 code-review agent |
| `chapters/ch05_ci_triage_agent` | 5 | A Level 0 CI-failure triage agent with honest confidence |
| `chapters/ch06_pr_quality_agent` | 6 | PR quality review, hardened against prompt injection |
| `chapters/ch07_agent_memory` | 7 | Persistent incident memory, and how it gets poisoned |
| `chapters/ch08_mcp_github_server` | 8 | A real MCP server exposing three narrow GitHub tools |
| `chapters/ch09_multi_agent_pipeline` | 9 | Investigator → Diagnostician → Communicator sequential pipeline |
| `chapters/ch10_observability_and_budget` | 10 | Tracing, a dashboard, retry caps, and budget enforcement |
| `chapters/ch11_guardrails_and_approval` | 11 | A structural approval gate and a defensible audit trail |
| `chapters/ch12_adoption_roi` | 12 | Paired ROI tracking (speed *and* quality, never just one) |

Chapters 1, 13, and 14 are conceptual/reflective and have no standalone
code — their guardrails and checklists are folded into `checklists/` and
each relevant chapter folder's README.

## Getting started

```bash
git clone <this-repo>
cd agentic-ai-companion
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Each chapter folder is self-contained — read its README before running
anything, since several chapters intentionally build on the repo created in
Chapter 2 (`chapters/ch02_fundamentals_refresher/ci-fundamentals-demo`).

You'll need your own API key for whichever LLM provider you use
(`export ANTHROPIC_API_KEY="..."` for the Anthropic examples as written),
and — for Chapter 8 onward — a fine-grained GitHub token scoped to exactly
one repository with `Issues: Read and write` only.

## A note on staleness, from the book itself

> "Where a sample uses a specific SDK or API, treat the exact method names
> and parameters as illustrative of a pattern rather than as
> guaranteed-current syntax — check your provider's live documentation
> before relying on any specific call."

The model name strings throughout this repo (`"your-provider-model-name"`)
are intentionally generic placeholders — swap in whatever your provider's
current API expects.

## License

See `LICENSE`. Applies to the code in this repository only, not to the
book's text.
