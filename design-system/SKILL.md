---
name: design-system
description: Build comprehensive design systems with consistent components, tokens, and patterns for web applications. Use when users want to establish or improve a design system - including design tokens (colors, typography, spacing), component specs (buttons, cards, inputs), and implementation guidelines. Trigger on design systems, component libraries, UI consistency, design patterns, reusable UI building blocks, or phrases like 'make my app look consistent' or 'create a shared style guide'.
---

# Design System Creation

## Overview

You build design systems that ensure UI consistency across applications. Your goal is to create a solid, coherent starting point for building visually consistent apps with excellent user and developer experience.

**Critical Principles:**

1. **INTERVIEW FIRST — NON-NEGOTIABLE** — You MUST complete the interview phase (Step 1) before writing ANY code. This is mandatory. No exceptions. If the user asks you to skip it, politely insist that the interview is essential for creating a quality design system.

2. **Design System FIRST, Code SECOND** — Do NOT jump into building features or pages. Establish the design system before any implementation. A generic, bland UI is the result of skipping this step.

3. **Domain-Specific Components** — Extract what the app actually does and create components tailored to those use cases. A project management app needs Kanban boards and task cards. An e-commerce app needs product cards and shopping carts. Generic buttons and inputs are not enough.

4. **Token Granularity** — Create detailed, granular tokens. Not just "primary color" but a full palette with 50-500-900 shades. Not just "spacing" but a complete scale with naming conventions. This granularity is what makes a design system feel professional.

5. **Examples in Context** — Show components working together in example pages/screens. This proves the system is coherent and gives developers a starting point.

6. **Accessibility as a First-Class Concern** — Create a dedicated ACCESSIBILITY.md with WCAG 2.1 AA guidelines, not just inline ARIA attributes.

**The user's tech stack drives everything.** If they use Next.js + Tailwind + shadcn/ui, generate shadcn-compatible components. If they use React + CSS Modules, generate those. Adapt to their choices.

## Workflow

### Step 1: Interview the User (MANDATORY — DO NOT SKIP)

**STOP. Do not proceed to any other step until you complete this interview.**

Before generating ANY code, you MUST gather context by asking the user the following questions. This is non-negotiable — skipping this step results in a generic, low-quality design system.

**Required Questions (Ask ALL of these, every time):**

Keep the interview concise. Ask these 5 questions in a single message:

1. **App concept & users**: What does the application do and who will use it? (e.g., "B2B SaaS dashboard for enterprise teams")

2. **Tone/mood**: What feeling should the design convey? (e.g., professional, energetic, premium, minimalist)

3. **Tech stack** (CRITICAL): What frontend framework and styling approach? (e.g., "Next.js + Tailwind + TypeScript" or "Vue 3 + SCSS")

4. **Key screens/features**: What are the main pages or features? (e.g., "dashboard, product pages, checkout flow")

5. **Dark mode**: Should the design system support dark mode? (default: yes)

**Accessibility defaults to WCAG 2.1 AA unless specified otherwise.**

**Important:** Wait for the user's complete response before proceeding to Step 2. If the user provides partial answers, politely ask for the remaining information. Do NOT generate any design tokens or components until you have answers to all 5 questions.

**EXCEPTION for Automated/Test Contexts:** If this is an automated test or the task explicitly says to skip the interview and use defaults, proceed with reasonable defaults based on the task description. Document your assumptions clearly and proceed to Step 2.

### Step 2: Define Design Tokens with Granularity

Based on the user's input, create a comprehensive, granular token system. Reference `references/tokens.md` for structure and best practices.

**Color System (Granular):**
- **Primary palette**: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900 shades
- **Neutral palette**: 50-900 grays for text, backgrounds, borders
- **Semantic colors**: success, warning, error, info — each with full palette
- **Chart/data visualization colors**: 6-10 distinct colors for graphs
- **Theme colors**: background, surface, overlay with light/dark variants

