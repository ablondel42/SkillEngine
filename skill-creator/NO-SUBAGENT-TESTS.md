# No-Subagent Test Suite

Complete skill testing without any API calls or subagent execution.

---

## Overview

This test suite runs **100% locally** with zero subagent calls. Perfect for:
- Limited quota situations
- Quick iteration during development
- CI/CD pipelines
- Pre-commit checks

---

## Tests Included

| Test | Script | Time | Subagents |
|------|--------|------|-----------|
| Quick Validation | `quick_validate.py` | < 1 sec | 0 |
| Static Analysis | `static_analysis.py` | < 1 sec | 0 |
| Eval Definition Review | `review_evals.py` | < 1 sec | 0 |
| File Structure Check | `check_structure.py` | < 1 sec | 0 |

**Total time:** < 5 seconds  
**Total subagents:** 0

---

## Running the Full Suite

```bash
# Run all tests
python3 skill-creator/scripts/test_suite.py design-system

# Or run individually:

# 1. Quick Validation (syntax check)
python3 skill-creator/scripts/quick_validate.py design-system

# 2. Static Analysis (quality check)
python3 skill-creator/scripts/static_analysis.py design-system

# 3. Eval Review (eval definitions)
python3 skill-creator/scripts/review_evals.py design-system

# 4. Structure Check (file organization)
python3 skill-creator/scripts/check_structure.py design-system
```

---

## What Gets Tested

### 1. Quick Validation ✅

**Checks:**
- SKILL.md exists
- Frontmatter is valid YAML
- Required fields present (name, description)
- Naming conventions (kebab-case)
- Description format (no angle brackets)
- Length limits respected

**Pass/Fail:** Binary

### 2. Static Analysis ✅

**Checks:**
- Description quality (length, trigger phrases)
- Workflow definition (steps, phases)
- Examples/output formats
- Reference files present
- Eval definitions present
- Helper scripts present
- Documentation quality

**Score:** 0-100%

### 3. Eval Definition Review ✅

**Checks:**
- Evals file exists and is valid JSON
- Each eval has required fields (id, prompt, expectations)
- Expectations are verifiable (not subjective)
- Prompts are realistic
- Coverage across different use cases

**Score:** Pass/Fail per eval

### 4. File Structure Check ✅

**Checks:**
- Required directories exist (evals/, references/)
- Required files exist (SKILL.md, evals/*.json)
- Optional directories present (scripts/, assets/)
- File naming conventions
- No orphaned files

**Score:** Pass/Fail per check

---

## Example Output

```
============================================================
NO-SUBAGENT TEST SUITE
============================================================

Skill: design-system
Path: /Users/arnaud/dev/SkillEngine/design-system

TEST 1: Quick Validation
✅ PASS - Skill is valid

TEST 2: Static Analysis
✅ PASS - Score: 90/95 (94.7%)
  - Description: 616 chars (slightly long)
  - Trigger phrases: 5 found
  - Workflow steps: 3 found
  - References: 9 files
  - Evals: 3 defined
  - Scripts: 2 found

TEST 3: Eval Definition Review
✅ PASS - 3 evals reviewed
  - Eval 1: saas-dashboard-nextjs-shadcn ✅
  - Eval 2: fitness-app-react-styled-components ✅
  - Eval 3: ecommerce-vue-tailwind-luxury ✅

TEST 4: File Structure Check
✅ PASS - Structure is correct
  - SKILL.md ✅
  - evals/eval_group*.json ✅ (3 eval groups)
  - references/ (9 files) ✅
  - scripts/ (2 files) ✅

============================================================
OVERALL: ✅ ALL TESTS PASSED
============================================================

Total time: 0.5 seconds
Subagents used: 0
```

---

## When to Use

**Use no-subagent tests for:**
- ✅ Quick iteration during development
- ✅ Pre-commit checks
- ✅ CI/CD pipelines
- ✅ When quota is limited
- ✅ Initial skill review

**Use subagent tests for:**
- ✅ Final validation before release
- ✅ Workflow compliance verification
- ✅ Output quality assessment
- ✅ Comparative testing (with/without skill)

---

## Test Frequency

| Test Type | When to Run |
|-----------|-------------|
| No-subagent suite | Every change |
| Trigger tests | Once per skill |
| Single eval | Major changes |
| Full parallel evals | Before release only |

---

## Creating the Test Suite Script

Create `skill-creator/scripts/test_suite.py`:

```python
#!/usr/bin/env python3
"""Run all no-subagent tests."""

import subprocess
import sys
from pathlib import Path

def run_test(name: str, command: list) -> bool:
    """Run a test and return success/failure."""
    print(f"\n{name}")
    print("-" * 40)
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_suite.py <skill_directory>")
        sys.exit(1)
    
    skill_path = Path(sys.argv[1])
    script_dir = Path(__file__).parent
    
    print("="*60)
    print("NO-SUBAGENT TEST SUITE")
    print("="*60)
    print(f"\nSkill: {skill_path.name}")
    
    tests = [
        ("TEST 1: Quick Validation", 
         ["python3", script_dir / "quick_validate.py", skill_path]),
        
        ("TEST 2: Static Analysis",
         ["python3", script_dir / "static_analysis.py", skill_path]),
        
        ("TEST 3: Eval Definition Review",
         ["python3", script_dir / "review_evals.py", skill_path]),
        
        ("TEST 4: File Structure Check",
         ["python3", script_dir / "check_structure.py", skill_path]),
    ]
    
    results = []
    for name, command in tests:
        results.append(run_test(name, command))
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"OVERALL: ✅ ALL {total} TESTS PASSED")
    else:
        print(f"OVERALL: ⚠️  {passed}/{total} TESTS PASSED")
    
    print("="*60)
    print(f"\nTotal time: < 5 seconds")
    print(f"Subagents used: 0")
    
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
```

---

## Benefits

| Benefit | Impact |
|---------|--------|
| **Zero quota usage** | Unlimited runs |
| **Fast execution** | < 5 seconds |
| **CI/CD friendly** | Automated checks |
| **Early detection** | Catch issues before subagent tests |
| **Consistent** | No flakiness from API calls |

---

## Limitations

**What no-subagent tests CAN check:**
- ✅ File structure
- ✅ Syntax validity
- ✅ Description quality
- ✅ Eval definitions
- ✅ Documentation completeness

**What no-subagent tests CANNOT check:**
- ❌ Actual skill execution
- ❌ Workflow compliance
- ❌ Output quality
- ❌ Trigger behavior
- ❌ Real-world performance

**Recommendation:** Use no-subagent tests for development, subagent tests for validation.

---

## References

- `skill-creator/scripts/static_analysis.py` - Static analysis script
- `skill-creator/scripts/quick_validate.py` - Syntax validation
- `TESTING-WORKFLOW.md` - Complete testing workflow
- `skill-creator/PARALLEL-EXECUTION.md` - Parallel execution guide
