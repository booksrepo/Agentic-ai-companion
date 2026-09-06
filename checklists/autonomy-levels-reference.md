# Progressive Autonomy Levels — Full Reference Table

*From Appendix A. The poster version — pin this near your desk. Every
promotion between levels should be a deliberate, evidence-based decision
(Chapter 6), never a default that happens because nobody thought about it.*

**The one rule that applies at every level:** the level describes the
system you've built around a model, not a property of the model itself
(Chapter 13). The same underlying LLM can sit behind a Level 0 tool and a
Level 3 operator — what changes is the validation, scoping, and oversight
engineered around it.

## Table A.1 — What each level is and who's involved

| Level | Name | What it means | Human involvement | Example |
|---|---|---|---|---|
| 0 | Suggest-only | Agent produces recommendations; takes no real-world action | Human reads every output; nothing happens without separate human-initiated action | An agent that reads a diff and prints review comments to a console — nothing is posted anywhere |
| 1 | Approve-every-action | Agent proposes one specific action; a human approves or rejects each one individually | Human reviews and explicitly approves each proposed action before it happens | An agent that drafts a single GitHub comment and waits for a human to click "post" |
| 2 | Approve-in-batches | Agent proposes a set of related actions; a human reviews and approves the batch as a whole | Human reviews the full batch before any part of it executes | An agent that drafts an entire PR (multiple file changes) for human review and merge |
| 3 | Autonomous-in-sandbox | Agent acts without per-action approval, but only within an isolated, low-consequence environment | Human monitors aggregate behavior and outcomes, not individual actions | An agent that can freely create, modify, and destroy resources in a scratch/dev cloud account with no real traffic |
| 4 | Autonomous-in-production | Agent acts without per-action human approval, against real, live systems | Human sets numeric or policy bounds in advance and audits after the fact | A rare, heavily audited case — e.g., an agent auto-scaling infrastructure within pre-approved numeric bounds |

## Table A.2 — What it takes to reach each level, and what to watch for

| Level | Typical credential scope | Evidence required for promotion | Primary risk if misused |
|---|---|---|---|
| 0 | None required — agent can be entirely read-only | None — the safe default starting point for any new agent | Output is trusted reflexively instead of verified (Ch. 4) |
| 1 | Scoped to exactly one action type (e.g., post-comment only, per Ch. 8) | A measured accuracy track record from Level 0, plus adversarial testing (Ch. 6) | Approval becomes a reflex rather than genuine review (Ch. 6) |
| 2 | Scoped to the batch's action type, no broader than necessary | Sustained, measured track record at Level 1, where a wrong batch is cheap to reverse | A single bad item in an otherwise-good batch gets approved by association |
| 3 | Scoped entirely to the sandbox — no path to production | Documented success at Level 2, and a genuinely isolated environment | Sandbox isolation is weaker than assumed, letting actions leak into real systems |
| 4 | Scoped as narrowly as the bounded task allows, even in production | Rare — requires organizational sign-off, not just engineering confidence (Ch. 11) | Any gap between bounds set and bounds needed becomes a real, live incident |

## For reference — Script vs. Chatbot vs. Agent (Chapter 1)

| | Script | Chatbot | Agent |
|---|---|---|---|
| Decision-making | None — fixed logic, same input always produces same output | Produces a response based on the conversation, but takes no action | Decides what action to take based on current state |
| Tool use | Executes fixed operations, no reasoning about which to use | None — text in, text out | Chooses and calls tools as part of reaching a goal |
| Adaptability | Zero — a script does exactly what it's coded to do, forever | Can vary its wording, but not its capability | Can vary both what it says and what it does |
| Failure mode | Predictable — the same bug fires the same way every time | Says something wrong, but changes nothing in the world | Can act on a wrong belief, which changes something real |
| Example | cron job that runs a nightly backup | An FAQ assistant answering "how do I reset my password" | A system that reads a failed build, forms a hypothesis, checks the lockfile, and reports a diagnosis |
