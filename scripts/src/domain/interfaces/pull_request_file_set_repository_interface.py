"""
Interface for repository handling pull request file sets.
"""

from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from ..repository_identifier import RepositoryIdentifier
from ...infrastructure.pull_request_file_set import PullRequestFileSet


class PullRequestFileSetRepositoryInterface(ABC):
    """Interface for repository handling pull request file sets."""
    
    @abstractmethod
    def find_pull_request_file_sets(self, output_directory: Path, repository_id: RepositoryIdentifier) -> List[PullRequestFileSet]:
        """Find all pull request file sets for the given repository."""
        pass