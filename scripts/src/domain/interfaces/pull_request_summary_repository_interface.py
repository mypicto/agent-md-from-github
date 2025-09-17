"""
Interface for PullRequestSummary repository.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from ..pull_request_metadata import PullRequestMetadata


class PullRequestSummaryRepositoryInterface(ABC):
    """Interface for checking PullRequestSummary existence."""

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