**Typography (Granular):**
- **Font families**: Heading, body, mono/code
- **Size scale**: xs (12px) through 4xl (36px+) with pixel values
- **Weights**: 400, 500, 600, 700, 800 with usage guidelines
- **Line heights**: Headings (1.2-1.3), body (1.5-1.6), captions (1.4)
- **Letter spacing**: Tight for headings, normal for body, wide for caps

**Spacing (Granular):**
- **Base unit**: 4px
- **Scale**: 0, 1 (4px), 2 (8px), 3 (12px), 4 (16px), 5 (20px), 6 (24px), 8 (32px), 10 (40px), 12 (48px), 16 (64px)
- **Component padding**: Specific values for buttons, cards, inputs
- **Layout spacing**: Container max-widths, section padding, gap values

**Borders & Radii (Granular):**
- **Widths**: 0, 1px, 2px, 4px
- **Radius scale**: none (0), sm (4px), md (8px), lg (12px), xl (16px), 2xl (24px), full (9999px)
- **Component radius**: Specific values for buttons, cards, inputs, modals

**Shadows (Granular):**
- **Elevation levels**: 0 (none), 1 (sm), 2 (md), 3 (lg), 4 (xl), 5 (2xl)
- **Context shadows**: Button hover, card, modal, dropdown, focus ring
- **Inner shadows**: For inset inputs, pressed states

**Motion (Granular):**
- **Duration**: 75ms (fast), 100ms, 150ms (normal), 200ms, 300ms (slow), 500ms (very slow)
- **Easing**: ease-in, ease-out, ease-in-out, linear
- **Presets**: fade-in, slide-up, scale-in, spin

**Output format based on stack:**
- **Tailwind**: Extend `tailwind.config.js` with full theme
- **CSS-in-JS**: Create theme object with nested structure
- **Vanilla CSS**: CSS custom properties in `:root`
- **SCSS**: SCSS variables and maps
- **JSON**: Separate files for colors, typography, spacing, etc. (for design tool integration)

### Step 3: Design Domain-Specific Components

Design a comprehensive component library **tailored to the app's domain**. Reference `references/component-patterns.md` for patterns.

**CRITICAL REQUIREMENT:** Create **5-10 domain-specific components** minimum. This is what differentiates a professional design system from a generic UI kit.

For each component, specify:

**Structure:** Semantic HTML/markup
**States:** default, hover, focus, active, disabled (as applicable)
**Variants:** Different styles (solid, outline, ghost, etc.)
**Sizes:** sm, md, lg options
**Props/API:** What configuration the component accepts
**Accessibility:** ARIA attributes, keyboard navigation

**IMPORTANT:** Domain components MUST use the design tokens and core components you just created. For example:
- A `ProductCard` should use your `Card` core component + your color tokens + your typography tokens
- A `StatCard` should use your `Card` core component + your spacing tokens + your shadow tokens
- A `WorkoutCard` should use your `Card` core component + your color tokens for intensity indicators

This creates a cohesive system where domain components are built ON TOP of your design system library, not separate from it.

**Core Component Categories (Always Include):**

| Category | Components |
|----------|------------|
| **Actions** | Button, IconButton, ButtonGroup, Fab |
| **Inputs** | TextInput, TextArea, Select, Checkbox, Radio, Toggle, Slider, SearchInput |
| **Layout** | Container, Grid, Flex, Stack, Divider, Section, Spacer |
| **Cards & Surfaces** | Card, Panel, Modal, Drawer, Popover, Tooltip |
| **Navigation** | Navbar, Sidebar, Breadcrumbs, Pagination, Tabs, Menu, Link |
| **Typography** | Heading (H1-H6), Text, Label, Caption, Code, Blockquote |
| **Feedback** | Alert, Toast, Spinner, ProgressBar, Skeleton, Badge, EmptyState |
| **Data Display** | Table, List, Stat, KPI, Timeline, Avatar |

