"""
Review comment value object.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ReviewComment:
    """Represents a single review comment."""
    
    comment_id: int
    file_path: str
    position: Optional[int]
    commit_id: str
    author: str
    created_at: datetime
    body: str
    diff_context: str