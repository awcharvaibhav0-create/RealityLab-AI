class Validator:
    @staticmethod
    def validate_positive(value: float, name: str) -> None:
        if value < 0:
            raise ValueError(f"{name} cannot be negative.")

    @staticmethod
    def validate_scenario(task: dict) -> bool:
        required_keys = [
            "price_per_unit",
            "units_sold",
            "fixed_costs",
            "variable_cost_per_unit",
            "initial_investment",
        ]
        for key in required_keys:
            if key not in task:
                raise ValueError(f"Missing required field in task: {key}")
            if not isinstance(task[key], (int, float)):
                raise TypeError(f"Field {key} must be a number")
        return True
