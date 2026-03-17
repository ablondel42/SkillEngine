#!/usr/bin/env python3
"""
Design system consistency checker.

This script analyzes CSS/SCSS files to check for design system compliance.
It verifies that color values, spacing values, and other tokens match
the defined design system tokens.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def load_tokens(tokens_file: Path) -> dict:
    """Load design system tokens from JSON file."""
    with open(tokens_file) as f:
        return json.load(f)


def extract_css_variables(css_content: str) -> dict:
    """Extract CSS custom properties from content."""
    pattern = r'--([a-zA-Z0-9_-]+):\s*([^;]+);'
    matches = re.findall(pattern, css_content)
    return {f"--{k}": v.strip() for k, v in matches}


def check_colors(tokens: dict, css_content: str, token_name: str = "colors") -> list:
    """Check if CSS uses only defined color tokens."""
    issues = []

    # Get defined color tokens
    color_tokens = tokens.get(token_name, {})

    # Find all hex colors in CSS
    hex_pattern = r'#[0-9A-Fa-f]{3,8}'
    found_colors = set(re.findall(hex_pattern, css_content))

    # Find CSS variable references
    var_pattern = r'var\((--[a-zA-Z0-9_-]+)\)'
    found_vars = set(re.findall(var_pattern, css_content))

    # Check for colors not in tokens
    for color in found_colors:
        found = False
        for name, value in color_tokens.items():
            if isinstance(value, str) and value.upper() == color.upper():
                found = True
                break
        if not found:
            issues.append(f"Found undefined color: {color}")

    return issues


def check_spacing(tokens: dict, css_content: str) -> list:
    """Check if CSS uses only defined spacing tokens."""
    issues = []

    spacing_tokens = tokens.get("spacing", {})
    defined_values = set(spacing_tokens.values())

    # Find all pixel values
    px_pattern = r'\b(\d+)px\b'
    found_px = re.findall(px_pattern, css_content)

    for px in found_px:
        if px not in spacing_tokens.values():
            # Check if it's a multiple of the base (e.g., 4px)
            px_int = int(px)
            base = 4  # Common base for spacing systems
            if px_int % base != 0:
                issues.append(f"Non-standard spacing: {px}px")

    return issues


def check_shadows(tokens: dict, css_content: str) -> list:
    """Check if CSS uses only defined shadow tokens."""
    issues = []

    shadow_tokens = tokens.get("shadows", {})

    # Find box-shadow values
    shadow_pattern = r'box-shadow:\s*([^;]+);'
    found_shadows = re.findall(shadow_pattern, css_content)

    for shadow in found_shadows:
        # Check if it matches a defined token
        found = False
        for name, value in shadow_tokens.items():
            if value in shadow:
                found = True
                break
        if not found:
            issues.append(f"Non-standard shadow: {shadow[:50]}...")

    return issues


def check_border_radius(tokens: dict, css_content: str) -> list:
    """Check if CSS uses only defined border radius tokens."""
    issues = []

    radius_tokens = tokens.get("borders", {}).get("radius", {})

    # Find border-radius values
    radius_pattern = r'border-radius:\s*([^;]+);'
    found_radii = re.findall(radius_pattern, css_content)

    for radius in found_radii:
        # Check if it matches a defined token
        found = False
        for name, value in radius_tokens.items():
            if value in radius:
                found = True
                break
        if not found:
            issues.append(f"Non-standard radius: {radius}")

    return issues


def analyze_file(file_path: Path, tokens: dict) -> dict:
    """Analyze a CSS/SCSS file for design system compliance."""
    with open(file_path) as f:
        content = f.read()

    issues = []
    issues.extend(check_colors(tokens, content))
    issues.extend(check_spacing(tokens, content))
    issues.extend(check_shadows(tokens, content))
    issues.extend(check_border_radius(tokens, content))

    return {
        "file": str(file_path),
        "issues": issues,
        "issue_count": len(issues)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Check CSS/SCSS files for design system compliance"
    )
    parser.add_argument(
        "tokens_file",
        type=Path,
        help="Path to design system tokens JSON file"
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="CSS/SCSS files to analyze"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    if not args.tokens_file.exists():
        print(f"Error: Tokens file not found: {args.tokens_file}", file=sys.stderr)
        sys.exit(1)

    tokens = load_tokens(args.tokens_file)

    results = []
    total_issues = 0

    for file_path in args.files:
        if not Path(file_path).exists():
            print(f"Warning: File not found: {file_path}", file=sys.stderr)
            continue

        result = analyze_file(Path(file_path), tokens)
        results.append(result)
        total_issues += result["issue_count"]

    if args.json:
        output = {
            "summary": {
                "files_analyzed": len(results),
                "total_issues": total_issues
            },
            "results": results
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Design System Consistency Check")
        print(f"================================")
        print(f"Files analyzed: {len(results)}")
        print(f"Total issues: {total_issues}")
        print()

        for result in results:
            if result["issue_count"] > 0:
                print(f"File: {result['file']}")
                for issue in result["issues"]:
                    print(f"  - {issue}")
                print()

    sys.exit(0 if total_issues == 0 else 1)


if __name__ == "__main__":
    main()
