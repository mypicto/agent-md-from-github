"""
Comment thread value object.
"""

from dataclasses import dataclass
from typing import List, Optional
from .review_comment import ReviewComment


@dataclass(frozen=True)
class CommentThread:
    """Represents a thread of review comments grouped by file_path and position."""
    
    file_path: str
    position: Optional[int]
    comments: List[ReviewComment]