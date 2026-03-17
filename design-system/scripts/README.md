# Design System Scripts

This directory contains helper scripts for working with the design system.

## check_consistency.py

Checks CSS/SCSS files for design system compliance.

```bash
python scripts/check_consistency.py tokens.json src/**/*.css
```

### Features:
- Validates color usage against token definitions
- Checks spacing values for standardization
- Verifies shadow levels match defined tokens
- Confirms border radius values are from the token set

### Output:
- Console report of findings
- Optional JSON output for CI integration
