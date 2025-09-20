"""
Workspace switch error for application layer exceptions.

This module defines the exception class for workspace switching
operation failures in the application layer.
"""


class WorkspaceSwitchError(Exception):
    """Exception raised when workspace switch operation fails.
    
    This exception is raised when any step of the workspace switching
    process encounters an error that prevents successful completion.
    """

    def __init__(self, message: str):
        """Initialize workspace switch error.
        
        Args:
            message: Error description message
        """
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of the error.
        
        Returns:
            Error message string
        """
        return f"WorkspaceSwitchError: {self.message}"