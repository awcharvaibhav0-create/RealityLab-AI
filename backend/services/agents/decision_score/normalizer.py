class Normalizer:
    """Base logic for value normalization."""

    @staticmethod
    def min_max_normalize(value: float, min_val: float, max_val: float) -> float:
        """Normalizes a value between 0 and 1 using min-max scaling."""
        if max_val == min_val:
            return 1.0 if value > 0 else 0.0
        return (value - min_val) / (max_val - min_val)
