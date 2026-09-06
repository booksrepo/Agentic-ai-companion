# approval_gate.py
#
# A structural gate, not a social convention: the pipeline's actual "send"
# function cannot run without first calling get_approved_content, which
# raises unless a human has explicitly recorded approval. The same
# distinction Chapter 8 drew between a tool's interface and the credential
# enforcing it underneath.

import json
import sqlite3
from datetime import datetime


def init_approval_db(path="approvals.db"):
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pending_approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT NOT NULL,
            proposed_content TEXT NOT NULL,
            supporting_evidence TEXT NOT NULL,
            prompt_version TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            decided_by TEXT,
            decision_reason TEXT,
            requested_at TEXT NOT NULL,
            decided_at TEXT
        )
    """)
    conn.commit()
    return conn


def request_approval(conn, action_type, proposed_content, supporting_evidence, prompt_version):
    """supporting_evidence and prompt_version are both mandatory, captured
    at the moment the approval is requested — an immutable snapshot, never
    a live reference to something that can keep changing underneath the
    approval. supporting_evidence should be the FULL diagnosis object,
    captured right now, not a foreign key to a row that might be updated
    later (see break_it_example.py for why that distinction matters)."""
    conn.execute(
        """INSERT INTO pending_approvals
           (action_type, proposed_content, supporting_evidence, prompt_version, requested_at)
           VALUES (?, ?, ?, ?, ?)""",
        (action_type, proposed_content, json.dumps(supporting_evidence), prompt_version, datetime.utcnow().isoformat())
    )
    conn.commit()
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def decide_approval(conn, approval_id, approved, decided_by, reason):
    status = "approved" if approved else "rejected"
    conn.execute(
        """UPDATE pending_approvals
           SET status = ?, decided_by = ?, decision_reason = ?, decided_at = ?
           WHERE id = ? AND status = 'pending'""",
        (status, decided_by, reason, datetime.utcnow().isoformat(), approval_id)
    )
    conn.commit()


def get_approved_content(conn, approval_id):
    row = conn.execute(
        "SELECT proposed_content, status FROM pending_approvals WHERE id = ?", (approval_id,)
    ).fetchone()
    if row is None or row[1] != "approved":
        raise PermissionError(f"Approval {approval_id} is not in an approved state — cannot proceed.")
    return row[0]
