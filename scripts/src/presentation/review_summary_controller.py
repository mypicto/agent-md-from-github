"""
Review summary controller for setting PR summaries.
"""

import argparse
import os
import sys
from pathlib import Path

from ..application.exceptions.pr_review_collection_error import PRReviewCollectionError
from ..domain.repository_identifier import RepositoryIdentifier
from ..infrastructure.service_factory import ServiceFactory
from ..infrastructure.services.token_manager import TokenManager


class ReviewSummaryController:
    """Controller for setting review summaries."""
    
    def __init__(self):
        """Initialize review summary controller."""
        self._setup_argument_parser()
    
    def _setup_argument_parser(self) -> None:
        """Setup command-line argument parser."""
        self._parser = argparse.ArgumentParser(
            description="Set review summary for a GitHub PR",
            prog="set_summary"
        )
        
        self._parser.add_argument(
            "--repo",
            required=True,
            help="Repository name in format 'owner/repo'"
        )
        
        self._parser.add_argument(
            "--pr",
            type=int,
            required=True,
            help="PR number"
        )
        
        self._parser.add_argument(
            "--priority",
            required=True,
            choices=["high", "middle", "low"],
            help="Priority level"
        )
        
        self._parser.add_argument(
            "--file",
            required=True,
            help="Path to summary file (Markdown format)"
        )
    
    def run(self, args: list[str] = None) -> None:
        """Run the review summary application.
        
        Args:
            args: Command line arguments (optional)
        """
        parsed_args = self._parser.parse_args(args)
        
        try:
            # Parse repository identifier
            repository_id = RepositoryIdentifier.from_string(parsed_args.repo)
            
            # Read summary from file
            summary_text = Path(parsed_args.file).read_text(encoding='utf-8')
            
            # Create service
            service = ServiceFactory.create_review_summary_service()
            
            # Set summary
            service.set_summary(
                repository_id=repository_id,
                pr_number=parsed_args.pr,
                priority=parsed_args.priority,
                summary=summary_text
            )
            
            print(f"Successfully saved summary for PR #{parsed_args.pr} in {parsed_args.repo}")
            
        except FileNotFoundError:
            print(f"Error: File not found: {parsed_args.file}", file=sys.stderr)
            sys.exit(1)
        except PRReviewCollectionError as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {str(e)}", file=sys.stderr)
            sys.exit(1)