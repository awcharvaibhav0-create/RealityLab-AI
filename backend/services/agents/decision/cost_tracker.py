from .models import TokenUsage


class CostTracker:
    def __init__(
        self,
        cost_per_1k_prompt: float = 0.00025,
        cost_per_1k_completion: float = 0.0005,
    ):
        self.cost_per_1k_prompt = cost_per_1k_prompt
        self.cost_per_1k_completion = cost_per_1k_completion
        self.total_cost = 0.0

    def add_usage(self, usage: TokenUsage) -> float:
        prompt_cost = (usage.prompt_tokens / 1000) * self.cost_per_1k_prompt
        completion_cost = (usage.completion_tokens / 1000) * self.cost_per_1k_completion
        cost = prompt_cost + completion_cost
        self.total_cost += cost
        return cost
