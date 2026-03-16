<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# < AI SKILLS REPORT >

You are an elite specification writer for AI coding skills.

Create a complete package of 10 production-grade skills for a full-stack AI coding agent.

CRITICAL DELIVERY RULES

- Output exactly 10 separate Markdown file payloads in the response.
- Each payload must represent one complete standalone Markdown file.
- Do not merge multiple skills into one file payload.
- Do not output JSON.
- Do not output commentary, explanations, notes, summaries, or apologies.
- Do not wrap the full response in one giant code block.
- Do not rename any skill.
- Do not reorder the skills.
- If you cannot complete all 10 file payloads in one response, output exactly: INCOMPLETE

EXACT OUTPUT FILES

Report exactly these 10 Markdown files in exactly this order:

1. codebase-understanding.md
2. architecture-planning.md
3. frontend-ui-ux.md
4. backend-api-data.md
5. testing-qa.md
6. devops-cicd.md
7. security-compliance.md
8. integrations-services.md
9. debugging-performance.md
10. docs-knowledge.md

OUTPUT FORMAT

Use this exact pattern for each file:

=== FILE: <filename> ===
<full markdown content>

Rules:

- Output exactly 10 file blocks.
- Each block must contain one complete Markdown file only.
- Do not add any text before the first file block.
- Do not add any text between file blocks except the next file delimiter.
- Do not add any text after the tenth file block.
- Do not use triple backticks anywhere in the output.

FILE-TO-SKILL MAPPING

Each file represents one skill.

Inside each file, the frontmatter `name` field must exactly match the filename without `.md`.

Examples:

- codebase-understanding.md -> name: codebase-understanding
- architecture-planning.md -> name: architecture-planning

GLOBAL OBJECTIVE

Write 10 highly usable, production-grade AI coding skills for professional full-stack development.

Across the entire set, repeatedly and concretely reinforce these standards wherever relevant:

- frontend design quality
- UI/UX quality
- accessibility
- responsive design
- mobile-first thinking
- design systems
- interaction states
- polished product behavior
- performance-aware web engineering
- cohesion between product design, frontend, backend, testing, security, operations, integrations, debugging, and documentation

This emphasis must appear across multiple skills, not only the frontend one.

Examples of how this should show up:

- backend guidance must preserve API contracts that enable clean loading, empty, error, success, and partial-data UI states
- testing guidance must protect core user journeys, accessibility behavior, and responsive behavior
- debugging guidance must inspect rendering, hydration, layout shifts, responsiveness, interaction regressions, and performance bottlenecks
- documentation guidance must explain user flows, component usage, decisions, assumptions, and design rationale
- security guidance must preserve safe auth and session behavior without creating unnecessary user friction

REQUIRED FORMAT INSIDE EACH FILE

Each file must begin with exactly this YAML structure:

---
name: <skill-name>
description: <1 to 3 sentences>
license: Complete terms in LICENSE.txt
---

Rules:

- `name` must exactly match the target filename without `.md`
- use lowercase kebab-case
- letters and hyphens only
- `description` must clearly explain what the skill does, when to use it, likely trigger phrases, task examples, or repository signals
- the description must be specific enough for automatic routing

REQUIRED H2 SECTIONS IN EVERY FILE

Every file must contain all of these sections:

## Overview

## When to Use This Skill

## Ownership and Boundaries

## Core Responsibilities

## Step-by-Step Workflow

## Best Practices and Heuristics

## Things to Avoid

## Quality Bar

Add these sections when materially useful:

## Collaboration With Other Skills

## Edge Cases

SECTION REQUIREMENTS

For every skill:

1. Overview

- 1 short paragraph
- state the skill's purpose in practical terms
- state what it owns
- state what success looks like

2. When to Use This Skill

- 8 to 12 bullets
- include direct user requests, repository context, and workflow signals
- include signals like CI failures, missing UI states, broken layouts, flaky tests, API gaps, logs, traces, design drift, or documentation drift where relevant

3. Ownership and Boundaries

- 6 to 10 bullets
- explicitly define:
    - what this skill owns
    - what it does not own
    - when to preserve existing project patterns
    - when to modernize carefully
    - when to ask for clarification
    - when to stop and ask for approval before risky, destructive, or breaking changes

4. Core Responsibilities

- 8 to 12 bullets
- be concrete and operational

5. Step-by-Step Workflow

- 6 to 10 numbered steps
- written as execution instructions for an expert AI coding agent
- include inspection, planning, implementation, validation, and handoff behavior
- require the agent to propose a plan before risky changes

6. Best Practices and Heuristics

- 10 to 14 bullets
- be opinionated, modern, and production-grade
- include UX, accessibility, responsive behavior, maintainability, and performance thinking where relevant

7. Things to Avoid

- 8 to 12 bullets
- include anti-patterns, lazy shortcuts, and unacceptable behaviors

8. Quality Bar

- 6 to 10 bullets
- define what done well means in observable terms

9. Collaboration With Other Skills

- add when helpful
- explain handoffs, dependencies, coordination, and escalation paths

10. Edge Cases

- add when helpful
- cover realistic unusual conditions and how to handle them

WRITING STYLE

Write as instructions for an expert AI coding agent.

Use:

- direct, imperative language
- operational guidance
- strong opinions
- realistic engineering tradeoffs
- repository-aware execution behavior
- production-grade standards

Do not use:

- vague advice
- soft suggestions
- motivational filler
- classroom teaching tone
- abstract principles without execution detail

Assume the AI agent can:

- inspect the codebase
- compare patterns across the repository
- work iteratively
- propose a plan before risky changes
- reason about implementation tradeoffs
- validate behavior against repository conventions and product expectations

MODERN PRODUCT AND UI EXPECTATIONS

Embed these repeatedly and concretely across the relevant skills:

1. Accessibility by default

- semantic markup
- keyboard navigation
- visible focus states
- labels and descriptions
- contrast awareness
- reduced motion support
- screen reader compatibility
- usable validation and error messaging

2. Design system discipline

- prefer existing tokens, primitives, spacing scales, type scales, and component APIs
- avoid one-off styling
- if no design system exists, create reusable conventions instead of isolated implementations

3. Responsive and mobile-first execution

- prioritize small screens first
- protect key flows on mobile
- respect touch target sizing
- handle long and variable content gracefully
- avoid desktop-only assumptions

4. UX completeness

- loading states
- empty states
- error states
- success feedback
- async progress feedback
- predictable navigation
- sensible defaults
- low-friction forms

5. Performance-aware implementation

- avoid unnecessary client-side complexity
- protect bundle size
- reduce over-fetching
- minimize unnecessary rerenders
- preserve SSR and hydration assumptions when relevant
- prefer progressive enhancement where appropriate

6. Product-quality implementation

- reuse existing components before creating new ones
- keep state transitions explicit
- preserve user trust
- avoid inaccessible custom controls
- reject flashy but low-value complexity

SKILL-SPECIFIC INTENT

The 10 skills should feel distinct and complementary:

- codebase-understanding: repository discovery, conventions, dependency mapping, architectural reading, hotspot identification
- architecture-planning: solution design, change scoping, interfaces, migration strategy, risk planning
- frontend-ui-ux: UI implementation, accessibility, responsive behavior, interaction quality, design system usage
- backend-api-data: API contracts, data modeling, validation, persistence, background jobs, frontend-compatible response design
- testing-qa: automated test strategy, user journey coverage, regression protection, reliability, accessibility-sensitive testing
- devops-cicd: build pipelines, environments, release confidence, observability hooks, safe automation
- security-compliance: auth, authorization, secrets, safe defaults, data protection, abuse prevention, usability-preserving safeguards
- integrations-services: third-party APIs, retries, idempotency, sync behavior, contract isolation, failure handling
- debugging-performance: root-cause analysis, rendering issues, performance bottlenecks, hydration issues, logs, profiling, reproducibility
- docs-knowledge: architecture docs, runbooks, onboarding, decision records, component usage, user flows, rationale, maintenance guidance

QUALITY REQUIREMENTS

- Every skill must be specific enough that an AI agent could actually use it
- Every skill must be materially different from the others
- Avoid copy-paste bullets with only renamed nouns
- Preserve existing repository patterns unless there is a clear reason to improve them
- Recommend modernization only when the current pattern is weak, inconsistent, unsafe, or blocking product quality
- Require approval before breaking public APIs, deleting code, changing schemas with migration risk, replacing shared UI primitives, changing auth flows, or making infrastructure-level changes with deployment risk
- Ask for clarification when product intent, UX expectations, data semantics, or migration constraints are ambiguous

PER-FILE COMPLETENESS CHECK

Before writing each file, internally verify:

- filename matches the skill name
- frontmatter is present
- all required H2 sections are present
- ownership, boundaries, approval thresholds, and clarification triggers are explicit
- modern UI/UX/accessibility/responsive/performance thinking is embedded where relevant

FINAL EXECUTION RULE

Output the 10 file blocks only.
Do not explain what you are doing.
Do not emit placeholders.
Do not stop after fewer than 10 files.

=== FILE: codebase-understanding.md
***
name: codebase-understanding
description: Defines how the agent analyzes an existing repository, discovers conventions, maps dependencies, and identifies hotspots before making changes. Triggered by initial onboarding to a repo, unclear structure, or when planning significant frontend, backend, UX, or infrastructure work.
license: Complete terms in LICENSE.txt
***

## Overview

This skill is responsible for deeply understanding the existing codebase, its architecture, patterns, and hotspots before any significant implementation work. It owns repository discovery, mapping of modules and flows, and surfacing constraints that affect frontend, backend, UX, accessibility, performance, and operations. Success means the agent can navigate the repo confidently, respect existing patterns, and propose changes that fit naturally into the system.

## When to Use This Skill

- When first attaching to a new repository or monorepo.
- When the user asks, "Can you understand this codebase?" or "Give me an overview of this project."
- Before major refactors, migrations, or redesigns (frontend, backend, or infrastructure).
- When planning new features that span UI, APIs, data models, and background jobs.
- When CI failures, flaky tests, or production issues suggest systemic architectural problems.
- When layouts, UX flows, or API contracts feel inconsistent across features.
- When bundle size, performance metrics, or Core Web Vitals regress without an obvious local cause.
- When there are multiple design systems, component libraries, or styling approaches in the same repo.
- When documentation, comments, and actual implementation behavior are clearly drifting apart.
- When third-party integrations or shared services are used inconsistently across the codebase.
- When ownership boundaries between teams, domains, or packages are unclear from the directory structure.
- When the user requests a "map" of services, modules, or critical user journeys.


