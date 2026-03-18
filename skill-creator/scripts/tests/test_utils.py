#!/usr/bin/env python3
"""
Unit tests for utils.py.

Tests cover:
- Constants and configuration values
- parse_skill_md function
- Edge cases and error handling

Usage: python -m pytest scripts/tests/test_utils.py -v
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    ALLOWED_FRONTMATTER_PROPERTIES,
    EVALS_JSON_FILENAME,
    EVALS_KEY,
    EXCLUDE_DIRS,
    EXCLUDE_FILES,
    EXCLUDE_GLOBS,
    FORBIDDEN_DESCRIPTION_CHARS,
    MAX_COMPATIBILITY_LENGTH,
    MAX_DESCRIPTION_LENGTH,
    MAX_NAME_LENGTH,
    MIN_ACCEPTABLE_SCORE_PERCENTAGE,
    MIN_PASSING_SCORE_PERCENTAGE,
    NAME_PATTERN,
    ROOT_EXCLUDE_DIRS,
    SCORE_DESCRIPTION_QUALITY,
    SCORE_ERROR_HANDLING,
    SCORE_EVAL_DEFINITIONS,
    SCORE_INTERVIEW_PHASE,
    SCORE_OUTPUT_FORMAT,
    SCORE_SKILL_MD_EXISTS,
    SCORE_WORKFLOW_STRUCTURE,
    SKILL_FILE_EXTENSION,
    SKILL_MD_FILENAME,
    parse_skill_md,
)


class TestConstants:
    """Test that constants are properly defined."""

    def test_file_constants(self):
        """Test file-related constants."""
        assert SKILL_MD_FILENAME == "SKILL.md"
        assert SKILL_FILE_EXTENSION == ".skill"
        assert EVALS_JSON_FILENAME == "evals.json"
        assert EVALS_KEY == "evals"

    def test_exclude_constants(self):
        """Test exclusion pattern constants."""
        assert isinstance(EXCLUDE_DIRS, frozenset)
        assert isinstance(EXCLUDE_FILES, frozenset)
        assert isinstance(EXCLUDE_GLOBS, frozenset)
        assert isinstance(ROOT_EXCLUDE_DIRS, frozenset)

        assert "__pycache__" in EXCLUDE_DIRS
        assert "node_modules" in EXCLUDE_DIRS
        assert ".DS_Store" in EXCLUDE_FILES
        assert "evals" in ROOT_EXCLUDE_DIRS

    def test_allowed_frontmatter_properties(self):
        """Test allowed frontmatter properties."""
        assert isinstance(ALLOWED_FRONTMATTER_PROPERTIES, frozenset)
        assert "name" in ALLOWED_FRONTMATTER_PROPERTIES
        assert "description" in ALLOWED_FRONTMATTER_PROPERTIES
        assert "license" in ALLOWED_FRONTMATTER_PROPERTIES
        assert "allowed-tools" in ALLOWED_FRONTMATTER_PROPERTIES
        assert "metadata" in ALLOWED_FRONTMATTER_PROPERTIES
        assert "compatibility" in ALLOWED_FRONTMATTER_PROPERTIES

    def test_validation_constants(self):
        """Test validation-related constants."""
        assert MAX_NAME_LENGTH == 64
        assert MAX_DESCRIPTION_LENGTH == 1024
        assert MAX_COMPATIBILITY_LENGTH == 500
        assert isinstance(FORBIDDEN_DESCRIPTION_CHARS, frozenset)
        assert "<" in FORBIDDEN_DESCRIPTION_CHARS
        assert ">" in FORBIDDEN_DESCRIPTION_CHARS
        assert NAME_PATTERN == r"^[a-z0-9-]+$"

    def test_scoring_constants(self):
        """Test scoring constants."""
        # Critical checks
        assert SCORE_SKILL_MD_EXISTS == 20
        assert SCORE_EVAL_DEFINITIONS == 20

        # Important checks
        assert SCORE_WORKFLOW_STRUCTURE == 20
        assert SCORE_INTERVIEW_PHASE == 15
        assert SCORE_OUTPUT_FORMAT == 15
        assert SCORE_ERROR_HANDLING == 15
        assert SCORE_DESCRIPTION_QUALITY == 15

        # Thresholds
        assert MIN_PASSING_SCORE_PERCENTAGE == 70
        assert MIN_ACCEPTABLE_SCORE_PERCENTAGE == 50

        # Verify total max score
        total_max = (
            SCORE_SKILL_MD_EXISTS +
            SCORE_EVAL_DEFINITIONS +
            SCORE_WORKFLOW_STRUCTURE +
            SCORE_INTERVIEW_PHASE +
            SCORE_OUTPUT_FORMAT +
            SCORE_ERROR_HANDLING +
            SCORE_DESCRIPTION_QUALITY
        )
        assert total_max == 120


class TestParseSkillMd:
    """Test the parse_skill_md function."""

    def test_parse_valid_skill_md(self, tmp_path):
        """Test parsing a valid SKILL.md file."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill for validation
