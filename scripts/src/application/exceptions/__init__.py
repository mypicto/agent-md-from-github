"""
Application exceptions package.
"""

from .pr_review_collection_error import PRReviewCollectionError
from .github_api_error import GitHubApiError

__all__ = [
    "PRReviewCollectionError",
    "GitHubApiError"
]