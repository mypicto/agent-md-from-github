"""
Pull request metadata value object.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

from .review_comment import ReviewComment


@dataclass(frozen=True)
class PullRequestMetadata:
    """Represents PR metadata."""
    
    number: int
    title: str
    closed_at: datetime
    is_merged: bool
    review_comments: List[ReviewComment]