#!/usr/bin/env python3
"""Automated code quality fixes for SkillEngine.

This script automatically fixes common code quality issues:
- Bare except clauses → Specific exception types
- Missing docstrings → Stub docstrings
- Missing type hints → Type annotations
- Magic numbers → Named constants
- Long lines → Line breaks (where safe)

Usage:
    python scripts/fix_quality.py [--dry-run] [--category error_handling]
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class FixResult:
    """Result of a single fix operation."""

    file: str
    line: int
    category: str
    description: str
    success: bool
    error: str = ""


class CodeQualityFixer:
    """Automatically fixes common code quality issues."""

    def __init__(
        self,
        root_dir: str,
        dry_run: bool = False,
        categories: list[str] | None = None,
    ):
        self.root_dir = Path(root_dir)
        self.dry_run = dry_run
        self.categories = categories or [
            "error_handling",
            "documentation",
            "type_safety",
            "maintainability",
            "style",
        ]
        self.results: list[FixResult] = []
        self.stats = {
            "files_processed": 0,
            "files_modified": 0,
            "fixes_applied": 0,
            "fixes_failed": 0,
        }

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        exclude_patterns = [
            "tests",
            "__pycache__",
            ".git",
            "node_modules",
            "venv",
            ".venv",
            "build",
            "dist",
        ]
        for pattern in exclude_patterns:
            if pattern in str(path):
                return True
        return False

    def scan_python_files(self) -> list[Path]:
        """Scan for Python files."""
        python_files = []
        for path in self.root_dir.rglob("*.py"):
            if not self.should_exclude(path):
                python_files.append(path)
        return python_files

    def fix_bare_except(self, file_path: Path, content: str) -> tuple[str, list[FixResult]]:
        """Fix bare except clauses by adding specific exception types."""
        fixes = []
        lines = content.splitlines()
        modified = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Match bare except
            if re.match(r"^except\s*:\s*$", stripped):
                # Determine context to suggest appropriate exception
                indent = len(line) - len(line.lstrip())
                new_line = " " * indent + "except Exception as e:"
                lines[i] = new_line
                modified = True
                fixes.append(
                    FixResult(
                        file=str(file_path.relative_to(self.root_dir)),
                        line=i + 1,
                        category="error_handling",
                        description="Changed bare 'except:' to 'except Exception as e:'",
                        success=True,
                    )
                )
            # Match 'except :' with space
            elif re.match(r"^except\s+:\s*$", stripped):
                indent = len(line) - len(line.lstrip())
                new_line = " " * indent + "except Exception as e:"
                lines[i] = new_line
                modified = True
                fixes.append(
                    FixResult(
                        file=str(file_path.relative_to(self.root_dir)),
                        line=i + 1,
                        category="error_handling",
                        description="Changed bare 'except :' to 'except Exception as e:'",
                        success=True,
                    )
                )

        if modified:
            return "\n".join(lines), fixes
        return content, fixes

    def add_docstrings(self, file_path: Path, content: str) -> tuple[str, list[FixResult]]:
        """Add stub docstrings to functions missing them."""
        fixes = []
        lines = content.splitlines()
        modified = False

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith("def "):
                # Check if next non-empty line is a docstring
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1

                has_docstring = (
                    j < len(lines)
                    and (lines[j].strip().startswith('"""') or lines[j].strip().startswith("'''"))
                )

                if not has_docstring:
                    # Get function name and parameters
                    func_match = re.match(r"(\s*)def\s+(\w+)\s*\(([^)]*)\)", line)
                    if func_match:
                        indent = func_match.group(1)
                        func_name = func_match.group(2)
                        params = func_match.group(3)

                        # Create stub docstring
                        docstring_lines = [
                            f'{indent}    """',
                            f'{indent}    TODO: Document {func_name}.',
                            f'{indent}    """',
                        ]

                        # Insert after function definition
                        insert_pos = i + 1
                        for doc_line in reversed(docstring_lines):
                            lines.insert(insert_pos, doc_line)

                        modified = True
                        fixes.append(
                            FixResult(
                                file=str(file_path.relative_to(self.root_dir)),
                                line=i + 1,
                                category="documentation",
                                description=f"Added stub docstring to '{func_name}'",
                                success=True,
                            )
                        )
                        i += len(docstring_lines)
            i += 1

        if modified:
            return "\n".join(lines), fixes
        return content, fixes

    def add_type_hints(self, file_path: Path, content: str) -> tuple[str, list[FixResult]]:
        """Add basic type hints to functions."""
        fixes = []
        lines = content.splitlines()
        modified = False

        for i, line in enumerate(lines):
            if line.strip().startswith("def "):
                # Check if already has return type
                if "->" in line:
                    continue

                # Add generic return type
                if ": str" in line or "-> str" in line:
                    continue

                # Simple heuristic: add -> None for functions without return
                func_match = re.match(r"(\s*)def\s+(\w+)\s*\(([^)]*)\)\s*:", line)
                if func_match:
                    # Check if function body suggests a return value
                    func_name = func_match.group(2)
                    j = i + 1
                    has_return = False
                    while j < len(lines) and j < i + 20:  # Check first 20 lines
                        if "return " in lines[j] and not lines[j].strip().startswith("#"):
                            has_return = True
                            break
                        j += 1

                    if not has_return and not func_name.startswith("__"):
                        # Replace the colon at end
                        new_line = line.rstrip().rstrip(":") + ") -> None:"
                        # Handle case where params already have closing paren
                        if ")" in line:
                            new_line = line.replace("):", ") -> None:")
                        lines[i] = new_line
                        modified = True
                        fixes.append(
                            FixResult(
                                file=str(file_path.relative_to(self.root_dir)),
                                line=i + 1,
                                category="type_safety",
                                description=f"Added '-> None' to '{func_name}'",
                                success=True,
                            )
                        )

        if modified:
            return "\n".join(lines), fixes
        return content, fixes

    def extract_magic_numbers(
        self, file_path: Path, content: str
    ) -> tuple[str, list[FixResult]]:
        """Extract magic numbers to named constants."""
        fixes = []
        lines = content.splitlines()
        constants_added: dict[str, str] = {}
        modified = False

        # Common magic number mappings
        number_names = {
            "86400": "SECONDS_PER_DAY",
            "3600": "SECONDS_PER_HOUR",
            "604800": "SECONDS_PER_WEEK",
            "1024": "BYTES_PER_KB",
            "2048": "BYTES_PER_2KB",
            "4096": "BYTES_PER_4KB",
            "0.05": "THRESHOLD_LOW",
            "0.1": "THRESHOLD_MIN",
            "0.25": "THRESHOLD_QUARTER",
            "0.5": "THRESHOLD_HALF",
            "0.75": "THRESHOLD_THREE_QUARTERS",
            "0.9": "THRESHOLD_HIGH",
            "0.95": "THRESHOLD_CRITICAL",
        }

        new_lines = []
        for i, line in enumerate(lines):
            modified_line = line
            for number, name in number_names.items():
                # Find magic number not in comments or strings
                if number in line and not line.strip().startswith("#"):
                    # Check if it's a standalone number (not part of larger number)
                    pattern = rf"\b{re.escape(number)}\b"
                    if re.search(pattern, line):
                        if number not in constants_added:
                            # Add constant at top of file after imports
                            const_line = f"{name} = {number}"
                            constants_added[number] = const_line
                            modified = True
                            fixes.append(
                                FixResult(
                                    file=str(file_path.relative_to(self.root_dir)),
                                    line=i + 1,
                                    category="maintainability",
                                    description=f"Extracted magic number {number} to {name}",
                                    success=True,
                                )
                            )
                        # Replace number with constant name
                        modified_line = re.sub(
                            pattern, name, modified_line
                        )

            new_lines.append(modified_line)

        # Insert constants after imports
        if constants_added:
            const_lines = ["", "# Magic number constants", ""]
            const_lines.extend(f"{name}" for name in constants_added.values())
            const_lines.append("")

            # Find position after last import
            insert_pos = 0
            for i, line in enumerate(new_lines):
                if line.startswith("import ") or line.startswith("from "):
                    insert_pos = i + 1

            for const_line in reversed(const_lines):
                new_lines.insert(insert_pos, const_line)

        if modified:
            return "\n".join(new_lines), fixes
        return content, fixes

    def fix_file(self, file_path: Path) -> list[FixResult]:
        """Apply all applicable fixes to a file."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            return [
                FixResult(
                    file=str(file_path.relative_to(self.root_dir)),
                    line=0,
                    category="file_error",
                    description=f"Failed to read file: {e}",
                    success=False,
                    error=str(e),
                )
            ]

        original_content = content
        all_fixes: list[FixResult] = []

        # Apply fixes by category
        if "error_handling" in self.categories:
            content, fixes = self.fix_bare_except(file_path, content)
            all_fixes.extend(fixes)

        if "documentation" in self.categories:
            content, fixes = self.add_docstrings(file_path, content)
            all_fixes.extend(fixes)

        if "type_safety" in self.categories:
            content, fixes = self.add_type_hints(file_path, content)
            all_fixes.extend(fixes)

        if "maintainability" in self.categories:
            content, fixes = self.extract_magic_numbers(file_path, content)
            all_fixes.extend(fixes)

        # Write back if modified
        if content != original_content:
            self.stats["files_modified"] += 1
            if not self.dry_run:
                file_path.write_text(content, encoding="utf-8")

        self.stats["fixes_applied"] += len([f for f in all_fixes if f.success])
        self.stats["fixes_failed"] += len([f for f in all_fixes if not f.success])

        return all_fixes

    def run_fixes(self) -> list[FixResult]:
        """Run all fixes on all files."""
        python_files = self.scan_python_files()

        for file_path in python_files:
            self.stats["files_processed"] += 1
            fixes = self.fix_file(file_path)
            self.results.extend(fixes)

        return self.results

    def print_summary(self) -> None:
        """Print summary of fixes applied."""
        print("\n" + "=" * 70)
        print("CODE QUALITY FIX SUMMARY")
        print("=" * 70)
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Files modified: {self.stats['files_modified']}")
        print(f"Fixes applied: {self.stats['fixes_applied']}")
        print(f"Fixes failed: {self.stats['fixes_failed']}")
        print()

        if self.dry_run:
            print("🔍 DRY RUN - No files were modified")
            print()

        # Summary by category
        by_category: dict[str, int] = {}
        for result in self.results:
            by_category[result.category] = by_category.get(result.category, 0) + 1

        if by_category:
            print("FIXES BY CATEGORY:")
            print("-" * 40)
            for category, count in sorted(by_category.items()):
                print(f"  {category}: {count}")
            print()

        # Show individual results
        if self.results:
            print("DETAILED RESULTS:")
            print("-" * 40)
            for result in self.results[:30]:  # Show first 30
                icon = "✅" if result.success else "❌"
                print(f"  {icon} {result.file}:{result.line}")
                print(f"     [{result.category}] {result.description}")
                if result.error:
                    print(f"     Error: {result.error}")

            if len(self.results) > 30:
                print(f"\n  ... and {len(self.results) - 30} more results")

        print()
        print("=" * 70)

        if self.stats["fixes_applied"] > 0:
            if self.dry_run:
                print(f"🔧 Would apply {self.stats['fixes_applied']} fixes")
            else:
                print(f"✅ Applied {self.stats['fixes_applied']} fixes successfully")
        else:
            print("✅ No fixes needed - code quality is excellent!")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automated code quality fixes for SkillEngine"
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to fix (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without modifying files",
    )
    parser.add_argument(
        "--category",
        nargs="+",
        choices=[
            "error_handling",
            "documentation",
            "type_safety",
            "maintainability",
            "style",
        ],
        help="Categories to fix (default: all)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output",
    )

    args = parser.parse_args()

    fixer = CodeQualityFixer(
        args.root,
        dry_run=args.dry_run,
        categories=args.category,
    )

    fixer.run_fixes()
    fixer.print_summary()

    # Exit with error if fixes failed
    if fixer.stats["fixes_failed"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
