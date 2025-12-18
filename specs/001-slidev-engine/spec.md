# Feature Specification: Slidev Layout Engine with Vue Renderer

**Feature Branch**: `001-slidev-engine`  
**Created**: 2024-12-18  
**Status**: Draft  
**Input**: User description: "Create Slidev layout engine with Vue renderer that translates slide JSON to Slidev-style Markdown using slot syntax and frontmatter configuration. Implements theme-agnostic components (business/cyber themes) with CSS variables and UnoCSS shortcuts for LLM-friendly content generation."

## Clarifications

### Session 2024-12-18

- Q: What is the exact structure of the slide JSON that `src/generation/content/generator.py` outputs and the Slidev renderer must consume? → A: JSON mirrors dummy engine structure with widgets grouped by slot names (e.g., `{"layout": "Bento.Standard", "widgets": {"cell_1": {"type": "Type.Display", "parameters": {...}}}}`)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - LLM Generates Slide JSON for Slidev Layouts (Priority: P1)

Content generation LLM (via `src/generation/content/generator.py`) produces slide JSON using Slidev layout documentation, specifying slots and widget content that the Slidev renderer will convert to natural `::slot::` Markdown syntax.

**Why this priority**: Core value proposition - LLM generates structured JSON following Slidev layout documentation (smart-grid with slots: header, col1-colN), which renderer converts to LLM-friendly Markdown. This decouples content generation from rendering format.

**Independent Test**: LLM generates slide JSON with `layout: "smart-grid"`, `cols: 3`, widgets in slots (header, col1, col2, col3). Renderer produces Slidev Markdown with `::header::`, `::col1::`, `::col2::`, `::col3::` sections that render correctly.

**Acceptance Scenarios**:

1. **Given** LLM reads Slidev layout documentation describing smart-grid with header and col1-colN slots, **When** LLM generates JSON with `{"layout": "smart-grid", "parameters": {"cols": 3}, "widgets": {"header": {...}, "col1": {...}, "col2": {...}, "col3": {...}}}`, **Then** renderer outputs Markdown with `::header::`, `::col1::`, `::col2::`, `::col3::` sections
2. **Given** layout documentation describes MetricCard component with label/value/variant parameters, **When** LLM generates widget with `{"type": "Data.BigNum", "parameters": {"text": "Revenue\n$5.2M", "preset": {"variant": "primary"}}}`, **Then** renderer outputs `<MetricCard label="Revenue" value="$5.2M" variant="primary" />` in appropriate slot
3. **Given** widget type is `Type.Code` with syntax highlighting parameter, **When** renderer processes JSON, **Then** output contains properly formatted code block with language specifier in slot content

---

### User Story 2 - Theme Switching Without Component Changes (Priority: P1)

Designer switches between `business` and `cyber` themes by changing one frontmatter parameter. All components and layouts automatically adapt without modifying component code.

**Why this priority**: Enables reusable content across different presentation contexts (corporate meetings vs tech conferences). Critical for maintaining single source of truth.

**Independent Test**: Take existing slide deck with `theme: "business"`, change to `theme: "cyber"`, verify all colors, fonts, and shadows update correctly.

**Acceptance Scenarios**:

