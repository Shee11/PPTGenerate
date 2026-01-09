# Tasks: Extended Chart Types with Intelligent Selection

**Input**: Design documents from `/specs/003-extended-chart-types/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Tests are NOT explicitly requested in the feature specification. Implementation tasks do not include test tasks, but testing strategy is defined in plan.md for optional TDD approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md project structure:
- React components: `src/paged/render/react/components/blocks/`
- Python generation: `src/generation/content/`
- Layout engine: `src/paged/layout/react/`
- Types: `src/paged/render/react/types/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and type definitions

- [X] T001 Create chart type definitions in src/paged/render/react/types/chart.ts
- [X] T002 [P] Create shared chart CSS variables in src/paged/render/react/styles/chart-theme.css
- [X] T003 [P] Verify Recharts dependency is installed and up-to-date in package.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Export ChartType and ChartDataPoint types from src/paged/render/react/types/index.ts
- [X] T005 [P] Create shared chart utility functions in src/paged/render/react/components/blocks/chartUtils.ts (colors, default props)
- [X] T006 [P] Verify existing ChartBar.tsx, ChartLine.tsx, ChartPie.tsx patterns for consistency

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Render Extended Chart Types (Priority: P1) 🎯 MVP

**Goal**: Enable rendering of all 8 chart types with soft, organic styling

**Independent Test**: Render each chart type with sample data and verify visual output matches acceptance scenarios

### Implementation for User Story 1

- [X] T007 [P] [US1] Create ChartArea component in src/paged/render/react/components/blocks/ChartArea.tsx
- [X] T008 [P] [US1] Create ChartBubble component in src/paged/render/react/components/blocks/ChartBubble.tsx
- [X] T009 [P] [US1] Create ChartRadar component in src/paged/render/react/components/blocks/ChartRadar.tsx
- [X] T010 [P] [US1] Create ChartPolar component in src/paged/render/react/components/blocks/ChartPolar.tsx
- [X] T011 [P] [US1] Create BarStats component in src/paged/render/react/components/blocks/BarStats.tsx
- [X] T012 [US1] Extend ChartBar with orientation prop in src/paged/render/react/components/blocks/ChartBar.tsx
- [X] T013 [US1] Update exports in src/paged/render/react/components/blocks/index.ts to include all new chart components
- [X] T014 [US1] Apply soft organic styling (gradient fills, rounded edges) to ChartArea in src/paged/render/react/components/blocks/ChartArea.tsx
- [X] T015 [US1] Apply translucent bubble styling to ChartBubble in src/paged/render/react/components/blocks/ChartBubble.tsx
- [X] T016 [US1] Apply soft fill opacity styling to ChartRadar in src/paged/render/react/components/blocks/ChartRadar.tsx
- [X] T017 [US1] Apply earthy color palette to ChartPolar in src/paged/render/react/components/blocks/ChartPolar.tsx
- [X] T018 [US1] Apply gentle emphasis styling to BarStats in src/paged/render/react/components/blocks/BarStats.tsx

**Checkpoint**: All 8 chart types render correctly with soft, organic styling. User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - LLM-Based Chart Type Selection (Priority: P1)

**Goal**: Automatically determine the best chart type for data patterns via LLM

**Independent Test**: Provide different data patterns (time-series, categorical, proportional, 3D) to chart selector and verify appropriate chart type selection

### Implementation for User Story 2

- [X] T019 [US2] Create chart_selector.py module in src/generation/content/chart_selector.py
- [X] T020 [US2] Implement ChartSelectionContext and ChartSelectionResult dataclasses in src/generation/content/chart_selector.py
- [X] T021 [US2] Implement select_chart_type() function with LLM prompt in src/generation/content/chart_selector.py
- [X] T022 [US2] Define chart selection prompt template with data pattern rules in src/generation/content/chart_selector.py
- [X] T023 [US2] Integrate chart selector into layout_generator.py when atom.visual="chart" in src/generation/content/layout_generator.py
- [X] T024 [US2] Implement fallback to bar chart when confidence < 0.5 in src/generation/content/chart_selector.py
- [X] T025 [US2] Honor explicit chart type (skip LLM selection) in src/generation/content/chart_selector.py
- [X] T026 [US2] Add logging for chart selection reasoning in src/generation/content/chart_selector.py

