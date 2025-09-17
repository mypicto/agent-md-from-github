"""
PullRequestSummary repository implementation for checking summary file existence.
"""

from pathlib import Path

from ...domain.interfaces.pull_request_summary_repository_interface import PullRequestSummaryRepositoryInterface
from ...domain.pull_request_metadata import PullRequestMetadata


class PullRequestSummaryRepository(PullRequestSummaryRepositoryInterface):
    """Repository for checking PullRequestSummary file existence."""

    def exists_summary(self, metadata: PullRequestMetadata, output_directory: Path) -> bool:
        """Check if summary file exists for the given PR metadata.

        Args:
            metadata: The PR metadata
            output_directory: Base output directory

        Returns:
            True if summary file exists
        """
        date_str = metadata.closed_at.strftime("%Y-%m-%d")
        summary_path = output_directory / metadata.repository_id.owner / metadata.repository_id.name / date_str / f"PR-{metadata.number}-summary.md"
        return summary_path.exists()