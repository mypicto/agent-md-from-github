"""
Tests for PRReviewCollectionError.
"""

from prcollector.src.application.exceptions.pr_review_collection_error import PRReviewCollectionError


class TestPRReviewCollectionError:
    """Test cases for PRReviewCollectionError."""

    def test_exception_初期化_例外が正しく初期化される(self):
        """Test that PRReviewCollectionError initializes correctly."""
        error = PRReviewCollectionError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)