#!/usr/bin/env python3
"""
Design system tokens utilities.

Shared functions for loading and manipulating design system tokens.
"""

import json
from pathlib import Path
from typing import Any


def load_tokens(tokens_file: Path) -> dict[str, Any]:
    """Load design system tokens from JSON file.

    Args:
        tokens_file: Path to the JSON file containing design tokens.

    Returns:
        Dictionary containing the loaded tokens.

    Raises:
        FileNotFoundError: If the tokens file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    with open(tokens_file) as f:
        return json.load(f)
