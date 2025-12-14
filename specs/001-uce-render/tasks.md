---
description: "Task list for UCE Rendering System implementation"
---

# Tasks: Universal Content Engine - Rendering System

**Input**: Design documents from `/specs/001-uce-render/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: This feature uses TDD (Test-Driven Development). All test tasks MUST be completed and failing before implementation tasks begin.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure (src/, tests/, cli/, examples/)
- [X] T002 Initialize Python project with pyproject.toml and setup.py
- [X] T003 [P] Configure pytest with pytest.ini and test fixtures directory
- [X] T004 [P] Add dependencies: Pydantic 2.x, Jinja2 3.x, Click 8.x, pytest 7.x
- [X] T005 [P] Create .gitignore for Python (__pycache/, .venv/, *.pyc, dist/)
- [X] T006 [P] Setup linting with ruff configuration in pyproject.toml
- [X] T007 [P] Configure mypy for type checking in pyproject.toml
- [X] T008 Create tests/fixtures/ directory with sample JSON files
- [X] T009 [P] Create src/__init__.py, src/common/__init__.py, src/layout/__init__.py, src/render/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundation

- [X] T010 [P] Contract test for SizeClass enum in tests/contract/test_size_class_schema.py
- [X] T011 [P] Unit test for SizeClass ordering in tests/unit/test_size_validation.py
- [X] T012 [P] Unit test for PatchableContextPydantic.patch() in tests/unit/test_patchable_context.py
- [X] T013 [P] Contract test for Theme JSON schema in tests/contract/test_style_schema.py
- [X] T014 [P] Contract test for Style JSON schema in tests/contract/test_style_schema.py
- [X] T014a [P] Unit test for Bounds model in tests/unit/test_bounds.py
- [X] T014b [P] Unit test for WidgetMeasurement utilities in tests/unit/test_measurement.py
- [X] T014c [P] Unit test for LayoutContext calculation in tests/unit/test_layout_context.py

### Implementation for Foundation

- [X] T015 [P] Implement SizeClass enum in src/common/size_class.py
- [ ] T016 Implement PatchableContextPydantic base class in src/common/patchable_context_pydantic.py
- [X] T017 [P] Implement Theme model in src/layout/theme.py
- [X] T018 [P] Implement Style model in src/layout/style.py (depends on T017)
- [X] T019 [P] Implement Slot model in src/common/slot.py (depends on T015)
- [X] T019a [P] Implement Bounds model in src/common/bounds.py
- [X] T019b [P] Implement MeasuredSize and WidgetMeasurement in src/common/measurement.py
- [X] T019c [P] Implement LayoutContext and LayoutStrategy protocol in src/layout/layout_protocol.py
- [ ] T020 Implement Layouts collection in src/common/patchable_context_pydantic.py (depends on T016)
- [ ] T021 Implement Styles collection in src/common/patchable_context_pydantic.py (depends on T016)
- [X] T022 [P] Create BaseWidget abstract class in src/widgets/base.py (depends on T015)
- [X] T022a [P] Add measure() abstract method to BaseWidget in src/widgets/base.py (depends on T019b)
- [X] T023 [P] Implement WidgetRegistry pattern in src/widgets/base.py (depends on T022)
- [X] T024 Create LayoutStrategy protocol in src/layout/strategies/base.py (depends on T019)
- [X] T024a Update LayoutStrategy protocol with calculate_layout() in src/layout/layout_protocol.py (depends on T019c)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Layout Rendering (Priority: P1) 🎯 MVP

**Goal**: Render simple layouts (Bento.Standard, Swiss.Poster, Cinematic.Split_50_50) with basic widgets using proper auto-layout

**Independent Test**: Provide JSON configuration → verify HTML output with absolute widget positions calculated by LayoutEngine

**⚠️ CRITICAL AUTO-LAYOUT**: Layout strategies must calculate absolute (x, y, width, height) positions. Widgets must measure content size. LayoutEngine coordinates the two-phase process: measure → layout.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T025 [P] [US1] Contract test for Bento.Standard layout schema in tests/contract/test_layout_schema.py
- [X] T026 [P] [US1] Contract test for Swiss.Poster layout schema in tests/contract/test_layout_schema.py
- [X] T027 [P] [US1] Contract test for Cinematic.Split_50_50 layout schema in tests/contract/test_layout_schema.py
- [X] T027a [P] [US1] Unit test for BentoStandardStrategy.calculate_layout() in tests/unit/test_bento_layout_algorithm.py
- [X] T027b [P] [US1] Unit test for SwissPosterStrategy.calculate_layout() in tests/unit/test_swiss_layout_algorithm.py
- [X] T027c [P] [US1] Unit test for CinematicSplit5050Strategy.calculate_layout() in tests/unit/test_cinematic_layout_algorithm.py
- [X] T028 [P] [US1] Integration test for Bento.Standard rendering in tests/integration/test_bento_rendering.py
- [X] T029 [P] [US1] Integration test for Swiss.Poster rendering in tests/integration/test_swiss_rendering.py
- [X] T030 [P] [US1] Integration test for Cinematic.Split_50_50 rendering in tests/integration/test_cinematic_rendering.py
- [X] T031 [P] [US1] Unit test for BentoStandardStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T032 [P] [US1] Unit test for SwissPosterStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T033 [P] [US1] Unit test for CinematicSplit5050Strategy slot definitions in tests/unit/test_strategy_slots.py
- [ ] T033a [P] [US1] Integration test verifying bounds in RenderableLayout in tests/integration/test_layout_bounds.py
- [X] T033b [P] [US1] Unit test for spacing parsing utilities (px, %, rem) in tests/unit/test_spacing_utils.py

### Implementation for User Story 1

**Auto-Layout Core** (NEW - Critical):
- [X] T034a [P] [US1] Implement spacing parser (px/% → pixels) in src/common/spacing_utils.py
- [X] T034b [P] [US1] Update RenderableLayout.WidgetAssignment to include bounds in src/common/renderable_layout.py

**Widget Measurement** (NEW - Critical):
- [X] T038a [P] [US1] Implement measure() in TypeDisplayWidget in src/widgets/typography.py
- [X] T039a [P] [US1] Implement measure() in TypeBodyWidget in src/widgets/typography.py
- [X] T040a [P] [US1] Implement measure() in DataBigNumWidget in src/widgets/data.py

**Layout Strategies with Auto-Layout** (UPDATED - Critical):
- [X] T034 [P] [US1] Implement BentoStandardStrategy with calculate_layout() in src/layout/strategies/bento.py
- [X] T035 [P] [US1] Implement SwissPosterStrategy with calculate_layout() in src/layout/strategies/swiss.py
- [X] T036 [P] [US1] Implement CinematicSplit5050Strategy with calculate_layout() in src/layout/strategies/cinematic.py

**LayoutEngine Refactor** (UPDATED - Critical):
- [X] T037 [US1] Rewrite LayoutEngine.calculate() with two-phase auto-layout in src/layout/layout_engine.py:
  - Phase 1: Call widget.measure() for each widget → MeasuredSize
  - Create LayoutContext with canvas dimensions, margins, spacing
  - Phase 2: Call strategy.calculate_layout() → Bounds map
  - Create WidgetAssignments with calculated bounds
  - Return RenderableLayout with absolute positions
  - (depends on T034, T035, T036, T034a, T034b, T038a, T039a, T040a)

**Widget Implementation** (Existing):
- [X] T038 [P] [US1] Implement TypeDisplayWidget in src/widgets/typography.py
- [X] T039 [P] [US1] Implement TypeBodyWidget in src/widgets/typography.py
- [X] T040 [P] [US1] Implement DataBigNumWidget in src/widgets/data.py

**Templates - Absolute Positioning** (UPDATED - Critical):
- [ ] T041 [US1] Update Jinja2 base template with absolute positioning in src/render/templates/base.html.j2
- [ ] T042 [P] [US1] Update Bento layout template to use bounds in src/render/templates/layouts/bento.html.j2
- [ ] T043 [P] [US1] Update Swiss layout template to use bounds in src/render/templates/layouts/swiss.html.j2
- [ ] T044 [P] [US1] Update Cinematic layout template to use bounds in src/render/templates/layouts/cinematic.html.j2
- [X] T045 [P] [US1] Create typography widget template in src/render/templates/widgets/typography.html.j2
- [X] T046 [P] [US1] Create data widget template in src/render/templates/widgets/data.html.j2

**Rendering** (UPDATED):
- [ ] T047 [US1] Update HTMLRenderer.render() to pass bounds to templates in src/render/html_renderer.py (depends on T041-T046)
- [X] T048 [US1] Implement RenderableLayout model in src/common/renderable_layout.py
- [ ] T049 [US1] Wire LayoutEngine auto-layout with HTMLRenderer in integration tests (depends on T037, T047)

**Checkpoint**: At this point, User Story 1 should be fully functional with proper auto-layout - LayoutEngine calculates absolute positions, not CSS Grid

---

## Phase 4: User Story 2 - T-Shirt Size Validation (Priority: P1)

**Goal**: Enforce size constraints (S/M/L/XL) and provide clear error messages

**Independent Test**: Attempt invalid widget-to-slot assignments → verify rejection with specific error

### Tests for User Story 2

- [X] T050 [P] [US2] Unit test for size constraint validation logic in tests/unit/test_size_validation.py
- [X] T051 [P] [US2] Integration test for size violation detection in tests/integration/test_size_validation_e2e.py
- [X] T052 [P] [US2] Unit test for SizeConstraintError formatting in tests/unit/test_size_validation.py
- [X] T053 [P] [US2] Unit test for MissingReferenceError formatting in tests/unit/test_size_validation.py

### Implementation for User Story 2

- [X] T054 [P] [US2] Implement SizeConstraintError exception in src/common/exceptions.py
- [X] T055 [P] [US2] Implement MissingReferenceError exception in src/common/exceptions.py
- [X] T056 [US2] Add size validation to LayoutEngine.calculate() in src/layout/layout_engine.py (depends on T054)
- [X] T057 [US2] Add reference validation to LayoutEngine.calculate() in src/layout/layout_engine.py (depends on T055)
- [X] T058 [P] [US2] Add error message formatting with suggestions in src/common/exceptions.py
- [X] T059 [US2] Add comprehensive validation error tests in tests/integration/test_size_validation_e2e.py

**Checkpoint**: Size validation prevents broken layouts; all constraints enforced

---

## Phase 5: User Story 3 - Widget Parameter Application (Priority: P2)

**Goal**: Apply widget-specific parameters (colors, alignment, styles) correctly

**Independent Test**: Render same widget with different parameters → verify each parameter affects only its property

### Tests for User Story 3

- [X] T060 [P] [US3] Unit test for TypeDisplay parameter validation in tests/unit/test_widgets/test_typography_widgets.py
- [X] T061 [P] [US3] Unit test for DataBigNum parameter validation in tests/unit/test_widgets/test_data_widgets.py
- [X] T062 [P] [US3] Integration test for style parameter application in tests/integration/test_style_application.py
- [X] T063 [P] [US3] Unit test for Theme-to-CSS conversion in tests/unit/test_style_resolution.py

### Implementation for User Story 3

- [X] T064 [P] [US3] Add parameter schema to TypeDisplayWidget in src/render/widgets/typography.py
- [X] T065 [P] [US3] Add parameter schema to TypeHeadingWidget in src/render/widgets/typography.py
- [X] T066 [P] [US3] Add parameter schema to TypeBodyWidget in src/render/widgets/typography.py
- [X] T067 [P] [US3] Add parameter schema to DataBigNumWidget in src/render/widgets/data.py
- [X] T068 [P] [US3] Add parameter schema to DataTrendWidget in src/render/widgets/data.py
- [X] T069 [US3] Implement Style resolution to CSS in src/layout/style.py
- [X] T070 [US3] Apply resolved styles in HTMLRenderer templates (depends on T069)
- [X] T071 [US3] Add parameter application to widget templates in src/render/templates/widgets/

**Checkpoint**: Widget parameters enable customization while maintaining structure

---

## Phase 6: User Story 4 - Multi-Variant Layout Support (Priority: P2)

**Goal**: Support all layout variants (10+ total across Bento, Swiss, Cinematic) with proper auto-layout algorithms

**Independent Test**: Render each variant → verify absolute bounds match specification

**⚠️ CRITICAL**: Each strategy variant must implement calculate_layout() with its specific algorithm (fixed grid, proportional split, content-driven, full-bleed)

### Tests for User Story 4

- [X] T072a [P] [US4] Unit test for BentoHeroLeftStrategy.calculate_layout() in tests/unit/test_bento_layout_algorithm.py
- [X] T073a [P] [US4] Unit test for BentoHeroTopStrategy.calculate_layout() in tests/unit/test_bento_layout_algorithm.py
- [X] T074a [P] [US4] Unit test for BentoQuarterStrategy.calculate_layout() in tests/unit/test_bento_layout_algorithm.py
- [X] T072 [P] [US4] Unit test for BentoHeroLeftStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T073 [P] [US4] Unit test for BentoHeroTopStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T074 [P] [US4] Unit test for BentoQuarterStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T075 [P] [US4] Unit test for SwissAsymmetryStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T076 [P] [US4] Unit test for SwissSplitTypoStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T077 [P] [US4] Unit test for CinematicFullBleedStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T078 [P] [US4] Unit test for CinematicSplit3070Strategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T079 [P] [US4] Integration test for all Bento variants in tests/integration/test_bento_rendering.py
- [X] T080 [P] [US4] Integration test for all Swiss variants in tests/integration/test_swiss_rendering.py
- [X] T081 [P] [US4] Integration test for all Cinematic variants in tests/integration/test_cinematic_rendering.py

### Implementation for User Story 4

**Layout Algorithms** (UPDATED - each needs calculate_layout()):
- [X] T082 [P] [US4] Implement BentoHeroLeftStrategy with 2/3-1/3 split algorithm in src/layout/strategies/bento.py
- [X] T083 [P] [US4] Implement BentoHeroTopStrategy with top hero + footer grid in src/layout/strategies/bento.py
- [X] T084 [P] [US4] Implement BentoQuarterStrategy with 2x2 equal grid in src/layout/strategies/bento.py
- [X] T085 [P] [US4] Implement SwissAsymmetryStrategy with asymmetric positioning in src/layout/strategies/swiss.py
- [X] T086 [P] [US4] Implement SwissSplitTypoStrategy with split layout in src/layout/strategies/swiss.py
- [X] T087 [P] [US4] Implement CinematicFullBleedStrategy with single full-canvas widget in src/layout/strategies/cinematic.py
- [X] T088 [P] [US4] Implement CinematicSplit3070Strategy with 30/70 proportional split in src/layout/strategies/cinematic.py
- [X] T089 [US4] Register all strategies in LayoutEngine strategy registry (depends on T082-T088)
- [ ] T090 [US4] Update layout templates to render absolute positioned widgets (depends on T082-T088)

**Checkpoint**: All 10+ layout variants with proper auto-layout algorithms; each calculates absolute widget bounds

---

## Phase 6: User Story 6 - Extended Layout Families (Priority: P2)

**Goal**: Support additional layout families (Edit, Data.KPI, Focus, Strategy) with specialized positioning algorithms

**Independent Test**: Render each extended layout → verify absolute bounds match specification

**Layout Families**:
- **Edit Family**: Overlap and collage effects (Edit.Overlap_Left, Edit.Magazine_Collage, Edit.Staggered)
- **Data.KPI Family**: Metric displays (Data.KPI_Row)
- **Focus Family**: Radial and minimal layouts (Focus.Solar_System, Focus.Offset_Title)
- **Strategy Family**: Strategic planning layouts (to be defined)

### Tests for User Story 6

- [X] T151 [P] [US6] Unit test for EditOverlapLeftStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T152 [P] [US6] Unit test for EditMagazineCollageStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T153 [P] [US6] Unit test for EditStaggeredStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T154 [P] [US6] Unit test for DataKPIRowStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T155 [P] [US6] Unit test for FocusSolarSystemStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T156 [P] [US6] Unit test for FocusOffsetTitleStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T157 [P] [US6] Unit test for EditOverlapLeftStrategy.calculate_layout() in tests/unit/test_edit_layout_algorithm.py
- [X] T158 [P] [US6] Unit test for EditMagazineCollageStrategy.calculate_layout() in tests/unit/test_edit_layout_algorithm.py
- [X] T159 [P] [US6] Unit test for EditStaggeredStrategy.calculate_layout() in tests/unit/test_edit_layout_algorithm.py
- [X] T160 [P] [US6] Unit test for DataKPIRowStrategy.calculate_layout() in tests/unit/test_data_layout_algorithm.py
- [X] T161 [P] [US6] Unit test for FocusSolarSystemStrategy.calculate_layout() in tests/unit/test_focus_layout_algorithm.py
- [X] T162 [P] [US6] Unit test for FocusOffsetTitleStrategy.calculate_layout() in tests/unit/test_focus_layout_algorithm.py
- [ ] T163 [P] [US6] Integration test for Edit family layouts in tests/integration/test_edit_rendering.py
- [ ] T164 [P] [US6] Integration test for Focus family layouts in tests/integration/test_focus_rendering.py

### Implementation for User Story 6

**Edit Family Strategies** (Overlap & Collage Effects):
- [X] T165 [P] [US6] Implement EditOverlapLeftStrategy in src/layout/strategies/edit.py:
  - Slots: back (XL, full background), card (L, overlapping left side)
  - Algorithm: Background fills content area, card positioned at 20% from left with 60% width, creating 2.5D depth
  - Use case: Layered card designs, product showcases with context

- [X] T166 [P] [US6] Implement EditMagazineCollageStrategy in src/layout/strategies/edit.py:
  - Slots: hero (XL, anchor center), sticker_1 to sticker_N (S, random positions)
  - Algorithm: Hero centered, stickers randomly scattered around with rotation and offset
  - Use case: Mood boards, creative collages, playful compositions

- [X] T167 [P] [US6] Implement EditStaggeredStrategy in src/layout/strategies/edit.py:
  - Slots: item_1 (M, left), item_2 (M, right offset down), item_3 (M, left offset down)
  - Algorithm: Z-pattern staggered positioning, each item offset vertically from previous
  - Use case: Multi-step processes, alternating image-text flows

**Data.KPI Family Strategies** (Metric Displays):
- [X] T168 [P] [US6] Implement DataKPIRowStrategy in src/layout/strategies/data.py:
  - Slots: header (M, top span), kpi_1 to kpi_4 (S, bottom row)
  - Algorithm: Header 30% height top, KPIs evenly distributed in bottom 70%
  - Use case: Dashboard headers, quarterly reports, metric overviews

**Focus Family Strategies** (Radial & Minimal):
- [X] T169 [P] [US6] Implement FocusSolarSystemStrategy in src/layout/strategies/focus.py:
  - Slots: sun (XL, center), planet_1 to planet_N (S, orbital positions)
  - Algorithm: Sun centered, planets positioned in circular orbit with equal angular spacing
  - Use case: Ecosystem diagrams, mind maps, concept relationships

- [X] T170 [P] [US6] Implement FocusOffsetTitleStrategy in src/layout/strategies/focus.py:
  - Slots: main (XL, bottom-left corner)
  - Algorithm: Title positioned in bottom-left 10% area, 90% whitespace
  - Use case: Minimalist chapter dividers, section breaks

**Templates & Registration**:
- [ ] T171 [P] [US6] Create Edit layout template in src/render/templates/layouts/edit.html.j2
- [ ] T172 [P] [US6] Create Focus layout template in src/render/templates/layouts/focus.html.j2
- [ ] T173 [P] [US6] Create Data.KPI layout template in src/render/templates/layouts/data.html.j2
- [X] T174 [US6] Register Edit/Focus/Data.KPI strategies in LayoutEngine (depends on T165-T170)

**Checkpoint**: Extended layout families enable creative, data-driven, and strategic compositions

---

## Phase 7: User Story 5 - Chart Data Binding (Priority: P3)

**Goal**: Render chart widgets (Bar, Line, Pie, Radar, Sankey) with data binding

**Independent Test**: Provide data payloads → verify visualizations accurately represent data

### Tests for User Story 5

- [ ] T091 [P] [US5] Unit test for ChartBarWidget in tests/unit/test_widgets/test_chart_widgets.py
- [ ] T092 [P] [US5] Unit test for ChartLineWidget in tests/unit/test_widgets/test_chart_widgets.py
- [ ] T093 [P] [US5] Unit test for ChartPieWidget in tests/unit/test_widgets/test_chart_widgets.py
- [ ] T094 [P] [US5] Unit test for ChartRadarWidget in tests/unit/test_widgets/test_chart_widgets.py
- [ ] T095 [P] [US5] Unit test for ChartSankeyWidget in tests/unit/test_widgets/test_chart_widgets.py
- [ ] T096 [P] [US5] Integration test for chart data binding in tests/integration/test_chart_rendering.py

### Implementation for User Story 5

- [ ] T097 [P] [US5] Implement ChartBarWidget in src/render/widgets/charts.py
- [ ] T098 [P] [US5] Implement ChartLineWidget in src/render/widgets/charts.py
- [ ] T099 [P] [US5] Implement ChartPieWidget in src/render/widgets/charts.py
- [ ] T100 [P] [US5] Implement ChartRadarWidget in src/render/widgets/charts.py
- [ ] T101 [P] [US5] Implement ChartSankeyWidget in src/render/widgets/charts.py
- [ ] T102 [US5] Create chart widget template in src/render/templates/widgets/charts.html.j2
- [ ] T103 [US5] Add atom_data binding to HTMLRenderer in src/render/html_renderer.py
- [ ] T104 [US5] Register chart widgets in WidgetRegistry (depends on T097-T101)

**Checkpoint**: Charts enable data-driven content; all 5 chart types supported

---

## Phase 8: CLI Implementation

**Purpose**: Command-line interface for end-to-end rendering

### Tests for CLI

- [X] T105 [P] Contract test for CLI exit codes in tests/contract/test_cli_contract.py
- [X] T106 [P] Contract test for CLI error message format in tests/contract/test_cli_contract.py
- [X] T107 [P] Contract test for CLI JSON output format in tests/contract/test_cli_contract.py
- [X] T108 [P] Contract test for CLI validation mode in tests/contract/test_cli_contract.py

### Implementation for CLI

- [X] T109 [P] Implement Click command structure in cli/uce_render.py
- [X] T110 [P] Add file loading and JSON validation in cli/uce_render.py
- [X] T111 [P] Add --output option handler in cli/uce_render.py
- [X] T112 [P] Add --format option (html/json) in cli/uce_render.py
- [X] T113 [P] Add --validate-only flag in cli/uce_render.py
- [X] T114 [P] Add --verbose logging in cli/uce_render.py
- [X] T115 Implement error handling and exit codes in cli/uce_render.py
- [X] T116 Add CLI entry point to pyproject.toml
- [X] T117 Create CLI help text and examples in cli/uce_render.py

**Checkpoint**: CLI enables end-users to render layouts via command line

---

## Phase 9: Remaining Widgets

**Purpose**: Complete widget library (Typography, Data, Media) with measure() implementation for all

**⚠️ CRITICAL**: All widgets must implement measure() method for auto-layout to work

### Tests for Remaining Widgets

- [X] T118 [P] Unit test for TypeListWidget in tests/unit/test_widgets/test_typography_widgets.py
- [X] T119 [P] Unit test for TypeQuoteWidget in tests/unit/test_widgets/test_typography_widgets.py
- [X] T120 [P] Unit test for DataProgressWidget in tests/unit/test_widgets/test_data_widgets.py
- [ ] T121 [P] Unit test for MediaFrameWidget in tests/unit/test_widgets/test_media_widgets.py
- [ ] T122 [P] Unit test for MediaCodeWidget in tests/unit/test_widgets/test_media_widgets.py
- [ ] T123 [P] Unit test for MediaIconWidget in tests/unit/test_widgets/test_media_widgets.py
- [ ] T123a [P] Unit test for TypeHeadingWidget.measure() in tests/unit/test_widget_measurement.py
- [ ] T123b [P] Unit test for TypeListWidget.measure() in tests/unit/test_widget_measurement.py
- [ ] T123c [P] Unit test for TypeQuoteWidget.measure() in tests/unit/test_widget_measurement.py
- [ ] T123d [P] Unit test for DataTrendWidget.measure() in tests/unit/test_widget_measurement.py
- [ ] T123e [P] Unit test for DataProgressWidget.measure() in tests/unit/test_widget_measurement.py

### Implementation for Remaining Widgets

**Widget Classes** (Existing):
- [X] T124 [P] Implement TypeHeadingWidget in src/widgets/typography.py
- [X] T125 [P] Implement TypeListWidget in src/widgets/typography.py
- [X] T126 [P] Implement TypeQuoteWidget in src/widgets/typography.py
- [X] T127 [P] Implement DataTrendWidget in src/widgets/data.py
- [X] T128 [P] Implement DataProgressWidget in src/widgets/data.py
- [X] T129 [P] Implement MediaFrameWidget in src/widgets/media.py
- [X] T130 [P] Implement MediaCodeWidget in src/widgets/media.py
- [X] T131 [P] Implement MediaIconWidget in src/widgets/media.py

**Widget Measurement** (NEW - Critical for auto-layout):
- [X] T124a [P] Implement measure() in TypeHeadingWidget in src/widgets/typography.py
- [X] T125a [P] Implement measure() in TypeListWidget in src/widgets/typography.py
- [X] T126a [P] Implement measure() in TypeQuoteWidget in src/widgets/typography.py
- [X] T127a [P] Implement measure() in DataTrendWidget in src/widgets/data.py
- [X] T128a [P] Implement measure() in DataProgressWidget in src/widgets/data.py
- [X] T129a [P] Implement measure() in MediaFrameWidget (fixed size) in src/widgets/media.py
- [X] T130a [P] Implement measure() in MediaCodeWidget (text-based) in src/widgets/media.py
- [X] T131a [P] Implement measure() in MediaIconWidget (fixed size) in src/widgets/media.py

**Templates**:
- [X] T132 [P] Create media widget template in src/render/templates/widgets/media.html.j2
- [X] T133 Register all remaining widgets in WidgetRegistry (depends on T124-T131)

**Checkpoint**: Complete widget library with all 4 categories (Typography, Data, Media, Charts) - all widgets can measure their content size

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Performance, documentation, and examples

### Documentation & Examples

- [ ] T134 [P] Create executive-dashboard example in examples/executive-dashboard/
- [ ] T135 [P] Create product-launch example in examples/product-launch/
- [ ] T136 [P] Create comparison-view example in examples/comparison-view/
- [X] T137 [P] Write example README files with use cases
- [ ] T138 [P] Generate sample HTML outputs for examples
- [X] T139 Create main README.md with quickstart and examples
- [ ] T140 [P] Add docstrings to all public APIs (LayoutEngine, HTMLRenderer, widgets)
- [ ] T141 [P] Generate API documentation from docstrings

### Performance & Quality

- [ ] T142 Performance test for simple layouts (<100ms) in tests/performance/test_render_performance.py
- [ ] T143 Performance test for complex layouts (<500ms) in tests/performance/test_render_performance.py
- [ ] T144 Memory test (<50MB per render) in tests/performance/test_memory_usage.py
- [ ] T145 [P] Implement Jinja2 template caching in src/render/html_renderer.py
- [ ] T146 [P] Add widget HTML memoization in src/render/widgets/base.py
- [X] T147 Run ruff linter and fix all issues
- [X] T148 Run mypy type checker and fix all issues
- [X] T149 Verify 90% test coverage with pytest-cov
- [ ] T150 Create comprehensive integration test suite covering all user stories

---

## Dependency Graph

**Story Completion Order**:

```
Setup (Phase 1)
  ↓
