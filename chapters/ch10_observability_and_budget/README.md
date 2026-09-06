# Chapter 10 — Running and Observing a Multi-Agent Workflow

Takes Chapter 9's pipeline and runs it for real: instrumentation, a live
dashboard, and the guardrails that stop an agent loop from quietly costing
far more than intended before anyone notices.

## Instrumentation

`tracing_setup.py` and `instrumented_pipeline.py` wrap every agent call in an
OpenTelemetry span, tagging role, input size, token usage, and confidence.
`dashboard.py` gives you a same-day summary across all agent roles.

```bash
pip install opentelemetry-api opentelemetry-sdk
```

## Break It

`runaway_loop_example.py`'s `run_incident_pipeline_unbounded` looks
reasonable — "if we're not confident, look again" — but nothing bounds how
many times "again" can happen. This is the exact same shape as an infinite
`while` loop in any ordinary program, except each iteration costs real money
and real time, and nothing about the failure is visible from the pipeline's
final output. If it eventually terminates, you get a normal-looking result
with no indication it silently burned forty times the expected cost getting
there.

## Fix It / Guardrails

`pipeline_with_guardrails.py` fixes this with three independent limits:

1. **`MAX_RETRIES`** — a hard cap on confidence-driven retries.
2. **`call_with_backoff`** — exponential backoff for *transient* errors
   (rate limits) only, kept separate from the confidence-retry logic above.
3. **`BudgetTracker`** — an enforced per-run token budget that raises a
   clear, immediate, catchable `BudgetExceededError` the moment a single
   run's cost crosses a threshold you chose deliberately in advance.

Before you ship any loop — a retry, a supervisor re-invoking a worker,
anything with a `while` condition driven by a model's own output — ask
explicitly: *"what's the maximum this could cost if the exit condition is
never naturally satisfied?"* and put a hard limit in code that enforces the
answer you're comfortable with. That question costs thirty seconds at
design time. Skipping it costs a surprise you find out about from a bill
instead of from a trace.

See also `appendix/appendix_d_budget_worksheet/` for a daily (not just
per-run) budget extension of `BudgetTracker`.
