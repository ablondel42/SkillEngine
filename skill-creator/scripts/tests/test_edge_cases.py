#!/usr/bin/env python3
"""
Edge case tests for skill validation and analysis.

Tests cover:
- Malformed SKILL.md files
- Missing eval files
- Invalid agent definitions
- Concurrent test execution scenarios

Usage: python -m pytest scripts/tests/test_edge_cases.py -v
"""

import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from quick_validate import validate_skill
from static_analysis import analyze_skill
from review_evals import review_evals


class TestMalformedSkillMd:
    """Test handling of malformed SKILL.md files."""

    def test_completely_empty_file(self, tmp_path):
        """Test handling of completely empty SKILL.md."""
        skill_dir = tmp_path / "empty-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False

        # Static analysis should not crash
        results = analyze_skill(skill_dir)
        assert isinstance(results, dict)
        assert results["score"] == 0

    def test_binary_content(self, tmp_path):
        """Test handling of binary content in SKILL.md."""
        skill_dir = tmp_path / "binary-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        # Write some binary-like content
        skill_md.write_bytes(b"\x00\x01\x02\x03\x04\x05")

        # Should not crash, should handle gracefully
        results = analyze_skill(skill_dir)
        assert isinstance(results, dict)

    def test_only_whitespace(self, tmp_path):
        """Test handling of file with only whitespace."""
        skill_dir = tmp_path / "whitespace-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("   \n\t\n   \n")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "frontmatter" in message.lower()

    def test_unclosed_yaml_string(self, tmp_path):
        """Test handling of unclosed YAML string."""
        skill_dir = tmp_path / "unclosed-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: "unclosed string
description: Test
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is False
        assert "yaml" in message.lower() or "invalid" in message.lower()

    def test_malformed_yaml_list_as_name(self, tmp_path):
        """Test handling of list value where string expected."""
        skill_dir = tmp_path / "list-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name:
  - item1
  - item2
description: Test
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        # Should fail because name should be a string
        assert is_valid is False

    def test_yaml_anchor_reference(self, tmp_path):
        """Test handling of YAML anchor references."""
        skill_dir = tmp_path / "anchor-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: &anchor test-skill
description: *anchor
---
Content
""")

        # This is actually valid YAML with anchors
        is_valid, message = validate_skill(skill_dir)
        # May pass or fail depending on YAML parser handling
        assert isinstance(is_valid, bool)

    def test_extremely_long_lines(self, tmp_path):
        """Test handling of extremely long lines."""
        skill_dir = tmp_path / "longline-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        # Create a line with 10000 characters
        long_line = "a" * 10000
        skill_md.write_text(f"""---
name: test-skill
description: {long_line}
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        # Should fail due to description length
        assert is_valid is False
        assert "too long" in message.lower()

    def test_null_values_in_frontmatter(self, tmp_path):
        """Test handling of null values in frontmatter."""
        skill_dir = tmp_path / "null-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: null
description: ~
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        # name is null, description is null (YAML ~)
        assert is_valid is False

    def test_duplicate_keys(self, tmp_path):
        """Test handling of duplicate keys in frontmatter."""
        skill_dir = tmp_path / "duplicate-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        # YAML doesn't allow duplicate keys, but test parser behavior
        skill_md.write_text("""---
name: test-skill
name: another-skill
description: Test
---
Content
""")

        # YAML parser will typically use the last value
        is_valid, message = validate_skill(skill_dir)
        # Should still be valid (last name wins)
        assert isinstance(is_valid, bool)

    def test_special_yaml_characters(self, tmp_path):
        """Test handling of special YAML characters."""
        skill_dir = tmp_path / "special-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: "Value with # comment & ampersand * asterisk"
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        # Should handle quoted special characters
        assert is_valid is True


class TestMissingEvalFiles:
    """Test handling of missing eval files."""

    def test_no_evals_directory(self, tmp_path):
        """Test handling when evals/ directory doesn't exist."""
        skill_dir = tmp_path / "noevals-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test
