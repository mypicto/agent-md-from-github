"""
Tests for CLIController.
"""

import argparse
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock
from prcollector.src.presentation.cli_controller import CLIController, parse_date


class TestCLIController:
    """Test cases for CLIController."""

    def test___init___初期化_コントローラが正しく初期化される(self):
        """Test __init__ method initializes the controller correctly."""
        controller = CLIController()
        assert controller._parser is not None
        assert isinstance(controller._parser, type(controller._parser))

    def test__setup_argument_parser_パーサー設定_パーサーが設定される(self):
        """Test _setup_argument_parser sets up the parser correctly."""
        controller = CLIController()
        assert controller._parser is not None
        # Add more assertions for parser arguments

    def test_run_正常実行_レビューコメントが収集される(self):
        """Test run method executes successfully."""
        # Mock dependencies
        with patch('prcollector.src.presentation.cli_controller.ServiceFactory') as mock_factory:
            mock_logger = MagicMock()
            mock_service = MagicMock()
            mock_factory.setup_logging.return_value = mock_logger
            mock_factory.create_pr_collection_service.return_value = mock_service

            controller = CLIController()
            args = ['--repo', 'owner/repo', '--from-date', '2023-01-01', '--to-date', '2023-01-02', '--token', 'test_token']

            controller.run(args)

            mock_service.collect_review_comments.assert_called_once()

    def test_run_エラー発生_適切なエラーメッセージが表示される(self):
        """Test run method handles errors appropriately."""
        controller = CLIController()
        args = ['--repo', 'owner/repo', '--from-date', '2023-01-01', '--to-date', '2023-01-02']

        with patch('builtins.print') as mock_print:
            with patch('prcollector.src.presentation.cli_controller.ServiceFactory') as mock_factory:
                mock_factory.setup_logging.side_effect = Exception("Test error")

                with pytest.raises(SystemExit):
                    controller.run(args)

                mock_print.assert_called()

    def test__get_github_token_トークン提供_トークンが返される(self):
        """Test _get_github_token returns token when provided."""
        controller = CLIController()
        token = controller._get_github_token("test_token")
        assert token == "test_token"

    def test__get_github_token_トークンなし_ValueErrorが発生する(self):
        """Test _get_github_token raises ValueError when no token."""
        controller = CLIController()
        with pytest.raises(ValueError):
            controller._get_github_token(None)

    def test__create_date_range_有効な日付範囲_DateRangeが作成される(self):
        """Test _create_date_range creates DateRange for valid dates."""
        controller = CLIController()
        args = MagicMock()
        args.from_date = datetime(2023, 1, 1)
        args.to_date = datetime(2023, 1, 2)

        with patch('prcollector.src.presentation.cli_controller.TimezoneConverter') as mock_converter:
            mock_converter_instance = MagicMock()
            mock_converter.return_value = mock_converter_instance
            mock_converter_instance.localize_date_range.return_value = (args.from_date, args.to_date)

            date_range = controller._create_date_range(args, "Asia/Tokyo")

            assert date_range is not None

    def test__create_date_range_無効な日付範囲_ValueErrorが発生する(self):
        """Test _create_date_range raises ValueError for invalid date range."""
        controller = CLIController()
        args = MagicMock()
        args.from_date = datetime(2023, 1, 2)
        args.to_date = datetime(2023, 1, 1)

        with pytest.raises(ValueError):
            controller._create_date_range(args, "Asia/Tokyo")


class TestParseDate:
    """Test cases for parse_date function."""

    def test_parse_date_有効な日付文字列_datetimeオブジェクトが返される(self):
        """Test parse_date parses valid date string."""
        date_str = "2023-01-01"
        result = parse_date(date_str)
        assert result == datetime(2023, 1, 1)

    def test_parse_date_無効な日付文字列_ArgumentTypeErrorが発生する(self):
        """Test parse_date raises ArgumentTypeError for invalid date."""
        date_str = "invalid-date"
        with pytest.raises(argparse.ArgumentTypeError):
            parse_date(date_str)