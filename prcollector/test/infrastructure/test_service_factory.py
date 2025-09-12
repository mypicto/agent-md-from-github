"""
Tests for ServiceFactory.
"""

import pytest
import logging
from unittest.mock import patch, MagicMock
from prcollector.src.infrastructure.service_factory import ServiceFactory


class TestServiceFactory:
    """Test cases for ServiceFactory."""

    def test_create_pr_collection_service_正常作成_サービスが作成される(self):
        """Test create_pr_collection_service creates service correctly."""
        with patch('prcollector.src.infrastructure.service_factory.Github') as mock_github_class:
            with patch('prcollector.src.infrastructure.service_factory.TimezoneConverter') as mock_timezone_class:
                with patch('prcollector.src.infrastructure.service_factory.GitHubRepository') as mock_repo_class:
                    with patch('prcollector.src.infrastructure.service_factory.JsonOutputFormatter') as mock_formatter_class:
                        with patch('prcollector.src.infrastructure.service_factory.FileSystemOutputWriter') as mock_writer_class:
                            with patch('prcollector.src.infrastructure.service_factory.PRReviewCollectionService') as mock_service_class:

                                mock_github_instance = MagicMock()
                                mock_github_class.return_value = mock_github_instance

                                mock_timezone_instance = MagicMock()
                                mock_timezone_class.return_value = mock_timezone_instance

                                mock_repo_instance = MagicMock()
                                mock_repo_class.return_value = mock_repo_instance

                                mock_formatter_instance = MagicMock()
                                mock_formatter_class.return_value = mock_formatter_instance

                                mock_writer_instance = MagicMock()
                                mock_writer_class.return_value = mock_writer_instance

                                mock_service_instance = MagicMock()
                                mock_service_class.return_value = mock_service_instance

                                service = ServiceFactory.create_pr_collection_service("token", "Asia/Tokyo")

                                assert service == mock_service_instance
                                mock_github_class.assert_called_once_with("token")
                                mock_timezone_class.assert_called_once_with("Asia/Tokyo")
                                mock_repo_class.assert_called_once_with(mock_github_instance, mock_timezone_instance)
                                mock_formatter_class.assert_called_once()
                                mock_writer_class.assert_called_once()
                                mock_service_class.assert_called_once_with(
                                    github_repository=mock_repo_instance,
                                    output_formatter=mock_formatter_instance,
                                    output_writer=mock_writer_instance
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