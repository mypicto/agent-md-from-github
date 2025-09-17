#!/usr/bin/env python3
"""
Entry point for the set summary functionality.
"""

import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

if __name__ == "__main__":
    from scripts.src.presentation.review_summary_controller import ReviewSummaryController
    controller = ReviewSummaryController()
    controller.run()