#!/usr/bin/env python3
"""
Generate CSS custom properties from design system tokens.

This script converts a tokens.json file into a CSS file with
CSS custom properties for use in stylesheets.
"""

import argparse
import sys
from pathlib import Path

from tokens import load_tokens


def generate_css_variables(tokens: dict) -> str:
    """Generate CSS custom properties from tokens."""
    lines = [
        "/* Design System CSS Variables */",
        "/* Auto-generated from tokens.json */",
        "",
        ":root {"
    ]

    # Colors
    lines.append("  /* Colors */")
    colors = tokens.get("colors", {})
    for name, value in colors.items():
        if isinstance(value, str):
            lines.append(f"  --color-{name}: {value};")
        elif isinstance(value, dict):
            for sub_name, sub_value in value.items():
                lines.append(f"  --color-{name}-{sub_name}: {sub_value};")

    # Typography
    lines.append("")
    lines.append("  /* Typography */")
    typography = tokens.get("typography", {})
    fonts = typography.get("fonts", {})
    for name, value in fonts.items():
        lines.append(f"  --font-{name}: {value};")

    sizes = typography.get("sizes", {})
    for name, value in sizes.items():
        lines.append(f"  --text-{name}: {value};")

    weights = typography.get("weights", {})
    for name, value in weights.items():
        lines.append(f"  --font-weight-{name}: {value};")

    # Spacing
    lines.append("")
    lines.append("  /* Spacing */")
    spacing = tokens.get("spacing", {})
    for name, value in spacing.items():
        lines.append(f"  --spacing-{name}: {value};")

    # Borders
    lines.append("")
    lines.append("  /* Borders */")
    borders = tokens.get("borders", {})
    widths = borders.get("widths", {})
    for name, value in widths.items():
        lines.append(f"  --border-{name}: {value};")

    radius = borders.get("radius", {})
    for name, value in radius.items():
        lines.append(f"  --radius-{name}: {value};")

    # Shadows
    lines.append("")
    lines.append("  /* Shadows */")
    shadows = tokens.get("shadows", {})
    for name, value in shadows.items():
        lines.append(f"  --shadow-{name}: {value};")

    lines.append("}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate CSS variables from design system tokens"
    )
    parser.add_argument(
        "tokens_file",
        type=Path,
        help="Path to tokens JSON file"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output CSS file (default: stdout)"
    )

    args = parser.parse_args()

    if not args.tokens_file.exists():
        print(f"Error: Tokens file not found: {args.tokens_file}", file=sys.stderr)
        sys.exit(1)

    tokens = load_tokens(args.tokens_file)
    css_output = generate_css_variables(tokens)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            f.write(css_output)
        print(f"Generated CSS variables: {args.output}")
    else:
        print(css_output)


if __name__ == "__main__":
    main()
