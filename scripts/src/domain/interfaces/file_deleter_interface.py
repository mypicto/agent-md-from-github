"""
Interface for file deletion operations.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from ..file_deletion_criteria import FileDeletionCriteria


class FileDeleterInterface(ABC):
    """Interface for deleting files based on criteria."""
    
    @abstractmethod
    def delete_files(self, criteria: FileDeletionCriteria, base_directory: Path) -> List[Path]:
        """Delete files matching the criteria.
        
        Args:
            criteria: Deletion criteria
            base_directory: Base directory to search
            
        Returns:
            List of deleted file paths
        """
        pass