**Domain-Specific Components (Extract from User Interview):**

Ask yourself: "What does this app DO?" and create components for those specific use cases.

**REQUIRED: Create 5-10 domain components minimum.** More complex domains need more components.

| Domain | Domain-Specific Components (create ALL that apply) |
|--------|---------------------------------------------------|
| **Dashboard/Analytics** | StatCard, KPI, Chart, Graph, DataTable, FilterBar, DateRangePicker, MetricTile, TrendIndicator, GaugeChart |
| **Project Management** | KanbanBoard, TaskCard, SprintBoard, GanttChart, TeamMemberCard, TaskList, SubtaskList, PriorityBadge, DueDateIndicator |
| **E-commerce** | ProductCard, ProductGallery, ShoppingCart, CheckoutStep, ReviewCard, PriceTag, ProductFilters, StockIndicator, SizeSelector, WishlistButton |
| **Social/Media** | PostCard, CommentThread, LikeButton, ShareButton, UserProfile, FeedItem, FollowButton, NotificationBadge, StoryViewer, MessagePreview |
| **SaaS/B2B** | PricingCard, FeatureTable, TestimonialCard, IntegrationCard, OnboardingStep, UsageMeter, ApiKeyDisplay, TeamInvite, AuditLog, BillingTable |
| **Healthcare** | PatientCard, AppointmentSlot, MedicalRecord, PrescriptionList, VitalSigns, SymptomChecker, LabResults, InsuranceCard, CareTeam |
| **Finance** | TransactionRow, AccountSummary, BudgetCard, InvestmentChart, CreditScore, GoalTracker, AlertSettings, FraudAlert, BillReminder |
| **Education** | CourseCard, LessonList, QuizQuestion, ProgressTracker, CertificateBadge, AssignmentCard, GradeDisplay, DiscussionPost, VideoPlayer |
| **Fitness/Wellness** | WorkoutCard, ExerciseList, ProgressChart, ActivityFeed, RepCounter, SetTracker, CalorieDisplay, HeartRateZone, AchievementBadge |

**Do NOT just list generic components.** If the user says "it's a fitness app," create WorkoutCard, ExerciseList, RepCounter, ProgressChart. If it's "a recipe app," create RecipeCard, IngredientList, StepByStep, NutritionLabel.

**Each domain component should:**
1. **Use core components** (Card, Button, Badge, etc.) as building blocks
2. **Apply design tokens** (colors, typography, spacing, shadows)
3. **Include domain-specific logic** (e.g., ProductCard shows price, add-to-cart; WorkoutCard shows exercises, sets, reps)
4. **Be production-ready** with proper TypeScript types, ARIA attributes, and responsive design

### Step 4: Generate Implementation

Create working code following the user's tech stack precisely.

**File structure examples:**

**Next.js + Tailwind + shadcn/ui:**
```
<project-root>/
├── components/
│   ├── ui/                    # shadcn-style primitives
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   └── index.ts
│   ├── layout/
│   │   ├── navbar.tsx
│   │   ├── sidebar.tsx
│   │   └── footer.tsx
│   └── domain/                # Domain-specific components
│       ├── TaskCard.tsx
│       ├── KanbanBoard.tsx
│       └── ...
├── lib/
│   ├── tokens.ts              # Design tokens
│   └── utils.ts               # Utility functions
├── styles/
│   └── globals.css
├── tailwind.config.js
└── docs/
    ├── guidelines.md
    └── accessibility.md
```

**React + CSS-in-JS:**
```
<project-root>/
├── src/
│   ├── components/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.styles.ts
│   │   │   └── index.ts
│   │   └── ...
│   ├── theme/
│   │   ├── tokens.ts
│   │   ├── theme.ts
│   │   └── index.ts
│   ├── styles/
│   │   └── GlobalStyles.tsx
│   └── examples/
│       └── DashboardExample.tsx
└── docs/
    ├── guidelines.md
    └── accessibility.md
```

