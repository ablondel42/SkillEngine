#!/usr/bin/env python3
"""
Unit tests for static_analysis.py.

Tests cover:
- Scoring algorithm correctness
- Workflow pattern detection
- Eval validation logic
- Edge cases and error handling

Usage: python -m pytest scripts/tests/test_static_analysis.py -v
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from static_analysis import analyze_skill


class TestScoringAlgorithm:
    """Test the scoring algorithm in static_analysis.py."""

    def test_score_skill_md_exists(self, tmp_path):
        """Test that SKILL.md existence is scored correctly."""
        # Create a minimal skill directory
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()

        # Test without SKILL.md
        results = analyze_skill(skill_dir)
        assert results["score"] == 0
        assert results["max_score"] == 20  # SCORE_SKILL_MD_EXISTS
        assert any(c["name"] == "SKILL.md exists" and not c["passed"] for c in results["checks"])

        # Test with SKILL.md
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: test\n---\nContent")
        results = analyze_skill(skill_dir)
        assert results["score"] >= 20
        assert any(c["name"] == "SKILL.md exists" and c["passed"] for c in results["checks"])

    def test_score_workflow_structure(self, tmp_path):
        """Test workflow structure detection."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()

        # Test with strong workflow patterns
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test
description: Test skill
---
# Workflow
Step 1: Do something
Step 2: Do another thing
MANDATORY: Must follow steps
""")
        results = analyze_skill(skill_dir)
        workflow_check = next(c for c in results["checks"] if c["name"] == "Workflow structure defined")
        assert workflow_check["passed"] is True

        # Test without workflow patterns
        skill_md.write_text("""---
name: test
description: Test skill
---
# Random Content
This is just some text without structure.
""")
        results = analyze_skill(skill_dir)
        workflow_check = next(c for c in results["checks"] if c["name"] == "Workflow structure defined")
        assert workflow_check["passed"] is False

    def test_score_interview_phase(self, tmp_path):
        """Test interview/gathering phase detection."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        # Test with interview patterns
        skill_md.write_text("""---
name: test
description: Test skill
---
# Interview Phase
Before I start, I need to ask you some questions.
Please wait for my response before proceeding.
""")
        results = analyze_skill(skill_dir)
        interview_check = next(c for c in results["checks"] if c["name"] == "Information gathering phase")
        assert interview_check["passed"] is True

        # Test without interview patterns
        skill_md.write_text("""---
name: test
description: Test skill
---
# Direct Execution
I'll just do it without asking.
""")
        results = analyze_skill(skill_dir)
        interview_check = next(c for c in results["checks"] if c["name"] == "Information gathering phase")
        assert interview_check["passed"] is False

    def test_score_output_format(self, tmp_path):
        """Test output format specification detection."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        # Test with format patterns
        skill_md.write_text("""---
name: test
description: Test skill
---
# Output Format
Save the result to output.md
```python
# Example code
```
""")
        results = analyze_skill(skill_dir)
        format_check = next(c for c in results["checks"] if c["name"] == "Output format specified")
        assert format_check["passed"] is True

        # Test without format patterns
        skill_md.write_text("""---
