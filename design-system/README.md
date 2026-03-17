# Design System Skill

A skill for building comprehensive design systems with consistent components, tokens, and patterns for web applications.

## Overview

This skill ensures agents establish a design system **before** jumping into coding features. It produces:

- **Granular design tokens** (full color palettes 50-900, typography scales, spacing systems)
- **Core components** (Button, Card, Input, Layout, Navigation, Typography, Feedback, Data Display)
- **Domain-specific components** (tailored to the app's use case)
- **Example pages** showing components in realistic contexts
- **Documentation** (guidelines.md + accessibility.md with WCAG 2.1 AA)

---

## Test Results

### Evaluation Summary

| Eval | Domain | Stack | With Skill | Without Skill |
|------|--------|-------|------------|---------------|
| 1 | SaaS Dashboard | Next.js + Tailwind + shadcn | ✅ Comprehensive | ✅ Comprehensive |
| 2 | Fitness App | React + styled-components | ✅ Comprehensive | ✅ Comprehensive |
| 3 | E-commerce | Vue 3 + Tailwind | ✅ Comprehensive | ✅ Comprehensive |

---

## Detailed Results

### Eval 1: SaaS Dashboard (Next.js + Tailwind + shadcn)

**Prompt:** *"I'm building a B2B SaaS dashboard for project management. It's a Next.js app using Tailwind CSS and I'd like to use shadcn/ui components as a base..."*

| Criteria | With Skill | Without Skill | Winner |
|----------|------------|---------------|--------|
| Granular tokens | ✅ tokens.ts with 50-900 shades | ✅ Separate JSON files | Tie |
| Domain components | ✅ TaskCard, KanbanBoard, StatCard | ✅ stat-card, kanban | Tie |
| Example pages | 2 pages | 5 pages | Without |
| guidelines.md | ✅ | ✅ | Tie |
| accessibility.md | ✅ WCAG 2.1 AA | ❌ (merged into other docs) | **With** |
| Organization | ui/, layout/, domain/ | components/, config/, examples/ | With (clearer) |

**Output Locations:**
- With Skill: `design-system-workspace/iteration-2/eval-1-saas-dashboard/with_skill/outputs/`
- Without Skill: `design-system-workspace/iteration-2/eval-1-saas-dashboard/without_skill/outputs/`

---

### Eval 2: Fitness App (React + styled-components)

**Prompt:** *"I need a consumer-facing mobile app (react native web). We're using React with styled-components. The app is a fitness/wellness tracker targeting millennials..."*

| Criteria | With Skill | Without Skill | Winner |
|----------|------------|---------------|--------|
| Granular tokens | ✅ colors.ts (energetic coral) | ✅ JSON tokens | Tie |
| Domain components | ✅ WorkoutCard, ExerciseList, ProgressChart, SocialFeed | ✅ workout-card, stat-card, activity-feed | With (more comprehensive) |
| Example pages | 5 pages | 1 page | **With** |
| guidelines.md | ✅ | ✅ | Tie |
| accessibility.md | ✅ WCAG 2.1 AA | ✅ ACCESSIBILITY.md | Tie |
| Mobile optimization | ✅ BottomNav, 44px targets | ✅ BottomNav, 44px targets | Tie |

**Output Locations:**
- With Skill: `design-system-workspace/iteration-2/eval-2-fitness-app/with_skill/outputs/`
- Without Skill: `design-system-workspace/iteration-2/eval-2-fitness-app/without_skill/outputs/`

---

### Eval 3: E-commerce (Vue 3 + Tailwind)

**Prompt:** *"Building an e-commerce storefront for a luxury skincare brand. Using Vue 3 with Tailwind CSS. The design should feel premium, minimalist, and elegant..."*

| Criteria | With Skill | Without Skill | Winner |
|----------|------------|---------------|--------|
| Granular tokens | ✅ JSON + TS (rose gold palette) | ✅ design-tokens.json | Tie |
| Domain components | ✅ ProductCard, ProductGallery, ShoppingCart, CheckoutStep, ReviewCard, PriceTag | ✅ ProductCard, ProductGrid, CartSidebar | **With** (more comprehensive) |
| Example pages | 5 pages | 6 pages | Without |
| guidelines.md | ✅ | ✅ (DESIGN_SYSTEM.md) | Tie |
| accessibility.md | ✅ WCAG 2.1 AA | ❌ (no dedicated doc) | **With** |
| Dark mode | ✅ | ✅ | Tie |

**Output Locations:**
- With Skill: `design-system-workspace/iteration-2/eval-3-ecommerce/with_skill/outputs/`
- Without Skill: `design-system-workspace/iteration-2/eval-3-ecommerce/without_skill/outputs/`

---

## Summary

| Metric | With Skill | Without Skill |
|--------|------------|---------------|
| **accessibility.md** | 3/3 ✅ | 1/3 ✅ |
| **Domain components** | Strong in all 3 | Strong in all 3 |
| **Example pages** | 12 total | 12 total |
| **Token granularity** | Strong (TS format) | Strong (JSON format) |
| **File organization** | Consistent (ui/, domain/, docs/) | Variable |

---

## Key Findings

### What the Skill Does Better

1. **Consistently produces accessibility.md** — This is the biggest differentiator (3/3 vs 1/3)
2. **More organized file structure** — Consistent ui/, domain/, layout/, docs/ folders
3. **Domain component comprehensiveness** — Slightly more thorough (e.g., 6 e-commerce components vs 3)

### What the Baseline Does Equally Well or Better

1. **Example pages** — Baseline sometimes produces MORE pages (12 total vs 12 total — tie)
2. **Token granularity** — Both produce detailed tokens, just different formats
3. **Domain awareness** — Both create domain-specific components without the skill

---

## Conclusion

**The skill is working but the improvements are incremental, not dramatic.** The main consistent advantage is the dedicated `accessibility.md` file.

### What Works

- ✅ Prevents jumping straight to coding (both versions establish design systems)
- ✅ Produces domain-specific components (both do this)
- ✅ Creates granular tokens (both do this)
- ✅ Consistent accessibility documentation (skill wins here)
- ✅ Organized file structure (skill is more consistent)

### Areas for Improvement

1. **Interview phase** — The skill's "design system first" principle isn't clearly differentiating results. None of the outputs show evidence of the agent asking clarifying questions first.
2. **Example pages consistency** — The count varies; skill should specify a minimum.
3. **Pushiness** — Consider making the skill more assertive about the interview process and output requirements.

---

## File Structure (With Skill)

```
design-system/
├── SKILL.md                 # Skill definition
├── README.md                # This file
├── evals/
│   └── evals.json           # Test cases
├── references/
│   ├── tokens.md            # Token reference
│   ├── component-patterns.md # Component patterns
│   └── schemas.md           # JSON schemas
├── scripts/
│   ├── check_consistency.py
│   ├── generate_css.py
│   └── README.md
└── assets/                  # (empty - for future assets)
```

### Generated Output Structure

```
<project-root>/
├── lib/                     # Design tokens (TS/JSON)
├── components/
│   ├── ui/                  # Primitive components
│   ├── layout/              # Layout components
│   └── domain/              # Domain-specific components
├── examples/                # Example pages
├── docs/
│   ├── guidelines.md        # Usage documentation
│   └── accessibility.md     # WCAG 2.1 AA guidelines
├── styles/
├── config/
└── package.json
```

---

## Usage

Trigger this skill when:
- User mentions building a new app/project
- User wants to establish UI consistency
- User mentions design systems, component libraries, or design tokens
- Even casual mentions like "make my app look consistent"

The skill will interview the user, then produce a complete design system tailored to their stack and domain.
