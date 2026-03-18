#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import re
import sys
from pathlib import Path

import yaml

from scripts.utils import (
    ALLOWED_FRONTMATTER_PROPERTIES,
    FORBIDDEN_DESCRIPTION_CHARS,
    MAX_COMPATIBILITY_LENGTH,
    MAX_DESCRIPTION_LENGTH,
    MAX_NAME_LENGTH,
    NAME_PATTERN,
    SKILL_MD_FILENAME,
)


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    """Basic validation of a skill.

    Args:
        skill_path: Path to the skill directory.

    Returns:
        Tuple of (is_valid, message).
    """
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / SKILL_MD_FILENAME
    if not skill_md.exists():
        return False, f"{SKILL_MD_FILENAME} not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_FRONTMATTER_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in {SKILL_MD_FILENAME} frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_FRONTMATTER_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(NAME_PATTERN, name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > MAX_NAME_LENGTH:
            return False, f"Name is too long ({len(name)} characters). Maximum is {MAX_NAME_LENGTH} characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if any(char in description for char in FORBIDDEN_DESCRIPTION_CHARS):
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > MAX_DESCRIPTION_LENGTH:
            return False, f"Description is too long ({len(description)} characters). Maximum is {MAX_DESCRIPTION_LENGTH} characters."

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > MAX_COMPATIBILITY_LENGTH:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is {MAX_COMPATIBILITY_LENGTH} characters."

    return True, "Skill is valid!"


def main() -> None:
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(Path(sys.argv[1]))
    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()