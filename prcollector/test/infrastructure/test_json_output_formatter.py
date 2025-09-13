"""
Tests for JsonOutputFormatter.
"""

import json
from datetime import datetime
from prcollector.src.infrastructure.json_output_formatter import JsonOutputFormatter
from prcollector.src.domain.pull_request_metadata import PullRequestMetadata
from prcollector.src.domain.review_comment import ReviewComment
from prcollector.src.domain.repository_identifier import RepositoryIdentifier


class TestJsonOutputFormatter:
    """Test cases for JsonOutputFormatter."""

    def test_format_comments_正常フォーマット_JSON文字列が返される(self):
        """Test format_comments formats comments as JSON string."""
        formatter = JsonOutputFormatter()
        repo_id = RepositoryIdentifier(owner="test", name="repo")
        comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=10,
            commit_id="abc123",
            author="testuser",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            body="Test comment",
            diff_context="+ test line"
        )
        pr_metadata = PullRequestMetadata(
            number=1,
            title="Test PR",
            closed_at=datetime(2023, 1, 1, 12, 0, 0),
            is_merged=True,
            review_comments=[comment],
            repository_id=repo_id
        )

        result = formatter.format_comments(pr_metadata)

        # Parse JSON to verify structure
        data = json.loads(result)
        assert data["pr_number"] == 1
        assert data["merged"] is True
        assert len(data["review_comments"]) == 1
        assert data["review_comments"][0]["id"] == 1

    def test_format_diff_excerpt_正常フォーマット_マークダウン文字列が返される(self):
        """Test format_diff_excerpt formats diff as markdown string."""
        formatter = JsonOutputFormatter()
        repo_id = RepositoryIdentifier(owner="test", name="repo")
        comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=10,
            commit_id="abc123",
            author="testuser",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            body="Test comment",
            diff_context="+ test line"
        )
        pr_metadata = PullRequestMetadata(
            number=1,
            title="Test PR",
            closed_at=datetime(2023, 1, 1, 12, 0, 0),
            is_merged=True,
            review_comments=[comment],
            repository_id=repo_id
        )

        result = formatter.format_diff_excerpt(pr_metadata)

        assert f"# PR #{pr_metadata.number}" in result
        assert f"## File: {comment.file_path}" in result
        assert f"Comment by {comment.author}" in result
        assert "```diff" in result
        assert comment.diff_context in result

    def test__format_review_comment_正常フォーマット_辞書が返される(self):
        """Test _format_review_comment formats comment as dictionary."""
        formatter = JsonOutputFormatter()
        comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=10,
            commit_id="abc123",
            author="testuser",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            body="Test comment",
            diff_context="+ test line"
        )

        result = formatter._format_review_comment(comment)

        assert result["id"] == 1
        assert result["path"] == "test.py"
        assert result["user"] == "testuser"
        assert result["body"] == "Test comment"

    def test__group_comments_by_file_正常グループ化_ファイルごとの辞書が返される(self):
        """Test _group_comments_by_file groups comments by file path."""
        formatter = JsonOutputFormatter()
        comment1 = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=10,
            commit_id="abc123",
            author="user1",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            body="Comment 1",
            diff_context="+ line 1"
        )
        comment2 = ReviewComment(
            comment_id=2,
            file_path="test.py",
            position=20,
            commit_id="def456",
            author="user2",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            body="Comment 2",
            diff_context="+ line 2"
        )
        comment3 = ReviewComment(
            comment_id=3,
            file_path="other.py",
            position=5,
            commit_id="ghi789",
            author="user3",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            body="Comment 3",
            diff_context="+ line 3"
        )

        result = formatter._group_comments_by_file([comment1, comment2, comment3])

        assert "test.py" in result
        assert "other.py" in result
        assert len(result["test.py"]) == 2
        assert len(result["other.py"]) == 1