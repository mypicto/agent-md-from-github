"""
Controller for getting comments.
"""

import argparse
import sys
from pathlib import Path

from ..domain.repository_identifier import RepositoryIdentifier
from ..infrastructure.service_factory import ServiceFactory
from ..application.exceptions.comments_service_error import CommentsServiceError


class CommentsController:
    """Controller for getting comments."""
    
    def __init__(self):
        """Initialize controller."""
        self._setup_argument_parser()
    
    def _setup_argument_parser(self) -> None:
        """Setup command-line argument parser."""
        self._parser = argparse.ArgumentParser(
            description="Get comments for a PR",
            prog="get_comments"
        )
        self._parser.add_argument(
            "--repo",
            required=True,
            help="Repository name in format 'owner/repo'"
        )
        self._parser.add_argument(
            "--pr",
            required=True,
            help="PR number in format 'PR-<number>'"
        )
        self._parser.add_argument(
            "--output-dir",
            default="pullrequests",
            help="Output directory (default: pullrequests)"
        )
    
    def run(self, args: list[str] = None) -> None:
        """Run the controller.
        
        Args:
            args: Command-line arguments
        """
        parsed_args = self._parser.parse_args(args)
        self._handle_command(parsed_args)
    
    def _handle_command(self, parsed_args) -> None:
        """Handle the command."""
        try:
            repository_id = RepositoryIdentifier.from_string(parsed_args.repo)
            output_directory = Path(parsed_args.output_dir)
            
            # Parse PR number from 'PR-<number>' format
            pr_arg = parsed_args.pr
            if not pr_arg.startswith("PR-"):
                raise ValueError(f"PR number must be in format 'PR-<number>', got: {pr_arg}")
            try:
                pr_number = pr_arg[3:]  # Remove 'PR-' prefix
            except IndexError:
                raise ValueError(f"Invalid PR format: {pr_arg}")
            
            # Create service
            service = ServiceFactory.create_comments_service()
            
            # Get comments markdown
            markdown = service.get_comments_markdown(
                repository_id, pr_number, output_directory
            )
            
            # Output
            print(markdown)
            
        except CommentsServiceError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)