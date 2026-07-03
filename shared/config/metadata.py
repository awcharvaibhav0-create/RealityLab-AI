"""
Application Metadata
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ConfigurationMetadata:
    """Metadata for configuration."""

    version: str
    profile: str
    checksum: str
    created: datetime
    updated: datetime
    author: Optional[str] = None
