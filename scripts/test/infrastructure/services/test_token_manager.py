"""
Tests for TokenManager.
"""

import unittest
from unittest.mock import patch, MagicMock

from scripts.src.infrastructure.services.token_manager import TokenManager


class TestTokenManager(unittest.TestCase):
    """Test cases for TokenManager."""

    def setUp(self):
        """Set up test fixtures."""
        # Clear any existing token before each test
        try:
            TokenManager.clear_token()
        except:
            pass

    def tearDown(self):
        """Clean up after each test."""
        # Clear any token after each test
        try:
            TokenManager.clear_token()
        except:
            pass

    @patch('scripts.src.infrastructure.services.token_manager.keyring')
    def test_store_token_成功時_トークンが保存される(self, mock_keyring):
        """Test successful token storage."""
        mock_keyring.set_password = MagicMock()

        TokenManager.store_token("test-token")

        mock_keyring.set_password.assert_called_once_with(
            TokenManager.SERVICE_NAME,
            TokenManager.USERNAME,
            "test-token"
        )

    @patch('scripts.src.infrastructure.services.token_manager.keyring')
    def test_store_token_失敗時_例外が発生する(self, mock_keyring):
        """Test token storage failure."""
        mock_keyring.set_password.side_effect = Exception("Storage failed")

        with self.assertRaises(RuntimeError) as context:
            TokenManager.store_token("test-token")

        self.assertIn("Failed to store token", str(context.exception))

    @patch('scripts.src.infrastructure.services.token_manager.keyring')
    def test_get_token_成功時_トークンが返される(self, mock_keyring):
        """Test successful token retrieval."""
        mock_keyring.get_password.return_value = "stored-token"

        result = TokenManager.get_token()

        self.assertEqual(result, "stored-token")
        mock_keyring.get_password.assert_called_once_with(
            TokenManager.SERVICE_NAME,
            TokenManager.USERNAME
        )

    @patch('scripts.src.infrastructure.services.token_manager.keyring')
    def test_get_token_見つからない場合_Noneが返される(self, mock_keyring):
        """Test token retrieval when not found."""
        mock_keyring.get_password.return_value = None

        result = TokenManager.get_token()

        self.assertIsNone(result)

    @patch('scripts.src.infrastructure.services.token_manager.keyring')
    def test_get_token_例外発生時_Noneが返される(self, mock_keyring):
        """Test token retrieval with exception."""
        mock_keyring.get_password.side_effect = Exception("Retrieval failed")

        result = TokenManager.get_token()

        self.assertIsNone(result)

    @patch('scripts.src.infrastructure.services.token_manager.keyring')
    def test_clear_token_成功時_Trueが返される(self, mock_keyring):
        """Test successful token clearing."""
        mock_keyring.delete_password = MagicMock()

        result = TokenManager.clear_token()

        self.assertTrue(result)
        mock_keyring.delete_password.assert_called_once_with(
            TokenManager.SERVICE_NAME,
            TokenManager.USERNAME
        )

    @patch('scripts.src.infrastructure.services.token_manager.keyring')
    def test_clear_token_見つからない場合_Falseが返される(self, mock_keyring):
        """Test token clearing when not found."""
        mock_keyring.delete_password.side_effect = Exception("Password not found")

        result = TokenManager.clear_token()

        self.assertFalse(result)

    @patch('scripts.src.infrastructure.services.token_manager.keyring')
    def test_clear_token_例外発生時_例外が発生する(self, mock_keyring):
        """Test token clearing with exception."""
        mock_keyring.delete_password.side_effect = Exception("Clear failed")

        with self.assertRaises(RuntimeError) as context:
            TokenManager.clear_token()

        self.assertIn("Failed to clear token", str(context.exception))

    @patch('scripts.src.infrastructure.services.token_manager.keyring')
    def test_has_token_トークン存在時_Trueが返される(self, mock_keyring):
        """Test has_token when token exists."""
        mock_keyring.get_password.return_value = "stored-token"

        result = TokenManager.has_token()

        self.assertTrue(result)

    @patch('scripts.src.infrastructure.services.token_manager.keyring')
    def test_has_token_トークン不存在時_Falseが返される(self, mock_keyring):
        """Test has_token when token doesn't exist."""
        mock_keyring.get_password.return_value = None

        result = TokenManager.has_token()

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()