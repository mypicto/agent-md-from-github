"""
Tests for GitHubApiError.
"""

from scripts.src.application.exceptions.github_api_error import GitHubApiError


class TestGitHubApiError:
    """Test cases for GitHubApiError."""

    def test_exception_初期化_例外が正しく初期化される(self):
        """Test that GitHubApiError initializes correctly."""
        error = GitHubApiError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)