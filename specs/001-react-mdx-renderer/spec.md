# Feature Specification: React MDX Presentation Renderer

**Feature Branch**: `001-react-mdx-renderer`  
**Created**: 2025-12-25  
**Status**: Draft  
**Input**: User description: "Create React layout & renderer with MDX as intermediate format. Build React components and layouts following src/paged/LAYOUT_DESIGN.md. Strictly Semantic generative presentation system where MDX handles structure & data, React handles layout & styling."

## Overview

Build a **Strictly Semantic** generative presentation system using React and MDX. The system enforces a clear separation:
- **MDX Layer**: Structure and data only (no styling)
- **React Layer**: Layout and styling (via Compound Components)

The Agent (LLM) outputs MDX code that uses **only** semantic components—no `div`, `className`, or `style` attributes allowed.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Semantic MDX Slides (Priority: P1)

As an LLM Agent, I can generate MDX slides using only the provided Layout and Block components, without any HTML tags or CSS styling, so that the output is consistently structured and easily renderable.

**Why this priority**: This is the core value proposition—enabling AI to generate valid, renderable presentations without knowing CSS/HTML details.

**Independent Test**: Generate 5 different slide types (cover, split, grid, chart, quote) using only semantic components and verify they render correctly.

**Acceptance Scenarios**:

1. **Given** a content prompt, **When** the Agent generates MDX, **Then** the output contains only Layout and Block components (no `div`, `span`, `className`, `style`)
2. **Given** a split layout requirement, **When** the Agent uses `<LayoutSplit>`, **Then** content is correctly placed in `<LayoutSplit.Left>` and `<LayoutSplit.Right>` slots
3. **Given** data for a chart, **When** the Agent uses `<ChartBar data={...}>`, **Then** the chart renders with correct data without any styling props

---

### User Story 2 - Render MDX to Interactive Presentation (Priority: P1)

As a User, I can view generated MDX content as a professional-looking presentation in the browser, so that I can present or share the content.

**Why this priority**: Without rendering, the MDX output has no value—this is essential for the complete pipeline.

**Independent Test**: Load a `.mdx` file and verify it renders as an interactive slide deck with navigation.

**Acceptance Scenarios**:

1. **Given** valid MDX content, **When** passed to the renderer, **Then** a slide deck is displayed with proper styling
2. **Given** a presentation with 10 slides, **When** rendered, **Then** user can navigate between slides using keyboard/UI controls
3. **Given** theme configuration, **When** slides render, **Then** all components use consistent colors, typography, and spacing

---

### User Story 3 - Apply Themes to Presentations (Priority: P2)

As a User, I can select from predefined themes (business, cyber, minimal, etc.) to change the visual style of my presentation without modifying the MDX content.

**Why this priority**: Theme flexibility increases reusability of content and supports different use cases.

**Independent Test**: Render the same MDX file with 3 different themes and verify visual differences while content remains identical.

**Acceptance Scenarios**:

1. **Given** MDX content, **When** theme is set to "business", **Then** slides use dark blue background with blue/purple accents
2. **Given** MDX content, **When** theme is changed from "business" to "minimal", **Then** slides update to white background with black text
3. **Given** a custom theme configuration, **When** applied, **Then** CSS variables are correctly set for all components

---

### User Story 4 - Export to Static HTML (Priority: P2)

As a User, I can export my presentation to a single HTML file (or folder with assets), so that I can share it without requiring a running server.

**Why this priority**: Enables offline viewing and easy distribution of presentations.

**Independent Test**: Export a presentation and open the HTML file in a browser without any server.

**Acceptance Scenarios**:

1. **Given** a rendered presentation, **When** export is triggered, **Then** a self-contained HTML file is generated
2. **Given** exported HTML, **When** opened in a browser, **Then** all slides, charts, and components render correctly
3. **Given** a presentation with images, **When** exported, **Then** images are either inlined or included in an assets folder

---

### User Story 5 - CLI Integration (Priority: P3)

As a Developer, I can use a CLI command to render MDX files to HTML, so that I can integrate this into CI/CD pipelines.

**Why this priority**: Automation enables scalable content generation workflows.

**Independent Test**: Run `uce-render --render state.json --project react-mdx -o output.html` and verify output.

**Acceptance Scenarios**:

1. **Given** a valid MDX file, **When** CLI is run with `--project react-mdx`, **Then** HTML output is generated
2. **Given** invalid MDX, **When** CLI is run, **Then** clear error message is shown with line number
3. **Given** `--verbose` flag, **When** CLI runs, **Then** progress and debug info is logged

---

### Edge Cases

- What happens when Agent outputs forbidden HTML tags? → Validation error with suggestion to use semantic component
- How does system handle missing component imports? → Auto-import from component library
- What happens with deeply nested components? → Max depth limit of 5 with warning
- How does system handle large data arrays in charts? → Display first 20 items with "show more" indicator
- What happens when theme is not found? → Fall back to "business" theme with console warning

---

## Requirements *(mandatory)*

### Functional Requirements

#### Architecture (L0-L3 Layers)

- **FR-001**: System MUST enforce a 4-layer architecture:
  - **L0 (Forbidden)**: Raw HTML/CSS (`div`, `span`, `className`, `style`)
  - **L1 (Layouts)**: Page structure components (`LayoutSplit`, `LayoutCover`, `LayoutGrid`)
  - **L2 (Blocks)**: Business logic components (`SmartList`, `ChartBar`, `MetricGroup`)
  - **L3 (Atoms)**: Typography elements (`Heading`, `Text`, `Callout`, `Image`)

