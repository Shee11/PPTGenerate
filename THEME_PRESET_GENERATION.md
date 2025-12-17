# Theme and Preset Generation Feature

## Overview

The UCE Render system now supports **dynamic theme and preset generation** based on detected presentation intent. The LLM analyzes user instructions and generates contextually appropriate visual styling.

## Implementation Summary

### 1. New Patch Operations

Added two new operation types to the patch schema:

- **`SetThemeOperation`**: Applies custom theme (colors, fonts, spacing)
- **`SetPresetOperation`**: Applies global visual presets (surface, shape, fill, effect)

**File**: `src/common/patchable_context_pydantic.py`

```python
class SetThemeOperation(BaseModel):
    """Set theme operation - theme configuration"""
    set_theme: Dict[str, Any]

class SetPresetOperation(BaseModel):
    """Set preset operation - global preset configuration"""
    set_preset: Dict[str, Any]
```

### 2. Slides Collection Extensions

The `Slides` class now stores theme and preset configurations:

**File**: `src/common/slides.py`

```python
class Slides(PatchableCollection):
    def __init__(self, id: str = "slides"):
        super().__init__(id=id, model_class=Slide)
        self.theme: Optional[Dict[str, Any]] = None
        self.preset: Optional[Dict[str, Any]] = None
    
    def patch(self, patch: Patch) -> 'Slides':
        # Handle set_theme and set_preset operations
        for op in patch.operations:
            if isinstance(op, SetThemeOperation):
                self.theme = op.set_theme
            elif isinstance(op, SetPresetOperation):
                self.preset = op.set_preset
        # Delegate to parent for add/remove/replace
        super().patch(patch)
        return self
```

### 3. Enhanced Content Generation Prompts

Updated the content generation system prompt to include:

**File**: `src/generation/content/prompts.py`

- **Theme Schema**: JSON schema for theme generation with color palette, fonts, spacing
- **Preset Schema**: JSON schema for preset generation with surface/shape/fill/effect categories
- **Theme Guidelines**:
  - Professional/Business → Blues, grays, clean fonts
  - Creative/Energetic → Bold colors, modern fonts
  - Technical → Dark backgrounds, monospace
  - Minimal → Neutrals, whitespace
- **Preset Guidelines**:
  - TechTuber → Elevated, Rounded, Gradient, Glow
  - Professional → Flat, Sharp, Solid, no effects
  - Creative → Glass, Organic, Gradient_Mesh, various effects

Example prompt output:
```json
[
  {"set_theme": {"id": "energetic_tech", "primary_color": "#0066ff", "accent_color": "#ff4400", ...}},
  {"set_preset": {"surface": "Elevated", "shape": "Rounded", "fill": "Gradient_Linear", "effect": "Glow"}},
  {"replace": {"id": "slide_001", ...}}
]
```

### 4. CLI Integration

The CLI now uses generated themes and presets when available:

**File**: `cli/uce_render.py`

```python
# Use generated theme if available
if slides.theme:
    theme = Theme(**slides.theme)
else:
    theme = Theme()  # Default

# Apply generated preset to style
if slides.preset:
    for widget_type in style_data.get('widgets', {}).keys():
        style_data['widgets'][widget_type].update(slides.preset)
```

## Usage Examples

### TechTuber Style (Dark + Bold Colors)

```bash
python -m cli --source data/context/career_short.txt \
  --user-instruction "Create a TechTuber style presentation with bold colors" \
  --output output/techtuber.html --verbose
```

**Generated Theme**:
- Primary: `#3B82F6` (blue)
- Accent: `#22C55E` (green)
- Background: `#020617` (dark)

### Professional Business (Corporate Blues)

```bash
python -m cli --source data/context/career_short.txt \
  --user-instruction "Create a professional business presentation for executives" \
  --output output/professional.html --verbose
```

**Generated Theme**:
- Primary: `#004B8D` (corporate blue)
- Accent: `#F5A623` (gold)
- Background: `#FFFFFF` (white)

### Creative Vibrant (Designer Friendly)

```bash
python -m cli --source data/context/career_short.txt \
  --user-instruction "Create a creative vibrant presentation for designers" \
  --output output/creative.html --verbose
```

**Generated Theme**:
- Primary: `#FF3366` (hot pink)
- Accent: `#FACC15` (bright yellow)
- Background: `#050816` (dark blue)

## How It Works

1. **Intent Detection**: User instruction analyzed to determine audience, tone, pattern
2. **Theme Generation**: LLM generates contextual theme based on:
   - Audience (executives → professional colors, developers → tech colors)
   - Tone (energetic → vibrant, professional → muted)
   - Pattern (TechTuber → dark + bold, Pitch → corporate + clean)
3. **Preset Application**: Global visual presets applied to all widgets:
   - Surface (Flat, Elevated, Glass)
   - Shape (Sharp, Rounded, Organic)
   - Fill (Solid, Gradient, Pattern)
   - Effect (Glow, Shadow, none)
4. **Patch Processing**: `set_theme` and `set_preset` operations stored in Slides collection
5. **Rendering**: CLI extracts theme/preset and applies to HTML output

## Verification

Run test suite:
```bash
# TechTuber style
python -m cli --source data/context/career_short.txt \
  --user-instruction "TechTuber presentation" \
  --output output/test_techtuber.html --verbose

# Professional style
python -m cli --source data/context/career_short.txt \
  --user-instruction "professional business presentation" \
  --output output/test_professional.html --verbose

# Creative style
python -m cli --source data/context/career_short.txt \
  --user-instruction "creative vibrant presentation" \
  --output output/test_creative.html --verbose
```

Check generated HTML for CSS variables:
```bash
# Check theme colors in output
Get-Content output/test_*.html | Select-String "color-primary|color-accent|color-background"
```

## Benefits

1. **Contextual Styling**: Themes automatically match presentation intent
2. **Audience Alignment**: Professional colors for executives, vibrant colors for designers
3. **Consistent Branding**: Global presets ensure unified visual language
4. **LLM-Driven**: No manual theme configuration needed
5. **Extensible**: Easy to add new theme patterns and preset combinations

## Future Enhancements

- [ ] Theme validation and fallback handling
- [ ] Theme library with reusable patterns
- [ ] Per-slide theme overrides
- [ ] Preset variations per widget type
- [ ] Theme preview in CLI
- [ ] Export/import theme JSON