Foundation (Phase 2) ← BLOCKING for all user stories
  ↓
  ├─→ US1 (P1 MVP) ← Can start after Foundation
  ├─→ US2 (P1 Validation) ← Can start after Foundation, enhances US1
  ├─→ US3 (P2 Parameters) ← Requires US1 complete
  ├─→ US4 (P2 Variants) ← Requires US1 complete
  ├─→ US6 (P2 Extended Layouts) ← Requires US1 complete (NEW)
  └─→ US5 (P3 Charts) ← Requires US1 complete
  
CLI (Phase 8) ← Requires US1 + US2 complete
Remaining Widgets (Phase 9) ← Can happen in parallel with US3-US6
Polish (Phase 10) ← Requires all user stories complete
```

**Critical Path**: Setup → Foundation → US1 → US2 → CLI → Polish

**Parallel Opportunities**:
- After Foundation: US1, US2 can start simultaneously
- After US1: US3, US4, US5, US6 can proceed in parallel
- Throughout: Test tasks can run in parallel with implementation tasks (TDD cycle)
- Phase 9 (Remaining Widgets) can overlap with US3-US6

---

## Parallel Execution Examples

### After Foundation Complete:

**Parallel Track A** (US1):
- T025-T033 (tests)
- T034-T049 (implementation)

**Parallel Track B** (US2):
- T050-T053 (tests)
- T054-T059 (implementation)

Both tracks can proceed independently as they work on different files.

### After US1 Complete:

**Parallel Track A** (US3):
- T060-T071 (parameters)

**Parallel Track B** (US4):
- T072-T090 (variants)

**Parallel Track C** (US6):
- T151-T174 (extended layouts)

**Parallel Track D** (US5):
- T091-T104 (charts)

All four tracks work on different widget categories and layout families, can proceed simultaneously.

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Phase 1 + 2 + 3 + 4** = Core MVP
- Setup + Foundation + US1 (Basic Rendering) + US2 (Size Validation)
- **Result**: Can render 3 layout variants with 3 widgets, enforcing size constraints
- **Time Estimate**: ~40% of total tasks (60 tasks)
- **Value**: Fully functional rendering system, independently testable

### Incremental Delivery

1. **Milestone 1**: MVP (Phases 1-4) - Basic rendering with validation
2. **Milestone 2**: Add CLI (Phase 8) - Command-line usability
3. **Milestone 3**: Add Parameters & Variants (US3, US4, US6) - Customization & flexibility
4. **Milestone 4**: Add Extended Layouts (US6) - Creative & specialized compositions
5. **Milestone 5**: Add Charts (US5) - Data visualization
6. **Milestone 6**: Complete Widget Library (Phase 9) - Full feature set
7. **Milestone 7**: Polish (Phase 10) - Production ready

---

## Auto-Layout Architecture Summary

**⚠️ CRITICAL DESIGN PRINCIPLE**: The LayoutEngine performs explicit auto-layout calculation and is **renderer-agnostic**. It does NOT defer positioning to CSS Grid or any rendering technology.

### Two-Phase Auto-Layout Process

**Phase 1: Measurement**
- Each widget implements `measure(style, max_width, max_height) → MeasuredSize`
- Widgets calculate required space based on content (text length, font size, padding)
- Example: TypeDisplayWidget measures text with font metrics
- Example: DataBigNumWidget measures number + label dimensions
- Example: MediaFrameWidget returns fixed image dimensions

**Phase 2: Layout Calculation**
- Each layout strategy implements `calculate_layout(widgets, context) → Dict[role, Bounds]`
- Strategies calculate absolute (x, y, width, height) positions
- Algorithm types:
  - **Fixed Grid** (Bento.Standard): Equal cell divisions
  - **Proportional Split** (Bento.HeroLeft, Cinematic): Percentage-based
  - **Content-Driven** (Swiss.Asymmetry): Based on measured widget sizes
  - **Full Bleed** (Swiss.Poster): Single widget fills canvas

**LayoutEngine Orchestration**
```python
def calculate():
    # 1. Measure all widgets
    for widget in widgets:
        style = resolve_style(widget.type)
        measured_size = widget.measure(style, max_width, max_height)
    
    # 2. Create layout context
    context = LayoutContext(
        canvas_width, canvas_height,
        margin_x, margin_y, gutter,
        header_height, footer_height
    )
    
    # 3. Call strategy's layout algorithm
    bounds_map = strategy.calculate_layout(widgets, context)
    
    # 4. Create assignments with absolute bounds
    assignments = [
        WidgetAssignment(
            role=role,
            widget=widget,
            slot=slot,
            bounds=bounds  # Absolute position
        )
    ]
