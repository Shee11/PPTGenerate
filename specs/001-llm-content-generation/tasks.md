# Tasks: LLM-Based Content Generation System

**Branch**: `001-llm-content-generation`  
**Input**: Design documents from `/specs/001-llm-content-generation/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Following TDD approach - tests written BEFORE implementation per plan.md

**Organization**: Tasks grouped by user story to enable independent implementation and testing

**Note**: This is a NEW system build - no backward compatibility requirements

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3, US4) - only for story-specific tasks
- File paths follow structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency management

- [X] T001 Add Azure OpenAI SDK dependency to pyproject.toml (openai>=1.0.0)
- [X] T002 Add python-dotenv dependency to pyproject.toml (python-dotenv>=1.0.0)
- [X] T003 [P] Create .env.example with Azure OpenAI configuration template
- [X] T004 [P] Add .cache/ and .env to .gitignore
- [X] T005 [P] Create directory structure: src/utils/, src/generation/atom/, src/generation/content/
- [X] T006 [P] Create cache directories: .cache/atoms/, .cache/layouts/

**Checkpoint**: Dependencies installed, directories created, configuration template ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### LLM Client Infrastructure

- [X] T007 Create test_llm_client.py - test singleton pattern, retry logic, connection pooling in tests/unit/test_llm_client.py
- [X] T008 Implement src/utils/llm_client.py with get_llm_client() singleton and call_llm() function
- [X] T009 Create test_generation_config.py - test GenerationConfig validation in tests/unit/test_generation_config.py
- [X] T010 [P] Implement src/utils/generation_config.py with GenerationConfig Pydantic model

### Caching Infrastructure

- [X] T011 Create test_cache.py - test hash computation, file operations, cache hits/misses in tests/unit/test_cache.py
- [X] T012 Implement src/utils/cache.py with GenerationCache class (hash_key, save, load methods)

### Source Model

- [X] T013 Create test_source.py - test Source and SourceReference validation in tests/unit/test_source.py
- [X] T014 Implement src/common/source.py with Source and SourceReference Pydantic models

**Checkpoint**: Foundation ready - LLM client works, caching works, Source model defined. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Extract Atoms from Source Content (Priority: P1) 🎯 MVP

**Goal**: Extract meaningful atoms (statements, processes, comparisons) from text/VTT files with preserved relationships and source links

**Independent Test**: Provide text file → verify atoms extracted with relationships and source references

### Atom Models & Collection (US1 Foundation)

- [X] T015 Create test_atom_models.py - test Atom base class, StatementAtom, ProcessAtom, ComparisonAtom validation in tests/unit/test_atom_models.py
- [X] T016 Implement src/generation/atom/models.py with Atom base class (extends PatchableContextBase), StatementAtom, ProcessAtom, ComparisonAtom subclasses
- [X] T017 Create test_atom_collection.py - test AtomCollection operations, patch application, filtering in tests/unit/test_atom_collection.py
- [X] T018 Implement src/generation/atom/collection.py with AtomCollection class (extends PatchableCollection)

### Atom Extraction Prompts

- [X] T019 Create test_atom_prompts.py - test prompt template rendering with source content in tests/unit/test_atom_prompts.py
- [X] T020 Implement src/generation/atom/prompts.py with system/user prompt templates for atom extraction

### Atom Extraction Integration

- [X] T021 Create test_atom_extractor.py - integration test for end-to-end extraction with mocked LLM in tests/integration/test_atom_extractor.py
- [X] T022 Implement src/generation/atom/extractor.py with extract_atoms(source, config, use_cache) function
- [X] T023 Add caching logic to extract_atoms() - check cache before LLM call, save results after

### Contract Validation for Atom Extraction

- [X] T024 Create test_llm_atom_schema.py - verify LLM atom extraction outputs match Pydantic schemas in tests/contract/test_llm_atom_schema.py
- [X] T025 Refine atom extraction prompts based on contract test failures (iterate until passing)

**Checkpoint**: At this point, User Story 1 is fully functional - atoms can be extracted from text files with relationships preserved

---

## Phase 3.5: Atom-to-Layout Integration Checkpoint

**Purpose**: Verify atoms can feed into layout generation before fine-tuning both flows

**Note**: This phase validates integration point between US1 and US2

### Integration Verification

- [X] T025a Create test_atom_to_layout_integration.py - verify atoms output format works as layout generation input in tests/integration/test_atom_to_layout_integration.py
- [X] T025b [P] Test AtomCollection serialization to JSON matches expected format for layout prompts
- [X] T025c [P] Test atom relationship data is preserved in serialized format
- [X] T025d Test mock layout generation can consume atom data without errors

**Checkpoint**: Integration point validated - atoms ready to feed layout generation

---

## Phase 4: User Story 3 - Apply Patches to Patchable Collections (Priority: P1)

**Goal**: Verify existing PatchableCollection infrastructure supports atom and slide patch operations

**Independent Test**: Create collection, apply patches, verify state maintained correctly

**Note**: PatchableContextBase and PatchableCollection already exist in src/common/patchable_context_pydantic.py

### Verification & Integration Tests

- [X] T026 Create test_patchable_integration.py - verify existing patch operations work with AtomCollection in tests/integration/test_patchable_integration.py
- [X] T027 [US3] Test AddOperation with atoms - verify atoms added correctly to AtomCollection
- [X] T028 [US3] Test RemoveOperation with atoms - verify atoms removed correctly from AtomCollection
- [X] T029 [US3] Test ReplaceOperation with atoms - verify atoms replaced correctly in AtomCollection
- [X] T030 [US3] Test sequential patch application - verify collection state evolves correctly
- [X] T031 [US3] Test patch validation - verify invalid patches rejected (non-existent IDs, orphan references)

**Checkpoint**: Patch operations verified working for AtomCollection. Ready for layout generation.

---

## Phase 5: User Story 2 - Generate Layout Content with State Management (Priority: P2)

**Goal**: Generate slide layouts from atoms with two-step state management (DRAFT → ACTIVE)

**Independent Test**: Provide atoms → verify slides progress through DRAFT state before finalizing to ACTIVE with schema-compliant content

**Note**: Slide and Slides classes already exist in src/common/slide.py and src/common/slides.py

### Layout Generation Prompts

- [X] T032 Create test_layout_prompts.py - test two-step prompt templates (state transition + content) in tests/unit/test_layout_prompts.py
- [X] T033 Implement src/generation/content/prompts.py with state transition prompt and content generation prompt templates

### Layout Generation Integration

- [X] T034 Create test_layout_generator.py - integration test for two-step generation with mocked LLM in tests/integration/test_layout_generator.py
- [X] T035 [US2] Implement src/generation/content/generator.py with generate_layout(atoms, config, use_cache) function
- [X] T036 [US2] Implement step 1: Generate state transition patch (set slides to DRAFT state)
- [X] T037 [US2] Implement step 2: Generate content patch (populate slide widgets, update to ACTIVE state)
- [X] T038 [US2] Add caching logic to generate_layout() - check cache before LLM calls, save results after

### State Transition Verification

- [X] T039 Create test_slides_state_transitions.py - verify DRAFT→ACTIVE transitions work correctly with existing Slides in tests/integration/test_slides_state_transitions.py
- [X] T040 [US2] Test state transition patch application - verify slides move to DRAFT
- [X] T041 [US2] Test content generation patch application - verify slides populate and move to ACTIVE
- [X] T042 [US2] Test state transition validation - verify out-of-sequence transitions rejected

### Contract Validation for Layout Generation

- [X] T043 Create test_llm_layout_schema.py - verify LLM layout generation outputs match existing layout schema in tests/contract/test_llm_layout_schema.py
- [X] T044 [US2] Verify LLM outputs only use supported widget types and attributes
- [X] T045 [US2] Refine prompts based on validation test failures to ensure schema compliance

**Checkpoint**: At this point, User Stories 1, 2, and 3 are all functional - full pipeline from source → atoms → layouts works

---

## Phase 5.5: Layout-to-Render Integration Checkpoint

**Purpose**: Verify generated layout configs can be rendered as HTML using existing rendering pipeline

**Note**: This validates that LLM-generated layout configs work with LayoutEngine and HTMLRenderer

### E2E Rendering Verification

- [X] T045a Create test_layout_to_render_integration.py - verify generated Slides can be rendered to HTML in tests/integration/test_layout_to_render_integration.py
- [X] T045b [US2] Test generated Slides collection passes through LayoutEngine.calculate_slides() without errors
- [X] T045c [US2] Test LayoutEngine output (renderables) can be rendered by HTMLRenderer.render()
- [X] T045d [US2] Test generated HTML output is valid (contains expected structure, no broken widgets)
- [X] T045e [US2] Verify generated slides with state=ACTIVE render correctly (DRAFT slides should be filtered or handled)

**Checkpoint**: Generated layouts confirmed working with existing rendering pipeline - ready for E2E CLI integration

---

## Phase 6: User Story 4 - Two-Flow Separation: Atoms vs Layouts (Priority: P3)

**Goal**: Ensure atom extraction and layout generation are independent flows with clear separation

**Independent Test**: Verify atom extraction completes independently, layout generation uses atom output without coupling

### Flow Separation Verification

- [ ] T046 Create test_flow_separation.py - test that flows are decoupled in tests/integration/test_flow_separation.py
- [ ] T047 [US4] Test atom extraction completes without layout generation dependency
- [ ] T048 [US4] Test layout generation receives full atom context as input
- [ ] T049 [US4] Test atom extraction failure prevents layout generation (validation)
- [ ] T050 [US4] Test modifying atom extraction logic doesn't affect layout generation logic

**Checkpoint**: All user stories independently functional with clean separation of concerns

---

## Phase 7: CLI Integration

**Purpose**: Add LLM-based content generation capabilities to CLI

**Note**: Adding new functionality to cli/uce_render.py

### CLI Implementation

- [X] T051 Create test_cli_generate.py - test new CLI flags and generation workflow in tests/integration/test_cli_generate.py
- [X] T052 Add --source flag to cli/uce_render.py to accept source content file path (.txt or .vtt)
- [X] T053 Add --user-instruction flag to cli/uce_render.py for user guidance text
- [X] T054 Add --use-cache flag to cli/uce_render.py (default: true) for cache control
- [X] T055 Implement CLI workflow: when --source flag provided, call extract_atoms() for atom extraction
- [X] T056 Implement CLI workflow: when atoms extracted, call generate_layout() to create Slides collection
- [X] T057 Implement CLI workflow: generated Slides feed into LayoutEngine.calculate_slides() pipeline
- [X] T058 Implement CLI workflow: HTMLRenderer.render() outputs final HTML from LLM-generated slides

### End-to-End Testing

- [ ] T059 Create test_cli_e2e.py - test CLI workflow from source files to generated layouts in tests/e2e/test_cli_e2e.py
- [ ] T060 [P] Test CLI with --source flag and plain text file (.txt)
- [ ] T061 [P] Test CLI with --source flag and VTT subtitle file (.vtt)
- [ ] T062 [P] Test CLI with --use-cache=true vs --use-cache=false
- [ ] T063 Test CLI error handling (empty source, invalid file path, LLM failure)

**Checkpoint**: CLI fully functional - source files to generated layout configs

---

## Phase 7.5: E2E HTML Rendering from Source

**Purpose**: Verify complete pipeline from source content → atoms → layout config → rendered HTML through CLI

**Note**: This validates the full integration - source files in, HTML slides out via CLI

### Complete Pipeline E2E Tests

- [ ] T064 Create test_cli_e2e_render.py - complete pipeline including HTML rendering via CLI in tests/e2e/test_cli_e2e_render.py
- [ ] T065 Test: uce-render --source source.txt --output result.html produces valid HTML
- [ ] T066 Verify generated HTML contains expected number of slides from source content
- [ ] T067 Verify generated HTML slides contain widget content extracted from source atoms
- [ ] T068 Test CLI flags work together: --source with --width, --height, --format
- [ ] T069 Test rendered HTML file can be opened in browser (file validation)
- [ ] T070 [P] Test E2E with different source types: --source text.txt vs --source subtitles.vtt
- [ ] T071 [P] Test E2E with cache: verify second run with same source is faster (cache hit)
- [ ] T072 Test E2E with theme/style flags (ensure compatibility with LLM-generated content)

**Checkpoint**: Complete pipeline validated - CLI produces HTML presentations from source content

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Documentation & Validation

- [ ] T073 [P] Update quickstart.md with LLM-based content generation usage examples
- [ ] T074 [P] Add docstrings to all public functions following plan.md contracts
- [ ] T075 [P] Run quickstart.md validation - verify all examples work
- [ ] T076 [P] Update README with new CLI flags documentation (--source, --user-instruction, --use-cache)
- [ ] T077 [P] Add examples to CLI help text showing LLM-based usage

### Error Handling & Robustness

- [ ] T078 Add comprehensive error handling to extract_atoms() (empty content, LLM failures, validation errors)
- [ ] T079 Add comprehensive error handling to generate_layout() (missing atoms, schema violations)
- [ ] T080 [P] Add retry logic with exponential backoff to LLM client (per plan.md)
- [ ] T081 [P] Add logging throughout atom extraction and layout generation flows
- [ ] T082 Ensure CLI provides helpful error messages when --source flag fails (file not found, unsupported format, etc.)

### Performance & Optimization

- [ ] T083 [P] Verify cache performance meets SC-008 (>80% hit rate during iteration)
- [ ] T084 [P] Verify atom extraction meets SC-001 (<10s for 1000-word documents)
- [ ] T085 [P] Verify layout generation meets SC-006 (<30s for 10-slide presentations)

### Code Quality

- [ ] T086 [P] Run linting and fix any issues
- [ ] T087 [P] Run type checking (mypy) and fix type issues
- [ ] T088 [P] Code cleanup and refactoring for clarity

**Checkpoint**: Feature complete, tested, documented, and optimized

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ⚠️ BLOCKS all user stories
    ↓
    ├─→ Phase 3 (US1 - Atom Extraction) [P1] 🎯
    │       ↓
    │   Phase 3.5 (Atom-to-Layout Integration Checkpoint)
    │       ↓
    ├─→ Phase 4 (US3 - Patch Operations) [P1]
    └─→ Phase 5 (US2 - Layout Generation) [P2] (needs Phase 3 atoms)
            ↓
        Phase 5.5 (Layout-to-Render Integration Checkpoint)
            ↓
        Phase 6 (US4 - Flow Separation) [P3]
            ↓
        Phase 7 (CLI Integration with Rendering)
            ↓
        Phase 7.5 (E2E HTML Rendering from Source)
            ↓
        Phase 8 (Polish)
```

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 - No dependencies on other stories ✅
- **US3 (P1)**: Can start after Phase 2 - Parallel with US1 ✅
- **US2 (P2)**: Can start after Phase 2, but needs atoms from US1 for integration testing
- **US4 (P3)**: Can start after US1 and US2 complete - Validates separation

