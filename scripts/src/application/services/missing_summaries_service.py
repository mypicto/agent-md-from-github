"""
Application service for listing missing summaries.
"""

from typing import List
from pathlib import Path

from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.interfaces.pull_request_metadata_repository_interface import PullRequestMetadataRepositoryInterface
from ...domain.interfaces.pull_request_summary_repository_interface import PullRequestSummaryRepositoryInterface


class MissingSummariesService:
    """Application service for listing missing summaries."""
    
    def __init__(self, pr_metadata_repository: PullRequestMetadataRepositoryInterface, summary_repository: PullRequestSummaryRepositoryInterface):
        """Initialize missing summaries service.
        
        Args:
            pr_metadata_repository: Repository for pull request metadata
            summary_repository: Repository for checking summary existence
        """
        self._pr_metadata_repository = pr_metadata_repository
        self._summary_repository = summary_repository
    
    def list_missing_summaries(self, repository_id: RepositoryIdentifier, output_directory: Path) -> List[int]:
        """List PR numbers that are missing corresponding summary files.
        
        Args:
            repository_id: Target repository identifier
            output_directory: Output directory
            
        Returns:
            List of PR numbers missing summaries
        """
        metadata_list = self._pr_metadata_repository.find_all_by_repository(output_directory, repository_id)
        
        missing_numbers = []
        for metadata in metadata_list:
            if not self._summary_repository.exists_summary(metadata, output_directory):
                missing_numbers.append(metadata.number)
        
        return missing_numbers