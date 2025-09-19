"""
Test for PopCommentsService.
"""

import unittest
from unittest.mock import MagicMock

from scripts.src.application.services.pop_comments_service import PopCommentsService


class TestPopCommentsService(unittest.TestCase):
    """Test cases for PopCommentsService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.missing_summaries_service = MagicMock()
        self.comments_service = MagicMock()
        self.service = PopCommentsService(
            self.missing_summaries_service,
            self.comments_service
        )
    
    def test_get_next_missing_comments_markdown_正常系_欠落PRあり(self):
        """正常系: 欠落PRがある場合のテスト"""
        # Arrange
        self.missing_summaries_service.list_missing_summaries.return_value = [123, 456]
        self.comments_service.get_comments_markdown.return_value = "# PR-123 Comments\n\nSome comments..."
        
        # Act
        result = self.service.get_next_missing_comments_markdown(MagicMock(), MagicMock())
        
        # Assert
        self.assertEqual(result, "# PR-123 Comments\n\nSome comments...")
        self.comments_service.get_comments_markdown.assert_called_once()
    
    def test_get_next_missing_comments_markdown_正常系_欠落PRなし(self):
        """正常系: 欠落PRがない場合のテスト"""
        # Arrange
        self.missing_summaries_service.list_missing_summaries.return_value = []
        
        # Act
        result = self.service.get_next_missing_comments_markdown(MagicMock(), MagicMock())
        
        # Assert
        self.assertEqual(result, "No missing summaries found.")
        self.comments_service.get_comments_markdown.assert_not_called()