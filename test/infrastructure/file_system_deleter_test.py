"""
Tests for FileSystemDeleter.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.src.domain.file_deletion_criteria import FileDeletionCriteria
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.infrastructure.file_system_deleter import FileSystemDeleter


class TestFileSystemDeleter:
    """Test cases for FileSystemDeleter."""
    
    def test_delete_files_ファイルなし(self):
        """Test deleting when no files match."""
        with tempfile.TemporaryDirectory() as temp_dir:
            criteria = FileDeletionCriteria()
            deleter = FileSystemDeleter()
            
            result = deleter.delete_files(criteria, Path(temp_dir))
            assert result == []
    
    def test_delete_files_マッチファイル削除(self):
        """Test deleting matching files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test files
            (temp_path / "PR-123-summary.md").touch()
            (temp_path / "PR-456-summary.md").touch()
            (temp_path / "other-file.txt").touch()
            
            criteria = FileDeletionCriteria()
            deleter = FileSystemDeleter()
            
            result = deleter.delete_files(criteria, temp_path)
            
            assert len(result) == 2
            assert not (temp_path / "PR-123-summary.md").exists()
            assert not (temp_path / "PR-456-summary.md").exists()
            assert (temp_path / "other-file.txt").exists()
    
    def test_delete_files_サブディレクトリ(self):
        """Test deleting files in subdirectories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create subdirectory with files
            sub_dir = temp_path / "subdir"
            sub_dir.mkdir()
            (sub_dir / "PR-789-summary.md").touch()
            
            criteria = FileDeletionCriteria()
            deleter = FileSystemDeleter()
            
            result = deleter.delete_files(criteria, temp_path)
            
            assert len(result) == 1
            assert not (sub_dir / "PR-789-summary.md").exists()
    
    def test_delete_files_リポジトリ指定(self):
        """Test deleting with repository specified."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create repository structure
            repo_dir = temp_path / "owner" / "repo"
            repo_dir.mkdir(parents=True)
            (repo_dir / "PR-999-summary.md").touch()
            
            repo_id = RepositoryIdentifier("owner", "repo")
            criteria = FileDeletionCriteria(repository_id=repo_id)
            deleter = FileSystemDeleter()
            
            result = deleter.delete_files(criteria, temp_path)
            
            assert len(result) == 1
            assert not (repo_dir / "PR-999-summary.md").exists()
    
    @patch('pathlib.Path.unlink')
    def test_delete_files_削除失敗(self, mock_unlink):
        """Test handling deletion failure."""
        mock_unlink.side_effect = OSError("Permission denied")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "PR-123-summary.md").touch()
            
            criteria = FileDeletionCriteria()
            deleter = FileSystemDeleter()
            
            with patch('pathlib.Path.exists', return_value=True):
                result = deleter.delete_files(criteria, temp_path)
                assert result == []  # Failed deletions not included