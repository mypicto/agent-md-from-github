"""
Secure token management using system keyring.
"""

import keyring
from typing import Optional


class TokenManager:
    """Manages GitHub tokens securely using system keyring."""

    SERVICE_NAME = "prcollector-github"
    USERNAME = "github-token"

    @classmethod
    def store_token(cls, token: str) -> None:
        """Store GitHub token in system keyring.

        Args:
            token: GitHub personal access token to store
        """
        try:
            keyring.set_password(cls.SERVICE_NAME, cls.USERNAME, token)
        except Exception as e:
            raise RuntimeError(f"Failed to store token in keyring: {e}")

    @classmethod
    def get_token(cls) -> Optional[str]:
        """Retrieve GitHub token from system keyring.

        Returns:
            Stored GitHub token, or None if not found
        """
        try:
            return keyring.get_password(cls.SERVICE_NAME, cls.USERNAME)
        except Exception:
            return None

    @classmethod
    def clear_token(cls) -> bool:
        """Remove GitHub token from system keyring.

        Returns:
            True if token was successfully removed, False if not found
        """
        try:
            keyring.delete_password(cls.SERVICE_NAME, cls.USERNAME)
            return True
        except Exception as e:
            # Check if it's a "not found" type error
            if "not found" in str(e).lower() or "delete" in str(e).lower():
                return False
            else:
                raise RuntimeError(f"Failed to clear token from keyring: {e}")

    @classmethod
    def has_token(cls) -> bool:
        """Check if a GitHub token is stored in keyring.

        Returns:
            True if token exists, False otherwise
        """
        return cls.get_token() is not None