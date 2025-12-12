# CLI Contract: UCE Render

**Version**: 1.0.0  
**Purpose**: Define command-line interface contract for the UCE rendering system

## Command: `uce-render`

Main command for rendering layouts with styles.

### Synopsis

```bash
uce-render [OPTIONS] LAYOUTS_FILE STYLES_FILE
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `LAYOUTS_FILE` | Path | Yes | Path to JSON file containing Layouts collection |
| `STYLES_FILE` | Path | Yes | Path to JSON file containing Styles collection |

### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--output` | `-o` | Path | stdout | Output file path (HTML) |
| `--format` | `-f` | Choice | html | Output format: html, json |
| `--validate-only` | - | Flag | False | Only validate inputs, don't render |
| `--verbose` | `-v` | Flag | False | Enable verbose logging |
| `--help` | `-h` | Flag | - | Show help message |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Invalid arguments or file not found |
| 2 | Validation error (size constraint, missing reference) |
| 3 | Rendering error (template error, I/O error) |

### Output Formats

#### HTML Format (default)

Produces a complete HTML document with embedded CSS.

**Example**:
```bash
uce-render layouts.json styles.json -o output.html
```

**Output**: HTML file at `output.html`

#### JSON Format

Produces a RenderableLayout JSON representation (for debugging).

**Example**:
```bash
uce-render layouts.json styles.json -f json -o renderable.json
```

**Output**:
```json
{
  "layout": { "strategy": "Bento", "variant": "HeroLeft", ... },
  "widget_assignments": [
    {
      "role": "main",
      "widget": { "widget_type": "Chart.Bar", ... },
      "style_name": "modern"
    }
  ],
  "resolved_styles": {
    "modern": {
      "border-radius": "8px",
      "box-shadow": "0 2px 8px rgba(0,0,0,0.1)",
      ...
    }
  }
}
```

### Validation-Only Mode

Use `--validate-only` to check inputs without rendering.

**Example**:
```bash
uce-render layouts.json styles.json --validate-only
```

**Success Output** (exit code 0):
```
✓ Layouts file valid
✓ Styles file valid
✓ Size constraints satisfied
✓ All references resolved
Ready to render
```

**Error Output** (exit code 2):
```
✗ Validation failed

Error in layouts.json:
  Widget "Chart.Sankey" requires size XL but assigned to slot "sidebar" with size M
  
  Location: widget_assignments[2]
  Suggestion: Use a larger slot or choose a smaller widget type
```

### Error Messages

All errors include:
- Clear description of what went wrong
- Location in JSON file (if applicable)
- Actionable suggestion for fixing

**Example - Missing File**:
```
Error: Layouts file not found
  Path: /path/to/layouts.json
  Suggestion: Check file path or create the file
Exit code: 1
```

**Example - Size Violation**:
```
Error: Size constraint violation
  Widget: Type.Display (requires M)
  Slot: cell_1 (size S)
  Location: layouts.layouts.hero.widget_assignments[0]
  Suggestion: Assign widget to a larger slot (M, L, or XL)
Exit code: 2
```

**Example - Missing Reference**:
```
Error: Style not found
  Style name: "modern_dark"
  Referenced by: widget_assignments[1]
  Available styles: ["modern", "minimal", "bold"]
  Suggestion: Use one of the available styles or define "modern_dark" in styles.json
Exit code: 2
```

## Input File Contracts

### Layouts File Schema

**File**: `layouts.json`

**Schema**:
```json
{
  "layouts": {
    "<layout_id>": {
      "strategy": "Bento" | "Swiss" | "Cinematic",
      "variant": "<variant_name>",
      "gap": "<css_length>",
      "padding": "<css_length>",
      "background": "<css_background>",
      "widget_assignments": [
        {
          "role": "<slot_role>",
          "widget_type": "<widget_type>",
          "atom_id": "<atom_id>",
          "params": { ... },
          "style_name": "<style_name>"
        }
      ]
    }
  },
  "active_layout_id": "<layout_id>"
}
```

**Validation Rules**:
- `active_layout_id` must exist in `layouts` object
- Each `strategy` must be one of: Bento, Swiss, Cinematic
- Each `variant` must be valid for its strategy
- Each `role` in widget_assignments must match a slot defined by the variant
- Each `widget_type` must be registered in the widget registry

### Styles File Schema

**File**: `styles.json`

**Schema**:
```json
{
  "themes": {
    "<theme_name>": {
      "primary_font": "<font_family>",
      "secondary_font": "<font_family>",
      "foreground_primary_color": "<css_color>",
      "foreground_secondary_color": "<css_color>",
      "background_primary_color": "<css_color>",
      "background_secondary_color": "<css_color>",
      "accent_color": "<css_color>",
      "error_color": "<css_color>",
      "success_color": "<css_color>"
    }
  },
  "styles": {
    "<style_name>": {
      "theme_name": "<theme_name>",
      "border_radius": "<css_length>",
      "shadow_intensity": "none" | "subtle" | "medium" | "strong",
      "spacing_scale": <number>,
      "transition_duration": "<css_time>"
    }
  },
  "default_style_name": "<style_name>"
}
```

**Validation Rules**:
- Each `theme_name` in styles must exist in `themes` object
- `default_style_name` must exist in `styles` object
- All color values must be valid CSS colors
- `spacing_scale` must be a positive number

## Contract Tests

The following test scenarios validate the CLI contract:

### Test: Successful Rendering

```bash
uce-render tests/fixtures/valid_layout.json tests/fixtures/valid_styles.json -o output.html
echo $?  # Should output: 0
test -f output.html  # Should exist
```

### Test: Validation Error Detection

```bash
uce-render tests/fixtures/invalid_size.json tests/fixtures/valid_styles.json --validate-only
echo $?  # Should output: 2
```

### Test: JSON Output Format

```bash
uce-render tests/fixtures/valid_layout.json tests/fixtures/valid_styles.json -f json -o renderable.json
jq '.layout.strategy' renderable.json  # Should output: "Bento"
```

### Test: Missing File Handling

```bash
uce-render nonexistent.json styles.json 2>&1 | grep "not found"
echo $?  # Should output: 1
```

### Test: Help Text

```bash
uce-render --help | grep "LAYOUTS_FILE"
```

## Future Extensions

### Planned Options (Not in v1.0)

- `--template-dir`: Custom Jinja2 template directory
- `--widget-registry`: Load custom widget definitions
- `--theme-override`: Override theme values via CLI
- `--watch`: Auto-regenerate on file changes
