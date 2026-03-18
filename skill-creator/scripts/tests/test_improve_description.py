#!/usr/bin/env python3
"""
Unit tests for improve_description.py.

Tests cover:
- Description improvement logic
- Skill parsing
- Iteration handling
- Edge cases and error handling

Usage: python -m pytest scripts/tests/test_improve_description.py -v
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from improve_description import _call_claude, improve_description, main


class TestCallClaude:
    """Test _call_claude function."""

    def test_call_claude_basic(self):
        """Test basic claude call without model."""
        with patch("improve_description.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Response", stderr="")

            result = _call_claude("Test prompt", None)

            assert result == "Response"
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert cmd == ["claude", "-p", "--output-format", "text"]

    def test_call_claude_with_model(self):
        """Test claude call with specific model."""
        with patch("improve_description.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Response", stderr="")

            result = _call_claude("Test prompt", "claude-3-opus-20240229")

            assert result == "Response"
            cmd = mock_run.call_args[0][0]
            assert "--model" in cmd
            assert "claude-3-opus-20240229" in cmd

    def test_call_claude_nonzero_exit(self):
        """Test handling of nonzero exit code."""
        with patch("improve_description.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout="",
                stderr="Error occurred"
            )

            with pytest.raises(RuntimeError, match="exited 1"):
                _call_claude("Test prompt", None)

    def test_call_claude_removes_claudecode_env(self):
        """Test that CLAUDECODE env var is removed."""
        with patch("improve_description.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Response", stderr="")

            with patch("improve_description.os.environ", {"CLAUDECODE": "1", "OTHER": "value"}):
                _call_claude("Test prompt", None)

            # Check that env was passed without CLAUDECODE
            env = mock_run.call_args[1]["env"]
            assert "CLAUDECODE" not in env
            assert "OTHER" in env

    def test_call_claude_with_timeout(self):
        """Test claude call with custom timeout."""
        with patch("improve_description.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Response", stderr="")

            _call_claude("Test prompt", None, timeout=600)

            assert mock_run.call_args[1]["timeout"] == 600

    def test_call_claude_default_timeout(self):
        """Test claude call with default timeout."""
        with patch("improve_description.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Response", stderr="")

            _call_claude("Test prompt", None)

            assert mock_run.call_args[1]["timeout"] == 300

    def test_call_claude_input_via_stdin(self):
        """Test that prompt is passed via stdin."""
        with patch("improve_description.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Response", stderr="")

            _call_claude("Test prompt content", None)

            assert mock_run.call_args[1]["input"] == "Test prompt content"
            assert mock_run.call_args[1]["capture_output"] is True
            assert mock_run.call_args[1]["text"] is True


class TestImproveDescriptionBasic:
    """Test basic improve_description functionality."""

    def test_improve_description_basic(self):
        """Test basic description improvement."""
        eval_results = {
            "results": [
                {"query": "Query 1", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1},
                {"query": "Query 2", "should_trigger": True, "pass": False, "triggers": 0, "runs": 1}
            ],
            "summary": {"passed": 1, "failed": 1, "total": 2},
            "description": "Original description"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved description</new_description>'

            result = improve_description(
                skill_name="test-skill",
                skill_content="# Skill content",
                current_description="Original description",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == "Improved description"
            mock_claude.assert_called_once()

    def test_improve_description_no_xml_tags(self):
        """Test handling of response without XML tags."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "failed": 0, "total": 1},
            "description": "Original"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = "Just plain text response"

            result = improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Original",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == "Just plain text response"

    def test_improve_description_with_quotes(self):
        """Test handling of quoted description."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Original"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>"Quoted description"</new_description>'

            result = improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Original",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == "Quoted description"

    def test_improve_description_with_test_results(self):
        """Test improvement with test/holdout results."""
        eval_results = {
            "results": [{"query": "Train", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1}],
            "summary": {"passed": 1, "total": 1},
            "description": "Original"
        }
        test_results = {
            "results": [{"query": "Test", "should_trigger": True, "pass": False, "triggers": 0, "runs": 1}],
            "summary": {"passed": 0, "total": 1}
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Original",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet",
                test_results=test_results
            )

            # Check that test score is included in prompt
            prompt = mock_claude.call_args[0][0]
            assert "Test:" in prompt


class TestSkillParsing:
    """Test skill parsing in improve_description."""

    def test_improve_description_with_history(self):
        """Test improvement with previous attempts history."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current description"
        }
        history = [
            {
                "description": "Previous attempt 1",
                "passed": 3,
                "total": 5,
                "results": [
                    {"query": "Query 1", "pass": True, "triggers": 1, "runs": 1}
                ]
            }
        ]

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>New attempt</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=history,
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "PREVIOUS ATTEMPTS" in prompt
            assert "Previous attempt 1" in prompt

    def test_improve_description_with_test_results_in_history(self):
        """Test history with test results."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }
        history = [
            {
                "description": "Previous",
                "train_passed": 4,
                "train_total": 5,
                "test_passed": 3,
                "test_total": 5,
                "results": []
            }
        ]

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>New</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=history,
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "train=" in prompt
            assert "test=" in prompt

    def test_improve_description_with_note_in_history(self):
        """Test history with notes."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }
        history = [
            {
                "description": "Previous",
                "passed": 3,
                "total": 5,
                "note": "This attempt failed because..."
            }
        ]

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>New</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=history,
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "Note:" in prompt
            assert "This attempt failed because..." in prompt


