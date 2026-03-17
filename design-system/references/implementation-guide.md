# Implementation Guide

Stack-agnostic patterns for implementing design systems. Adapt these to your
tech stack.

---

## File Structure

Organize your design system for scalability:

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.[ext]      # Component implementation
│   │   ├── Button.styles.[ext] # Styles (if separate)
│   │   └── index.[ext]       # Public exports
│   ├── Card/
│   └── ...
├── styles/
│   ├── tokens.css            # Design tokens (CSS custom properties)
│   └── global.css            # Global styles, resets
├── theme/
│   └── tokens.[ext]          # Token definitions (if using JS)
└── examples/                 # Showcase and example pages
```

---

## Design Tokens

### Use CSS Custom Properties

CSS custom properties enable easy theming and dark mode:

```css
:root {
  /* Colors */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-background: #ffffff;
  --color-surface: #fafafa;
  --color-foreground: #171717;
  --color-border: #e5e5e5;

  /* Typography */
  --font-family-heading: 'Inter', system-ui, sans-serif;
  --font-family-body: 'Inter', system-ui, sans-serif;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;

  /* Spacing (4px base) */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-6: 1.5rem;

  /* Borders */
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px rgb(0 0 0 / 0.1);
}

/* Dark mode */
.dark {
  --color-background: #171717;
  --color-surface: #262626;
  --color-foreground: #fafafa;
  --color-border: #404040;
}
```

### Token Granularity

Create detailed scales, not single values:

```css
/* Good: Full palette */
--primary-50: #eff6ff;
--primary-100: #dbeafe;
--primary-500: #3b82f6;
--primary-700: #1d4ed8;
--primary-900: #1e3a8a;

/* Bad: Single color */
--primary: blue;
```

---

## Component Patterns

### Basic Structure

Every component should have:

1. **Props/API** - Clear, typed interface
2. **Variants** - Different visual styles
3. **Sizes** - sm, md, lg options
4. **States** - default, hover, focus, disabled, loading
5. **Accessibility** - ARIA attributes, keyboard support

### Button Example (Conceptual)

```
Props:
- variant: 'primary' | 'secondary' | 'outline' | 'ghost'
- size: 'sm' | 'md' | 'lg'
- disabled: boolean
- loading: boolean
- children: ReactNode

States to style:
- Default
- Hover
- Focus (visible indicator!)
- Active/Pressed
- Disabled
- Loading (with spinner)

Accessibility:
- Focus visible on keyboard nav
- aria-busy="true" when loading
- Disabled attribute when disabled
```

### Input Example (Conceptual)

```
Props:
- label: string
- value: string
- placeholder: string
- error: string
- hint: string
- disabled: boolean

States to style:
- Default
- Focus (with ring)
- Error (red border + message)
- Success (green border)
- Disabled

Accessibility:
- Label associated with input (for/id or wrapping)
- Error linked with aria-describedby
- aria-invalid for error state
```

---

## Variant Patterns

### Using a Variant System

Define variants clearly:

```
Button variants:
- primary   → Filled background, bold
- secondary → Subtle background
- outline   → Border only
- ghost     → Transparent, hover bg
- danger    → Red, destructive actions

Input variants:
- outlined  → Border visible
- filled    → Background fill
- underlined → Bottom border only
```

### Size System

Consistent sizing across components:

```
sm  → Compact, density-focused
md  → Default, balanced
lg  → Comfortable, touch-friendly

Example button heights:
- sm: 36px (2.25rem)
- md: 40px (2.5rem)
- lg: 48px (3rem)
```

---

## State Management

### Theme Toggle

For dark mode support:

```javascript
// Conceptual approach
function useTheme() {
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    // Check localStorage or system preference
    const prefersDark = window.matchMedia(
      '(prefers-color-scheme: dark)'
    ).matches
    setIsDark(prefersDark)
  }, [])

  useEffect(() => {
    // Apply to document
    document.documentElement.classList.toggle('dark', isDark)
  }, [isDark])

  return { isDark, toggle: () => setIsDark(!isDark) }
}
```

### Component States

Handle states consistently:

```
Loading state:
- Show spinner
- Disable interactions
- Set aria-busy="true"

Disabled state:
- Reduce opacity
- Remove hover effects
- Set disabled attribute
- Remove from tab order
```

---

## Accessibility Checklist

Apply to all components:

- [ ] Keyboard accessible (Tab, Enter, Space, Escape)
- [ ] Visible focus indicator
- [ ] ARIA attributes where needed
- [ ] Color isn't the only indicator
- [ ] Labels for all inputs
- [ ] Error messages announced to screen readers
- [ ] Reduced motion respected

---

## Tips by Stack

### Utility-First (Tailwind)
- Use `class-variance-authority` for variants
- Extend `tailwind.config.js` with tokens
- Use CSS variables for theme colors

### CSS-in-JS (styled-components, Emotion)
- Use ThemeProvider for tokens
- Use transient props (`$prop`) for styling-only values
- Define tokens as JS objects

### SCSS/CSS Modules
- Use SCSS maps for tokens
- CSS custom properties for dynamic values
- Mixins for common patterns

### Vue/Svelte
- Use `v-bind()` or CSS custom properties
- Stores/context for theme state
- Scoped styles with global token references

---

## Common Patterns

### Card Layout
```
Card
├── Header (optional)
│   ├── Title
│   └── Actions
├── Content
└── Footer (optional)
```

### Form Field
```
FormField
├── Label (with required indicator)
├── Input
├── Hint (optional)
└── Error (optional, shown on error)
```

### Alert
```
Alert
├── Icon (based on type)
├── Content
│   ├── Title (optional)
│   └── Message
└── Close button (optional)
```

---

## Best Practices

1. **Use tokens everywhere** - No hardcoded values
2. **Test dark mode early** - Don't add it last
3. **Forward refs** - For DOM access when needed
4. **Type your props** - Catch errors early
5. **Document as you build** - Don't leave it for later
6. **Build the showcase page** - Visual reference helps everyone
