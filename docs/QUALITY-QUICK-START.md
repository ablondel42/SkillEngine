# Code Quality Tools - Quick Reference

## Commands

```bash
# Audit code quality
python scripts/audit_quality.py --verbose

# Auto-fix issues (preview first!)
python scripts/fix_quality.py --dry-run
python scripts/fix_quality.py

# Generate dashboard
python scripts/quality_dashboard.py
open quality-dashboard.html
```

## Common Workflows

### Before Commit
```bash
python scripts/audit_quality.py --threshold 70
```

### Weekly Review
```bash
python scripts/audit_quality.py --output quality-audit.json
python scripts/quality_dashboard.py
open quality-dashboard.html
```

### Fix Common Issues
```bash
# Preview
python scripts/fix_quality.py --dry-run

# Apply error handling fixes only
python scripts/fix_quality.py --category error_handling

# Apply all fixes
python scripts/fix_quality.py
```

## Score Targets

| Score | Status | Action |
|-------|--------|--------|
| 90-100 | ✅ Excellent | Maintain |
| 70-89 | ✅ Good | Minor improvements |
| 50-69 | ⚠️ Needs Work | Fix high priority |
| 0-49 | ❌ Poor | Run auto-fix + review |

## Files Generated

| File | Description |
|------|-------------|
| `quality-audit.json` | Detailed audit results |
| `quality-dashboard.html` | Visual dashboard |
| `.quality-history.json` | Trend data |

## Pre-commit Setup

```bash
pip install pre-commit
pre-commit install
```

## CI/CD

Quality audit runs automatically:
- On every PR/push (threshold: 80)
- Weekly (Monday 9 AM UTC)
- Reports uploaded as artifacts

## Documentation

Full docs: `docs/CODE-QUALITY-TOOLS.md`
