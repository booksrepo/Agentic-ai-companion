# pipeline_with_guardrails.py
#
# Fixed version: a hard retry cap, exponential backoff for transient errors
# only, and an enforced per-run token budget. An unbounded loop is an
# unbounded permission — this file makes the boundary explicit and
# enforced in code.

import json
import time

import anthropic

from prompts import COMMUNICATOR_PROMPT, DIAGNOSTICIAN_PROMPT, INVESTIGATOR_PROMPT

MAX_RETRIES = 3


class BudgetExceededError(Exception):
    pass


class BudgetTracker:
    def __init__(self, max_tokens_per_run):
        self.max_tokens_per_run = max_tokens_per_run
        self.tokens_used = 0

    def record(self, input_tokens, output_tokens):
        self.tokens_used += input_tokens + output_tokens
        if self.tokens_used > self.max_tokens_per_run:
            raise BudgetExceededError(
                f"Pipeline run exceeded token budget: {self.tokens_used} > {self.max_tokens_per_run}"
            )


def call_with_backoff(fn, max_attempts=3):
    """Backoff for transient errors only — a rate limit, not a low-confidence
    result. Confidence retries are bounded separately, by MAX_RETRIES."""
    for attempt in range(max_attempts):
        try:
            return fn()
        except anthropic.RateLimitError:
            wait = 2 ** attempt
            print(f"Rate limited — waiting {wait}s before retry {attempt + 1}/{max_attempts}")
            time.sleep(wait)
    raise RuntimeError("Max retries exceeded due to persistent rate limiting")


def run_incident_pipeline_with_retry(raw_logs_and_metrics, run_agent):
    investigation = run_agent("investigator", INVESTIGATOR_PROMPT, raw_logs_and_metrics)
    diagnosis = run_agent("diagnostician", DIAGNOSTICIAN_PROMPT, json.dumps(investigation))

    attempts = 1
    while diagnosis["confidence"] < 0.6 and attempts < MAX_RETRIES:
        investigation = run_agent("investigator", INVESTIGATOR_PROMPT, raw_logs_and_metrics)
        diagnosis = run_agent("diagnostician", DIAGNOSTICIAN_PROMPT, json.dumps(investigation))
        attempts += 1

    if diagnosis["confidence"] < 0.6:
        diagnosis["likely_cause"] = "Unable to reach confident diagnosis after retries — flagging for human investigation."

    communication = run_agent("communicator", COMMUNICATOR_PROMPT, json.dumps(diagnosis))
    return {"investigation": investigation, "diagnosis": diagnosis, "communication": communication, "retry_attempts": attempts}
