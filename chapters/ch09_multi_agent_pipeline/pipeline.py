# pipeline.py
import json

import anthropic

from prompts import COMMUNICATOR_PROMPT, DIAGNOSTICIAN_PROMPT, INVESTIGATOR_PROMPT

client = anthropic.Anthropic()


def run_agent(system_prompt, user_content):
    response = client.messages.create(
        model="your-provider-model-name",
        max_tokens=800,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}]
    )
    return json.loads(response.content[0].text)


def verify_diagnosis_grounded(diagnosis, investigation):
    """A deterministic verification step between stages, not just a better
    prompt. Before the Diagnostician's output is trusted, verify its
    supporting_observations actually trace back to something the
    Investigator genuinely reported — the same evidence-checking discipline
    as Chapter 4's line-hint validation, now applied across an agent-to-agent
    boundary instead of an agent-to-raw-data one."""
    raw_text = json.dumps(investigation)
    for claim in diagnosis.get("supporting_observations", []):
        if claim not in raw_text:
            diagnosis["confidence"] = 0.0
            diagnosis["likely_cause"] = "UNVERIFIED — diagnosis referenced an observation not actually present in the investigation output."
            return diagnosis
    return diagnosis


def run_incident_pipeline(raw_logs_and_metrics):
    investigation = run_agent(INVESTIGATOR_PROMPT, raw_logs_and_metrics)

    diagnosis = run_agent(DIAGNOSTICIAN_PROMPT, json.dumps(investigation))
    diagnosis = verify_diagnosis_grounded(diagnosis, investigation)

    communication = run_agent(COMMUNICATOR_PROMPT, json.dumps(diagnosis))

    return {
        "investigation": investigation,
        "diagnosis": diagnosis,
        "communication": communication
    }