---
Content
""")

        # Static analysis should report missing evals
        results = analyze_skill(skill_dir)
        eval_check = next(c for c in results["checks"] if c["name"] == "Eval definitions")
        assert eval_check["passed"] is False

        # Review evals should handle gracefully
        review_results = review_evals(skill_dir)
        assert review_results["percentage"] == 0

    def test_empty_evals_directory(self, tmp_path):
        """Test handling when evals/ exists but is empty."""
        skill_dir = tmp_path / "emptyevals-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test
---
Content
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()

        results = analyze_skill(skill_dir)
        eval_check = next(c for c in results["checks"] if c["name"] == "Eval definitions")
        assert eval_check["passed"] is False

    def test_evals_directory_with_wrong_files(self, tmp_path):
        """Test handling when evals/ has wrong file types."""
        skill_dir = tmp_path / "wrongevals-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test
---
Content
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()

        # Create wrong file types
        (evals_dir / "readme.txt").write_text("Not an eval file")
        (evals_dir / "data.csv").write_text("id,prompt\n1,test")
        (evals_dir / "config.yaml").write_text("key: value")

        results = analyze_skill(skill_dir)
        eval_check = next(c for c in results["checks"] if c["name"] == "Eval definitions")
        assert eval_check["passed"] is False

    def test_evals_file_is_directory(self, tmp_path):
        """Test handling when evals.json is actually a directory."""
        skill_dir = tmp_path / "direvals-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test
---
Content
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()

        # Create directory where file should be
        (evals_dir / "evals.json").mkdir()

        results = analyze_skill(skill_dir)
        # Should handle gracefully
        assert isinstance(results, dict)

    def test_evals_file_not_readable(self, tmp_path):
        """Test handling when evals file exists but isn't readable."""
        skill_dir = tmp_path / "unreadableevals-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test
---
Content
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text("{}")

        # Make file unreadable (only works on Unix systems)
        try:
            evals_file.chmod(0o000)
            results = analyze_skill(skill_dir)
            # Should handle permission error gracefully
            assert isinstance(results, dict)
        finally:
            # Restore permissions for cleanup
            evals_file.chmod(0o644)


class TestInvalidAgentDefinitions:
    """Test handling of invalid agent definitions."""

    def test_eval_missing_required_fields(self, tmp_path):
        """Test handling of eval missing required fields."""
        skill_dir = tmp_path / "missingfields-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test
---
Content
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        # Missing 'prompt' and 'expected_output'
        evals_file.write_text(json.dumps({
            "evals": [
                {"id": 1}
            ]
        }))

        review_results = review_evals(skill_dir)
        # Should detect missing fields
        failed_checks = [c for c in review_results["checks"] if not c["passed"]]
        assert len(failed_checks) > 0

    def test_eval_with_empty_prompt(self, tmp_path):
        """Test handling of eval with empty prompt."""
        skill_dir = tmp_path / "emptyprompt-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test
---
Content
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text(json.dumps({
            "evals": [
                {"id": 1, "prompt": "", "expected_output": "Test"}
            ]
        }))

        review_results = review_evals(skill_dir)
        # Empty prompt should fail length check
        prompt_check = next((c for c in review_results["checks"]
                            if "prompt length" in c["name"].lower()), None)
        if prompt_check:
            assert prompt_check["passed"] is False

    def test_eval_with_non_dict_expectations(self, tmp_path):
        """Test handling of eval with non-dict expectations."""
        skill_dir = tmp_path / "badexpectations-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test
---
Content
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text(json.dumps({
            "evals": [
                {
                    "id": 1,
                    "prompt": "Test prompt",
                    "expected_output": "Test",
                    "expectations": "not a list"  # Should be list
                }
            ]
        }))

        # Should not crash
        review_results = review_evals(skill_dir)
        assert isinstance(review_results, dict)

    def test_eval_with_vague_expectations(self, tmp_path):
        """Test handling of eval with vague expectations."""
        skill_dir = tmp_path / "vagueexpectations-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test
---
Content
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text(json.dumps({
            "evals": [
                {
                    "id": 1,
                    "prompt": "Test prompt",
                    "expected_output": "Test",
                    "expectations": [
                        "Do it properly",
                        "Make it good",
                        "Should work correctly"
                    ]
                }
            ]
        }))

        review_results = review_evals(skill_dir)
        # Should detect vague expectations
        testable_check = next((c for c in review_results["checks"]
                              if "testable" in c["name"].lower()), None)
        if testable_check:
            assert testable_check["passed"] is False

    def test_eval_file_invalid_json(self, tmp_path):
        """Test handling of eval file with invalid JSON."""
        skill_dir = tmp_path / "invalidjson-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test
---
Content
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text("{ invalid json content }")

        review_results = review_evals(skill_dir)
        # Should handle invalid JSON gracefully
        assert isinstance(review_results, dict)
        assert review_results["percentage"] == 0


