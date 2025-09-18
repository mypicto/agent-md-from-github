"""
Interface for managing PR summaries.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from ..pull_request_metadata import PullRequestMetadata
from ..review_summary import ReviewSummary
from ..repository_identifier import RepositoryIdentifier


class SummaryRepositoryInterface(ABC):
    """Interface for managing PR summaries."""

    @abstractmethod
    def exists_summary(self, metadata: PullRequestMetadata, output_directory: Path) -> bool:
        """Check if summary file exists for the given PR metadata.

        Args:
            metadata: The PR metadata
            output_directory: Base output directory

        Returns:
            True if summary file exists
        """
        pass

    @abstractmethod
    def save(self, summary: ReviewSummary) -> None:
        """Save a review summary.
        
        Args:
            summary: The review summary to save
        """
        pass
    
    @abstractmethod
    def get(self, repository_id: RepositoryIdentifier, pr_number: int) -> Optional[ReviewSummary]:
        """Get a review summary by repository and PR number.
        
        Args:
            repository_id: Repository identifier
            pr_number: PR number
            
        Returns:
            ReviewSummary if found, None otherwise
        """
        pass