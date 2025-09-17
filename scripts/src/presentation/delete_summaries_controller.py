"""
Controller for deleting PR summary files.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from ..domain.repository_identifier import RepositoryIdentifier
from ..infrastructure.service_factory import ServiceFactory


class DeleteSummariesController:
    """Controller for deleting PR summary files."""
    
    def __init__(self):
        """Initialize controller."""
        self._setup_argument_parser()
    
    def _setup_argument_parser(self) -> None:
        """Setup command-line argument parser."""
        self._parser = argparse.ArgumentParser(
            description="Delete PR summary files",
            prog="delete_summaries"
        )
        
        self._parser.add_argument(
            "--repo",
            help="Repository name in format 'owner/repo' (optional, deletes from all repos if not specified)"
        )
        
        self._parser.add_argument(
            "--output-dir",
            default="pullrequests",
            help="Output directory (default: pullrequests)"
        )
    
    def run(self, args: Optional[list[str]] = None) -> None:
        """Run the controller.
        
        Args:
            args: Command-line arguments
        """
        parsed_args = self._parser.parse_args(args)
        self._handle_command(parsed_args)
    
    def _handle_command(self, parsed_args) -> None:
        """Handle the command."""
        try:
            repository_id = None
            if parsed_args.repo:
                repository_id = RepositoryIdentifier.from_string(parsed_args.repo)
            
            output_directory = Path(parsed_args.output_dir)
            
            # Create service
            service = ServiceFactory.create_delete_summaries_service()
            
            # Execute deletion
            deleted_files = service.delete_summaries(repository_id, output_directory)
            
            # Output results
            if not deleted_files:
                print("No summary files found to delete.")
                return
            
            print(f"Deleted {len(deleted_files)} summary files:")
            for file_path in deleted_files:
                print(f"  {file_path}")
        
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)