"""
Tests for PullRequestMetadata.
"""

import pytest
from datetime import datetime
from prcollector.src.domain.pull_request_metadata import PullRequestMetadata
from prcollector.src.domain.review_comment import ReviewComment


class TestPullRequestMetadata:
    """Test cases for PullRequestMetadata."""

    def test_has_review_comments_コメントあり_Trueが返される(self):
        """Test has_review_comments returns True when comments exist."""
        comment = ReviewComment(
            comment_id=1,
            file_path="test.py",
            position=10,
            commit_id="abc123",
            author="testuser",
            created_at=datetime.now(),
            body="Test comment",
            diff_context="+ test line"
        )
        pr = PullRequestMetadata(
            number=1,
            title="Test PR",
            closed_at=datetime.now(),
            is_merged=True,
            review_comments=[comment]
        )
        assert pr.has_review_comments() is True

    def test_has_review_comments_コメントなし_Falseが返される(self):
        """Test has_review_comments returns False when no comments."""
        pr = PullRequestMetadata(
            number=1,
            title="Test PR",
            closed_at=datetime.now(),
            is_merged=True,
            review_comments=[]
        )
        assert pr.has_review_comments() is False