"""
Tests for ReviewComment.
"""

from datetime import datetime
from prcollector.src.domain.review_comment import ReviewComment


class TestReviewComment:
    """Test cases for ReviewComment."""

    def test___init___有効な値_正常に初期化される(self):
        """Test __init__ initializes correctly with valid values."""
        created_at = datetime.now()
        comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=10,
            commit_id="abc123",
            author="testuser",
            created_at=created_at,
            body="Test comment",
            diff_context="+ test line"
        )
        assert comment.comment_id == 1
        assert comment.file_path == "test.py"
        assert comment.position == 10
        assert comment.commit_id == "abc123"
        assert comment.author == "testuser"
        assert comment.created_at == created_at
        assert comment.body == "Test comment"
        assert comment.diff_context == "+ test line"