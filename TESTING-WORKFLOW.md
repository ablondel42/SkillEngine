# Skill Testing Workflow (Qwen-Compatible)

**Last Updated:** 2026-03-18  
**Status:** Production Ready  
**Test Coverage:** 29 trigger tests + 5 static analyses + 3 comparison tests

---

## Overview

The testing workflow validates skills across multiple dimensions using Qwen's
Task tool. No external CLI authentication required.

**Three Test Suites:**

| Suite | Scripts | Subagents | Use Case |
|-------|---------|-----------|----------|
| **Static Tests** | `static_test_suite.py` | 0 | Quick validation, CI/CD, pre-commit |
| **Trigger Tests** | Manual (Task tool) | Yes | Verify skill triggering behavior |
| **Comparison Tests** | `run_comparison.py` + Task tool | Yes | **PRIMARY: Measure skill added value** |

**Key Principle:** A skill must demonstrate **measurable improvement** over baseline (without skill) to be considered valuable. **Comparison tests are REQUIRED** - execution tests without comparison are meaningless.

---

## Test Philosophy

**Why Comparison Tests Are Essential:**

| Test Type | Question Answered | Value |
|-----------|-------------------|-------|
| **Execution (skill only)** | "Does the skill work?" | Low - doesn't prove value |
| **Comparison (with vs without)** | "Is the skill worth using?" | **High - proves added value** |

**A skill that works but doesn't improve over baseline provides no value.**

Therefore:
- ✅ Static tests: Validate skill structure
- ✅ Trigger tests: Validate skill triggering  
- ✅ **Comparison tests: Validate skill VALUE (PRIMARY METRIC)**
- ❌ Execution-only tests: Removed (meaningless without comparison)

---

## Quick Start

### Run All Static Tests (Recommended for Development)

```bash
# Run all 5 static tests (no subagents, < 1 second)
python3 skill-creator/scripts/static_test_suite.py <skill-path>

# Example
python3 skill-creator/scripts/static_test_suite.py design-system
```

**Tests Included:**
1. Quick Validation (syntax)
2. Static Analysis (quality)
3. Trigger Readiness (optimization)
4. Eval Definitions (structure)
5. File Structure (organization)

---

## Test Types

### Static Tests (No Subagents)

| Test | Script | Time | What It Checks |
|------|--------|------|----------------|
| **Quick Validation** | `quick_validate.py` | < 1s | Syntax, frontmatter, naming |
| **Static Analysis** | `static_analysis.py` | < 1s | Workflow, error handling, evals |
| **Trigger Readiness** | `trigger_readiness.py` | < 1s | Description optimization |
| **Eval Review** | `review_evals.py` | < 1s | Eval structure, testability |
| **File Structure** | `check_structure.py` | < 1s | Required files/directories |

**Run All:** `python3 scripts/static_test_suite.py <skill-path>`

---

### Trigger Tests (With Subagents)

**Comprehensive Suite:** 29 tests across 5 groups

| Group | Tests | Category | File |
|-------|-------|----------|------|
| **Group 1** | 6 | Explicit Commands + Direct Match | `trigger_tests_group1.json` |
| **Group 2** | 6 | Direct Matches + Related Terms | `trigger_tests_group2.json` |
| **Group 3** | 7 | Vague Requests + Component-Specific | `trigger_tests_group3.json` |
| **Group 4** | 6 | Negative Cases (Part 1) | `trigger_tests_group4.json` |
| **Group 5** | 4 | Negative Cases (Part 2) | `trigger_tests_group5.json` |

**Run Individual Group:**
```bash
# Spawn Task subagents for each test in the group
# See design-system/evals/trigger_tests_groupN.json for test cases
```

---

### Comparison Tests (PRIMARY - With Skill vs Without Skill)

**Use for:**
- **Measuring skill added value (REQUIRED)**
- Before/after release validation
- Demonstrating skill effectiveness
- Identifying skill weaknesses

**Principle:** A skill must demonstrate **measurable improvement** over baseline to be considered valuable.

**How It Works:**

For each eval, run TWO executions:
1. **WITH skill** - Uses the skill
2. **WITHOUT skill** - Baseline (no skill invoked)

Then compare both outputs blindly to determine which is better.

