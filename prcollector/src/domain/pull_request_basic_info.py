"""
Pull request basic info value object.
"""

from dataclasses import dataclass
from datetime import datetime

from .repository_identifier import RepositoryIdentifier


@dataclass(frozen=True)
class PullRequestBasicInfo:
    """Represents basic PR information."""

    number: int
    title: str
    closed_at: datetime
    is_merged: bool
    repository_id: RepositoryIdentifier