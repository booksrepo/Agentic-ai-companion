# dashboard.py
import sqlite3


def print_daily_summary(conn):
    cursor = conn.execute("""
        SELECT agent_role,
               COUNT(*) as run_count,
               AVG(tokens_input + tokens_output) as avg_tokens,
               AVG(confidence) as avg_confidence,
               SUM(CASE WHEN error IS NOT NULL THEN 1 ELSE 0 END) as error_count
        FROM agent_spans
        WHERE date(created_at) = date('now')
        GROUP BY agent_role
    """)
    print(f"{'Agent':<15} {'Runs':<6} {'Avg Tokens':<12} {'Avg Conf':<10} {'Errors':<6}")
    for row in cursor.fetchall():
        agent, runs, avg_tok, avg_conf, errors = row
        conf_display = f"{avg_conf:.2f}" if avg_conf is not None else "n/a"
        print(f"{agent:<15} {runs:<6} {avg_tok:<12.0f} {conf_display:<10} {errors:<6}")
