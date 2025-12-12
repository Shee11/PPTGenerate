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
- [ ] T012 [P] Unit test for PatchableContextPydantic.patch() in tests/unit/test_patchable_context.py
- [X] T013 [P] Contract test for Theme JSON schema in tests/contract/test_style_schema.py
- [X] T014 [P] Contract test for Style JSON schema in tests/contract/test_style_schema.py

### Implementation for Foundation

- [X] T015 [P] Implement SizeClass enum in src/common/size_class.py
- [ ] T016 Implement PatchableContextPydantic base class in src/common/patchable_context_pydantic.py
- [X] T017 [P] Implement Theme model in src/layout/theme.py
- [X] T018 [P] Implement Style model in src/layout/style.py (depends on T017)
- [X] T019 [P] Implement Slot model in src/common/slot.py (depends on T015)
- [ ] T020 Implement Layouts collection in src/common/patchable_context_pydantic.py (depends on T016)
- [ ] T021 Implement Styles collection in src/common/patchable_context_pydantic.py (depends on T016)
- [X] T022 [P] Create BaseWidget abstract class in src/render/widgets/base.py (depends on T015)
- [X] T023 [P] Implement WidgetRegistry pattern in src/render/widgets/base.py (depends on T022)
- [X] T024 Create LayoutStrategy protocol in src/layout/strategies/base.py (depends on T019)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Layout Rendering (Priority: P1) 🎯 MVP

**Goal**: Render simple layouts (Bento.Standard, Swiss.Poster, Cinematic.Split_50_50) with basic widgets

**Independent Test**: Provide JSON configuration → verify HTML output with correct slot positions

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T025 [P] [US1] Contract test for Bento.Standard layout schema in tests/contract/test_layout_schema.py
- [X] T026 [P] [US1] Contract test for Swiss.Poster layout schema in tests/contract/test_layout_schema.py
- [X] T027 [P] [US1] Contract test for Cinematic.Split_50_50 layout schema in tests/contract/test_layout_schema.py
- [X] T028 [P] [US1] Integration test for Bento.Standard rendering in tests/integration/test_bento_rendering.py
- [X] T029 [P] [US1] Integration test for Swiss.Poster rendering in tests/integration/test_swiss_rendering.py
- [X] T030 [P] [US1] Integration test for Cinematic.Split_50_50 rendering in tests/integration/test_cinematic_rendering.py
- [X] T031 [P] [US1] Unit test for BentoStandardStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T032 [P] [US1] Unit test for SwissPosterStrategy slot definitions in tests/unit/test_strategy_slots.py
- [X] T033 [P] [US1] Unit test for CinematicSplit5050Strategy slot definitions in tests/unit/test_strategy_slots.py

### Implementation for User Story 1

- [X] T034 [P] [US1] Implement BentoStandardStrategy in src/layout/strategies/bento.py
- [X] T035 [P] [US1] Implement SwissPosterStrategy in src/layout/strategies/swiss.py
- [X] T036 [P] [US1] Implement CinematicSplit5050Strategy in src/layout/strategies/cinematic.py
- [X] T037 [US1] Implement LayoutEngine.calculate() core logic in src/layout/layout_engine.py (depends on T034, T035, T036)
- [X] T038 [P] [US1] Implement TypeDisplayWidget in src/render/widgets/typography.py
- [X] T039 [P] [US1] Implement TypeBodyWidget in src/render/widgets/typography.py
- [X] T040 [P] [US1] Implement DataBigNumWidget in src/render/widgets/data.py
- [X] T041 [US1] Create Jinja2 base template in src/render/templates/base.html.j2
- [X] T042 [P] [US1] Create Bento layout template in src/render/templates/layouts/bento.html.j2
- [X] T043 [P] [US1] Create Swiss layout template in src/render/templates/layouts/swiss.html.j2
- [X] T044 [P] [US1] Create Cinematic layout template in src/render/templates/layouts/cinematic.html.j2
- [X] T045 [P] [US1] Create typography widget template in src/render/templates/widgets/typography.html.j2
- [X] T046 [P] [US1] Create data widget template in src/render/templates/widgets/data.html.j2
- [X] T047 [US1] Implement HTMLRenderer.render() in src/render/html_renderer.py (depends on T041-T046)
- [X] T048 [US1] Implement RenderableLayout model in src/common/renderable_layout.py
- [X] T049 [US1] Wire LayoutEngine and HTMLRenderer in integration tests (depends on T037, T047)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

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

**Goal**: Support all layout variants (10+ total across Bento, Swiss, Cinematic)

**Independent Test**: Render each variant → verify slot roles, sizes, positions match specification

### Tests for User Story 4

- [X] T072 [P] [US4] Unit test for BentoHeroLeftStrategy in tests/unit/test_strategy_slots.py
- [X] T073 [P] [US4] Unit test for BentoHeroTopStrategy in tests/unit/test_strategy_slots.py
- [X] T074 [P] [US4] Unit test for BentoQuarterStrategy in tests/unit/test_strategy_slots.py
- [X] T075 [P] [US4] Unit test for SwissAsymmetryStrategy in tests/unit/test_strategy_slots.py
- [X] T076 [P] [US4] Unit test for SwissSplitTypoStrategy in tests/unit/test_strategy_slots.py
- [X] T077 [P] [US4] Unit test for CinematicFullBleedStrategy in tests/unit/test_strategy_slots.py
- [X] T078 [P] [US4] Unit test for CinematicSplit3070Strategy in tests/unit/test_strategy_slots.py
- [X] T079 [P] [US4] Integration test for all Bento variants in tests/integration/test_bento_rendering.py
- [X] T080 [P] [US4] Integration test for all Swiss variants in tests/integration/test_swiss_rendering.py
- [X] T081 [P] [US4] Integration test for all Cinematic variants in tests/integration/test_cinematic_rendering.py

