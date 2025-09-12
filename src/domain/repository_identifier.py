"""
Repository identifier value object.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryIdentifier:
    """Represents a GitHub repository identifier."""
    
    owner: str
    name: str
    
    def __post_init__(self):
        """Validate repository identifier."""
        if not self.owner or not self.name:
            raise ValueError("Owner and name must not be empty")
    
    @classmethod
    def from_string(cls, repo_string: str) -> 'RepositoryIdentifier':
        """Create from 'owner/repo' format string."""
        try:
            owner, name = repo_string.split('/', 1)
            return cls(owner=owner, name=name)
        except ValueError:
            raise ValueError(f"Invalid repository format: {repo_string}. Use 'owner/repo'")
    
    def to_string(self) -> str:
        """Convert to 'owner/repo' format string."""
        return f"{self.owner}/{self.name}"