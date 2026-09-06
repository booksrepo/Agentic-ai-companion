# incident_memory_rubric.py — Chapter 7
# An incident-triage rubric that explicitly distinguishes VERIFIED from
# UNVERIFIED past incidents when reasoning from memory.

INCIDENT_RUBRIC = """
You are helping triage a live incident. You will be given the current
symptoms and, if available, relevant past incidents from memory.

Treat VERIFIED past incidents as reliable precedent. Treat UNVERIFIED
past incidents as a hint worth considering, not a confirmed pattern —
say so explicitly if you rely on one.

Return a JSON object with "likely_cause", "suggested_next_step", and
"based_on_memory" (true/false, and if true, which specific memory).
"""
