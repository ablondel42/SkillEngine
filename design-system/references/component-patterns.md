# Component Patterns

## Button

### Structure
```html
<button class="btn">
  <span class="btn-label">Button Text</span>
</button>
```

### States

| State | Background | Text | Border |
|-------|------------|------|--------|
| Default | Primary | White | None |
| Hover | Primary dark | White | None |
| Active | Primary darker | White | None |
| Focus | Primary | White | 2px focus ring |
| Disabled | Gray 200 | Gray 500 | None |

### Variants

| Variant | Style |
|---------|-------|
| solid | Filled background, bold |
| outline | Border only, transparent bg |
| ghost | Transparent, hover background |
| text | No background or border |

### Sizes

| Size | Padding | Font size |
|------|---------|-----------|
| sm | 8px 16px | 14px |
| md | 12px 24px | 16px |
| lg | 16px 32px | 18px |

---

## Card

### Structure
```html
<div class="card">
  <div class="card-header">Title</div>
  <div class="card-body">Content</div>
  <div class="card-footer">Actions</div>
</div>
```

### States

| State | Shadow |
|-------|--------|
| Default | Level 2 |
| Hover | Level 3 |

### Variants

| Variant | Style |
|---------|-------|
| elevated | Shadow, rounded corners |
| flat | Border only, subtle |
| interactive | Hover state active |

---

## Input

### Structure
```html
<div class="input-wrapper">
  <label class="input-label">Label</label>
  <input class="input" type="text" />
  <span class="input-hint">Helper text</span>
</div>
```

### States

| State | Border | Background | Label |
|-------|--------|------------|-------|
| Default | Gray 300 | White | Gray 600 |
| Focus | Primary | White | Primary |
| Error | Error | Error 50 | Error |
| Success | Success | Success 50 | Success |
| Disabled | Gray 200 | Gray 50 | Gray 400 |

---

## Alert

### Structure
```html
<div class="alert alert-{type}">
  <span class="alert-icon">Icon</span>
  <div class="alert-content">Message</div>
  <button class="alert-close">Close</button>
</div>
```

### Types

| Type | Background | Text | Icon |
|------|------------|------|------|
| success | Success 100 | Success | Check |
| warning | Warning 100 | Warning | Alert |
| error | Error 100 | Error | X |
| info | Info 100 | Info | Info |

---

## Modal

### Structure
```html
<div class="modal-overlay">
  <div class="modal">
    <div class="modal-header">Title</div>
    <div class="modal-body">Content</div>
    <div class="modal-footer">Actions</div>
  </div>
</div>
```

### Behavior

- Backdrop click to close (configurable)
- Escape key to close
- Focus trap within modal
- Animation: fade in + slide up

---

## Navigation

### Structure
```html
<nav class="nav">
  <a class="nav-item active" href="#">Home</a>
  <a class="nav-item" href="#">Features</a>
  <a class="nav-item" href="#">Settings</a>
</nav>
```

### States

| State | Text | Background |
|-------|------|------------|
| Default | Gray 600 | Transparent |
| Active | Primary | Primary 100 |
| Hover | Gray 800 | Gray 100 |

---

## Badges

### Sizes

| Size | Padding | Font size |
|------|---------|-----------|
| sm | 4px 8px | 12px |
| md | 6px 12px | 14px |

### Types

| Type | Background | Text |
|------|------------|------|
| neutral | Gray 200 | Gray 800 |
| success | Success 200 | Success 800 |
| warning | Warning 200 | Warning 800 |
| error | Error 200 | Error 800 |
| info | Info 200 | Info 800 |
