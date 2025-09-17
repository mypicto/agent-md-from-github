"""
Comment filter interface.
"""

from abc import ABC, abstractmethod
from typing import List

from ..review_comment import ReviewComment


class CommentFilterInterface(ABC):
    """Interface for filtering review comments."""
    
    @abstractmethod
    def filter_comments(self, comments: List[ReviewComment]) -> List[ReviewComment]:
        """Filter the list of review comments.
        
        Args:
            comments: List of review comments to filter
            
        Returns:
            Filtered list of review comments
        """
        pass