# Design System Skill

A skill for building comprehensive design systems with consistent components,
tokens, and patterns for web applications.

## Overview

This skill ensures agents establish a design system **before** jumping into
coding features. It produces:

- **Granular design tokens** (full color palettes 50-900, typography scales,
  spacing systems)
- **Core components** (Button, Card, Input, Layout, Navigation, Typography,
  Feedback, Data Display)
- **Domain-specific components** (tailored to the app's use case)
- **Example pages** showing components in realistic contexts
- **Documentation** (guidelines.md + accessibility.md with WCAG 2.1 AA)

---

## Usage

Trigger this skill when:

- User mentions building a new app/project
- User wants to establish UI consistency
- User mentions design systems, component libraries, or design tokens
- Even casual mentions like "make my app look consistent"

The skill will interview the user, then produce a complete design system
tailored to their stack and domain.

---

## Workflow

1. **Interview** — Ask 7 required questions (app concept, users, tone, stack,
   screens, accessibility, dark mode)
2. **Tokens** — Create granular design tokens (colors, typography, spacing,
   borders, shadows, motion)
3. **Components** — Design core + domain-specific components
4. **Implementation** — Generate code matching user's tech stack
5. **Examples** — Create showcase page + 2 context pages
6. **Documentation** — Write guidelines.md and accessibility.md

See `SKILL.md` for the complete workflow.

---

## File Structure

```
design-system/
├── SKILL.md                 # Skill definition and workflow
├── README.md                # This file
├── evals/
│   └── evals.json           # Test cases for validation
├── references/
│   ├── tokens.md            # Token reference (colors, typography, spacing)
│   ├── component-patterns.md # Component patterns and specs
│   ├── domain-components-library.md # Domain-specific component ideas
│   ├── example-showcase-page.md # How to build showcase pages
│   ├── implementation-guide.md # Stack-agnostic implementation patterns
│   ├── interview-questionnaire.md # Interview guidance
│   ├── quality-checklist.md # Delivery checklist
│   ├── accessibility-checklist.md # WCAG 2.1 AA quick reference
│   └── schemas.md           # JSON schemas for tokens/components
├── scripts/
│   ├── check_consistency.py # CSS/token compliance checker
│   ├── generate_css.py      # CSS variable generator
│   └── README.md            # Script documentation
└── assets/                  # Example outputs (coming soon)
```

---

## Key Principles

**Interview First (NON-NEGOTIABLE)**

Always complete the full interview before writing any code. Ask all 7 required
questions and wait for complete answers.

**Design System First**

Never jump to coding features or pages without establishing the system. A
generic UI is the direct result of skipping design system work.

**Domain Specificity**

Extract what the app does and create components for those use cases. Generic
buttons and cards are not enough.

**Token Granularity**

Detailed palettes (50-900 shades) not single colors. Complete scales not just a
few values.

**Examples in Context**

Show components working together. Give developers a starting point. Prove the
system is coherent.

**Accessibility First-Class**

Dedicated documentation, not inline notes. WCAG 2.1 AA compliance.

---

## Output Checklist

Before considering the task complete, ensure you've delivered:

- [ ] **Interview completed**: All 7 required questions answered by the user
- [ ] **Granular tokens**: Full color palettes (50-900), typography scale,
      spacing scale, borders, shadows, motion
- [ ] **Core components**: Actions, Inputs, Layout, Cards, Navigation,
      Typography, Feedback, Data
- [ ] **Domain-specific components**: Components tailored to the app's use cases
- [ ] **Tech stack alignment**: Code matches user's framework, styling
      approach, libraries
- [ ] **Showcase page**: Complete design system hierarchy for review
- [ ] **Context pages**: Minimum 2 pages showing components in realistic
      contexts
- [ ] **guidelines.md**: Usage documentation with principles, tokens,
      components, best practices
- [ ] **accessibility.md**: Dedicated WCAG 2.1 AA guidelines
- [ ] **File structure**: Organized, scalable, ready for integration

---

## Reference Files

| File | Purpose |
|------|---------|
| `tokens.md` | Token structure: colors, typography, spacing, borders, shadows |
| `component-patterns.md` | Component specs: states, variants, sizes, accessibility |
| `domain-components-library.md` | Domain-specific component ideas (8 domains) |
| `example-showcase-page.md` | How to build a comprehensive showcase page |
| `implementation-guide.md` | Stack-agnostic implementation patterns |
| `interview-questionnaire.md` | How to conduct the design system interview |
| `quality-checklist.md` | Quick sanity check before delivery |
| `accessibility-checklist.md` | WCAG 2.1 AA quick reference |
| `schemas.md` | JSON schemas for tokens and components |

---

## Scripts

| Script | Purpose |
|--------|---------|
| `check_consistency.py` | Validate CSS/SCSS against design tokens |
| `generate_css.py` | Generate CSS custom properties from tokens.json |

See `scripts/README.md` for usage.

---

## Evaluation

Test cases are defined in `evals/evals.json`:

1. **SaaS Dashboard** — Next.js + Tailwind + shadcn/ui
2. **Fitness App** — React + styled-components (mobile-first)
3. **E-commerce** — Vue 3 + Tailwind (luxury/minimalist)

Each eval tests the skill's ability to:

- Conduct a proper interview
- Create granular, domain-appropriate tokens
- Build domain-specific components
- Produce coherent example pages
- Generate proper documentation
