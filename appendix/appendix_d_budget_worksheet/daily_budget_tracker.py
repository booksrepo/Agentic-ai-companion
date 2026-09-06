# daily_budget_tracker.py — Appendix D
#
# Extends chapters/ch10_observability_and_budget/pipeline_with_guardrails.BudgetTracker
# with a daily (not just per-run) ceiling.

from pipeline_with_guardrails import BudgetExceededError, BudgetTracker


class DailyBudgetTracker(BudgetTracker):
    def __init__(self, max_tokens_per_run, max_daily_cost_usd, cost_per_1k_tokens):
        super().__init__(max_tokens_per_run)
        self.max_daily_cost_usd = max_daily_cost_usd
        self.cost_per_1k_tokens = cost_per_1k_tokens
        self.daily_spend = 0.0

    def record_run_cost(self, total_tokens):
        cost = (total_tokens / 1000) * self.cost_per_1k_tokens
        self.daily_spend += cost
        if self.daily_spend > self.max_daily_cost_usd:
            raise BudgetExceededError(
                f"Daily budget exceeded: ${self.daily_spend:.2f} > ${self.max_daily_cost_usd:.2f}"
            )