### Critical Path

1. **Setup** (T001-T006) → 2. **Foundational** (T007-T014) → 3. **US1 Atom Extraction** (T015-T025) → 3.5. **Atom-to-Layout Integration** (T025a-T025d) → 4. **US2 Layout Generation** (T032-T045) → 5.5. **Layout-to-Render Integration** (T045a-T045e) → 6. **CLI Extension** (T051-T058) → 7. **CLI E2E Testing** (T059-T063) → 8. **E2E HTML Rendering** (T064-T072)

### Within Each User Story

**US1 (Atom Extraction)**:
- Models (T015-T018) → Prompts (T019-T020) → Extractor (T021-T023) → Contract Validation (T024-T025) → Integration Checkpoint (T025a-T025d)

**US3 (Patch Operations)**:
- All tests can run in parallel once AtomCollection exists (T026-T031 after T018)

**US2 (Layout Generation)**:
- Prompts (T032-T033) → Generator (T034-T038) → State Verification (T039-T042) → Contract Validation (T043-T045) → Render Integration Checkpoint (T045a-T045e)

**US4 (Flow Separation)**:
- All tests can run in parallel (T046-T050)

**CLI Integration**:
- CLI Extension (T051-T058) → E2E Tests (T059-T063) → E2E HTML Rendering (T064-T072)