name: test
description: Test skill
---
# No Format
Just do it somehow.
""")
        results = analyze_skill(skill_dir)
        format_check = next(c for c in results["checks"] if c["name"] == "Output format specified")
        assert format_check["passed"] is False

    def test_score_error_handling(self, tmp_path):
        """Test error handling detection."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        # Test with error handling patterns
        skill_md.write_text("""---
name: test
description: Test skill
---
# Error Handling
If the file cannot be read, handle the error gracefully.
For edge cases, use a fallback approach.
""")
        results = analyze_skill(skill_dir)
        error_check = next(c for c in results["checks"] if c["name"] == "Error handling defined")
        assert error_check["passed"] is True

        # Test without error handling
        skill_md.write_text("""---
name: test
description: Test skill
---
# Happy Path
Everything will work perfectly.
""")
        results = analyze_skill(skill_dir)
        error_check = next(c for c in results["checks"] if c["name"] == "Error handling defined")
        assert error_check["passed"] is False

    def test_score_eval_definitions(self, tmp_path):
        """Test eval definitions detection."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: test\n---\nContent")

        # Test without evals
        results = analyze_skill(skill_dir)
        eval_check = next(c for c in results["checks"] if c["name"] == "Eval definitions")
        assert eval_check["passed"] is False

        # Test with valid evals
        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text(json.dumps({
            "evals": [
                {
                    "id": 1,
                    "prompt": "Test prompt",
                    "expected_output": "Test output"
                }
            ]
        }))
        results = analyze_skill(skill_dir)
        eval_check = next(c for c in results["checks"] if c["name"] == "Eval definitions")
        assert eval_check["passed"] is True
        assert "1 evals" in eval_check.get("count", "")

    def test_score_description_quality(self, tmp_path):
        """Test description quality scoring."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        # Test with high-quality description
        skill_md.write_text("""---
name: test
description: Build comprehensive design systems when users need to create consistent UI components for web applications. Use this skill when users mention design systems, component libraries, or want to establish reusable patterns.
---
Content
""")
        results = analyze_skill(skill_dir)
        desc_check = next(c for c in results["checks"] if c["name"] == "Description quality")
        assert desc_check["passed"] is True

        # Test with poor description (too short)
        skill_md.write_text("""---
name: test
description: A test skill.
---
Content
""")
        results = analyze_skill(skill_dir)
        desc_check = next(c for c in results["checks"] if c["name"] == "Description quality")
        assert desc_check["passed"] is False

    def test_total_score_calculation(self, tmp_path):
        """Test that total score is calculated correctly."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test
description: Build comprehensive design systems when users need to create consistent UI components for web applications. Use this skill when users mention design systems, component libraries, or want to establish reusable patterns.
---
# Workflow
Step 1: Interview the user
Step 2: Create components
MANDATORY: Follow all steps

# Error Handling
Handle edge cases gracefully.

# Output
Save to output.md
```python
# Example
```
""")

        # Add evals
        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text(json.dumps({
            "evals": [{"id": 1, "prompt": "Test", "expected_output": "Test"}]
        }))

        results = analyze_skill(skill_dir)

        # Verify percentage calculation
        assert results["percentage"] == round(results["score"] / results["max_score"] * 100, 1)
        assert results["max_score"] > 0


