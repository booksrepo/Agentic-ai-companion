# test_triage_agent.py
from triage_agent import triage_failure


def test_triage_zero_division():
    with open("fixtures/zero_division_log.txt") as f:
        log = f.read()
    result = triage_failure(log)
    assert result["category"] == "test_logic"
    assert result["confidence"] > 0.7
    assert "ZeroDivisionError" in result["evidence"]