1. **Given** slide has `theme: "business"` with white background and blue accents, **When** changed to `theme: "cyber"`, **Then** background becomes dark (#050505), accents become neon green (#00ffa3), grid pattern overlay appears
2. **Given** `MetricCard` component with `variant="primary"`, **When** theme switches from business to cyber, **Then** primary color updates from #2563eb to #00ffa3 without component code changes
3. **Given** slide contains custom text with `text-theme-main` class, **When** theme changes, **Then** text color automatically adjusts from dark (#0f172a) to light (#e2e8f0)

---

### User Story 3 - Layout Engine Provides Documentation for LLM Prompts (Priority: P1)

Slidev layout engine implements `get_layout_documentation()` protocol method that returns complete guide for LLMs including available layouts, slot names, widget-to-component mappings, and theme options.

**Why this priority**: Integration requirement - must work with existing content generation pipeline (`src/generation/content/prompts.py`). Without this, LLMs cannot generate valid slide JSON with correct slot names and widget types.

**Independent Test**: Call `SlidevLayoutEngine.get_layout_documentation()`, verify output includes Smart Grid layout description with slot names ("header", "col1"-"colN"), widget type mappings (Data.BigNum → MetricCard), and theme descriptions.

**Acceptance Scenarios**:

1. **Given** content generation prompts call `get_layout_documentation()`, **When** documentation is retrieved, **Then** output contains layout descriptions formatted like: "Smart Grid: Dynamic column-based layout. Slot names: 'header', 'col1' through 'colN' (where N = cols parameter, range 2-4). Use these as keys in widgets dictionary."
2. **Given** LLM reads widget-to-component mapping documentation, **When** generating slide content, **Then** LLM correctly assigns `{"type": "Data.BigNum", "parameters": {"text": "Revenue\n$5.2M", "preset": {"variant": "primary"}}}` to slot, knowing renderer will convert to MetricCard component
3. **Given** documentation includes theme descriptions (business: blue/white, cyber: green/dark), **When** LLM selects theme based on user intent (e.g., "tech presentation"), **Then** LLM includes theme name in JSON parameters or uses appropriate theme colors

---

### User Story 4 - Render Slide JSON to Slidev Markdown Files (Priority: P2)

System translates internal slide JSON format (from orchestrator) into Slidev Markdown format with frontmatter configuration and slot-based content distribution.

**Why this priority**: Renderer implementation - converts abstract slide model to concrete Slidev format. Secondary to P1 because it builds on layout documentation foundation.

**Independent Test**: Pass slide JSON with widgets, theme, and layout to renderer, receive valid `slides.md` file that Slidev can parse and display.

**Acceptance Scenarios**:

1. **Given** slide JSON has `{"layout": "smart-grid", "parameters": {"cols": 3}, "widgets": {"header": {...}, "col1": {...}, "col2": {...}, "col3": {...}}}`, **When** renderer processes JSON, **Then** output Markdown has frontmatter `layout: smart-grid`, `cols: 3` and content in `::header::`, `::col1::`, `::col2::`, `::col3::` sections
2. **Given** widget is `{"type": "Type.Display", "parameters": {"text": "**Bold** and ==highlighted== text"}}`, **When** renderer translates to Markdown, **Then** output preserves markdown syntax (`**Bold** and ==highlighted== text`) in slot content
3. **Given** slide JSON has `{"widgets": {"header": {"type": "Type.Heading", "parameters": {"text": "Main Title"}}, "footer": {"type": "Type.Body", "parameters": {"text": "© 2024"}}}}`, **When** rendered, **Then** Markdown has `::header::` slot with heading and footer in frontmatter or dedicated slot

---

### User Story 5 - Support Multi-Slide Presentations (Priority: P2)

Renderer outputs multi-slide Slidev presentations where each slide is separated by `---` delimiter and has independent frontmatter configuration.

**Why this priority**: Real-world presentations require multiple slides. Secondary because single-slide rendering must work first.

**Independent Test**: Generate 5-slide presentation with alternating themes (business, cyber, business, cyber, business), verify Slidev renders 5 distinct slides with correct theme per slide.

**Acceptance Scenarios**:

1. **Given** renderer receives array of 5 slide JSON objects (each with `layout`, `parameters`, `widgets` fields), **When** processing completes, **Then** output Markdown contains 4 `---` separators creating 5 slides with individual frontmatter sections
2. **Given** slides have varying theme configurations (slides 1/3 with business theme colors, slides 2/4 with cyber theme colors), **When** rendered in Slidev, **Then** each slide displays with its specified theme based on `theme` field or color-to-theme mapping
3. **Given** slide 2 has `{"layout": "smart-grid", "parameters": {"cols": 2}}`, slide 3 has `{"layout": "hero-split", "parameters": {"ratio": "60-40"}}`, **When** navigating between slides in Slidev, **Then** layout structure changes correctly (grid vs split)

---

### User Story 6 - Widget-to-Component Translation for Structured Data (Priority: P3)

Slidev renderer translates specific widget types (Data.BigNum, Data.Progress, Data.Trend) from JSON into Vue components (`MetricCard`, `StatusBadge`, `ProgressBar`) for enhanced visual presentation beyond basic markdown.

**Why this priority**: Enhances presentation quality but not essential for MVP. Typography widgets (Type.*) rendered as markdown are sufficient for most content.

**Independent Test**: LLM generates slide JSON with Data.BigNum, Data.Progress, and Type.Body widgets in same layout, renderer outputs MetricCard, ProgressBar components mixed with markdown text, all render correctly with theme styling.

**Acceptance Scenarios**:

1. **Given** widget is `{"type": "Data.BigNum", "parameters": {"text": "Revenue\n$5.2M", "preset": {"variant": "primary"}}}`, **When** rendered with business theme, **Then** output contains `<MetricCard label="Revenue" value="$5.2M" variant="primary" />` with blue accent color (#2563eb)
2. **Given** widget is `{"type": "Data.Progress", "parameters": {"label": "CPU Usage", "value": 85, "status": "warning"}}`, **When** rendered with cyber theme, **Then** output contains `<StatusBadge status="warning" text="High CPU" />` or equivalent component with neon yellow glow
3. **Given** slot has mix of `{"type": "Type.Body", "parameters": {"text": "Description..."}}` and `{"type": "Data.BigNum", ...}`, **When** rendered, **Then** both markdown text and MetricCard component display in same slot without layout conflicts

---

### Edge Cases

- What happens when JSON has `{"parameters": {"cols": 5}}` but smart-grid layout only supports 2-4 columns? (Clamp to max 4, log warning)
- How does system handle invalid theme colors or missing theme field in JSON? (Fall back to `business` default theme)
- What if widget `parameters.text` contains unclosed HTML tags (e.g., `"<div>text"`)? (Slidev's markdown parser should isolate errors to that slide)
- How are CSS variable conflicts resolved when custom components define their own `--c-primary`? (Component-scoped variables take precedence via CSS specificity)
- What if JSON includes widgets for slots that don't exist in chosen layout (e.g., `"col4"` key when `cols: 3`)? (Renderer ignores unmapped widgets, logs warning)

## Data Model *(mandatory)*

### Input JSON Structure (from `src/generation/content/generator.py`)

The Slidev renderer consumes slide JSON generated by the existing content generation pipeline. This JSON follows the established schema used by the dummy layout engine:

```json
{
  "layout": "smart-grid",
  "parameters": {
    "cols": 3
  },
  "theme": {
    "primary_color": "#00ffa3",
    "accent_color": "#ff006e",
    "font_family": "Orbitron, monospace"
  },
  "style": {
    "gap": "24px",
    "padding": "32px"
  },
  "widgets": {
    "header": {
      "type": "Type.Heading",
      "parameters": {
        "text": "Q4 Revenue Analysis"
      }
    },
    "col1": {
      "type": "Data.BigNum",
      "parameters": {
        "text": "Revenue\n$5.2M",
        "preset": {
          "variant": "primary"
        }
      }
    },
    "col2": {
      "type": "Type.Body",
      "parameters": {
        "text": "Key insight text..."
      }
    },
    "col3": {
      "type": "Type.Code",
      "parameters": {
        "code": "SELECT * FROM revenue",
        "language": "sql"
      }
    }
  }
}
```

**Key Fields**:
- `layout`: Layout strategy name (e.g., "smart-grid", "hero-split", "full-bleed")
- `parameters`: Layout-specific parameters (e.g., `cols` for smart-grid)
- `theme`: Theme configuration (optional; renderer uses theme name from parameters if present)
- `widgets`: Dictionary mapping slot names to widget configurations
  - Each widget has `type` (e.g., "Type.Display", "Data.BigNum") and `parameters`
  - Widget types follow existing taxonomy: Type.* (typography), Data.* (metrics), Media.*

### Output Markdown Structure (Slidev Format)

The renderer translates the above JSON into Slidev Markdown with frontmatter and slot syntax:

```markdown
---
layout: smart-grid
theme: cyber
cols: 3
---

::header::
# Q4 Revenue Analysis
::

::col1::
<MetricCard label="Revenue" value="$5.2M" variant="primary" />
::

::col2::
Key insight text...
::

::col3::
```sql
SELECT * FROM revenue
```
::
```

**Slot Mapping Rules**:
- Slot names from JSON `widgets` keys map directly to `::slotName::` sections
- Widget content rendered based on widget type:
  - Typography widgets (Type.*): Markdown text with formatting
  - Data widgets (Data.BigNum): Converted to Vue components (MetricCard)
  - Code widgets (Type.Code): Markdown code blocks with language
- Theme translated from `theme.primary_color` to semantic theme name ("business" vs "cyber") or explicit theme parameter

## Requirements *(mandatory)*

### Functional Requirements

#### Layout Engine Integration
- **FR-001**: System MUST implement `LayoutEngine` protocol with `get_layout_documentation()` method returning Slidev-specific layout guide
- **FR-002**: Documentation MUST describe available layouts (Smart Grid, Hero Split, Full Bleed) with their slot names (e.g., "header", "col1", "col2" for smart-grid), parameters (e.g., `cols: 2-4`), and intended widget placements (LLM generates JSON with these slot names as keys in `widgets` dictionary)
- **FR-003**: Documentation MUST list widget type to Vue component mappings (e.g., Data.BigNum → MetricCard) so LLM knows which widget types trigger component conversion in renderer
- **FR-004**: Documentation MUST specify supported themes (`business`, `cyber`) with visual characteristic descriptions (colors, typography, effects) to guide LLM theme selection
- **FR-005**: Layout engine MUST register with `LayoutEngineRegistry` under name `"slidev"`

#### Renderer Implementation
- **FR-006**: Renderer MUST translate slide JSON (with layout, widgets, theme) to Slidev Markdown format
- **FR-007**: Renderer MUST generate frontmatter section with layout, theme, cols, title, subtitle, footer fields
- **FR-008**: Renderer MUST distribute widget content to appropriate slot sections using `::slotName::` syntax
- **FR-009**: Renderer MUST preserve markdown formatting in widget text (`==highlight==`, `**bold**`, code blocks)
- **FR-010**: Renderer MUST separate multi-slide output with `---` delimiters
- **FR-011**: Renderer MUST output `.md` files compatible with Slidev CLI (`slidev slides.md`)

#### Theme System
- **FR-012**: Themes MUST be defined via CSS variables in `SlideShell.vue` component
- **FR-013**: Business theme MUST use white background (#ffffff), blue primary (#2563eb), Inter font
- **FR-014**: Cyber theme MUST use dark background (#050505), neon green primary (#00ffa3), Orbitron font, grid pattern overlay, glow shadows
- **FR-015**: UnoCSS shortcuts MUST provide semantic class names (`bg-theme-base`, `text-theme-main`, `border-theme`, `shadow-theme`)
- **FR-016**: All Vue components MUST reference theme via CSS variables (`var(--c-primary)`) not hardcoded colors

#### Layout Implementations
- **FR-017**: Smart Grid layout MUST accept `cols` parameter (2-4) and generate CSS grid with specified columns
- **FR-018**: Smart Grid MUST provide `::header::` slot spanning full width
- **FR-019**: Smart Grid MUST provide `::col1::` through `::colN::` slots (where N = cols parameter)
- **FR-020**: Each grid cell MUST have rounded borders, theme-based background, and theme-consistent shadow

#### Component Library
- **FR-021**: `MetricCard` component MUST accept `label`, `value`, `variant` (primary/success/danger) props
- **FR-022**: `MetricCard` MUST display label in uppercase with muted color, value in large mono font with variant color
- **FR-023**: `StatusBadge` component MUST accept `status` (success/warning/error) and `text` props
- **FR-024**: `SlideShell` component MUST inject theme CSS variables, render header/footer from frontmatter, and wrap slot content

### Key Entities

- **SlidevLayoutEngine**: Implements LayoutEngine protocol, provides documentation about Slidev-specific layouts, slots, themes, and components. Manages layout strategy registration.
- **SlidevRenderer**: Translates slide JSON objects to Slidev Markdown format. Handles frontmatter generation, slot mapping, widget content distribution, and multi-slide concatenation.
- **SlideShell.vue**: Vue wrapper component that reads frontmatter theme parameter, injects CSS variables, renders header/footer, and wraps slide content.
- **SmartGrid.vue**: Layout component that parses `cols` parameter from frontmatter, generates CSS grid, and distributes slot content to grid cells.
- **MetricCard.vue**: Reusable Vue component for displaying labeled numeric values with theme-aware styling and variant support.
- **Theme Definition**: Object mapping theme names (business, cyber) to CSS variable sets (colors, fonts, shadows). Consumed by SlideShell to configure presentation appearance.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: LLM generates valid slide JSON (with correct layout, slot names, widget types) in single attempt with 95% success rate, and renderer produces Slidev Markdown without syntax errors requiring manual fixes
- **SC-002**: Theme switching from business to cyber completes instantly (<100ms) with zero component code changes required
- **SC-003**: Renderer processes 10-slide presentation JSON to Slidev Markdown in under 500ms
- **SC-004**: Slidev CLI successfully renders 100% of generated `.md` files without parse errors
- **SC-005**: Content prompts using `get_layout_documentation()` generate slide JSON 30% faster than previous HTML-based approach (measured by token count reduction in layout documentation)
- **SC-006**: Developers can add new theme variant (e.g., "minimal") by modifying only `SlideShell.vue` theme definitions without touching component code
- **SC-007**: 90% of common presentation widgets (Type.*, Data.*) render correctly using markdown + widget-to-component translation (MetricCard, StatusBadge, ProgressBar)
