"""
AI comment filter implementation.
"""

from typing import List

from ...domain.interfaces.comment_filter_interface import CommentFilterInterface
from ...domain.review_comment import ReviewComment


class AICommentFilter(CommentFilterInterface):
    """Filter to remove comments authored by AI systems."""
    
    # List of AI author names to filter out
    AI_AUTHORS = {"Copilot"}
    
    def filter_comments(self, comments: List[ReviewComment]) -> List[ReviewComment]:
        """Filter out comments authored by AI systems.
        
        Args:
            comments: List of review comments to filter
            
        Returns:
            Filtered list of review comments excluding AI-generated comments
        """
        return [comment for comment in comments if comment.author not in self.AI_AUTHORS]