class TestIterationHandling:
    """Test iteration handling in improve_description."""

    def test_improve_description_with_iteration(self):
        """Test improvement with iteration number."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            with patch("improve_description.Path") as mock_path:
                mock_file = MagicMock()
                mock_path.return_value = mock_file

                mock_claude.return_value = '<new_description>New</new_description>'

                improve_description(
                    skill_name="test-skill",
                    skill_content="Content",
                    current_description="Current",
                    eval_results=eval_results,
                    history=[],
                    model="claude-3-sonnet",
                    iteration=5,
                    log_dir=Path("/tmp/logs")
                )

                # Check log file was created with iteration number
                assert mock_file.write_text.called
                log_content = mock_file.write_text.call_args[0][0]
                log_data = json.loads(log_content)
                assert log_data["iteration"] == 5

    def test_improve_description_without_iteration(self):
        """Test improvement without iteration number."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            with patch("improve_description.Path") as mock_path:
                mock_file = MagicMock()
                mock_path.return_value = mock_file

                mock_claude.return_value = '<new_description>New</new_description>'

                improve_description(
                    skill_name="test-skill",
                    skill_content="Content",
                    current_description="Current",
                    eval_results=eval_results,
                    history=[],
                    model="claude-3-sonnet",
                    log_dir=Path("/tmp/logs")
                )

                # Check log file was created
                assert mock_file.write_text.called
                log_content = mock_file.write_text.call_args[0][0]
                log_data = json.loads(log_content)
                assert log_data["iteration"] is None

    def test_improve_description_creates_log_dir(self):
        """Test that log directory is created."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            with patch("improve_description.Path") as mock_path:
                mock_file = MagicMock()
                mock_dir = MagicMock()
                mock_path.return_value = mock_file
                mock_path.side_effect = lambda x, **kwargs: mock_dir if "logs" in str(x) else mock_file

                mock_claude.return_value = '<new_description>New</new_description>'

                improve_description(
                    skill_name="test-skill",
                    skill_content="Content",
                    current_description="Current",
                    eval_results=eval_results,
                    history=[],
                    model="claude-3-sonnet",
                    log_dir=Path("/tmp/logs")
                )

                # Check mkdir was called
                assert mock_dir.mkdir.called
                assert mock_dir.mkdir.call_args[1]["parents"] is True
                assert mock_dir.mkdir.call_args[1]["exist_ok"] is True


class TestFailedTriggers:
    """Test failed trigger handling."""

    def test_improve_description_with_failed_triggers(self):
        """Test improvement with failed triggers."""
        eval_results = {
            "results": [
                {"query": "Failed query", "should_trigger": True, "pass": False, "triggers": 0, "runs": 1}
            ],
            "summary": {"passed": 0, "failed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "FAILED TO TRIGGER" in prompt
            assert "Failed query" in prompt

    def test_improve_description_with_false_triggers(self):
        """Test improvement with false triggers."""
        eval_results = {
            "results": [
                {"query": "False trigger", "should_trigger": False, "pass": False, "triggers": 1, "runs": 1}
            ],
            "summary": {"passed": 0, "failed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "FALSE TRIGGERS" in prompt
            assert "False trigger" in prompt

    def test_improve_description_with_both_failures(self):
        """Test improvement with both types of failures."""
        eval_results = {
            "results": [
                {"query": "Failed", "should_trigger": True, "pass": False, "triggers": 0, "runs": 1},
                {"query": "False", "should_trigger": False, "pass": False, "triggers": 1, "runs": 1}
            ],
            "summary": {"passed": 0, "failed": 2, "total": 2},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "FAILED TO TRIGGER" in prompt
            assert "FALSE TRIGGERS" in prompt


class TestDescriptionLengthHandling:
    """Test description length handling."""

    def test_improve_description_under_limit(self):
        """Test handling of description under character limit."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            short_desc = "A" * 500
            mock_claude.return_value = f'<new_description>{short_desc}</new_description>'

            result = improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == short_desc
            # Should only call claude once
            assert mock_claude.call_count == 1

    def test_improve_description_over_limit(self):
        """Test handling of description over character limit."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            long_desc = "A" * 1100
            short_desc = "B" * 500

            # First call returns long description
            # Second call returns short description
            mock_claude.side_effect = [
                f'<new_description>{long_desc}</new_description>',
                f'<new_description>{short_desc}</new_description>'
            ]

            result = improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == short_desc
            # Should call claude twice
            assert mock_claude.call_count == 2

    def test_improve_description_over_limit_transcript(self):
        """Test transcript includes rewrite info when over limit."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            with patch("improve_description.Path") as mock_path:
                mock_file = MagicMock()
                mock_path.return_value = mock_file

                long_desc = "A" * 1100
                short_desc = "B" * 500

                mock_claude.side_effect = [
                    f'<new_description>{long_desc}</new_description>',
                    f'<new_description>{short_desc}</new_description>'
                ]

                improve_description(
                    skill_name="test-skill",
                    skill_content="Content",
                    current_description="Current",
                    eval_results=eval_results,
                    history=[],
                    model="claude-3-sonnet",
                    log_dir=Path("/tmp/logs")
                )

                # Check transcript includes rewrite info
                log_content = mock_file.write_text.call_args[0][0]
                log_data = json.loads(log_content)
                assert "rewrite_prompt" in log_data
                assert "rewrite_response" in log_data
                assert "rewrite_description" in log_data
                assert "rewrite_char_count" in log_data


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_improve_description_empty_results(self):
        """Test improvement with empty results."""
        eval_results = {
            "results": [],
            "summary": {"passed": 0, "failed": 0, "total": 0},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            result = improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == "Improved"

    def test_improve_description_no_summary_key(self):
        """Test handling of missing summary key."""
        eval_results = {
            "results": [],
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            # Should handle missing summary gracefully
            with pytest.raises((KeyError, TypeError)):
                improve_description(
                    skill_name="test-skill",
                    skill_content="Content",
                    current_description="Current",
                    eval_results=eval_results,
                    history=[],
                    model="claude-3-sonnet"
                )

    def test_improve_description_whitespace_handling(self):
        """Test whitespace handling in description."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>  Trimmed description  </new_description>'

            result = improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == "Trimmed description"

    def test_improve_description_multiline(self):
        """Test handling of multiline descriptions."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            multiline = "Line 1\nLine 2\nLine 3"
            mock_claude.return_value = f'<new_description>{multiline}</new_description>'

            result = improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == multiline

    def test_improve_description_special_characters(self):
        """Test handling of special characters."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            special = "Special: <>&\"'"
            mock_claude.return_value = f'<new_description>{special}</new_description>'

            result = improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == special

    def test_improve_description_unicode(self):
        """Test handling of unicode characters."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            unicode_text = "测试 🎉 émojis"
            mock_claude.return_value = f'<new_description>{unicode_text}</new_description>'

            result = improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == unicode_text

    def test_improve_description_no_skill_content(self):
        """Test handling of empty skill content."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            result = improve_description(
                skill_name="test-skill",
                skill_content="",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == "Improved"
            # Check skill_content is in prompt
            prompt = mock_claude.call_args[0][0]
            assert "<skill_content>" in prompt

    def test_improve_description_long_skill_content(self):
        """Test handling of long skill content."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }
        long_content = "A" * 10000

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            result = improve_description(
                skill_name="test-skill",
                skill_content=long_content,
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            assert result == "Improved"


class TestPromptContent:
    """Test prompt content generation."""

    def test_prompt_includes_skill_name(self):
        """Test that prompt includes skill name."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            improve_description(
                skill_name="my-test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "my-test-skill" in prompt

    def test_prompt_includes_current_description(self):
        """Test that prompt includes current description."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current description text"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current description text",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "Current description text" in prompt
            assert "<current_description>" in prompt

    def test_prompt_includes_scores_summary(self):
        """Test that prompt includes scores summary."""
        eval_results = {
            "results": [],
            "summary": {"passed": 8, "failed": 2, "total": 10},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "Train:" in prompt
            assert "8/" in prompt
            assert "10" in prompt

    def test_prompt_includes_tips(self):
        """Test that prompt includes optimization tips."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "100-200 words" in prompt
            assert "1024 characters" in prompt
            assert "Avoid overfitting" in prompt

    def test_prompt_includes_xml_tags(self):
        """Test that prompt uses XML tags for structure."""
        eval_results = {
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }

        with patch("improve_description._call_claude") as mock_claude:
            mock_claude.return_value = '<new_description>Improved</new_description>'

            improve_description(
                skill_name="test-skill",
                skill_content="Content",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-3-sonnet"
            )

            prompt = mock_claude.call_args[0][0]
            assert "<current_description>" in prompt
            assert "</current_description>" in prompt
            assert "<skill_content>" in prompt
            assert "</skill_content>" in prompt
            assert "<new_description>" in prompt


class TestMainFunction:
    """Test main function."""

    def test_main_basic(self, tmp_path):
        """Test main function basic execution."""
        eval_file = tmp_path / "eval_results.json"
        eval_file.write_text(json.dumps({
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }))

        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("""---
name: test-skill
description: Current
---
Content
""")

        import sys
        original_argv = sys.argv
        sys.argv = [
            "improve_description.py",
            "--eval-results", str(eval_file),
            "--skill-path", str(skill_dir),
            "--model", "claude-3-sonnet"
        ]

        try:
            with patch("improve_description._call_claude") as mock_claude:
                mock_claude.return_value = '<new_description>Improved</new_description>'
                main()
        except SystemExit:
            pass
        finally:
            sys.argv = original_argv

    def test_main_with_history(self, tmp_path):
        """Test main function with history file."""
        eval_file = tmp_path / "eval_results.json"
        eval_file.write_text(json.dumps({
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }))

        history_file = tmp_path / "history.json"
        history_file.write_text(json.dumps([
            {"description": "Previous", "passed": 3, "total": 5}
        ]))

        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("""---
name: test-skill
description: Current
---
Content
""")

        import sys
        original_argv = sys.argv
        sys.argv = [
            "improve_description.py",
            "--eval-results", str(eval_file),
            "--skill-path", str(skill_dir),
            "--history", str(history_file),
            "--model", "claude-3-sonnet"
        ]

        try:
            with patch("improve_description._call_claude") as mock_claude:
                mock_claude.return_value = '<new_description>Improved</new_description>'
                main()
        except SystemExit:
            pass
        finally:
            sys.argv = original_argv

    def test_main_no_skill_md(self, tmp_path, capsys):
        """Test main function without SKILL.md."""
        eval_file = tmp_path / "eval_results.json"
        eval_file.write_text(json.dumps({
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }))

        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()

        import sys
        original_argv = sys.argv
        sys.argv = [
            "improve_description.py",
            "--eval-results", str(eval_file),
            "--skill-path", str(skill_dir),
            "--model", "claude-3-sonnet"
        ]

        try:
            main()
        except SystemExit as e:
            assert e.code == 1
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Error" in captured.err

    def test_main_verbose(self, tmp_path, capsys):
        """Test main function with verbose flag."""
        eval_file = tmp_path / "eval_results.json"
        eval_file.write_text(json.dumps({
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }))

        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("""---
name: test-skill
description: Current
---
Content
""")

        import sys
        original_argv = sys.argv
        sys.argv = [
            "improve_description.py",
            "--eval-results", str(eval_file),
            "--skill-path", str(skill_dir),
            "--model", "claude-3-sonnet",
            "--verbose"
        ]

        try:
            with patch("improve_description._call_claude") as mock_claude:
                mock_claude.return_value = '<new_description>Improved</new_description>'
                main()
        except SystemExit:
            pass
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Current:" in captured.err
        assert "Score:" in captured.err
        assert "Improved:" in captured.err

    def test_main_output_json(self, tmp_path, capsys):
        """Test main function outputs JSON."""
        eval_file = tmp_path / "eval_results.json"
        eval_file.write_text(json.dumps({
            "results": [],
            "summary": {"passed": 1, "total": 1},
            "description": "Current"
        }))

        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("""---
name: test-skill
description: Current
---
Content
""")

        import sys
        original_argv = sys.argv
        sys.argv = [
            "improve_description.py",
            "--eval-results", str(eval_file),
            "--skill-path", str(skill_dir),
            "--model", "claude-3-sonnet"
        ]

        try:
            with patch("improve_description._call_claude") as mock_claude:
                mock_claude.return_value = '<new_description>Improved</new_description>'
                main()
        except SystemExit:
            pass
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        # Should output valid JSON
        output = json.loads(captured.out)
        assert "description" in output
        assert "history" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
