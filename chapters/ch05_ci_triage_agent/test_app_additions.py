# Add this test to ci-fundamentals-demo/test_app.py
from app import calculate_average


def test_calculate_average_empty_list():
    assert calculate_average([]) == 0


# --- A deliberately flawed, timing-sensitive test, used in this chapter's
# --- "Break It" section to show a triage agent mis-categorizing a flaky
# --- test as a genuine test_logic bug. Do not keep this test long-term.
import time


def test_calculate_average_timing_sensitive():
    start = time.time()
    result = calculate_average([1, 2, 3])
    elapsed = time.time() - start
    # A poorly-written test that assumes unrealistic timing guarantees
    assert elapsed < 0.0001
