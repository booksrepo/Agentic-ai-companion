# memory_poisoning_example.py
#
# "Break It": a bad record written as verified=True "in the rush," without
# real confirmation. Because it's marked verified, it sorts ahead of
# genuinely correct memories and gets treated as reliable precedent by
# triage_with_memory — recommending a database restart that does nothing
# for the real problem, and re-entrenching itself every time it's cited.

from memory_store import record_resolution

def poison_the_memory(conn):
    record_resolution(
        conn,
        incident_type="payments_service_5xx",
        root_cause="database needs a restart to clear memory leaks",
        resolution="restarted the primary database instance",
        created_by="oncall-engineer-jsmith",
        verified=True  # marked verified in the rush, without real confirmation
    )
