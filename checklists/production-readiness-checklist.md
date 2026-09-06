# Production Readiness Checklist (Consolidated)

*From Chapter 13. The one-page version, gathering every chapter's individual
guardrail into a single reference — also reproduced in Appendix B, mapped
back to the chapter each item came from.*

Before trusting any agent beyond personal experimentation, confirm:

- [ ] Structured output is validated, and malformed responses are treated
      as failures, never silently as success.
- [ ] Confidence is honestly reported and enforced in code, not just
      requested in a prompt.
- [ ] The agent has been tested against adversarial and ambiguous input,
      not just clean, cooperative examples.
- [ ] Any memory is provisional until explicitly confirmed, with an easy
      retraction path and an expiry policy.
- [ ] Tools are narrow and specific; credentials are scoped to least
      privilege matching those tools exactly.
- [ ] Any multi-agent handoff carries evidence and confidence forward, and
      downstream stages verify rather than blindly trust.
- [ ] The system is instrumented with traces, logs, and metrics sufficient
      to reconstruct any run after the fact.
- [ ] Hard budget caps and retry limits exist in code, sized to what you're
      actually willing to spend if an exit condition is never naturally
      satisfied.
- [ ] Prompts, schemas, and thresholds are version-controlled and reviewed
      like code.
- [ ] Any promotion up the autonomy scale has a documented, defensible
      approval record, made by someone with the authority to accept the
      resulting risk.

If you can't check most of these boxes for a given agent, that's not a
failure — it just tells you honestly which phase of the rollout plan you're
actually in.
