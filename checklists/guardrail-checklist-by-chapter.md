# Guardrail Checklist by Chapter

*From Appendix B. A map back to where each specific guardrail came from —
useful when you need to explain why a rule exists, not just that it does.*

| Chapter | Guardrail |
|---|---|
| 1 | Deterministic checks around probabilistic output. The foundational principle every later guardrail is a specific implementation of. |
| 2 | Never automate what you can't read and explain yourself. Applies to CI pipelines, IaC configs, and anything else you'd hand an agent access to. |
| 3 | Human-in-the-loop as a non-negotiable default. No AI-generated code merges without a human reading it line by line and writing at least one independent test. |
| 4 | A Level 0 agent's output is a draft, never a verdict. Structure in an output (JSON, schemas) guarantees parseability, not correctness. |
| 5 | A model's self-reported confidence is itself a probabilistic claim. Enforce thresholds in code; don't trust the prompt to be obeyed. |
| 6 | The Level 0-to-1 promotion checklist: measured track record, adversarial testing, narrow scope, narrow credentials, an easy undo path, genuine (not reflexive) human review. |
| 7 | Memory is an attack surface. Separate "recorded" from "confirmed," give bad memories a fast retraction path, apply expiry as a default. |
| 8 | Tool interface design is itself a security boundary. Build narrow, specific tools; scope credentials to match; sanitize and truncate what comes back from a tool. |
| 9 | One agent's output is not ground truth just because it came from inside your own pipeline. Carry confidence and provenance across every handoff; verify before trusting downstream. |
| 10 | Cost governance belongs in initial design. Hard retry caps, backoff for transient errors only, enforced budget limits — an unbounded loop is an unbounded permission. |
| 11 | A defensible audit trail snapshots what was known at decision time. Never reference something that can keep changing underneath an approval. |
| 12 | Never report a speed or cost metric without its paired quality metric. An ROI claim built on one number deserves the same skepticism as an ungrounded AI output. |
| 13 | The level describes the system, not the model. Revisit this whenever a "smarter model" is offered as justification for more autonomy. |
