"""
Controller for popping comments from missing summaries.
"""

import argparse
import sys
from pathlib import Path

from ..domain.workspace_config import WorkspaceConfig
from ..infrastructure.service_factory import ServiceFactory


class PopCommentsController:
    """Controller for popping comments from missing summaries."""
    
    def __init__(self):
        """Initialize controller."""
        self._setup_argument_parser()
    
    def _setup_argument_parser(self) -> None:
        """Setup command-line argument parser."""
        self._parser = argparse.ArgumentParser(
            description="Get comments for the next missing summary PR",
            prog="pop_comments"
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
            workspace_config = WorkspaceConfig()
            repository_id = workspace_config.get_repository_identifier()
            output_directory = Path("workspace/pullrequests")
            
            # Create service
            service = ServiceFactory.create_pop_comments_service()
            
            # Get comments markdown
            markdown = service.get_next_missing_comments_markdown(
                repository_id, output_directory
            )
            
            # Output
            print(markdown)
            
        except (ValueError, FileNotFoundError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)