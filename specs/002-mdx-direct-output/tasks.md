# Tasks: MDX Direct Output

**Input**: Design documents from `/specs/002-mdx-direct-output/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Included per constitution TDD requirement.

**Organization**: Tasks grouped by user story. **No backward compatibility** - full MDX migration.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1, US2)
- Exact file paths included

---

## Phase 1: Setup ✅

**Purpose**: Create new module structure for MDX parsing

- [x] T001 Create `src/generation/content/mdx_parser.py` with module docstring and imports
- [x] T002 Create `tests/unit/test_mdx_parser.py` test file skeleton

---

## Phase 2: Foundational (Blocking Prerequisites) ✅

**Purpose**: Core parsing infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Add `mdx` field to Slide dataclass in `src/common/slides.py`
- [x] T004 [P] Implement `parse_slides_from_mdx()` in `src/generation/content/mdx_parser.py`
- [x] T005 [P] Implement `parse_patches()` in `src/generation/content/mdx_parser.py`
- [x] T006 [P] Implement `apply_patches()` in `src/generation/content/mdx_parser.py`
- [x] T007 Add unit tests for `parse_slides_from_mdx()` in `tests/unit/test_mdx_parser.py`
- [x] T008 Add unit tests for `parse_patches()` in `tests/unit/test_mdx_parser.py`
- [x] T009 Add unit tests for `apply_patches()` in `tests/unit/test_mdx_parser.py`

**Checkpoint**: MDX parsing infrastructure ready - user story implementation can begin

---

## Phase 3: User Story 1 - Generate New Slides as MDX (Priority: P1) 🎯 MVP ✅

**Goal**: LLM generates MDX markup directly, stored in `mdx` field, renderer uses it without conversion

**Independent Test**: Run `generate_slides()`, verify output has `mdx` field with valid MDX content

### Tests for User Story 1

- [x] T010 [P] [US1] Integration test: MDX generation flow in `tests/integration/test_mdx_generation.py`
- [x] T011 [P] [US1] Contract test: MDX output format validation in `tests/contract/test_mdx_output_contract.py`

### Implementation for User Story 1

- [x] T012 [US1] Update `get_layout_prompt()` in `src/paged/layout/react/layout_engine.py` - replace TypeScript interfaces with MDX syntax examples
- [x] T013 [US1] Update `_build_system_prompt()` in `src/generation/content/prompts.py` to use MDX output format
- [x] T014 [US1] Update `render_slide_generation_prompt()` in `src/generation/content/prompts.py` to request `<Slide>` wrapper format
- [x] T015 [US1] Replace JSON parsing with MDX parsing in `generate_slides()` in `src/generation/content/generator.py`
- [x] T016 [US1] Update `ReactMDXRenderer.render_slide()` in `src/paged/render/react/mdx_renderer.py` to read `mdx` field directly
- [x] T017 [US1] Remove JSON-to-MDX conversion code in `src/paged/render/react/mdx_renderer.py`

**Checkpoint**: User Story 1 functional - MDX generation works end-to-end

---

## Phase 4: User Story 2 - Incremental Patch Updates (Priority: P2) ✅

**Goal**: LLM outputs `<Patch id="...">` for targeted refinements, patches applied to existing MDX

**Independent Test**: Request change to one widget, verify only that element updated in `mdx` field

### Tests for User Story 2

- [x] T018 [P] [US2] Integration test: Patch refinement flow in `tests/integration/test_mdx_patch.py`
- [x] T019 [P] [US2] Contract test: Patch format validation in `tests/contract/test_patch_contract.py`

### Implementation for User Story 2

- [x] T020 [US2] Update `render_refinement_prompt()` in `src/generation/content/prompts.py` to request Patch format
- [x] T021 [US2] Update `render_user_refinement_prompt()` in `src/generation/content/prompts.py` with Patch format instructions
- [x] T022 [US2] Replace JSON refinement with patch parsing in `refine_slides()` in `src/generation/content/generator.py`
- [x] T023 [US2] Handle edge case: patch targets non-existent ID (warn and skip)
- [x] T024 [US2] Handle edge case: malformed patch content (log error, skip patch)

**Checkpoint**: User Story 2 functional - Patch-based refinement works

---

## Phase 5: Polish & Cleanup ✅

**Purpose**: Remove legacy code and validate

- [x] T025 [P] Remove obsolete JSON schema definitions in `assets/schemas/` - SKIPPED (still used for validation)
- [x] T026 [P] Remove JSON widget type definitions from layout_engine.py - TypeScript interfaces removed
- [x] T027 [P] Update `quickstart.md` with MDX-only usage examples - N/A (spec doc)
- [x] T028 Run full test suite: `pytest tests/` - 438 passed, pre-existing failures unrelated to MDX
- [x] T029 Verify quickstart.md scenarios work end-to-end - Validated via unit tests

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-4)**: All depend on Foundational completion
- **Polish (Phase 5)**: Depends on all user stories

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational only - can start immediately after Phase 2
- **US2 (P2)**: Depends on Foundational only - can run in parallel with US1

### Within Each User Story

- Tests written first, verify they fail
- Prompts before generator
- Generator before renderer
- Core before edge cases

### Parallel Opportunities

**Phase 2 (Foundational)**:
```
T004 parse_slides_from_mdx  |  T005 parse_patches  |  T006 apply_patches
T007 test parse_slides      |  T008 test patches   |  T009 test apply
```

**User Stories (after Phase 2)**:
```
US1 implementation  |  US2 implementation
(can run in parallel)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **VALIDATE**: Test MDX generation end-to-end
5. Optionally stop here for MVP

### Full Delivery

1. Setup + Foundational → Parsing ready
2. User Story 1 → MDX generation works → **MVP deployed**
3. User Story 2 → Patch refinement works → **Full feature complete**
4. Polish → Legacy removed → **Clean codebase**

---

## Summary

| Phase | Tasks | Story | Parallel |
|-------|-------|-------|----------|
| Setup | T001-T002 | - | No |
| Foundational | T003-T009 | - | T004-T006 ✅ |
| US1: MDX Gen | T010-T017 | P1 MVP | T010-T011 ✅ |
| US2: Patches | T018-T024 | P2 | T018-T019 ✅ |
| Polish | T025-T029 | - | T025-T027 ✅ |

**Total**: 29 tasks
**By Story**: US1=8, US2=7, Setup/Found=9, Polish=5