## Ownership and Boundaries

- Owns reading, indexing, and summarizing the repository structure, technologies, and conventions.
- Owns mapping critical user flows across frontend, backend, data, and external services.
- Owns identifying existing design systems, UI primitives, style tokens, and component patterns.
- Owns identifying public APIs, shared contracts, and schemas that must not break without explicit approval.
- Owns surfacing hotspots: high-churn files, complex modules, brittle areas, and known TODOs or FIXMEs.
- Does not independently rewrite architecture, schemas, or design systems; it only informs such decisions.
- Does not delete code, rename packages, or break API contracts without a separate, explicit change plan and approval.
- Preserves existing patterns and style guides unless there is clear evidence they are harmful, inconsistent, or blocking quality.
- Requests clarification when business domain, product intent, or UX expectations are ambiguous from the code alone.
- Stops and asks for approval before proposing large-scale refactors, framework swaps, or cross-cutting design system changes.


## Core Responsibilities

- Enumerate frameworks, languages, build systems, and main runtime environments (web, mobile web, server, workers).
- Map high-level architecture: frontends, backends, services, databases, queues, and third-party integrations.
- Identify core design system primitives, shared UI components, and styling conventions used across the app.
- Trace key user journeys end-to-end (route → UI → state → API → data layer → background jobs).
- Catalog API contracts, data models, and event schemas used by critical UX flows and UI states.
- Locate test suites (unit, integration, end-to-end) and understand what they cover and miss.
- Identify performance-critical paths (initial page load, primary dashboards, mobile-critical screens).
- Surface areas with poor accessibility, inconsistent responsive behavior, or missing loading/empty/error states.
- Identify configuration, feature flags, and environment-specific behaviors that affect UX and operations.
- Document ownership indicators (CODEOWNERS, labels, directories) to respect team and domain boundaries.
- Produce a concise architecture and dependency summary that can be referenced by other skills.
- Highlight outdated or duplicated patterns (legacy components, legacy endpoints, deprecated services) and where they appear.


## Step-by-Step Workflow

1. Scan the repository structure (monorepo packages, apps, services, libraries) and create a high-level map of domains and responsibilities.
2. Identify entry points (frontend routes, CLI commands, workers, API gateways) and map them to their main modules.
3. Inspect package manifests, build configs, and tooling to understand frameworks, design systems, and test infrastructure.
4. Trace at least two or three primary user journeys end-to-end, annotating involved components, APIs, and data models.
5. Locate and summarize shared UI primitives, layout components, and design tokens, noting how they enable responsive and accessible UX.
6. Enumerate major APIs and data stores, including how responses are shaped to support UI loading, empty, error, and success states.
7. Inspect observability, logging, and error handling patterns for signals about common failures or performance bottlenecks.
8. Identify and list hotspots (high complexity, high churn, many TODOs, test gaps) that pose risk for future work.
9. Summarize findings into a compact architecture and patterns overview, referencing concrete files, directories, and flows.
10. Share this overview as a basis for subsequent skills (architecture-planning, frontend-ui-ux, backend-api-data), updating it as the codebase evolves.

## Best Practices and Heuristics

- Prefer reading code paths from the perspective of real user journeys rather than starting from low-level utilities.
- Use commit history, blame views, and issue links to understand why architectural decisions were made, not just how.
- Classify patterns as "canonical", "legacy", or "one-off" to guide future contributions and refactors.
- Pay special attention to mobile-critical routes and components, ensuring you understand how responsive layouts are implemented.
- Identify how accessibility is currently handled (ARIA usage, focus management, keyboard handling) and where it is missing.
- Understand how design tokens (colors, spacing, typography) flow from configuration to actual UI components.
- Map how data loading is orchestrated (SSR, client fetches, caching) to avoid regressions in performance or hydration.
- Track how error boundaries, fallback UI, and retry mechanisms are implemented across the app.
- Note implicit contracts between frontend and backend (field names, status codes, pagination) that tests rely on.
- Align with repository-wide research and documentation standards configured for this environment.
- When documenting patterns, include concrete file paths and examples to anchor future changes in reality.
- Continuously update the mental and written map as new information surfaces from tests, logs, or user stories.
- Treat inconsistencies (multiple ways of doing the same thing) as signals to be cataloged, not fixed immediately.
- Preserve working, battle-tested patterns even if they are not the most "modern", unless they clearly block product quality.


## Things to Avoid

- Do not jump directly into implementation changes without first understanding how the repository is structured.
- Do not assume that the newest-looking pattern is the canonical one; verify usage frequency and documentation.
- Do not propose replacing frameworks, design systems, or build tools based on preference rather than concrete issues.
- Do not break assumptions baked into shared components, hooks, or helpers without a clear migration plan.
- Do not ignore mobile and accessibility behavior when mapping UX flows, even if desktop code looks richer.
- Do not overlook test suites; failing to understand existing tests leads to fragile refactors and regressions.
- Do not rely solely on comments or docs; always cross-check with current implementation and tests.
- Do not downplay the risk of changes in areas with high complexity, low test coverage, or many TODOs.
- Do not treat external services as black boxes; understand how their contracts and failure modes affect UX.
- Do not create sprawling internal documentation; prefer concise, navigable overviews linked to actual code.


## Quality Bar

- The agent can succinctly describe the system architecture and main flows to another engineer without hand-waving.
- Canonical patterns for UI components, styling, routing, data loading, and error handling are clearly identified.
- Key user journeys and their supporting APIs and data models are documented with specific file and route references.
- High-risk zones (legacy patterns, poor tests, performance hotspots) are clearly called out with reasons.
- The mapping enables architecture-planning, frontend, backend, and testing skills to operate confidently and consistently.
- The agent can quickly answer "Where should this go?" for new features, components, and services.
- Documentation of the codebase understanding is kept up to date as meaningful structural changes land.
- The resulting understanding directly reduces the risk of regressions in UX, accessibility, performance, and operations.


## Collaboration With Other Skills

- Provide architecture-planning with an up-to-date map of modules, dependencies, and hotspots to scope changes accurately.
- Inform frontend-ui-ux about existing design systems, layout primitives, and accessibility patterns to reuse.
- Guide backend-api-data on existing contracts, data models, and performance constraints to avoid breaking UX.
- Enable testing-qa to identify under-tested user journeys, integration points, and accessibility gaps.
- Help devops-cicd understand how builds, bundling, and deployment pipelines align with the logical architecture.
- Support debugging-performance by highlighting complex or high-traffic paths that require extra monitoring and profiling.


## Edge Cases

- Legacy monoliths with partial migrations to microservices or micro-frontends where patterns conflict.
- Multiple coexisting design systems or component libraries in different parts of the same app.
- Forked or vendored third-party code that looks like first-party modules and must not be modified lightly.
- Repos where documentation is badly outdated, requiring heavier reliance on tests and logs for truth.
- Systems with heavy runtime configuration or feature flags that drastically alter UX depending on environment or tenant.
- Environments where some services are stubbed or mocked locally, requiring care when inferring real production behavior.

=== FILE: architecture-planning.md
***
name: architecture-planning
description: Governs solution design, change scoping, interface contracts, and migration strategies for new features and refactors. Triggered when planning non-trivial changes that affect multiple layers (UI, APIs, data, infra) or risk breaking existing behavior.
license: Complete terms in LICENSE.txt
***

## Overview

This skill designs and plans architectural changes that balance product needs, UX quality, performance, and operational safety. It owns defining interfaces, data flows, and migration strategies so that frontend, backend, testing, and operations can execute coherently. Success means changes are scoped, incremental, reversible where possible, and compatible with existing UX, accessibility, and responsive behavior.

## When to Use This Skill

- When the user asks for a new feature that touches both frontend and backend.
- When planning refactors to routing, state management, or component architecture in the UI.
- When designing new APIs, data models, or background jobs to support new UX flows.
- When consolidating or replacing design systems, component libraries, or styling strategies.
- When migrating between frameworks, ORMs (object relational mappers), or deployment targets.
- When repeated bugs or performance issues suggest an architectural rather than local problem.
- When CI pipelines show frequent failures around flakiness, timeouts, or brittle integration tests.
- When user metrics (latency, error rates, layout shifts) indicate architectural constraints on UX quality.
- When introducing new third-party services that affect auth, payments, notifications, or analytics UX.
- When database schemas, queues, or caches must change in ways that can affect existing clients.
- When ownership boundaries between services or modules need to be clarified or redrawn.
- When planning feature flags, rollout strategy, and migration paths for risky changes.


## Ownership and Boundaries

- Owns designing architectures, module boundaries, and contracts that support the desired product and UX.
- Owns describing how frontend, backend, data, and integrations will collaborate to support responsive, accessible UIs.
- Owns defining migration strategies, rollout plans, and fallback paths for high-risk changes.
- Owns documenting decisions, tradeoffs, and assumptions in a form that other skills can follow.
- Does not unilaterally implement all changes; hands off to the appropriate execution skills for code changes.
- Does not break existing public APIs, schemas, or auth flows without explicit user approval and a migration plan.
- Preserves existing patterns when they are coherent and battle-tested, favoring incremental improvements.
- Proposes modernization (new frameworks, patterns) only when current approaches clearly block quality or maintainability.
- Asks for clarification when product goals, UX requirements, or data semantics are ambiguous.
- Stops and requests approval before planning large-scale re-architecture that spans multiple teams or services.


## Core Responsibilities

- Translate product and UX requirements into clear technical goals, constraints, and success metrics.
- Propose system designs that respect existing patterns and design systems while addressing new needs.
- Define clean interfaces and contracts between frontend components, APIs, data models, and background processes.
- Ensure API responses and data shapes explicitly support loading, empty, error, success, and partial-data UI states.
- Consider accessibility, responsive design, and mobile-first constraints when planning component and layout structure.
- Model data flows, caching layers, and eventing so that performance and consistency requirements are met.
- Plan migrations for schemas, endpoints, and shared components, including versioning and deprecation strategies.
- Identify risks (breaking changes, data loss, UX regressions) and propose mitigations and observability hooks.
- Decide where to place logic (client vs server vs worker) to optimize UX, performance, and maintainability.
- Specify testing strategies (unit, integration, E2E) tied to the architecture to protect key user journeys.
- Align deployment, rollback, and feature flagging strategies with the planned architecture.
- Produce diagrams or structured descriptions of the architecture so other skills can execute with minimal ambiguity.


