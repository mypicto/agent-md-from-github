"""
Tests for PullRequestMetadataRepository.
"""

import json
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from scripts.src.domain.pull_request_basic_info import PullRequestBasicInfo
from scripts.src.domain.pull_request_metadata import PullRequestMetadata
from scripts.src.domain.repository_identifier import RepositoryIdentifier
from scripts.src.domain.review_comment import ReviewComment
from scripts.src.infrastructure.repositories.pull_request_metadata_repository import PullRequestMetadataRepository


class TestPullRequestMetadataRepository:
    """Test cases for PullRequestMetadataRepository."""

    def test_save_保存が成功する(self):
        """Test that save creates the correct JSON file."""
        # Arrange
        repo = PullRequestMetadataRepository()
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")
        closed_at = datetime(2023, 10, 1, 12, 0, 0)
        comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=10,
            commit_id="abc123",
            author="test-user",
            created_at=datetime(2023, 9, 30, 10, 0, 0),
            body="Test comment",
            diff_context="@@ -1 +1 @@\n-old\n+new"
        )
        pr_metadata = PullRequestMetadata(
            number=123,
            title="Test PR",
            closed_at=closed_at,
            is_merged=True,
            review_comments=[comment],
            repository_id=repo_id
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            # Act
            repo.save(pr_metadata, output_dir)

            # Assert
            expected_path = output_dir / "test-owner" / "test-repo" / "2023-10-01" / "PR-123-metadata.json"
            assert expected_path.exists()

            with open(expected_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            assert data["number"] == 123
            assert data["title"] == "Test PR"
            assert data["closed_at"] == "2023-10-01T12:00:00"
            assert data["is_merged"] is True
            assert len(data["review_comments"]) == 1
            assert data["review_comments"][0]["body"] == "Test comment"
            assert data["repository_id"]["owner"] == "test-owner"
            assert data["repository_id"]["name"] == "test-repo"

    def test_exists_ファイルが存在する場合Trueを返す(self):
        """Test that exists returns True when file exists."""
        # Arrange
        repo = PullRequestMetadataRepository()
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")
        closed_at = datetime(2023, 10, 1, 12, 0, 0)
        basic_info = PullRequestBasicInfo(
            number=123,
            title="Test PR",
            closed_at=closed_at,
            is_merged=True,
            repository_id=repo_id
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            # Create the file
            file_path = output_dir / "test-owner" / "test-repo" / "2023-10-01" / "PR-123-metadata.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()

            # Act
            result = repo.exists(basic_info, output_dir)

            # Assert
            assert result is True

    def test_exists_ファイルが存在しない場合Falseを返す(self):
        """Test that exists returns False when file does not exist."""
        # Arrange
        repo = PullRequestMetadataRepository()
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")
        closed_at = datetime(2023, 10, 1, 12, 0, 0)
        basic_info = PullRequestBasicInfo(
            number=123,
            title="Test PR",
            closed_at=closed_at,
            is_merged=True,
            repository_id=repo_id
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            # Act
            result = repo.exists(basic_info, output_dir)

            # Assert
            assert result is False