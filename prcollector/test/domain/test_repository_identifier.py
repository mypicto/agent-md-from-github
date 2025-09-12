"""
Tests for RepositoryIdentifier.
"""

import pytest
from prcollector.src.domain.repository_identifier import RepositoryIdentifier


class TestRepositoryIdentifier:
    """Test cases for RepositoryIdentifier."""

    def test___post_init___有効な値_正常に初期化される(self):
        """Test __post_init__ validates correctly for valid values."""
        repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
        assert repo_id.owner == "testowner"
        assert repo_id.name == "testrepo"

    def test___post_init___空のオーナー_ValueErrorが発生する(self):
        """Test __post_init__ raises ValueError for empty owner."""
        with pytest.raises(ValueError):
            RepositoryIdentifier(owner="", name="testrepo")

    def test___post_init___空の名前_ValueErrorが発生する(self):
        """Test __post_init__ raises ValueError for empty name."""
        with pytest.raises(ValueError):
            RepositoryIdentifier(owner="testowner", name="")

    def test_from_string_有効な文字列_RepositoryIdentifierが作成される(self):
        """Test from_string creates RepositoryIdentifier for valid string."""
        repo_string = "testowner/testrepo"
        repo_id = RepositoryIdentifier.from_string(repo_string)
        assert repo_id.owner == "testowner"
        assert repo_id.name == "testrepo"

    def test_from_string_無効な文字列_ValueErrorが発生する(self):
        """Test from_string raises ValueError for invalid string."""
        repo_string = "invalidformat"
        with pytest.raises(ValueError):
            RepositoryIdentifier.from_string(repo_string)

    def test_to_string_正常_文字列が返される(self):
        """Test to_string returns correct string format."""
        repo_id = RepositoryIdentifier(owner="testowner", name="testrepo")
        result = repo_id.to_string()
        assert result == "testowner/testrepo"