## Step-by-Step Workflow

1. Collect requirements: clarify user goals, UX flows, performance constraints, and data semantics from specs, code, and stakeholders.
2. Inspect existing architecture and patterns from the codebase-understanding skill to avoid disruptive or inconsistent designs.
3. Enumerate possible designs, considering tradeoffs in complexity, performance, UX flexibility, and operational overhead.
4. Select a preferred design and at least one fallback, explicitly stating why the chosen approach fits the project constraints.
5. Define interfaces and contracts between modules and layers, including request/response shapes and error semantics.
6. Design migration and rollout steps (feature flags, phased rollouts, schema changes) with clear, incremental milestones.
7. Specify required tests, monitoring, and validation steps to ensure architectural integrity and UX quality.
8. Review risks and open questions; if high-risk or ambiguous, surface a proposal and request approval before proceeding.
9. Produce an actionable implementation plan, broken down into tasks and handoffs for frontend, backend, testing, and devops.
10. Update or create architecture documentation so future changes can build on the new structure safely.

## Best Practices and Heuristics

- Favor incremental, additive designs over disruptive rewrites, especially in high-traffic or poorly tested areas.
- Design APIs and contracts from the perspective of the UX, including async states, pagination, and validation feedback.
- Prefer using existing design system components and patterns; extend them only when genuinely necessary.
- Keep boundaries cohesive: group by business domain and user journeys, not just by technical layer.
- Push heavy computation and data aggregation to the server when it meaningfully reduces client complexity and bundle size.
- Respect mobile-first and responsive needs; ensure planned layouts and data payloads work on slow networks and small screens.
- Plan for accessibility early: error semantics, status messages, focus management, and ARIA roles should be contractually supported.
- Use event-driven, asynchronous workflows where latency or reliability requirements justify them, but avoid overcomplication.
- Explicitly design for failure: timeouts, retries, circuit breakers, and user-visible error states should be part of the plan.
- Prefer schemas and contracts that are forward-compatible, supporting unknown fields and partial responses gracefully.
- Align architectural decisions with how teams work (ownership, deployment boundaries), not only technical purity.
- Keep diagrams and docs close to the code (in-repo) to reduce drift and ensure they evolve with the implementation.
- Use feature flags and dark launches for risky changes; plan rollback conditions and monitoring beforehand.
- Revisit architecture plans after initial implementation feedback, adjusting when reality reveals better constraints.


## Things to Avoid

- Do not design architectures that require a full "big bang" cutover without a safe rollback path.
- Do not propose entirely new design systems or frameworks solely for stylistic reasons.
- Do not design APIs that only work for the immediate feature and cannot support foreseeable variations.
- Do not overload the client with orchestration and heavy data processing when the server is better suited.
- Do not ignore accessibility, mobile, and performance requirements because they are not explicitly mentioned.
- Do not break existing consumers (internal or external) without versioning or clear deprecation timelines.
- Do not spread business logic across too many layers, making it hard to reason about or test.
- Do not hide complexity in undocumented helpers, decorators, or magic configuration.
- Do not rely purely on "implicit" contracts; always document tolerated shapes, errors, and edge cases.
- Do not let diagrams or docs drift from implementation; outdated architecture docs are worse than none.
- Do not overfit the design to current tooling if it prevents future migrations or scaling.


## Quality Bar

- Architecture proposal clearly maps product goals to technical structures and interfaces.
- Frontend, backend, and integrations can implement their parts with minimal clarification and no contradictions.
- API contracts and data models are explicit, versioned where needed, and support complete UX states.
- Migration and rollout steps are safe, incremental, testable, and easy to monitor.
- Performance, accessibility, and responsive behavior are first-class in the design, not bolted on.
- Risks, tradeoffs, and alternatives are documented so future engineers understand why choices were made.
- Implementation can be validated against the plan, and any deviations are intentional and documented.
- The resulting system is simpler to reason about than before, or at least no more complex for significantly more capability.


## Collaboration With Other Skills

- Consume maps and hotspot analyses from codebase-understanding to ground architectural decisions.
- Provide backend-api-data with contracts and data flow expectations, including error handling and pagination.
- Guide frontend-ui-ux on how components should consume data and represent states across devices.
- Inform testing-qa of architectural seams and critical paths to prioritize in test coverage.
- Coordinate with devops-cicd on deployment topology, environment configuration, and observability requirements.
- Work with security-compliance to embed auth, authorization, and data protection into the design rather than adding it later.
- Align integrations-services work with isolation boundaries so third-party failures do not cascade into core UX flows.


## Edge Cases

- Systems with partial migrations where new and old architectures must coexist for an extended period.
- Multitenant environments where tenants have different feature sets, schemas, or UX requirements.
- Offline or low-connectivity scenarios where data syncing and conflict resolution must be planned.
- Heavy data or media workloads where bandwidth and processing constraints drive architectural choices.
- Regulated domains where compliance needs (audit trails, data residency) shape storage and interface design.

=== FILE: frontend-ui-ux.md
***
name: frontend-ui-ux
description: Handles implementation and refinement of user interfaces, interaction flows, accessibility, responsive behavior, and design system usage. Triggered by any UI work: new screens, components, layout fixes, design polish, or UX bug reports.
license: Complete terms in LICENSE.txt
***

## Overview

This skill is responsible for building and refining frontend UI that is accessible, responsive, performant, and aligned with the design system and product goals. It owns components, layouts, interaction states, and browser-side behavior, ensuring polished, mobile-first user experiences. Success means users experience predictable, fast, and inclusive interfaces across devices and scenarios.

## When to Use This Skill

- When implementing new pages, screens, or components based on designs or product requirements.
- When the user asks to "improve the UI", "polish the UX", or "make this responsive/mobile-friendly".
- When fixing layout issues, broken styles, overlapping elements, or layout shift problems.
- When adding or correcting loading, empty, error, success, and partial-data states in the UI.
- When implementing or extending the design system, component library, or styling tokens.
- When addressing accessibility bugs or ensuring WCAG-aligned behavior and keyboard navigation.
- When integrating new APIs or data sources into views, lists, forms, or dashboards.
- When improving perceived performance via skeletons, progressive rendering, or code splitting.
- When user feedback or analytics show poor engagement or friction in critical flows.
- When updating UI to match refreshed branding, themes, or visual language.
- When refactoring legacy views to align with modern patterns, frameworks, or design systems.
- When cross-browser or cross-device inconsistencies are reported.


## Ownership and Boundaries

- Owns visual and interaction behavior of web UIs, including components, layouts, and transitions.
- Owns adopting and extending the design system, including tokens, primitives, and reusable components.
- Owns implementing accessibility, keyboard support, focus management, and meaningful semantics.
- Owns defining and rendering all UI states for a given view (loading, empty, error, success, partial, disabled).
- Collaborates with backend-api-data to shape responses that support clean UI states.
- Does not change business rules, core data models, or API semantics without backend coordination.
- Does not introduce new theming or design systems without aligning with architecture-planning and product intent.
- Preserves existing component APIs and patterns unless there is a clear, documented reason to evolve them.
- Requests clarification when designs conflict with technical constraints or accessibility requirements.
- Stops and asks for approval before replacing foundational layout systems, routing layers, or shared primitives.


## Core Responsibilities

- Implement semantic, accessible markup using the framework's idioms (e.g., React, Vue, Svelte).
- Use the design system components and tokens to build consistent, theme-aware UIs.
- Design and implement mobile-first responsive layouts using established grid and spacing scales.
- Implement and wire up all interaction states: hover, focus, active, disabled, loading, and error.
- Integrate with APIs and data sources using patterns that support streaming, pagination, and partial data.
- Implement localized and accessible error messages, form validation feedback, and status updates.
- Optimize rendering performance by minimizing rerenders, memoizing where appropriate, and splitting bundles.
- Ensure SSR and hydration behavior are preserved where used, avoiding client-only assumptions.
- Implement keyboard and screen reader support, including focus order, skip links, and ARIA roles where needed.
- Add visual regression and interaction tests for critical components and flows in collaboration with testing-qa.
- Ensure forms, navigation, and primary actions are easy to use via touch and pointer devices.
- Maintain storybooks, sandboxes, or component demos that document usage and edge cases.


## Step-by-Step Workflow

1. Review designs, product requirements, and existing patterns to understand the target UX and constraints.
2. Inspect the codebase for existing components, layout primitives, and tokens to reuse or extend.
3. Propose a component and layout structure, including how data and state will flow through the UI.
4. Implement the UI using semantic markup, design system primitives, and mobile-first responsive patterns.
5. Wire up data fetching, state management, and side effects using established patterns and contracts.
6. Implement all UI states (loading, empty, error, success, disabled, partial) and ensure they are visually and accessibly distinct.
7. Add keyboard navigation, focus management, ARIA attributes, and accessible labels/descriptions.
8. Optimize for performance (bundle size, rerenders, lazy loading) and validate behavior across devices and browsers.
9. Add or update tests (unit, integration, visual) for critical components and flows with testing-qa.
10. Document component APIs, expected props, usage patterns, and known limitations for docs-knowledge.

## Best Practices and Heuristics

- Start designs mobile-first: ensure small screens and touch interactions work flawlessly before optimizing desktop layouts.
- Use existing design tokens and components; only extend or create new ones when patterns truly diverge.
- Keep components small, focused, and composable; avoid deeply nested hierarchies that are hard to test and reason about.
- Favor flex and grid layouts with fluid widths and min/max constraints to handle variable content gracefully.
- Use clear, descriptive labels, helper text, and error messages that assist both sighted users and screen reader users.
- Maintain visible focus states, logical tab order, and skip navigation for keyboard users.
- Use progressive enhancement: core flows should work without JavaScript-heavy features when possible.
- Handle long loading operations with skeletons, spinners, and progress indicators; avoid frozen or ambiguous states.
- Avoid overfetching and redundant network requests; cache or reuse data where appropriate.
- Defer heavy, non-critical scripts below-the-fold using lazy loading and code splitting.
- Keep animations subtle and optional; respect reduced-motion preferences and avoid seizure triggers.
- Use logical color contrasts, font sizes, and line heights that meet or exceed accessibility guidelines.
- Validate that layouts and interactions behave correctly across major browsers and device sizes.
- Collaborate early with backend and testing skills to ensure contracts and test coverage match the intended UX.


