# Skill Testing Workflow (Qwen-Compatible)

**Last Updated:** 2026-03-18
**Status:** Production Ready
**Test Coverage:** 16 trigger tests + 3 comparison tests

---

## Overview

The testing workflow validates skills across multiple dimensions using Qwen's
Task tool. No external CLI authentication required.

**Two Test Suites:**

| Suite | Scripts | Subagents | Use Case |
|-------|---------|-----------|----------|
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
- ✅ Trigger tests: Validate skill triggering
- ✅ **Comparison tests: Validate skill VALUE (PRIMARY METRIC)**
- ❌ Execution-only tests: Removed (meaningless without comparison)

---

## Quick Start

### Run Trigger Tests

```bash
# Spawn Task subagents for each of the 16 trigger tests
# See design-system/evals/trigger_tests.json for all test cases
```

---

## Test Types

### Trigger Tests (With Subagents)

**Curated Suite:** 16 tests in a single batch (45% reduction from 29)

| Category | Tests | Description |
|----------|-------|-------------|
| Explicit Commands | 2 | Slash (`/design-system`) and colon (`skill:`) syntax |
| Direct Matches | 3 | "Design system", "component library", "UI kit" |
| Related Terms | 2 | "Design tokens", "UI building blocks" |
| Vague Requests | 2 | Implied design needs with varying specificity |
| Component-Specific | 2 | Basic components + accessibility-focused |
| Negative Cases | 5 | Unrelated domains: file, script, DB, infra, ML |
| **Total** | **16** | **Essential coverage without redundancy** |

**Run Trigger Tests:**
```bash
# Spawn Task subagents for each test
# See design-system/evals/trigger_tests.json for all 16 test cases
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

**File:** `design-system/evals/evals.json` - All 3 evals in a single batch

| Eval | Domain | Stack |
|------|--------|-------|
| **saas-dashboard-nextjs-shadcn** | B2B SaaS | Next.js, Tailwind, shadcn/ui |
| **fitness-app-react-styled-components** | Consumer Mobile | React, styled-components |
| **ecommerce-vue-tailwind-luxury** | E-commerce | Vue 3, Tailwind, luxury |

**How to Run:**

```bash
# Run comparison for all 3 evals in a single batch
python3 skill-creator/scripts/run_comparison.py \
  --eval-set design-system/evals/evals.json \
  --skill-path design-system \
  --output-dir design-system/eval-outputs/comparison
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
| **During development** | Trigger tests (subset if needed) |
| **Pre-commit** | Trigger tests (critical paths only) |
| **Before release** | **ALL** trigger tests + **ALL 3 comparison tests** |
| **Production validation** | Full suite (trigger + all 3 comparison tests) |
| **CI/CD pipeline** | Trigger tests (subset) |
| **Quota limited** | Trigger tests only (16 tests) |
| **Demonstrating skill value** | **Comparison tests (REQUIRED)** |

---

## Script Status

| Script | Status | Notes |
|--------|--------|-------|
| `run_comparison.py` | ✅ Production Ready | With/without skill comparison |
| `run_task_eval.py` | ⚠️ Deprecated | Only used by comparison tests |
| `collect_results.py` | ⚠️ Deprecated | Only used by comparison tests |

---

## Test Results Reference

### Design-System Skill (2026-03-18)

| Test Suite | Tests | Passed | Failed | Success Rate |
|------------|-------|--------|--------|--------------|
| Trigger Tests | 16 | Ready to run | - | - |
| Comparison Tests | 3 | Ready to run | - | - |
| **Total** | **19** | **0** | **0** | **Pending** |

**Trigger Test Breakdown:**
- Explicit Commands: 2 tests
- Direct Matches: 3 tests
- Related Terms: 2 tests
- Vague Requests: 2 tests
- Component-Specific: 2 tests
- Negative Cases: 5 tests

**Comparison Tests (Ready to Run):**
- saas-dashboard-nextjs-shadcn: WITH skill vs WITHOUT skill
- fitness-app-react-styled-components: WITH skill vs WITHOUT skill
- ecommerce-vue-tailwind-luxury: WITH skill vs WITHOUT skill

**Success Criteria for Comparison Tests:**
- Win rate: > 67% (2/3 evals)
- Avg improvement: > 20% pass rate
- Key differentiators: Granular tokens, domain components, documentation

---

## File Structure

```
skill-creator/
├── scripts/
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
│ ├── PARALLEL-EXECUTION.md      # Parallel subagent guide
│ └── TESTING-WORKFLOW.md        # This file
│
└── evals/
    ├── evals.json               # All 3 prompt evals (consolidated)
    └── trigger_tests.json       # All 16 trigger tests (consolidated)
```

---

## Quick Reference

### Run Trigger Tests
```bash
# Spawn Task subagents for each of the 16 trigger tests
# See design-system/evals/trigger_tests.json for all test cases
```

### Run Comparison Tests (REQUIRED)
```bash
# Run comparison for all 3 evals in a single batch
python3 skill-creator/scripts/run_comparison.py \
  --eval-set design-system/evals/evals.json \
  --skill-path design-system \
  --output-dir design-system/eval-outputs/comparison
```

**What Happens:**
1. Prepares `with_skill/` and `without_skill/` directories
2. Spawn TWO subagents per eval (one with skill, one without)
3. Spawn comparator subagent to compare outputs blindly
4. Save comparison results with winner and reasoning

### Clean Up Output Files (After Reviewing Results)
```bash
# Clean up comparison output directory
python3 skill-creator/scripts/run_comparison.py \
  --output-dir design-system/eval-outputs/comparison --cleanup
```

**Note:** Always clean up after reviewing results to keep the workspace clean.

---

**For questions or issues, refer to `skill-creator/QWEN-COMPATIBLE.md` or the individual test script documentation.**
