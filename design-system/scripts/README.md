# Design System Scripts

Helper scripts for working with design system tokens and CSS.

---

## check_consistency.py

Validates CSS/SCSS files against design token definitions.

**Usage:**
```bash
python3 scripts/check_consistency.py <tokens.json> <css_files...>
```

**Example:**
```bash
python3 scripts/check_consistency.py tokens.json src/**/*.css
```

**What it checks:**
- Color values match defined token palette
- Spacing values use standard scale (4px base)
- Shadow levels match defined tokens
- Border radius values are from token set

**Output:**
- Console report of findings
- Optional JSON output (`--json` flag) for CI integration

---

## generate_css.py

Generates CSS custom properties from design tokens JSON.

**Usage:**
```bash
python3 scripts/generate_css.py <tokens.json> [-o output.css]
```

**Example:**
```bash
# Output to stdout
python3 scripts/generate_css.py tokens.json

# Output to file
python3 scripts/generate_css.py tokens.json -o styles/globals.css
```

**What it generates:**
- `--color-*` variables for all color tokens
- `--font-*` variables for font families
- `--text-*` variables for font sizes
- `--spacing-*` variables for spacing scale
- `--border-*` variables for border widths and radius
- `--shadow-*` variables for shadow levels

**Output format:**
```css
:root {
  --color-primary: #3b82f6;
  --color-primary-50: #eff6ff;
  --color-primary-900: #1e3a8a;
  --font-heading: 'Inter', sans-serif;
  --text-sm: 0.875rem;
  --spacing-4: 1rem;
  --radius-md: 0.5rem;
  --shadow-md: 0 4px 6px rgb(0 0 0 / 0.1);
}
```

---

## Token Format

Both scripts expect a `tokens.json` file with this structure:

```json
{
  "colors": {
    "primary": "#3b82f6",
    "primary-50": "#eff6ff",
    "primary-900": "#1e3a8a"
  },
  "typography": {
    "fonts": {
      "heading": "'Inter', sans-serif",
      "body": "'Inter', sans-serif"
    },
    "sizes": {
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem"
    }
  },
  "spacing": {
    "0": "0",
    "4": "1rem",
    "8": "2rem"
  },
  "borders": {
    "widths": {
      "1px": "1px",
      "2px": "2px"
    },
    "radius": {
      "sm": "0.25rem",
      "md": "0.5rem"
    }
  },
  "shadows": {
    "sm": "0 1px 2px rgb(0 0 0 / 0.05)",
    "md": "0 4px 6px rgb(0 0 0 / 0.1)"
  }
}
```

See `references/schemas.md` for the full JSON schema.

---

## Dependencies

Both scripts use only Python standard library:
- `argparse` - CLI argument parsing
- `json` - JSON parsing
- `re` - Regular expressions for CSS parsing
- `pathlib` - Path handling

No external dependencies required.

---

## Integration

### In Your Build Process

```bash
# Generate CSS during build
python3 scripts/generate_css.py tokens.json -o dist/styles.css

# Validate CSS before deploy
python3 scripts/check_consistency.py tokens.json dist/**/*.css
```

### In CI/CD

```yaml
# Example GitHub Actions step
- name: Validate CSS against tokens
  run: |
    python3 scripts/check_consistency.py tokens.json src/**/*.css --json > css-report.json
```

---

## Troubleshooting

**"No module named 'yaml'"**
- These scripts don't use yaml - you may be running a different script

**"File not found: tokens.json"**
- Ensure you're running from the design-system directory
- Or provide full path: `python3 scripts/generate_css.py /path/to/tokens.json`

**"Invalid JSON"**
- Check your tokens.json syntax
- Validate against schema in `references/schemas.md`