## Things to Avoid

- Do not bypass the design system by hardcoding colors, spacing, or typography without a justified exception.
- Do not rely solely on visual cues (color, position) to communicate important information.
- Do not implement custom controls (selects, sliders, date pickers) without strong justification and accessibility coverage.
- Do not couple components tightly to specific APIs; keep them adaptable to future contract changes.
- Do not introduce blocking synchronous work (heavy computations) on the main thread that hurts responsiveness.
- Do not hide errors silently; always show understandable messages and recovery paths where appropriate.
- Do not assume high bandwidth or desktop screen sizes; avoid fixed widths and oversized assets.
- Do not scatter inline styles or ad hoc utility classes that duplicate design tokens.
- Do not bypass SSR or hydration constraints with client-only hacks that break routing or initial render.
- Do not leave interactive elements without hover/focus/active feedback.
- Do not degrade keyboard support or introduce focus traps when adding modals, popovers, or drawers.
- Do not merge UI changes without basic cross-browser and device sanity checks.


## Quality Bar

- UI matches design intent while respecting design system constraints and project conventions.
- All critical flows are responsive, keyboard-accessible, and screen-reader-friendly.
- All async operations expose clear loading, error, and success states with actionable messages.
- Layouts handle variable content without overlap, clipping, or layout shifts in normal usage.
- Initial load and interactions feel snappy on mid-range mobile devices and typical networks.
- Component APIs are documented, predictable, and fit naturally into the existing frontend architecture.
- New UI work does not introduce visual or interaction regressions in other parts of the app.
- Tests guard critical user journeys, including responsive and accessibility behavior where feasible.


## Collaboration With Other Skills

- Work with backend-api-data to ensure endpoints support the data shapes needed for rich UI states.
- Coordinate with architecture-planning when introducing new layout or state management patterns.
- Partner with testing-qa to define and automate tests that exercise critical flows and accessibility behavior.
- Collaborate with security-compliance to ensure auth, session, and permissions are correctly surfaced in UI.
- Align with integrations-services to expose third-party failures and retries through clear, user-friendly states.
- Provide docs-knowledge with component usage guidelines, UX rationale, and edge case handling.


## Edge Cases

- Very long or localized text strings that can break layouts or overflow controls.
- Low-vision or screen reader users interacting with complex components like tables, carousels, or modals.
- Offline or degraded network states where cached data must be reconciled with fresh data.
- High-density data views (tables, dashboards) on small screens requiring adaptive summarization.
- User sessions expiring mid-flow (e.g., in forms) and needing non-destructive recovery patterns.

=== FILE: backend-api-data.md
***
name: backend-api-data
description: Manages API design and implementation, data modeling, validation, persistence, and background processing. Triggered by server-side feature work, new endpoints, schema changes, or data pipeline updates that support frontend and integrations.
license: Complete terms in LICENSE.txt
***

## Overview

This skill is responsible for designing and implementing backend APIs, data models, and persistence logic that reliably support product and UX needs. It owns request handling, validation, data shaping, and background jobs, ensuring responses enable rich UI states and performant, secure behavior. Success means stable contracts, correct data, and predictable performance across environments.

## When to Use This Skill

- When adding, updating, or deprecating REST, GraphQL, RPC, or WebSocket endpoints.
- When implementing new data models, database tables, migrations, or indexes.
- When designing responses to support detailed UI loading, empty, error, success, and partial-data states.
- When adding validation, sanitization, or normalization logic for inputs from UI or external services.
- When implementing background jobs, queues, scheduled tasks, or event processing.
- When optimizing offline or caching strategies that affect UX and data freshness.
- When adjusting APIs to serve new devices, platforms, or client types.
- When improving backend performance, latency, throughput, or query efficiency for key flows.
- When adding integration points that read or write to internal data stores.
- When refactoring legacy code paths that serve critical UX flows or integrations.
- When aligning with new architecture plans that affect service boundaries or contracts.
- When dealing with data migrations that can affect existing user data and analytics.


## Ownership and Boundaries

- Owns the design and implementation of backend APIs and data access patterns.
- Owns ensuring responses are shaped to support frontend UI states and performance expectations.
- Owns database schemas, migrations, and data integrity, including indexes and constraints.
- Owns data validation, normalization, and error semantics for incoming requests.
- Collaborates with frontend-ui-ux to align contracts with UX needs and interaction states.
- Collaborates with security-compliance to enforce auth, authorization, and data protection on server side.
- Does not change UX copy or visual presentation; it shapes data and semantics, not pixels.
- Does not modify infrastructure-level deployment settings without devops-cicd coordination.
- Preserves existing public APIs and schemas unless there is a clear, approved migration path.
- Requests clarification and approval before destructive data operations or contract-breaking schema changes.


## Core Responsibilities

- Design API routes, methods, and payloads that align with domain models and UX requirements.
- Implement request handling, validation, and error mapping using framework idioms and shared utilities.
- Model data with appropriate normalization/denormalization tradeoffs, indexes, and constraints.
- Implement migrations safely, considering data volumes, locking, and rollback strategies.
- Ensure responses include sufficient metadata (pagination, cursors, counts, flags) for rich UI behavior.
- Implement consistent error semantics (codes, messages) that allow UI to distinguish and handle failure types.
- Design and implement background jobs and queues for long-running or async operations.
- Optimize queries and data access paths to meet latency and throughput goals, especially for critical UX flows.
- Add logging, metrics, and traces that enable debugging and performance analysis.
- Provide test fixtures, factories, and integration tests that validate contracts end-to-end.
- Support caching strategies (HTTP caching, server caches) that improve performance without stale or inconsistent UX.
- Maintain compatibility where possible with existing clients, including mobile apps or external consumers.


## Step-by-Step Workflow

1. Clarify requirements with frontend-ui-ux and architecture-planning: what data is needed, when, and with which states.
2. Inspect existing APIs and data models to identify reusable patterns and avoid duplicating logic.
3. Design endpoints, request/response shapes, and data models, documenting them clearly before implementation.
4. Implement request handling, validation, and persistence logic using established conventions and libraries.
5. Add or update database migrations, indexes, and constraints, planning for safe rollout and rollback.
6. Implement error handling semantics that distinguish client errors, server errors, and transient failures.
7. Add necessary background jobs, queues, or event handlers, ensuring idempotency and observability.
8. Write or extend automated tests (unit, integration) to enforce contracts and protect against regressions.
9. Validate performance characteristics with representative data, adjusting queries and caching as needed.
10. Communicate changes to frontend, integrations, and docs-knowledge, updating references and documentation.

## Best Practices and Heuristics

- Design APIs around business domain and user journeys, not just database tables.
- Include explicit fields that help the UI represent states (e.g., status enums, flags, timestamps, progress).
- Use pagination and server-side filtering to avoid large payloads that hurt mobile performance.
- Fail fast and clearly on validation errors; return helpful, localized error codes/messages for UI mapping.
- Make long-running operations asynchronous with job queues and progress polling or push notifications.
- Prefer additive changes (new fields, new endpoints) over in-place breaking changes; deprecate gradually.
- Use transactions, constraints, and idempotent operations to protect data integrity under retries and concurrency.
- Index on query patterns used in critical UX paths, not only on primary keys.
- Log structured events and metrics for key operations to support debugging and performance analysis.
- Avoid exposing internal implementation details (table names, stack traces) in public API responses.
- Consider eventual consistency and data staleness; communicate via fields the UI can interpret.
- Keep business logic centralized where appropriate; avoid scattering critical rules across many layers.
- Test with realistic data volumes and access patterns, especially for dashboards and list views.
- Document contracts and examples so other skills and services can integrate confidently.


## Things to Avoid

- Do not shape APIs purely around the current UI; anticipate reasonable extensions and reuse.
- Do not return ambiguous responses that force the UI to infer states from fragile heuristics.
- Do not expose sensitive internal fields or implementation details in public outputs.
- Do not rely solely on client-side validation; always enforce server-side validation and authorization.
- Do not run dangerous migrations (drops, type changes) without backups, rollbacks, and approvals.
- Do not ignore query performance in favor of "clean" abstractions when real data volumes are high.
- Do not conflate transport-level errors (network, timeouts) with domain errors in error codes.
- Do not silently swallow exceptions; log and categorize errors for observability and alerts.
- Do not implement ad hoc caching without understanding cache invalidation and UX expectations.
- Do not add new persistence technologies lightly; align with architecture-planning and devops-cicd.
- Do not break existing clients without versioning, migration guides, and deprecation communication.


## Quality Bar

- APIs are predictable, well-documented, and aligned with domain language and UX needs.
- Responses support all necessary UI states while minimizing overfetching and payload size.
- Data models and queries scale to expected workloads with acceptable latency and resource usage.
- Error semantics are consistent, actionable, and safe to expose to end users where needed.
- Migrations run safely in production with monitoring and rollback plans.
- Tests cover critical endpoints, data flows, and edge cases, catching regressions before release.
- Logs and metrics provide enough insight to troubleshoot incidents and performance issues.
- Frontend, integrations, and docs consumers can rely on contracts with high confidence.


## Collaboration With Other Skills

- Align with architecture-planning on service boundaries, data modeling, and migration strategies.
- Coordinate with frontend-ui-ux to support UI statefulness, validation, and responsive performance.
- Partner with testing-qa to build integration tests that exercise real contracts and data flows.
- Work with security-compliance to enforce auth, authorization, rate limiting, and audit logging.
- Collaborate with integrations-services when internal APIs feed or depend on external services.
- Inform devops-cicd about resource needs, migrations, and rollout sequencing for backend changes.
- Provide docs-knowledge with up-to-date API and schema references.


## Edge Cases

- Large, bursty traffic patterns (campaigns, launches) that stress endpoints and database connections.
- Multi-region deployments where latency and consistency differ across data centers.
- Tenants or customers with custom fields, feature sets, or SLAs that complicate shared schemas.
- Historical data migrations where legacy formats and missing fields must be reconciled.
- Regulatory requirements that demand data retention, deletion, or residency behavior.

=== FILE: testing-qa.md
***
name: testing-qa
description: Defines how to design and maintain automated tests and quality gates that protect critical user journeys, accessibility, and responsive behavior. Triggered by new features, regressions, CI failures, or when improving test strategy.
license: Complete terms in LICENSE.txt
***

## Overview

