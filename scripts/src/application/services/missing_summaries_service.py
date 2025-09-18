"""
Application service for listing missing summaries.
"""

from typing import List
from pathlib import Path

from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.pull_request_metadata import PullRequestMetadata
from ...domain.interfaces.pull_request_metadata_repository_interface import PullRequestMetadataRepositoryInterface
from ...domain.interfaces.summary_repository_interface import SummaryRepositoryInterface


class MissingSummariesService:
    """Application service for listing missing summaries."""
    
    def __init__(self, pr_metadata_repository: PullRequestMetadataRepositoryInterface, summary_repository: SummaryRepositoryInterface):
        """Initialize missing summaries service.
        
        Args:
            pr_metadata_repository: Repository for pull request metadata
            summary_repository: Repository for checking summary existence
        """
        self._pr_metadata_repository = pr_metadata_repository
        self._summary_repository = summary_repository
    
    def list_missing_summaries(self, repository_id: RepositoryIdentifier, output_directory: Path) -> List[int]:
        """List PR numbers that are missing corresponding summary files.
        
        Filters out PRs with no review comments and sorts by review comment count in descending order.
        
        Args:
            repository_id: Target repository identifier
            output_directory: Output directory
            
        Returns:
            List of PR numbers missing summaries, filtered and sorted
        """
        metadata_list = self._pr_metadata_repository.find_all_by_repository(output_directory, repository_id)
        
        metadata_list = self._filter_metadata(metadata_list)
        metadata_list = self._sort_metadata(metadata_list)
        
        missing_numbers = self._find_missing_numbers(metadata_list, output_directory)
        
        return missing_numbers
    
    def _filter_metadata(self, metadata_list: List[PullRequestMetadata]) -> List[PullRequestMetadata]:
        """Filter out PRs with no review comments.
        
        Args:
            metadata_list: List of PR metadata
            
        Returns:
            Filtered list of PR metadata
        """
        return [metadata for metadata in metadata_list if len(metadata.review_comments) > 0]
    
    def _sort_metadata(self, metadata_list: List[PullRequestMetadata]) -> List[PullRequestMetadata]:
        """Sort PR metadata by review comment count in descending order.
        
        Args:
            metadata_list: List of PR metadata
            
        Returns:
            Sorted list of PR metadata
        """
        return sorted(metadata_list, key=lambda m: len(m.review_comments), reverse=True)
    
    def _find_missing_numbers(self, metadata_list: List[PullRequestMetadata], output_directory: Path) -> List[int]:
        """Find PR numbers that are missing corresponding summary files.
        
        Args:
            metadata_list: Filtered and sorted list of PR metadata
            output_directory: Output directory
            
        Returns:
            List of PR numbers missing summaries
        """
        missing_numbers = []
        for metadata in metadata_list:
            if not self._summary_repository.exists_summary(metadata, output_directory):
                missing_numbers.append(metadata.number)
        
        return missing_numbers