# Chapter 9 — When (and Why) to Use Multiple Agents

A sequential pipeline: Investigator → Diagnostician → Communicator. Simple,
predictable, and easy to debug — but a mistake anywhere in the chain flows
straight through to every downstream stage.

## Run it

```python
from pipeline import run_incident_pipeline

result = run_incident_pipeline("<raw logs and metrics here>")
print(result["communication"]["status_update"])
```

## Break It

`prompts.INVESTIGATOR_PROMPT_ORIGINAL` is the under-specified version used
in this chapter's "Break It" section. Feed it a batch of metrics where CPU
usage is reported as `340%` — a real but slightly unusual value that can
legitimately occur when per-core percentages are summed on a multi-core
system. An imprecise Investigator may report: *"CPU usage spiked to 340%,
indicating a severe single-process runaway loop."* The number is accurate;
the interpretation ("a runaway loop") is a plausible-sounding guess dressed
as an observation.

The Diagnostician has no way to know the framing was an unearned
interpretation rather than a directly observed fact — from its point of
view, that's simply what "the investigation" reported. It builds a confident
diagnosis on top of it: `likely_cause: "A runaway process is consuming
excessive CPU..."`, `confidence: 0.85`. This is a **cascading
hallucination**: an unearned claim from one stage propagating, unquestioned,
into every downstream conclusion.

## Fix It / Guardrails

1. **`prompts.INVESTIGATOR_PROMPT`** (the version wired into `pipeline.py`
   by default) restricts the Investigator to direct quotes with no
   interpretation added, and a factual `notable_because` reason instead of
   a diagnosis.
2. **`verify_diagnosis_grounded`** adds a deterministic check between
   stages: before a diagnosis is trusted, its `supporting_observations`
   must actually trace back to something the Investigator genuinely
   reported. If not, confidence is forced to `0.0` and the diagnosis is
   marked unverified.

One agent's output is not ground truth just because it came from inside
your own pipeline. Carry confidence and provenance across every handoff;
verify before trusting downstream.

## Exercise

Identify one additional deterministic check you could add at the boundary
between the Diagnostician and Communicator stages, similar to
`verify_diagnosis_grounded`.