This skill is responsible for planning and implementing test coverage that protects core functionality, UX behavior, accessibility, and performance-critical flows. It owns test strategy, structure, and reliability across unit, integration, and end-to-end levels. Success means changes ship with confidence, and regressions in key UX and data behaviors are caught early.

## When to Use This Skill

- When implementing new features or refactors that affect user journeys, APIs, or data flows.
- When tests are missing, flaky, failing intermittently, or providing poor signal.
- When CI pipelines are slow, unreliable, or frequently blocked by brittle tests.
- When critical bugs reach production that should have been caught earlier.
- When adding or modifying accessibility and responsive behaviors in the UI.
- When changing API contracts, data models, or background jobs.
- When refactoring legacy areas with little or no automated coverage.
- When instrumenting performance-sensitive endpoints or views that need regression protection.
- When the user requests "add tests", "improve test coverage", or "stabilize CI".
- When introducing new tools (test runners, linters, visual regression tools) or reorganizing test suites.
- When documenting quality gates for release and deployment workflows.
- When accessibility audits or UX reviews uncover issues that need automated checks.


## Ownership and Boundaries

- Owns the design of the test pyramid: unit, integration, E2E, and their distribution.
- Owns selection and configuration of test tools, runners, and helpers within project norms.
- Owns writing and maintaining test cases that protect critical journeys and contracts.
- Owns defining CI test stages, gates, and fast feedback loops in collaboration with devops-cicd.
- Collaborates with frontend-ui-ux to cover responsive, interactive, and accessibility behaviors.
- Collaborates with backend-api-data to cover endpoints, data integrity, and error semantics.
- Does not own product requirements or UX design decisions; it validates their implementation.
- Does not gate releases with new heavy test suites without discussing impact on cycle times.
- Preserves existing test patterns unless they are clearly brittle, misleading, or inconsistent.
- Requests clarification when expected behavior is unclear, undocumented, or contradictory across specs and code.


## Core Responsibilities

- Identify and prioritize critical user journeys, APIs, and data flows that require automated protection.
- Design test cases that validate both happy paths and realistic edge cases, including error and empty states.
- Implement unit tests for core logic, utilities, and pure functions to keep them reliable and refactor-friendly.
- Implement integration tests that exercise module boundaries, APIs, and data store interactions.
- Implement E2E tests for high-value flows, including responsive behavior and key interaction sequences.
- Add accessibility checks (e.g., axe, ARIA validation) into appropriate layers of the test suite.
- Incorporate visual or snapshot tests cautiously for components and layouts prone to regression.
- Configure test data factories, fixtures, and seeders that mirror realistic usage scenarios.
- Monitor test flakiness, execution time, and coverage, and continuously improve reliability.
- Integrate tests into CI pipelines, gating merges and deployments appropriately.
- Document test strategy, conventions, and how to run/debug tests for other contributors.


## Step-by-Step Workflow

1. Review product requirements, architecture maps, and recent incidents to identify what must be protected.
2. Inspect existing test suites to understand current patterns, coverage, and pain points.
3. Propose or adjust the test strategy for the change: which layers, which cases, and desired confidence.
4. Implement or update tests incrementally alongside the production code changes.
5. Run tests locally and in CI, analyzing failures and flakiness; fix issues at the root, not just assertions.
6. Optimize slow or brittle tests by adjusting scopes, selectors, data setup, or tooling configuration.
7. Add accessibility, responsiveness, and interaction coverage where relevant for UI work.
8. Update documentation and test helpers to make it easier for future contributors to write good tests.
9. Review test results and coverage after merge to ensure gains are realized and maintained.
10. Coordinate with devops-cicd to adjust test stages and gating rules based on new coverage and performance.

## Best Practices and Heuristics

- Focus on protecting business-critical and user-critical flows first (signup, auth, payments, core workflows).
- Prefer fast, deterministic unit and integration tests over brittle, slow E2E coverage for every detail.
- Use realistic, minimal test data that exercises key paths without overcomplicating setup.
- Mock only where necessary; favor integration tests that hit real components and endpoints for contracts.
- Use semantic queries in UI tests (roles, labels) rather than brittle CSS selectors, reinforcing accessibility.
- Ensure tests explicitly cover loading, empty, error, and success states for UI components.
- Include tests for responsive behavior (e.g., viewport changes, breakpoint-specific layouts) where critical.
- Run accessibility checks in CI to catch regressions in ARIA attributes, color contrast, and keyboard flows.
- Parallelize tests, shard by suite, and optimize setup/teardown to keep feedback loops fast.
- Tag tests by criticality or ownership to prioritize runs and debugging during incidents.
- Regularly prune redundant or low-value tests that slow pipelines without adding confidence.
- Keep test code clean, readable, and refactor-friendly; follow the same standards as production code.
- Record regressions as new tests to ensure they never reoccur without detection.
- Align test naming and organization with domain concepts so failures are easy to interpret.


## Things to Avoid

- Do not assert on irrelevant implementation details that make tests fragile (CSS class names, internal props).
- Do not couple tests tightly to internal component structure; treat UI like a user would.
- Do not rely on long arbitrary timeouts instead of waiting for specific conditions or events.
- Do not let flakiness persist; investigate root causes instead of adding retries blindly.
- Do not add excessive E2E coverage that duplicates lower-level tests without added value.
- Do not skip tests in CI without clear documentation and a plan to fix them.
- Do not use production data or secrets in tests; always use safe fixtures and test environments.
- Do not mock external services in ways that diverge from real responses and failure modes.
- Do not ignore accessibility or responsive behavior in tests when they are part of core flows.
- Do not hardcode environment-specific paths, URLs, or credentials into tests.
- Do not merge tests that have inconsistent outcomes across platforms or environments.


## Quality Bar

- Critical user journeys are covered by reliable tests that fail when behavior breaks.
- Tests run within acceptable time limits for frequent feedback, even on CI.
- Failure messages clearly indicate what broke and why, minimizing debugging time.
- Accessibility and responsive behavior are tested for relevant features, preventing regressions.
- Test suites are stable over time; flakiness is systematically reduced, not tolerated.
- New features land with corresponding tests; coverage does not trend downward.
- Contributors can easily discover how and where to add tests for new work.
- CI gating based on tests reflects real confidence, not false positives or negatives.


## Collaboration With Other Skills

- Work with frontend-ui-ux to define what "correct" looks like for interactions, states, and accessibility.
- Coordinate with backend-api-data to cover contracts, error semantics, and performance-critical endpoints.
- Align with devops-cicd on how tests are run, parallelized, and used to gate releases.
- Inform debugging-performance work through tests that reproduce and guard against previous issues.
- Provide docs-knowledge with updated test strategy, examples, and troubleshooting tips.


## Edge Cases

- Multi-tenant behavior where tests must validate different feature flags or configurations.
- Time-dependent logic (scheduling, expirations) where clocks must be controlled or simulated.
- Browser-specific quirks that require targeted tests or shims.
- Flows depending on external services or payments that need realistic sandbox behavior.

=== FILE: devops-cicd.md
***
name: devops-cicd
description: Manages build pipelines, environments, deployment workflows, and observability hooks to ship changes safely and quickly. Triggered when adjusting CI/CD, adding environments, or improving reliability and release confidence.
license: Complete terms in LICENSE.txt
***

## Overview

This skill is responsible for configuring and maintaining CI/CD pipelines, environment orchestration, and observability so that frontend, backend, and infrastructure changes ship safely. It owns build, test, deploy, and rollback workflows, ensuring performance, UX, and security are preserved across environments. Success means predictable, low-friction releases with strong safeguards.

## When to Use This Skill

- When setting up or modifying CI pipelines for builds, tests, and checks.
- When configuring deployment workflows for web frontends, APIs, workers, or scheduled jobs.
- When adding or adjusting environments (dev, staging, preview, production).
- When CI is slow, flaky, or failing in ways that block development.
- When releases are manual, error-prone, or missing rollback strategies.
- When introducing new services, design systems, or frameworks that need build adjustments.
- When frontends need preview environments for UX and responsive testing.
- When adding observability (logging, metrics, traces) or error monitoring for deployments.
- When implementing feature flags, canary deploys, or progressive rollouts.
- When adjusting caching, CDNs, or asset pipelines for performance improvements.
- When incidents reveal gaps in monitoring, alerting, or environment parity.
- When defining release processes and quality gates with other teams.


## Ownership and Boundaries

- Owns CI pipeline definitions, stages, caching, and resource configuration.
- Owns CD workflows, including deployment triggers, approvals, and rollback mechanisms.
- Owns environment configuration and secrets wiring, not the secrets themselves.
- Owns integration of tests, linters, and checks into the CI/CD flow with testing-qa.
- Collaborates with backend-api-data and frontend-ui-ux on build tooling and environment needs.
- Collaborates with security-compliance on secrets management, scanning, and hardening steps.
- Does not redefine architectural boundaries or service responsibilities; it operationalizes them.
- Does not modify product logic or UX behavior except as needed for environment toggles.
- Preserves existing reliable pipelines, optimizing rather than rewriting when possible.
- Requests approval before changing deployment strategies, environments, or access controls in risky ways.


## Core Responsibilities

- Configure CI workflows to build, lint, test, and package applications efficiently.
- Set up caching for dependencies and build artifacts to speed up pipelines.
- Configure environment-specific variables and secrets through secure mechanisms.
- Define deployment jobs for frontend assets, APIs, and background workers with clear ordering and dependencies.
- Implement blue-green, canary, or rolling deployments where appropriate for risk reduction.
- Integrate automated tests, quality gates, and security scans into CI.
- Set up observability hooks (logs, metrics, traces) and error reporting for deployments.
- Provide preview environments or branches for UX review, responsive checks, and stakeholder signoff.
- Configure rollbacks and disaster recovery playbooks for failed deploys.
- Document CI/CD processes, environment behavior, and how to troubleshoot failures.


## Step-by-Step Workflow

1. Assess existing pipelines, deployment strategies, and pain points using logs, configs, and stakeholder input.
2. Define desired workflows for build, test, and deploy stages based on the project’s size and criticality.
3. Implement or adjust CI configurations, ensuring builds are reproducible and efficient.
4. Integrate test suites, linters, and security scans into appropriate pipeline stages with clear gating rules.
5. Configure deployment workflows, including environment variables, secrets, and necessary approvals.
6. Add observability and notifications around deployments, including success, failures, and rollbacks.
7. Optimize pipeline performance with caching, parallelization, and scoped triggers.
8. Test changes in non-production environments, verifying that frontend, backend, and integrations behave correctly.
9. Roll out changes to production carefully, monitoring metrics and logs; be ready to rollback if necessary.
10. Update documentation and runbooks to reflect new pipelines, environments, and operational procedures.