class TestConcurrentExecution:
    """Test concurrent test execution scenarios."""

    def test_concurrent_validation(self, tmp_path):
        """Test running validation concurrently on multiple skills."""
        # Create multiple skill directories
        skill_dirs = []
        for i in range(5):
            skill_dir = tmp_path / f"skill-{i}"
            skill_dir.mkdir()
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text(f"""---
name: test-skill-{i}
description: Test skill number {i}
---
Content {i}
""")
            skill_dirs.append(skill_dir)

        results = []

        def validate_skill_thread(skill_dir):
            return validate_skill(skill_dir)

        # Run validations concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(validate_skill_thread, sd): sd for sd in skill_dirs}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)

        # All should complete successfully
        assert len(results) == 5
        assert all(r[0] is True for r in results)

    def test_concurrent_static_analysis(self, tmp_path):
        """Test running static analysis concurrently."""
        # Create multiple skill directories
        skill_dirs = []
        for i in range(3):
            skill_dir = tmp_path / f"skill-{i}"
            skill_dir.mkdir()
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text(f"""---
name: test-skill-{i}
description: Test skill number {i} for concurrent analysis
---
Content {i}
""")

            evals_dir = skill_dir / "evals"
            evals_dir.mkdir()
            evals_file = evals_dir / "evals.json"
            evals_file.write_text(json.dumps({
                "evals": [{"id": 1, "prompt": f"Test {i}", "expected_output": f"Output {i}"}]
            }))

            skill_dirs.append(skill_dir)

        results = []

        def analyze_skill_thread(skill_dir):
            return analyze_skill(skill_dir)

        # Run analyses concurrently
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(analyze_skill_thread, sd): sd for sd in skill_dirs}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)

        # All should complete successfully
        assert len(results) == 3
        assert all(isinstance(r, dict) for r in results)

    def test_same_skill_concurrent_analysis(self, tmp_path):
        """Test running multiple analyses on the same skill concurrently."""
        skill_dir = tmp_path / "concurrent-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test skill for concurrent analysis
---
Content
""")

        evals_dir = skill_dir / "evals"
        evals_dir.mkdir()
        evals_file = evals_dir / "evals.json"
        evals_file.write_text(json.dumps({
            "evals": [{"id": 1, "prompt": "Test", "expected_output": "Output"}]
        }))

        results = []
        errors = []

        def analyze_skill_thread(skill_dir, thread_id):
            try:
                result = analyze_skill(skill_dir)
                return (thread_id, result, None)
            except Exception as e:
                return (thread_id, None, e)

        # Run 10 concurrent analyses on same skill
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(analyze_skill_thread, skill_dir, i)
                for i in range(10)
            ]
            for future in as_completed(futures):
                thread_id, result, error = future.result()
                if error:
                    errors.append((thread_id, error))
                else:
                    results.append((thread_id, result))

        # All should complete without errors
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 10

        # All results should be consistent
        scores = [r[1]["score"] for r in results]
        assert all(s == scores[0] for s in scores)

    def test_rapid_sequential_validation(self, tmp_path):
        """Test rapid sequential validation (stress test)."""
        skill_dir = tmp_path / "rapid-skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test skill for rapid validation
---
Content
""")

        results = []
        start_time = time.time()

        # Run 100 validations rapidly
        for i in range(100):
            is_valid, message = validate_skill(skill_dir)
            results.append((is_valid, message))

        elapsed = time.time() - start_time

        # All should be valid
        assert all(r[0] is True for r in results)
        # Should complete in reasonable time (< 5 seconds for 100 validations)
        assert elapsed < 5.0


class TestFilesystemEdgeCases:
    """Test filesystem-related edge cases."""

    def test_symlink_to_skill_md(self, tmp_path):
        """Test handling when SKILL.md is a symlink."""
        skill_dir = tmp_path / "symlink-skill"
        skill_dir.mkdir()

        # Create actual file elsewhere
        real_file = tmp_path / "real-skill.md"
        real_file.write_text("""---
name: test-skill
description: Test via symlink
---
Content
""")

        # Create symlink
        skill_md = skill_dir / "SKILL.md"
        try:
            skill_md.symlink_to(real_file)

            is_valid, message = validate_skill(skill_dir)
            assert is_valid is True
        except OSError:
            # Symlinks may not work on all systems
            pytest.skip("Symlinks not supported on this system")

    def test_skill_directory_is_symlink(self, tmp_path):
        """Test handling when skill directory is a symlink."""
        real_skill_dir = tmp_path / "real-skill"
        real_skill_dir.mkdir()
        skill_md = real_skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test via directory symlink
---
Content
""")

        symlink_dir = tmp_path / "symlink-skill"
        try:
            symlink_dir.symlink_to(real_skill_dir)

            is_valid, message = validate_skill(symlink_dir)
            assert is_valid is True
        except OSError:
            pytest.skip("Symlinks not supported on this system")

    def test_very_deep_directory_structure(self, tmp_path):
        """Test handling of very deep directory structure."""
        # Create deeply nested skill directory
        skill_dir = tmp_path / "a" / "b" / "c" / "d" / "e" / "skill"
        skill_dir.mkdir(parents=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test in deep directory
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True

    def test_skill_with_spaces_in_path(self, tmp_path):
        """Test handling of spaces in directory path."""
        skill_dir = tmp_path / "my skill directory"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test with spaces in path
---
Content
""")

        is_valid, message = validate_skill(skill_dir)
        assert is_valid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
