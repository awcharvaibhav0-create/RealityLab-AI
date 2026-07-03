"""
Data models for the configuration subsystem.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class DatabaseConfig:
    path: str


@dataclass
class ReportsConfig:
    directory: str


@dataclass
class LoggingConfig:
    level: str


@dataclass
class FeatureFlags:
    ENABLE_DEVELOPER_MODE: bool = False
    ENABLE_REPORT_EXPORT: bool = True
    ENABLE_GEMINI: bool = True
    ENABLE_CACHE: bool = True


@dataclass
class ApplicationConfiguration:
    """Main configuration model for the application."""

    environment: str
    database: DatabaseConfig
    reports: ReportsConfig
    logging: LoggingConfig
    feature_flags: FeatureFlags = field(default_factory=FeatureFlags)
    secrets: Dict[str, str] = field(default_factory=dict)
