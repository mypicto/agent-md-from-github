"""
Factory for creating application services and dependencies.
"""

import logging
from typing import Optional

from github import Github

from ..application.services.pr_review_collection_service import PRReviewCollectionService
from .file_system_output_writer import FileSystemOutputWriter
from .repositories.github_repository import GitHubRepository
from .json_output_formatter import JsonOutputFormatter
from .services.timezone_converter import TimezoneConverter


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
        
        # Create output formatter and writer
        output_formatter = JsonOutputFormatter()
        output_writer = FileSystemOutputWriter()
        
        # Create and return application service
        return PRReviewCollectionService(
            github_repository=github_repository,
            output_formatter=output_formatter,
            output_writer=output_writer
        )
    
    @staticmethod
    def setup_logging(verbose: bool = False) -> logging.Logger:
        """Setup logging configuration.
        
        Args:
            verbose: Enable debug level logging
            
        Returns:
            Configured logger
        """
        logger = logging.getLogger("prcollector")
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger