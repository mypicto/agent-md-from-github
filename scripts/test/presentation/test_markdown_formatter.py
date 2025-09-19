"""
Test for MarkdownFormatter.
"""

from datetime import datetime

from scripts.src.presentation.markdown_formatter import MarkdownFormatter
from scripts.src.domain.comment_thread import CommentThread
from scripts.src.domain.review_comment import ReviewComment


class TestMarkdownFormatter:
    """Test cases for MarkdownFormatter."""

    def test_format_スレッドがある_正しいMarkdownが生成される(self):
        # Arrange
        comment1 = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=10,
            commit_id="abc",
            author="user1",
            created_at=datetime(2023, 1, 1),
            body="First comment",
            diff_context="+ added line"
        )
        comment2 = ReviewComment(
            comment_id=2,
            file_path="test.py",
            position=10,
            commit_id="abc",
            author="user2",
            created_at=datetime(2023, 1, 2),
            body="Second comment",
            diff_context=""
        )
        
        thread = CommentThread(
            file_path="test.py",
            position=10,
            comments=[comment1, comment2]
        )
        
        formatter = MarkdownFormatter()
        
        # Act
        result = formatter.format(123, [thread])
        
        # Assert
        assert "## test.py" in result
        assert "```diff" in result
        assert "+ added line" in result
        assert "- **user1**: First comment" in result
        assert "- **user2**: Second comment" in result

    def test_format_空のスレッドリスト_空文字列が返される(self):
        # Arrange
        formatter = MarkdownFormatter()
        
        # Act
        result = formatter.format(123, [])
        
        # Assert
        assert result == "# PR-123 Review Comments"

    def test_format_diff_contextなし_コードブロックなし(self):
        # Arrange
        comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=10,
            commit_id="abc",
            author="user1",
            created_at=datetime(2023, 1, 1),
            body="Comment",
            diff_context=""
        )
        
        thread = CommentThread(
            file_path="test.py",
            position=10,
            comments=[comment]
        )
        
        formatter = MarkdownFormatter()
        
        # Act
        result = formatter.format(123, [thread])
        
        # Assert
        assert "```diff" not in result