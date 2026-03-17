# Accessibility Quick Reference

Essential accessibility checks for design system components. Target: WCAG 2.1 AA.

---

## Color & Contrast

**Text contrast:** 4.5:1 for normal text, 3:1 for large text (18pt+)

**Quick checks:**
- Color isn't the only way to convey information
- Links have underlines or other non-color indicators
- Error states include icons or text, not just red
- Focus indicators are visible with 3:1 contrast

**Tools:** WebAIM Contrast Checker, Stark plugin

---

## Keyboard Navigation

**Must be keyboard accessible:**
- All buttons, links, inputs
- Dropdowns, tabs, modals
- Custom interactive components

**Focus indicators:**
- Visible on all interactive elements
- At least 2px thick
- Never removed via CSS

**Key interactions:**
| Component | Keys |
|-----------|------|
| Buttons | Enter, Space |
| Modals | Escape, Tab (trapped) |
| Tabs | Arrow keys, Enter |
| Selects | Arrow keys, Enter, Escape |

---

## Screen Reader Basics

**Common ARIA attributes:**
- `aria-label` - For icon-only buttons
- `aria-expanded` - For collapsible sections
- `aria-invalid` + `aria-describedby` - For form errors
- `aria-hidden="true"` - On decorative icons

**Landmarks to use:**
```html
<header>, <nav>, <main>, <aside>, <footer>
```

**Dynamic announcements:**
```html
<div aria-live="polite">Success message</div>
<div aria-live="assertive" role="alert">Error message</div>
```

---

## Form Accessibility

**Every input needs:**
- A visible `<label>` (not just placeholder)
- Error messages linked with `aria-describedby`
- Required fields marked with `aria-required`

**Example:**
```html
<label for="email">Email</label>
<input
  id="email"
  type="email"
  aria-required="true"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">Invalid email</span>
```

---

## Images & Icons

| Type | Treatment |
|------|-----------|
| Informative images | Descriptive `alt` text |
| Decorative images | `alt="" aria-hidden="true"` |
| Functional icons | `aria-label` on parent button |
| Icon + text | `aria-hidden="true"` on icon |

---

## Motion

**Respect reduced motion preference:**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Avoid:**
- Auto-playing animations longer than 5 seconds
- Content flashing more than 3 times/second

---

## Quick Test Checklist

**Automated:**
- Run axe DevTools
- Run Lighthouse accessibility audit

**Manual:**
- Navigate with keyboard only (Tab, Enter, Escape)
- Test with a screen reader (VoiceOver or NVDA)
- Zoom to 200% - content still usable
- Check color contrast ratios

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Missing alt | Add descriptive alt text |
| Empty links | Use descriptive link text |
| No focus styles | Add visible `:focus-visible` styles |
| Color-only errors | Add icons and text labels |
| Unlabeled inputs | Add visible labels |
