# Design System Schema

This document defines the JSON schema for design system files.

## tokens.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "colors": {
      "type": "object",
      "properties": {
        "primary": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "secondary": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "success": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "warning": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "error": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "info": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "background": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "surface": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "text": {
          "type": "object",
          "properties": {
            "primary": { "type": "string" },
            "secondary": { "type": "string" }
          }
        }
      }
    },
    "typography": {
      "type": "object",
      "properties": {
        "fonts": {
          "type": "object",
          "properties": {
            "heading": { "type": "string" },
            "body": { "type": "string" },
            "mono": { "type": "string" }
          }
        },
        "sizes": {
          "type": "object",
          "properties": {
            "xs": { "type": "string" },
            "sm": { "type": "string" },
            "base": { "type": "string" },
            "lg": { "type": "string" },
            "xl": { "type": "string" },
            "2xl": { "type": "string" },
            "3xl": { "type": "string" },
            "4xl": { "type": "string" }
          }
        },
        "weights": {
          "type": "object",
          "properties": {
            "regular": { "type": "integer" },
            "medium": { "type": "integer" },
            "semibold": { "type": "integer" },
            "bold": { "type": "integer" }
          }
        }
      }
    },
    "spacing": {
      "type": "object",
      "properties": {
        "0": { "type": "string" },
        "1": { "type": "string" },
        "2": { "type": "string" },
        "4": { "type": "string" },
        "6": { "type": "string" },
        "8": { "type": "string" },
        "10": { "type": "string" },
        "12": { "type": "string" },
        "16": { "type": "string" }
      }
    },
    "borders": {
      "type": "object",
      "properties": {
        "widths": {
          "type": "object",
          "properties": {
            "1px": { "type": "string" },
            "2px": { "type": "string" }
          }
        },
        "radius": {
          "type": "object",
          "properties": {
            "sm": { "type": "string" },
            "md": { "type": "string" },
            "lg": { "type": "string" },
            "xl": { "type": "string" },
            "full": { "type": "string" }
          }
        },
        "colors": {
          "type": "object",
          "properties": {
            "default": { "type": "string" },
            "focus": { "type": "string" }
          }
        }
      }
    },
    "shadows": {
      "type": "object",
      "properties": {
        "level1": { "type": "string" },
        "level2": { "type": "string" },
        "level3": { "type": "string" },
        "level4": { "type": "string" }
      }
    }
  },
  "required": ["colors", "typography", "spacing", "borders", "shadows"]
}
```

## component-schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "description": { "type": "string" },
    "category": {
      "type": "string",
      "enum": ["button", "card", "input", "typography", "feedback", "navigation", "layout"]
    },
    "states": {
      "type": "array",
      "items": { "type": "string" }
    },
    "variants": {
      "type": "array",
      "items": { "type": "object" }
    },
    "sizes": {
      "type": "array",
      "items": { "type": "object" }
    }
  },
  "required": ["name", "description", "category", "states"]
}
```
