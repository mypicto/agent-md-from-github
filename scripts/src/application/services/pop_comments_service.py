"""
Application service for popping comments from missing summaries.
"""

from pathlib import Path

from ...domain.repository_identifier import RepositoryIdentifier
from .missing_summaries_service import MissingSummariesService
from .comments_service import CommentsService


class PopCommentsService:
    """Application service for getting comments from the next missing summary PR."""
    
    def __init__(
        self,
        missing_summaries_service: MissingSummariesService,
        comments_service: CommentsService
    ):
        """Initialize pop comments service.
        
        Args:
            missing_summaries_service: Service for listing missing summaries
            comments_service: Service for getting comments markdown
        """
        self._missing_summaries_service = missing_summaries_service
        self._comments_service = comments_service
    
    def get_next_missing_comments_markdown(
        self,
        repository_id: RepositoryIdentifier,
        output_directory: Path
    ) -> str:
        """Get comments markdown for the next missing summary PR.
        
        Args:
            repository_id: Repository identifier
            output_directory: Output directory
            
        Returns:
            Markdown formatted comments for the first missing summary PR,
            or "No missing summaries found." if none exist
        """
        missing_numbers = self._missing_summaries_service.list_missing_summaries(
            repository_id, output_directory
        )
        
        if not missing_numbers:
            return "No missing summaries found."
        
        pr_number = missing_numbers[0]
        return self._comments_service.get_comments_markdown(
            repository_id, pr_number, output_directory
        )