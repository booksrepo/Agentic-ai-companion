# memory_store.py
import sqlite3
from datetime import datetime, timedelta


def init_db(path="incident_memory.db"):
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS incident_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT NOT NULL,
            root_cause TEXT NOT NULL,
            resolution TEXT NOT NULL,
            verified_by_human INTEGER NOT NULL DEFAULT 0,
            provisional INTEGER NOT NULL DEFAULT 1,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def record_resolution(conn, incident_type, root_cause, resolution, created_by,
                       verified=False, provisional=True):
    """`verified` defaults to False and `provisional` defaults to True: an
    agent that concludes an incident is resolved does not get to write a
    trusted memory on its own authority. Records start provisional
    regardless of who entered them, and only get promoted to fully trusted
    status through a deliberate, separate post-incident review."""
    conn.execute(
        """INSERT INTO incident_memory
           (incident_type, root_cause, resolution, verified_by_human, created_by, created_at, provisional)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (incident_type, root_cause, resolution, int(verified), created_by,
         datetime.utcnow().isoformat(), int(provisional))
    )
    conn.commit()


def promote_from_provisional(conn, record_id, confirmed_by):
    """Call this only after a genuine post-incident review, not during the
    incident itself — the cooling-off mechanism that separates 'someone
    typed this' from 'someone confirmed this after the dust settled.'"""
    conn.execute(
        "UPDATE incident_memory SET provisional = 0 WHERE id = ?",
        (record_id,)
    )
    conn.commit()


def get_relevant_memories(conn, incident_type, max_age_days=180):
    cutoff = (datetime.utcnow() - timedelta(days=max_age_days)).isoformat()
    cursor = conn.execute(
        """SELECT id, root_cause, resolution, verified_by_human, created_at
           FROM incident_memory
           WHERE incident_type = ? AND created_at > ?
           ORDER BY verified_by_human DESC, created_at DESC
           LIMIT 5""",
        (incident_type, cutoff)
    )
    return [
        {"id": r[0], "root_cause": r[1], "resolution": r[2], "verified": bool(r[3]), "date": r[4]}
        for r in cursor.fetchall()
    ]


def retract_memory(conn, record_id, retracted_by, reason):
    """A memory needs a fast retraction path. Log the retraction itself —
    the audit trail matters as much as the memory did."""
    conn.execute("DELETE FROM incident_memory WHERE id = ?", (record_id,))
    print(f"Memory record {record_id} retracted by {retracted_by}: {reason}")
