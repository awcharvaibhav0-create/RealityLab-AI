"""
Configuration validation module.
"""

from typing import Dict, Any


class ConfigurationError(Exception):
    """Exception raised for configuration errors."""

    pass


class ConfigurationValidator:
    """Validates configuration dictionaries."""

    def validate(self, config: Dict[str, Any]) -> None:
        """Validates that required configuration is present."""
        if "environment" not in config:
            raise ConfigurationError("Missing required config: environment")

        if "database" not in config or "path" not in config["database"]:
            raise ConfigurationError("Missing required config: database.path")
