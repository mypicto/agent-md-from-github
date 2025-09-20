"""
Tests for ServiceFactory.
"""

import logging
from unittest.mock import patch, MagicMock
from scripts.src.infrastructure.service_factory import ServiceFactory


class TestServiceFactory:
    """Test cases for ServiceFactory."""

    def test_create_pr_collection_service_正常作成_サービスが作成される(self):
        """Test create_pr_collection_service creates service correctly."""
        with patch('scripts.src.infrastructure.service_factory.Github') as mock_github_class, \
             patch('scripts.src.infrastructure.service_factory.TimezoneConverter') as mock_timezone_class, \
             patch('scripts.src.infrastructure.service_factory.GitHubRepository') as mock_github_repo_class, \
             patch('scripts.src.infrastructure.service_factory.PullRequestMetadataRepository') as mock_pr_repo_class, \
             patch('scripts.src.infrastructure.service_factory.AICommentFilter') as mock_filter_class, \
             patch('scripts.src.infrastructure.service_factory.PRReviewCollectionService') as mock_service_class:

            # Setup mock instances
            mock_github_instance = MagicMock()
            mock_github_class.return_value = mock_github_instance

            mock_timezone_instance = MagicMock()
            mock_timezone_class.return_value = mock_timezone_instance

            mock_github_repo_instance = MagicMock()
            mock_github_repo_class.return_value = mock_github_repo_instance

            mock_pr_repo_instance = MagicMock()
            mock_pr_repo_class.return_value = mock_pr_repo_instance

            mock_filter_instance = MagicMock()
            mock_filter_class.return_value = mock_filter_instance

            mock_service_instance = MagicMock()
            mock_service_class.return_value = mock_service_instance

            # Call the method
            service = ServiceFactory.create_pr_collection_service("token", "UTC")

            # Assertions
            assert service == mock_service_instance
            mock_github_class.assert_called_once_with("token")
            mock_timezone_class.assert_called_once_with("UTC")
            mock_github_repo_class.assert_called_once_with(mock_github_instance, mock_timezone_instance)
            mock_pr_repo_class.assert_called_once_with()  # PullRequestMetadataRepository()
            mock_filter_class.assert_called_once()
            mock_service_class.assert_called_once_with(
                github_repository=mock_github_repo_instance,
                pr_metadata_repository=mock_pr_repo_instance,
                comment_filter=mock_filter_instance
            )

    def test_setup_logging_verboseモード_デバッグレベルが設定される(self):
        """Test setup_logging sets debug level when verbose is True."""
        logger = ServiceFactory.setup_logging(verbose=True)
        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_setup_logging_通常モード_情報レベルが設定される(self):
        """Test setup_logging sets info level when verbose is False."""
        logger = ServiceFactory.setup_logging(verbose=False)
        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO

    def test_create_missing_summaries_service_正常作成_サービスが作成される(self):
        """Test create_missing_summaries_service creates service correctly."""
        with patch('scripts.src.infrastructure.service_factory.PullRequestMetadataRepository') as mock_metadata_repo_class:
            with patch('scripts.src.infrastructure.service_factory.SummaryRepository') as mock_summary_repo_class:
                with patch('scripts.src.infrastructure.service_factory.MissingSummariesService') as mock_service_class:
                    mock_metadata_repo_instance = MagicMock()
                    mock_metadata_repo_class.return_value = mock_metadata_repo_instance
                    
                    mock_summary_repo_instance = MagicMock()
                    mock_summary_repo_class.return_value = mock_summary_repo_instance

                    mock_service_instance = MagicMock()
                    mock_service_class.return_value = mock_service_instance

                    service = ServiceFactory.create_missing_summaries_service()

                    assert service == mock_service_instance
                    mock_metadata_repo_class.assert_called_once()
                    mock_summary_repo_class.assert_called_once()
                    mock_service_class.assert_called_once_with(mock_metadata_repo_instance, mock_summary_repo_instance)

    def test_create_review_summary_service_正常作成_サービスが作成される(self):
        """Test create_review_summary_service creates service correctly."""
        with patch('scripts.src.infrastructure.service_factory.SummaryRepository') as mock_summary_repo_class:
            with patch('scripts.src.infrastructure.service_factory.PullRequestMetadataRepository') as mock_metadata_repo_class:
                with patch('scripts.src.infrastructure.service_factory.ReviewSummaryService') as mock_service_class:
                    mock_summary_repo_instance = MagicMock()
                    mock_summary_repo_class.return_value = mock_summary_repo_instance
                    
                    mock_metadata_repo_instance = MagicMock()
                    mock_metadata_repo_class.return_value = mock_metadata_repo_instance

                    mock_service_instance = MagicMock()
                    mock_service_class.return_value = mock_service_instance

                    service = ServiceFactory.create_review_summary_service()

                    assert service == mock_service_instance
                    mock_summary_repo_class.assert_called_once()
                    mock_metadata_repo_class.assert_called_once()
                    mock_service_class.assert_called_once_with(mock_summary_repo_instance, mock_metadata_repo_instance)