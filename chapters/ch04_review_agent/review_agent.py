# review_agent.py
#
# A Level 0 (suggest-only) code review agent. It reads the currently staged
# git diff, asks an LLM to flag issues against a rubric, validates the
# response deterministically, and prints suggestions to the terminal.
# It never posts anywhere and never takes any action on your behalf.

import json
import subprocess

import anthropic

client = anthropic.Anthropic()

REVIEW_RUBRIC = """
You are reviewing a code diff. For each issue you find, return a JSON array
of objects with exactly these fields:
- "file": the filename
- "line_hint": a short quoted snippet from the diff near the issue (not a line number)
- "severity": one of "nit", "suggestion", "concern"
- "comment": a one or two sentence explanation

Only comment on things actually present in the diff. If you find nothing
worth flagging, return an empty array. Return ONLY the JSON array, nothing else.
"""


def get_staged_diff():
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True, text=True, check=True
    )
    return result.stdout


def get_review_suggestions(diff_text):
    if not diff_text.strip():
        return []

    response = client.messages.create(
        model="your-provider-model-name",
        max_tokens=1000,
        system=REVIEW_RUBRIC,
        messages=[{"role": "user", "content": diff_text}]
    )
    raw_text = response.content[0].text
    try:
        suggestions = json.loads(raw_text)
    except json.JSONDecodeError:
        print("WARNING: agent returned unparseable output — treating as zero suggestions, not success.")
        return []
    return validate_suggestions(suggestions, diff_text)


def validate_suggestions(suggestions, diff_text):
    """Deterministic check wrapped around probabilistic output. If line_hint
    isn't a real substring of the diff, the agent hallucinated it — catch
    that mechanically instead of relying on a human to notice."""
    valid = []
    for s in suggestions:
        required_fields = {"file", "line_hint", "severity", "comment"}
        if not required_fields.issubset(s.keys()):
            print(f"WARNING: dropped malformed suggestion: {s}")
            continue
        if s["line_hint"] not in diff_text:
            print(f"WARNING: dropped suggestion referencing text not found in diff: {s['line_hint']!r}")
            continue
        if s["severity"] not in {"nit", "suggestion", "concern"}:
            print(f"WARNING: dropped suggestion with invalid severity: {s['severity']}")
            continue
        valid.append(s)
    return valid


def display_suggestions(suggestions):
    if not suggestions:
        print("No suggestions. (This does not mean the diff is bug-free —")
        print("it means the agent found nothing worth flagging.)")
        return

    for s in suggestions:
        print(f"\n[{s['severity'].upper()}] {s['file']}")
        print(f"  near: \"{s['line_hint']}\"")
        print(f"  {s['comment']}")


if __name__ == "__main__":
    diff = get_staged_diff()
    suggestions = get_review_suggestions(diff)
    display_suggestions(suggestions)
