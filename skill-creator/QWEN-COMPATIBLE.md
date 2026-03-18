# Qwen-Compatible Skill Testing Framework

This document describes how to test and improve skills using Qwen's Task tool
instead of Claude Code's `claude -p` subprocesses.

---

## Architecture Differences

| Claude Code | Qwen Code |
|-------------|-----------|
| `claude -p` subprocesses | Task tool subagents |
| `.claude/commands/` registration | Direct skill file reference |
| Auto-trigger by description | Explicit skill invocation |
| Stream JSON parsing | Direct task output capture |

---

## Skill Anatomy (Unchanged)

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code
    ├── references/ - Documentation
    └── assets/     - Templates, resources
```

---

## Testing Workflow (Qwen-Compatible)

### Phase 1: Quick Validation

```bash
python3 skill-creator/scripts/quick_validate.py <skill-path>
```

Validates SKILL.md syntax, frontmatter, naming conventions.

---

### Phase 2: Manual Trigger Testing

Since Qwen doesn't auto-trigger skills by description matching, we test
**explicit skill invocation compliance**:

**Test Query:** "I want to build a design system for my React app"

**Expected Behavior:**
1. Agent explicitly invokes: `skill: "design-system"`
2. Agent reads SKILL.md
3. Agent follows skill workflow (interview-first, etc.)
4. Agent produces skill-defined outputs

**Grading Criteria:**
- ✅ Skill invoked explicitly
- ✅ Workflow followed (per SKILL.md)
- ✅ Outputs match skill specification
- ❌ Skill not invoked = FAIL
- ❌ Workflow skipped = FAIL

---

### Phase 3: Comparison Testing (REQUIRED)

**Step 1: Prepare comparison structure**

```bash
python3 skill-creator/scripts/run_comparison.py \
  --eval-set design-system/evals/eval_group1.json \
  --skill-path design-system \
  --output-dir design-system/eval-outputs/comparison-group1
```

**Step 2: Spawn subagents for comparison**

For each eval, spawn TWO subagents in the same message:

```
# Subagent 1: WITH skill
Task: Execute this task using the {skill_name} skill
Skill path: {skill_path}
Task prompt: {eval_prompt}
Output directory: {with_skill_dir}/outputs/

