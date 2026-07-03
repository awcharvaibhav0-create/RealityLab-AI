class TokenCounter:
    def count_tokens(self, text: str) -> int:
        """Basic approximation for token counting."""
        return int(len(text.split()) * 1.3)
