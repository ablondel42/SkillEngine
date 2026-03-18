#!/usr/bin/env python3
"""
Unit tests for generate_report.py.

Tests cover:
- generate_html() function
- HTML table generation
- Column handling
- Edge cases and error handling

Usage: python -m pytest scripts/tests/test_generate_report.py -v
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_report import generate_html, main


class TestGenerateHtmlBasic:
    """Test basic HTML generation functionality."""

    def test_generate_html_empty_data(self):
        """Test HTML generation with empty data."""
        data = {}
        html = generate_html(data)

        assert "<!DOCTYPE html>" in html
        assert "<html>" in html
        assert "</html>" in html
        assert "<table>" in html
        assert "<tbody>" in html

    def test_generate_html_with_skill_name(self):
        """Test HTML generation with skill name prefix."""
        data = {}
        html = generate_html(data, skill_name="test-skill")

        assert "test-skill \u2014 Skill Description Optimization" in html
        assert "<title>test-skill \u2014 Skill Description Optimization</title>" in html

    def test_generate_html_with_history(self):
        """Test HTML generation with history data."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test description",
                    "passed": 5,
                    "total": 10,
                    "results": [
                        {
                            "query": "Test query 1",
                            "should_trigger": True,
                            "pass": True,
                            "triggers": 1,
                            "runs": 1
                        }
                    ]
                }
            ]
        }
        html = generate_html(data)

        assert "Test description" in html
        assert "Test query 1" in html
        assert "iteration" in html.lower() or "Iter" in html

    def test_generate_html_with_holdout(self):
        """Test HTML generation with holdout value."""
        data = {
            "holdout": 3,
            "history": []
        }
        html = generate_html(data)

        assert "<!DOCTYPE html>" in html

    def test_generate_html_complete_structure(self):
        """Test that HTML has complete structure."""
        data = {}
        html = generate_html(data)

        # Check for required HTML elements
        assert "<head>" in html
        assert "<body>" in html
        assert "<h1>" in html
        assert "<table>" in html
        assert "<thead>" in html
        assert "<tbody>" in html

        # Check for CSS styles
        assert "<style>" in html
        assert "font-family" in html
        assert "background" in html

        # Check for Google Fonts
        assert "fonts.googleapis.com" in html
        assert "Poppins" in html
        assert "Lora" in html


