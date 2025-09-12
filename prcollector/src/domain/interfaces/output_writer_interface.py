"""
Interface for output writing strategies.
"""

from pathlib import Path
from typing import Protocol

from ..pull_request_metadata import PullRequestMetadata


class OutputWriterInterface(Protocol):
    """Interface for output writing strategies."""
    
    def write_pr_data(
        self, 
        pr_metadata: PullRequestMetadata, 
        comments_content: str, 
        diff_content: str, 
        output_directory: Path
    ) -> None:
        """Write PR data to storage."""
        ...
    
    def file_exists(self, pr_metadata: PullRequestMetadata, output_directory: Path) -> bool:
        """Check if PR files already exist (for idempotency)."""
        ...