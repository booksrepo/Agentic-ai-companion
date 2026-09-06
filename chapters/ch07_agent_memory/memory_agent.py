# memory_agent.py
import json

import anthropic

from memory_store import get_relevant_memories

client = anthropic.Anthropic()

INCIDENT_RUBRIC = """
You are helping triage a live incident. You will be given the current
symptoms and, if available, relevant past incidents from memory.

Treat VERIFIED past incidents as reliable precedent. Treat UNVERIFIED
past incidents as a hint worth considering, not a confirmed pattern —
say so explicitly if you rely on one.

Return a JSON object with "likely_cause", "suggested_next_step", and
"based_on_memory" (true/false, and if true, which specific memory).
"""


def triage_with_memory(conn, incident_type, current_symptoms):
    memories = get_relevant_memories(conn, incident_type)
    memory_context = "\n".join(
        f"- [{'VERIFIED' if m['verified'] else 'UNVERIFIED'}] {m['root_cause']} -> {m['resolution']} ({m['date']})"
        for m in memories
    ) or "No relevant past incidents found."

    prompt = f"Current symptoms: {current_symptoms}\n\nRelevant memory:\n{memory_context}"
    response = client.messages.create(
        model="your-provider-model-name",
        max_tokens=500,
        system=INCIDENT_RUBRIC,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.content[0].text)
