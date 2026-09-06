# review_rubric.py — Chapter 4
# A general-purpose code-review rubric. Asks for a verifiable "line_hint"
# snippet rather than a "line_number" the model would have to count
# correctly — adapt the categories, keep the verifiable-reference pattern.

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
