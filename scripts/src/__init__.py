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
    PullRequestMetadataRepositoryInterface,
    SummaryRepositoryInterface,
    TimezoneConverterInterface
)

# Domain layer - value objects
from .domain.date_range import DateRange
from .domain.pull_request_metadata import PullRequestMetadata
from .domain.repository_identifier import RepositoryIdentifier
from .domain.review_comment import ReviewComment

# Infrastructure layer
from .infrastructure.service_factory import ServiceFactory
from .infrastructure.repositories import GitHubRepository, PullRequestMetadataRepository, SummaryRepository
from .infrastructure.services import TimezoneConverter


__version__ = "2.0.0"

__all__ = [
    # Main entry points
    "ServiceFactory",
    
    # Application layer
    "PRReviewCollectionService",
    "PRReviewCollectionError",
    "GitHubApiError",
    
    # Domain layer - interfaces
    "GitHubRepositoryInterface",
    "PullRequestMetadataRepositoryInterface",
    "SummaryRepositoryInterface",
    "TimezoneConverterInterface",
    
    # Domain layer - value objects
    "DateRange",
    "PullRequestMetadata",
    "RepositoryIdentifier", 
    "ReviewComment",
    
    # Infrastructure layer
        # Infrastructure layer
    "GitHubRepository",
    "PullRequestMetadataRepository",
    "SummaryRepository",
    "ServiceFactory",
    "TimezoneConverter"
]