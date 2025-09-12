"""
GitHub PR Review Comments Collector

A clean architecture implementation for collecting review comments 
from GitHub pull requests.
"""

# Application layer
from .application.exceptions import (
    PRReviewCollectionError,
    GitHubApiError
)
from .application.services import (
    PRReviewCollectionService
)

# Domain layer - interfaces
from .domain.interfaces import (
    GitHubRepositoryInterface,
    OutputFormatterInterface,
    OutputWriterInterface,
    TimezoneConverterInterface
)

# Domain layer - value objects
from .domain.date_range import DateRange
from .domain.pull_request_metadata import PullRequestMetadata
from .domain.repository_identifier import RepositoryIdentifier
from .domain.review_comment import ReviewComment

# Infrastructure layer
from .infrastructure.file_system_output_writer import FileSystemOutputWriter
from .infrastructure.json_output_formatter import JsonOutputFormatter
from .infrastructure.service_factory import ServiceFactory
from .infrastructure.repositories import GitHubRepository
from .infrastructure.services import TimezoneConverter

# Presentation layer
from .presentation.cli_controller import CLIController


__version__ = "2.0.0"

def main():
    """Main entry point for CLI application."""
    cli = CLIController()
    cli.run()

__all__ = [
    # Main entry points
    "main",
    "CLIController",
    "ServiceFactory",
    
    # Application layer
    "PRReviewCollectionService",
    "PRReviewCollectionError",
    "GitHubApiError",
    
    # Domain layer - interfaces
    "GitHubRepositoryInterface",
    "OutputFormatterInterface",
    "OutputWriterInterface", 
    "TimezoneConverterInterface",
    
    # Domain layer - value objects
    "DateRange",
    "PullRequestMetadata",
    "RepositoryIdentifier", 
    "ReviewComment",
    
    # Infrastructure layer
    "FileSystemOutputWriter",
    "GitHubRepository",
    "JsonOutputFormatter",
    "TimezoneConverter"
]