# triage_agent.py
import json

import anthropic

client = anthropic.Anthropic()

TRIAGE_RUBRIC = """
You are triaging a CI pipeline failure. You will be given raw test output.

Return ONLY a JSON object with exactly these fields:
- "category": one of "dependency", "test_logic", "environment", "flaky", "infrastructure", "unknown"
- "evidence": a short quoted snippet from the log that directly supports your diagnosis
- "diagnosis": one or two sentences explaining what you believe went wrong
- "confidence": a number from 0.0 to 1.0, reflecting your actual certainty —
  use "unknown" as the category and a low confidence score if the log
  does not clearly point to a cause
- "suggested_fix": a short, specific suggestion, or null if you're not
  confident enough to suggest one

Do not guess a specific fix if your confidence is below 0.6. Return null
for suggested_fix instead. Being honestly uncertain is more valuable than
a confident wrong answer.
"""


def triage_failure(log_text, recent_pass_rate=None):
    context = log_text
    if recent_pass_rate is not None:
        context += f"\n\n[Additional context: this test has passed {recent_pass_rate:.0%} of its last 20 runs.]"
    response = client.messages.create(
        model="your-provider-model-name",
        max_tokens=500,
        system=TRIAGE_RUBRIC,
        messages=[{"role": "user", "content": context}]
    )
    return json.loads(response.content[0].text)


def validate_triage(result):
    """A model's self-reported confidence is itself a probabilistic claim.
    Enforce the threshold in code — don't trust the prompt to be obeyed."""
    if result["confidence"] < 0.6 and result["suggested_fix"] is not None:
        print("WARNING: agent suggested a fix despite low confidence — discarding fix.")
        result["suggested_fix"] = None
        result["category"] = "unknown"
    return result


def triage_with_consistency_check(log_text):
    """Run the same triage twice. If the category flips between runs, treat
    it as ambiguous rather than trusting whichever answer came out first."""
    first = triage_failure(log_text)
    second = triage_failure(log_text)
    if first["category"] != second["category"]:
        return {
            "category": "unknown",
            "diagnosis": "Diagnosis was inconsistent across repeated attempts — likely an ambiguous failure requiring human investigation.",
            "confidence": 0.0,
            "suggested_fix": None,
            "evidence": f"First attempt: {first['category']} ({first['confidence']}). Second attempt: {second['category']} ({second['confidence']})."
        }
    return first


def triage_failure_with_cost(log_text):
    """Same as triage_failure, but logs token usage — the habit this book
    insists on building in from day one, rather than discovering cost only
    when a bill arrives."""
    response = client.messages.create(
        model="your-provider-model-name",
        max_tokens=500,
        system=TRIAGE_RUBRIC,
        messages=[{"role": "user", "content": log_text}]
    )
    usage = response.usage
    print(f"Input tokens: {usage.input_tokens}, Output tokens: {usage.output_tokens}")
    return json.loads(response.content[0].text)


if __name__ == "__main__":
    with open("failure_log.txt") as f:
        log_text = f.read()
    result = triage_failure(log_text)
    print(json.dumps(result, indent=2))
