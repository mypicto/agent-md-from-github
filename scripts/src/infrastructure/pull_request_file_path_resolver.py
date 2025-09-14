"""
Pull request file path resolver for handling file paths and naming conventions.
"""

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

from ..domain.repository_identifier import RepositoryIdentifier

@dataclass(frozen=True)
class PullRequestFilePathResolver:
    """Resolves file paths and naming conventions for pull request data."""

    _output_directory: Path
    _repository_id: RepositoryIdentifier
    _closed_at: datetime
    _pr_number: int

    def get_pr_directory(self) -> Path:
        """Get the directory path for a pull request."""
        date_folder = self._closed_at.strftime("%Y-%m-%d")
        return self._output_directory / self._repository_id.owner / self._repository_id.name / date_folder

    def get_comments_file_path(self) -> Path:
        """Get the file path for comments."""
        pr_directory = self.get_pr_directory()
        return pr_directory / f"PR-{self._pr_number}-comments.json"

    def get_diff_file_path(self) -> Path:
        """Get the file path for diff."""
        pr_directory = self.get_pr_directory()
        return pr_directory / f"PR-{self._pr_number}-diff.patch"

    def file_exists(self) -> bool:
        """Check if a file exists."""
        file_path = self.get_comments_file_path()
        return file_path.exists()