"""
File system implementation for file deletion.
"""

import fnmatch
import logging
from pathlib import Path
from typing import List

from ..domain.file_deletion_criteria import FileDeletionCriteria
from ..domain.interfaces.file_deleter_interface import FileDeleterInterface


class FileSystemDeleter(FileDeleterInterface):
    """File system implementation for deleting files."""
    
    def __init__(self):
        """Initialize file system deleter."""
        self._logger = logging.getLogger("filesystem_deleter")
    
    def delete_files(self, criteria: FileDeletionCriteria, base_directory: Path) -> List[Path]:
        """Delete files matching the criteria.
        
        Args:
            criteria: Deletion criteria
            base_directory: Base directory to search
            
        Returns:
            List of deleted file paths
        """
        target_directory = Path(criteria.get_target_directory(str(base_directory)))
        
        if not target_directory.exists():
            self._logger.warning(f"Target directory does not exist: {target_directory}")
            return []
        
        deleted_files = []
        
        # Recursively find and delete matching files
        for file_path in target_directory.rglob("*"):
            if file_path.is_file() and fnmatch.fnmatch(file_path.name, criteria.file_pattern):
                try:
                    file_path.unlink()
                    deleted_files.append(file_path)
                    self._logger.info(f"Deleted file: {file_path}")
                except OSError as e:
                    self._logger.error(f"Failed to delete file {file_path}: {e}")
        
        return deleted_files