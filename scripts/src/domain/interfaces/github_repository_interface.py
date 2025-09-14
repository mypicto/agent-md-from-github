"""
Interface for GitHub repository operations.
"""

from typing import Protocol, Generator

from ..date_range import DateRange
from ..pull_request_metadata import PullRequestMetadata
from ..pull_request_basic_info import PullRequestBasicInfo
from ..repository_identifier import RepositoryIdentifier


class GitHubRepositoryInterface(Protocol):
    """Interface for GitHub repository operations."""
    
    def find_closed_prs_basic_info(
        self, 
        repo_id: RepositoryIdentifier, 
        date_range: DateRange
    ) -> Generator[PullRequestBasicInfo, None, None]:
        """Find closed PRs basic info within the specified date range.
        
        Returns basic PR information without review comments.
        """
        ...
    
    def get_full_pr_metadata(
        self, 
        pr_number: int, 
        repo_id: RepositoryIdentifier
    ) -> PullRequestMetadata:
        """Get full PR metadata including review comments for a specific PR."""
        ...