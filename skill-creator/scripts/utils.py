"""Shared utilities for skill-creator scripts.

This module provides shared constants and utility functions used across
skill-creator scripts.
"""

from pathlib import Path


# =============================================================================
# File and Directory Constants
# =============================================================================

SKILL_MD_FILENAME = "SKILL.md"
SKILL_FILE_EXTENSION = ".skill"

# Eval file patterns
EVAL_DIR_NAME = "evals"
EVAL_FILE_PATTERN = "eval_group*.json"
EVALS_JSON_FILENAME = "evals.json"
EVALS_KEY = "evals"

# Command directory for Claude
CLAUDE_DIR_NAME = ".claude"
CLAUDE_COMMANDS_DIR = "commands"

# Exclusion patterns for packaging
EXCLUDE_DIRS = frozenset({"__pycache__", "node_modules"})
EXCLUDE_GLOBS = frozenset({"*.pyc"})
EXCLUDE_FILES = frozenset({".DS_Store"})
ROOT_EXCLUDE_DIRS = frozenset({"evals"})


# =============================================================================
# Scoring Constants (Static Analysis)
# =============================================================================

# Critical checks
SCORE_SKILL_MD_EXISTS = 20
SCORE_EVAL_DEFINITIONS = 20

# Important checks
SCORE_WORKFLOW_STRUCTURE = 20
SCORE_INTERVIEW_PHASE = 15
SCORE_OUTPUT_FORMAT = 15
SCORE_ERROR_HANDLING = 15
SCORE_DESCRIPTION_QUALITY = 15

# Minimum passing score percentage
MIN_PASSING_SCORE_PERCENTAGE = 70
MIN_ACCEPTABLE_SCORE_PERCENTAGE = 50


# =============================================================================
# Validation Constants
# =============================================================================

# Allowed frontmatter properties
ALLOWED_FRONTMATTER_PROPERTIES = frozenset({
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
})

# Name validation
MAX_NAME_LENGTH = 64
NAME_PATTERN = r"^[a-z0-9-]+$"

# Description validation
MAX_DESCRIPTION_LENGTH = 1024
FORBIDDEN_DESCRIPTION_CHARS = frozenset({"<", ">"})

# Compatibility validation
MAX_COMPATIBILITY_LENGTH = 500


# =============================================================================
# Evaluation Constants
# =============================================================================

# Default evaluation settings
DEFAULT_NUM_WORKERS = 10
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_RUNS_PER_QUERY = 3
DEFAULT_TRIGGER_THRESHOLD = 0.5
DEFAULT_HOLDOUT_FRACTION = 0.4
DEFAULT_MAX_ITERATIONS = 5

# Model defaults
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"


# =============================================================================
# Utility Functions
# =============================================================================

def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Parse a SKILL.md file, returning (name, description, full_content).

    Args:
        skill_path: Path to the skill directory containing SKILL.md.

    Returns:
        Tuple of (name, description, full_content).

    Raises:
        ValueError: If the SKILL.md file has invalid frontmatter.
    """
    content = (skill_path / SKILL_MD_FILENAME).read_text()
    lines = content.split("\n")

    if lines[0].strip() != "---":
        raise ValueError(f"{SKILL_MD_FILENAME} missing frontmatter (no opening ---)")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise ValueError(f"{SKILL_MD_FILENAME} missing frontmatter (no closing ---)")

    name = ""
    description = ""
    frontmatter_lines = lines[1:end_idx]
    i = 0
    while i < len(frontmatter_lines):
        line = frontmatter_lines[i]
        if line.startswith("name:"):
            name = line[len("name:"):].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            value = line[len("description:"):].strip()
            # Handle YAML multiline indicators (>, |, >-, |-)
            if value in (">", "|", ">-", "|-"):
                continuation_lines: list[str] = []
                i += 1
                while i < len(frontmatter_lines) and (frontmatter_lines[i].startswith("  ") or frontmatter_lines[i].startswith("\t")):
                    continuation_lines.append(frontmatter_lines[i].strip())
                    i += 1
                description = " ".join(continuation_lines)
                continue
            else:
                description = value.strip('"').strip("'")
        i += 1

    return name, description, content