## Best Practices and Heuristics

- Keep pipelines simple and composable; separate build, test, and deploy concerns clearly.
- Run fast, critical checks early (lint, unit tests) to fail quickly; defer heavier checks to later stages.
- Use environment variables and secret managers (not hardcoded configs) for sensitive data.
- Pre-build frontend assets and static content with cache-busting to avoid stale UX in browsers.
- Provide branch or PR-based preview environments so UX and responsive issues can be caught early.
- Use infrastructure-as-code where possible to minimize configuration drift between environments.
- Set baseline SLOs (service level objectives) for latency, error rates, and availability; monitor them around deploys.
- Use feature flags and gradual rollouts to de-risk large UX or backend changes.
- Automate rollbacks and verify their correctness regularly, not just on paper.
- Limit access and permissions for CI/CD credentials following least-privilege principles.
- Keep logs and artifacts (screenshots, bundles) from failed deploys/tests for easier debugging.
- Continuously refine workflows based on real failure modes and developer feedback.
- Ensure that performance and accessibility checks (e.g., Lighthouse) are periodically run and tracked.
- Align deploy windows and processes with business impact and user traffic patterns.


## Things to Avoid

- Do not make deployments manual by default; aim for automation with clear, minimal approvals.
- Do not embed secrets directly in code, configs, or CI definitions.
- Do not tie pipelines too tightly to a single person’s environment or assumptions.
- Do not allow CI to become excessively slow; avoid running all heavy jobs on every trivial change.
- Do not deploy directly to production from unreviewed branches or without passing tests.
- Do not ignore environment differences; ensure staging is representative of production where feasible.
- Do not skip rollbacks or treat them as an afterthought; they must be tested and documented.
- Do not use opaque, undocumented scripts that only one person understands.
- Do not ignore frontend build and cache invalidation issues that affect UX and responsiveness.
- Do not disable checks (tests, linters, security scans) to "get things out the door" without follow-up.


## Quality Bar

- Pipelines are reliable, fast, and transparent; developers understand what runs and why.
- Deployments are low-drama events with clear logs, metrics, and rollback options.
- All important checks (tests, security scans, accessibility or performance checks where configured) run consistently.
- Environments (dev, staging, production) behave predictably with well-defined purposes.
- Incidents due to deployment misconfigurations or environment drift are rare.
- Preview environments support UX, accessibility, and responsive testing before merging.
- Documentation makes it easy for new contributors to understand how code moves to production.
- Security, compliance, and privacy considerations are enforced in CI/CD workflows.


## Collaboration With Other Skills

- Coordinate with testing-qa to stage tests and define gating policies.
- Work with backend-api-data and frontend-ui-ux to ensure build and runtime configs meet their needs.
- Collaborate with security-compliance on secret management, scanning, and policy enforcement.
- Enable debugging-performance by ensuring logs, metrics, and traces are captured during deploys.
- Provide docs-knowledge with up-to-date CI/CD docs and runbooks.


## Edge Cases

- Multi-region or multi-cloud deployments that require coordinated rollouts.
- Blue-green or canary deployments where only a subset of users see new UI or APIs.
- Legacy systems that cannot easily be containerized or managed with modern tools.
- High-compliance environments where additional approvals and checks are legally required.

=== FILE: security-compliance.md
***
name: security-compliance
description: Ensures authentication, authorization, data protection, and abuse prevention are implemented safely while preserving good UX. Triggered by auth work, handling sensitive data, adding integrations, or responding to security concerns.
license: Complete terms in LICENSE.txt
***

## Overview

This skill is responsible for embedding security and compliance best practices into code, APIs, and UX flows without introducing unnecessary friction. It owns auth logic, permission checks, secrets management usage, and data protection patterns. Success means users are protected, regulators are satisfied, and flows remain usable and consistent across devices.

## When to Use This Skill

- When implementing or modifying authentication, authorization, or session management.
- When handling sensitive data (PII, payments, health, secrets) in frontend or backend code.
- When integrating third-party auth providers, payment processors, or data processors.
- When adding new APIs or endpoints that expose or modify user or system data.
- When building admin panels, elevated privilege flows, or multi-tenant access controls.
- When enabling features like password reset, MFA (multi-factor authentication), or device trust.
- When addressing security issues found in audits, bug reports, or vulnerability scans.
- When configuring secrets in CI/CD or environment variables.
- When implementing rate limiting, abuse prevention, or input sanitization mechanisms.
- When working in regulated environments with explicit compliance requirements (GDPR, HIPAA, PCI).
- When building or adjusting logs and audit trails related to user actions or data access.
- When designing error and timeout handling for auth-related flows.


## Ownership and Boundaries

- Owns guidelines and implementation patterns for auth, permissions, and sensitive data handling.
- Owns security-focused input validation, encoding, and sanitization patterns.
- Owns recommending and using proper secrets management, not storing secrets directly in code.
- Collaborates with frontend-ui-ux to design usable and accessible auth and security flows.
- Collaborates with backend-api-data to enforce authorization and data access controls at the server.
- Collaborates with devops-cicd on secure configuration, scanning, and least-privilege CI/CD practices.
- Does not design overall product UX; it shapes constraints and security posture rather than visual design.
- Does not handle legal interpretation of compliance rules; it implements technical mitigations as directed.
- Preserves existing, proven security patterns unless there is a clear vulnerability or compliance gap.
- Requires approval before changing core auth models, token formats, or session lifetimes that impact many flows.


## Core Responsibilities

- Implement secure authentication flows (login, signup, logout, password reset) with proper session management.
- Enforce authorization checks consistently across APIs, background jobs, and UI controls.
- Ensure sensitive data is encrypted at rest and in transit, using modern protocols and libraries.
- Avoid exposing secrets or tokens in client code, logs, or URL query strings.
- Apply defense-in-depth: validate inputs, encode outputs, and use safe query/ORM patterns.
- Implement CSRF, XSS, SSRF, and injection mitigations as appropriate for the stack.
- Design security measures that balance protection with good UX (e.g., reasonable session timeouts, clear feedback).
- Configure rate limiting, captcha where necessary, and abuse detection for critical endpoints.
- Ensure logs and audit trails capture necessary events without leaking sensitive data.
- Participate in threat modeling and review of new features or integrations.
- Add automated checks (linters, dependency scanning, SAST/DAST) into CI/CD with devops-cicd.
- Provide clear documentation of security-related flows, assumptions, and operational procedures.


## Step-by-Step Workflow

1. Identify the data, users, and assets at risk in the feature or change being implemented.
2. Review existing auth, permissions, and data handling patterns to align with established practices.
3. Design or adjust flows (UI and API) to enforce proper authentication and authorization at appropriate boundaries.
4. Implement secure session handling, token storage, and cookie configurations consistent with the threat model.
5. Add validation, sanitization, and encoding at inputs and outputs to mitigate common vulnerabilities.
6. Integrate rate limiting, logging, and monitoring for security-sensitive endpoints.
7. Review changes against relevant compliance or security guidelines; adjust as needed.
8. Write or update tests to verify auth rules, permission checks, and edge cases (expired sessions, revoked access).
9. Coordinate with devops-cicd for secure configuration, secrets setup, and runtime checks.
10. Document the security model, assumptions, and procedures for incident response.

## Best Practices and Heuristics

- Use proven libraries and frameworks for auth and crypto; avoid rolling your own.
- Prefer server-side sessions or HTTP-only secure cookies for tokens where feasible.
- Use least privilege for all roles and services; deny by default and explicitly grant access.
- Avoid storing sensitive data in localStorage or other insecure client-side locations.
- Provide clear, accessible error and help texts for auth failures without oversharing details.
- Enforce strong password and MFA policies where appropriate, but avoid excessive friction for low-risk actions.
- Validate and constrain inputs at every trust boundary; avoid passing raw user inputs to queries or shell commands.
- Sanitize HTML content and use content security policies to reduce XSS risk.
- Limit data exposure in APIs to what is necessary; avoid wildcards or overly broad filters.
- Ensure logout, revocation, and rotation flows work across devices and sessions.
- Regularly update dependencies and monitor for known vulnerabilities.
- Restrict access to secrets; use vaults or managed secret stores integrated with CI/CD.
- Log security-relevant events (logins, permission changes) with enough context for audits.
- Consider accessibility in security UIs (MFA prompts, captchas) to avoid excluding users with disabilities.


## Things to Avoid

- Do not embed API keys, passwords, or tokens directly in source code or public repositories.
- Do not use outdated crypto algorithms or insecure token formats.
- Do not rely solely on client-side checks for permissions or data filtering.
- Do not give verbose error messages that help attackers distinguish valid vs invalid accounts.
- Do not overcomplicate auth flows without a clear threat model or risk justification.
- Do not allow mixed-content or insecure transport for sensitive flows.
- Do not log full tokens, passwords, or sensitive fields; redact where appropriate.
- Do not bypass established auth or permission middleware for expediency.
- Do not ignore security test failures or vulnerability scans without analysis and mitigation.
- Do not disable security headers (CSP, HSTS, X-Frame-Options) without reasoned alternatives.
- Do not implement captchas or security challenges that are unusable on mobile or with assistive tech.


## Quality Bar

- Auth flows are robust, consistent, and intuitive across devices and assistive technologies.
- Permissions are enforced reliably at server and client levels, with no obvious bypasses.
- Sensitive data is appropriately protected in transit, at rest, and in logs.
- Security controls do not introduce unnecessary friction or confusion for legitimate users.
- Dependencies and configurations are regularly updated and scanned for vulnerabilities.
- Incident response and recovery steps are clear and testable.
- Security assumptions and design choices are documented and reviewable.
- Compliance obligations are met with verifiable controls and logs where required.


## Collaboration With Other Skills

- Coordinate with frontend-ui-ux to design usable, accessible auth and security UX.
- Partner with backend-api-data to enforce access control and data minimization at the API level.
- Work with devops-cicd on secrets management, scanning, and secure environment configs.
- Inform testing-qa of security-critical flows that need automated coverage.
- Provide docs-knowledge with clear explanations of security models and operational procedures.
- Align with integrations-services on safe ways to interact with third-party APIs and data processors.


## Edge Cases

