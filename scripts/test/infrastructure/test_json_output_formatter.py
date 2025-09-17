"""
Tests for JsonOutputFormatter.
"""

import json
from datetime import datetime
from scripts.src.infrastructure.json_output_formatter import JsonOutputFormatter
from scripts.src.domain.pull_request_metadata import PullRequestMetadata
from scripts.src.domain.review_comment import ReviewComment
from scripts.src.domain.repository_identifier import RepositoryIdentifier


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
