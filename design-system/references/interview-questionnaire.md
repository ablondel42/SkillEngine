# Interview Guide

Quick reference for conducting design system interviews. The goal is to
understand the user's needs before writing any code.

---

## The 5 Essential Questions

Ask these in a SINGLE message. Keep it concise.

### 1. App Concept & Users
**Ask:** What does the application do and who will use it?

**Examples:**
- "B2B SaaS dashboard for enterprise teams managing projects"
- "Consumer fitness app targeting millennials"
- "E-commerce storefront for luxury skincare brand"

**Listen for:** Domain, user type, core purpose

---

### 2. Tone/Mood
**Ask:** What feeling should the design convey?

**Options to offer:**
- **Professional** - Trustworthy, reliable, serious
- **Energetic** - Modern, motivating, bold
- **Premium** - Elegant, minimalist, luxury
- **Friendly** - Warm, approachable, playful

**Listen for:** 2-3 adjectives describing the desired feel

---

### 3. Tech Stack (CRITICAL)
**Ask:** What frontend framework and styling approach?

**Examples:**
- "Next.js + Tailwind + TypeScript"
- "Vue 3 + SCSS"
- "React + styled-components"

**Listen for:** Framework, styling approach, TypeScript vs JavaScript

---

### 4. Key Screens/Features
**Ask:** What are the main pages or features?

**Examples:**
- "Dashboard, product pages, checkout flow"
- "Home dashboard, workout tracker, progress charts, social feed"
- "Homepage, product listing, cart, account dashboard"

**Listen for:** 3-5 main screens or features

---

### 5. Dark Mode
**Ask:** Should the design system support dark mode?

**Default:** Yes (unless specified otherwise)

---

## Accessibility

**Default:** WCAG 2.1 AA

Only ask if user has specific requirements beyond this.

---

## Before You Start Coding

Make sure you:
- [ ] Understand the domain well enough to name 5-10 domain components
- [ ] Know which screens to build as examples
- [ ] Can describe the tone in 2-3 words
- [ ] Have crystal-clear tech stack details

**If anything is unclear, ask follow-up questions.** It's better to clarify
now than to rebuild later.

---

## Example Interview Message

```
I'll help you create a comprehensive design system! Before I start, I need 
to understand your requirements. Please answer these 5 questions:

1. **App concept & users**: What does the application do and who will use it?

2. **Tone/mood**: What feeling should the design convey? (e.g., professional, 
   energetic, premium, minimalist)

3. **Tech stack**: What frontend framework and styling approach? 
   (e.g., "Next.js + Tailwind + TypeScript")

4. **Key screens/features**: What are the main pages or features?

5. **Dark mode**: Should the design system support dark mode?

(Accessibility defaults to WCAG 2.1 AA)
```

---

## Tips

1. **Ask all 5 questions in ONE message** - Don't drag out the interview
2. **Keep it conversational** - Use natural language, not a rigid form
3. **Provide examples** - Help users understand what you're asking
4. **Wait for complete answers** - Don't proceed until you have all 5
5. **Document assumptions** - If user is vague, note your interpretation

---

## Common Follow-ups

**If user is vague on tech stack:**
> "Got it. To clarify: are you using React, Next.js, Vue, or something else? 
> And for styling: Tailwind, CSS-in-JS, SCSS, or vanilla CSS?"

**If user is vague on tone:**
> "Should the design feel more professional and trustworthy, or energetic 
> and modern? Or perhaps premium and minimalist?"

**If user doesn't mention dark mode:**
> "Should I include dark mode support? (This is usually recommended for 
> modern apps)"
