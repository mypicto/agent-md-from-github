"""
Switch workspace controller for workspace switching operations.

This module provides the command-line interface controller for workspace
switching functionality following the presentation layer pattern.
"""

import argparse
import sys
from typing import List

from ..application.exceptions.workspace_switch_error import WorkspaceSwitchError
from ..infrastructure.service_factory import ServiceFactory


class SwitchWorkspaceController:
    """Controller for workspace switching command-line interface.
    
    This controller handles command-line argument parsing and orchestrates
    the workspace switching operation through the application service layer.
    """

    def __init__(self):
        """Initialize switch workspace controller."""
        pass

    def run(self, args: List[str] = None) -> None:
        """Run workspace switching operation with command-line arguments.
        
        Args:
            args: Optional list of command-line arguments (defaults to sys.argv)
            
        Raises:
            SystemExit: On argument parsing errors or operation failures
        """
        try:
            # Parse command-line arguments
            parsed_args = self._parse_arguments(args)
            
            # Setup logging
            logger = ServiceFactory.setup_logging(verbose=parsed_args.verbose)
            
            # Create workspace switch service
            workspace_service = ServiceFactory.create_workspace_switch_service(logger)
            
            # Execute workspace switch
            workspace_service.switch_workspace(parsed_args.repo)
            
            print(f"Successfully switched workspace to: {parsed_args.repo}")
            
        except WorkspaceSwitchError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)

    def _parse_arguments(self, args: List[str] = None) -> argparse.Namespace:
        """Parse command-line arguments.
        
        Args:
            args: Optional list of arguments (defaults to sys.argv)
            
        Returns:
            Parsed arguments namespace
            
        Raises:
            SystemExit: If argument parsing fails
        """
        parser = argparse.ArgumentParser(
            description="Switch workspace to different repository",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_usage_examples()
        )
        
        # Required arguments
        parser.add_argument(
            "--repo",
            required=True,
            help="Repository specification in 'owner/repository' format"
        )
        
        # Optional arguments
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Enable verbose output"
        )
        
        return parser.parse_args(args)

    def _get_usage_examples(self) -> str:
        """Get usage examples for help text.
        
        Returns:
            Formatted usage examples string
        """
        return """
Examples:
  # Switch to existing repository workspace
  python scripts/src/switch_workspace.py --repo "owner/repository"
  
  # Switch with verbose output
  python scripts/src/switch_workspace.py --repo "owner/repository" --verbose
  
  # Switch to organization repository
  python scripts/src/switch_workspace.py --repo "my-org/my-project"

Notes:
  - Current workspace will be automatically backed up to workspaces/<owner>/<repository>/
  - If target repository workspace exists, it will be restored
  - If target repository workspace doesn't exist, a new one will be initialized
  - Repository specification must follow GitHub owner/repository format
        """