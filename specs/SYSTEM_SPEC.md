# UCE Render System Specification

## Overview

UCE Render (Universal Content Engine) transforms source content into engaging presentation slides through a multi-stage LLM-powered pipeline.

```
┌─────────┐   ┌──────────────┐   ┌──────────────────┐   ┌────────┐   ┌────────┐
│  Input  │ → │ Atom Extract │ → │ Slide Generation │ → │ Render │ → │ Output │
└─────────┘   └──────────────┘   └──────────────────┘   └────────┘   └────────┘
                                         ↓
                                 ┌──────────────┐
                                 │    Theme     │
                                 │  Generation  │
                                 └──────────────┘
```

---

## 1. Input Stage

### 1.1 Source Content

| Input Type | Format | Description |
|------------|--------|-------------|
| Text file | `.txt` | Plain text content |
| Transcript | `.vtt` | WebVTT subtitles with timestamps |

### 1.2 User Instruction

Natural language guidance for the presentation:
- Slide count: "Create 5 slides"
- Focus: "Focus on career transitions"
- Audience: "For technical executives"
- Style: "Make it punchy and visual"

### 1.3 Source Object

```python
class Source:
    source_id: str          # Unique identifier
    name: str               # Display name
    file_path: str          # Path or virtual path
    content: str            # Full text content
    content_type: str       # MIME type
    metadata: dict          # Additional info (abstract, etc.)
```

---

## 2. Atom Extraction Stage

### 2.1 Purpose

Extract structured, reusable content units from source material.

### 2.2 Atom Types

| Type | Description | Key Fields |
|------|-------------|------------|
| `BioAtom` | Person/entity info | name, role, organization, background |
| `StatAtom` | Numerical data | value, unit, context, comparison |
| `QuoteAtom` | Memorable statements | text, speaker, context |
| `FactAtom` | Factual information | claim, evidence, source_ref |
| `TensionAtom` | Conflict/challenge | challenge, stakes, resolution |
| `ConceptAtom` | Abstract ideas | name, definition, examples |
| `VisualAtom` | Visual descriptions | description, style, mood |

### 2.3 Atom Structure

```python
class Atom(BaseModel):
    id: str                 # Unique identifier (e.g., "fact_001")
    type: str               # Atom type
    content: str            # Main content text
    source_ref: str         # Reference to source
    confidence: float       # Extraction confidence (0-1)
    metadata: dict          # Type-specific fields
```

### 2.4 AtomCollection

```python
class AtomCollection(PatchableContextCollection):
    id: str
    model: str = "Atom"
    contexts: List[Atom]
```

### 2.5 Extraction Process

```
Source Content → LLM (structured output) → AtomCollection
```

**Prompt guidance includes:**
- Extract diverse atom types
- Preserve speaker attribution
- Identify tensions and turning points
- Extract memorable quotes verbatim

---

## 3. Slide Generation Stage (Unified)

### 3.1 Purpose

Generate complete slides with deck-level awareness in a single LLM call.
This ensures layout variety, widget distribution, and narrative coherence.

### 3.2 Input

```json
{
  "atoms": [...],           // All extracted atoms
  "user_instruction": "Create 5 slides about career",
  "intent_guidance": "...", // From intent detection
  "themes": [...]           // Available themes
}
```

### 3.3 Output

Complete slides with layout, widgets, and content:

```json
{
  "slides": [
    {
      "id": "slide_1",
      "rank": 1,
      "state": "active",
      "story": "Hook with career duration number",
      "atoms": ["bio_001"],
      "layout": "hero-split",
      "density": "minimal",
      "widgets": {
        "left": {
          "type": "Data.BigNum",
          "parameters": { "value": "14", "label": "Years in AI" }
        },
        "right": {
          "type": "Type.Quote",
          "parameters": { "text": "From training models to orchestrating intelligence" }
        }
      },
      "header": { ... },
      "footer": { ... },
      "parameters": { "ratio": "40-60", "vibe": "aurora" }
    }
  ]
}
```

### 3.4 Deck-Level Planning (Enforced in Prompt)

The single-step generation ensures variety through prompt rules:

**Layout Variety Rules:**
- Maximum 2 consecutive slides with same layout
- A 5-slide deck should use at least 3 different layouts
- Opening slide: use `hero-split` or `center`
- Closing slide: use `center` or `hero-split`

**Widget Distribution Rules:**
- At least 1 slide must have `Data.BigNum` (key number anchor)
- At least 1 slide must have `Type.Quote` (memorable statement)
- At least 1 slide must have `Data.Metric` (milestone/stat)
- No more than 50% of slides should use `Type.List` as primary widget

