# Parallel Execution Guide

**Key Finding:** Qwen subagents CAN run in parallel when spawned in the SAME message.

---

## How It Works

**Sequential (SLOW - Don't Use):**
```
Message 1: Spawn subagent 1 → Wait 10 min → Complete
Message 2: Spawn subagent 2 → Wait 10 min → Complete
Message 3: Spawn subagent 3 → Wait 10 min → Complete
Total: 30 minutes
```

**Parallel (FAST - Use This):**
```
Message 1: Spawn subagent 1 + 2 + 3 together
           → All run concurrently
           → All complete in ~10-15 min
Total: 10-15 minutes
Time saved: 50%
```

---

## How to Spawn Parallel Subagents

### Correct Way (Parallel)

Spawn ALL subagents in ONE message:

```
[Task: Eval 1] [Task: Eval 2] [Task: Eval 3]
     ↓              ↓              ↓
  Runs          Runs           Runs
  concurrently  concurrently   concurrently
```

**Example:**
```
Spawn 3 subagents with these prompts:

Subagent 1: "Execute eval 1: SaaS Dashboard design system..."
Subagent 2: "Execute eval 2: Fitness App design system..."
Subagent 3: "Execute eval 3: E-commerce design system..."

All 3 run at the same time.
```

### Wrong Way (Sequential)

Spawn subagents one at a time in separate messages:

```
Message 1: [Task: Eval 1] → Wait for completion
Message 2: [Task: Eval 2] → Wait for completion
Message 3: [Task: Eval 3] → Wait for completion
```

**Don't do this** - it's 3x slower.

---

## Time Comparison

| Scenario | Sequential | Parallel | Savings |
|----------|------------|----------|---------|
| 3 evals (10 min each) | 30 min | 10-15 min | 50-67% |
| 3 graders (2 min each) | 6 min | 2-3 min | 50-67% |
| Full test cycle | 40 min | 15-20 min | 50-60% |

---

## Parallel Execution Template

### For 3 Evals

```
Spawn these subagents in the SAME message for EACH comparison:

**For Eval 1 (SaaS Dashboard) - Comparison:**

```
# Subagent 1: WITH skill
Task: Execute using design-system skill
Prompt: [eval 1 prompt]
Output: eval-outputs/comparison-group1/eval-1/with_skill/outputs/

# Subagent 2: WITHOUT skill
Task: Execute WITHOUT using any skills
Prompt: [eval 1 prompt]
Output: eval-outputs/comparison-group1/eval-1/without_skill/outputs/
```

**For Eval 2 (Fitness App) - Comparison:**

```
# Subagent 1: WITH skill
Output: eval-outputs/comparison-group2/eval-1/with_skill/outputs/

# Subagent 2: WITHOUT skill
Output: eval-outputs/comparison-group2/eval-1/without_skill/outputs/
```

**For Eval 3 (E-commerce) - Comparison:**

```
# Subagent 1: WITH skill
Output: eval-outputs/comparison-group3/eval-1/with_skill/outputs/

# Subagent 2: WITHOUT skill
Output: eval-outputs/comparison-group3/eval-1/without_skill/outputs/
```

### For Parallel Comparison

```
Spawn these comparator subagents in the SAME message:

**Comparator 1: Compare Eval 1**
Task: Compare two outputs blindly
Output A: eval-outputs/comparison-group1/eval-1/with_skill/outputs/
Output B: eval-outputs/comparison-group1/eval-1/without_skill/outputs/
Output: eval-outputs/comparison-group1/eval-1/comparison.json

**Comparator 2: Compare Eval 2**
Output A: eval-outputs/comparison-group2/.../with_skill/outputs/
Output B: eval-outputs/comparison-group2/.../without_skill/outputs/
Output: eval-outputs/comparison-group2/eval-1/comparison.json

**Comparator 3: Compare Eval 3**
Output A: eval-outputs/comparison-group3/.../with_skill/outputs/
Output B: eval-outputs/comparison-group3/.../without_skill/outputs/
Output: eval-outputs/comparison-group3/eval-1/comparison.json
```

---

## Best Practices

### DO

✅ Spawn all subagents in ONE message  
✅ Use clear task descriptions  
✅ Specify output directories  
✅ Include all context in prompt  

### DON'T

❌ Spawn subagents in separate messages  
❌ Wait for one to complete before spawning next  
❌ Mix sequential and parallel (pick one)  

---

## Limitations

**Quota limits:**
- Free tier: Limited subagent calls per day
- Parallel execution uses quota faster
- Plan accordingly for large test runs

**Resource limits:**
- Too many parallel subagents may hit rate limits
- Recommended: 3-5 subagents max per message
- For more, split into multiple messages

---

## Example: Full Parallel Test Cycle

```bash
# Step 1: Validate (sequential)
python3 quick_validate.py design-system

# Step 2: Prepare comparison (sequential)
python3 run_comparison.py --eval-set evals/eval_group1.json ...

# Step 3: Execute comparison (PARALLEL)
# Spawn 2 subagents in ONE message for each eval:
# - Subagent 1: WITH skill
# - Subagent 2: WITHOUT skill
# Wait 10-15 min

# Step 4: Compare outputs (PARALLEL)
# Spawn comparator subagents in ONE message:
# - Comparator 1: Compare Eval 1 outputs
# - Comparator 2: Compare Eval 2 outputs
# - Comparator 3: Compare Eval 3 outputs
# Wait 5-10 min

# Step 5: Clean up (sequential)
python3 run_comparison.py --output-dir eval-outputs/comparison-group1 --cleanup
```

**Total time:** 15-25 min (with parallel execution)
**Sequential time:** 40+ min
**Time saved:** ~50%

---

## Verification Test

To verify parallel execution works:

```
Spawn 3 subagents in ONE message:
- Subagent 1: "Wait 10 seconds, report completion time"
- Subagent 2: "Wait 10 seconds, report completion time"
- Subagent 3: "Wait 10 seconds, report completion time"

Expected: All complete in ~10 seconds (not 30 seconds)
```

**Result:** ✅ Confirmed - parallel execution works!

---

## References

- `TESTING-WORKFLOW.md` - Complete workflow with parallel execution
- `skill-creator/TRIGGERING-TEST.md` - Trigger testing guide
- `skill-creator/FAST-TESTING.md` - Quick testing (3-5 min)
