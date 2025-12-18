---
description: "Task breakdown for Slidev Layout Engine implementation"
---

# Tasks: Slidev Layout Engine with Vue Renderer

**Input**: Design documents from `specs/001-slidev-engine/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Organization**: Tasks organized by user story (US1-US6) to enable independent implementation and testing. Each phase delivers a testable increment.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3, US4, US5, US6)
- File paths are absolute from repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure

- [X] T001 Create Python package structure: `src/layout/slidev/` with `__init__.py`, `layout_engine.py`, and empty `strategies/` directory
- [X] T002 Create Python package structure: `src/render/slidev/` with `__init__.py`, `markdown_renderer.py`, and `templates/` directory
- [X] T003 [P] Create test directory structure: `tests/contract/`, `tests/integration/`, `tests/unit/` for Slidev-specific tests
- [X] T004 [P] Create Slidev project structure: `slidev-project/` with subdirectories `layouts/`, `components/`, `styles/`
- [X] T005 [P] Initialize `slidev-project/package.json` with Slidev, Vue 3, UnoCSS dependencies
- [X] T006 [P] Create `slidev-project/uno.config.ts` with UnoCSS configuration skeleton

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Register SlidevLayoutEngine with LayoutEngineRegistry in `src/layout/slidev/__init__.py` (name: "slidev")
- [X] T008 [P] Create Jinja2 template files: `src/render/slidev/templates/frontmatter.j2`, `src/render/slidev/templates/slot.j2`, `src/render/slidev/templates/slide.j2`
- [X] T009 [P] Create base SlideShell.vue component in `slidev-project/components/SlideShell.vue` with CSS variable injection logic (business/cyber themes)
- [X] T010 Add theme CSS variable definitions to SlideShell.vue: business theme (white bg #ffffff, blue primary #2563eb, Inter font)
- [X] T011 Add theme CSS variable definitions to SlideShell.vue: cyber theme (dark bg #050505, neon green primary #00ffa3, Orbitron font, grid overlay)
- [X] T012 [P] Create UnoCSS shortcuts in `slidev-project/uno.config.ts`: `bg-theme-base`, `text-theme-main`, `border-theme`, `shadow-theme`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - LLM Generates Slide JSON for Slidev Layouts (Priority: P1) 🎯 MVP

**Goal**: Enable LLM to generate valid slide JSON with correct slot names by implementing `get_layout_documentation()` method that returns comprehensive Slidev layout guide

**Independent Test**: Call `SlidevLayoutEngine.get_layout_documentation()`, verify output includes smart-grid layout with slot names ("header", "col1"-"col4"), widget type mappings (Data.BigNum → MetricCard), and theme descriptions (business/cyber)

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Contract test for LayoutEngine protocol compliance in `tests/contract/test_slidev_layout_engine_schema.py` - verify SlidevLayoutEngine has `get_layout_documentation()` classmethod, verify `calculate()` raises NotImplementedError
- [X] T014 [P] [US1] Contract test for layout documentation schema in `tests/contract/test_slidev_layout_engine_schema.py` - verify output contains "smart-grid", "hero-split", "full-bleed", "Data.BigNum", "Type.Display", "business", "cyber" keywords
- [X] T015 [P] [US1] Integration test for LLM prompt integration in `tests/integration/test_slidev_layout_documentation.py` - verify documentation is >500 chars, contains slot names for each layout, widget-to-component mappings present

### Implementation for User Story 1

- [X] T016 [P] [US1] Implement SlidevLayoutEngine class skeleton in `src/layout/slidev/layout_engine.py` with LayoutEngine protocol inheritance
- [X] T017 [US1] Implement `get_layout_documentation()` classmethod in `src/layout/slidev/layout_engine.py` - return formatted string with Smart Grid layout description (slots: header, col1-col4, cols parameter 2-4)
- [X] T018 [US1] Add Hero Split layout documentation to `get_layout_documentation()` - slots: left, right, ratio parameter (e.g., "60-40", "50-50")
- [X] T019 [US1] Add Full Bleed layout documentation to `get_layout_documentation()` - slot: default (unnamed), align parameter (top/center/bottom)
- [X] T020 [US1] Add widget-to-component mappings to documentation - Typography widgets (Type.Display, Type.Heading, Type.Body, Type.List, Type.Quote, Type.Code) render as markdown
- [X] T021 [US1] Add data widget mappings to documentation - Data.BigNum → MetricCard, Data.Progress → ProgressBar, Data.Trend → StatusBadge components
- [X] T022 [US1] Add theme descriptions to documentation - business theme (blue/white, Inter, professional), cyber theme (green/dark, Orbitron, tech aesthetic)
- [X] T023 [US1] Implement `calculate()` method in `src/layout/slidev/layout_engine.py` - raise NotImplementedError with message "Slidev engine does not use calculate() - use SlidevRenderer directly"

**Checkpoint**: User Story 1 complete - LLM can now generate valid slide JSON with correct slot names and widget types based on layout documentation

---

## Phase 4: User Story 2 - Theme Switching Without Component Changes (Priority: P1)

**Goal**: Enable instant theme switching (<100ms) by changing frontmatter parameter, with all components automatically adapting via CSS variables

**Independent Test**: Create slide with `theme: "business"`, change to `theme: "cyber"`, verify colors/fonts/shadows update without component code changes

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T024 [P] [US2] Unit test for theme resolution in `tests/unit/test_slidev_theme_resolution.py` - verify hex color #2563eb maps to "business" theme, #00ffa3 maps to "cyber" theme
- [X] T025 [P] [US2] Unit test for theme CSS variable injection in `tests/unit/test_slidev_theme_resolution.py` - verify SlideShell.vue sets --c-primary, --c-bg-base, --font-family based on theme parameter
- [X] T026 [P] [US2] Integration test for theme switching in `tests/integration/test_slidev_theme_switching.py` - verify business → cyber changes background from white to dark, primary from blue to green

### Implementation for User Story 2

- [X] T027 [P] [US2] Implement theme resolution helper in `src/render/slidev/markdown_renderer.py` - function to map hex colors to semantic theme names (business/cyber)
- [X] T028 [P] [US2] Add theme parameter to frontmatter generation logic in `src/render/slidev/markdown_renderer.py` - include `theme: "business"` or `theme: "cyber"` in YAML
- [X] T029 [US2] Update SlideShell.vue to read `theme` from frontmatter and inject corresponding CSS variables (--c-primary, --c-bg-base, --c-accent, --font-family, --shadow-theme)
- [X] T030 [US2] Add theme-specific styling to SlideShell.vue: business theme uses clean shadows (`0 1px 3px rgba(0,0,0,0.1)`), cyber theme uses neon glow (`0 0 20px var(--c-primary)`)
- [X] T031 [US2] Add grid pattern overlay CSS for cyber theme in SlideShell.vue: `background-image: linear-gradient(...)` for tech aesthetic

**Checkpoint**: User Story 2 complete - Theme switching works instantly via CSS variables without component code changes

---

## Phase 5: User Story 3 - Layout Engine Provides Documentation for LLM Prompts (Priority: P1)

**Goal**: Integrate SlidevLayoutEngine with existing content generation pipeline so LLMs can retrieve layout documentation and generate valid slide JSON

**Independent Test**: From `src/generation/content/generator.py`, call `LayoutEngineRegistry.get_engine("slidev").get_layout_documentation()`, verify LLM receives complete guide with layouts, slots, widgets, themes

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T032 [P] [US3] Integration test for engine registration in `tests/integration/test_slidev_engine_registration.py` - verify `LayoutEngineRegistry.list_engines()` includes "slidev" after import
- [ ] T033 [P] [US3] Integration test for documentation retrieval in `tests/integration/test_slidev_engine_registration.py` - verify `LayoutEngineRegistry.get_engine("slidev").get_layout_documentation()` returns string >500 chars
- [ ] T034 [P] [US3] Contract test for documentation content in `tests/contract/test_slidev_layout_engine_schema.py` - verify documentation includes example JSON showing slot names as keys in widgets dictionary

### Implementation for User Story 3

- [ ] T035 [US3] Verify registration in `src/layout/slidev/__init__.py` calls `LayoutEngineRegistry.register("slidev", SlidevLayoutEngine)` on module import
- [ ] T036 [US3] Add usage examples to documentation in `src/layout/slidev/layout_engine.py` - show JSON snippet with `"widgets": {"header": {...}, "col1": {...}}` structure
- [ ] T037 [US3] Add best practices section to documentation - guide LLMs to use slot names from layout descriptions as keys in widgets dictionary

**Checkpoint**: User Story 3 complete - Content generation pipeline can retrieve Slidev layout documentation and LLMs generate valid JSON

---

## Phase 6: User Story 4 - Render Slide JSON to Slidev Markdown Files (Priority: P2)

**Goal**: Implement SlidevRenderer to transform slide JSON into Slidev markdown with frontmatter, slots, and widget-to-component translation

**Independent Test**: Pass slide JSON (with smart-grid layout, 3 columns, mixed widgets) to renderer, receive valid `.md` file that Slidev can parse and display

### Tests for User Story 4

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T038 [P] [US4] Contract test for Renderer protocol methods in `tests/contract/test_slidev_renderer_schema.py` - verify SlidevRenderer has `render()`, `render_single_slide()`, `render_multi_slide()` methods
- [X] T039 [P] [US4] Unit test for frontmatter generation in `tests/unit/test_slidev_frontmatter_generation.py` - verify YAML output has layout, theme, cols fields from JSON input
- [X] T040 [P] [US4] Unit test for widget-to-markdown mapping in `tests/unit/test_slidev_widget_mapping.py` - verify Type.Display renders as plain text, Type.Heading as `# Heading`, Type.Code as code block
- [X] T041 [P] [US4] Unit test for widget-to-component mapping in `tests/unit/test_slidev_widget_mapping.py` - verify Data.BigNum renders as `<MetricCard ... />`, Data.Progress as `<ProgressBar ... />`
- [X] T042 [P] [US4] Integration test for single slide rendering in `tests/integration/test_slidev_json_to_markdown.py` - verify full JSON input produces parseable markdown with frontmatter + slots
- [X] T043 [P] [US4] Integration test for Slidev CLI compatibility in `tests/integration/test_slidev_cli_compatibility.py` - verify generated .md file can be parsed by Slidev without errors

