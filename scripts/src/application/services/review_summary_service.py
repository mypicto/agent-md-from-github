"""
Application service for review summary management.
"""

import logging
from pathlib import Path

from ...domain.review_summary import ReviewSummary
from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.interfaces.review_summary_repository_interface import ReviewSummaryRepositoryInterface
from ...domain.interfaces.pull_request_metadata_repository_interface import PullRequestMetadataRepositoryInterface
from ..exceptions.pr_review_collection_error import PRReviewCollectionError


class ReviewSummaryService:
    """Application service for managing review summaries."""
    
    def __init__(
        self,
        review_summary_repository: ReviewSummaryRepositoryInterface,
        pr_metadata_repository: PullRequestMetadataRepositoryInterface
    ):
        """Initialize review summary service.
        
        Args:
            review_summary_repository: Repository for review summaries
            pr_metadata_repository: Repository for PR metadata validation
        """
        self._review_summary_repository = review_summary_repository
        self._pr_metadata_repository = pr_metadata_repository
        self._logger = logging.getLogger("review_summary")
    
    def set_summary(
        self,
        repository_id: RepositoryIdentifier,
        pr_number: int,
        priority: str,
        summary: str
    ) -> None:
        """Set a review summary for a PR.
        
        Args:
            repository_id: Repository identifier
            pr_number: PR number
            priority: Priority level ('high', 'middle', 'low')
            summary: Summary text
            
        Raises:
            PRReviewCollectionError: If PR does not exist or other errors occur
        """
        # Validate PR exists by checking local metadata
        pr_exists = self._pr_metadata_repository.find_by_pr_number(Path("pullrequests"), repository_id, pr_number)
        if not pr_exists:
            raise PRReviewCollectionError(f"PR #{pr_number} not found in local metadata for {repository_id.to_string()}")
        
        # Create and save summary
        review_summary = ReviewSummary(
            repository_id=repository_id,
            pr_number=pr_number,
            priority=priority,
            summary=summary
        )
        
        self._review_summary_repository.save(review_summary)
        self._logger.info(f"Saved summary for PR #{pr_number} in {repository_id.to_string()}")