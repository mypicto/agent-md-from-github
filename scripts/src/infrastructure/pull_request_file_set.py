"""
Pull request file path resolver for handling file paths and naming conventions.
"""

from dataclasses import dataclass
from pathlib import Path

from ..domain.pull_request_basic_info import PullRequestBasicInfo
from ..domain.pull_request_metadata import PullRequestMetadata

@dataclass(frozen=True)
class PullRequestFileSet:
    """Resolves file paths and naming conventions for pull request data."""

    _directory_path: Path
    _pr_number: int

    @classmethod
    def create_with_metadata(cls, output_directory: Path, pr_metadata: PullRequestMetadata):
        date_folder = pr_metadata.closed_at.strftime("%Y-%m-%d")
        directory_path = output_directory / pr_metadata.repository_id.owner / pr_metadata.repository_id.name / date_folder
        return cls(directory_path, pr_metadata.number)
    
    @classmethod
    def create_with_basic_info(cls, output_directory: Path, basic_info: PullRequestBasicInfo):
        date_folder = basic_info.closed_at.strftime("%Y-%m-%d")
        directory_path = output_directory / basic_info.repository_id.owner / basic_info.repository_id.name / date_folder
        return cls(directory_path, basic_info.number)

    def get_pr_directory(self) -> Path:
        """Get the directory path for a pull request."""
        return self._directory_path

    def get_comments_file_path(self) -> Path:
        """Get the file path for comments."""
        return self._directory_path / f"PR-{self._pr_number}-comments.json"

    def get_diff_file_path(self) -> Path:
        """Get the file path for diff."""
        return self._directory_path / f"PR-{self._pr_number}-diff.patch"

    def file_exists(self) -> bool:
        """Check if a file exists."""
        file_path = self.get_comments_file_path()
        return file_path.exists()