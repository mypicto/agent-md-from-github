"""
Factory for creating application services and dependencies.
"""

import logging
from typing import Optional

from github import Github

from ..application.services.pr_review_collection_service import PRReviewCollectionService
from ..application.services.missing_summaries_service import MissingSummariesService
from ..application.services.delete_summaries_service import DeleteSummariesService
from ..application.services.comments_service import CommentsService
from .repositories.github_repository import GitHubRepository
from .repositories.pull_request_metadata_repository import PullRequestMetadataRepository
from .repositories.pull_request_summary_repository import PullRequestSummaryRepository
from .services.timezone_converter import TimezoneConverter
from .file_system_deleter import FileSystemDeleter
from .filters.ai_comment_filter import AICommentFilter
from ..presentation.markdown_formatter import MarkdownFormatter


class ServiceFactory:
    """Factory for creating application services with proper dependencies."""
    
    @staticmethod
    def create_pr_collection_service(
        github_token: str,
        timezone: str = "Asia/Tokyo",
        logger: Optional[logging.Logger] = None
    ) -> PRReviewCollectionService:
        """Create a PR review collection service with all dependencies.
        
        Args:
            github_token: GitHub personal access token
            timezone: Target timezone for date conversion
            logger: Optional logger instance
            
        Returns:
            Configured PR review collection service
        """
        # Create GitHub client
        github_client = Github(github_token)
        
        # Create timezone converter
        timezone_converter = TimezoneConverter(timezone)
        
        # Create GitHub repository
        github_repository = GitHubRepository(github_client, timezone_converter)
        
        # Create PR metadata repository
        pr_metadata_repository = PullRequestMetadataRepository()
        
        # Create comment filter
        comment_filter = AICommentFilter()
        
        # Create and return application service
        return PRReviewCollectionService(
            github_repository=github_repository,
            pr_metadata_repository=pr_metadata_repository,
            comment_filter=comment_filter
        )
    
    @staticmethod
    def setup_logging(verbose: bool = False) -> logging.Logger:
        """Setup logging configuration.
        
        Args:
            verbose: Enable debug level logging
            
        Returns:
            Configured logger
        """
        # Set up root logger for the application
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create and configure handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        
        # Return the application-specific logger
        logger = logging.getLogger()
        return logger
    
    @staticmethod
    def create_missing_summaries_service() -> MissingSummariesService:
        """Create a missing summaries service with all dependencies.
        
        Returns:
            Configured missing summaries service
        """
        pr_metadata_repository = PullRequestMetadataRepository()
        summary_repository = PullRequestSummaryRepository()
        return MissingSummariesService(pr_metadata_repository, summary_repository)
    
    @staticmethod
    def create_delete_summaries_service() -> DeleteSummariesService:
        """Create a delete summaries service with all dependencies.
        
        Returns:
            Configured delete summaries service
        """
        file_deleter = FileSystemDeleter()
        return DeleteSummariesService(file_deleter)
    
    @staticmethod
    def create_comments_service() -> CommentsService:
        """Create a comments service with all dependencies.
        
        Returns:
            Configured comments service
        """
        pr_metadata_repository = PullRequestMetadataRepository()
        markdown_formatter = MarkdownFormatter()
        return CommentsService(pr_metadata_repository, markdown_formatter)