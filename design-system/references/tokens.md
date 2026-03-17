# Color System

## Semantic Colors

| Token | Usage |
|-------|-------|
| `primary` | Main brand color, primary buttons, links |
| `secondary` | Secondary actions, accents |
| `success` | Success states, positive feedback |
| `warning` | Warnings, caution states |
| `error` | Errors, destructive actions, alerts |
| `info` | Informational messages |

## Color Roles

| Role | Usage |
|------|-------|
| `background` | Page background, main container |
| `surface` | Cards, modals, elevated elements |
| `text-primary` | Main content text |
| `text-secondary` | Secondary text, metadata |
| `border` | Dividers, input borders |
| `overlay` | Modal/backdrop overlays |

## Best Practices

- Limit palette to 6-8 colors plus neutrals
- Test color contrast for WCAG AA compliance
- Use semantic names, not descriptive (e.g., "primary" not "blue")
- Define hover states as color variations, not new colors

---

# Typography

## Font Families

```
heading: 'Inter Display', 'Inter', sans-serif
body: 'Inter', system-ui, sans-serif
mono: 'JetBrains Mono', 'Fira Code', monospace
```

## Scale

| Size | Pixels | Usage |
|------|--------|-------|
| xs | 12px | Captions, helper text |
| sm | 14px | Body text, labels |
| base | 16px | Default body text |
| lg | 18px | Prominent body text |
| xl | 20px | Subheadings |
| 2xl | 24px | Headings |
| 3xl | 30px | Page headers |
| 4xl | 36px | Hero headers |

## Weights

| Weight | Usage |
|--------|-------|
| 400 | Body text, regular |
| 500 | Labels, emphasize |
| 600 | Subheadings |
| 700 | Headings |
| 800 | Strong emphasis |

## Line Heights

| Text type | Line height |
|-----------|-------------|
| Headings | 1.2-1.3 |
| Body | 1.5-1.6 |
| Captions | 1.4 |

---

# Spacing

## Scale (4px base)

| Token | Pixels | Usage |
|-------|--------|-------|
| 0 | 0 | No spacing |
| 1 | 4px | Tight spacing, tight gaps |
| 2 | 8px | Small spacing |
| 3 | 12px | Small-medium spacing |
| 4 | 16px | Base spacing, padding |
| 5 | 20px | Medium spacing |
| 6 | 24px | Medium-large spacing |
| 8 | 32px | Large spacing |
| 10 | 40px | Section spacing |
| 12 | 48px | Large section spacing |
| 16 | 64px | Hero spacing |

## Block Spacing (Vertical)

Use spacing scale for vertical rhythm between blocks.

## Padding Guidelines

- Buttons: `8px 16px` (sm), `12px 24px` (md), `16px 32px` (lg)
- Cards: `24px` padding
- Containers: `16px` (mobile), `24px` (desktop) horizontal padding

---

# Borders

## Widths

| Width | Usage |
|-------|-------|
| 1px | Inputs, dividers, standard borders |
| 2px | Emphasized borders, active states |
| 0 | No border |

## Radius (Border Radius)

| Size | Pixels | Usage |
|------|--------|-------|
| sm | 4px | Small buttons, tags |
| md | 8px | Cards, inputs |
| lg | 12px | Modals, popovers |
| xl | 16px | Large modals, sheets |
| full | 9999px | Pills, circular |

## Shadow Levels

| Level | Usage |
|-------|-------|
| 0 | No shadow |
| 1 | Subtle lift (buttons on hover) |
| 2 | Cards |
| 3 | Modals, popovers |
| 4 | Dropdowns, tooltips |

---

# Components Reference

## Button

**States**: default, hover, active, focus, disabled

**Variants**: solid, outline, ghost, text

**Sizes**: sm, md, lg

## Card

**States**: default, hover, active

**Variants**: elevated, flat, interactive

**Content**: header, body, footer

## Input

**States**: default, focus, error, disabled, success

**Variants**: outlined, filled, underlined

**Sizes**: sm, md, lg

## Typography

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 36px | 700 | 1.2 |
| H2 | 28px | 700 | 1.3 |
| H3 | 22px | 600 | 1.3 |
| H4 | 18px | 600 | 1.4 |
| Body | 16px | 400 | 1.5 |
| Small | 14px | 400 | 1.5 |
| Caption | 12px | 400 | 1.4 |