### Implementation for User Story 4

- [X] T044 [P] [US4] Implement SlidevRenderer class skeleton in `src/render/slidev/markdown_renderer.py` with `__init__()` method (load Jinja2 templates)
- [X] T045 [US4] Implement `render()` method in `src/render/slidev/markdown_renderer.py` - dispatch to `render_single_slide()` or `render_multi_slide()` based on input type
- [X] T046 [US4] Implement frontmatter template in `src/render/slidev/templates/frontmatter.j2` - render YAML with layout, theme, and parameters fields
- [X] T047 [US4] Implement slot template in `src/render/slidev/templates/slot.j2` - render `::slotName::` wrapper with widget content inside
- [X] T048 [US4] Implement `_generate_frontmatter()` helper in `src/render/slidev/markdown_renderer.py` - extract layout, resolve theme, merge parameters into YAML dict
- [X] T049 [US4] Implement `_render_widget()` helper in `src/render/slidev/markdown_renderer.py` - dispatch widget rendering based on type (Type.* vs Data.*)
- [X] T050 [US4] Implement `_render_typography_widget()` in `src/render/slidev/markdown_renderer.py` - handle Type.Display (plain text), Type.Heading (# markdown), Type.Body (paragraph), Type.List (bullets), Type.Quote (blockquote), Type.Code (code blocks)
- [X] T051 [US4] Implement `_render_data_widget()` in `src/render/slidev/markdown_renderer.py` - handle Data.BigNum (MetricCard), Data.Progress (ProgressBar), Data.Trend (StatusBadge) as Vue component tags
- [X] T052 [US4] Implement `render_single_slide()` method in `src/render/slidev/markdown_renderer.py` - combine frontmatter + slot sections using templates
- [X] T053 [US4] Add markdown preservation logic to `_render_typography_widget()` - preserve `**bold**`, `==highlight==`, inline code from widget text
- [X] T054 [US4] Add validation in `render_single_slide()` - raise ValueError if `layout` or `widgets` fields missing from JSON

**Checkpoint**: User Story 4 complete - Renderer transforms slide JSON to valid Slidev markdown with frontmatter and slots

---

## Phase 7: User Story 5 - Support Multi-Slide Presentations (Priority: P2)

**Goal**: Enable renderer to process arrays of slide JSON and output multi-slide presentations with `---` separators

**Independent Test**: Generate 5-slide presentation JSON array with alternating themes, verify Slidev renders 5 distinct slides with correct theme per slide

### Tests for User Story 5

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T055 [P] [US5] Integration test for multi-slide rendering in `tests/integration/test_slidev_multi_slide_rendering.py` - verify 3-slide JSON array produces markdown with 2 `---` separators
- [ ] T056 [P] [US5] Integration test for theme variation in `tests/integration/test_slidev_multi_slide_rendering.py` - verify slides with different theme parameters maintain individual frontmatter sections
- [ ] T057 [P] [US5] Performance test in `tests/integration/test_slidev_multi_slide_rendering.py` - verify 10-slide array renders in <500ms (SC-003)

### Implementation for User Story 5

- [ ] T058 [US5] Implement `render_multi_slide()` method in `src/render/slidev/markdown_renderer.py` - iterate slides, call `render_single_slide()` for each, join with `\n---\n` separator
- [ ] T059 [US5] Add slide count validation in `render_multi_slide()` - handle empty array (return empty string or raise ValueError)
- [ ] T060 [US5] Optimize rendering performance - implement Jinja2 template caching in `__init__()` to meet <500ms target for 10 slides

**Checkpoint**: User Story 5 complete - Multi-slide presentations render correctly with individual frontmatter and separators

---

## Phase 8: User Story 6 - Widget-to-Component Translation for Structured Data (Priority: P3)

**Goal**: Implement Vue components (MetricCard, StatusBadge, ProgressBar) that renderer uses for Data.* widgets, with theme-aware styling

**Independent Test**: LLM generates slide JSON with Data.BigNum, Data.Progress, Type.Body widgets in same layout, renderer outputs MetricCard, ProgressBar mixed with markdown, all render correctly with theme styling

### Tests for User Story 6

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T061 [P] [US6] Unit test for MetricCard props in `tests/unit/test_slidev_vue_components.py` - verify component accepts label, value, variant props
- [ ] T062 [P] [US6] Unit test for StatusBadge props in `tests/unit/test_slidev_vue_components.py` - verify component accepts status, text props
- [ ] T063 [P] [US6] Unit test for ProgressBar props in `tests/unit/test_slidev_vue_components.py` - verify component accepts label, value, status props
- [ ] T064 [P] [US6] Integration test for mixed widget rendering in `tests/integration/test_slidev_mixed_widgets.py` - verify slot with Type.Body + Data.BigNum renders both markdown and MetricCard
- [ ] T065 [P] [US6] Integration test for component theme styling in `tests/integration/test_slidev_component_theming.py` - verify MetricCard variant="primary" uses --c-primary CSS variable (blue in business, green in cyber)

### Implementation for User Story 6

- [ ] T066 [P] [US6] Create MetricCard.vue component in `slidev-project/components/MetricCard.vue` - define props (label: string, value: string, variant: "primary"|"success"|"danger")
- [ ] T067 [P] [US6] Create StatusBadge.vue component in `slidev-project/components/StatusBadge.vue` - define props (status: "success"|"warning"|"error", text: string)
- [ ] T068 [P] [US6] Create ProgressBar.vue component in `slidev-project/components/ProgressBar.vue` - define props (label: string, value: number, status: "success"|"warning"|"error")
- [ ] T069 [US6] Implement MetricCard.vue template - display label (uppercase, muted color), value (large mono font with variant color from theme)
- [ ] T070 [US6] Implement MetricCard.vue styling - use CSS variables (var(--c-primary), var(--c-success), var(--c-danger)) based on variant prop
- [ ] T071 [US6] Implement StatusBadge.vue template - display text with background color based on status prop
- [ ] T072 [US6] Implement StatusBadge.vue styling - use theme CSS variables for status colors (success: green, warning: yellow, error: red)
- [ ] T073 [US6] Implement ProgressBar.vue template - display label, progress bar with percentage fill based on value prop
- [ ] T074 [US6] Implement ProgressBar.vue styling - use theme CSS variables for bar background and status-based fill color
- [ ] T075 [US6] Add component imports to `slidev-project/components/` - ensure MetricCard, StatusBadge, ProgressBar are auto-imported by Slidev
- [ ] T076 [US6] Update `_render_data_widget()` in `src/render/slidev/markdown_renderer.py` - parse widget `parameters.text` to extract label/value for MetricCard (split on newline)
- [ ] T077 [US6] Add prop extraction logic to `_render_data_widget()` - map widget `preset.variant` to component variant prop, widget `status` to component status prop

**Checkpoint**: User Story 6 complete - Data widgets render as Vue components with theme-aware styling, mixed with markdown content

---

## Phase 9: Vue Layout Components (Foundational for All Stories)

**Goal**: Implement Slidev Vue layout components (SmartGrid, HeroSplit, FullBleed) that frontmatter references and slot content populates

**Independent Test**: Create .md file with `layout: smart-grid`, `cols: 3`, and `::header::`, `::col1::`, `::col2::`, `::col3::` slots, verify Slidev renders 3-column grid layout

### Tests for Vue Layouts

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T078 [P] [US4] Integration test for SmartGrid layout in `tests/integration/test_slidev_layouts.py` - verify `cols: 2` creates 2-column grid, `cols: 4` creates 4-column grid
- [X] T079 [P] [US4] Integration test for HeroSplit layout in `tests/integration/test_slidev_layouts.py` - verify `ratio: "60-40"` creates left panel 60% width, right panel 40% width
- [X] T080 [P] [US4] Integration test for FullBleed layout in `tests/integration/test_slidev_layouts.py` - verify `align: "center"` centers content vertically

### Implementation for Vue Layouts

- [X] T081 [P] [US4] Create SmartGrid.vue layout in `slidev-project/layouts/smart-grid.vue` - define slots (header, col1, col2, col3, col4), read `cols` from frontmatter
- [X] T082 [P] [US4] Create HeroSplit.vue layout in `slidev-project/layouts/hero-split.vue` - define slots (left, right), read `ratio` parameter from frontmatter
- [X] T083 [P] [US4] Create FullBleed.vue layout in `slidev-project/layouts/full-bleed.vue` - define default slot, read `align` parameter for vertical alignment
- [X] T084 [US4] Implement SmartGrid.vue CSS - use `display: grid`, `grid-template-columns: repeat(var(--cols), 1fr)`, full-width header spanning all columns
- [X] T085 [US4] Add grid cell styling to SmartGrid.vue - rounded borders (8px), theme background (`bg-theme-base`), theme shadow (`shadow-theme`)
- [X] T086 [US4] Implement HeroSplit.vue CSS - use flexbox with ratio-based widths (parse `ratio` parameter like "60-40" into flex percentages)
- [X] T087 [US4] Implement FullBleed.vue CSS - use flexbox with vertical alignment based on `align` parameter (top/center/bottom → flex-start/center/flex-end)
- [X] T088 [US4] Add theme-aware styling to all layouts - reference CSS variables for colors, borders, shadows (var(--c-bg-base), var(--border-theme))

**Checkpoint**: Vue layout components complete - Slidev can render smart-grid, hero-split, full-bleed layouts with correct slot distribution

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements, edge case handling, performance optimization, documentation

- [ ] T089 [P] Add edge case handling to renderer - clamp `cols` parameter to 2-4 range if exceeded, log warning
- [ ] T090 [P] Add edge case handling to renderer - fall back to "business" theme if `theme` field missing or invalid color
- [ ] T091 [P] Add validation to renderer - ignore widgets for non-existent slots (e.g., "col4" when `cols: 3`), log warning
- [ ] T092 [P] Add error handling to renderer - escape unclosed HTML tags in widget text to prevent Slidev parse errors
- [ ] T093 Add performance optimization - implement Jinja2 template caching with `jinja2.Environment(cache_size=100)` in renderer init
- [ ] T094 [P] Create example .md output file in `slidev-project/slides.md` - demonstrate smart-grid layout with mixed widgets
- [ ] T095 [P] Add inline code comments to `src/layout/slidev/layout_engine.py` - explain slot naming conventions, layout parameter ranges
- [ ] T096 [P] Add inline code comments to `src/render/slidev/markdown_renderer.py` - explain widget type dispatch logic, theme resolution
- [ ] T097 Update `specs/001-slidev-engine/quickstart.md` - add "Running Your First Slidev Presentation" section with CLI commands
- [ ] T098 Create integration example in quickstart.md - show complete workflow from LLM JSON generation to Slidev rendering

---

## Dependencies & Parallel Execution

### Story Completion Order (Sequential Dependencies)

```
Phase 1 (Setup) → Phase 2 (Foundation)
    ↓
Phase 3 (US1 - Layout Documentation) ← Must complete FIRST
    ↓
┌───────────────────────────────────────┐
│   Parallel Track 1        Parallel Track 2        Parallel Track 3   │
│   Phase 4 (US2 - Theme)   Phase 5 (US4 - Renderer)  Phase 9 (Vue Layouts) │
└───────────────────────────────────────┘
    ↓
Phase 6 (US3 - Integration) ← Depends on US1 + US2
    ↓
Phase 7 (US5 - Multi-Slide) ← Depends on US4
    ↓
Phase 8 (US6 - Components) ← Depends on US4 + US2
    ↓
Phase 10 (Polish)
```

### Parallel Execution Examples

**After Phase 2 Complete**, these can run simultaneously:

- **US1 Implementation Group** (T016-T023): Layout engine implementation - all tasks operate on same file, sequential
- **Foundation Group** (T007-T012): Setup tasks in different directories (Python vs Vue), fully parallel

**After US1 Complete**, these tracks are independent:

- **Theme Track** (US2): T024-T031 - SlideShell.vue, theme resolution
- **Renderer Track** (US4): T038-T054 - markdown_renderer.py, Jinja2 templates
- **Vue Layouts Track** (Phase 9): T078-T088 - SmartGrid.vue, HeroSplit.vue, FullBleed.vue

All three tracks can proceed in parallel as they modify different files.

**After US4 Complete**:

- US5 (Multi-Slide) and US6 (Components) can start in parallel
- Both depend on renderer being functional but modify different aspects

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Include**: User Story 1, User Story 2, User Story 4, Phase 9 (Vue Layouts)

**Rationale**: This combination delivers:
- LLM can generate valid slide JSON (US1)
- Theme switching works (US2)
- Single slides render to Slidev (US4)
- Layouts display correctly (Phase 9)

**Exclude from MVP**: US5 (multi-slide), US6 (data components), US3 (full integration)

**MVP Demo**: LLM generates smart-grid slide JSON with 3 columns, renderer produces .md file, Slidev displays with business theme, developer switches to cyber theme, colors update instantly.

### Incremental Delivery Plan

1. **Sprint 1** (MVP): Complete Phase 1-2, US1, US2, US4, Phase 9 → Deliverable: Single slide generation with theme switching
2. **Sprint 2**: Complete US3, US5 → Deliverable: Multi-slide presentations integrated with content pipeline
3. **Sprint 3**: Complete US6, Phase 10 → Deliverable: Full feature with data components and polish

---

## Task Summary

- **Total Tasks**: 98
- **Setup Phase**: 6 tasks (T001-T006)
- **Foundation Phase**: 6 tasks (T007-T012)
- **User Story 1**: 11 tasks (3 tests + 8 implementation)
- **User Story 2**: 8 tasks (3 tests + 5 implementation)
- **User Story 3**: 6 tasks (3 tests + 3 implementation)
- **User Story 4**: 17 tasks (6 tests + 11 implementation)
- **User Story 5**: 6 tasks (3 tests + 3 implementation)
- **User Story 6**: 18 tasks (5 tests + 13 implementation)
- **Vue Layouts (Phase 9)**: 11 tasks (3 tests + 8 implementation)
- **Polish Phase**: 10 tasks (edge cases, optimization, docs)

**Parallel Opportunities**: 42 tasks marked [P] can run in parallel with other tasks in same phase

**Independent Test Criteria Per Story**:
- US1: Documentation contains all layouts, slots, widgets, themes
- US2: Theme switching changes colors/fonts without code changes
- US3: Engine registered, documentation retrievable from registry
- US4: Single slide JSON → valid Slidev markdown parseable by CLI
- US5: Multi-slide array → markdown with separators, correct theme per slide
- US6: Data widgets render as Vue components with theme styling

**Format Validation**: ✅ All 98 tasks follow checklist format (checkbox, ID, optional [P], optional [Story], description with file paths)

---

**Tasks Status**: ✅ COMPLETE  
**Ready for Checklist Generation**: ✅ YES  
**Next Step**: Run `/speckit.checklist` to generate quality checklists for each phase