class TestWorkflowPatternDetection:
    """Test workflow pattern detection logic."""

    def test_workflow_patterns_step_format(self, tmp_path):
        """Test detection of 'Step N:' pattern."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        patterns = [
            "Step 1: Do this",
            "step 1: Do this",
            "STEP 1: Do this",
            "Step 1:Do this",
            "Phase 1: Start here",
            "phase 2: Continue here"
        ]

        for pattern in patterns:
            skill_md.write_text(f"---\nname: test\n---\n{pattern}")
            results = analyze_skill(skill_dir)
            workflow_check = next(c for c in results["checks"] if c["name"] == "Workflow structure defined")
            assert workflow_check["passed"] is True, f"Failed to detect: {pattern}"

    def test_workflow_patterns_mandatory_keywords(self, tmp_path):
        """Test detection of mandatory/required keywords."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        patterns = [
            "MANDATORY: Do this first",
            "REQUIRED: Follow these steps",
            "MUST complete before proceeding",
            "NON-NEGOTIABLE: Always interview first"
        ]

        for pattern in patterns:
            skill_md.write_text(f"---\nname: test\n---\n{pattern}")
            results = analyze_skill(skill_dir)
            workflow_check = next(c for c in results["checks"] if c["name"] == "Workflow structure defined")
            assert workflow_check["passed"] is True, f"Failed to detect: {pattern}"

    def test_workflow_patterns_sequential_words(self, tmp_path):
        """Test detection of sequential words."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"

        patterns = [
            "Before starting, gather requirements",
            "After interviewing, create tokens",
            "Then proceed to components",
            "Finally, generate documentation"
        ]

        for pattern in patterns:
            skill_md.write_text(f"---\nname: test\n---\n{pattern}")
            results = analyze_skill(skill_dir)
            # Note: Sequential words alone may not be enough, need 2+ patterns
            # This tests that they are counted
            workflow_check = next(c for c in results["checks"] if c["name"] == "Workflow structure defined")
            # At least one pattern detected
            assert workflow_check["note"] is not None


class TestEvalValidationLogic:
    """Test eval validation logic."""

    def test_eval_file_pattern_matching(self, tmp_path):
        """Test that eval file patterns are matched correctly."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: test\n---\nContent")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()

        # Test eval_group*.json pattern
        eval_group1 = evals_dir / "eval_group1.json"
        eval_group1.write_text(json.dumps({"evals": [{"id": 1, "prompt": "Test"}]}))

        eval_group2 = evals_dir / "eval_group2.json"
        eval_group2.write_text(json.dumps({"evals": [{"id": 2, "prompt": "Test"}]}))

        # Test original evals.json
        evals_json = evals_dir / "evals.json"
        evals_json.write_text(json.dumps({"evals": [{"id": 3, "prompt": "Test"}]}))

        results = analyze_skill(skill_dir)
        eval_check = next(c for c in results["checks"] if c["name"] == "Eval definitions")
        assert eval_check["passed"] is True
        assert "3 evals" in eval_check.get("count", "")
        assert "3 file" in eval_check.get("count", "")

    def test_invalid_json_handling(self, tmp_path):
        """Test that invalid JSON is handled gracefully."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: test\n---\nContent")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()

        # Create invalid JSON file
        evals_file = evals_dir / "evals.json"
        evals_file.write_text("{ invalid json }")

        # Should not crash, should report eval check as failed
        results = analyze_skill(skill_dir)
        eval_check = next(c for c in results["checks"] if c["name"] == "Eval definitions")
        assert eval_check["passed"] is False

    def test_empty_evals_array(self, tmp_path):
        """Test handling of empty evals array."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: test\n---\nContent")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text(json.dumps({"evals": []}))

        results = analyze_skill(skill_dir)
        eval_check = next(c for c in results["checks"] if c["name"] == "Eval definitions")
        assert eval_check["passed"] is False
        assert "no evals defined" in eval_check.get("note", "").lower()

    def test_missing_evals_key(self, tmp_path):
        """Test handling of missing 'evals' key."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: test\n---\nContent")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text(json.dumps({"other_key": []}))

        results = analyze_skill(skill_dir)
        eval_check = next(c for c in results["checks"] if c["name"] == "Eval definitions")
        assert eval_check["passed"] is False


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_nonexistent_directory(self):
        """Test handling of nonexistent directory."""
        from pathlib import Path
        results = analyze_skill(Path("/nonexistent/path"))
        assert results["score"] == 0
        assert results["max_score"] == 20  # Only SKILL.md check attempted

    def test_empty_skill_md(self, tmp_path):
        """Test handling of empty SKILL.md."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("")

        results = analyze_skill(skill_dir)
        # Should not crash, should handle gracefully
        assert isinstance(results, dict)

    def test_malformed_frontmatter(self, tmp_path):
        """Test handling of malformed frontmatter."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""name: test
description: No frontmatter delimiters
Content here
""")

        results = analyze_skill(skill_dir)
        # Should not crash
        assert isinstance(results, dict)
        # Description quality check should fail
        desc_check = next(c for c in results["checks"] if c["name"] == "Description quality")
        assert desc_check["passed"] is False

    def test_unicode_content(self, tmp_path):
        """Test handling of unicode content."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-技能
description: 构建综合设计系统 (Build comprehensive design systems)
---
# 工作流
Step 1: 采访用户
""")

        results = analyze_skill(skill_dir)
        # Should handle unicode without crashing
        assert isinstance(results, dict)

    def test_very_long_description(self, tmp_path):
        """Test handling of very long description."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        long_desc = "A" * 1000
        skill_md.write_text(f"""---
name: test
description: {long_desc}
---
Content
""")

        results = analyze_skill(skill_dir)
        desc_check = next(c for c in results["checks"] if c["name"] == "Description quality")
        # Long descriptions should fail the length check (50-500 chars optimal)
        assert desc_check["passed"] is False

    def test_missing_description(self, tmp_path):
        """Test handling of missing description."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test
---
Content without description
""")

        results = analyze_skill(skill_dir)
        desc_check = next(c for c in results["checks"] if c["name"] == "Description quality")
        assert desc_check["passed"] is False
        assert "no description found" in desc_check.get("note", "").lower()


class TestScoreThresholds:
    """Test score threshold calculations."""

    def test_excellent_threshold(self, tmp_path):
        """Test that excellent skills score >= 90%."""
        skill_dir = tmp_path / "perfect-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test
description: Build comprehensive design systems when users need to create consistent UI components for web applications. Use this skill when users mention design systems, component libraries, or want to establish reusable patterns.
---
# Workflow
Step 1: Interview
MANDATORY: Follow steps

# Error Handling
Handle edge cases and errors gracefully.

# Output
Save to output.md
```python
# Example
```
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text(json.dumps({
            "evals": [{"id": 1, "prompt": "Test", "expected_output": "Test"}]
        }))

        results = analyze_skill(skill_dir)
        # All checks should pass for perfect skill
        assert results["percentage"] >= 90

    def test_poor_threshold(self, tmp_path):
        """Test that poor skills score < 50%."""
        skill_dir = tmp_path / "poor-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test
description: Short desc.
---
Random content without structure.
""")

        results = analyze_skill(skill_dir)
        # Many checks should fail
        assert results["percentage"] < 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
