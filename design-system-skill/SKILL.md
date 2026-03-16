---
name: frontend-design-system
description: Defines a reusable, context-aware frontend design system before implementation. Use this skill whenever the user mentions UI architecture, design tokens, component libraries, or visual branding rules. Trigger it early in the project life cycle, even if the user only mentions "styling" or "web aesthetic," to ensure consistent layout and structural foundations from the start.
license: Complete terms in LICENSE.txt
---

# Frontend Design System

## When to use this skill

Use this skill before building any page, screen, or feature UI when the project does not yet have a clear design system.

Use it when you want to define the visual and structural rules of the frontend first, so later page implementation stays consistent, faster, and easier to review.

Use it when product context matters, especially app subject, target audience, mission, positioning, and brand tone, because those inputs should shape the system instead of letting random component choices shape the product.

Use it when a project is starting to accumulate one-off components, inconsistent spacing, mismatched colors, duplicated variants, or vibe-coded UI decisions with no reusable logic behind them.

## Do not use this skill when

Do not use this skill to implement pages, routes, views, or feature flows directly. This skill defines the system; another skill should build pages from it.

Do not use this skill if a solid design system already exists and the real task is just to add one small component that clearly fits existing tokens, primitives, and usage rules.

Do not use this skill for brand strategy, logo exploration, or open-ended visual identity work with no product direction at all. It can reflect brand tone, but it is not a substitute for product positioning work.

Do not use this skill if the user only wants quick mockup code without caring about maintainability. In that case, say clearly that skipping the system will create future inconsistency and debt.

## Inputs and prerequisites

Collect or infer these inputs before doing the work:

- App subject: what the product does in plain language.
- Audience: who it serves, how technical they are, and what they care about.
- Mission: what outcome the product wants to create.
- Brand tone: examples include calm, premium, playful, trustworthy, technical, blunt, minimalist.
- Main interface types: dashboard, marketing site, internal tool, mobile app, content app, SaaS product, marketplace, and so on.
- Accessibility expectations: minimum contrast, keyboard use, reduced motion, screen reader support, touch targets.
- Platform constraints: web, mobile web, native wrapper, desktop app shell, embedded app, kiosk, and so on.
- Existing constraints if any: current brand colors, legal requirements, known product patterns, legacy components, or customer expectations.

If critical product context is missing, do not invent fake certainty. State assumptions explicitly and build a conservative system that is easy to adapt.

## Core responsibilities

This skill must define the design system before page implementation.

This skill must translate product context into reusable system rules, not just visual preferences.

This skill must define:

- Design principles tied to product context.
- Tokens, including color, typography, spacing, radius, elevation, border, motion, and interaction states.
- Primitives, meaning low-level reusable building blocks.
- Layout patterns and container rules.
- Component hierarchy from foundations to composed patterns.
- Usage rules so different contributors make similar decisions.
- A registry checklist so every component added later follows the same contract.

This skill must actively prevent one-off vibe-coded components by requiring every proposed component to justify its place in the system.

This skill must mandate an interview phase before any design work begins. The assistant MUST NOT generate tokens, primitives, or layouts until the user has provided enough product and technical context.

This skill must stop before page implementation and hand off page construction to another skill.

## Step-by-step workflow

1. The Interview Phase.
   You MUST start by interviewing the user to gather context. Do not make assumptions. Ask these specific questions:
   - What is the subject and main mission of the app?
   - What is the target audience (technical level, role)?
   - What is the technical stack (if not already defined)?
   - What is the desired brand tone or theme (e.g., minimalist, playful, industrial, corporate)?
   - Can you provide a short summary of the core user journey or main job to be done?

   After asking these questions, you MUST STOP and wait for the user to respond before proceeding to the next step.

2. Capture product context.
   Summarize the answers from the interview. If anything is still missing, state assumptions clearly and ask for final confirmation.

3. Derive design goals from product reality.
   Define 4 to 7 system goals such as clarity, trust, speed, density, warmth, focus, or operational efficiency. Every later decision should connect back to these goals.

4. Define visual foundations.
   Create design tokens for:
   - Color roles, not just raw colors, such as background, surface, text, muted text, border, accent, success, warning, danger.
   - Typography scale and text roles, such as display, title, body, label, caption, mono if needed.
   - Spacing scale.
   - Radius scale.
   - Border widths.
   - Shadow or elevation scale if relevant.
   - Motion rules, including duration and when motion should be reduced.
   - Opacity and state treatment if needed.

5. Define semantic rules for tokens.
   Explain where each token category is allowed, where it is not allowed, and how to avoid ad hoc usage. Example: “accent color is for actions and focus, not for decorative random highlights.”

6. Define primitives.
   List the smallest reusable building blocks. Examples:
   - Text
   - Heading
   - Stack
   - Inline
   - Grid
   - Box
   - Surface
   - Divider
   - Icon container
   - Interactive base
   - Field base

   For each primitive, define purpose, allowed props or configuration ideas, and what should never be customized casually.

7. Define layout system.
   Establish page width strategy, responsive breakpoints if needed, vertical rhythm, section spacing, sidebar behavior, panel behavior, card grouping, and dense versus relaxed layouts.

8. Define component hierarchy.
   Organize components in layers such as:
   - Tokens
   - Primitives
   - Composed controls
   - Composite sections
   - Domain-specific patterns

   Make clear that higher-level components must be built from lower-level layers instead of bypassing them.

