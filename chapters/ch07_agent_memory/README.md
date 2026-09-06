# Chapter 7 — Memory for Agents

Memory is an attack surface. This chapter gives an incident-triage agent
persistent memory of past incidents, then deliberately poisons it to show
why "verified" and "confirmed effective" must be separate concepts.

## Demo

```python
from memory_store import init_db, record_resolution
from memory_agent import triage_with_memory

conn = init_db()
record_resolution(
    conn, "payments_service_5xx",
    root_cause="connection pool exhaustion under load",
    resolution="increased pool size from 10 to 50, added pool utilization alert",
    created_by="oncall-engineer-jdoe",
    verified=True,
)
result = triage_with_memory(conn, "payments_service_5xx", "5xx errors spiking again")
```

## Break It

Run `poison_the_memory(conn)` from `memory_poisoning_example.py` — a bad
record, written as `verified=True` "in the rush," without real confirmation.
Call `triage_with_memory` again for the same incident type. Because the bad
record is marked verified, it sorts ahead of genuinely correct memories and
gets treated as reliable precedent — the agent confidently suggests
restarting the database, which does nothing for the real problem, and (worse)
will get recorded as "verified" again if the same rushed process repeats.

## Fix It / Guardrails

1. **Separate "verified" from "confirmed effective."** `record_resolution`
   now defaults both `verified` and `provisional` sensibly — a human typing
   something in is not the same as a human confirming it actually worked
   after some observation period. Records start `provisional=True`
   regardless of who entered them.
2. **`promote_from_provisional`** is the only path to trusted status, and
   should only be called after a genuine post-incident review — not the same
   rushed moment the original resolution was recorded in.
3. **`retract_memory`** gives every bad memory a fast retraction path, and
   logs the retraction itself.
4. **`max_age_days` in `get_relevant_memories`** applies expiry as a
   default: an unreviewed bad memory eventually ages out of consideration
   even if nobody catches it manually.

Treat "the agent decided to remember something" as an action on the same
autonomy scale as any other agent action — a memory write is not a passive
operation. It's a decision that will influence every future decision that
reads it.
