"""
Tests for FileSystemOutputWriter.
"""

from datetime import datetime
from pathlib import Path
from unittest.mock import patch, mock_open
from scripts.src.infrastructure.file_system_output_writer import FileSystemOutputWriter
from scripts.src.domain.pull_request_metadata import PullRequestMetadata
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestFileSystemOutputWriter:
    """Test cases for FileSystemOutputWriter."""

    def test_write_pr_data_正常書き込み_ファイルが作成される(self):
        """Test write_pr_data writes files correctly."""
        writer = FileSystemOutputWriter()
        repo_id = RepositoryIdentifier(owner="test", name="repo")
        pr_metadata = PullRequestMetadata(
            number=1,
            title="Test PR",
            closed_at=datetime(2023, 1, 1),
            is_merged=True,
            review_comments=[],
            repository_id=repo_id
        )
        comments_content = '{"test": "data"}'
        diff_content = "diff content"
        output_directory = Path("test_output")

        with patch('builtins.open', mock_open()) as mock_file:
            with patch('pathlib.Path.mkdir') as mock_mkdir:
                writer.write_pr_data(pr_metadata, comments_content, diff_content, output_directory)

                # Check that mkdir was called
                mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

                # Check that open was called twice (for comments and diff files)
                assert mock_file.call_count == 2

    def test__write_text_file_正常書き込み_ファイルが書き込まれる(self):
        """Test _write_text_file writes content correctly."""
        writer = FileSystemOutputWriter()
        file_path = Path("test_file.txt")
        content = "test content"

        with patch('builtins.open', mock_open()) as mock_file:
            writer._write_text_file(file_path, content)

            mock_file.assert_called_once_with(file_path, 'w', encoding='utf-8')
            mock_file().write.assert_called_once_with(content)