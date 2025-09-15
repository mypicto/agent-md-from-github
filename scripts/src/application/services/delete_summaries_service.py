"""
Application service for deleting PR summary files.
"""

import logging
from pathlib import Path
from typing import List, Optional

from ...domain.file_deletion_criteria import FileDeletionCriteria
from ...domain.interfaces.file_deleter_interface import FileDeleterInterface
from ...domain.repository_identifier import RepositoryIdentifier


class DeleteSummariesService:
    """Application service for deleting PR summary files."""
    
    def __init__(self, file_deleter: FileDeleterInterface):
        """Initialize delete summaries service.
        
        Args:
            file_deleter: File deleter implementation
        """
        self._file_deleter = file_deleter
        self._logger = logging.getLogger("delete_summaries_service")
    
    def delete_summaries(
        self,
        repository_id: Optional[RepositoryIdentifier],
        output_directory: Path
    ) -> List[Path]:
        """Delete PR summary files.
        
        Args:
            repository_id: Target repository (None for all)
            output_directory: Base output directory
            
        Returns:
            List of deleted file paths
        """
        criteria = FileDeletionCriteria(repository_id=repository_id)
        
        self._logger.info(f"Starting deletion with criteria: {criteria}")
        
        deleted_files = self._file_deleter.delete_files(criteria, output_directory)
        
        self._logger.info(f"Deleted {len(deleted_files)} files")
        
        return deleted_files