# Code Quality Tools

Automated code quality audit, fix, and monitoring tools for SkillEngine.

## Quick Start

```bash
# Run a quality audit
python scripts/audit_quality.py --verbose

# Auto-fix common issues
python scripts/fix_quality.py --dry-run  # Preview first
python scripts/fix_quality.py            # Apply fixes

# Generate quality dashboard
python scripts/quality_dashboard.py
```

## Tools Overview

### 1. Quality Audit (`audit_quality.py`)

Performs comprehensive code quality analysis and generates detailed reports.

**Checks:**
- 🔴 **Critical**: Bare except clauses
- 🟠 **High**: Functions >50 lines
- 🟡 **Medium**: Missing docstrings, duplicate code
- 🟢 **Low**: Missing type hints, magic numbers, long lines

**Usage:**
```bash
# Basic audit
python scripts/audit_quality.py

# With JSON output
python scripts/audit_quality.py --output quality-audit.json

# Verbose with detailed findings
python scripts/audit_quality.py --verbose

# Custom threshold (fail if score < 80)
python scripts/audit_quality.py --threshold 80

# Exclude additional patterns
python scripts/audit_quality.py --exclude vendor tools
```

**Output:**
- Console report with severity breakdown
- JSON report (with `--output`)
- Exit code based on score (0=excellent, 1=needs improvement, 2=poor)

### 2. Quality Fixer (`fix_quality.py`)

Automatically fixes common code quality issues.

**Fixes:**
- `error_handling`: Bare `except:` → `except Exception as e:`
- `documentation`: Adds stub docstrings to functions
- `type_safety`: Adds `-> None` return types
- `maintainability`: Extracts magic numbers to constants

**Usage:**
```bash
# Preview fixes (dry run)
python scripts/fix_quality.py --dry-run

# Apply all fixes
python scripts/fix_quality.py

# Fix specific categories only
python scripts/fix_quality.py --category error_handling documentation

# Verbose output
python scripts/fix_quality.py --verbose
```

**⚠️ Warning:** Always review auto-fixes before committing. Run with
`--dry-run` first to preview changes.

### 3. Quality Dashboard (`quality_dashboard.py`)

Generates visual HTML dashboard with trends and metrics.

**Features:**
- Overall quality score (0-100)
- Trend charts over time
- Issue distribution by severity/category
- Detailed findings table
- Prioritized recommendations

**Usage:**
```bash
# Generate dashboard (requires audit JSON)
python scripts/quality_dashboard.py

# Custom output file
python scripts/quality_dashboard.py --output dashboard.html

# Custom history file
python scripts/quality_dashboard.py --history .my-history.json
```

**Output:**
- `quality-dashboard.html` - Visual dashboard
- `.quality-history.json` - Trend data (auto-updated)

## Pre-commit Hooks

Automatically run quality checks before each commit.

**Setup:**
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files (optional)
pre-commit run --all-files
```

**Hooks configured:**
- `audit-quality` - Runs quality audit (threshold: 70)
- `validate-skills` - Validates SKILL.md files
- `static-analysis` - Runs static analysis
- Plus: ruff, mypy, bandit, trailing whitespace, etc.

## CI/CD Integration

Quality audit runs automatically in GitHub Actions:

- **On every PR/push**: Quality gate check (threshold: 80)
- **Weekly**: Full audit with dashboard generation
- **Artifacts**: Reports retained for 30 days

**Workflow jobs:**
1. `code-quality-audit` - Runs audit and generates dashboard
2. `quality-gate-check` - Fails if score < 80
3. `test-summary` - Aggregates all test results

## Quality Score Calculation

Scores are calculated as follows:

```
Base Score: 100

Deductions:
- Critical issues: -10 points each
- High issues: -5 points each
- Medium issues: -2 points each
- Low issues: -1 point each

Bonuses:
- >90% docstring coverage: +5 points
- >70% docstring coverage: +2 points

Final Score: max(0, min(100, base - deductions + bonuses))
```

**Score interpretation:**
- 90-100: ✅ Excellent
- 70-89: ✅ Good
- 50-69: ⚠️ Needs Improvement
- 0-49: ❌ Poor

## Recommended Workflow

### Daily Development

```bash
# Before committing
python scripts/fix_quality.py --dry-run
python scripts/audit_quality.py --threshold 70
```

### Weekly Maintenance

```bash
# Run full audit and generate dashboard
python scripts/audit_quality.py --output quality-audit.json
python scripts/quality_dashboard.py

# Review dashboard in browser
open quality-dashboard.html
```

### Before Release

```bash
# Ensure high quality threshold
python scripts/audit_quality.py --threshold 90 --verbose

# Apply safe auto-fixes
python scripts/fix_quality.py --category error_handling

# Review remaining issues
python scripts/fix_quality.py --dry-run --category documentation type_safety
```

## Troubleshooting

### Audit score dropped suddenly

1. Check `.quality-history.json` for trend data
2. Open `quality-dashboard.html` to see new issues
3. Run `audit_quality.py --verbose` for details

### Auto-fix broke something

1. Review git diff before committing
2. Run tests after applying fixes
3. Exclude specific categories: `--category error_handling`

### Pre-commit hook failing

```bash
# See what's failing
pre-commit run --all-files --verbose

# Temporarily skip (not recommended)
git commit --no-verify
```

### Dashboard not loading

1. Ensure audit JSON exists: `quality-audit.json`
2. Check browser console for errors
3. Regenerate: `python quality_dashboard.py`

## Configuration

### pyproject.toml

Quality tools respect settings in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100

[tool.mypy]
python_version = "3.10"

[tool.audit-quality]
threshold = 80
exclude = ["tests", "vendor"]
```

### Custom Rules

Extend the auditor by adding custom checks in `audit_quality.py`:

```python
def check_custom_rule(self, file_path: Path, content: str) -> None:
    """Add your custom quality check."""
    # Your logic here
    self.findings.append(Finding(...))
```

## Metrics Tracked

| Metric | Description | Target |
|--------|-------------|--------|
| Quality Score | Overall code quality (0-100) | ≥80 |
| Doc Coverage | % functions with docstrings | ≥90% |
| Critical Issues | Bare except, security issues | 0 |
| High Issues | Long functions, complexity | <5 |
| Files Scanned | Total Python files audited | - |
| Lines Scanned | Total lines of code | - |

## Export Formats

**JSON Report** (`--output report.json`):
```json
{
  "timestamp": "2026-03-18T10:30:00",
  "score": 92,
  "total_files": 45,
  "total_lines": 8234,
  "findings": [...],
  "summary": {...}
}
```

**HTML Dashboard** (`quality-dashboard.html`):
- Interactive charts (Chart.js)
- Sortable findings table
- Trend visualization
- Actionable recommendations

## Best Practices

1. **Run audit frequently** - Catch issues early
2. **Review auto-fixes** - Don't blindly apply
3. **Track trends** - Use dashboard for improvement
4. **Set realistic thresholds** - Start at 70, aim for 90
5. **Fix critical first** - Prioritize by severity

## Contributing

To add new quality checks:

1. Add check method to `CodeQualityAuditor`
2. Add corresponding fix to `CodeQualityFixer`
3. Update documentation
4. Add tests for new checks

## License

Part of SkillEngine codebase.
