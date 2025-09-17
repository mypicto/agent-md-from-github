"""
Interface for review summary repository.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ..review_summary import ReviewSummary
from ..repository_identifier import RepositoryIdentifier


class ReviewSummaryRepositoryInterface(ABC):
    """Interface for managing review summaries."""
    
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