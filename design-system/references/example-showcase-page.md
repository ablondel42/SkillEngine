# Showcase Page Guide

A showcase page displays your entire design system in one place. Think of it
as a visual catalog for review and iteration.

---

## What to Include

**Must-have sections:**

1. **Colors** - All palettes (primary, neutral, semantic, theme)
2. **Typography** - Font sizes, weights, headings
3. **Spacing** - The full spacing scale
4. **Borders & Shadows** - Radius values, shadow levels
5. **Components** - All variants, states, with names and descriptions
6. **Layout** - Consistent section spacing and grouping
7. **Examples** - Components composed together

---

## Simple Structure

```
ShowcasePage
├── Hero (title + theme toggle)
├── Colors
│   ├── Primary (50-900 swatches with labels)
│   ├── Semantic (success, warning, error, info)
│   └── Theme (background, surface, foreground, border)
├── Typography
│   ├── Font sizes (xs through 4xl with usage notes)
│   ├── Font weights
│   └── Headings (H1-H4)
├── Spacing
│   └── Scale visualization (0 through 16)
├── Borders & Radius
├── Shadows
├── Components (organized by category)
│   ├── Actions
│   │   ├── Button (name + description + all variants/sizes/states)
│   │   └── IconButton (name + description + variants)
│   ├── Inputs
│   │   ├── Input (name + description + states)
│   │   ├── Select
│   │   └── Checkbox/Radio
│   ├── Layout
│   │   ├── Card
│   │   ├── Container
│   │   └── Divider
│   ├── Feedback
│   │   ├── Alert (name + description + variants)
│   │   ├── Badge
│   │   └── Spinner
│   └── Domain Components
│       └── (e.g., StatCard, TaskCard - with descriptions)
└── Examples (component compositions)
```

---

## Component Cards

Each component should display:

```
┌─────────────────────────────────────┐
│ Component Name                      │
│ Brief description of when to use    │
├─────────────────────────────────────┤
│                                     │
│   [Visual display of component]     │
│   [All variants side by side]       │
│   [All states if applicable]        │
│                                     │
└─────────────────────────────────────┘
```

**Example:**
```
┌─────────────────────────────────────┐
│ Button                              │
│ Triggers actions or navigation      │
├─────────────────────────────────────┤
│  [Primary] [Secondary] [Outline]    │
│  [Ghost]   [Danger]                 │
│                                     │
│  [Small] [Medium] [Large]           │
│                                     │
│  [Default] [Hover] [Disabled]       │
└─────────────────────────────────────┘
```

---

## Layout & Spacing

**Use consistent section spacing:**

```css
/* Between major sections */
--section-spacing: var(--spacing-16); /* 64px */

/* Between component categories */
--category-spacing: var(--spacing-12); /* 48px */

/* Between component cards */
--card-spacing: var(--spacing-8); /* 32px */
```

**Container structure:**
```
Page Container (max-width: 1200px, centered)
├── Section (padding: 64px vertical)
│   ├── Section Title (margin-bottom: 32px)
│   └── Content Grid (gap: 32px)
│       ├── Component Card (padding: 24px)
│       └── Component Card
```

**Tips:**
- Use the same gap consistently within each section type
- Add visual dividers between major sections
- Keep component cards aligned to a grid

---

## Tips by Section

**For colors:**
- Show swatches with labels (shade name + variable)
- Group related colors together
- Include both light and dark mode if applicable

**For typography:**
- Show actual text samples, not just "Aa"
- Include usage notes (e.g., "H1 for page titles")

**For components:**
- Always show component name as a heading
- Add a one-line description below the name
- Show all variants side by side for comparison
- Include disabled and loading states where relevant
- Group by category (Actions, Inputs, Layout, Feedback)

**For layout components:**
- Show Card with different content scenarios
- Show Container with visible boundaries
- Show Divider in context

**For examples:**
- Build realistic mini-scenes (a form card, a stats row)
- Show how components work together
- Use consistent internal padding (e.g., 24px)

---

## Quick Example (React)

```tsx
// Component card wrapper - consistent styling
function ComponentCard({ name, description, children }) {
  return (
    <div className="component-card">
      <div className="component-header">
        <h3 className="component-name">{name}</h3>
        <p className="component-description">{description}</p>
      </div>
      <div className="component-preview">
        {children}
      </div>
    </div>
  )
}

// Usage in showcase
<ComponentCard
  name="Button"
  description="Triggers actions or navigation"
>
  <div className="flex gap-4">
    <Button variant="primary">Primary</Button>
    <Button variant="secondary">Secondary</Button>
    <Button variant="outline">Outline</Button>
  </div>
</ComponentCard>
```

---

## Keep It Useful

The showcase page should be:
- **Scannable** - Clear sections, consistent layout
- **Labeled** - Every component has a name and description
- **Complete** - All tokens and components visible
- **Consistent** - Same spacing throughout
- **Living** - Update it as the design system evolves

Don't over-engineer it. A simple, organized page is better than a fancy
incomplete one.
