# break_it_example.py
#
# The flawed version — shown to demonstrate why it fails. It stores a
# REFERENCE to the diagnosis (diagnosis_id) instead of a snapshot, expecting
# the approver to look up the current diagnosis when they get around to
# reviewing it.
#
# If the underlying incident evolves while the approval sits in the queue
# (e.g. the Diagnostician re-runs on new logs), the diagnosis the approver
# sees at review time may not match the one that existed when the request
# was made. Weeks later, the approval record shows diagnosis_id: 4821,
# approved by a named person — but diagnosis 4821 no longer matches what
# the approver actually saw, because it's since been updated again.
# You can prove an approval happened. You cannot prove what information
# the approver was looking at when they made it. That gap is what makes an
# audit trail non-defensible, regardless of how complete it looks at a
# glance.

from datetime import datetime


def request_approval_flawed(conn, action_type, proposed_content, diagnosis_id):
    conn.execute(
        "INSERT INTO pending_approvals (action_type, proposed_content, diagnosis_id, requested_at) VALUES (?, ?, ?, ?)",
        (action_type, proposed_content, diagnosis_id, datetime.utcnow().isoformat())
    )