**Checkpoint**: LLM correctly selects chart types based on data patterns. User Story 2 is fully functional and testable independently.

---

## Phase 5: User Story 3 - Chart Type Documentation (Priority: P2)

**Goal**: Provide comprehensive chart type documentation for LLM consumption

**Independent Test**: Call get_layout_documentation() and verify all 8 chart types are documented with usage guidance

### Implementation for User Story 3

- [X] T027 [US3] Update get_layout_documentation() with all 8 chart types in src/paged/layout/react/layout_engine.py
- [X] T028 [US3] Add data format specification for each chart type in src/paged/layout/react/layout_engine.py
- [X] T029 [US3] Add best use case descriptions for each chart type in src/paged/layout/react/layout_engine.py
- [X] T030 [US3] Add example MDX syntax for each chart type in src/paged/layout/react/layout_engine.py
- [X] T031 [US3] Update prompts.py with chart selection guidance in src/generation/content/prompts.py
- [X] T032 [US3] Add chart type examples to MDX output format section in src/generation/content/prompts.py

**Checkpoint**: Layout documentation includes all 8 chart types with complete guidance. User Story 3 is fully functional and testable independently.

---

## Phase 6: User Story 4 - Consistent Visual Styling (Priority: P3)

**Goal**: Ensure all charts share consistent soft, organic visual styling

**Independent Test**: Render multiple chart types on same slide and verify consistent color palette, border radius, and styling

### Implementation for User Story 4

- [X] T033 [US4] Define earthy color palette CSS custom properties in src/paged/render/react/styles/chart-theme.css
- [X] T034 [US4] Apply soft border-radius to all chart containers in src/paged/render/react/styles/chart-theme.css
- [X] T035 [US4] Apply subtle shadows for depth in src/paged/render/react/styles/chart-theme.css
- [X] T036 [US4] Apply consistent typography for chart titles/labels in src/paged/render/react/styles/chart-theme.css
- [X] T037 [US4] Verify accessibility contrast ratios for earthy color palette in src/paged/render/react/styles/chart-theme.css
- [X] T038 [US4] Import chart-theme.css in all chart components that require styling (via globals.css import)

**Checkpoint**: All charts display consistent soft, organic styling. User Story 4 is fully functional and testable independently.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [X] T039 [P] Update quickstart.md with actual test commands in specs/003-extended-chart-types/quickstart.md
- [X] T040 [P] Add edge case handling for empty data in all chart components
- [X] T041 [P] Add edge case handling for insufficient radar data (< 3 points) with fallback
- [X] T042 [P] Add edge case handling for missing bubble size dimension
- [X] T043 Code cleanup and remove any console.log statements from chart components
- [X] T044 Run quickstart.md validation to verify all chart types render

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can proceed in priority order (P1 → P2 → P3)
  - US1 and US2 are both P1, can start in parallel
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Charts render even without LLM selection (manual type)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Documentation independent of implementation
- **User Story 4 (P3)**: Can start after US1 components exist - Applies styling to existing components

### Within Each User Story

- All component creation tasks [P] within US1 can run in parallel
- US2 tasks are sequential (depends on previous task's output)
- US3 tasks are sequential (building documentation incrementally)
- US4 styling tasks [P] can mostly run in parallel

### Parallel Opportunities

Within Phase 3 (User Story 1):
```
Parallel Group A: T007, T008, T009, T010, T011 (all new chart components)
Sequential: T012 (extend existing), T013 (exports depend on components)
Parallel Group B: T014, T015, T016, T017, T018 (styling for each component)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Render Charts)
4. **STOP and VALIDATE**: All 8 chart types render with sample data
5. Deploy/demo chart rendering capability

### Full Feature Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test chart rendering → **MVP ready**
3. Add User Story 2 → Test LLM selection → **Intelligent selection ready**
4. Add User Story 3 → Test documentation → **LLM guidance complete**
5. Add User Story 4 → Test visual consistency → **Feature complete**

### Suggested MVP Scope

**MVP = User Story 1 only**: This delivers all 8 chart types with manual type selection. LLM-based selection (US2), documentation (US3), and enhanced styling (US4) can follow incrementally.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US1 and US2 are both P1 priority - complete US1 first for MVP, then US2
