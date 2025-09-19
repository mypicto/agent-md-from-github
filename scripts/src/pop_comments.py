#!/usr/bin/env python3
"""
Entry point for the pop comments functionality.

This module provides the pop comments functionality following
Robert C. Martin's design principles with proper class-to-file mapping.
"""

import sys
import os

# Add the parent directory to Python path to enable relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

if __name__ == "__main__":
    from scripts.src.presentation.pop_comments_controller import PopCommentsController
    controller = PopCommentsController()
    controller.run()