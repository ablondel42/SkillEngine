# Fast Skill Testing Guide

Quick testing workflow for rapid iteration. Target: < 5 minutes per test cycle.

---

## Principle: Test Less, Test Smarter

Instead of running 3 full evals (30+ minutes), run:
- **1 trigger test** (does skill activate?)
- **1 execution test** (does skill follow its workflow?)
- **Spot check** (are key outputs present?)

---

## Phase 1: Trigger Compliance Test (1 min)

**Goal:** Verify skill is invoked when explicitly requested.

**Test:**
```
Task: "I want to build a design system for my React app"

Expected:
✅ Agent invokes skill: "design-system"
✅ Agent reads SKILL.md
✅ Agent mentions using the design-system skill
```

**Pass Criteria:**
- Skill tool called within first 2 messages
- SKILL.md read before any code generation
- Skill workflow mentioned

**Fail Criteria:**
- No skill invocation
- Code generated before reading skill
- Generic response without skill mention

---

## Phase 2: Workflow Compliance Test (2 min)

**Goal:** Verify skill follows its own defined workflow.

**Test:**
```
Task: "Using the design-system skill, create a component library"

Expected per SKILL.md:
1. Interview questions (7 required) OR skip with justification
2. Design tokens (colors 50-900, typography, spacing, etc.)
3. Core components
4. Domain components
5. Example pages
6. Documentation (guidelines.md + accessibility.md)
```

**Pass Criteria:**
- Workflow steps followed in order
- Required outputs created
- Token granularity meets spec (50-900 shades)

**Fail Criteria:**
- Steps skipped without reason
- Outputs missing
- Tokens not granular (single colors instead of palettes)

---

## Phase 3: Spot Check (1 min)

**Goal:** Verify key outputs exist.

**Checklist:**
```
□ tokens.ts or tokens.json exists
□ Button component defined
□ Card component defined
□ Domain component created (e.g., StatCard)
□ Example page created
□ guidelines.md exists
□ accessibility.md exists
```

**Pass:** 6/7 or better
**Fail:** 5/7 or worse

---

## Full Workflow (When Needed)

For major changes or before release, run the full workflow:

```bash
# 1. Validate
python3 skill-creator/scripts/quick_validate.py design-system

# 2. Run comparison tests (REQUIRED for production validation)
python3 skill-creator/scripts/run_comparison.py \
  --eval-set design-system/evals/eval_group1.json \
  --skill-path design-system \
  --output-dir design-system/eval-outputs/comparison-group1

# Repeat for group2 and group3
# Each comparison runs WITH skill and WITHOUT skill, then compares blindly
```

**Time:** 10-15 min per comparison (2 executions + 1 comparison)

**Note:** Comparison tests are REQUIRED - execution tests without comparison don't prove skill value.

---

## Choosing Test Depth

| Situation | Test Type | Time |
|-----------|-----------|------|
| Minor edit | Fast test (Phases 1-3) | 3 min |
| New component | Fast test + spot check | 5 min |
| Workflow change | Full execution (1 eval) | 10 min |
| Before release | Full suite (3 evals) | 30 min |
| Bug fix | Fast test only | 3 min |

---

## Trigger Test Templates

Copy/paste these for quick trigger testing:

### Test 1: Explicit mention
```
I want to build a design system for my React app. Can you help?
```

### Test 2: Component library
```
I need to create a component library with consistent styling.
```

### Test 3: Vague app request
```
Build a dashboard for my SaaS product.
```

### Test 4: Negative (should NOT trigger)
```
Convert this PDF to text format.
```

---

## Quick Grading Rubric

| Criteria | Pass | Fail |
|----------|------|------|
| Skill invoked | Within 2 messages | Never or after code |
| Interview step | Asked or justified skip | Skipped silently |
| Token granularity | 50-900 palettes | Single colors |
| Domain components | 3+ created | 0-2 created |
| Documentation | Both .md files | Missing files |

**Overall:** Pass 4/5 or better = skill working

---

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Skill not invoked | Task didn't mention skill | Add "using the X skill" |
| Interview skipped | Agent rushed | Remind "follow skill workflow" |
| Tokens not granular | Agent cut corners | Specify "full 50-900 palettes required" |
| No domain components | Generic approach | Specify domain in prompt |
| Missing docs | Afterthought | Make docs required in task |

---

## Automation Tips

For repeated testing:

1. **Save test prompts** to `evals/quick_tests.json`
2. **Use same output dir** for comparison
3. **Diff outputs** between versions
4. **Track pass/fail** in simple spreadsheet

Example quick_tests.json:
```json
{
  "tests": [
    {
      "name": "explicit-trigger",
      "prompt": "I want to build a design system for my React app",
      "expect_skill": true
    },
    {
      "name": "component-library",
      "prompt": "Create a component library with consistent styling",
      "expect_skill": true
    },
    {
      "name": "negative-pdf",
      "prompt": "Convert this PDF to text",
      "expect_skill": false
    }
  ]
}
```
