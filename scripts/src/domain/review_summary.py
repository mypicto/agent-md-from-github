"""
Review summary value object.
"""

from dataclasses import dataclass

from .repository_identifier import RepositoryIdentifier


@dataclass(frozen=True)
class ReviewSummary:
    """Represents a review summary for a PR."""
    
    repository_id: RepositoryIdentifier
    pr_number: int
    priority: str
    summary: str
    
    def __post_init__(self):
        """Validate review summary."""
        if self.pr_number <= 0:
            raise ValueError("PR number must be positive")
        if self.priority not in ["high", "middle", "low"]:
            raise ValueError("Priority must be 'high', 'middle', or 'low'")
        if not self.summary.strip():
            raise ValueError("Summary must not be empty")