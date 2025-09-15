"""
Tests for FileDeletionCriteria.
"""

import pytest

from scripts.src.domain.file_deletion_criteria import FileDeletionCriteria
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestFileDeletionCriteria:
    """Test cases for FileDeletionCriteria."""
    
    def test_デフォルト値_正常作成(self):
        """Test creating with default values."""
        criteria = FileDeletionCriteria()
        assert criteria.file_pattern == "PR-*-summary.md"
        assert criteria.repository_id is None
    
    def test_repository_id指定_正常作成(self):
        """Test creating with repository ID."""
        repo_id = RepositoryIdentifier("owner", "repo")
        criteria = FileDeletionCriteria(repository_id=repo_id)
        assert criteria.repository_id == repo_id
    
    def test_空パターン_エラー(self):
        """Test validation with empty pattern."""
        with pytest.raises(ValueError, match="File pattern must not be empty"):
            FileDeletionCriteria(file_pattern="")
    
    def test_get_target_directory_リポジトリなし(self):
        """Test get_target_directory without repository."""
        criteria = FileDeletionCriteria()
        result = criteria.get_target_directory("pullrequests")
        assert result == "pullrequests"
    
    def test_get_target_directory_リポジトリあり(self):
        """Test get_target_directory with repository."""
        repo_id = RepositoryIdentifier("owner", "repo")
        criteria = FileDeletionCriteria(repository_id=repo_id)
        result = criteria.get_target_directory("pullrequests")
        assert result == "pullrequests/owner/repo"