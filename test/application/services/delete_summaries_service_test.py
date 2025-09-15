"""
Tests for DeleteSummariesService.
"""

from pathlib import Path
from unittest.mock import Mock

import pytest

from scripts.src.application.services.delete_summaries_service import DeleteSummariesService
from scripts.src.domain.file_deletion_criteria import FileDeletionCriteria
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestDeleteSummariesService:
    """Test cases for DeleteSummariesService."""
    
    def test_delete_summaries_リポジトリなし(self):
        """Test deleting summaries without repository filter."""
        mock_deleter = Mock()
        mock_deleter.delete_files.return_value = [Path("file1.md"), Path("file2.md")]
        
        service = DeleteSummariesService(mock_deleter)
        result = service.delete_summaries(None, Path("pullrequests"))
        
        assert len(result) == 2
        mock_deleter.delete_files.assert_called_once()
        criteria = mock_deleter.delete_files.call_args[0][0]
        assert criteria.repository_id is None
        assert criteria.file_pattern == "PR-*-summary.md"
    
    def test_delete_summaries_リポジトリ指定(self):
        """Test deleting summaries with repository filter."""
        mock_deleter = Mock()
        mock_deleter.delete_files.return_value = [Path("file1.md")]
        
        repo_id = RepositoryIdentifier("owner", "repo")
        service = DeleteSummariesService(mock_deleter)
        result = service.delete_summaries(repo_id, Path("pullrequests"))
        
        assert len(result) == 1
        mock_deleter.delete_files.assert_called_once()
        criteria = mock_deleter.delete_files.call_args[0][0]
        assert criteria.repository_id == repo_id
    
    def test_delete_summaries_空結果(self):
        """Test deleting summaries with no files found."""
        mock_deleter = Mock()
        mock_deleter.delete_files.return_value = []
        
        service = DeleteSummariesService(mock_deleter)
        result = service.delete_summaries(None, Path("pullrequests"))
        
        assert result == []