**Files:**
- `design-system/evals/eval_group1.json` - SaaS Dashboard
- `design-system/evals/eval_group2.json` - Fitness App
- `design-system/evals/eval_group3.json` - E-commerce

**How to Run:**

```bash
# Run comparison for all 3 evals
python3 skill-creator/scripts/run_comparison.py \
  --eval-set design-system/evals/eval_group1.json \
  --skill-path design-system \
  --output-dir design-system/eval-outputs/comparison-group1

# Repeat for group2 and group3
```

**What Happens:**

1. **Spawn WITH skill subagent**
   - Uses the skill
   - Follows skill workflow
   - Saves to `with_skill/outputs/`

2. **Spawn WITHOUT skill subagent**
   - No skill invoked
   - Handles request directly
   - Saves to `without_skill/outputs/`

3. **Spawn comparator subagent (blind)**
   - Doesn't know which is which
   - Compares outputs against expectations
   - Determines winner with reasoning

4. **Save comparison results**
   - Winner (A/B/TIE)
   - Reasoning
   - Rubric scores
   - Expectation pass rates

**Expected Output:**

```json
{
  "eval_name": "saas-dashboard",
  "winner": "A",
  "winner_type": "with_skill",
  "reasoning": "Output A provides granular design tokens with full 50-900 color palettes, while Output B only has basic colors...",
  "rubric": {
    "A": { "content_score": 4.5, "structure_score": 4.0, "overall_score": 8.5 },
    "B": { "content_score": 2.5, "structure_score": 2.0, "overall_score": 4.5 }
  },
  "expectation_results": {
    "A": { "passed": 14, "total": 16, "pass_rate": 0.875 },
    "B": { "passed": 4, "total": 16, "pass_rate": 0.25 }
  },
  "skill_improvement": "+62.5%"
}
```

**Time:** 10-15 min per comparison (2 executions + 1 comparison)

**Success Criteria:**

| Metric | Threshold |
|--------|-----------|
| Win rate | > 67% (2/3 evals) |
| Avg improvement | > 20% pass rate |
| Key differentiators | Skill provides: granular tokens, domain components, docs |

---

## When to Use Each Test

| Situation | Recommended Tests |
|-----------|-------------------|
| **During development** | Static tests only (`static_test_suite.py`) |
| **Pre-commit** | Static tests only |
| **Before release** | Static + Trigger + **ALL 3 Comparison tests** |
| **Production validation** | Full suite (static + trigger + all 3 comparison tests) |
| **CI/CD pipeline** | Static tests only |
| **Quota limited** | Static tests only |
| **Demonstrating skill value** | **Comparison tests (REQUIRED)** |

---

## Script Status

| Script | Status | Notes |
|--------|--------|-------|
| `static_test_suite.py` | ✅ Production Ready | Run all 5 static tests |
| `quick_validate.py` | ✅ Production Ready | Syntax validation |
| `static_analysis.py` | ✅ Production Ready | Quality analysis |
| `trigger_readiness.py` | ✅ Production Ready | Trigger optimization |
| `review_evals.py` | ✅ Production Ready | Eval definitions |
| `check_structure.py` | ✅ Production Ready | File structure |
| `run_comparison.py` | ✅ Production Ready | With/without skill comparison |
| `run_task_eval.py` | ⚠️ Deprecated | Only used by comparison tests |
| `collect_results.py` | ⚠️ Deprecated | Only used by comparison tests |

---

## Test Results Reference

### Design-System Skill (2026-03-18)

| Test Suite | Tests | Passed | Failed | Success Rate |
|------------|-------|--------|--------|--------------|
| Static Analysis | 5 | 5 | 0 | 100% |
| Trigger Tests | 29 | 29 | 0 | 100% |
| Comparison Tests | 3 | Ready to run | - | - |
| **Total** | **37** | **34** | **0** | **100%** (pending: 3) |

**Trigger Test Breakdown:**
- Explicit Commands: 4/4 (100%)
- Direct Matches: 6/6 (100%)
- Related Terms: 4/4 (100%)
- Vague Requests: 3/3 (100%)
- Component-Specific: 2/2 (100%)
- Negative Cases: 10/10 (100%)

**Static Analysis Scores:**
- Quick Validation: 100%
- Static Analysis: 100%
- Trigger Readiness: 100%
- Eval Definitions: 100%
- File Structure: 100%