- Shared devices, public kiosks, or low-trust environments where session behavior must be stricter.
- Users with limited devices or connectivity who cannot easily complete complex MFA.
- Regions with specific data residency or privacy rules that affect storage and replication.
- Emergency access or break-glass procedures that require special handling.

=== FILE: integrations-services.md
***
name: integrations-services
description: Manages integration with third-party APIs and internal services, including contracts, retries, idempotency, and failure handling. Triggered when adding or modifying external or cross-service dependencies that affect product behavior.
license: Complete terms in LICENSE.txt
***

## Overview

This skill is responsible for designing and implementing integrations with third-party services and internal microservices in a way that isolates failures and preserves good UX. It owns client libraries, contract management, retries, and sync semantics. Success means external dependencies enhance the product without compromising stability, performance, or user trust.

## When to Use This Skill

- When integrating payment processors, messaging platforms, analytics, or identity providers.
- When calling internal microservices or shared APIs from the main application.
- When updating or migrating existing integrations to new versions or providers.
- When repeated outages or latency from external services impact UX or reliability.
- When implementing webhooks, event subscriptions, or data synchronizations.
- When handling high-risk operations (billing, legal documents) involving third-party APIs.
- When designing how failures and timeouts are surfaced to the user in the UI.
- When adding background jobs or batch processes that depend on external services.
- When reviewing or writing client libraries or SDK wrappers around external APIs.
- When compliance requirements dictate how data can be shared with or from third parties.
- When responding to vendor deprecations, contract changes, or new capabilities.
- When debugging cross-service issues that span logs, traces, and systems.


## Ownership and Boundaries

- Owns integration patterns, client abstractions, and error handling for external and internal services.
- Owns defining how external failures are translated into user-visible states and retries.
- Owns idempotency strategies, request deduplication, and at-least/at-most-once semantics.
- Collaborates with backend-api-data on where integration logic should live (service boundaries).
- Collaborates with frontend-ui-ux to design UX for pending, failed, and retried operations.
- Collaborates with security-compliance on data sharing, token handling, and scopes.
- Does not own the external service behavior; it adapts to provider contracts and SLAs.
- Does not bypass core domain models or invariants to "fit" an integration shortcut.
- Preserves existing, stable integration contracts unless deprecations or issues demand change.
- Requests approval before switching providers, changing integration models, or exposing new data externally.


## Core Responsibilities

- Evaluate provider APIs, SLAs, and docs to understand capabilities and limitations.
- Design integration boundaries and data mappings that align with domain models and UX needs.
- Implement robust client libraries or wrappers with proper timeouts, retries, and backoff strategies.
- Implement idempotent endpoints or job handlers for operations that may be retried.
- Handle webhooks and callbacks securely, verifying signatures and authenticity.
- Normalize and validate data from external services before persisting or exposing it.
- Log and monitor integration calls, errors, and latency to track reliability and performance.
- Ensure integration errors are surfaced to users as clear, actionable messages where relevant.
- Implement fallbacks or degraded modes when external services are unavailable.
- Manage configuration, credentials, and environment-specific endpoints via secure mechanisms.
- Provide test doubles, sandboxes, and contract tests to validate integration behavior.
- Document integration flows, dependencies, and operational considerations.


## Step-by-Step Workflow

1. Clarify the product and UX requirements for the integration, including failure behavior and acceptable latency.
2. Review provider docs, sample code, and existing internal integrations for patterns to reuse.
3. Design the integration architecture: where clients live, how data flows, and what contracts look like.
4. Implement client wrappers with standardized error mapping, timeouts, and retry logic.
5. Integrate with backend and, if necessary, frontend, ensuring UX supports pending, success, and failure modes.
6. Configure secure credentials and environment-specific settings via devops-cicd.
7. Write tests (unit, integration, contract) using provider sandboxes or mocks where appropriate.
8. Deploy to non-production environments and validate behavior under realistic conditions (including failures).
9. Monitor logs and metrics for integration calls, adjusting timeouts, retries, and error handling.
10. Document the integration, including how to debug, rotate keys, and handle provider changes.

## Best Practices and Heuristics

- Treat external services as unreliable; design for failures, latency spikes, and timeouts from day one.
- Use timeouts, retry with exponential backoff, and circuit breakers to protect core systems.
- Prefer asynchronous patterns for long-running or bulk operations; update UX accordingly.
- Minimize data coupling; store only what you need and avoid mirroring entire external schemas.
- Validate and sanitize data from external sources, treating it as untrusted input.
- Use provider sandbox environments for tests; avoid hitting production endpoints from CI.
- Implement structured logging with correlation IDs across calls for easier debugging.
- Clearly separate integration concerns from core domain logic to isolate changes.
- Ensure that UI clearly communicates when operations depend on external services and what happens on failure.
- Implement idempotency via keys or tokens for operations like payments or order creation.
- Track provider versions and deprecation timelines; plan migrations early.
- Avoid blocking critical UX on non-critical integrations; degrade gracefully (e.g., missing avatars, secondary analytics).
- Share integration abstractions across services to avoid duplicated, inconsistent client implementations.
- Regularly review integrations for security, compliance, and performance issues.


## Things to Avoid

- Do not call external services directly from scattered locations in the codebase; centralize clients.
- Do not block user flows on non-essential integration calls when they can be deferred.
- Do not ignore backpressure or rate limits; handle them explicitly.
- Do not blindly trust webhook payloads or callback URLs without verification.
- Do not embed provider-specific assumptions deep into domain logic.
- Do not hardcode credentials, endpoints, or tenant IDs in code.
- Do not ignore provider deprecation warnings or error codes.
- Do not rely solely on logs for integrations; add metrics and traces as well.
- Do not surface raw provider error messages directly to users without sanitization.
- Do not fail silently when an integration is down; provide clear signals to operations and, where appropriate, users.


## Quality Bar

- Integrations are reliable under normal conditions and degrade gracefully under failures.
- External service behavior does not cause cascading failures or unacceptable UX degradation.
- Idempotency and consistency guarantees are clear and honored.
- Logs, metrics, and traces make integration issues easy to detect and debug.
- Security and privacy of shared data are enforced according to policies and contracts.
- Documentation clearly explains how integrations work and how to change or troubleshoot them.
- Changes to integrations are rolled out safely with tests and monitoring.
- Users maintain trust, even when external providers have issues, through clear and fair UX.


## Collaboration With Other Skills

- Work with backend-api-data to define where integration logic lives and how data is modeled.
- Coordinate with frontend-ui-ux to represent integration states (pending, failed, retried) in the UI.
- Partner with devops-cicd on environment config, secrets, and monitoring for external calls.
- Collaborate with security-compliance on scopes, tokens, and data minimization.
- Inform debugging-performance of any known latency or reliability characteristics of providers.
- Provide docs-knowledge with up-to-date integration diagrams and operational notes.


## Edge Cases

- Providers that lack proper sandbox environments, requiring careful use of production with safeguards.
- Multi-tenant integrations where different tenants use different providers or credentials.
- Cross-region latency and data residency constraints affecting external calls.
- Provider outages, partial outages, or subtle contract changes that require rapid adaptation.

=== FILE: debugging-performance.md
***
name: debugging-performance
description: Handles root-cause analysis of bugs, rendering issues, and performance bottlenecks across frontend, backend, and integrations. Triggered by incidents, regressions, slow pages, errors, or unexplained behavior.
license: Complete terms in LICENSE.txt
***

## Overview

This skill is responsible for systematically debugging functional issues and performance problems, from UI rendering and hydration to backend latency and integration failures. It owns reproducing issues, narrowing causes, and validating fixes. Success means issues are reliably reproduced, accurately diagnosed, and resolved without collateral regressions.

## When to Use This Skill

- When users report bugs, crashes, or unexpected behavior in UI or APIs.
- When performance metrics (LCP, FID, TTFB, error rates) regress or fail targets.
- When pages show layout shifts, hydration mismatches, or broken responsive behavior.
- When background jobs, queues, or integrations start timing out or backing up.
- When new features introduce increased CPU, memory, or network usage.
- When CI tests fail intermittently or inconsistently, indicating flakiness.
- When logs or monitoring reveal new errors or spikes in specific endpoints or routes.
- When UX polish issues arise (janky animations, delayed feedback, frozen interactions).
- When memory leaks, runaway timers, or event listeners cause degradation over time.
- When cache behavior or CDN issues cause stale or inconsistent UX.
- When database queries or locks slow down critical requests.
- When authentication or session issues cause unpredictable access problems.


## Ownership and Boundaries

- Owns the debugging process: reproduction, hypothesis, instrumentation, and verification.
- Owns cross-layer analysis: client, server, network, data stores, and third-party services.
- Owns adding temporary or permanent instrumentation needed to understand issues.
- Collaborates with frontend-ui-ux, backend-api-data, integrations-services, and devops-cicd for targeted fixes.
- Does not permanently alter architecture; it informs architecture-planning when systemic issues are found.
- Does not leave debug logs, flags, or hacks in production code after resolution.
- Preserves existing working behaviors while fixing specific issues; avoids broad, unnecessary changes.
- Requests clarification when expected behavior is unclear or conflicting across specs and stakeholders.
- Seeks approval before enabling heavy instrumentation or profiling in production environments.
- Avoids speculative rewrites; focuses on measured, evidence-backed interventions.


## Core Responsibilities

- Reproduce issues reliably in appropriate environments (local, staging, production replicas).
- Collect and correlate evidence across logs, traces, metrics, and browser devtools.
- Analyze frontend rendering behavior, including hydration, state updates, and event handling.
- Analyze backend performance, including queries, caching, and request fan-out patterns.
- Analyze integration behavior, including timeouts, retries, and provider-specific errors.
- Formulate and test hypotheses to isolate root causes, not just symptoms.
- Implement or coordinate fixes that are minimal, targeted, and well-tested.
- Validate fixes with benchmarks, profiling, and regression tests where appropriate.
- Document findings, root causes, and mitigations for future reference.
- Identify patterns of recurring issues and propose architectural or process improvements.


## Step-by-Step Workflow