```

**Rendering**
- Templates receive `bounds` with absolute positions
- Use `position: absolute` with `left`, `top`, `width`, `height`
- NO CSS Grid, NO flexbox for positioning (only for widget internals)

### Key Files

**Foundation**:
- `src/common/bounds.py` - Bounds(x, y, width, height) model
- `src/common/measurement.py` - MeasuredSize, WidgetMeasurement utilities
- `src/layout/layout_protocol.py` - LayoutContext, LayoutStrategy protocol
- `src/common/spacing_utils.py` - Parse "40px", "15%" to pixels

**Widgets** (must implement `measure()`):
- `src/widgets/typography.py` - 5 text widgets
- `src/widgets/data.py` - 3 data widgets
- `src/widgets/media.py` - 3 media widgets (future)
- `src/widgets/charts.py` - 5 chart widgets (future)

**Layout Strategies** (must implement `calculate_layout()`):
- `src/layout/strategies/bento.py` - 4 variants
- `src/layout/strategies/swiss.py` - 3 variants
- `src/layout/strategies/cinematic.py` - 3 variants

**Orchestration**:
- `src/layout/layout_engine.py` - Two-phase auto-layout orchestrator
- `src/render/html_renderer.py` - Applies bounds to templates
- `src/render/templates/` - Use absolute positioning

---

## Task Summary

- **Total Tasks**: ~200 (added ~25 auto-layout tasks + ~24 extended layout tasks)
- **Test Tasks**: ~79 (added measurement/layout algorithm tests + extended layout tests)
- **Implementation Tasks**: ~121
- **Parallelizable**: ~115 tasks marked [P]
- **User Story Breakdown**:
  - Setup: 9 tasks
  - Foundation: 15 tasks (10 blocking)
  - US1 (P1): 25 tasks
  - US2 (P1): 10 tasks
  - US3 (P2): 12 tasks
  - US4 (P2): 19 tasks
  - US6 (P2): 24 tasks (NEW - Extended Layouts)
  - US5 (P3): 14 tasks
  - CLI: 13 tasks
  - Remaining Widgets: 16 tasks
  - Polish: 17 tasks

**Extended Layout Families (US6)**:
- Edit Family: 3 strategies (Overlap_Left, Magazine_Collage, Staggered)
- Data.KPI Family: 1 strategy (KPI_Row)
- Focus Family: 2 strategies (Solar_System, Offset_Title)
- Total: 6 new layout strategies with specialized positioning algorithms

---

## Phase 12: User Story 7 - Widget Style Presets (Priority: P2) ✨

**Goal**: Enable inline visual customization of widgets through preset system with 22 variants across 4 categories (Surface, Shape, Fill, Effect)

**Independent Test**: Configure widget with preset field in JSON, render HTML, verify preset CSS classes applied

**Design Documents**: data-model.md (WidgetPreset entity), preset-quickstart.md, contracts/preset-schema.json

### Setup for Presets (Documentation already complete ✅)

- [X] T501 Create preset schema in specs/001-uce-render/contracts/preset-schema.json
- [X] T502 Create widget config schema in specs/001-uce-render/contracts/widget-config-schema.json
- [X] T503 Update data-model.md with WidgetPreset entity and 22 variant definitions
- [X] T504 Update research.md with preset pass-through architecture
- [X] T505 Create preset-quickstart.md user guide

### Data Model Updates (Pass-Through Fields)

- [X] T506 [P] [US7] Add `preset: Dict[str, str] | None` field to SlotAssignment in src/common/renderable_layout.py
- [X] T507 [P] [US7] Verify Slide model supports Dict[str, Any] for widget configs (no changes needed to src/common/slide.py)

**Checkpoint**: Data models ready to pass preset through pipeline

### Layout Engine Pass-Through

- [X] T508 [US7] Update LayoutEngine.calculate_slots() to extract preset from widget_config and pass to SlotAssignment in src/layout/layout_engine.py

**Checkpoint**: Preset flows Slide → LayoutEngine → RenderableLayout

### CSS Preset Definitions

- [X] T509 [US7] Create src/render/static/presets.css with base structure and CSS variables
- [X] T510 [P] [US7] Define 6 Surface variants (Flat, Elevated, Outline, Glass, Sunken, NeoBrutal) in presets.css
- [X] T511 [P] [US7] Define 6 Shape variants (Sharp, Rounded, Curve, Pill, Squircle, Organic) in presets.css
- [X] T512 [P] [US7] Define 6 Fill variants (Solid_Brand, Subtle, Gradient_Linear, Gradient_Mesh, Pattern_Dot, Noise) in presets.css
- [X] T513 [P] [US7] Define 4 Effect variants (Duotone, Glitch, Glow, Tape) in presets.css
- [X] T514 [US7] Add SVG clip-path definitions for Squircle and Organic shapes in presets.css
- [ ] T515 [US7] Test preset CSS combinations for visual conflicts (manual verification)

**Checkpoint**: All 22 preset CSS classes defined with theme color support

### HTML Renderer Updates

- [X] T516 [US7] Update HTMLRenderer.render_widget() to pass preset from SlotAssignment to template context in src/render/html_renderer.py
- [X] T517 [US7] Link presets.css in HTML template head section in src/render/templates/base.html.j2

**Checkpoint**: Templates receive preset data and CSS is loaded

### Widget Template Updates

- [X] T518 [P] [US7] Update Type.Display template to apply preset classes in src/render/templates/widgets/typography.html.j2
- [X] T519 [P] [US7] Update Type.Heading template to apply preset classes in src/render/templates/widgets/typography.html.j2
- [X] T520 [P] [US7] Update Type.Body template to apply preset classes in src/render/templates/widgets/typography.html.j2
- [X] T521 [P] [US7] Update Type.Quote template to apply preset classes in src/render/templates/widgets/typography.html.j2
- [X] T522 [P] [US7] Update Type.List template to apply preset classes in src/render/templates/widgets/typography.html.j2
- [X] T523 [P] [US7] Update Data.BigNum template to apply preset classes in src/render/templates/widgets/data.html.j2
- [X] T524 [P] [US7] Update Data.Trend template to apply preset classes in src/render/templates/widgets/data.html.j2
- [X] T525 [P] [US7] Update Data.Progress template to apply preset classes in src/render/templates/widgets/data.html.j2
- [X] T526 [P] [US7] Update Media.Frame template to apply preset classes in src/render/templates/widgets/media.html.j2
- [X] T527 [P] [US7] Update Media.Icon template to apply preset classes in src/render/templates/widgets/media.html.j2
- [X] T528 [P] [US7] Update Media.Code template to apply preset classes in src/render/templates/widgets/media.html.j2

**Template Pattern** (consistent across all widgets):
```jinja
<div class="widget {{ widget.widget_type|lower|replace('.', '-') }}
            preset-surface-{{ preset.surface|lower|default('flat') if preset else 'flat' }}
            preset-shape-{{ preset.shape|lower|default('rounded') if preset else 'rounded' }}
            {% if preset and preset.fill %}preset-fill-{{ preset.fill|lower }}{% endif %}
            {% if preset and preset.effect %}preset-effect-{{ preset.effect|lower }}{% endif %}">
  <!-- existing widget content -->