9. Define component families.
   Create the main reusable component groups the product likely needs, based on context. Typical examples:
   - Navigation
   - Buttons and actions
   - Inputs and forms
   - Feedback and status
   - Overlays
   - Data display
   - Content presentation
   - Lists and tables
   - Empty, loading, and error states

   For each family, define purpose, core variants, behavior expectations, and constraints.

10. Define usage rules.
   Add rules that prevent entropy. Examples:
   - No custom spacing values outside the spacing scale.
   - No new color usage without a semantic token role.
   - No component variant unless it supports a repeated use case.
   - No page-specific styling inside shared components.
   - No duplicate component with slightly different naming.
   - Composition first, new component second.

11. Define a registry checklist.
   Create a checklist every new component must satisfy before entering the system.

12. Prepare handoff.
   End by stating that page implementation should now be handled by another skill using the design system as the source of truth.

## Examples

**Example 1: SaaS Dashboard (Data-heavy)**

Input Product Context:
- App Subject: Cloud infrastructure monitoring dashboard.
- Audience: DevOps engineers and SREs.
- Brand Tone: Technical, precise, high-density, trustworthy.

Output Strategy:
- Small radius, thin borders.
- Cool palette (blues/grays) with high-contrast status colors.
- Dense spacing scale, monospaced typography for metrics.

**Example 2: Children's Educational Platform (Playful)**

Input Product Context:
- App Subject: Interactive reading and math games for ages 5-10.
- Audience: Young children and parents.
- Brand Tone: Playful, warm, energetic, accessible.

Output Strategy:
- Large radius (pill-shaped), chunky borders.
- Vibrant primary colors, warm accents.
- Relaxed spacing scale, large rounded typography.

## Required output format

Output a single structured design-system specification in Markdown.

Use this exact section structure in the final deliverable:

1. Product Context
2. Design Goals
3. Design Principles
4. Tokens
5. Primitives
6. Layout System
7. Component Hierarchy
8. Component Families
9. Usage Rules
10. Component Registry Checklist
11. Assumptions and Open Questions
12. Handoff to Page Implementation

Inside “Tokens”, always include at least:

- Color roles
- Typography roles
- Spacing scale
- Radius scale
- Border treatment
- Elevation or shadow policy
- Motion policy
- State behavior

Inside “Component Registry Checklist”, each component entry must include:

- Name
- Purpose
- Layer in hierarchy
- Depends on which primitives
- Variants
- States
- Accessibility requirements
- Responsive behavior
- Usage rules
- Anti-patterns
- Whether it is truly reusable
- Whether an existing component can be extended instead

Do not output implementation code unless explicitly requested elsewhere. This skill defines the system contract, not the framework code.

## Best practices and heuristics

Start from product meaning, not Dribbble-looking decoration. A good system should feel native to the app’s mission and audience.

Prefer semantic tokens over raw values. “surface-muted” is better than “gray-100” as the main decision surface because it explains intent.

Keep the primitive layer small and boring. If primitives are unstable, everything above them becomes expensive to change.

Create as few component variants as possible. Variants should solve recurring needs, not personal taste.

Use composition before invention. If a new UI need can be built from existing primitives and patterns, do that instead of adding another special component.

Name things by role, not by page. “EmptyState” is reusable; “BillingEmptyCard” is usually a smell unless it represents a real domain pattern.

Design for states early. Loading, empty, error, disabled, focus, hover, selected, and invalid states should not be afterthoughts.

Make accessibility a default rule, not a cleanup step. Color contrast, keyboard behavior, visible focus, readable density, and reduced motion should be part of the system definition.

Be honest about domain-specific components. Some components belong to the product domain, but they still need rules and registry entries instead of being treated like exceptions.

## Things to avoid

Avoid defining components directly from page screenshots or isolated inspiration. That usually creates brittle one-offs.

Avoid raw hardcoded values spread everywhere, especially colors, spacing, font sizes, shadows, and border radius.

Avoid multiple components that differ only slightly in padding, border, or naming. That is fake reuse and real maintenance cost.

Avoid adding “just this one custom version” for a page unless it is promoted into a justified reusable pattern.

Avoid giant component APIs with too many flags. That usually means the component has mixed responsibilities and should be split.

Avoid mixing brand expression with functional meaning. For example, do not use decorative color choices to communicate warning or success unless the semantic role is clear.

Avoid starting implementation before the system contract is written down. Otherwise the first pages become the accidental design system.

## Edge cases

If the product has weak or missing brand direction, build a neutral, high-clarity system and mark the tone-dependent parts as assumptions.

If the app serves multiple audiences, define shared foundations first, then note where density, language, or workflow patterns may branch by audience type.

If the product already has messy legacy UI, do not mirror the mess as if it were a system. Extract stable patterns, mark debt explicitly, and define migration-safe rules.

If the interface is highly domain-specific, allow domain patterns in the hierarchy, but require them to inherit tokens, primitives, and layout rules like everything else.

If a stakeholder requests a one-off component, require one of these outcomes: it becomes a reusable pattern with rules, it is composed from existing parts, or it is rejected as design debt.

If implementation pressure is high, keep the first version of the system compact. A small consistent system is better than a big fake system nobody follows.

## Interaction and Communication

Be helpful, curious, and collaborative. Treat the design system as a living contract between you and the user.

- **Interviewing**: When asking questions, explain *why* you are asking (e.g., "Knowing your stack helps me define appropriate motion and border tokens").
- **Iterating**: If the user provides vague answers, offer examples of what you're looking for.
- **Confirmation**: Always confirm you have understood the context before moving from the interview to the design goals.
- **Brevity**: Keep your questions concise. Do not overwhelm the user with too many questions at once; 4-6 high-impact questions are usually enough.