---
# Content
This is the skill content.
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == "test-skill"
        assert description == "A test skill for validation"
        assert "# Content" in full_content

    def test_parse_skill_md_with_quoted_values(self, tmp_path):
        """Test parsing SKILL.md with quoted frontmatter values."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: "test-skill"
description: 'A test skill with quotes'
---
Content
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == "test-skill"
        assert description == "A test skill with quotes"

    def test_parse_skill_md_multiline_description(self, tmp_path):
        """Test parsing SKILL.md with multiline description."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  A comprehensive test skill that spans
  multiple lines for better readability
  and testing purposes
---
Content
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == "test-skill"
        assert "A comprehensive test skill" in description
        assert "multiple lines" in description

    def test_parse_skill_md_no_name(self, tmp_path):
        """Test parsing SKILL.md without name field."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
description: A skill without a name
---
Content
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == ""
        assert description == "A skill without a name"

    def test_parse_skill_md_no_description(self, tmp_path):
        """Test parsing SKILL.md without description field."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
---
Content without description
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == "test-skill"
        assert description == ""

    def test_parse_skill_md_missing_opening_delimiter(self, tmp_path):
        """Test parsing SKILL.md without opening ---."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""name: test-skill
description: No opening delimiter
---
Content
""")

        with pytest.raises(ValueError, match="missing frontmatter"):
            parse_skill_md(skill_dir)

    def test_parse_skill_md_missing_closing_delimiter(self, tmp_path):
        """Test parsing SKILL.md without closing ---."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: No closing delimiter

Content
""")

        with pytest.raises(ValueError, match="missing frontmatter"):
            parse_skill_md(skill_dir)

    def test_parse_skill_md_empty_file(self, tmp_path):
        """Test parsing empty SKILL.md."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("")

        with pytest.raises((ValueError, IndexError)):
            parse_skill_md(skill_dir)

    def test_parse_skill_md_only_frontmatter(self, tmp_path):
        """Test parsing SKILL.md with only frontmatter."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Only frontmatter
---
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == "test-skill"
        assert description == "Only frontmatter"
        assert full_content.strip() == """---
name: test-skill
description: Only frontmatter
---"""

    def test_parse_skill_md_with_tabs_in_multiline(self, tmp_path):
        """Test parsing SKILL.md with tabs in multiline description."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
\tTab-indented line
\tAnother tabbed line
---
Content
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == "test-skill"
        assert "Tab-indented line" in description

    def test_parse_skill_md_complex_frontmatter(self, tmp_path):
        """Test parsing SKILL.md with complex frontmatter."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A complex skill
license: MIT
allowed-tools: glob, read_file
metadata:
  version: 1.0
  author: Test
compatibility: Claude 3.5+
---
Content
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == "test-skill"
        assert description == "A complex skill"
        assert "license: MIT" in full_content


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_parse_nonexistent_file(self, tmp_path):
        """Test parsing nonexistent file."""
        skill_dir = tmp_path / "nonexistent-skill"

        with pytest.raises(FileNotFoundError):
            parse_skill_md(skill_dir)

    def test_parse_skill_md_whitespace_handling(self, tmp_path):
        """Test whitespace handling in frontmatter."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name:   test-skill
description:   A skill with extra spaces
---
Content
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == "test-skill"
        assert description == "A skill with extra spaces"

    def test_parse_skill_md_special_characters(self, tmp_path):
        """Test parsing SKILL.md with special characters."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill-特殊文字
description: 特殊文字テスト (Special character test)
---
Content with special chars: @#$%^&*()
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == "test-skill-特殊文字"
        assert "特殊文字テスト" in description

    def test_parse_skill_md_very_long_values(self, tmp_path):
        """Test parsing SKILL.md with very long values."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        long_name = "a" * 100
        long_desc = "b" * 500
        skill_md.write_text(f"""---
name: {long_name}
description: {long_desc}
---
Content
""")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == long_name
        assert description == long_desc

    def test_parse_skill_md_mixed_line_endings(self, tmp_path):
        """Test parsing SKILL.md with mixed line endings."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        # Mix of \n and \r\n
        skill_md.write_text("---\r\nname: test-skill\r\ndescription: Mixed endings\r\n---\r\nContent\n")

        name, description, full_content = parse_skill_md(skill_dir)

        assert name == "test-skill"
        assert description == "Mixed endings"


class TestConstantImmutability:
    """Test that frozenset constants are truly immutable."""

    def test_exclude_dirs_immutable(self):
        """Test that EXCLUDE_DIRS cannot be modified."""
        with pytest.raises((AttributeError, TypeError)):
            EXCLUDE_DIRS.add("new_dir")

    def test_exclude_files_immutable(self):
        """Test that EXCLUDE_FILES cannot be modified."""
        with pytest.raises((AttributeError, TypeError)):
            EXCLUDE_FILES.add("new_file.txt")

    def test_allowed_properties_immutable(self):
        """Test that ALLOWED_FRONTMATTER_PROPERTIES cannot be modified."""
        with pytest.raises((AttributeError, TypeError)):
            ALLOWED_FRONTMATTER_PROPERTIES.add("new_property")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