class TestHtmlTableGeneration:
    """Test HTML table generation."""

    def test_table_header_structure(self):
        """Test table header is properly generated."""
        data = {
            "history": [],
            "train_size": 5,
            "test_size": 3
        }
        html = generate_html(data)

        assert "<thead>" in html
        assert "<tr>" in html
        assert "<th>" in html
        assert "Iter" in html
        assert "Train" in html
        assert "Test" in html
        assert "Description" in html

    def test_table_body_with_iterations(self):
        """Test table body with multiple iterations."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "First attempt",
                    "passed": 3,
                    "total": 5
                },
                {
                    "iteration": 2,
                    "description": "Second attempt",
                    "passed": 4,
                    "total": 5
                }
            ]
        }
        html = generate_html(data)

        assert "First attempt" in html
        assert "Second attempt" in html
        assert "1" in html
        assert "2" in html

    def test_table_row_best_iteration(self):
        """Test best iteration row highlighting."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Worse attempt",
                    "train_passed": 3,
                    "train_total": 5,
                    "train_results": []
                },
                {
                    "iteration": 2,
                    "description": "Best attempt",
                    "train_passed": 5,
                    "train_total": 5,
                    "train_results": []
                }
            ]
        }
        html = generate_html(data)

        # Best row should have best-row class
        assert 'class="best-row"' in html

    def test_table_with_train_results(self):
        """Test table generation with train results."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test desc",
                    "train_results": [
                        {
                            "query": "Train query 1",
                            "should_trigger": True,
                            "pass": True,
                            "triggers": 1,
                            "runs": 1
                        },
                        {
                            "query": "Train query 2",
                            "should_trigger": False,
                            "pass": False,
                            "triggers": 1,
                            "runs": 1
                        }
                    ]
                }
            ]
        }
        html = generate_html(data)

        assert "Train query 1" in html
        assert "Train query 2" in html
        # Check for pass/fail indicators
        assert "✓" in html or "✗" in html

    def test_table_with_test_results(self):
        """Test table generation with test/holdout results."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test desc",
                    "train_results": [
                        {
                            "query": "Train query",
                            "should_trigger": True,
                            "pass": True,
                            "triggers": 1,
                            "runs": 1
                        }
                    ],
                    "test_results": [
                        {
                            "query": "Test query",
                            "should_trigger": True,
                            "pass": True,
                            "triggers": 1,
                            "runs": 1
                        }
                    ]
                }
            ]
        }
        html = generate_html(data)

        assert "Test query" in html
        # Test columns should have test-col class
        assert "test-col" in html
        # Test results should have test-result class
        assert "test-result" in html

    def test_table_column_polarity(self):
        """Test column polarity classes for should_trigger."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": [
                        {
                            "query": "Should trigger",
                            "should_trigger": True,
                            "pass": True,
                            "triggers": 1,
                            "runs": 1
                        },
                        {
                            "query": "Should not trigger",
                            "should_trigger": False,
                            "pass": True,
                            "triggers": 0,
                            "runs": 1
                        }
                    ]
                }
            ]
        }
        html = generate_html(data)

        # Positive columns should have positive-col class
        assert "positive-col" in html
        # Negative columns should have negative-col class
        assert "negative-col" in html


class TestColumnHandling:
    """Test column handling in HTML generation."""

    def test_query_column_width(self):
        """Test query column has proper width styling."""
        data = {"history": []}
        html = generate_html(data)

        assert "query-col" in html
        assert "min-width" in html

    def test_description_column_styling(self):
        """Test description column styling."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "A" * 100,
                    "train_results": []
                }
            ]
        }
        html = generate_html(data)

        assert "description" in html
        assert "monospace" in html or "font-family" in html
        assert "word-wrap" in html or "break-word" in html

    def test_result_column_alignment(self):
        """Test result column alignment."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": [
                        {
                            "query": "Query",
                            "should_trigger": True,
                            "pass": True,
                            "triggers": 1,
                            "runs": 1
                        }
                    ]
                }
            ]
        }
        html = generate_html(data)

        assert "text-align" in html
        assert "result" in html

    def test_score_column_formatting(self):
        """Test score column formatting."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_passed": 8,
                    "train_total": 10,
                    "train_results": []
                }
            ]
        }
        html = generate_html(data)

        assert "8/" in html
        assert "10" in html
        assert "score" in html

    def test_multiple_query_columns(self):
        """Test handling of multiple query columns."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": [
                        {"query": f"Query {i}", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1}
                        for i in range(5)
                    ]
                }
            ]
        }
        html = generate_html(data)

        # All queries should appear in headers
        for i in range(5):
            assert f"Query {i}" in html

    def test_train_test_column_distinction(self):
        """Test train and test columns are visually distinct."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": [
                        {"query": "Train", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1}
                    ],
                    "test_results": [
                        {"query": "Test", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1}
                    ]
                }
            ]
        }
        html = generate_html(data)

        # Test columns should have different background
        assert "test-col" in html


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_history(self):
        """Test HTML generation with empty history."""
        data = {"history": []}
        html = generate_html(data)

        assert "<tbody>" in html
        # Should have empty tbody
        assert "</tbody>" in html

    def test_missing_history_key(self):
        """Test handling of missing history key."""
        data = {}
        html = generate_html(data)

        assert "<table>" in html
        assert "<tbody>" in html

    def test_missing_train_results(self):
        """Test handling of missing train_results key."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "results": [
                        {"query": "Query", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1}
                    ]
                }
            ]
        }
        html = generate_html(data)

        # Should fall back to "results" key
        assert "Query" in html

    def test_missing_test_results(self):
        """Test handling of missing test_results key."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": [
                        {"query": "Train", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1}
                    ]
                }
            ]
        }
        html = generate_html(data)

        # Should not crash
        assert "<table>" in html

    def test_empty_results_array(self):
        """Test handling of empty results array."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": []
                }
            ]
        }
        html = generate_html(data)

        assert "<table>" in html

    def test_missing_query_in_result(self):
        """Test handling of missing query in result."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": [
                        {"should_trigger": True, "pass": True, "triggers": 1, "runs": 1}
                    ]
                }
            ]
        }
        # Should not crash
        html = generate_html(data)
        assert "<table>" in html

    def test_missing_should_trigger_in_result(self):
        """Test handling of missing should_trigger in result."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": [
                        {"query": "Query", "pass": True, "triggers": 1, "runs": 1}
                    ]
                }
            ]
        }
        # Should default to True and not crash
        html = generate_html(data)
        assert "Query" in html

    def test_missing_pass_in_result(self):
        """Test handling of missing pass in result."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": [
                        {"query": "Query", "should_trigger": True, "triggers": 1, "runs": 1}
                    ]
                }
            ]
        }
        # Should not crash
        html = generate_html(data)
        assert "Query" in html

    def test_missing_triggers_runs_in_result(self):
        """Test handling of missing triggers/runs in result."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": [
                        {"query": "Query", "should_trigger": True, "pass": True}
                    ]
                }
            ]
        }
        # Should not crash
        html = generate_html(data)
        assert "Query" in html

    def test_special_characters_in_description(self):
        """Test HTML escaping of special characters in description."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test <script>alert('xss')</script>",
                    "train_results": []
                }
            ]
        }
        html = generate_html(data)

        # Should be escaped
        assert "&lt;script&gt;" in html
        assert "<script>" not in html

    def test_special_characters_in_query(self):
        """Test HTML escaping of special characters in query."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_results": [
                        {"query": "Query & <test>", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1}
                    ]
                }
            ]
        }
        html = generate_html(data)

        # Should be escaped
        assert "&amp;" in html
        assert "&lt;" in html
        assert "&gt;" in html

    def test_unicode_content(self):
        """Test handling of unicode content."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "测试描述 🎉",
                    "train_results": [
                        {"query": "测试查询", "should_trigger": True, "pass": True, "triggers": 1, "runs": 1}
                    ]
                }
            ]
        }
        html = generate_html(data)

        assert "测试描述" in html
        assert "测试查询" in html

    def test_very_long_description(self):
        """Test handling of very long description."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "A" * 1000,
                    "train_results": []
                }
            ]
        }
        html = generate_html(data)

        assert "A" * 100 in html
        # Should not crash

    def test_auto_refresh_tag(self):
        """Test auto refresh meta tag."""
        data = {}
        html = generate_html(data, auto_refresh=True)

        assert '<meta http-equiv="refresh" content="5">' in html

    def test_no_auto_refresh_tag(self):
        """Test no auto refresh when disabled."""
        data = {}
        html = generate_html(data, auto_refresh=False)

        assert '<meta http-equiv="refresh"' not in html


class TestSummarySection:
    """Test summary section generation."""

    def test_summary_with_original_description(self):
        """Test summary displays original description."""
        data = {
            "original_description": "Original test description",
            "history": []
        }
        html = generate_html(data)

        assert "Original:" in html
        assert "Original test description" in html

    def test_summary_with_best_description(self):
        """Test summary displays best description."""
        data = {
            "best_description": "Best test description",
            "history": []
        }
        html = generate_html(data)

        assert "Best:" in html
        assert "Best test description" in html

    def test_summary_with_scores(self):
        """Test summary displays scores."""
        data = {
            "best_score": 0.85,
            "best_test_score": 0.80,
            "history": []
        }
        html = generate_html(data)

        assert "Best Score:" in html
        assert "0.85" in html
        assert "(test)" in html

    def test_summary_with_iteration_count(self):
        """Test summary displays iteration count."""
        data = {
            "iterations_run": 10,
            "train_size": 5,
            "test_size": 3,
            "history": []
        }
        html = generate_html(data)

        assert "Iterations:" in html
        assert "10" in html
        assert "Train:" in html
        assert "5" in html
        assert "Test:" in html
        assert "3" in html


class TestLegendSection:
    """Test legend section generation."""

    def test_legend_present(self):
        """Test legend is present in HTML."""
        data = {"history": []}
        html = generate_html(data)

        assert "legend" in html.lower()
        assert "Query columns:" in html

    def test_legend_items(self):
        """Test legend items are present."""
        data = {"history": []}
        html = generate_html(data)

        assert "Should trigger" in html
        assert "Should NOT trigger" in html
        assert "Train" in html
        assert "Test" in html

    def test_legend_swatch_colors(self):
        """Test legend swatch colors."""
        data = {"history": []}
        html = generate_html(data)

        assert "swatch-positive" in html
        assert "swatch-negative" in html
        assert "swatch-train" in html
        assert "swatch-test" in html


class TestScoreClasses:
    """Test score class calculations."""

    def test_score_class_good(self):
        """Test score class for good scores (>=80%)."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_passed": 8,
                    "train_total": 10,
                    "train_results": []
                }
            ]
        }
        html = generate_html(data)

        assert "score-good" in html

    def test_score_class_ok(self):
        """Test score class for ok scores (50-79%)."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_passed": 6,
                    "train_total": 10,
                    "train_results": []
                }
            ]
        }
        html = generate_html(data)

        assert "score-ok" in html

    def test_score_class_bad(self):
        """Test score class for bad scores (<50%)."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_passed": 3,
                    "train_total": 10,
                    "train_results": []
                }
            ]
        }
        html = generate_html(data)

        assert "score-bad" in html

    def test_score_class_zero_total(self):
        """Test score class when total is zero."""
        data = {
            "history": [
                {
                    "iteration": 1,
                    "description": "Test",
                    "train_passed": 0,
                    "train_total": 0,
                    "train_results": []
                }
            ]
        }
        html = generate_html(data)

        assert "score-bad" in html


