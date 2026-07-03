"""
Secret management module for configuration.
"""

import os
from typing import Dict, Any


class SecretManager:
    """Manages sensitive configuration values from environment variables."""

    @staticmethod
    def load_secrets() -> Dict[str, str]:
        """Load secrets from environment variables."""
        secrets = {}
        # Load API keys
        if "GEMINI_API_KEY" in os.environ:
            secrets["GEMINI_API_KEY"] = os.environ["GEMINI_API_KEY"]

        return secrets

    @staticmethod
    def mask_secrets(config: Dict[str, Any]) -> Dict[str, Any]:
        """Return a copy of the config dictionary with secrets masked for logging."""
        # Config currently holds secrets under 'secrets' dictionary.
        # But we ensure they are not exposed.
        safe_config = config.copy()
        if "secrets" in safe_config:
            safe_config["secrets"] = {k: "********" for k in safe_config["secrets"]}
        return safe_config
