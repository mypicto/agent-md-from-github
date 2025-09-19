"""
Test for CommentThread value object.
"""

import pytest
from datetime import datetime
from scripts.src.domain.comment_thread import CommentThread
from scripts.src.domain.review_comment import ReviewComment


class TestCommentThread:
    """Test cases for CommentThread."""

    def test_CommentThread_インスタンス化_属性が正しく設定される(self):
        # Arrange
        comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=10,
            commit_id="abc123",
            author="testuser",
            created_at=datetime(2023, 1, 1),
            body="Test comment",
            diff_context="+ line"
        )
        comments = [comment]

        # Act
        thread = CommentThread(
            file_path="test.py",
            position=10,
            comments=comments
        )

        # Assert
        assert thread.file_path == "test.py"
        assert thread.position == 10
        assert thread.comments == comments

    def test_CommentThread_空のコメントリスト_正常に作成される(self):
        # Act
        thread = CommentThread(
            file_path="test.py",
            position=None,
            comments=[]
        )

        # Assert
        assert thread.file_path == "test.py"
        assert thread.position is None
        assert thread.comments == []

    def test_CommentThread_frozen_属性変更不可(self):
        # Arrange
        thread = CommentThread(
            file_path="test.py",
            position=10,
            comments=[]
        )

        # Act & Assert
        with pytest.raises(AttributeError):
            thread.file_path = "changed.py"