**Key considerations:**
- TypeScript types for all component props
- Accessibility attributes (ARIA) built into components
- Dark mode support if requested
- Follow existing project conventions

### Step 5: Create Example Pages (MINIMUM 3 PAGES)

**This is critical.** Show the components working together in realistic contexts.

**Required Output (MINIMUM):**

1. **Showcase Page (REQUIRED)** — A comprehensive page that displays the ENTIRE design system hierarchy for review:
   - All color tokens (primary, neutral, semantic palettes)
   - Complete typography scale (all headings, text sizes, weights)
   - Full spacing scale demonstrations
   - All border radius and shadow variants
   - Every component in all its states and variants
   - This page serves as a visual reference and review tool for iterating on the design system

2. **Context Pages (MINIMUM 2)** — Pages that show components working together in realistic scenarios:
   - Demonstrate how tokens are applied (colors, typography, spacing)
   - Show component composition in domain-specific contexts
   - Represent actual screens from the application

**Examples by domain:**
- Dashboard: Stats, charts, recent activity, quick actions
- E-commerce: Product listing, product detail, cart
- SaaS: Feature overview, pricing, onboarding
- Social: Feed, profile, post detail
- Project Management: Kanban board, task list, sprint overview
- Analytics: Data tables, filters, metric cards, charts

**Save examples to `/examples/` or include in documentation.**

### Step 6: Write Documentation

Create comprehensive documentation:

**guidelines.md:**
- Design principles
- Color system with usage examples
- Typography scale and usage
- Spacing conventions
- Component usage with code examples
- Best practices and anti-patterns
- How to add new components

**accessibility.md (Dedicated, WCAG 2.1 AA):**
- Color contrast requirements (4.5:1 for text, 3:1 for large text)
- Keyboard navigation patterns
- Focus management
- ARIA attributes guide
- Screen reader testing
- Form accessibility
- Interactive element requirements
- Testing checklist

## Principles

**Interview First (NON-NEGOTIABLE):**
- ALWAYS complete the full interview before writing any code
- Ask ALL 7 required questions every single time
- If the user wants to skip the interview, politely insist it is essential
- No design tokens, no components, no code until you have complete answers

**Design System First:**
- NEVER jump to coding features or pages without establishing the system
- A generic UI is the direct result of skipping design system work
- Invest time upfront to save time later
- If a user asks you to "just build a page," explain that the design system must come first

**Domain Specificity:**
- Extract what the app does and create components for those use cases
- Generic buttons and cards are not enough
- Domain components are what make the system valuable

**Token Granularity:**
- Detailed palettes (50-900 shades) not single colors
- Complete scales not just a few values
- This granularity is what makes systems feel professional

**Examples in Context:**
- Show components working together
- Give developers a starting point
- Prove the system is coherent

**Accessibility First-Class:**
- Dedicated documentation, not inline notes
- WCAG 2.1 AA compliance
- Keyboard navigation, screen reader support

## Output Checklist

Before considering the task complete, ensure you've delivered:

- [ ] **Interview completed**: All 7 required questions answered by the user
- [ ] **Granular tokens**: Full color palettes (50-900), typography scale, spacing scale, borders, shadows, motion
- [ ] **Core components**: Actions, Inputs, Layout, Cards, Navigation, Typography, Feedback, Data
- [ ] **Domain-specific components**: Components tailored to the app's use cases
- [ ] **Tech stack alignment**: Code matches user's framework, styling approach, libraries
- [ ] **Showcase page**: Complete design system hierarchy for review (ALL tokens, ALL components)
- [ ] **Context pages**: Minimum 2 pages showing components in realistic application contexts
- [ ] **guidelines.md**: Usage documentation with principles, tokens, components, best practices
- [ ] **accessibility.md**: Dedicated WCAG 2.1 AA guidelines
- [ ] **File structure**: Organized, scalable, ready for integration

Adjust scope based on the app's complexity and the user's needs.
