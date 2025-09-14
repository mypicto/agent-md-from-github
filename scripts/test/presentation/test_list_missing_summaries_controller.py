"""
Tests for ListMissingSummariesController.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
from scripts.src.presentation.list_missing_summaries_controller import ListMissingSummariesController
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestListMissingSummariesController:
    """Test cases for ListMissingSummariesController."""

    def test_run_正常実行_結果が出力される(self, capsys):
        """Test run executes successfully and outputs results."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_directory = Path(temp_dir)
            repo_id = RepositoryIdentifier(owner="test_owner", name="test_repo")
            # Mock service
            mock_service = Mock()
            mock_service.list_missing_summaries.return_value = [
                output_directory / "test_owner" / "test_repo" / "2023-01-01" / "PR-123-comments.json"
            ]
            with patch('scripts.src.presentation.list_missing_summaries_controller.ServiceFactory.create_missing_summaries_service', return_value=mock_service):
                controller = ListMissingSummariesController()
                controller.run(['--repo', 'test_owner/test_repo', '--output-dir', str(output_directory)])
                captured = capsys.readouterr()
                assert str(output_directory / "test_owner" / "test_repo" / "2023-01-01" / "PR-123-comments.json") in captured.out

    def test_run_無効なリポジトリ_ValueErrorが発生(self, capsys):
        """Test run raises ValueError for invalid repository."""
        controller = ListMissingSummariesController()
        with pytest.raises(SystemExit):
            controller.run(['--repo', 'invalid-repo'])
        captured = capsys.readouterr()
        assert "Error:" in captured.out