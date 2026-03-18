# SkillEngine

A hobby project for experimenting with AI agent skills and testing workflows.

---

## What Is This?

SkillEngine is a personal sandbox for exploring how AI agents can be guided to perform specialized tasks through structured instructions (called "skills").

Each skill is a folder containing:
- `SKILL.md` - Instructions the agent follows
- `references/` - Supporting documentation
- `evals/` - Test cases for validation
- `scripts/` - Helper utilities

---

## Current Skills

| Skill | Purpose |
|-------|---------|
| [`design-system/`](./design-system) | Build comprehensive design systems with tokens, components, and documentation |
| [`skill-creator/`](./skill-creator) | Create, test, and improve other skills |

---

## Testing Workflow

The project includes a complete testing framework:

1. **Static Tests** - Validate skill structure (< 1 second)
2. **Trigger Tests** - Verify skill activates correctly (29 patterns)
3. **Comparison Tests** - Measure skill value vs baseline (with/without skill)

Run tests:
```bash
# Static tests (no subagents)
python3 skill-creator/scripts/static_test_suite.py <skill-path>

# Comparison tests (measures skill added value)
python3 skill-creator/scripts/run_comparison.py \
  --eval-set design-system/evals/eval_group1.json \
  --skill-path design-system \
  --output-dir design-system/eval-outputs/comparison-group1
```

---

## Project Status

**This is a hobby project.** It's a space for learning and experimentation, not a production system.

- 🧪 Experimental - Testing new patterns and approaches
- 📚 Learning-focused - Documenting what works and what doesn't
- 🔧 Evolving - Structure and workflows may change frequently

---

## Documentation

- [`TESTING-WORKFLOW.md`](./TESTING-WORKFLOW.md) - Complete testing guide
- [`design-system/SKILL.md`](./design-system/SKILL.md) - Design system skill
- [`skill-creator/SKILL.md`](./skill-creator/SKILL.md) - Skill creation workflow

---

## License

MIT License - See individual skill folders for specific licenses.

---

*Last updated: March 2026*
