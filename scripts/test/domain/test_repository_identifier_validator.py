"""
Tests for RepositoryIdentifierValidator class.
"""

import pytest

from scripts.src.domain.repository_identifier_validator import RepositoryIdentifierValidator
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestRepositoryIdentifierValidator:
    """Test cases for RepositoryIdentifierValidator class."""

    def test_validate_format_valid_repositories(self):
        """有効なリポジトリ形式のバリデーションをテストする."""
        valid_specs = [
            "owner/repo",
            "my-org/my-project", 
            "user123/project-name",
            "org/repo_with_underscores",
            "company/project.with.dots"
        ]
        
        for spec in valid_specs:
            assert RepositoryIdentifierValidator.validate_format(spec), f"Failed for: {spec}"

    def test_validate_format_invalid_repositories(self):
        """無効なリポジトリ形式のバリデーションをテストする."""
        invalid_specs = [
            "",
            "invalid",
            "owner/",
            "/repo",
            "owner//repo",
            "owner/repo/extra",
            "-invalid/repo",
            "owner/-invalid",
            "owner/repo-",
            "o" * 40 + "/repo",  # owner too long
            "owner/" + "r" * 101,  # repo too long
            "owner/.repo",  # repo starts with dot
        ]
        
        for spec in invalid_specs:
            assert not RepositoryIdentifierValidator.validate_format(spec), f"Should fail for: {spec}"

    def test_validate_format_none_and_non_string(self):
        """None値と非文字列値のバリデーションをテストする."""
        assert not RepositoryIdentifierValidator.validate_format(None)
        assert not RepositoryIdentifierValidator.validate_format(123)
        assert not RepositoryIdentifierValidator.validate_format([])

    def test_parse_repository_spec_valid(self):
        """有効なリポジトリ仕様の解析をテストする."""
        spec = "owner/repo"
        result = RepositoryIdentifierValidator.parse_repository_spec(spec)
        
        assert isinstance(result, RepositoryIdentifier)
        assert result.owner == "owner"
        assert result.name == "repo"

    def test_parse_repository_spec_invalid(self):
        """無効なリポジトリ仕様の解析でValueErrorが発生することをテストする."""
        invalid_specs = [
            "invalid",
            "owner/",
            "/repo",
            "",
        ]
        
        for spec in invalid_specs:
            with pytest.raises(ValueError, match="Invalid repository specification format"):
                RepositoryIdentifierValidator.parse_repository_spec(spec)

    def test_owner_validation_edge_cases(self):
        """オーナー名のバリデーションのエッジケースをテストする."""
        # Maximum length (39 characters)
        max_owner = "a" * 39
        assert RepositoryIdentifierValidator.validate_format(f"{max_owner}/repo")
        
        # Over maximum length (40 characters)
        over_max_owner = "a" * 40
        assert not RepositoryIdentifierValidator.validate_format(f"{over_max_owner}/repo")
        
        # Single character
        assert RepositoryIdentifierValidator.validate_format("a/repo")
        
        # Two characters with hyphen
        assert RepositoryIdentifierValidator.validate_format("a-b/repo")

    def test_repository_validation_edge_cases(self):
        """リポジトリ名のバリデーションのエッジケースをテストする."""
        # Maximum length (100 characters)
        max_repo = "a" * 100
        assert RepositoryIdentifierValidator.validate_format(f"owner/{max_repo}")
        
        # Over maximum length (101 characters)
        over_max_repo = "a" * 101
        assert not RepositoryIdentifierValidator.validate_format(f"owner/{over_max_repo}")
        
        # Single character
        assert RepositoryIdentifierValidator.validate_format("owner/a")
        
        # Various allowed characters
        assert RepositoryIdentifierValidator.validate_format("owner/repo-name_with.dots")