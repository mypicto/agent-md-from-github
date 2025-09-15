"""
Tests for AICommentFilter.
"""

import unittest
from datetime import datetime
from unittest.mock import Mock

from scripts.src.domain.review_comment import ReviewComment
from scripts.src.infrastructure.filters.ai_comment_filter import AICommentFilter


class TestAICommentFilter(unittest.TestCase):
    """Test cases for AICommentFilter."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.filter = AICommentFilter()
        
        # Create test comments
        self.copilot_comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=1,
            commit_id="abc123",
            author="Copilot",
            created_at=datetime(2025, 9, 15),
            body="This is a Copilot comment",
            diff_context="diff content"
        )
        
        self.github_copilot_comment = ReviewComment(
            comment_id=3,
            file_path="test.py",
            position=3,
            commit_id="ghi789",
            author="GitHub Copilot",
            created_at=datetime(2025, 9, 15),
            body="This is a GitHub Copilot comment",
            diff_context="diff content"
        )
        
        self.ai_assistant_comment = ReviewComment(
            comment_id=4,
            file_path="test.py",
            position=4,
            commit_id="jkl012",
            author="AI Assistant",
            created_at=datetime(2025, 9, 15),
            body="This is an AI Assistant comment",
            diff_context="diff content"
        )
        
        self.human_comment = ReviewComment(
            comment_id=2,
            file_path="test.py",
            position=2,
            commit_id="def456",
            author="human_user",
            created_at=datetime(2025, 9, 15),
            body="This is a human comment",
            diff_context="diff content"
        )
    
    def test_filter_comments_removes_ai_comments(self):
        """Test that AI comments are filtered out."""
        comments = [self.copilot_comment, self.github_copilot_comment, self.ai_assistant_comment, self.human_comment]
        filtered = self.filter.filter_comments(comments)
        
        # Only Copilot is filtered out, GitHub Copilot and AI Assistant are kept
        self.assertEqual(len(filtered), 3)
        authors = [comment.author for comment in filtered]
        self.assertIn("GitHub Copilot", authors)
        self.assertIn("AI Assistant", authors)
        self.assertIn("human_user", authors)
        self.assertNotIn("Copilot", authors)
    
    def test_filter_comments_keeps_human_comments(self):
        """Test that human comments are kept."""
        comments = [self.human_comment]
        filtered = self.filter.filter_comments(comments)
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].author, "human_user")
    
    def test_filter_comments_empty_list(self):
        """Test filtering an empty list."""
        comments = []
        filtered = self.filter.filter_comments(comments)
        
        self.assertEqual(len(filtered), 0)
    
    def test_filter_comments_only_ai_comments(self):
        """Test filtering a list with only AI comments."""
        comments = [self.copilot_comment, self.github_copilot_comment, self.ai_assistant_comment]
        filtered = self.filter.filter_comments(comments)
        
        # Only Copilot is filtered out, GitHub Copilot and AI Assistant are kept
        self.assertEqual(len(filtered), 2)
        authors = [comment.author for comment in filtered]
        self.assertIn("GitHub Copilot", authors)
        self.assertIn("AI Assistant", authors)
        self.assertNotIn("Copilot", authors)
    
    def test_filter_comments_mixed_authors(self):
        """Test filtering with various author types."""
        bot_comment = ReviewComment(
            comment_id=5,
            file_path="test.py",
            position=5,
            commit_id="mno345",
            author="Bot",
            created_at=datetime(2025, 9, 15),
            body="This is a Bot comment",
            diff_context="diff content"
        )
        
        comments = [self.copilot_comment, self.human_comment, bot_comment]
        filtered = self.filter.filter_comments(comments)
        
        # Only Copilot is filtered out, human and Bot comments are kept
        self.assertEqual(len(filtered), 2)
        authors = [comment.author for comment in filtered]
        self.assertIn("human_user", authors)
        self.assertIn("Bot", authors)
        self.assertNotIn("Copilot", authors)


if __name__ == "__main__":
    unittest.main()