### Parallel Opportunities

**Within Setup (Phase 1)**:
- T003, T004, T005, T006 can all run in parallel

**Within Foundational (Phase 2)**:
- T010 parallel with T007-T008 (different files)
- T013-T014 parallel with T007-T012 (different files)

**Within US1**:
- T015-T016 can run in parallel with T019-T020 (models vs prompts)
- Once both complete, T017-T018 and T021-T023 can proceed

**Within US3**:
- T027, T028, T029 can run in parallel (different test scenarios)

**Within US2**:
- T039-T042 can run in parallel (different state transition tests)
- T043, T044, T045 can run in parallel (different schema validations)

**Within Phase 8 (Polish)**:
- T073, T074, T075, T076, T077 can run in parallel (documentation)
- T080, T081 can run in parallel (error handling, logging)
- T083, T084, T085 can run in parallel (performance validation)
- T086, T087, T088 can run in parallel (code quality)

---

## Parallel Execution Example: User Story 1

```bash
# After Phase 2 completes, start US1 with parallel tasks:

# Terminal 1: Atom models
pytest tests/unit/test_atom_models.py  # Should FAIL
# Implement src/generation/atom/models.py
pytest tests/unit/test_atom_models.py  # Should PASS

# Terminal 2: Atom prompts (parallel with Terminal 1)
pytest tests/unit/test_atom_prompts.py  # Should FAIL
# Implement src/generation/atom/prompts.py
pytest tests/unit/test_atom_prompts.py  # Should PASS

# Terminal 3: Atom collection (after models complete)
pytest tests/unit/test_atom_collection.py  # Should FAIL
# Implement src/generation/atom/collection.py
pytest tests/unit/test_atom_collection.py  # Should PASS

# Then integrate:
pytest tests/integration/test_atom_extractor.py  # Should FAIL
# Implement src/generation/atom/extractor.py
pytest tests/integration/test_atom_extractor.py  # Should PASS
```

