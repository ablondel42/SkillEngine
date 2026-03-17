# Interview Guide

Quick reference for conducting design system interviews. The goal is to
understand the user's needs before writing any code.

---

## The 7 Essential Questions

Ask these in order. If answers are vague, offer suggestions based on their
domain.

### 1. App Concept

**Ask:** What does the application do? What problem does it solve?

**Listen for:** Clear problem statement, specific user actions, domain vocabulary

**If vague, suggest:**
> "For [domain] apps, typical features include: [list 3-4]. Which match your vision?"

---

### 2. Target Users

**Ask:** Who will use this app?

**Listen for:** Technical level, primary device, usage context

**If vague, suggest:**
> "For [domain], I'd design for: moderate tech skills, mixed desktop/mobile,
> short daily sessions. Does this match?"

---

### 3. Tone & Mood

**Ask:** What feeling should the design convey? (3 adjectives)

**Options to offer:**
- **Professional** - Trustworthy, reliable, serious
- **Modern** - Clean, innovative, forward
- **Friendly** - Warm, approachable, playful
- **Bold** - Confident, striking, memorable

---

### 4. Tech Stack (Critical)

**Ask:** Framework, styling approach, component libraries, TypeScript?

**If unsure, recommend:**
- **Startups:** Next.js + Tailwind + shadcn/ui + TypeScript
- **Enterprise:** React + CSS Modules + Radix UI + TypeScript
- **Vue shops:** Vue 3 + SCSS + TypeScript

---

### 5. Key Screens

**Ask:** What are the main pages or features?

**If vague, suggest common screens for their domain:**
- **Dashboard:** KPI cards, charts, data tables, filters
- **E-commerce:** Product list, detail, cart, checkout
- **SaaS:** Landing, pricing, onboarding, dashboard

---

### 6. Accessibility

**Ask:** Any specific WCAG level? (Default: 2.1 AA)

**If unsure:**
> "WCAG 2.1 AA is standard: 4.5:1 contrast, keyboard navigation, screen
> reader support. Should we target this?"

---

### 7. Dark Mode

**Ask:** Should the design system support dark mode?

**Guidance:**
- **Developer tools:** Essential
- **Media/entertainment:** Important
- **Enterprise/B2B:** Optional
- **Healthcare:** Often disabled for clinical accuracy

---

## Before You Start Coding

Make sure you:
- Understand the domain well enough to name 5-10 domain components
- Know which screens to build as examples
- Can describe the tone in 2-3 words
- Have crystal-clear tech stack details

**If anything is unclear, ask follow-up questions.** It's better to clarify
now than to rebuild later.
