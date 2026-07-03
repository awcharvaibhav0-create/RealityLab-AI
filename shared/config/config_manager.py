"""
Configuration manager module.
"""

from typing import Optional
from shared.config.loader import ConfigurationLoader
from shared.config.models import ApplicationConfiguration


class ConfigurationManager:
    """Centralized configuration manager."""

    _instance: Optional["ConfigurationManager"] = None
    _config: Optional[ApplicationConfiguration] = None

    def __init__(self):
        """Initialize the ConfigurationManager. Use get_instance() for singleton."""
        self.loader = ConfigurationLoader()

    @classmethod
    def get_instance(cls) -> "ConfigurationManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self) -> None:
        """Loads default configuration and environment profile."""
        self._config = self.loader.load()

    def get(self) -> ApplicationConfiguration:
        """Get the current active configuration."""
        if self._config is None:
            self.initialize()
        return self._config

    def reload(self) -> None:
        """Reload active configuration without restarting the application where safe."""
        self._config = self.loader.load()
