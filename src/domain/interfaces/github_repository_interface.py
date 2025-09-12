"""
Interface for GitHub repository operations.
"""

from typing import Protocol

from ..date_range import DateRange
from ..pull_request_metadata import PullRequestMetadata
from ..repository_identifier import RepositoryIdentifier


class GitHubRepositoryInterface(Protocol):
    """Interface for GitHub repository operations."""
    
    def find_closed_pull_requests_in_range(
        self, 
        repo_id: RepositoryIdentifier, 
        date_range: DateRange
    ) -> list[PullRequestMetadata]:
        """Find closed PRs within the specified date range."""
        ...