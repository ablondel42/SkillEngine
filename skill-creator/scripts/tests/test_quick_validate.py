#!/usr/bin/env python3
"""
Unit tests for quick_validate.py.

Tests cover:
- Frontmatter validation
- Name validation (kebab-case, length)
- Description validation (length, forbidden chars)
- Compatibility validation
- Edge cases and error handling

Usage: python -m pytest scripts/tests/test_quick_validate.py -v
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from quick_validate import validate_skill


class TestFrontmatterValidation:
    """Test frontmatter validation logic."""

    def test_valid_frontmatter(self, tmp_path):
        """Test validation of valid frontmatter."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A valid test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True
        assert "valid" in message.lower()

    def test_missing_frontmatter(self, tmp_path):
        """Test validation when frontmatter is missing."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("# No frontmatter\nJust content")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "frontmatter" in message.lower()

    def test_invalid_yaml_frontmatter(self, tmp_path):
        """Test validation with invalid YAML in frontmatter."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: [invalid yaml
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "yaml" in message.lower() or "invalid" in message.lower()

    def test_missing_closing_delimiter(self, tmp_path):
        """Test validation with missing closing ---."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: No closing delimiter

Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "frontmatter" in message.lower()

    def test_missing_name(self, tmp_path):
        """Test validation when name is missing."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
description: A skill without name
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "name" in message.lower()

    def test_missing_description(self, tmp_path):
        """Test validation when description is missing."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "description" in message.lower()

    def test_unexpected_frontmatter_property(self, tmp_path):
        """Test validation with unexpected frontmatter properties."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill
unknown_property: value
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "unexpected" in message.lower() or "unknown_property" in message

    def test_valid_metadata_property(self, tmp_path):
        """Test that metadata property is allowed (nested keys excluded from check)."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill
metadata:
  version: 1.0
  author: Test
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True


class TestNameValidation:
    """Test name validation logic."""

    def test_valid_kebab_case_name(self, tmp_path):
        """Test validation of valid kebab-case names."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()

        valid_names = [
            "test-skill",
            "design-system",
            "pdf-processor",
            "skill-123",
            "a",  # Single character
            "my-awesome-skill-2024"
        ]

        for name in valid_names:
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text(f"""---
name: {name}
description: A test skill
---
Content
""")
            is_valid, message = validate_skill(skill_dir)
            assert is_valid is True, f"Failed for name: {name}"

    def test_invalid_name_uppercase(self, tmp_path):
        """Test validation fails for uppercase names."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: Test-Skill
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "kebab-case" in message.lower() or "lowercase" in message.lower()

    def test_invalid_name_underscore(self, tmp_path):
        """Test validation fails for underscore in name."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test_skill
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "kebab-case" in message.lower()

    def test_invalid_name_spaces(self, tmp_path):
        """Test validation fails for spaces in name."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test skill
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False

    def test_invalid_name_starts_with_hyphen(self, tmp_path):
        """Test validation fails for name starting with hyphen."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: -test-skill
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "hyphen" in message.lower() or "start" in message.lower()

    def test_invalid_name_ends_with_hyphen(self, tmp_path):
        """Test validation fails for name ending with hyphen."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill-
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "hyphen" in message.lower() or "end" in message.lower()

    def test_invalid_name_consecutive_hyphens(self, tmp_path):
        """Test validation fails for consecutive hyphens."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test--skill
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "consecutive" in message.lower() or "hyphen" in message.lower()

    def test_name_too_long(self, tmp_path):
        """Test validation fails for name exceeding max length."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        long_name = "a" * 65  # Max is 64
        skill_md.write_text(f"""---
name: {long_name}
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "too long" in message.lower() or "characters" in message.lower()

    def test_name_at_max_length(self, tmp_path):
        """Test validation passes for name at max length."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        max_name = "a" * 64  # Exactly at max
        skill_md.write_text(f"""---
name: {max_name}
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_name_with_numbers(self, tmp_path):
        """Test validation passes for names with numbers."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: skill-2024-v2
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True


class TestDescriptionValidation:
    """Test description validation logic."""

    def test_valid_description(self, tmp_path):
        """Test validation of valid description."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A comprehensive test skill for validation purposes
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_description_with_angle_brackets(self, tmp_path):
        """Test validation fails for description with angle brackets."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        for bracket in ["<", ">"]:
            skill_md.write_text(f"""---
