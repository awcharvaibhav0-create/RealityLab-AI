"""
Configuration loader.
"""

import os
from shared.utils.json import load_json
from shared.config.models import (
    ApplicationConfiguration,
    DatabaseConfig,
    ReportsConfig,
    LoggingConfig,
    FeatureFlags,
)
from shared.config.secret_manager import SecretManager
from shared.config.validator import ConfigurationValidator


class ConfigurationLoader:
    """Loads configuration from JSON files and environment variables."""

    def __init__(self, config_dir: str = "config/configs"):
        self.config_dir = config_dir
        self.validator = ConfigurationValidator()

    def load(self) -> ApplicationConfiguration:
        """Loads and merges configuration based on the environment."""
        # 1. Determine environment
        env = os.environ.get("REALITYLAB_ENV", "development")

        # 2. Load defaults
        default_path = os.path.join(self.config_dir, "defaults.json")
        defaults = load_json(default_path) if os.path.exists(default_path) else {}

        # 3. Load environment specific
        env_path = os.path.join(self.config_dir, f"{env}.json")
        env_config = load_json(env_path) if os.path.exists(env_path) else {}

        # Merge dictionaries (simple shallow merge for MVP)
        merged_config = {**defaults, **env_config}
        merged_config["environment"] = env

        # 4. Load secrets
        secrets = SecretManager.load_secrets()
        merged_config["secrets"] = secrets

        # 5. Load Overrides from Environment Variables
        if "DATABASE_PATH" in os.environ:
            if "database" not in merged_config:
                merged_config["database"] = {}
            merged_config["database"]["path"] = os.environ["DATABASE_PATH"]

        if "LOG_LEVEL" in os.environ:
            if "logging" not in merged_config:
                merged_config["logging"] = {}
            merged_config["logging"]["level"] = os.environ["LOG_LEVEL"]

        # Validate
        self.validator.validate(merged_config)

        # Map to Dataclass
        return self._build_model(merged_config)

    def _build_model(self, config: dict) -> ApplicationConfiguration:
        """Converts raw dict to ApplicationConfiguration."""
        return ApplicationConfiguration(
            environment=config.get("environment", "development"),
            database=DatabaseConfig(
                **config.get("database", {"path": "database/main.db"})
            ),
            reports=ReportsConfig(
                **config.get("reports", {"directory": "reports/output"})
            ),
            logging=LoggingConfig(**config.get("logging", {"level": "INFO"})),
            feature_flags=FeatureFlags(**config.get("feature_flags", {})),
            secrets=config.get("secrets", {}),
        )
