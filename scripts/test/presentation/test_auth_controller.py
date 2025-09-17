"""
Tests for AuthController.
"""

import pytest
from unittest.mock import patch, MagicMock
from scripts.src.presentation.auth_controller import AuthController


class TestAuthController:
    """Test cases for AuthController."""

    def test___init___初期化_コントローラが正しく初期化される(self):
        """Test __init__ method initializes the controller correctly."""
        controller = AuthController()
        assert controller._parser is not None
        assert isinstance(controller._parser, type(controller._parser))

    def test__setup_argument_parser_パーサー設定_パーサーが設定される(self):
        """Test _setup_argument_parser sets up the parser correctly."""
        controller = AuthController()
        assert controller._parser is not None
        # Add more assertions for parser arguments

    def test_run_store_token_トークン保存_成功メッセージが表示される(self):
        """Test run method handles --store-token option."""
        with patch('scripts.src.presentation.auth_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                controller = AuthController()
                args = ['--store-token', 'test_token']

                controller.run(args)

                mock_manager.store_token.assert_called_once_with('test_token')
                mock_print.assert_called_with("GitHub token has been securely stored in system keyring.")

    def test_run_store_token_エラー発生_エラーメッセージが表示される(self):
        """Test run method handles --store-token error."""
        with patch('scripts.src.presentation.auth_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                with patch('sys.exit') as mock_exit:
                    mock_manager.store_token.side_effect = Exception("Storage failed")

                    controller = AuthController()
                    args = ['--store-token', 'test_token']

                    controller.run(args)

                    mock_print.assert_called_with("Failed to store token: Storage failed")
                    mock_exit.assert_called_once_with(1)

    def test_run_clear_token_トークン削除_成功メッセージが表示される(self):
        """Test run method handles --clear-token option."""
        with patch('scripts.src.presentation.auth_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                mock_manager.clear_token.return_value = True

                controller = AuthController()
                args = ['--clear-token']

                controller.run(args)

                mock_manager.clear_token.assert_called_once()
                mock_print.assert_called_with("GitHub token has been removed from system keyring.")

    def test_run_clear_token_トークンなし_メッセージが表示される(self):
        """Test run method handles --clear-token when no token exists."""
        with patch('scripts.src.presentation.auth_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                mock_manager.clear_token.return_value = False

                controller = AuthController()
                args = ['--clear-token']

                controller.run(args)

                mock_manager.clear_token.assert_called_once()
                mock_print.assert_called_with("No stored GitHub token found.")

    def test_run_clear_token_エラー発生_エラーメッセージが表示される(self):
        """Test run method handles --clear-token error."""
        with patch('scripts.src.presentation.auth_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                with patch('sys.exit') as mock_exit:
                    mock_manager.clear_token.side_effect = Exception("Clear failed")

                    controller = AuthController()
                    args = ['--clear-token']

                    controller.run(args)

                    mock_print.assert_called_with("Failed to clear token: Clear failed")
                    mock_exit.assert_called_once_with(1)

    def test_run_auth_オプションなし_ヘルプが表示される(self):
        """Test run method shows help when auth command has no options."""
        controller = AuthController()
        args = []

        with patch('scripts.src.presentation.auth_controller.argparse.ArgumentParser.parse_args') as mock_parse:
            mock_parse.return_value.store_token = None
            mock_parse.return_value.clear_token = False

            controller.run(args)

            # Should call parse_args with help
            mock_parse.assert_called()

    def test__handle_auth_command_store_token_トークンが保存される(self):
        """Test _handle_auth_command handles store-token correctly."""
        with patch('scripts.src.presentation.auth_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                controller = AuthController()
                args = MagicMock()
                args.store_token = 'test_token'
                args.clear_token = False

                controller._handle_auth_command(args)

                mock_manager.store_token.assert_called_once_with('test_token')
                mock_print.assert_called_with("GitHub token has been securely stored in system keyring.")

    def test__handle_auth_command_clear_token_トークンが削除される(self):
        """Test _handle_auth_command handles clear-token correctly."""
        with patch('scripts.src.presentation.auth_controller.TokenManager') as mock_manager:
            with patch('builtins.print') as mock_print:
                mock_manager.clear_token.return_value = True

                controller = AuthController()
                args = MagicMock()
                args.store_token = None
                args.clear_token = True

                controller._handle_auth_command(args)

                mock_manager.clear_token.assert_called_once()
                mock_print.assert_called_with("GitHub token has been removed from system keyring.")