"""
Controller for listing missing PR summary files.
"""

import argparse
import sys
from pathlib import Path

from ..domain.repository_identifier import RepositoryIdentifier
from ..infrastructure.service_factory import ServiceFactory


class ListMissingSummariesController:
    """Controller for listing missing PR summary files."""
    
    def __init__(self):
        """Initialize controller."""
        self._setup_argument_parser()
    
    def _setup_argument_parser(self) -> None:
        """Setup command-line argument parser."""
        self._parser = argparse.ArgumentParser(
            description="List missing PR summary files",
            prog="list_missing_summaries"
        )
        self._parser.add_argument(
            "--repo",
            required=True,
            help="Repository name in format 'owner/repo'"
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
            
            # Create service
            service = ServiceFactory.create_missing_summaries_service()
            
            # Execute
            missing_files = service.list_missing_summaries(repository_id, output_directory)
            
            # Output
            for file_path in missing_files:
                print(file_path)
        
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)