**Density Pacing:**
- Opening: minimal (1-2 points)
- Middle: moderate (3-4 points)
- Closing: minimal (strong finish)

### 3.5 Layout Options

| Layout | Slots | Best For |
|--------|-------|----------|
| `hero-split` | left, right | Opening, closing, key messages |
| `smart-grid` | col1-col4 | Multiple equal items |
| `timeline` | title, step1-step5 | Chronological content |
| `comparison` | title, beforeLabel, before, afterLabel, after | Contrasts |
| `center` | main | Single key message |

### 3.6 Widget Types

**Typography Widgets:**
| Widget | Parameters | Use Case |
|--------|------------|----------|
| `Type.Display` | text, tagline | Hero headlines |
| `Type.Heading` | text, level | Section headers |
| `Type.Body` | text, size | Paragraphs |
| `Type.Caption` | text | Small annotations |
| `Type.Quote` | text, attribution, size | Memorable quotes |
| `Type.List` | items, style | Bullet points |

**Data Widgets:**
| Widget | Parameters | Use Case |
|--------|------------|----------|
| `Data.BigNum` | value, label, sublabel, trend | Key numbers |
| `Data.Metric` | value, label, sublabel, delta | Stats with context |
| `Data.Table` | headers, rows | Tabular data |
| `Data.Chart` | type, data, options | Visualizations |

---

## 4. Theme Generation Stage

### 4.1 Purpose

Generate cohesive visual styling based on content and intent.

### 4.2 Theme Structure

```python
class Theme:
    id: str
    name: str
    primary_color: str      # Main accent color
    secondary_color: str    # Secondary accent
    background_color: str   # Slide background
    text_color: str         # Primary text
    font_family: str        # Font stack
    heading_font: str       # Heading font
```

### 4.3 Theme Generation Input

- Audience (e.g., "technical executives")
- Tone (e.g., "professional", "creative")
- Purpose (e.g., "inform", "persuade")
- Visual guidance from intent detection

---

## 5. Patch Operations

### 5.1 Purpose

Incremental state management for slides and atoms.

### 5.2 Operation Types

| Operation | Description | Example |
|-----------|-------------|---------|
| `add` | Add new context | Add a slide |
| `update` | Modify existing | Update widget content |
| `remove` | Delete context | Remove a slide |

### 5.3 Patch Structure

```json
{
  "operations": [
    {
      "add": {
        "id": "slide_1",
        "rank": 1,
        "state": "active",
        "layout": "hero-split",
        "widgets": { ... }
      }
    }
  ]
}
```

### 5.4 Slide States

| State | Description |
|-------|-------------|
| `active` | Ready for render |
| `archived` | Removed but preserved |

---

## 6. Layout Configuration

### 6.1 Layout Engine Interface

```python
class LayoutEngine(Protocol):
    def get_layouts(self) -> List[LayoutConfig]
    def get_layout(self, layout_id: str) -> LayoutConfig
    def validate_slide(self, slide: Slide) -> ValidationResult
```

### 6.2 Layout Configuration

```python
class LayoutConfig:
    id: str                 # e.g., "hero-split"
    name: str               # Display name
    slots: List[SlotConfig] # Available slots
    parameters: dict        # Layout-specific params
```

### 6.3 Slot Configuration

```python
class SlotConfig:
    id: str                 # e.g., "left", "col1"
    role: str               # Semantic role
    allowed_widgets: List[str]  # Compatible widget types
    size: str               # small, medium, large
```

### 6.4 Slidev Layout Mapping

| Layout | Slidev Class | Slots |
|--------|--------------|-------|
| `hero-split` | `.hero-split` | left, right |
| `smart-grid` | `.smart-grid` | col1-col4 |
| `timeline` | `.timeline` | title, step1-step5 |
| `comparison` | `.comparison` | title, before*, after* |
| `center` | `.center` | main |

---

## 7. Slidev Layout Engine

### 7.1 Purpose

Convert abstract slide definitions to Slidev-compatible format.

### 7.2 Layout Templates

Each layout has a CSS template:

```css
/* hero-split */
.hero-split {
  display: grid;
  grid-template-columns: var(--ratio-left, 1fr) var(--ratio-right, 1fr);
  gap: 2rem;
  height: 100%;
}
```

### 7.3 Widget Templates

Each widget type has a render template:

