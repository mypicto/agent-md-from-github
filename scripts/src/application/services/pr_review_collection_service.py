"""
Application service for PR review collection.
"""

import logging
from pathlib import Path

from ...domain.date_range import DateRange
from ...domain.pull_request_metadata import PullRequestMetadata
from ...domain.repository_identifier import RepositoryIdentifier
from ...domain.interfaces.github_repository_interface import GitHubRepositoryInterface
from ...domain.interfaces.output_formatter_interface import OutputFormatterInterface
from ...domain.interfaces.output_writer_interface import OutputWriterInterface
from ..exceptions.pr_review_collection_error import PRReviewCollectionError


class PRReviewCollectionService:
    """Application service for collecting PR review comments."""
    
    def __init__(
        self,
        github_repository: GitHubRepositoryInterface,
        output_formatter: OutputFormatterInterface,
        output_writer: OutputWriterInterface
    ):
        """Initialize PR review collection service.
        
        Args:
            github_repository: GitHub repository interface
            output_formatter: Output formatting strategy
            output_writer: Output writing strategy
        """
        self._github_repository = github_repository
        self._output_formatter = output_formatter
        self._output_writer = output_writer
        self._logger = logging.getLogger("fetch")
    
    def collect_review_comments(
        self,
        repository_id: RepositoryIdentifier,
        date_range: DateRange,
        output_directory: Path
    ) -> None:
        """Collect review comments from PRs in the specified date range.
        
        Args:
            repository_id: Target repository identifier
            date_range: Date range for filtering PRs
            output_directory: Output directory for results
        
        Raises:
            PRReviewCollectionError: If collection fails
        """
        self._logger.info(f"Starting collection for {repository_id.to_string()}")
        self._logger.info(f"Period: {date_range.start_date.date()} to {date_range.end_date.date()}")
        self._logger.info(f"Searching for PRs closed between {date_range.start_date.strftime('%Y-%m-%d %H:%M:%S%z')} and {date_range.end_date.strftime('%Y-%m-%d %H:%M:%S%z')}")
        
        try:
            # Find and process PRs in streaming fashion
            processed_count = 0
            total_found = 0
            skipped_count = 0
            
            for basic_info in self._github_repository.find_closed_prs_basic_info(
                repository_id, 
                date_range
            ):
                total_found += 1
                
                # Check if files already exist
                if self._output_writer.exists_file_from_basic_info(basic_info, output_directory):
                    skipped_count += 1
                    self._logger.info(f"Skipping PR #{basic_info.number} - files already exist")
                    continue
                
                # Get full PR metadata only if files don't exist
                pr_metadata = self._github_repository.get_full_pr_metadata(basic_info.number, repository_id)
                
                if self._process_single_pr(pr_metadata, output_directory):
                    processed_count += 1
            
            self._logger.info(f"Collection completed. Found {total_found} PRs, processed {processed_count} PRs, skipped {skipped_count} PRs.")
            
        except Exception as e:
            raise PRReviewCollectionError(f"Failed to collect review comments: {e}") from e
    
    def _process_single_pr(self, pr_metadata: PullRequestMetadata, output_directory: Path) -> bool:
        """Process a single PR.
        
        Args:
            pr_metadata: PR metadata
            output_directory: Output directory
            
        Returns:
            True if PR was processed, False
        """
        try:
            # Format output content
            comments_content = self._output_formatter.format_comments(pr_metadata)
            diff_content = self._output_formatter.format_diff_excerpt(pr_metadata)
            
            # Write output
            self._output_writer.write_pr_data(
                pr_metadata,
                comments_content,
                diff_content,
                output_directory
            )
            
            self._logger.info(
                f"Saved PR #{pr_metadata.number}: {pr_metadata.title} data ({len(pr_metadata.review_comments)} comments)"
            )
            return True
            
        except Exception as e:
            self._logger.error(f"Error processing PR #{pr_metadata.number}: {e}")
            return False