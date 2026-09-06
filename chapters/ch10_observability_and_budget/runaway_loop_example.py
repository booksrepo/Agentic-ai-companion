# runaway_loop_example.py
#
# "Break It": looks reasonable — if we're not confident, look again — but
# nothing here bounds how many times "again" can happen. Each iteration
# costs real money and real time, and none of it is visible from the
# pipeline's final output if it eventually terminates.

import json

from pipeline import COMMUNICATOR_PROMPT, DIAGNOSTICIAN_PROMPT, INVESTIGATOR_PROMPT, run_agent


def run_incident_pipeline_unbounded(raw_logs_and_metrics):
    investigation = run_agent("investigator", INVESTIGATOR_PROMPT, raw_logs_and_metrics)
    diagnosis = run_agent("diagnostician", DIAGNOSTICIAN_PROMPT, json.dumps(investigation))

    while diagnosis["confidence"] < 0.6:
        investigation = run_agent("investigator", INVESTIGATOR_PROMPT, raw_logs_and_metrics)
        diagnosis = run_agent("diagnostician", DIAGNOSTICIAN_PROMPT, json.dumps(investigation))

    communication = run_agent("communicator", COMMUNICATOR_PROMPT, json.dumps(diagnosis))
    return {"investigation": investigation, "diagnosis": diagnosis, "communication": communication}
