#!/usr/bin/env python3
"""
Unit tests for run_comparison.py.

Tests cover:
- prepare_comparison() function
- cleanup_comparison() function
- Eval file handling
- Edge cases and error handling

Usage: python -m pytest scripts/tests/test_run_comparison.py -v
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from run_comparison import prepare_comparison, cleanup_comparison, main


class TestPrepareComparisonBasic:
    """Test basic prepare_comparison functionality."""

    def test_prepare_comparison_basic(self, tmp_path):
        """Test basic comparison preparation."""
        eval_set = {
            "eval_name": "test-eval",
            "skill_name": "test-skill",
            "evals": [
                {"id": 1, "prompt": "Test prompt", "expectations": ["Expected output"]}
            ]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert manifest["skill_name"] == "test-skill"
        assert manifest["skill_path"] == str(skill_path)
        assert manifest["evals_run"] == 1
        assert "timestamp" in manifest
        assert "results" in manifest
        assert len(manifest["results"]) == 1

    def test_prepare_comparison_creates_output_dir(self, tmp_path):
        """Test that output directory is created."""
        eval_set = {
            "eval_name": "test-eval",
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "new-output"

        prepare_comparison(eval_set, skill_path, output_dir)

        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_prepare_comparison_creates_eval_dirs(self, tmp_path):
        """Test that eval output directories are created."""
        eval_set = {
            "eval_name": "test-eval",
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        prepare_comparison(eval_set, skill_path, output_dir)

        eval_dir = output_dir / "eval-1-test-eval"
        assert eval_dir.exists()
        assert (eval_dir / "with_skill").exists()
        assert (eval_dir / "without_skill").exists()
        assert (eval_dir / "with_skill" / "outputs").exists()
        assert (eval_dir / "without_skill" / "outputs").exists()

    def test_prepare_comparison_creates_metadata(self, tmp_path):
        """Test that eval metadata is created."""
        eval_set = {
            "eval_name": "test-eval",
            "skill_name": "test-skill",
            "evals": [
                {"id": 1, "prompt": "Test prompt", "expectations": ["Expected"]}
            ]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        prepare_comparison(eval_set, skill_path, output_dir)

        eval_dir = output_dir / "eval-1-test-eval"
        metadata_file = eval_dir / "eval_metadata.json"
        assert metadata_file.exists()

        metadata = json.loads(metadata_file.read_text())
        assert metadata["eval_id"] == 1
        assert metadata["eval_name"] == "test-eval"
        assert metadata["prompt"] == "Test prompt"
        assert metadata["expectations"] == ["Expected"]
        assert metadata["skill_path"] == str(skill_path)
        assert "timestamp" in metadata
        assert metadata["status"] == "pending"
        assert metadata["comparison_type"] == "with_vs_without_skill"

    def test_prepare_comparison_creates_manifest(self, tmp_path):
        """Test that manifest file is created."""
        eval_set = {
            "eval_name": "test-eval",
            "skill_name": "test-skill",
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        prepare_comparison(eval_set, skill_path, output_dir)

        manifest_file = output_dir / "manifest.json"
        assert manifest_file.exists()

        manifest = json.loads(manifest_file.read_text())
        assert manifest["skill_name"] == "test-skill"
        assert manifest["evals_run"] == 1
        assert manifest["comparison_type"] == "with_vs_without_skill"


class TestEvalFileHandling:
    """Test eval file handling in prepare_comparison."""

    def test_prepare_comparison_nested_evals_format(self, tmp_path):
        """Test handling of nested evals format."""
        eval_set = {
            "eval_name": "nested-eval",
            "skill_name": "test-skill",
            "evals": [
                {"id": 1, "prompt": "Prompt 1", "expectations": []},
                {"id": 2, "prompt": "Prompt 2", "expectations": []}
            ]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert manifest["evals_run"] == 2
        assert len(manifest["results"]) == 2

    def test_prepare_comparison_list_format(self, tmp_path):
        """Test handling of list format (no evals key)."""
        eval_set = [
            {"id": 1, "prompt": "Prompt 1", "expectations": []},
            {"id": 2, "prompt": "Prompt 2", "expectations": []}
        ]
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert manifest["evals_run"] == 2
        assert len(manifest["results"]) == 2

    def test_prepare_comparison_default_eval_name(self, tmp_path):
        """Test default eval name when not provided."""
        eval_set = {
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        eval_dir = output_dir / "eval-1-comparison"
        assert eval_dir.exists()

    def test_prepare_comparison_default_skill_name(self, tmp_path):
        """Test default skill name when not provided."""
        eval_set = {
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert manifest["skill_name"] == "unknown"

    def test_prepare_comparison_default_id(self, tmp_path):
        """Test default eval id when not provided."""
        eval_set = {
            "evals": [{"prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        # Default id should be 1
        eval_dir = output_dir / "eval-1-comparison"
        assert eval_dir.exists()

    def test_prepare_comparison_multiple_evals(self, tmp_path):
        """Test preparation with multiple evals."""
        eval_set = {
            "eval_name": "multi-eval",
            "evals": [
                {"id": 1, "prompt": "Prompt 1", "expectations": ["Exp 1"]},
                {"id": 2, "prompt": "Prompt 2", "expectations": ["Exp 2"]},
                {"id": 3, "prompt": "Prompt 3", "expectations": ["Exp 3"]}
            ]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert manifest["evals_run"] == 3

        for i in range(1, 4):
            eval_dir = output_dir / f"eval-{i}-multi-eval"
            assert eval_dir.exists()
            metadata = json.loads((eval_dir / "eval_metadata.json").read_text())
            assert metadata["eval_id"] == i

    def test_prepare_comparison_result_structure(self, tmp_path):
        """Test result structure in manifest."""
        eval_set = {
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        result = manifest["results"][0]
        assert "eval_id" in result
        assert "eval_name" in result
        assert "status" in result
        assert "output_dir" in result
        assert "prompt" in result
        assert "with_skill_dir" in result
        assert "without_skill_dir" in result

        assert result["status"] == "pending"
        assert result["eval_id"] == 1


class TestCleanupComparison:
    """Test cleanup_comparison function."""

    def test_cleanup_comparison_basic(self, tmp_path):
        """Test basic cleanup functionality."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Create eval directories
        eval_dir1 = output_dir / "eval-1-test"
        eval_dir1.mkdir()
        eval_dir2 = output_dir / "eval-2-test"
        eval_dir2.mkdir()

        # Create non-eval directory (should not be cleaned)
        other_dir = output_dir / "other"
        other_dir.mkdir()

        result = cleanup_comparison(output_dir)

        assert result["count"] == 2
        assert not eval_dir1.exists()
        assert not eval_dir2.exists()
        assert other_dir.exists()

    def test_cleanup_comparison_removes_manifest(self, tmp_path):
        """Test that cleanup removes manifest files."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Create eval directory
        eval_dir = output_dir / "eval-1-test"
        eval_dir.mkdir()

        # Create manifest files
        manifest1 = output_dir / "manifest.json"
        manifest1.write_text("{}")
        manifest2 = output_dir / "comparison_results.json"
        manifest2.write_text("{}")

        result = cleanup_comparison(output_dir)

        assert not manifest1.exists()
        assert not manifest2.exists()

    def test_cleanup_comparison_empty_dir(self, tmp_path):
        """Test cleanup of empty directory."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        result = cleanup_comparison(output_dir)

        assert result["count"] == 0
        assert result["cleaned"] == []
        assert output_dir.exists()

    def test_cleanup_comparison_nonexistent_dir(self, tmp_path):
        """Test cleanup of nonexistent directory."""
        output_dir = tmp_path / "nonexistent"

        result = cleanup_comparison(output_dir)

        assert result["count"] == 0
        assert result["cleaned"] == []

    def test_cleanup_comparison_mixed_files(self, tmp_path):
        """Test cleanup with mixed files and directories."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Create eval directories
        (output_dir / "eval-1-test").mkdir()
        (output_dir / "eval-2-test").mkdir()

        # Create other files
        (output_dir / "manifest.json").write_text("{}")
        (output_dir / "other.txt").write_text("other")
        (output_dir / "comparison_results.json").write_text("{}")

        result = cleanup_comparison(output_dir)

        assert result["count"] == 4  # 2 eval dirs + 2 manifest files
        assert not (output_dir / "eval-1-test").exists()
        assert not (output_dir / "eval-2-test").exists()
        assert not (output_dir / "manifest.json").exists()
        assert not (output_dir / "comparison_results.json").exists()
        assert (output_dir / "other.txt").exists()

    def test_cleanup_comparison_nested_eval_dirs(self, tmp_path):
        """Test cleanup with nested eval directories."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Create nested eval directory
        eval_dir = output_dir / "eval-1-test"
        eval_dir.mkdir()
        (eval_dir / "with_skill").mkdir()
        (eval_dir / "without_skill").mkdir()
        (eval_dir / "eval_metadata.json").write_text("{}")

        result = cleanup_comparison(output_dir)

        assert result["count"] == 1  # Only the top-level eval dir
        assert not eval_dir.exists()


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_prepare_comparison_empty_evals(self, tmp_path):
        """Test preparation with empty evals list."""
        eval_set = {
            "eval_name": "empty-eval",
            "evals": []
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert manifest["evals_run"] == 0
        assert manifest["results"] == []

    def test_prepare_comparison_missing_expectations(self, tmp_path):
        """Test handling of missing expectations."""
        eval_set = {
            "evals": [{"id": 1, "prompt": "Test"}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        eval_dir = output_dir / "eval-1-comparison"
        metadata = json.loads((eval_dir / "eval_metadata.json").read_text())
        assert metadata["expectations"] == []

    def test_prepare_comparison_missing_prompt(self, tmp_path):
        """Test handling of missing prompt."""
        eval_set = {
            "evals": [{"id": 1, "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        # Should handle missing prompt gracefully
        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        eval_dir = output_dir / "eval-1-comparison"
        metadata = json.loads((eval_dir / "eval_metadata.json").read_text())
        assert metadata["prompt"] is None

    def test_prepare_comparison_timestamp_format(self, tmp_path):
        """Test timestamp format in metadata."""
        eval_set = {
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        prepare_comparison(eval_set, skill_path, output_dir)

        eval_dir = output_dir / "eval-1-comparison"
        metadata = json.loads((eval_dir / "eval_metadata.json").read_text())

        # Timestamp should be ISO format
        timestamp = metadata["timestamp"]
        # Should be parseable as datetime
        datetime.fromisoformat(timestamp)

    def test_prepare_comparison_skill_path_in_metadata(self, tmp_path):
        """Test skill path is stored in metadata."""
        eval_set = {
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "my-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        prepare_comparison(eval_set, skill_path, output_dir)

        eval_dir = output_dir / "eval-1-comparison"
        metadata = json.loads((eval_dir / "eval_metadata.json").read_text())

        assert metadata["skill_path"] == str(skill_path)

    def test_cleanup_comparison_preserves_non_eval_dirs(self, tmp_path):
        """Test that cleanup preserves non-eval directories."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Create various directories
        (output_dir / "eval-1-test").mkdir()
        (output_dir / "results").mkdir()
        (output_dir / "logs").mkdir()
        (output_dir / "eval-cache").mkdir()  # Starts with eval but not eval-

        result = cleanup_comparison(output_dir)

        assert not (output_dir / "eval-1-test").exists()
        assert (output_dir / "results").exists()
        assert (output_dir / "logs").exists()
        assert (output_dir / "eval-cache").exists()

    def test_prepare_comparison_special_characters_in_name(self, tmp_path):
        """Test handling of special characters in eval name."""
        eval_set = {
            "eval_name": "test-eval with spaces & special",
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        # Should handle special characters in directory names
        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        eval_dir = output_dir / "eval-1-test-eval with spaces & special"
        assert eval_dir.exists()

    def test_prepare_comparison_very_long_eval_name(self, tmp_path):
        """Test handling of very long eval name."""
        eval_set = {
            "eval_name": "A" * 200,
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }
        skill_path = tmp_path / "test-skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        # Should handle long names
        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        eval_dir = output_dir / f"eval-1-{'A' * 200}"
        assert eval_dir.exists()

    def test_cleanup_comparison_symlinks(self, tmp_path):
        """Test cleanup with symlinks."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Create a symlink to eval directory
        real_dir = tmp_path / "real-eval"
        real_dir.mkdir()
        eval_link = output_dir / "eval-1-test"
        eval_link.symlink_to(real_dir)

        result = cleanup_comparison(output_dir)

        # Symlink should be removed
        assert not eval_link.exists()
        # But real directory should remain
        assert real_dir.exists()


class TestManifestStructure:
    """Test manifest structure in prepare_comparison."""

    def test_manifest_has_timestamp(self, tmp_path):
        """Test manifest includes timestamp."""
        eval_set = {"evals": [{"id": 1, "prompt": "Test", "expectations": []}]}
        skill_path = tmp_path / "skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert "timestamp" in manifest
        # Should be ISO format
        datetime.fromisoformat(manifest["timestamp"])

    def test_manifest_has_output_base_dir(self, tmp_path):
        """Test manifest includes output base directory."""
        eval_set = {"evals": [{"id": 1, "prompt": "Test", "expectations": []}]}
        skill_path = tmp_path / "skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert manifest["output_base_dir"] == str(output_dir)

    def test_result_has_eval_id(self, tmp_path):
        """Test result includes eval_id."""
        eval_set = {"evals": [{"id": 42, "prompt": "Test", "expectations": []}]}
        skill_path = tmp_path / "skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert manifest["results"][0]["eval_id"] == 42

    def test_result_has_status_pending(self, tmp_path):
        """Test result has pending status."""
        eval_set = {"evals": [{"id": 1, "prompt": "Test", "expectations": []}]}
        skill_path = tmp_path / "skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert manifest["results"][0]["status"] == "pending"

    def test_result_has_prompt(self, tmp_path):
        """Test result includes prompt."""
        eval_set = {"evals": [{"id": 1, "prompt": "My test prompt", "expectations": []}]}
        skill_path = tmp_path / "skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        assert manifest["results"][0]["prompt"] == "My test prompt"

    def test_result_directories_structure(self, tmp_path):
        """Test result directories are properly structured."""
        eval_set = {"evals": [{"id": 1, "prompt": "Test", "expectations": []}]}
        skill_path = tmp_path / "skill"
        skill_path.mkdir()
        output_dir = tmp_path / "output"

        manifest = prepare_comparison(eval_set, skill_path, output_dir)

        result = manifest["results"][0]
        assert "with_skill" in result["with_skill_dir"]
        assert "without_skill" in result["without_skill_dir"]
        assert result["with_skill_dir"] != result["without_skill_dir"]


class TestMainFunction:
    """Test main function."""

    def test_main_prepare_mode(self, tmp_path, capsys):
        """Test main function in prepare mode."""
        eval_file = tmp_path / "evals.json"
        eval_file.write_text(json.dumps({
            "eval_name": "test-eval",
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }))

        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: test\n---\nContent")

        output_dir = tmp_path / "output"

        import sys
        original_argv = sys.argv
        sys.argv = [
            "run_comparison.py",
            "--eval-set", str(eval_file),
            "--skill-path", str(skill_dir),
            "--output-dir", str(output_dir)
        ]

        try:
            result = main()
        except SystemExit as e:
            result = e.code
        finally:
            sys.argv = original_argv

        assert result == 0
        assert output_dir.exists()
        assert (output_dir / "manifest.json").exists()

        captured = capsys.readouterr()
        assert "Comparison Test Preparation Complete" in captured.out

    def test_main_cleanup_mode(self, tmp_path, capsys):
        """Test main function in cleanup mode."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        (output_dir / "eval-1-test").mkdir()
        (output_dir / "manifest.json").write_text("{}")

        import sys
        original_argv = sys.argv
        sys.argv = [
            "run_comparison.py",
            "--output-dir", str(output_dir),
            "--cleanup"
        ]

        try:
            result = main()
        except SystemExit as e:
            result = e.code
        finally:
            sys.argv = original_argv

        assert result == 0
        assert not (output_dir / "eval-1-test").exists()
        assert not (output_dir / "manifest.json").exists()

        captured = capsys.readouterr()
        assert "CLEANUP COMPLETE" in captured.out

    def test_main_missing_eval_set(self, tmp_path, capsys):
        """Test main function without eval-set in prepare mode."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        output_dir = tmp_path / "output"

        import sys
        original_argv = sys.argv
        sys.argv = [
            "run_comparison.py",
            "--skill-path", str(skill_dir),
            "--output-dir", str(output_dir)
        ]

        try:
            result = main()
        except SystemExit as e:
            result = e.code
        finally:
            sys.argv = original_argv

        assert result == 1
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_main_missing_skill_path(self, tmp_path, capsys):
        """Test main function without skill-path in prepare mode."""
        eval_file = tmp_path / "evals.json"
        eval_file.write_text(json.dumps({"evals": []}))

        output_dir = tmp_path / "output"

        import sys
        original_argv = sys.argv
        sys.argv = [
            "run_comparison.py",
            "--eval-set", str(eval_file),
            "--output-dir", str(output_dir)
        ]

        try:
            result = main()
        except SystemExit as e:
            result = e.code
        finally:
            sys.argv = original_argv

        assert result == 1
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_main_no_skill_md(self, tmp_path, capsys):
        """Test main function without SKILL.md."""
        eval_file = tmp_path / "evals.json"
        eval_file.write_text(json.dumps({"evals": []}))

        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        # No SKILL.md file

        output_dir = tmp_path / "output"

        import sys
        original_argv = sys.argv
        sys.argv = [
            "run_comparison.py",
            "--eval-set", str(eval_file),
            "--skill-path", str(skill_dir),
            "--output-dir", str(output_dir)
        ]

        try:
            result = main()
        except SystemExit as e:
            result = e.code
        finally:
            sys.argv = original_argv

        assert result == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err
        assert "SKILL.md" in captured.err

    def test_main_cleanup_no_eval_set_required(self, tmp_path, capsys):
        """Test that cleanup mode doesn't require eval-set."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        import sys
        original_argv = sys.argv
        sys.argv = [
            "run_comparison.py",
            "--output-dir", str(output_dir),
            "--cleanup"
        ]

        try:
            result = main()
        except SystemExit as e:
            result = e.code
        finally:
            sys.argv = original_argv

        assert result == 0

    def test_main_cleanup_no_skill_path_required(self, tmp_path, capsys):
        """Test that cleanup mode doesn't require skill-path."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        import sys
        original_argv = sys.argv
        sys.argv = [
            "run_comparison.py",
            "--output-dir", str(output_dir),
            "--cleanup"
        ]

        try:
            result = main()
        except SystemExit as e:
            result = e.code
        finally:
            sys.argv = original_argv

        assert result == 0

    def test_main_creates_output_dir(self, tmp_path):
        """Test that main creates output directory."""
        eval_file = tmp_path / "evals.json"
        eval_file.write_text(json.dumps({
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }))

        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: test\n---\nContent")

        output_dir = tmp_path / "new-output"

        import sys
        original_argv = sys.argv
        sys.argv = [
            "run_comparison.py",
            "--eval-set", str(eval_file),
            "--skill-path", str(skill_dir),
            "--output-dir", str(output_dir)
        ]

        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.argv = original_argv

        assert output_dir.exists()

    def test_main_output_json(self, tmp_path, capsys):
        """Test main function outputs JSON."""
        eval_file = tmp_path / "evals.json"
        eval_file.write_text(json.dumps({
            "eval_name": "test",
            "evals": [{"id": 1, "prompt": "Test", "expectations": []}]
        }))

        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: test\n---\nContent")

        output_dir = tmp_path / "output"

        import sys
        original_argv = sys.argv
        sys.argv = [
            "run_comparison.py",
            "--eval-set", str(eval_file),
            "--skill-path", str(skill_dir),
            "--output-dir", str(output_dir)
        ]

        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        # Should output valid JSON
        output = json.loads(captured.out)
        assert "skill_name" in output
        assert "evals_run" in output
        assert "results" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
