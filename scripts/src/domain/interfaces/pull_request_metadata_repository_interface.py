"""
Interface for PullRequestMetadata repository.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from ..pull_request_basic_info import PullRequestBasicInfo
from ..pull_request_metadata import PullRequestMetadata
from ..repository_identifier import RepositoryIdentifier


class PullRequestMetadataRepositoryInterface(ABC):
    """Interface for persisting PullRequestMetadata."""

    @abstractmethod
    def save(self, pr_metadata: PullRequestMetadata, output_directory: Path) -> None:
        """Save PullRequestMetadata to JSON file.

        Args:
            pr_metadata: The PR metadata to save
            output_directory: Base output directory
        """
        pass

    @abstractmethod
    def exists(self, basic_info: PullRequestBasicInfo, output_directory: Path) -> bool:
        """Check if PR metadata file already exists.

        Args:
            basic_info: Basic PR info
            output_directory: Base output directory

        Returns:
            True if file exists
        """
        pass

    @abstractmethod
    def find_all_by_repository(self, output_directory: Path, repository_id: RepositoryIdentifier) -> List[PullRequestMetadata]:
        """Find all PullRequestMetadata for the given repository.

        Args:
            output_directory: Base output directory
            repository_id: Repository identifier

        Returns:
            List of PullRequestMetadata
        """
        pass

    @abstractmethod
    def find_by_pr_number(self, output_directory: Path, repository_id: RepositoryIdentifier, pr_number: int) -> Optional[PullRequestMetadata]:
        """Find a specific PullRequestMetadata by PR number.

        Args:
            output_directory: Base output directory
            repository_id: Repository identifier
            pr_number: Pull request number

        Returns:
            PullRequestMetadata if found, None otherwise
        """
        pass