```html
<!-- Data.BigNum -->
<div class="widget bignum">
  <span class="value">{{ value }}</span>
  <span class="label">{{ label }}</span>
  <span class="sublabel">{{ sublabel }}</span>
</div>
```

### 7.4 Vibe Effects

| Vibe | CSS Effect |
|------|------------|
| `none` | No effect |
| `aurora` | Animated gradient background |
| `waves` | Subtle wave animation |
| `mesh` | Gradient mesh background |

---

## 8. Slidev Render

### 8.1 Purpose

Convert slides to Slidev markdown and build HTML.

### 8.2 Render Pipeline

```
Slides JSON → Markdown Generator → slides.md → Slidev Build → HTML
```

### 8.3 Markdown Structure

```markdown
---
theme: default
title: Presentation Title
---

# Slide 1

<div class="hero-split" style="--ratio-left: 40%; --ratio-right: 60%;">
  <div class="left">
    <div class="widget bignum">
      <span class="value">14</span>
      <span class="label">Years in AI</span>
    </div>
  </div>
  <div class="right">
    <div class="widget quote">
      <blockquote>"From training models..."</blockquote>
    </div>
  </div>
</div>

---

# Slide 2
...
```

### 8.4 Build Process

```bash
npx @slidev/cli build slides.md --base ./ --out dist
```

### 8.5 Output Files

| File | Description |
|------|-------------|
| `debug_storyline.json` | (Removed - merged into content) |
| `debug_content.json` | Final slides (active state) |
| `debug_markdown.md` | Generated Slidev markdown |
| `output.html` | Built HTML presentation |

---

## 9. Data Flow Summary

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              UCE RENDER PIPELINE                              │
└──────────────────────────────────────────────────────────────────────────────┘

1. INPUT
   ├── source.txt / source.vtt
   └── user_instruction: "Create 5 slides about career"

2. INTENT DETECTION (LLM)
   └── Output: audience, tone, pattern, visual_density

3. ATOM EXTRACTION (LLM)
   ├── Input: source content + intent guidance
   └── Output: AtomCollection [BioAtom, StatAtom, QuoteAtom, FactAtom, ...]

4. THEME GENERATION (LLM)
   ├── Input: intent (audience, tone, purpose)
   └── Output: Theme

5. SLIDE GENERATION (LLM) ← SINGLE STEP, DECK-LEVEL VIEW
   ├── Input: atoms + user_instruction + intent_guidance + themes
   └── Output: Complete slides with:
       ├── layout per slide (variety enforced)
       ├── widgets with content (distribution enforced)
       ├── density and vibe
       └── header/footer
   
   Enforces via prompt:
   ├── Layout variety (max 2 consecutive same)
   ├── Widget distribution (≥1 BigNum, ≥1 Quote, ≥1 Metric)
   └── Density pacing (minimal → moderate → minimal)

6. RENDER
   ├── Slides JSON → Slidev Markdown
   ├── Slidev Build → HTML
   └── Output: presentation.html

┌──────────────────────────────────────────────────────────────────────────────┐
│                              DEBUG OUTPUTS                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│  output/debug_content.json    - Complete slides with content                  │
│  output/debug_markdown.md     - Generated Slidev markdown                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Configuration

### 10.1 Generation Config

```python
class GenerationConfig:
    model: str              # LLM model name
    temperature: float      # Creativity (0-1)
    max_tokens: int         # Output limit
    system_prompt: str      # System context
```

### 10.2 Render Config

```yaml
# slidev.config.yaml
layout_engine: slidev
output_format: html
debug_output: true
build_dir: ./slidev_build
```

---

## 11. Error Handling

### 11.1 Validation Errors

| Error | Stage | Resolution |
|-------|-------|------------|
| Empty source | Input | Reject with message |
| Invalid atom type | Extraction | Skip or map to closest |
| Layout mismatch | Generation | Auto-fix or warn |
| Widget incompatibility | Generation | Suggest alternative |
| Build failure | Render | Show Slidev error |

### 11.2 Validation Hooks

```python
def validate_slide(slide: Slide) -> ValidationResult:
    # Check layout-widget compatibility
    # Check slot usage
    # Check content length
    return ValidationResult(valid=True, warnings=[], errors=[])
```

---

## 12. Future Considerations

### 12.1 Multi-Source Support

- Multiple input files
- Cross-source atom linking
- Source-specific extraction prompts

### 12.2 Interactive Refinement

- Per-slide editing
- Widget type changes
- Layout swapping
- Content regeneration

### 12.3 Export Formats

- PDF export
- PowerPoint export
- Image sequence
- Video with transitions
