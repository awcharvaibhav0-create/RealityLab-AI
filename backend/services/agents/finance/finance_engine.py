from .calculator import FinanceCalculator
from .models import FinanceResult
from shared.knowledge.local_knowledge_base import LocalKnowledgeBase


class FinanceEngine:
    """Engine that orchestrates deterministic financial calculations."""

    def __init__(self, lkb: LocalKnowledgeBase = None):
        self.calculator = FinanceCalculator()
        self.lkb = lkb or LocalKnowledgeBase()

    def run_analysis(self, scenario: dict) -> FinanceResult:
        business_type = scenario.get("business_type", "base_retail_business")

        # Load rules and defaults from Knowledge Base
        active_rules = self.lkb.get_active_rules(business_type).active_rules
        finance_rules = active_rules.get("finance", {})

        # Extract inputs with defaults from rules or 0.0
        initial_investment = scenario.get(
            "initial_investment", finance_rules.get("initial_investment", 0.0)
        )
        price_per_unit = scenario.get(
            "price_per_unit", finance_rules.get("price_per_unit", 0.0)
        )
        units_sold = scenario.get("units_sold", finance_rules.get("units_sold", 0.0))

        fixed_costs = scenario.get("fixed_costs", finance_rules.get("fixed_costs", {}))
        if isinstance(fixed_costs, (int, float)):
            fixed_costs = {"default_fixed": float(fixed_costs)}

        variable_cost_per_unit = scenario.get(
            "variable_cost_per_unit", finance_rules.get("variable_cost_per_unit", 0.0)
        )
        additional_revenue = scenario.get("additional_revenue", {})
        additional_costs = scenario.get("additional_costs", 0.0)

        scenario_name = scenario.get("name", "Unknown Scenario")

        # Calculate components
        total_investment = self.calculator.investment.calculate(
            initial_investment, additional_costs
        )

        base_revenue = self.calculator.revenue.calculate(
            price_per_unit=price_per_unit,
            units_sold=units_sold,
            additional_revenue=additional_revenue,
        ).total_revenue

        base_expenses = self.calculator.expenses.calculate(
            fixed_costs=fixed_costs,
            variable_cost_per_unit=variable_cost_per_unit,
            units_sold=units_sold,
        ).total_expenses

        growth_rate = finance_rules.get("average_growth_rate", 0.0)

        projected_revenue = {}
        projected_profit = {}

        for month in [1, 3, 6, 12]:
            rev = base_revenue * ((1 + growth_rate) ** month)
            exp = base_expenses * (
                (1 + (growth_rate * 0.5)) ** month
            )  # Expenses grow slower
            projected_revenue[f"month{month}"] = round(rev, 2)
            projected_profit[f"month{month}"] = round(rev - exp, 2)

        profit = projected_profit.get("month1", 0)

        roi_months_val = (total_investment / profit) if profit > 0 else 0
        roi_str = (
            f"{round(roi_months_val)} months" if roi_months_val > 0 else "Not reached"
        )

        break_even_val = (total_investment / profit) if profit > 0 else 0
        break_even_str = (
            f"{round(break_even_val)} months" if break_even_val > 0 else "Not reached"
        )

        cash_flow_str = "Positive" if profit > 0 else "Negative"

        # Determine confidence
        confidence = "Medium"
        if scenario.get("historical_data"):
            confidence = "High"

        return FinanceResult(
            scenario=scenario_name,
            projected_revenue=projected_revenue,
            projected_profit=projected_profit,
            roi=roi_str,
            break_even=break_even_str,
            cash_flow=cash_flow_str,
            confidence=confidence,
        )
