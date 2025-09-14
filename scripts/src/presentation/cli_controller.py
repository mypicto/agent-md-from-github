"""
Command-line interface controller.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from ..application.exceptions.pr_review_collection_error import PRReviewCollectionError
from ..domain.date_range import DateRange
from ..domain.repository_identifier import RepositoryIdentifier
from ..infrastructure.service_factory import ServiceFactory
from ..infrastructure.services.timezone_converter import TimezoneConverter
from ..infrastructure.services.token_manager import TokenManager


def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format.
    
    Args:
        date_str: Date string
        
    Returns:
        datetime object
        
    Raises:
        argparse.ArgumentTypeError: If date format is invalid
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")


class CLIController:
    """Command-line interface controller."""
    
    def __init__(self):
        """Initialize CLI controller."""
        self._setup_argument_parser()
    
    def _setup_argument_parser(self) -> None:
        """Setup command-line argument parser with subcommands."""
        self._parser = argparse.ArgumentParser(
            description="GitHub PR Review Comments Collector",
            prog="prcollector"
        )
        
        # Create subparsers
        subparsers = self._parser.add_subparsers(
            dest="command",
            help="Available commands",
            required=True
        )
        
        # Collector command
        collector_parser = subparsers.add_parser(
            "collector",
            help="Collect GitHub PR review comments and diffs"
        )
        self._setup_collector_arguments(collector_parser)
        
        # Auth command
        auth_parser = subparsers.add_parser(
            "auth",
            help="Manage GitHub authentication tokens"
        )
        self._setup_auth_arguments(auth_parser)
    
    def _setup_collector_arguments(self, parser) -> None:
        """Setup arguments for collector command."""
        parser.add_argument(
            "--repo",
            required=True,
            help="Repository name in format 'owner/repo'"
        )
        
        parser.add_argument(
            "--from-date",
            type=parse_date,
            required=True,
            help="Start date (inclusive) in YYYY-MM-DD format"
        )
        
        parser.add_argument(
            "--to-date",
            type=parse_date,
            required=True,
            help="End date (inclusive) in YYYY-MM-DD format"
        )
        
        parser.add_argument(
            "--output-dir",
            default="pullrequests",
            help="Output directory (default: pullrequests)"
        )
        
        parser.add_argument(
            "--timezone",
            default="Asia/Tokyo",
            help="Timezone for date filtering (default: Asia/Tokyo)"
        )
        
        parser.add_argument(
            "--token",
            help="GitHub personal access token (or set GITHUB_TOKEN environment variable)"
        )
        
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Enable verbose logging"
        )
    
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
        """Run the CLI application.
        
        Args:
            args: Command-line arguments (defaults to sys.argv)
        """
        parsed_args = self._parser.parse_args(args)
        
        # Handle auth commands
        if parsed_args.command == "auth":
            self._handle_auth_command(parsed_args)
            return
        
        # Handle collector command
        if parsed_args.command == "collector":
            self._handle_collector_command(parsed_args)
            return
    
    def _handle_auth_command(self, parsed_args) -> None:
        """Handle authentication-related commands."""
        if parsed_args.store_token:
            self._handle_store_token(parsed_args.store_token)
        elif parsed_args.clear_token:
            self._handle_clear_token()
        else:
            self._parser.parse_args(["auth", "--help"])
    
    def _handle_collector_command(self, parsed_args) -> None:
        """Handle PR collection command."""
        try:
            # Setup logging
            logger = ServiceFactory.setup_logging(parsed_args.verbose)
            
            # Validate and extract arguments
            github_token = self._get_github_token(parsed_args.token)
            repository_id = RepositoryIdentifier.from_string(parsed_args.repo)
            date_range = self._create_date_range(parsed_args, parsed_args.timezone)
            output_directory = Path(parsed_args.output_dir)
            
            # Create application service
            collection_service = ServiceFactory.create_pr_collection_service(
                github_token=github_token,
                timezone=parsed_args.timezone,
                logger=logger
            )
            
            # Execute collection
            collection_service.collect_review_comments(
                repository_id=repository_id,
                date_range=date_range,
                output_directory=output_directory
            )
            
        except (ValueError, PRReviewCollectionError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\\nOperation cancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)
    
    def _get_github_token(self, token_arg: str) -> str:
        """Get GitHub token from argument, keyring, or environment variable.
        
        Priority order:
        1. Command-line argument
        2. System keyring
        3. Environment variable
        
        Args:
            token_arg: Token from command-line argument
            
        Returns:
            GitHub token
            
        Raises:
            ValueError: If no token is provided
        """
        # 1. Check command-line argument first
        if token_arg:
            return token_arg
            
        # 2. Check system keyring
        stored_token = TokenManager.get_token()
        if stored_token:
            return stored_token
            
        # 3. Check environment variable
        env_token = os.getenv("GITHUB_TOKEN")
        if env_token:
            return env_token
            
        raise ValueError(
            "GitHub token not provided. Use --token, store with --store-token, "
            "or set GITHUB_TOKEN environment variable."
        )
    
    def _create_date_range(self, args, timezone: str) -> DateRange:
        """Create date range from parsed arguments.
        
        Args:
            args: Parsed command-line arguments
            timezone: Target timezone
            
        Returns:
            Date range with proper timezone localization
            
        Raises:
            ValueError: If date range is invalid
        """
        # Validate date range
        if args.from_date > args.to_date:
            raise ValueError("from-date must be before or equal to to-date")
        
        # Convert to timezone-aware datetime objects
        timezone_converter = TimezoneConverter(timezone)
        start_date, end_date = timezone_converter.localize_date_range(
            args.from_date, 
            args.to_date
        )
        
        return DateRange(start_date=start_date, end_date=end_date)
    
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