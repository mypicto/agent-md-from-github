#!/usr/bin/env python3
"""
Entry point for the GitHub authentication token management functionality.

This module provides the auth functionality following
Robert C. Martin's design principles with proper class-to-file mapping.
"""

import sys
import os

# Add the parent directory to Python path to enable relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

if __name__ == "__main__":
    from scripts.src.presentation.auth_controller import AuthController
    auth = AuthController()
    auth.run()