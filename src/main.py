#!/usr/bin/env python3
"""
Main entry point for the redesigned PR collector.

This module provides a clean architecture implementation following
Robert C. Martin's design principles with proper class-to-file mapping.
"""

import sys
import os

# Add the parent directory to Python path to enable relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    from src.presentation.cli_controller import CLIController
    cli = CLIController()
    cli.run()