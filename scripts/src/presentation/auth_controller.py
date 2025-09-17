"""
Auth controller for GitHub authentication token management.
"""

import argparse
import sys

from ..infrastructure.services.token_manager import TokenManager


class AuthController:
    """Controller for GitHub authentication token management."""

    def __init__(self):
        """Initialize auth controller."""
        self._setup_argument_parser()

    def _setup_argument_parser(self) -> None:
        """Setup command-line argument parser."""
        self._parser = argparse.ArgumentParser(
            description="GitHub Authentication Token Manager",
            prog="auth"
        )

        self._setup_auth_arguments(self._parser)

    def _setup_auth_arguments(self, parser) -> None:
        """Setup arguments for auth command."""
        parser.add_argument(
            "--store-token",
            help="Store GitHub token securely in system keyring"
        )

        parser.add_argument(
            "--clear-token",
            action="store_true",
            help="Remove stored GitHub token from system keyring"
        )

    def run(self, args: list[str] = None) -> None:
        """Run the auth application.

        Args:
            args: Command-line arguments (defaults to sys.argv)
        """
        parsed_args = self._parser.parse_args(args)
        self._handle_auth_command(parsed_args)

    def _handle_auth_command(self, parsed_args) -> None:
        """Handle authentication-related commands."""
        if parsed_args.store_token:
            self._handle_store_token(parsed_args.store_token)
        elif parsed_args.clear_token:
            self._handle_clear_token()
        else:
            self._parser.parse_args(["--help"])

    def _handle_store_token(self, token: str) -> None:
        """Handle token storage command.

        Args:
            token: Token to store
        """
        try:
            TokenManager.store_token(token)
            print("GitHub token has been securely stored in system keyring.")
        except Exception as e:
            print(f"Failed to store token: {e}")
            sys.exit(1)

    def _handle_clear_token(self) -> None:
        """Handle token clearing command."""
        try:
            if TokenManager.clear_token():
                print("GitHub token has been removed from system keyring.")
            else:
                print("No stored GitHub token found.")
        except Exception as e:
            print(f"Failed to clear token: {e}")
            sys.exit(1)