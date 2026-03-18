# Skill Creator

A skill for creating, testing, and improving AI agent skills.

---

## Overview

This skill helps you build new skills from scratch or improve existing ones through iterative testing and comparison.

**What it does:**
- Guides you through skill creation workflow
- Helps design effective test cases (evals)
- Runs comparison tests (with skill vs without skill)
- Analyzes results to identify improvements
- Optimizes skill descriptions for better triggering

---

## Usage

Use this skill when:
- You want to create a new skill from scratch
- You have an existing skill to improve
- You need to set up test cases for a skill
- You want to measure skill performance
- You need to optimize skill triggering

---

## Workflow

### Creating a New Skill

1. **Capture Intent** — Define what the skill should do
2. **Interview & Research** — Gather requirements and edge cases
3. **Write SKILL.md** — Create the skill definition
4. **Create Test Cases** — Write evals in `evals/evals.json`
5. **Run Tests** — Execute skill on test prompts
6. **Evaluate Results** — Review outputs and grade assertions
7. **Iterate** — Improve skill based on feedback

### Improving an Existing Skill

1. **Run Comparison Tests** — Compare current vs improved version
2. **Analyze Results** — Identify what changed and why
3. **Apply Improvements** — Update skill based on findings
4. **Re-test** — Verify improvements work

---

## File Structure

```
skill-creator/
├── SKILL.md                 # This skill's definition
├── agents/                  # Specialized subagent instructions
│   ├── grader.md           # Grades eval outputs
│   ├── comparator.md       # Blind A/B comparison
│   ├── analyzer.md         # Post-hoc analysis
│   └── test-coordinator.md # Orchestrates testing
├── evals/
│   └── evals.json          # Test cases for skill-creator
├── scripts/                # Testing and utility scripts
│   ├── static_test_suite.py    # Run all static tests
│   ├── run_comparison.py       # With/without comparison
│   ├── trigger_readiness.py    # Trigger optimization
│   └── ...
├── eval-viewer/            # HTML report generation
│   ├── generate_review.py
│   └── viewer.html
└── references/             # Reference documentation
    └── schemas.md          # JSON schemas for evals
```

---

## Testing

### Static Tests (No Subagents)

```bash
# Run all static tests
python3 scripts/static_test_suite.py <skill-path>

# Individual tests
python3 scripts/quick_validate.py <skill-path>
python3 scripts/static_analysis.py <skill-path>
python3 scripts/trigger_readiness.py <skill-path>
```

### Comparison Tests (With Subagents)

```bash
# Run comparison test
python3 scripts/run_comparison.py \
  --eval-set <skill-path>/evals/evals.json \
  --skill-path <skill-path> \
  --output-dir <skill-path>/eval-outputs/comparison
```

---

## Documentation

- [`TESTING-WORKFLOW.md`](../TESTING-WORKFLOW.md) - Complete testing guide
- [`QWEN-COMPATIBLE.md`](./QWEN-COMPATIBLE.md) - Qwen-specific guidance
- [`FAST-TESTING.md`](./FAST-TESTING.md) - Quick testing (<5 min)
- [`TRIGGERING-TEST.md`](./TRIGGERING-TEST.md) - Trigger testing strategy

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `static_test_suite.py` | Run all 5 static tests |
| `run_comparison.py` | With/without skill comparison |
| `quick_validate.py` | Syntax validation |
| `static_analysis.py` | Quality analysis |
| `trigger_readiness.py` | Trigger optimization |
| `review_evals.py` | Eval definitions review |
| `check_structure.py` | File structure validation |

See individual script docstrings for usage details.

---

## Best Practices

1. **Start with static tests** - Quick validation before running expensive tests
2. **Use comparison tests** - Prove skill value vs baseline
3. **Write specific expectations** - Verifiable, not subjective
4. **Test edge cases** - Not just happy paths
5. **Document failures** - Learn from what doesn't work

---

## License

MIT License - See root directory for details.