---

## Implementation Strategy

### MVP Scope (Recommended First Delivery)

**Target**: User Story 1 (P1) only - Atom extraction working end-to-end with integration checkpoint

- Complete Phase 1 (Setup)
- Complete Phase 2 (Foundational)
- Complete Phase 3 (US1 - Atom Extraction)
- Complete Phase 3.5 (Atom-to-Layout Integration Checkpoint)
- Skip Phase 4-8 for MVP

**MVP Deliverable**: CLI command that extracts atoms from text files with caching, validated integration format

**Estimated Timeline**: 2-3 days

### Full P1+P2 Scope (Complete Core Feature with Rendering)

**Target**: User Stories 1, 2, 3 (all P1+P2) - Full pipeline working with HTML output

- Complete Phase 1-5 (including both integration checkpoints: 3.5 and 5.5)
- Complete Phase 7 (CLI Integration)
- Complete Phase 7.5 (E2E HTML Rendering)
- Skip Phase 6 (US4 - P3), Phase 8 (Polish) for initial delivery

**Deliverable**: Complete pipeline - source text files → atoms → layout configs → rendered HTML slides

**Estimated Timeline**: 5-7 days

### Full Feature Scope (All User Stories)

**Target**: All user stories including P3 enhancements and polish

- Complete all phases 1-8 (including all integration checkpoints)

