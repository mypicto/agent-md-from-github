"""
Application service for listing missing summaries.
"""

from typing import List
from pathlib import Path

from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.interfaces.pull_request_file_set_repository_interface import PullRequestFileSetRepositoryInterface


class MissingSummariesService:
    """Application service for listing missing summaries."""
    
    def __init__(self, file_set_repository: PullRequestFileSetRepositoryInterface):
        """Initialize missing summaries service.
        
        Args:
            file_set_repository: Repository for pull request file sets
        """
        self._pull_request_file_set_repository = file_set_repository
    
    def list_missing_summaries(self, repository_id: RepositoryIdentifier, output_directory: Path) -> List[Path]:
        """List paths of PR comments files that are missing corresponding summary files.
        
        Args:
            repository_id: Target repository identifier
            output_directory: Output directory
            
        Returns:
            List of comment file paths missing summaries
        """
        file_sets = self._pull_request_file_set_repository.find_pull_request_file_sets(output_directory, repository_id)
        
        missing = []
        for file_set in file_sets:
            if not file_set.exists_summary():
                missing.append(file_set.get_comments_file_path())
        
        return missing