### Implementation for User Story 4

- [X] T082 [P] [US4] Implement BentoHeroLeftStrategy in src/layout/strategies/bento.py
- [X] T083 [P] [US4] Implement BentoHeroTopStrategy in src/layout/strategies/bento.py
- [X] T084 [P] [US4] Implement BentoQuarterStrategy in src/layout/strategies/bento.py
- [X] T085 [P] [US4] Implement SwissAsymmetryStrategy in src/layout/strategies/swiss.py
- [X] T086 [P] [US4] Implement SwissSplitTypoStrategy in src/layout/strategies/swiss.py
- [X] T087 [P] [US4] Implement CinematicFullBleedStrategy in src/layout/strategies/cinematic.py
- [X] T088 [P] [US4] Implement CinematicSplit3070Strategy in src/layout/strategies/cinematic.py
- [X] T089 [US4] Register all strategies in LayoutEngine strategy registry (depends on T082-T088)
- [X] T090 [US4] Update layout templates to handle all variants (depends on T082-T088)

**Checkpoint**: All 10+ layout variants available; content creators have full flexibility

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

**Purpose**: Complete widget library (Typography, Data, Media)

### Tests for Remaining Widgets

- [X] T118 [P] Unit test for TypeListWidget in tests/unit/test_widgets/test_typography_widgets.py
- [X] T119 [P] Unit test for TypeQuoteWidget in tests/unit/test_widgets/test_typography_widgets.py
- [X] T120 [P] Unit test for DataProgressWidget in tests/unit/test_widgets/test_data_widgets.py
- [ ] T121 [P] Unit test for MediaFrameWidget in tests/unit/test_widgets/test_media_widgets.py
- [ ] T122 [P] Unit test for MediaCodeWidget in tests/unit/test_widgets/test_media_widgets.py
- [ ] T123 [P] Unit test for MediaIconWidget in tests/unit/test_widgets/test_media_widgets.py

### Implementation for Remaining Widgets

- [X] T124 [P] Implement TypeHeadingWidget in src/render/widgets/typography.py
- [X] T125 [P] Implement TypeListWidget in src/render/widgets/typography.py
- [X] T126 [P] Implement TypeQuoteWidget in src/render/widgets/typography.py
- [X] T127 [P] Implement DataTrendWidget in src/render/widgets/data.py
- [X] T128 [P] Implement DataProgressWidget in src/render/widgets/data.py
- [ ] T129 [P] Implement MediaFrameWidget in src/render/widgets/media.py
- [ ] T130 [P] Implement MediaCodeWidget in src/render/widgets/media.py
- [ ] T131 [P] Implement MediaIconWidget in src/render/widgets/media.py
- [ ] T132 [P] Create media widget template in src/render/templates/widgets/media.html.j2
- [ ] T133 Register all remaining widgets in WidgetRegistry (depends on T124-T131)

**Checkpoint**: Complete widget library with all 4 categories (Typography, Data, Media, Charts)

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
  └─→ US5 (P3 Charts) ← Requires US1 complete
  
CLI (Phase 8) ← Requires US1 + US2 complete
Remaining Widgets (Phase 9) ← Can happen in parallel with US3-US5
Polish (Phase 10) ← Requires all user stories complete
```

**Critical Path**: Setup → Foundation → US1 → US2 → CLI → Polish

**Parallel Opportunities**:
- After Foundation: US1, US2 can start simultaneously
- After US1: US3, US4, US5 can proceed in parallel
- Throughout: Test tasks can run in parallel with implementation tasks (TDD cycle)
- Phase 9 (Remaining Widgets) can overlap with US3-US5

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

**Parallel Track C** (US5):
- T091-T104 (charts)

All three tracks work on different widget categories and can proceed simultaneously.

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
3. **Milestone 3**: Add Parameters & Variants (US3, US4) - Customization & flexibility
4. **Milestone 4**: Add Charts (US5) - Data visualization
5. **Milestone 5**: Complete Widget Library (Phase 9) - Full feature set
6. **Milestone 6**: Polish (Phase 10) - Production ready

---

## Task Summary

- **Total Tasks**: 150
- **Test Tasks**: 54 (36%)
- **Implementation Tasks**: 96 (64%)
- **Parallelizable**: 102 tasks marked [P]
- **User Story Breakdown**:
  - Setup: 9 tasks
  - Foundation: 15 tasks (10 blocking)
  - US1 (P1): 25 tasks
  - US2 (P1): 10 tasks
  - US3 (P2): 12 tasks
  - US4 (P2): 19 tasks
  - US5 (P3): 14 tasks
  - CLI: 13 tasks
  - Remaining Widgets: 16 tasks
  - Polish: 17 tasks

---

## Notes

- All test tasks MUST fail initially (RED phase of TDD)
- Implementation tasks begin only after their test tasks are complete
- Each phase checkpoint is independently testable
- Parallel tasks ([P]) work on different files with no shared state
- Constitution compliance: TDD enforced, user stories independent, cross-platform Python
