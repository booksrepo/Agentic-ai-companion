# Appendix D: Cost and Token Budgeting Worksheet

Use this before deploying any agent beyond personal experimentation,
extending Chapter 10's `BudgetTracker`.

## Worksheet Fields

| Field | How to estimate it | Your value |
|---|---|---|
| Avg. input tokens per call | Measure directly (Chapter 5's `usage.input_tokens`) across your fixture set | ___ |
| Avg. output tokens per call | Same, `usage.output_tokens` | ___ |
| Calls per run (single vs. multi-agent) | Count actual LLM calls in one full pipeline execution | ___ |
| Runs per day (expected) | Based on trigger frequency — every PR, every failed build, etc. | ___ |
| Cost per input/output token | From your provider's current pricing page — always verify current, not remembered | ___ |
| Retry/consistency-check multiplier | 1x if no retries; 2x if you added Chapter 5's consistency check; higher if retries are uncapped (never ship uncapped) | ___ |
| Reviewer time per output (minutes) | Honest estimate of human review time, per Chapter 3's checklist, not zero | ___ |
| Reviewer time cost per hour | Your team's loaded cost estimate | ___ |

## Formula

```
daily_token_cost = (avg_input_tokens + avg_output_tokens) * calls_per_run
                   * runs_per_day * retry_multiplier * cost_per_token

daily_review_cost = runs_per_day * (reviewer_minutes / 60) * reviewer_hourly_cost

daily_total_cost = daily_token_cost + daily_review_cost
```

## Extending Chapter 10's Budget Tracker

`daily_budget_tracker.py` in this folder extends Chapter 10's per-run
`BudgetTracker` with a *daily* ceiling — set `max_daily_cost_usd`
deliberately, in advance, as a number you and your team have explicitly
agreed you're comfortable with, not a number you discover you should have
set after the fact.