- **FR-002**: Agent output MUST only use L1, L2, and L3 components; L0 elements MUST be rejected during validation

- **FR-003**: All L1 Layout components MUST use Compound Component pattern with named slots (e.g., `LayoutSplit.Left`, `LayoutSplit.Right`)

#### Layouts (L1)

- **FR-010**: System MUST provide at least 6 layout components:
  - `LayoutCover` - Title slide with title/subtitle props
  - `LayoutSplit` - Two-column with configurable ratio (1:1, 2:1, 1:2)
  - `LayoutGrid` - Multi-column grid (2-4 columns)
  - `LayoutFullBleed` - Full-screen background with overlay content
  - `LayoutTimeline` - Horizontal timeline with steps
  - `LayoutDashboard` - Metrics dashboard with chart area

- **FR-011**: Each layout MUST accept `theme` and `vibe` props for styling control

- **FR-012**: Layouts MUST NOT accept `className` or `style` props

#### Blocks (L2)

- **FR-020**: System MUST provide data visualization blocks:
  - `ChartBar` - Bar chart with `data`, `title`, `height` props
  - `ChartLine` - Line chart with `data`, `title`, `height` props
  - `ChartPie` - Pie/donut chart with `data`, `title` props
  - `MetricGroup` - KPI metrics with `data`, `cols` props
  - `TableData` - Data table with `columns`, `rows` props

- **FR-021**: System MUST provide content blocks:
  - `SmartList` - Enhanced list with icons, highlights
  - `QuoteBlock` - Blockquote with attribution
  - `ImageBlock` - Image with caption, size control
  - `CardGroup` - Group of cards with consistent styling

- **FR-022**: All blocks MUST accept semantic props only:
  - `size`: 'sm' | 'md' | 'lg' | 'full'
  - `variant`: 'default' | 'primary' | 'outline' | 'ghost'
  - `intent`: 'info' | 'warning' | 'success' | 'danger'

#### Atoms (L3)

- **FR-030**: System MUST provide typography atoms:
  - `Heading` - Headings with `level` prop (1-6)
  - `Text` - Paragraphs with `variant` prop (default, lead, caption)
  - `Callout` - Highlighted text with `intent` prop

- **FR-031**: Typography atoms MUST NOT accept `className` or `style` props

#### Theming

- **FR-040**: System MUST support 7 theme presets matching existing Slidev implementation:
  - business, cyber, minimal, academic, creative, duolingo, dark

- **FR-041**: Themes MUST define CSS custom properties for:
  - Background layers (base, surface, elevated)
  - Colors (primary, accent, success, warning, danger)
  - Text colors (text, text-muted, text-dim)
  - Typography (font-body, font-heading, font-mono)
  - Effects (shadows, border-radius)

- **FR-042**: Theme MUST be injectable at render time without modifying MDX content

#### Rendering Pipeline

- **FR-050**: System MUST render MDX to HTML via React/Next.js toolchain

- **FR-051**: Renderer MUST support state.json input format compatible with existing pipeline

- **FR-052**: Renderer MUST integrate with CLI via `--project react-mdx` option

- **FR-053**: System MUST generate MDX from state.json widgets structure

#### Validation

- **FR-060**: System MUST validate MDX before rendering to catch L0 violations

- **FR-061**: Validation errors MUST include:
  - Line number of violation
  - Forbidden element/attribute found
  - Suggested fix or alternative

### Key Entities

- **Slide**: Represents a single presentation page with layout, widgets, and theme reference
- **Layout**: Container component defining page structure with named slots
- **Block**: Self-contained UI component for data visualization or content grouping
- **Atom**: Basic typography element for text content
- **Theme**: Collection of CSS custom properties defining visual style
- **Vibe**: Density/complexity modifier ('minimal', 'clean', 'balanced', 'decorative', 'expressive')

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Agent can generate valid MDX for 95% of slide types without manual correction
- **SC-002**: Zero instances of `div`, `className`, or `style` in Agent-generated MDX
- **SC-003**: Presentation renders in under 2 seconds for a 20-slide deck
- **SC-004**: Theme switching applies to all components within 100ms
- **SC-005**: Exported HTML file size under 500KB for a 10-slide presentation (excluding images)
- **SC-006**: 100% parity with existing Slidev layout types (cover, split, grid, timeline, dashboard, etc.)
- **SC-007**: CLI export completes in under 30 seconds for a 50-slide presentation

### Quality Criteria

- **QC-001**: All layouts render identically across Chrome, Firefox, Safari
- **QC-002**: Presentation is keyboard-navigable (arrow keys, space)
- **QC-003**: Components meet WCAG 2.1 AA contrast requirements
- **QC-004**: MDX validation catches 100% of L0 violations before render

---

## Assumptions

- React 18+ and Next.js 14+ will be used for the runtime
- Tailwind CSS will be used internally for styling (hidden from Agent)
- MDX 3.x will be used for JSX-in-markdown support
- Existing state.json schema will be extended, not replaced
- Charts will use a React charting library (e.g., Recharts or Victory)

---

## Out of Scope

- Animation/transition effects between slides
- Real-time collaboration features
- PDF export (focus on HTML only)
- Custom component authoring by end users
- Mobile-responsive layouts (desktop 16:9 aspect ratio only)
