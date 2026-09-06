# Chapter 12 — Building an AI Adoption Playbook (and Measuring ROI)

`roi_dashboard.py` tracks paired outcomes — AI-assisted vs. manual, for the
same task type — because a single metric reported in isolation can make a
real regression look like a real win.

## The trap this guards against

A dashboard that reports "cycle time dropped 80%" and nothing else looks
fantastic, and it's built on real data. But if nobody's tracking
`defect_found_later`, a plausible and realistic failure can hide underneath
that headline: reviewers, seeing the agent's summary consistently flag the
"obvious" issues, start skimming rather than reading line by line — exactly
the failure mode Chapter 3 warned about, now happening at team scale.
Defects a careful human reviewer would have caught start shipping more
often, but nobody notices until a production incident forces the question.

## Guardrail

Never report a speed or cost metric without its paired quality metric. An
ROI claim built on one number deserves the same skepticism as an ungrounded
AI output.

```python
from roi_dashboard import init_roi_db, print_roi_summary

conn = init_roi_db()
print_roi_summary(conn, task_type="pr_review")
```