1. Clarify the problem: collect reports, error messages, and expected vs actual behavior from users or logs.
2. Reproduce the issue in a controlled environment, noting steps, conditions, and variability.
3. Inspect logs, metrics, traces, and browser/network tools to narrow down suspicious layers and components.
4. Formulate hypotheses about root causes, prioritizing simple explanations grounded in evidence.
5. Add targeted instrumentation or logging if existing data is insufficient.
6. Test hypotheses by manipulating inputs, environments, or code paths, observing changes in behavior.
7. Implement minimal fixes, ensuring they respect existing patterns, UX expectations, and accessibility.
8. Validate the fix via tests, replayed scenarios, and performance measurements.
9. Remove temporary debug instrumentation and tidy code to production standards.
10. Document the incident, root cause, and fix; update tests and monitoring to catch similar issues early.

## Best Practices and Heuristics

- Start from user symptoms and work inward; avoid jumping straight into random code changes.
- Use binary search on the system (feature flags, deploy diffs, config toggles) to narrow where issues originate.
- Reproduce issues under realistic conditions, including network latency, device constraints, and data volumes.
- Pay attention to hydration warnings, console errors, and layout thrashing in the browser.
- Profile CPU, memory, and network usage on key pages, especially for mobile devices.
- Inspect query plans, indexes, and lock behavior for slow database operations.
- Validate caching layers (browser, CDN, server) to ensure they align with freshness and UX expectations.
- Investigate repeated errors across users and sessions; prioritize widely impacting issues.
- Use tools like flamegraphs, performance timelines, and heap snapshots to understand hotspots.
- Prefer surgical changes (e.g., memoization, batching, index addition) over broad speculative refactors.
- Ensure fixes maintain or improve accessibility and responsive behavior; do not regress UX for speed alone.
- Add regression tests when feasible to codify the behavior that was broken.
- Coordinate deploy timing and monitoring so fixes can be rolled back quickly if misdiagnosed.
- Reflect findings into architecture-planning when recurring patterns indicate deeper design problems.


## Things to Avoid

- Do not fix symptoms (e.g., adding arbitrary timeouts) without understanding root causes.
- Do not disable important checks, logs, or safeguards just to "make errors go away".
- Do not rely solely on local dev environments when issues are environment-specific.
- Do not guess at performance fixes without measuring before and after.
- Do not leave noisy debug logs, console statements, or profiling hooks in production.
- Do not overlap multiple speculative fixes in a single deploy; isolate changes for clear attribution.
- Do not ignore small regressions that are trending worse; address them before they become incidents.
- Do not use hacks that break accessibility, responsiveness, or consistency to hide rendering issues.
- Do not bypass tests or CI steps when debugging; keep feedback loops intact.
- Do not ignore user reports that conflict with metrics; both are signals that need reconciliation.


## Quality Bar

- Issues are reproducible, well-understood, and linked to concrete root causes.
- Fixes are minimal, targeted, and do not introduce new regressions in UX, accessibility, or performance.
- Metrics (performance, error rates) and user feedback confirm that issues are resolved.
- Debugging artifacts (logs, dashboards, docs) are organized for future investigations.
- The system's overall reliability and performance trend improves over time.
- Lessons from incidents are fed back into tests, architecture, and operational practices.
- Stakeholders understand what happened, why, and how it was fixed.
- Debugging processes themselves are efficient and repeatable.


## Collaboration With Other Skills

- Work with frontend-ui-ux to diagnose rendering, interaction, and responsive/layout problems.
- Collaborate with backend-api-data to analyze slow or erroneous endpoints and data flows.
- Coordinate with integrations-services to debug third-party timeouts, errors, or contract mismatches.
- Partner with devops-cicd to access logs, traces, and adjust monitoring or deploy strategies.
- Inform testing-qa so newly discovered failure modes are captured in tests.
- Provide docs-knowledge with incident reports and troubleshooting guides.


## Edge Cases

- Heisenbugs that disappear when debug logging or breakpoints are added.
- Performance regressions only visible under specific tenants, data shapes, or traffic patterns.
- Browser-specific bugs tied to particular versions or platforms.
- Memory leaks or resource exhaustion that only appear over long uptimes.

=== FILE: docs-knowledge.md
***
name: docs-knowledge
description: Manages creation and maintenance of documentation, runbooks, and knowledge structures for the codebase, architecture, components, and user flows. Triggered when documenting features, patterns, decisions, or when onboarding contributors.
license: Complete terms in LICENSE.txt
***

## Overview

This skill is responsible for capturing and organizing knowledge about the system so others can understand, extend, and operate it effectively. It owns architecture docs, component usage guides, runbooks, and decision records that explain how code relates to UX, data, and operations. Success means contributors can quickly find accurate information and make changes without guesswork.

## When to Use This Skill

- When shipping new features, architectures, or integrations that others will depend on.
- When updating or creating design systems, component libraries, or layout frameworks.
- When adding or changing APIs, data models, or background jobs.
- When documenting user flows, edge cases, and accessibility behavior for UI components.
- When writing onboarding guides for new developers or teams.
- When recording architectural decisions, tradeoffs, and migration plans.
- When creating or updating runbooks for incidents, deployments, or maintenance tasks.
- When tests, code, and docs diverge or become inconsistent.
- When users or developers repeatedly ask the same questions about how things work.
- When refactoring legacy areas that need clear before/after explanations.
- When deprecating features, APIs, or components.
- When performing post-incident reviews that need to be captured for future reference.


## Ownership and Boundaries

- Owns structure and content of technical documentation within the repository or associated knowledge base.
- Owns documenting architecture, domain concepts, and how they map to code and UX.
- Owns component docs, including props, usage patterns, responsive and accessibility considerations.
- Owns runbooks and operational docs in collaboration with devops-cicd and debugging-performance.
- Collaborates with architecture-planning to record decision logs and design rationales.
- Collaborates with frontend-ui-ux and backend-api-data to document APIs, flows, and edge cases.
- Does not override product specs; it reflects actual implementation and decisions, highlighting divergences.
- Does not invent behavior; it must be grounded in code, tests, and verified behavior.
- Preserves existing documentation structures where they are working; reorganizes only with clear improvements.
- Requests clarification when behavior is ambiguous or undocumented; resolves inconsistencies before documenting.


## Core Responsibilities

- Create and maintain high-level architecture overviews and diagrams.
- Document domain models, API contracts, and data flows with examples.
- Document UI components, layouts, and design system primitives with usage guidelines.
- Capture UX flows, including loading, empty, error, success, and partial-data states.
- Record accessibility expectations: keyboard behavior, ARIA usage, focus management, and screen reader text.
- Write runbooks for common operational tasks and incident response procedures.
- Maintain decision records (ADRs) that explain major architectural or product choices.
- Keep README and onboarding docs up to date with setup, scripts, and workflows.
- Organize docs into logical sections, with cross-links between architecture, components, and operations.
- Regularly review and update outdated docs, removing or clearly marking obsolete content.
- Encourage documentation standards (templates, style guides) that others can follow.
- Store documentation close to code where possible to reduce drift.


## Step-by-Step Workflow

1. Identify the feature, system, or process that needs documentation and its target audience.
2. Inspect the current implementation, tests, and existing docs to understand the truth and gaps.
3. Outline the document structure: overview, key concepts, flows, edge cases, and references.
4. Write clear, concise explanations using domain language and concrete examples.
5. Add diagrams or sequence sketches where architectures or flows are complex.
6. Document UX states, accessibility behavior, and responsive considerations explicitly.
7. Cross-link related docs (components to API references, runbooks to services).
8. Review docs for accuracy against code and tests; update as implementations change.
9. Share docs with stakeholders and incorporate feedback or corrections.
10. Periodically audit and prune stale docs, updating indexes and navigation.

## Best Practices and Heuristics

- Write for future maintainers: assume the reader is competent but unfamiliar with this specific system.
- Prefer small, focused docs per topic over monolithic documents that are hard to navigate.
- Use consistent templates for architecture overviews, component docs, and runbooks.
- Include concrete file paths, commands, and examples to ground explanations.
- Document how features behave on different devices, viewports, and input methods.
- Capture the rationale behind decisions, not just the final state, to aid future changes.
- Keep diagrams simple and close to the code (in-repo diagrams or text-based formats).
- Explicitly document invariants, constraints, and things that must not change without careful planning.
- Note tradeoffs and limitations, including known issues and technical debt areas.
- Keep language inclusive, clear, and free of unnecessary jargon.
- Ensure documentation reflects accessibility requirements and how they are met.
- Highlight how to run and interpret tests related to the documented area.
- Integrate links to monitoring dashboards, logs, and tools where relevant for operations.
- Encourage contributions to docs by making them easy to edit and review.


## Things to Avoid

- Do not copy-paste large code blocks without explanation; reference files and summarize behavior.
- Do not document speculative features or future plans as if they were implemented.
- Do not allow docs to drift from code; outdated docs must be updated, archived, or removed.
- Do not bury critical information in long prose; use headings, lists, and tables for clarity.
- Do not use ambiguous terms or internal-only jargon without definitions.
- Do not duplicate the same content across many files; centralize and link where appropriate.
- Do not ignore UX, accessibility, or responsive aspects; they are part of the product, not optional extras.
- Do not make docs dependent on proprietary tools or formats that others cannot access.
- Do not rely on tribal knowledge; capture operational "gotchas" explicitly.
- Do not treat documentation as a one-time task; maintain it as code and architecture evolve.


## Quality Bar

- Documentation is accurate, current, and consistent with the code and tests.
- Contributors can onboard and make meaningful changes with minimal synchronous help.
- Architecture, APIs, and components are understandable with clear examples and rationales.
- UX flows, accessibility behavior, and responsive considerations are clearly described.
- Runbooks enable non-authors to handle incidents and routine operations confidently.
- Decision records clarify why structures exist and how to safely evolve them.
- Documentation is discoverable and logically organized, with minimal duplication.
- Updates to code and architecture are accompanied by corresponding doc changes.


## Collaboration With Other Skills

- Work with codebase-understanding and architecture-planning to keep high-level overviews current.
- Collaborate with frontend-ui-ux to document components, design systems, and UX flows.
- Coordinate with backend-api-data to maintain accurate API and data model references.
- Partner with devops-cicd and debugging-performance on runbooks and troubleshooting guides.
- Align with security-compliance on documenting security models, auth flows, and incident procedures.
- Support testing-qa by documenting test strategy and how to interpret test outputs.


## Edge Cases

- Legacy systems with sparse or conflicting documentation that require careful reconstruction.
- Regulated environments where documentation itself has compliance requirements.
- Multi-tenant or white-label systems where docs must cover variations without duplication.
- Rapidly changing experimental features where docs must strike a balance between agility and clarity.

