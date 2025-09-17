"""
Interface for PullRequestMetadata repository.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from ..pull_request_basic_info import PullRequestBasicInfo
from ..pull_request_metadata import PullRequestMetadata


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