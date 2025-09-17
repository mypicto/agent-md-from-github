"""
Interface for output formatting strategies.
"""

from typing import Protocol

from ..pull_request_metadata import PullRequestMetadata


class OutputFormatterInterface(Protocol):
    """Interface for output formatting strategies."""
    
    def format_comments(self, pr_metadata: PullRequestMetadata) -> str:
        """Format review comments for output."""
        ...
