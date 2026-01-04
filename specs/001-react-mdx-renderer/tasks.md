# Tasks: React MDX Presentation Renderer

**Input**: Design documents from `/specs/001-react-mdx-renderer/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Included per TDD requirement in constitution.md

**Organization**: Tasks grouped by user story (US1-US5) to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1, US2, US3, US4, US5)
- Setup/Foundational phases have NO story label
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Next.js project and basic configuration

- [X] T001 Create Next.js project structure at src/paged/render/react/
- [X] T002 Initialize package.json with React 18, Next.js 14, MDX 3.x dependencies
- [X] T003 [P] Configure TypeScript with tsconfig.json for strict mode
- [X] T004 [P] Configure Tailwind CSS with tailwind.config.js
- [X] T005 [P] Configure Vitest for React testing in vitest.config.ts
- [X] T006 Configure next.config.mjs for MDX and static export
- [X] T007 [P] Create shared types in src/paged/render/react/utils/types.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 Create ThemeContext provider in src/paged/render/react/components/core/ThemeContext.tsx
- [X] T009 Create SlideWrapper component in src/paged/render/react/components/core/SlideWrapper.tsx
- [X] T010 [P] Create business theme definition in src/paged/render/react/themes/business.ts
- [X] T011 [P] Create theme registry and CSS variable injection in src/paged/render/react/themes/index.ts
- [X] T012 Create MDXProvider with component mapping in src/paged/render/react/components/core/MDXProvider.tsx
- [X] T013 Create base slide page template in src/paged/render/react/pages/[...slide].tsx
- [X] T014 [P] Create global styles with CSS variables in src/paged/render/react/styles/globals.css

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Generate Semantic MDX Slides (Priority: P1) 🎯 MVP

**Goal**: AI Agent can generate valid MDX using only semantic components (no HTML/CSS)

**Independent Test**: Generate 5 slide types (cover, split, grid, chart, quote) and verify no L0 violations

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T015 [P] [US1] Create MDX generator unit tests in tests/test_mdx_renderer.py
- [X] T016 [P] [US1] Create L0 validator tests in src/paged/render/react/__tests__/validator.test.ts

### Implementation for User Story 1

#### L3 Atoms (Typography)

- [X] T017 [P] [US1] Create Heading component in src/paged/render/react/components/atoms/Heading.tsx
- [X] T018 [P] [US1] Create Text component in src/paged/render/react/components/atoms/Text.tsx
- [X] T019 [P] [US1] Create Callout component in src/paged/render/react/components/atoms/Callout.tsx

#### L2 Blocks (Content - MVP subset)

- [X] T020 [P] [US1] Create SmartList component in src/paged/render/react/components/blocks/SmartList.tsx
- [X] T021 [P] [US1] Create ChartBar component in src/paged/render/react/components/blocks/ChartBar.tsx
- [X] T022 [P] [US1] Create MetricGroup component in src/paged/render/react/components/blocks/MetricGroup.tsx

#### L1 Layouts (MVP subset)

- [X] T023 [P] [US1] Create LayoutCover component in src/paged/render/react/components/layouts/LayoutCover.tsx
- [X] T024 [P] [US1] Create LayoutSplit component with .Left/.Right slots in src/paged/render/react/components/layouts/LayoutSplit.tsx
- [X] T025 [P] [US1] Create LayoutGrid component with .Col slots in src/paged/render/react/components/layouts/LayoutGrid.tsx

#### Python MDX Generator

- [X] T026 [US1] Create ReactMDXRenderer class in src/paged/render/react/mdx_renderer.py
- [X] T027 [US1] Implement widget type to component mapping in mdx_renderer.py
- [X] T028 [US1] Implement layout type to component mapping in mdx_renderer.py
- [X] T029 [US1] Implement render_slide() method in mdx_renderer.py
- [X] T030 [US1] Implement render_state() to generate MDX files from state.json

#### L0 Validator

- [X] T031 [US1] Create MDX validator in src/paged/render/react/utils/validator.ts
- [X] T032 [US1] Implement forbidden element detection (div, span, section)
- [X] T033 [US1] Implement forbidden attribute detection (className, style)
- [X] T034 [US1] Add line number and suggestion to validation errors

**Checkpoint**: US1 complete - Agent can generate valid MDX, validator catches L0 violations ✅

---

## Phase 4: User Story 2 - Render MDX to Interactive Presentation (Priority: P1) 🎯 MVP

**Goal**: User can view MDX as professional presentation in browser with navigation

**Independent Test**: Load .mdx file and verify slide deck renders with keyboard navigation

### Tests for User Story 2

- [X] T035 [P] [US2] Create layout render tests in src/paged/render/react/__tests__/layouts.test.tsx
- [X] T036 [P] [US2] Create block render tests in src/paged/render/react/__tests__/blocks.test.tsx
- [X] T037 [P] [US2] Create atom render tests in src/paged/render/react/__tests__/atoms.test.tsx

### Implementation for User Story 2

- [X] T038 [US2] Create SlideNavigation component in src/paged/render/react/components/core/SlideNavigation.tsx
- [X] T039 [US2] Implement keyboard navigation (arrow keys, space, escape)
- [X] T040 [US2] Add slide counter and progress indicator
- [X] T041 [US2] Create slide index page in src/paged/render/react/pages/index.tsx
- [X] T042 [US2] Register all components in MDXProvider mapping
- [X] T043 [US2] Test full render pipeline with sample MDX content

**Checkpoint**: US2 complete - MDX renders as interactive presentation with navigation ✅

---

## Phase 5: User Story 3 - Apply Themes to Presentations (Priority: P2)

**Goal**: User can switch between 7 predefined themes without modifying MDX

**Independent Test**: Render same MDX with 3 different themes, verify visual differences

### Tests for User Story 3

- [X] T044 [P] [US3] Create theme switching tests in src/paged/render/react/__tests__/themes.test.tsx
- [X] T045 [P] [US3] Create CSS variable injection tests

### Implementation for User Story 3

- [X] T046 [P] [US3] Create cyber theme in src/paged/render/react/themes/cyber.ts
- [X] T047 [P] [US3] Create minimal theme in src/paged/render/react/themes/minimal.ts
- [X] T048 [P] [US3] Create academic theme in src/paged/render/react/themes/academic.ts
- [X] T049 [P] [US3] Create creative theme in src/paged/render/react/themes/creative.ts
- [X] T050 [P] [US3] Create duolingo theme in src/paged/render/react/themes/duolingo.ts
- [X] T051 [P] [US3] Create dark theme in src/paged/render/react/themes/dark.ts
- [X] T052 [US3] Implement runtime theme switching in ThemeContext
- [X] T053 [US3] Add theme selector UI (optional, for dev mode)
- [X] T054 [P] [US3] Create vibe configurations (minimal, clean, balanced, decorative, expressive)
- [X] T055 [US3] Apply vibe modifiers to all components

**Checkpoint**: US3 complete - All 7 themes work, switching is instant ✅

---

## Phase 6: User Story 4 - Export to Static HTML (Priority: P2)

**Goal**: User can export presentation to standalone HTML file/folder

**Independent Test**: Export presentation, open HTML in browser without server

### Tests for User Story 4

- [X] T056 [P] [US4] Create export integration tests in tests/test_react_export.py
- [X] T057 [P] [US4] Create bundle size validation tests

### Implementation for User Story 4

- [X] T058 [US4] Configure Next.js static export in next.config.mjs
- [X] T059 [US4] Create export script in src/paged/render/react/scripts/export.ts
- [X] T060 [US4] Implement single HTML file bundling (inline CSS/JS)
- [X] T061 [US4] Handle image assets (inline base64 or copy to assets/)
- [X] T062 [US4] Add export progress reporting
- [X] T063 [US4] Validate exported HTML size <500KB (excl. images)

**Checkpoint**: US4 partial - Export script created, tests passing ✅

---

## Phase 7: User Story 5 - CLI Integration (Priority: P3)

**Goal**: Developer can render MDX via CLI for CI/CD pipelines

**Independent Test**: Run `uce-render --render state.json --project react-mdx -o output.html`

### Tests for User Story 5

- [X] T064 [P] [US5] Create CLI integration tests in tests/test_cli_react_mdx.py
- [X] T065 [P] [US5] Create error handling tests for invalid input

### Implementation for User Story 5

- [X] T066 [US5] Add 'react-mdx' to PROJECTS mapping in cli/uce_render.py
- [X] T067 [US5] Implement ReactMDXRenderer integration in CLI
- [X] T068 [US5] Add --validate-only flag for MDX validation without build
- [X] T069 [US5] Add --verbose flag for detailed progress output
- [X] T070 [US5] Implement error messages with line numbers for invalid MDX
- [X] T071 [US5] Add --theme flag to override theme from CLI

**Checkpoint**: US5 complete - Full CLI integration works

---

## Phase 8: Full Component Set (Extends US1/US2)

**Purpose**: Complete remaining layouts and blocks for feature parity

### Additional L1 Layouts

- [X] T072 [P] Create LayoutFullBleed component in src/paged/render/react/components/layouts/LayoutFullBleed.tsx
- [X] T073 [P] Create LayoutTimeline component in src/paged/render/react/components/layouts/LayoutTimeline.tsx
- [X] T074 [P] Create LayoutDashboard component in src/paged/render/react/components/layouts/LayoutDashboard.tsx

### Additional L2 Blocks

- [X] T075 [P] Create ChartLine component in src/paged/render/react/components/blocks/ChartLine.tsx
- [X] T076 [P] Create ChartPie component in src/paged/render/react/components/blocks/ChartPie.tsx
- [X] T077 [P] Create TableData component in src/paged/render/react/components/blocks/TableData.tsx
- [X] T078 [P] Create QuoteBlock component in src/paged/render/react/components/blocks/QuoteBlock.tsx
- [X] T079 [P] Create ImageBlock component in src/paged/render/react/components/blocks/ImageBlock.tsx
- [X] T080 [P] Create CardGroup component in src/paged/render/react/components/blocks/CardGroup.tsx

- [X] T081 Update MDXProvider to register all new components
- [X] T082 Update Python mdx_renderer.py to support all new components

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Quality improvements across all user stories

- [X] T083 [P] Add JSDoc documentation to all components
- [X] T084 [P] Create component index exports in src/paged/render/react/components/index.ts
- [X] T085 Performance optimization: lazy load Recharts components
- [X] T086 Cross-browser testing (Chrome, Firefox, Safari)
- [X] T087 [P] Update README.md in src/paged/render/react/
- [X] T088 Validate quickstart.md instructions work end-to-end
- [X] T089 Run full test suite and fix any failures
- [X] T090 Verify all success criteria from spec.md

**Checkpoint**: Feature complete - All tests passing, all criteria verified ✅

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ──────── BLOCKS ALL USER STORIES
    │
    ├──────────────────────────────────────────────────┐
    │                                                  │
    ▼                                                  ▼
Phase 3 (US1: MDX Gen) ◄────────────────────► Phase 4 (US2: Render)
    │                                                  │
    │  (can parallel if                               │
    │   different devs)                               │
    │                                                  │
    ▼                                                  ▼
Phase 5 (US3: Themes) ◄────────────────────► Phase 6 (US4: Export)
    │                                                  │
    └──────────────────────┬───────────────────────────┘
                           │
                           ▼
                    Phase 7 (US5: CLI)
                           │
                           ▼
                    Phase 8 (Full Components)
                           │
                           ▼
                    Phase 9 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|-----------|-------------------|
| US1 (MDX Gen) | Phase 2 | US2 (different files) |
| US2 (Render) | Phase 2, US1 components | US1 (MDX generator) |
| US3 (Themes) | Phase 2 | US4 |
| US4 (Export) | US2 | US3 |
| US5 (CLI) | US1, US4 | None (final integration) |

### Within Each User Story

1. Tests MUST be written and FAIL before implementation
2. Atoms → Blocks → Layouts (dependency order)
3. Components before integration
4. Story complete before moving to next priority

### Parallel Opportunities per Phase

**Phase 1 (Setup)**: T003, T004, T005, T007 can run in parallel  
**Phase 2 (Foundational)**: T010, T011, T014 can run in parallel  
**Phase 3 (US1)**: T015-T016, T017-T019, T020-T022, T023-T025 can all run in parallel  
**Phase 4 (US2)**: T035, T036, T037 can run in parallel  
**Phase 5 (US3)**: T044-T045, T046-T051, T054 can run in parallel  
**Phase 6 (US4)**: T056, T057 can run in parallel  
**Phase 7 (US5)**: T064, T065 can run in parallel  
**Phase 8 (Components)**: T072-T080 can ALL run in parallel  
**Phase 9 (Polish)**: T083, T084, T087 can run in parallel

---

## MVP Definition

**MVP = Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2)**

MVP delivers:
- ✅ state.json → MDX generation (Python)
- ✅ MDX → Browser rendering (React/Next.js)
- ✅ 3 layouts: Cover, Split, Grid
- ✅ 3 blocks: SmartList, ChartBar, MetricGroup  
- ✅ 3 atoms: Heading, Text, Callout
- ✅ 1 theme: Business
- ✅ L0 validation
- ✅ Keyboard navigation

**Post-MVP = Phase 5-9** (Themes, Export, CLI, Full Components, Polish)

---

## Task Count Summary

| Phase | Tasks | Parallel Tasks |
|-------|-------|----------------|
| Phase 1: Setup | 7 | 4 |
| Phase 2: Foundational | 7 | 3 |
| Phase 3: US1 | 20 | 14 |
| Phase 4: US2 | 9 | 3 |
| Phase 5: US3 | 12 | 9 |
| Phase 6: US4 | 8 | 2 |
| Phase 7: US5 | 8 | 2 |
| Phase 8: Components | 11 | 9 |
| Phase 9: Polish | 8 | 3 |
| **Total** | **90** | **49** |

Independent test criteria for each story ensures incremental delivery.