# Subagent 2: WITHOUT skill
Task: Execute this task WITHOUT using any skills
Task prompt: {eval_prompt}
Output directory: {without_skill_dir}/outputs/
```

**Step 3: Compare outputs (blind)**

Spawn comparator subagent:

```
Task: Compare two outputs blindly (you don't know which is which)

Output A: {output_a_dir}
Output B: {output_b_dir}
Eval prompt: {prompt}
Expectations: {expectations}

Generate rubric based on task requirements.
Score both outputs on content and structure.
Determine winner and explain why.

Save comparison.json to the eval output directory.
```

---

### Phase 4: Comparative Testing (A/B)

**Step 1: Run with-skill**

```
Task: Execute this task using the {skill_name} skill
Task prompt: {eval_prompt}
Output dir: {output_dir}/with_skill/
```

**Step 2: Run without-skill (baseline)**

```
Task: Execute this task WITHOUT using any skills
Task prompt: {eval_prompt}
Output dir: {output_dir}/without_skill/
```

**Step 3: Compare outputs**

Spawn comparator subagent:

```
Task: Compare two outputs (blind comparison)

Output A: {output_a_dir}
Output B: {output_b_dir}
Eval prompt: {eval_prompt}
Expectations: {expectations}

Generate rubric based on task requirements.
Score both outputs on content and structure.
Determine winner and explain why.

Save comparison.json with winner, reasoning, rubric scores.
```

---

## Scripts (Qwen-Compatible)

### quick_validate.py

Validates SKILL.md syntax and structure.

### run_comparison.py

Prepares comparison test structure.
Creates with_skill/ and without_skill/ directories.
Supports --cleanup flag to remove test artifacts.

### static_test_suite.py

Runs all 5 static tests (no subagents).
Includes: quick_validate, static_analysis, trigger_readiness, review_evals, check_structure.

---

## Agents (Modified for Qwen)

### grader.md

**Input changes:**
- Receives paths via task prompt (not CLI args)
- Saves grading.json to eval output directory

**Output format:**
```json
{
  "eval_id": 1,
  "expectations": [
    {
      "text": "The output includes X",
      "passed": true,
      "evidence": "Found in transcript line 42..."
    }
  ],
  "summary": {
    "passed": 5,
    "failed": 2,
    "total": 7,
    "pass_rate": 0.71
  }
}
```

### comparator.md

**Input changes:**
- Receives output paths via task prompt
- Produces comparison.json with blind evaluation

**Output format:**
```json
{
  "winner": "A",
  "reasoning": "Output A provides...",
  "rubric": {
    "A": { "content_score": 4.5, "structure_score": 4.0, "overall_score": 8.5 },
    "B": { "content_score": 3.0, "structure_score": 3.5, "overall_score": 6.5 }
  },
  "expectation_results": {
    "A": { "passed": 6, "total": 7, "pass_rate": 0.86 },
    "B": { "passed": 3, "total": 7, "pass_rate": 0.43 }
  }
}
```

### analyzer.md

**Input changes:**
- Analyzes comparison results post-hoc
- Generates improvement suggestions

**Output format:**
```json
{
  "comparison_summary": { ... },
  "winner_strengths": [ ... ],
  "loser_weaknesses": [ ... ],
  "improvement_suggestions": [ ... ]
}
```

### test-coordinator.md (New)

Orchestrates the complete testing workflow:
1. Prepares eval structure
2. Spawns execution subagents
3. Spawns grader subagents
4. Collects results
5. Generates report

---

## File Structures

### evals/evals.json

```json
{
  "skill_name": "design-system",
  "evals": [
    {
      "id": 1,
      "eval_name": "saas-dashboard",
      "prompt": "I'm building a B2B SaaS dashboard...",
      "expected_output": "Agent should establish...",
      "expectations": [
        "Design tokens include full color palettes (50-900)",
        "Core components defined (Button, Card, Input)",
        "Domain components created (StatCard, KanbanBoard)",
        "Example dashboard page created",
        "guidelines.md created",
        "accessibility.md created with WCAG 2.1 AA"
      ],
      "files": []
    }
  ]
}
```

### eval-outputs/comparison-groupN/manifest.json

```json
{
  "skill_name": "design-system",
  "skill_path": "../design-system",
  "evals_run": 1,
  "timestamp": "2026-03-18T10:00:00",
  "output_base_dir": "../design-system/eval-outputs/comparison-group1",
  "comparison_type": "with_vs_without_skill",
  "results": [
    {
      "eval_id": 1,
      "eval_name": "saas-dashboard",
      "status": "pending",
      "output_dir": "../design-system/eval-outputs/comparison-group1/eval-1-saas-dashboard",
      "with_skill_dir": ".../with_skill",
      "without_skill_dir": ".../without_skill"
    }
  ]
}
```

### eval-outputs/comparison-groupN/eval-1-{name}/eval_metadata.json

```json
{
  "eval_id": 1,
  "eval_name": "saas-dashboard",
  "prompt": "...",
  "expectations": ["...", "..."],
  "skill_path": "../design-system",
  "timestamp": "2026-03-18T10:00:00",
  "status": "pending",
  "comparison_type": "with_vs_without_skill"
}
```

### eval-outputs/comparison-groupN/eval-1-{name}/comparison.json

```json
{
  "eval_name": "saas-dashboard",
  "winner": "A",
  "winner_type": "with_skill",
  "reasoning": "Output A provides granular design tokens...",
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

---

## Usage Example

```bash
# Step 1: Validate skill
python3 skill-creator/scripts/quick_validate.py design-system

# Step 2: Run comparison tests (REQUIRED)
python3 skill-creator/scripts/run_comparison.py \
  --eval-set design-system/evals/eval_group1.json \
  --skill-path design-system \
  --output-dir design-system/eval-outputs/comparison-group1

# Step 3: Review manifest.json
cat design-system/eval-outputs/comparison-group1/manifest.json

# Step 4: Spawn subagents (see manifest for details)
# Spawn TWO subagents per eval:
#   - One WITH skill
#   - One WITHOUT skill
# Then spawn comparator subagent

# Step 5: Review comparison results
cat design-system/eval-outputs/comparison-group1/eval-1-*/comparison.json

# Step 6: Clean up (after reviewing)
python3 skill-creator/scripts/run_comparison.py \
  --output-dir design-system/eval-outputs/comparison-group1 --cleanup
```

---

## Key Differences from Claude Code

| Aspect | Claude Code | Qwen Code |
|--------|-------------|-----------|
| Skill triggering | Auto by description | Explicit invocation |
| Subprocess execution | `claude -p` | Task tool |
| Skill registration | `.claude/commands/` | Direct file reference |
| Stream parsing | JSON stream events | Direct task output |
| Authentication | Required for CLI | Uses session auth |

---

## Migration Notes

To migrate a skill from Claude Code to Qwen:

1. **Update evals/evals.json** - Add explicit expectations
2. **Modify test scripts** - Use Task tool instead of `claude -p`
3. **Update agent prompts** - Receive paths via task prompt
4. **Remove CLI dependencies** - No subprocess calls
5. **Add explicit skill invocation** - Tasks must specify skill path

---

## Troubleshooting

**Skill not invoked:**
- Ensure task prompt explicitly says "using the {skill_name} skill"
- Verify skill path is correct
- Check SKILL.md frontmatter has name and description

**Grading fails:**
- Verify transcript.md exists in output directory
- Check expectations are verifiable from outputs
- Ensure grading.json schema matches specification

**Comparison inconclusive:**
- Ensure both outputs are complete
- Verify comparator has full context (prompt + expectations)
- Check rubric is task-appropriate
