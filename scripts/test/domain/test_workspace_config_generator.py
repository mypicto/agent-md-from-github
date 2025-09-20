"""
Tests for WorkspaceConfigGenerator class.
"""

import pytest
import tempfile
import os
from pathlib import Path
from ruamel.yaml import YAML

from scripts.src.domain.workspace_config_generator import WorkspaceConfigGenerator
from scripts.src.domain.repository_identifier import RepositoryIdentifier


class TestWorkspaceConfigGenerator:
    """Test cases for WorkspaceConfigGenerator class."""

    def test_generate_config_content_simple_repository(self):
        """シンプルなリポジトリの設定コンテンツ生成をテストする."""
        repo_id = RepositoryIdentifier(owner="owner", name="repo")
        result = WorkspaceConfigGenerator.generate_config_content(repo_id)
        
        expected = {
            'workspace': {
                'organization': 'owner',
                'repository': 'repo'
            }
        }
        
        assert result == expected

    def test_generate_config_content_organization_repository(self):
        """組織リポジトリの設定コンテンツ生成をテストする."""
        repo_id = RepositoryIdentifier(owner="my-org", name="my-project")
        result = WorkspaceConfigGenerator.generate_config_content(repo_id)
        
        expected = {
            'workspace': {
                'organization': 'my-org',
                'repository': 'my-project'
            }
        }
        
        assert result == expected

    def test_generate_config_content_special_characters(self):
        """特殊文字を含むリポジトリの設定コンテンツ生成をテストする."""
        repo_id = RepositoryIdentifier(owner="user-name", name="repo_with.dots")
        result = WorkspaceConfigGenerator.generate_config_content(repo_id)
        
        expected = {
            'workspace': {
                'organization': 'user-name',
                'repository': 'repo_with.dots'
            }
        }
        
        assert result == expected

    def test_create_workspace_config_file(self):
        """ワークスペース設定ファイルの作成をテストする."""
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")
        generator = WorkspaceConfigGenerator()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "workspace.yml"
            
            # Create config file
            generator.create_workspace_config_file(repo_id, config_path)
            
            # Verify file exists
            assert config_path.exists()
            
            # Verify content
            yaml_loader = YAML()
            with open(config_path, 'r', encoding='utf-8') as f:
                content = yaml_loader.load(f)
            
            expected = {
                'workspace': {
                    'organization': 'test-owner',
                    'repository': 'test-repo'
                }
            }
            
            assert content == expected

    def test_create_workspace_config_file_creates_parent_directory(self):
        """親ディレクトリが存在しない場合の設定ファイル作成をテストする."""
        repo_id = RepositoryIdentifier(owner="test-owner", name="test-repo")
        generator = WorkspaceConfigGenerator()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use nested path that doesn't exist
            config_path = Path(temp_dir) / "nested" / "workspace.yml"
            
            # Create config file (should create parent directory)
            generator.create_workspace_config_file(repo_id, config_path)
            
            # Verify file and parent directory exist
            assert config_path.exists()
            assert config_path.parent.exists()

    def test_validate_config_content_valid(self):
        """有効な設定コンテンツのバリデーションをテストする."""
        valid_configs = [
            {
                'workspace': {
                    'organization': 'owner',
                    'repository': 'repo'
                }
            },
            {
                'workspace': {
                    'organization': 'my-org',
                    'repository': 'my-project'
                }
            }
        ]
        
        for config in valid_configs:
            assert WorkspaceConfigGenerator.validate_config_content(config)

    def test_validate_config_content_invalid_structure(self):
        """無効な構造の設定コンテンツのバリデーションをテストする."""
        invalid_configs = [
            # Not a dict
            "invalid",
            [],
            None,
            
            # Missing workspace key
            {'other': 'value'},
            
            # workspace is not a dict
            {'workspace': 'invalid'},
            {'workspace': []},
            
            # Missing required fields
            {'workspace': {}},
            {'workspace': {'organization': 'owner'}},
            {'workspace': {'repository': 'repo'}},
            
            # Invalid field types
            {'workspace': {'organization': 123, 'repository': 'repo'}},
            {'workspace': {'organization': 'owner', 'repository': []}},
            
            # Empty values
            {'workspace': {'organization': '', 'repository': 'repo'}},
            {'workspace': {'organization': 'owner', 'repository': ''}},
            {'workspace': {'organization': '   ', 'repository': 'repo'}},
        ]
        
        for config in invalid_configs:
            assert not WorkspaceConfigGenerator.validate_config_content(config), f"Should be invalid: {config}"

    def test_validate_config_content_extra_fields(self):
        """追加フィールドがある設定コンテンツのバリデーションをテストする."""
        # Extra fields should be allowed
        config_with_extra = {
            'workspace': {
                'organization': 'owner',
                'repository': 'repo',
                'extra_field': 'extra_value'
            },
            'other_section': {
                'other_field': 'other_value'
            }
        }
        
        assert WorkspaceConfigGenerator.validate_config_content(config_with_extra)