**Comparison Tests (Ready to Run):**
- Group 1: SaaS Dashboard - WITH skill vs WITHOUT skill
- Group 2: Fitness App - WITH skill vs WITHOUT skill
- Group 3: E-commerce - WITH skill vs WITHOUT skill

**Success Criteria for Comparison Tests:**
- Win rate: > 67% (2/3 evals)
- Avg improvement: > 20% pass rate
- Key differentiators: Granular tokens, domain components, documentation

---

## File Structure

```
skill-creator/
├── scripts/
│   # Static Tests (no subagents)
│   ├── quick_validate.py        # Syntax validation
│   ├── static_analysis.py       # Quality analysis
│   ├── trigger_readiness.py     # Trigger optimization
│   ├── review_evals.py          # Eval definitions
│   ├── check_structure.py       # File structure
│   ├── static_test_suite.py     # Run all static tests
│   │
│   # Comparison Tests (with subagents)
│   ├── run_comparison.py        # With/without skill comparison
│   │
│   # Deprecated (only used by comparison)
│   ├── run_task_eval.py         # Prepare evals (deprecated)
│   └── collect_results.py       # Aggregate results (deprecated)
│
├── agents/
│   ├── grader.md                # Grade eval outputs
│   ├── comparator.md            # Blind A/B comparison
│   ├── analyzer.md              # Post-hoc analysis
│   └── test-coordinator.md      # Orchestrate testing
│
├── Documentation
│ ├── SKILL.md                   # Skill creator skill
│ ├── QWEN-COMPATIBLE.md         # Qwen compatibility guide
│ ├── FAST-TESTING.md            # Quick testing (3-5 min)
│ ├── NO-SUBAGENT-TESTS.md       # Static testing guide
│ ├── PARALLEL-EXECUTION.md      # Parallel subagent guide
│ ├── QUICK-TRIGGER-TEST.md      # Trigger test templates
│ ├── TRIGGERING-TEST.md         # Complete trigger guide
│ └── TESTING-WORKFLOW.md        # This file
│
└── evals/
    ├── evals.json               # Original eval definitions
    ├── eval_group1.json         # SaaS Dashboard
    ├── eval_group2.json         # Fitness App
    ├── eval_group3.json         # E-commerce
    └── trigger_tests_group[1-5].json  # Trigger test cases
```

---

## Quick Reference

### Run Static Tests
```bash
python3 skill-creator/scripts/static_test_suite.py design-system
```

### Run Individual Static Tests
```bash
python3 skill-creator/scripts/quick_validate.py design-system
python3 skill-creator/scripts/static_analysis.py design-system
python3 skill-creator/scripts/trigger_readiness.py design-system
python3 skill-creator/scripts/review_evals.py design-system
python3 skill-creator/scripts/check_structure.py design-system
```

### Run Comparison Tests (REQUIRED)
```bash
# Group 1: SaaS Dashboard Comparison
python3 skill-creator/scripts/run_comparison.py \
  --eval-set design-system/evals/eval_group1.json \
  --skill-path design-system \
  --output-dir design-system/eval-outputs/comparison-group1

# Group 2: Fitness App Comparison
python3 skill-creator/scripts/run_comparison.py \
  --eval-set design-system/evals/eval_group2.json \
  --skill-path design-system \
  --output-dir design-system/eval-outputs/comparison-group2

# Group 3: E-commerce Comparison
python3 skill-creator/scripts/run_comparison.py \
  --eval-set design-system/evals/eval_group3.json \
  --skill-path design-system \
  --output-dir design-system/eval-outputs/comparison-group3
```

**What Happens:**
1. Prepares `with_skill/` and `without_skill/` directories
2. Spawn TWO subagents per eval (one with skill, one without)
3. Spawn comparator subagent to compare outputs blindly
4. Save comparison results with winner and reasoning

### Clean Up Output Files (After Reviewing Results)
```bash
# Clean up comparison output directories
python3 skill-creator/scripts/run_comparison.py \
  --output-dir design-system/eval-outputs/comparison-group1 --cleanup
```

**Note:** Always clean up after reviewing results to keep the workspace clean.

---

### Run Trigger Tests
```bash
# Spawn Task subagents for each test in group
# See design-system/evals/trigger_tests_groupN.json
```

---

**For questions or issues, refer to `skill-creator/QWEN-COMPATIBLE.md` or the individual test script documentation.**
