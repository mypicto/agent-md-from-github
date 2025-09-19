"""
Tests for PullRequestMetadataRepository.
"""

import json
import tempfile
from datetime import datetime
from pathlib import Path

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

    def test_find_all_by_repository_リポジトリの全PRメタデータを正しく読み込む(self):
        """Test that find_all_by_repository loads all PR metadata correctly."""
        # Arrange
        repo = PullRequestMetadataRepository()
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")

        # Create test data
        pr1_metadata = PullRequestMetadata(
            number=123,
            title="Test PR 1",
            closed_at=datetime(2023, 10, 1, 12, 0, 0),
            is_merged=True,
            review_comments=[
                ReviewComment(
                    comment_id=1,
                    file_path="file1.py",
                    position=None,
                    commit_id="commit1",
                    author="user1",
                    created_at=datetime(2023, 9, 30, 10, 0, 0),
                    body="Comment 1",
                    diff_context="@@ -1 +1 @@\n-old1\n+new1"
                )
            ],
            repository_id=repo_id
        )

        pr2_metadata = PullRequestMetadata(
            number=456,
            title="Test PR 2",
            closed_at=datetime(2023, 10, 2, 14, 0, 0),
            is_merged=False,
            review_comments=[
                ReviewComment(
                    comment_id=2,
                    file_path="file2.py",
                    position=None,
                    commit_id="commit2",
                    author="user2",
                    created_at=datetime(2023, 10, 1, 11, 0, 0),
                    body="Comment 2",
                    diff_context="@@ -2 +2 @@\n-old2\n+new2"
                )
            ],
            repository_id=repo_id
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            # Save test data
            repo.save(pr1_metadata, output_dir)
            repo.save(pr2_metadata, output_dir)

            # Act
            result = repo.find_all_by_repository(output_dir, repo_id)

            # Assert
            assert len(result) == 2
            # Sort by PR number for consistent comparison
            result.sort(key=lambda x: x.number)

            assert result[0].number == 123
            assert result[0].title == "Test PR 1"
            assert result[0].closed_at == datetime(2023, 10, 1, 12, 0, 0)
            assert result[0].is_merged is True
            assert len(result[0].review_comments) == 1
            assert result[0].review_comments[0].body == "Comment 1"
            assert result[0].repository_id.owner == "test-owner"
            assert result[0].repository_id.name == "test-repo"

            assert result[1].number == 456
            assert result[1].title == "Test PR 2"
            assert result[1].closed_at == datetime(2023, 10, 2, 14, 0, 0)
            assert result[1].is_merged is False
            assert len(result[1].review_comments) == 1
            assert result[1].review_comments[0].body == "Comment 2"

    def test_find_all_by_repository_ディレクトリが存在しない場合空リストを返す(self):
        """Test that find_all_by_repository returns empty list when directory doesn't exist."""
        # Arrange
        repo = PullRequestMetadataRepository()
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            # Act
            result = repo.find_all_by_repository(output_dir, repo_id)

            # Assert
            assert result == []

    def test_find_all_by_repository_無効なJSONファイルをスキップする(self):
        """Test that find_all_by_repository skips invalid JSON files."""
        # Arrange
        repo = PullRequestMetadataRepository()
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            repo_dir = output_dir / "test-owner" / "test-repo" / "2023-10-01"
            repo_dir.mkdir(parents=True, exist_ok=True)

            # Create valid JSON file
            valid_file = repo_dir / "PR-123-metadata.json"
            valid_data = {
                "number": 123,
                "title": "Valid PR",
                "closed_at": "2023-10-01T12:00:00",
                "is_merged": True,
                "review_comments": [],
                "repository_id": {"owner": "test-owner", "name": "test-repo"}
            }
            with open(valid_file, "w", encoding="utf-8") as f:
                json.dump(valid_data, f)

            # Create invalid JSON file
            invalid_file = repo_dir / "PR-456-metadata.json"
            with open(invalid_file, "w", encoding="utf-8") as f:
                f.write("invalid json content")

            # Act
            result = repo.find_all_by_repository(output_dir, repo_id)

            # Assert
            assert len(result) == 1
            assert result[0].number == 123
            assert result[0].title == "Valid PR"

    def test_find_by_pr_number_PRが見つかる場合正しく返す(self):
        """Test that find_by_pr_number returns the correct PR when found."""
        # Arrange
        repo = PullRequestMetadataRepository()
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")

        pr_metadata = PullRequestMetadata(
            number=123,
            title="Test PR",
            closed_at=datetime(2023, 10, 1, 12, 0, 0),
            is_merged=True,
            review_comments=[
                ReviewComment(
                    comment_id=1,
                    file_path="file.py",
                    position=None,
                    commit_id="commit1",
                    author="user1",
                    created_at=datetime(2023, 9, 30, 10, 0, 0),
                    body="Comment",
                    diff_context="@@ -1 +1 @@\n-old\n+new"
                )
            ],
            repository_id=repo_id
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            # Save test data
            repo.save(pr_metadata, output_dir)

            # Act
            result = repo.find_by_pr_number(output_dir, repo_id, 123)

            # Assert
            assert result is not None
            assert result.number == 123
            assert result.title == "Test PR"
            assert result.closed_at == datetime(2023, 10, 1, 12, 0, 0)
            assert result.is_merged is True
            assert len(result.review_comments) == 1
            assert result.review_comments[0].body == "Comment"

    def test_find_by_pr_number_PRが見つからない場合Noneを返す(self):
        """Test that find_by_pr_number returns None when PR is not found."""
        # Arrange
        repo = PullRequestMetadataRepository()
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")

        pr_metadata = PullRequestMetadata(
            number=123,
            title="Test PR",
            closed_at=datetime(2023, 10, 1, 12, 0, 0),
            is_merged=True,
            review_comments=[],
            repository_id=repo_id
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            # Save test data
            repo.save(pr_metadata, output_dir)

            # Act
            result = repo.find_by_pr_number(output_dir, repo_id, 999)  # Non-existent PR number

            # Assert
            assert result is None

    def test_find_by_pr_number_リポジトリにPRが存在しない場合Noneを返す(self):
        """Test that find_by_pr_number returns None when no PRs exist in repository."""
        # Arrange
        repo = PullRequestMetadataRepository()
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            # Act
            result = repo.find_by_pr_number(output_dir, repo_id, 123)

            # Assert
            assert result is None