name: test-skill
description: A test {bracket}script{bracket if bracket == ">" else ""} description
---
Content
""")
            is_valid, message = validate_skill(skill_dir)
            assert is_valid is False
            assert "angle bracket" in message.lower() or "<" in message or ">" in message

    def test_description_too_long(self, tmp_path):
        """Test validation fails for description exceeding max length."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        long_desc = "a" * 1025  # Max is 1024
        skill_md.write_text(f"""---
name: test-skill
description: {long_desc}
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "too long" in message.lower() or "characters" in message.lower()

    def test_description_at_max_length(self, tmp_path):
        """Test validation passes for description at max length."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        max_desc = "a" * 1024  # Exactly at max
        skill_md.write_text(f"""---
name: test-skill
description: {max_desc}
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_empty_description(self, tmp_path):
        """Test validation with empty description."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description:
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        # Empty description should be valid (just not useful)
        assert is_valid is True

    def test_description_with_special_chars(self, tmp_path):
        """Test validation passes for description with special characters."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill with @#$%^&*() special chars!
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_description_with_quotes(self, tmp_path):
        """Test validation passes for description with quotes."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: "A test skill with quotes"
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True


class TestCompatibilityValidation:
    """Test compatibility field validation."""

    def test_valid_compatibility(self, tmp_path):
        """Test validation of valid compatibility field."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill
compatibility: Claude 3.5+
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_compatibility_too_long(self, tmp_path):
        """Test validation fails for compatibility exceeding max length."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        long_compat = "a" * 501  # Max is 500
        skill_md.write_text(f"""---
name: test-skill
description: A test skill
compatibility: {long_compat}
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "too long" in message.lower() or "characters" in message.lower()

    def test_compatibility_at_max_length(self, tmp_path):
        """Test validation passes for compatibility at max length."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        max_compat = "a" * 500  # Exactly at max
        skill_md.write_text(f"""---
name: test-skill
description: A test skill
compatibility: {max_compat}
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_compatibility_non_string(self, tmp_path):
        """Test validation fails for non-string compatibility."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill
compatibility: 123
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "string" in message.lower()


class TestMissingSkillMd:
    """Test handling of missing SKILL.md."""

    def test_missing_skill_md(self, tmp_path):
        """Test validation fails when SKILL.md is missing."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        # Don't create SKILL.md

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "SKILL.md" in message or "not found" in message.lower()

    def test_nonexistent_directory(self, tmp_path):
        """Test validation fails for nonexistent directory."""
        skill_dir = tmp_path / "nonexistent-skill"

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "not found" in message.lower() or "exist" in message.lower()


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_skill_md(self, tmp_path):
        """Test validation of empty SKILL.md."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "frontmatter" in message.lower()

    def test_only_frontmatter(self, tmp_path):
        """Test validation with only frontmatter (no content)."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill
---
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_unicode_content(self, tmp_path):
        """Test validation with unicode content."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-技能
description: 构建综合设计系统 (Build comprehensive design systems)
---
Content with 日本語 and العربية
""")

        is_valid, message = validate_skill(skill_dir)
        # Unicode in name should fail kebab-case check
        assert is_valid is False

    def test_unicode_description(self, tmp_path):
        """Test validation with unicode in description only."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: 构建综合设计系统 (Build comprehensive design systems)
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_name_with_single_quotes(self, tmp_path):
        """Test validation with single-quoted name."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: 'test-skill'
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_name_with_double_quotes(self, tmp_path):
        """Test validation with double-quoted name."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: "test-skill"
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_non_string_name(self, tmp_path):
        """Test validation fails for non-string name."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: 123
description: A test skill
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "string" in message.lower()

    def test_non_string_description(self, tmp_path):
        """Test validation fails for non-string description."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: 123
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "string" in message.lower()


class TestFrontmatterNonDict:
    """Test handling of non-dict frontmatter."""

    def test_frontmatter_is_list(self, tmp_path):
        """Test validation fails when frontmatter is a list."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
- item1
- item2
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "dictionary" in message.lower() or "dict" in message.lower()

    def test_frontmatter_is_string(self, tmp_path):
        """Test validation fails when frontmatter is just a string."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
just a string
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        # YAML will parse this as a string, not a dict
        assert is_valid is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