</div>
```

**Checkpoint**: All widget templates apply preset CSS classes

### Example Updates

- [X] T529 [P] [US7] Add preset examples to examples/cyber-tech.json (3 widgets: Display, Heading, BigNum)
- [ ] T530 [P] [US7] Create examples/preset-showcase.json demonstrating all 22 variants
- [ ] T531 [US7] Regenerate cyber-tech.html and verify preset visual effects

**Checkpoint**: Examples showcase preset capabilities

### Documentation Updates

- [ ] T532 [P] [US7] Update main README.md with preset system section
- [ ] T533 [P] [US7] Add preset examples to existing quickstart.md
- [ ] T534 [P] [US7] Create visual preset reference (optional HTML showcase page)

**Checkpoint**: User Story 7 complete - preset system fully functional

---

## Phase 13: Polish & Cross-Cutting Concerns

- All test tasks MUST fail initially (RED phase of TDD)
- Implementation tasks begin only after their test tasks are complete
- Each phase checkpoint is independently testable
- Parallel tasks ([P]) work on different files with no shared state
- Constitution compliance: TDD enforced, user stories independent, cross-platform Python


---

## Task Summary (Updated with Presets)

- **Total Tasks**: ~234 (base: 200 + presets: 34)
- **Preset Tasks**: 34 (5 complete, 29 remaining)
  - Setup: 5 tasks 
  - Data Models: 2 tasks
  - Layout Engine: 1 task
  - CSS Definitions: 7 tasks
  - Renderer: 2 tasks
  - Templates: 11 tasks
  - Examples: 3 tasks
  - Documentation: 3 tasks
- **Parallelizable Preset Tasks**: 25 of 34 (74%)

**Widget Style Presets (US7)** :
- **Categories**: Surface (6), Shape (6), Fill (6), Effect (4) = 22 variants
- **Architecture**: Pass-through pattern with CSS class-based rendering
- **MVP Time**: ~45 minutes for core functionality
- **Files Modified**: renderable_layout.py, layout_engine.py, html_renderer.py, 11 widget templates, presets.css (new)

