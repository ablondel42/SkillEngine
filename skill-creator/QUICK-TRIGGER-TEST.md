# Quick Trigger Test Suite

Fast trigger testing for skills. Target: < 2 minutes total.

---

## Purpose

Test whether a skill triggers and follows its workflow when explicitly invoked.

---

## Test Setup (30 sec)

```bash
# 1. Verify skill is registered
ls ~/.qwen/skills/<skill-name>/SKILL.md

# 2. If not registered, register it
mkdir -p ~/.qwen/skills
ln -s /path/to/skill ~/.qwen/skills/<skill-name>
```

---

## Test Cases (3 total, ~30 sec each)

### Test 1: Explicit Skill Invocation

**Prompt:**
```
skill: design-system

I want to build a design system for my React app.
```

**Expected Behavior:**
- [ ] Skill tool invoked (check tool call history)
- [ ] SKILL.md read (check file access)
- [ ] Interview questions asked (7 questions per design-system SKILL.md)
- [ ] No code generated before interview complete

**Pass Criteria:** All 4 checkboxes checked

---

### Test 2: Implicit Skill Usage

**Prompt:**
```
Using the design-system skill, create a component library for my dashboard.
```

**Expected Behavior:**
- [ ] Skill tool invoked
- [ ] SKILL.md read
- [ ] Workflow followed (tokens → components → examples → docs)
- [ ] Token granularity correct (50-900 color shades)

**Pass Criteria:** All 4 checkboxes checked

---

### Test 3: Negative Case (Should NOT Trigger)

**Prompt:**
```
Convert this PDF file to text format.
```

**Expected Behavior:**
- [ ] Design-system skill NOT invoked
- [ ] Appropriate tool used instead (read_file for PDF)
- [ ] No design-system workflow mentioned

**Pass Criteria:** All 3 checkboxes checked

---

## Grading Rubric

| Score | Criteria |
|-------|----------|
| 3/3 | All tests pass |
| 2/3 | Trigger tests pass, negative fails |
| 1/3 | Only explicit trigger works |
| 0/3 | No tests pass |

**Minimum passing:** 2/3

---

## Quick Report Template

```markdown
## Trigger Test Results

**Skill:** <skill-name>
**Date:** <date>
**Tester:** <name>

### Test 1: Explicit Invocation
- Skill invoked: Y/N
- SKILL.md read: Y/N
- Workflow followed: Y/N
- Notes: ...

### Test 2: Implicit Usage
- Skill invoked: Y/N
- SKILL.md read: Y/N
- Workflow followed: Y/N
- Notes: ...

### Test 3: Negative Case
- Skill NOT invoked: Y/N
- Correct tool used: Y/N
- Notes: ...

### Overall Score: X/3
### Issues Found:
1. ...
2. ...

### Recommendations:
1. ...
```

---

## Automation Script

```python
#!/usr/bin/env python3
"""Quick trigger test runner."""

import json
from pathlib import Path

TESTS = [
    {
        "name": "explicit-invocation",
        "prompt": "skill: design-system\n\nI want to build a design system for my React app.",
        "should_trigger": True
    },
    {
        "name": "implicit-usage",
        "prompt": "Using the design-system skill, create a component library.",
        "should_trigger": True
    },
    {
        "name": "negative-pdf",
        "prompt": "Convert this PDF to text.",
        "should_trigger": False
    }
]

def run_tests():
    results = []
    for test in TESTS:
        # Spawn task with test prompt
        # Observe skill invocation
        # Record result
        results.append({
            "name": test["name"],
            "triggered": True/False,
            "expected": test["should_trigger"],
            "pass": True/False
        })
    
    # Save results
    Path("trigger-test-results.json").write_text(
        json.dumps({"tests": results}, indent=2)
    )
    
    # Print summary
    passed = sum(1 for r in results if r["pass"])
    print(f"Trigger Test Results: {passed}/{len(results)} passed")

if __name__ == "__main__":
    run_tests()
```

---

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Skill not invoked | Not registered | `ln -s /path/to/skill ~/.qwen/skills/` |
| Wrong workflow | SKILL.md not read | Check skill path in task |
| Interview skipped | Agent rushed | Add "follow skill workflow" to task |
| Negative triggers | Too broad description | Narrow skill description |

---

## When to Run

- After creating a new skill
- After modifying skill description
- After changing skill workflow
- Before releasing a skill update

---

## Time Budget

| Step | Time |
|------|------|
| Setup (registration check) | 30 sec |
| Test 1 (explicit) | 30 sec |
| Test 2 (implicit) | 30 sec |
| Test 3 (negative) | 30 sec |
| Grading | 30 sec |
| **Total** | **2.5 min** |
