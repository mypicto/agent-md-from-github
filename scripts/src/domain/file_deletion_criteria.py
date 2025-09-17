"""
File deletion criteria value object.
"""

from dataclasses import dataclass
from typing import Optional

from .repository_identifier import RepositoryIdentifier


@dataclass(frozen=True)
class FileDeletionCriteria:
    """Represents criteria for file deletion."""
    
    file_pattern: str = "PR-*-summary.md"
    repository_id: Optional[RepositoryIdentifier] = None
    
    def __post_init__(self):
        """Validate file deletion criteria."""
        if not self.file_pattern:
            raise ValueError("File pattern must not be empty")
    
    def get_target_directory(self, base_directory: str) -> str:
        """Get target directory based on repository ID.
        
        Args:
            base_directory: Base directory (e.g., 'pullrequests')
            
        Returns:
            Target directory path
        """
        if self.repository_id:
            return f"{base_directory}/{self.repository_id.owner}/{self.repository_id.name}"
        return base_directory