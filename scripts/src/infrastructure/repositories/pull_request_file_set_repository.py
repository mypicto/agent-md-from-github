"""
Repository for finding pull request file sets from file system.
"""

from typing import List
from pathlib import Path
from glob import glob

from ...domain.interfaces.pull_request_file_set_repository_interface import PullRequestFileSetRepositoryInterface
from ...domain.repository_identifier import RepositoryIdentifier
from ..pull_request_file_set import PullRequestFileSet


class PullRequestFileSetRepository(PullRequestFileSetRepositoryInterface):
    """Repository for finding pull request file sets from file system."""

    def find_pull_request_file_sets(self, output_directory: Path, repository_id: RepositoryIdentifier) -> List[PullRequestFileSet]:
        """Find all pull request file sets for the given repository."""
        repo_dir = output_directory / repository_id.owner / repository_id.name
        if not repo_dir.exists():
            return []
        
        pattern = repo_dir / "**" / PullRequestFileSet.get_comments_pattern()
        comment_files = glob(str(pattern), recursive=True)
        
        file_sets = []
        for file_path_str in comment_files:
            file_path = Path(file_path_str)
            file_set = PullRequestFileSet.create_from_comments_file_path(file_path)
            file_sets.append(file_set)
        return file_sets