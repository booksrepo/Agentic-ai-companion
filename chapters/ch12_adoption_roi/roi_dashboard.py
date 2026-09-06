# roi_dashboard.py
import sqlite3


def init_roi_db(path="roi_tracking.db"):
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS task_outcomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_type TEXT NOT NULL,
            used_agent INTEGER NOT NULL,  -- 1 if AI-assisted, 0 if fully manual (for comparison)
            cycle_time_minutes REAL NOT NULL,
            token_cost_usd REAL DEFAULT 0,
            reviewer_time_minutes REAL NOT NULL,
            defect_found_later INTEGER NOT NULL DEFAULT 0,  -- 1 if this task's output had a missed issue
            completed_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def print_roi_summary(conn, task_type):
    """Running this side by side — used_agent = 1 against used_agent = 0 —
    for the same task type gives the paired comparison an honest ROI claim
    requires: not just "the AI-assisted group was faster," but faster and
    at what defect rate, and at what real cost including reviewer time.
    A dashboard that only tracked cycle time would let a genuinely bad
    trade-off look like an unambiguous win."""
    cursor = conn.execute("""
        SELECT used_agent,
               COUNT(*) as n,
               AVG(cycle_time_minutes) as avg_cycle_time,
               AVG(token_cost_usd + reviewer_time_minutes * 0.75) as avg_cost_usd,
               AVG(defect_found_later) as defect_rate
        FROM task_outcomes
        WHERE task_type = ?
        GROUP BY used_agent
    """, (task_type,))

    print(f"\nROI summary for: {task_type}")
    print(f"{'Group':<15} {'N':<6} {'Avg Cycle (min)':<18} {'Avg Cost ($)':<15} {'Defect Rate':<12}")
    for row in cursor.fetchall():
        label = "AI-assisted" if row[0] == 1 else "Manual"
        print(f"{label:<15} {row[1]:<6} {row[2]:<18.1f} {row[3]:<15.2f} {row[4]:<12.1%}")
