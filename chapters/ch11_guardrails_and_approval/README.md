# Chapter 11 — AI Guardrails, Auditing, and Accountability

`project-structure.txt` shows how to version prompts, schemas, and
thresholds like code — so a later comparison against a new prompt version
is only meaningful if you know exactly which version produced which
historical result.

`approval_gate.py` is a structural approval gate: the pipeline's "send"
function cannot run without `get_approved_content`, which raises unless a
human has explicitly recorded approval.

## Break It

`break_it_example.py`'s `request_approval_flawed` stores a *reference* to
the diagnosis (`diagnosis_id`) instead of a snapshot. If the underlying
incident evolves while the approval sits in a queue — entirely realistic
during a live incident — the diagnosis the approver reviews may no longer
match what's on record weeks later. The audit trail technically exists but
can't answer the question it exists to answer: what did the approver
actually see?

## Fix It / Guardrail

`approval_gate.request_approval` stores the **full diagnosis object**,
captured at the moment of the request, as an immutable snapshot — never a
live reference to something that can keep changing underneath the approval.

A defensible audit trail snapshots what was known at decision time. Never
reference something that can keep changing underneath an approval.

## Exercises

- Walk through the flawed `request_approval_flawed` example and identify
  exactly why storing a reference instead of a snapshot broke the audit
  trail's usefulness, even though nothing about the approval process itself
  changed.
- Using this chapter's escalation guidance: if you personally wanted to
  raise `MAX_RETRIES` from Chapter 10's circuit breaker from 3 to 10, is
  that a decision you could reasonably make alone, or does it warrant
  escalation? Justify your answer using the underlying principle, not just
  the letter of the rule.
