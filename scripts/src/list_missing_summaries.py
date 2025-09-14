#!/usr/bin/env python3
"""
Entry point for the list missing summaries functionality.

This module provides the list missing summaries functionality following
Robert C. Martin's design principles with proper class-to-file mapping.
"""

import sys
import os

# Add the parent directory to Python path to enable relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

if __name__ == "__main__":
    from scripts.src.presentation.list_missing_summaries_controller import ListMissingSummariesController
    controller = ListMissingSummariesController()
    controller.run()