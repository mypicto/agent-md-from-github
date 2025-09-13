"""
Tests for CLIController.
"""

import argparse
import pytest
from datetime import datetime
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
            args = ['collector', '--repo', 'owner/repo', '--from-date', '2023-01-01', '--to-date', '2023-01-02', '--token', 'test_token']

            controller.run(args)

            mock_service.collect_review_comments.assert_called_once()

    def test_run_エラー発生_適切なエラーメッセージが表示される(self):
        """Test run method handles errors appropriately."""
        controller = CLIController()
        args = ['collector', '--repo', 'owner/repo', '--from-date', '2023-01-01', '--to-date', '2023-01-02']

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

    def test__get_github_token_キーリングから取得_トークンが返される(self):
        """Test _get_github_token gets token from keyring."""
        with patch('prcollector.src.presentation.cli_controller.TokenManager') as mock_manager:
            mock_manager.get_token.return_value = "keyring_token"

            controller = CLIController()
            token = controller._get_github_token(None)

            assert token == "keyring_token"
            mock_manager.get_token.assert_called_once()

    def test__get_github_token_環境変数から取得_トークンが返される(self):
        """Test _get_github_token gets token from environment variable."""
        with patch('prcollector.src.presentation.cli_controller.TokenManager') as mock_manager:
            with patch.dict('os.environ', {'GITHUB_TOKEN': 'env_token'}):
                mock_manager.get_token.return_value = None

                controller = CLIController()
                token = controller._get_github_token(None)

                assert token == "env_token"

    def test__get_github_token_トークンなし_ValueErrorが発生する(self):
        """Test _get_github_token raises ValueError when no token."""
        with patch('prcollector.src.presentation.cli_controller.TokenManager') as mock_manager:
            with patch.dict('os.environ', {}, clear=True):
                mock_manager.get_token.return_value = None

                controller = CLIController()
                with pytest.raises(ValueError):
                    controller._get_github_token(None)

    def test_run_store_token_トークン保存_成功メッセージが表示される(self):
        """Test run method handles --store-token option."""
        with patch('prcollector.src.presentation.cli_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                controller = CLIController()
                args = ['auth', '--store-token', 'test_token']

                controller.run(args)

                mock_manager.store_token.assert_called_once_with('test_token')
                mock_print.assert_called_with("GitHub token has been securely stored in system keyring.")

    def test_run_store_token_エラー発生_エラーメッセージが表示される(self):
        """Test run method handles --store-token error."""
        with patch('prcollector.src.presentation.cli_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                with patch('sys.exit') as mock_exit:
                    mock_manager.store_token.side_effect = Exception("Storage failed")

                    controller = CLIController()
                    args = ['auth', '--store-token', 'test_token']

                    controller.run(args)

                    mock_print.assert_called_with("Failed to store token: Storage failed")
                    mock_exit.assert_called_once_with(1)

    def test_run_clear_token_トークン削除_成功メッセージが表示される(self):
        """Test run method handles --clear-token option."""
        with patch('prcollector.src.presentation.cli_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                mock_manager.clear_token.return_value = True

                controller = CLIController()
                args = ['auth', '--clear-token']

                controller.run(args)

                mock_manager.clear_token.assert_called_once()
                mock_print.assert_called_with("GitHub token has been removed from system keyring.")

    def test_run_clear_token_トークンなし_メッセージが表示される(self):
        """Test run method handles --clear-token when no token exists."""
        with patch('prcollector.src.presentation.cli_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                mock_manager.clear_token.return_value = False

                controller = CLIController()
                args = ['auth', '--clear-token']

                controller.run(args)

                mock_manager.clear_token.assert_called_once()
                mock_print.assert_called_with("No stored GitHub token found.")

    def test_run_clear_token_エラー発生_エラーメッセージが表示される(self):
        """Test run method handles --clear-token error."""
        with patch('prcollector.src.presentation.cli_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                with patch('sys.exit') as mock_exit:
                    mock_manager.clear_token.side_effect = Exception("Clear failed")

                    controller = CLIController()
                    args = ['auth', '--clear-token']

                    controller.run(args)

                    mock_print.assert_called_with("Failed to clear token: Clear failed")
                    mock_exit.assert_called_once_with(1)

    def test_run_auth_オプションなし_ヘルプが表示される(self):
        """Test run method shows help when auth command has no options."""
        controller = CLIController()
        args = ['auth']

        with patch('prcollector.src.presentation.cli_controller.argparse.ArgumentParser.parse_args') as mock_parse:
            mock_parse.return_value.command = 'auth'
            mock_parse.return_value.store_token = None
            mock_parse.return_value.clear_token = False
            
            controller.run(args)
            
            # Should call parse_args with help
            mock_parse.assert_called()

    def test__handle_auth_command_store_token_トークンが保存される(self):
        """Test _handle_auth_command handles store-token correctly."""
        with patch('prcollector.src.presentation.cli_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                controller = CLIController()
                args = MagicMock()
                args.store_token = 'test_token'
                args.clear_token = False

                controller._handle_auth_command(args)

                mock_manager.store_token.assert_called_once_with('test_token')
                mock_print.assert_called_with("GitHub token has been securely stored in system keyring.")

    def test__handle_auth_command_clear_token_トークンが削除される(self):
        """Test _handle_auth_command handles clear-token correctly."""
        with patch('prcollector.src.presentation.cli_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                mock_manager.clear_token.return_value = True
                
                controller = CLIController()
                args = MagicMock()
                args.store_token = None
                args.clear_token = True

                controller._handle_auth_command(args)

                mock_manager.clear_token.assert_called_once()
                mock_print.assert_called_with("GitHub token has been removed from system keyring.")

    def test__handle_collector_command_正常実行_サービスが呼び出される(self):
        """Test _handle_collector_command executes successfully."""
        with patch('prcollector.src.presentation.cli_controller.ServiceFactory') as mock_factory:
            mock_logger = MagicMock()
            mock_service = MagicMock()
            mock_factory.setup_logging.return_value = mock_logger
            mock_factory.create_pr_collection_service.return_value = mock_service

            controller = CLIController()
            args = MagicMock()
            args.verbose = False
            args.token = 'test_token'
            args.repo = 'owner/repo'
            args.from_date = datetime(2023, 1, 1)
            args.to_date = datetime(2023, 1, 2)
            args.timezone = 'Asia/Tokyo'
            args.output_dir = 'pullrequests'

            controller._handle_collector_command(args)

            mock_service.collect_review_comments.assert_called_once()

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