#!/usr/bin/env python3
"""Automated code quality audit for SkillEngine.

This script performs comprehensive code quality analysis and generates
a detailed report with actionable findings.

Usage:
    python scripts/audit_quality.py [--output report.json] [--threshold 80]
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    """Represents a code quality finding."""

    category: str
    severity: str  # critical, high, medium, low
    file: str
    line: int
    message: str
    suggestion: str
    code_snippet: str = ""


@dataclass
class AuditResult:
    """Represents the complete audit result."""

    timestamp: str = ""
    total_files: int = 0
    total_lines: int = 0
    score: int = 0
    findings: list[Finding] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "total_files": self.total_files,
            "total_lines": self.total_lines,
            "score": self.score,
            "findings": [
                {
                    "category": f.category,
                    "severity": f.severity,
                    "file": f.file,
                    "line": f.line,
                    "message": f.message,
                    "suggestion": f.suggestion,
                    "code_snippet": f.code_snippet,
                }
                for f in self.findings
            ],
            "summary": self.summary,
        }


class CodeQualityAuditor:
    """Performs comprehensive code quality audits."""

    def __init__(self, root_dir: str, exclude_patterns: list[str] | None = None):
        self.root_dir = Path(root_dir)
        self.exclude_patterns = exclude_patterns or [
            "tests",
            "__pycache__",
            ".git",
            "node_modules",
            "venv",
            ".venv",
            "build",
            "dist",
        ]
        self.findings: list[Finding] = []
        self.stats = {
            "files_scanned": 0,
            "lines_scanned": 0,
            "functions_total": 0,
            "functions_with_docs": 0,
            "functions_with_types": 0,
        }

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from audit."""
        for pattern in self.exclude_patterns:
            if pattern in str(path):
                return True
        return False

    def scan_python_files(self) -> list[Path]:
        """Scan for all Python files in the project."""
        python_files = []
        for path in self.root_dir.rglob("*.py"):
            if not self.should_exclude(path):
                python_files.append(path)
        return python_files

    def check_bare_except(self, file_path: Path, content: str, lines: list[str]) -> None:
        """Check for bare except clauses."""
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Match bare except or except with colon only
            if re.match(r"^except\s*:", stripped):
                self.findings.append(
                    Finding(
                        category="error_handling",
                        severity="critical",
                        file=str(file_path.relative_to(self.root_dir)),
                        line=i,
                        message="Bare except clause catches all exceptions",
                        suggestion="Use specific exception types like "
                        "'except (ValueError, OSError):'",
                        code_snippet=stripped,
                    )
                )

    def check_long_functions(
        self, file_path: Path, content: str, lines: list[str], max_lines: int = 50
    ) -> None:
        """Check for functions exceeding maximum line count."""
        in_func = False
        func_start = 0
        func_name = ""
        func_lines = 0

        for i, line in enumerate(lines, 1):
            if line.strip().startswith("def "):
                # Report previous function if too long
                if in_func and func_lines > max_lines:
                    # Skip main entry points
                    if func_name not in ("main", "run_loop"):
                        self.findings.append(
                            Finding(
                                category="complexity",
                                severity="high",
                                file=str(file_path.relative_to(self.root_dir)),
                                line=func_start,
                                message=f"Function '{func_name}' is {func_lines} lines "
                                f"(max: {max_lines})",
                                suggestion="Extract helper functions to reduce complexity",
                                code_snippet=f"def {func_name}(...)",
                            )
                        )
                in_func = True
                func_start = i
                func_name = line.split("def ")[1].split("(")[0]
                func_lines = 0
            elif in_func:
                func_lines += 1

        # Check last function
        if in_func and func_lines > max_lines and func_name not in ("main", "run_loop"):
            self.findings.append(
                Finding(
                    category="complexity",
                    severity="high",
                    file=str(file_path.relative_to(self.root_dir)),
                    line=func_start,
                    message=f"Function '{func_name}' is {func_lines} lines "
                    f"(max: {max_lines})",
                    suggestion="Extract helper functions to reduce complexity",
                    code_snippet=f"def {func_name}(...)",
                )
            )

    def check_missing_docstrings(
        self, file_path: Path, content: str, lines: list[str]
    ) -> None:
        """Check for functions missing docstrings."""
        in_func = False
        func_name = ""
        func_line = 0

        for i, line in enumerate(lines, 1):
            if line.strip().startswith("def "):
                in_func = True
                func_name = line.split("def ")[1].split("(")[0]
                func_line = i
            elif in_func and '"""' in line:
                self.stats["functions_with_docs"] += 1
                in_func = False
            elif in_func and line.strip() and not line.strip().startswith(
                ("#", '"""', "'''", "Args:", "Returns:", "Raises:")
            ):
                # Function has no docstring
                if not func_name.startswith("_"):
                    self.findings.append(
                        Finding(
                            category="documentation",
                            severity="medium",
                            file=str(file_path.relative_to(self.root_dir)),
                            line=func_line,
                            message=f"Function '{func_name}' missing docstring",
                            suggestion="Add a docstring describing the function's purpose",
                            code_snippet=f"def {func_name}(...)",
                        )
                    )
                in_func = False

    def check_missing_type_hints(
        self, file_path: Path, content: str, lines: list[str]
    ) -> None:
        """Check for functions missing type hints."""
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("def "):
                func_name = line.split("def ")[1].split("(")[0]
                has_return_hint = "->" in line

                # Check for parameter type hints
                param_match = re.search(r"\(([^)]*)\)", line)
                has_param_hints = False
                if param_match:
                    params = param_match.group(1)
                    if params.strip() and ":" in params:
                        has_param_hints = True

                if not has_return_hint and not func_name.startswith("_"):
                    self.findings.append(
                        Finding(
                            category="type_safety",
                            severity="low",
                            file=str(file_path.relative_to(self.root_dir)),
                            line=i,
                            message=f"Function '{func_name}' missing return type hint",
                            suggestion="Add return type annotation (e.g., '-> str')",
                            code_snippet=line.strip()[:60],
                        )
                    )

    def check_magic_numbers(
        self, file_path: Path, content: str, lines: list[str]
    ) -> None:
        """Check for magic numbers that should be constants."""
        # Common magic numbers to flag
        magic_patterns = [
            r"\b(86400|3600|604800)\b",  # Time constants
            r"\b(1024|2048|4096|8192)\b",  # Size constants
            r"\b(0\.05|0\.1|0\.25|0\.5|0\.75|0\.9|0\.95)\b",  # Thresholds
        ]

        for i, line in enumerate(lines, 1):
            # Skip comments and string definitions
            if line.strip().startswith("#"):
                continue
            if "=" in line and ('"' in line or "'" in line):
                continue

            for pattern in magic_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    self.findings.append(
                        Finding(
                            category="maintainability",
                            severity="low",
                            file=str(file_path.relative_to(self.root_dir)),
                            line=i,
                            message=f"Magic number '{match}' should be a named constant",
                            suggestion=f"Define as constant: TIME_{match.upper()} = {match}",
                            code_snippet=line.strip()[:60],
                        )
                    )

    def check_duplicate_code(
        self, file_path: Path, content: str, all_functions: dict[str, list[tuple[str, int]]]
    ) -> None:
        """Check for duplicate function definitions across files."""
        # Extract function definitions
        func_pattern = r"def\s+(\w+)\s*\([^)]*\)\s*(?:->[^:]+)?:\s*(?:\"\"\"|''')"
        matches = re.finditer(func_pattern, content, re.MULTILINE)

        rel_path = str(file_path.relative_to(self.root_dir))
        for match in matches:
            func_name = match.group(1)
            line_num = content[: match.start()].count("\n") + 1

            if func_name not in all_functions:
                all_functions[func_name] = []
            all_functions[func_name].append((rel_path, line_num))

    def check_line_length(
        self, file_path: Path, lines: list[str], max_length: int = 100
    ) -> None:
        """Check for lines exceeding maximum length."""
        for i, line in enumerate(lines, 1):
            # Skip URLs and long strings
            if "http://" in line or "https://" in line:
                continue
            if line.strip().startswith('#'):
                continue

            if len(line.rstrip()) > max_length:
                self.findings.append(
                    Finding(
                        category="style",
                        severity="low",
                        file=str(file_path.relative_to(self.root_dir)),
                        line=i,
                        message=f"Line exceeds {max_length} characters "
                        f"({len(line.rstrip())} chars)",
                        suggestion="Break long lines or use string concatenation",
                        code_snippet=line.strip()[:50] + "...",
                    )
                )

    def audit_file(self, file_path: Path, all_functions: dict) -> None:
        """Perform all audits on a single file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.splitlines()
        except (UnicodeDecodeError, OSError) as e:
            self.findings.append(
                Finding(
                    category="file_error",
                    severity="medium",
                    file=str(file_path.relative_to(self.root_dir)),
                    line=0,
                    message=f"Failed to read file: {e}",
                    suggestion="Check file encoding or permissions",
                    code_snippet="",
                )
            )
            return

        self.stats["files_scanned"] += 1
        self.stats["lines_scanned"] += len(lines)

        # Count functions
        func_count = len(re.findall(r"^def\s+\w+", content, re.MULTILINE))
        self.stats["functions_total"] += func_count

        # Run all checks
        self.check_bare_except(file_path, content, lines)
        self.check_long_functions(file_path, content, lines)
        self.check_missing_docstrings(file_path, content, lines)
        self.check_missing_type_hints(file_path, content, lines)
        self.check_magic_numbers(file_path, content, lines)
        self.check_duplicate_code(file_path, content, all_functions)
        self.check_line_length(file_path, lines)

    def calculate_score(self) -> int:
        """Calculate overall quality score (0-100)."""
        # Start with perfect score
        score = 100

        # Deduct points based on findings
        severity_weights = {
            "critical": 10,
            "high": 5,
            "medium": 2,
            "low": 1,
        }

        for finding in self.findings:
            score -= severity_weights.get(finding.severity, 0)

        # Bonus for good practices
        if self.stats["functions_total"] > 0:
            doc_ratio = self.stats["functions_with_docs"] / self.stats["functions_total"]
            if doc_ratio > 0.9:
                score += 5
            elif doc_ratio > 0.7:
                score += 2

        return max(0, min(100, score))

    def generate_summary(self) -> dict[str, Any]:
        """Generate summary statistics."""
        by_category: dict[str, int] = {}
        by_severity: dict[str, int] = {}

        for finding in self.findings:
            by_category[finding.category] = by_category.get(finding.category, 0) + 1
            by_severity[finding.severity] = by_severity.get(finding.severity, 0) + 1

        return {
            "by_category": by_category,
            "by_severity": by_severity,
            "functions_with_docs": self.stats["functions_with_docs"],
            "functions_total": self.stats["functions_total"],
            "doc_coverage": round(
                (self.stats["functions_with_docs"] / max(1, self.stats["functions_total"])) * 100, 1
            ),
        }

    def run_audit(self) -> AuditResult:
        """Run the complete audit."""
        python_files = self.scan_python_files()
        all_functions: dict[str, list[tuple[str, int]]] = {}

        for file_path in python_files:
            self.audit_file(file_path, all_functions)

        # Check for duplicate functions
        for func_name, locations in all_functions.items():
            if len(locations) > 1:
                files = [loc[0] for loc in locations]
                # Only report if in different files
                if len(set(files)) > 1:
                    self.findings.append(
                        Finding(
                            category="duplication",
                            severity="medium",
                            file=files[0],
                            line=locations[0][1],
                            message=f"Function '{func_name}' defined in multiple files: {', '.join(files)}",
                            suggestion="Extract to shared module",
                            code_snippet=f"def {func_name}(...)",
                        )
                    )

        result = AuditResult(
            timestamp=datetime.now().isoformat(),
            total_files=self.stats["files_scanned"],
            total_lines=self.stats["lines_scanned"],
            score=self.calculate_score(),
            findings=self.findings,
            summary=self.generate_summary(),
        )

        return result


def print_report(result: AuditResult, verbose: bool = False) -> int:
    """Print audit report to console. Returns exit code."""
    print("\n" + "=" * 70)
    print("CODE QUALITY AUDIT REPORT")
    print("=" * 70)
    print(f"Timestamp: {result.timestamp}")
    print(f"Files scanned: {result.total_files}")
    print(f"Lines scanned: {result.total_lines}")
    print(f"Overall Score: {result.score}/100")
    print()

    # Summary by severity
    print("FINDINGS BY SEVERITY:")
    print("-" * 40)
    severity_order = ["critical", "high", "medium", "low"]
    for severity in severity_order:
        count = result.summary["by_severity"].get(severity, 0)
        if count > 0:
            icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(severity, "⚪")
            print(f"  {icon} {severity.upper()}: {count}")
    print()

    # Summary by category
    print("FINDINGS BY CATEGORY:")
    print("-" * 40)
    for category, count in sorted(result.summary["by_category"].items()):
        print(f"  {category}: {count}")
    print()

    # Docstring coverage
    print("DOCUMENTATION:")
    print("-" * 40)
    print(f"  Functions with docstrings: {result.summary['functions_with_docs']}/"
          f"{result.summary['functions_total']} "
          f"({result.summary['doc_coverage']}%)")
    print()

    # Detailed findings
    if verbose and result.findings:
        print("DETAILED FINDINGS:")
        print("-" * 40)
        for i, finding in enumerate(result.findings[:20], 1):  # Show first 20
            icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(
                finding.severity, "⚪"
            )
            print(f"\n{i}. {icon} [{finding.severity.upper()}] {finding.category}")
            print(f"   File: {finding.file}:{finding.line}")
            print(f"   Issue: {finding.message}")
            print(f"   Fix: {finding.suggestion}")
            if finding.code_snippet:
                print(f"   Code: {finding.code_snippet}")

        if len(result.findings) > 20:
            print(f"\n... and {len(result.findings) - 20} more findings")

    print()
    print("=" * 70)

    # Return exit code based on score (don't exit here - let main() handle it)
    if result.score >= 90:
        print("✅ EXCELLENT - Code quality is outstanding!")
        return 0
    elif result.score >= 70:
        print("✅ GOOD - Code quality is acceptable with minor issues")
        return 0
    elif result.score >= 50:
        print("⚠️  NEEDS IMPROVEMENT - Address high priority findings")
        return 1
    else:
        print("❌ POOR - Significant code quality issues detected")
        return 2


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automated code quality audit for SkillEngine"
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to audit (default: current directory)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON report file",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=70,
        help="Minimum acceptable score (default: 70)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed findings",
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        default=[],
        help="Additional patterns to exclude",
    )

    args = parser.parse_args()

    # Run audit
    exclude_patterns = [
        "tests",
        "__pycache__",
        ".git",
        "node_modules",
        "venv",
        ".venv",
        "build",
        "dist",
    ] + args.exclude

    auditor = CodeQualityAuditor(args.root, exclude_patterns)
    result = auditor.run_audit()

    # Save JSON report if requested (before printing to ensure it's always saved)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\n📄 Report saved to: {args.output}")

    # Print report and get exit code
    exit_code = print_report(result, args.verbose)

    # Check threshold
    if result.score < args.threshold:
        print(f"\n❌ Score {result.score} below threshold {args.threshold}")
        exit_code = 2

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