class TestMainFunction:
    """Test main function."""

    def test_main_with_file_input(self, tmp_path):
        """Test main function with file input."""
        input_file = tmp_path / "input.json"
        input_file.write_text(json.dumps({"history": []}))

        output_file = tmp_path / "output.html"

        # Mock sys.argv
        import sys
        original_argv = sys.argv
        sys.argv = ["generate_report.py", str(input_file), "-o", str(output_file)]

        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.argv = original_argv

        assert output_file.exists()
        assert "<!DOCTYPE html>" in output_file.read_text()

    def test_main_with_stdin_input(self, tmp_path):
        """Test main function with stdin input."""
        output_file = tmp_path / "output.html"

        # Mock sys.argv and sys.stdin
        import sys
        original_argv = sys.argv
        original_stdin = sys.stdin

        sys.argv = ["generate_report.py", "-", "-o", str(output_file)]
        sys.stdin = MagicMock()
        sys.stdin.read.return_value = json.dumps({"history": []})

        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.argv = original_argv
            sys.stdin = original_stdin

        assert output_file.exists()

    def test_main_with_skill_name(self, tmp_path):
        """Test main function with skill name."""
        input_file = tmp_path / "input.json"
        input_file.write_text(json.dumps({"history": []}))

        output_file = tmp_path / "output.html"

        import sys
        original_argv = sys.argv
        sys.argv = ["generate_report.py", str(input_file), "-o", str(output_file), "--skill-name", "test-skill"]

        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.argv = original_argv

        content = output_file.read_text()
        assert "test-skill" in content

    def test_main_stdout_output(self, tmp_path, capsys):
        """Test main function with stdout output."""
        input_file = tmp_path / "input.json"
        input_file.write_text(json.dumps({"history": []}))

        import sys
        original_argv = sys.argv
        sys.argv = ["generate_report.py", str(input_file)]

        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "<!DOCTYPE html>" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