**Deliverable**: Production-ready feature with all user stories, tests, documentation, E2E rendering validated

**Estimated Timeline**: 6-8 days

---

## Task Validation

**Format Check**: ✅ All tasks follow `- [ ] [ID] [P?] [Story?] Description with file path` format

**Coverage Check**:
- ✅ User Story 1 (P1): 11 tasks (T015-T025)
- ✅ Atom-to-Layout Integration: 4 tasks (T025a-T025d)
- ✅ User Story 2 (P2): 14 tasks (T032-T045)
- ✅ Layout-to-Render Integration: 5 tasks (T045a-T045e)
- ✅ User Story 3 (P1): 6 tasks (T026-T031)
- ✅ User Story 4 (P3): 5 tasks (T046-T050)
- ✅ Setup: 6 tasks (T001-T006)
- ✅ Foundational: 8 tasks (T007-T014)
- ✅ CLI Extension: 8 tasks (T051-T058)
- ✅ CLI E2E Testing: 5 tasks (T059-T063)
- ✅ E2E HTML Rendering: 9 tasks (T064-T072)
- ✅ Polish: 16 tasks (T073-T088)

**Total**: 88 tasks

**Independence Check**:
- ✅ Each user story has clear goal and independent test criteria
- ✅ Each user story can be tested without others (US1 outputs atoms, US2 uses atoms but can use mock data)
- ✅ Parallel opportunities clearly marked with [P]
- ✅ Story labels consistently applied ([US1], [US2], [US3], [US4])

**File Path Check**:
- ✅ All implementation tasks include exact file paths
- ✅ Paths follow structure from plan.md
- ✅ Test paths follow convention: tests/{unit,integration,contract,e2e}/test_*.py

**Alignment with Plan**:
- ✅ Uses existing PatchableContextBase and PatchableCollection (no new base classes)
- ✅ Atom models follow Slide pattern (extend PatchableContextBase)
- ✅ AtomCollection follows Slides pattern (extends PatchableCollection)
- ✅ LLM outputs existing custom patch format (Add/Remove/Replace)
- ✅ Caching infrastructure included (FR-030-034)
- ✅ Separate atom subclasses (StatementAtom, ProcessAtom, ComparisonAtom)

**Success Criteria Mapping**:
- SC-001 (extraction <10s): T084
- SC-002 (schema compliance): T043-T045
- SC-003 (state transitions): T039-T042
- SC-004 (patch consistency): T026-T031
- SC-005 (relationships 90%+): T024-T025
- SC-006 (generation <30s): T085
- SC-007 (independent flows): T046-T050
- SC-008 (cache 80%+): T083

**New System Build**:
- ✅ No backward compatibility requirements - building fresh LLM-based content generation system
- ✅ New CLI flags: --source, --user-instruction, --use-cache
- ✅ Pipeline: source files → atoms → layout configs → HTML rendering
- ✅ All components designed for LLM-based generation from scratch
