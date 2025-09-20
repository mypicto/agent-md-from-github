"""
List summary files controller.
"""

import argparse
import sys

from ..domain.workspace_config import WorkspaceConfig
from ..infrastructure.service_factory import ServiceFactory


class ListSummaryFilesController:
    """Controller for listing summary files based on priority."""

    def __init__(self):
        """Initialize the controller."""
        self._setup_argument_parser()

    def _setup_argument_parser(self) -> None:
        """Setup command-line argument parser."""
        self._parser = argparse.ArgumentParser(
            description="List summary files by priority",
            prog="list_summary_files"
        )
        self._parser.add_argument(
            "--priority",
            action="append",
            choices=["high", "middle", "low"],
            help="Priority level to filter by (can be specified multiple times)"
        )

    def run(self) -> None:
        """Run the controller."""
        args = self._parser.parse_args()

        try:
            # Parse repository identifier
            workspace_config = WorkspaceConfig()
            repository_id = workspace_config.get_repository_identifier()

            # Get priorities (empty list means all)
            priorities = args.priority if args.priority else []

            # Create service
            service = ServiceFactory.create_list_summary_files_service()

            # List summary files
            file_paths = service.list_summary_files(repository_id, priorities)

            # Output results
            for path in file_paths:
                print(path)

        except (ValueError, FileNotFoundError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)