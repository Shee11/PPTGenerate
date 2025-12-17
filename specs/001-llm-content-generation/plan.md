# Implementation Plan: LLM-Based Content Generation System

**Branch**: `001-llm-content-generation` | **Date**: December 15, 2025 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-llm-content-generation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Clarifications Summary

**Session Date**: December 15, 2025  
**Questions Resolved**: 5 of 5 (clarification complete)

| # | Question | Answer | Impact |
|---|----------|--------|--------|
| 1 | Should Atom inherit from PatchableContextBase (like Slide) with AtomCollection inheriting from PatchableCollection (like Slides)? | **Option A**: Yes - maintains consistency with existing codebase pattern | Updated data model, implementation order |
| 2 | Should atoms use existing PatchableContextState (DRAFT/ACTIVE/ARCHIVED/DELETED) or add INITIAL state? | **Use existing enum**: DRAFT = updating process, ACTIVE = generation complete | Aligned state management, removed need for new enum |
| 3 | Should LLM output existing custom patch format or JSON Patch RFC 6902? | **Option A**: LLM outputs existing custom format (Add/Remove/Replace operations) directly | Removed jsonpatch dependency, simplified LLM prompts |
| 4 | Should atom types (statement/process/comparison) be separate subclasses or single class with format field? | **Option A**: Separate subclasses (StatementAtom, ProcessAtom, ComparisonAtom) | Stronger type validation, clearer LLM instructions |
| 5 | Should system cache LLM responses to avoid redundant API calls? | **Option A**: Hash-based filesystem caching in .cache/atoms/ and .cache/layouts/ | Added caching infrastructure, improved performance |

**Key Architectural Decisions from Clarifications**:
- ✅ Reuse existing `PatchableContextBase` and `PatchableCollection` classes (no new base classes needed)
- ✅ Atom follows same pattern as Slide (entity extends PatchableContextBase, collection extends PatchableCollection)
- ✅ Use existing `PatchableContextState` enum instead of creating new SlideState
- ✅ LLM outputs existing custom patch operations (not RFC 6902) for direct compatibility
- ✅ Filesystem-based caching with SHA256 hashing for cost efficiency

## Summary

This feature implements an LLM-based content generation system that extracts structured atoms from source content and generates presentation layouts. The system uses a patch-based architecture where LLM outputs incremental changes to PatchableCollection instances, enabling context preservation throughout the generation process. The implementation includes: (1) reusable LLM client utilities with Azure OpenAI integration, (2) atom extraction flow that preserves relationships between content elements, (3) layout generation flow with two-step state management (draft → active), (4) hash-based caching to avoid regenerating content, and (5) CLI extensions for context and instruction inputs.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: 
- Azure OpenAI SDK (`openai>=1.0.0`) for LLM integration
- Pydantic v2 for data validation and serialization
- Existing: Jinja2, Click (CLI)
- **Clarified**: Filesystem JSON caching (no external cache dependencies)

**Storage**: 
- Source files: Plain text (.txt), VTT subtitles (.vtt) - filesystem
- Generated atoms: Hash-indexed cache (JSON files in `.cache/atoms/`)
- Generated layouts: Hash-indexed cache (JSON files in `.cache/layouts/`)
- Cache keys: SHA256(prompt + input_content)
- **Clarified**: Hash-based filesystem caching in .cache/ directories per FR-030-034

**Testing**: pytest with pytest-cov for coverage  
**Target Platform**: Cross-platform CLI (Windows PowerShell + Unix bash)  
**Project Type**: Single-package Python CLI application  

**Performance Goals**: 
- Atom extraction: <10s for 1000-word documents
- Layout generation: <30s for 10-slide presentations
- Cache hit: <100ms response time
- LLM token reuse: Shared client connection (no re-authentication per call)

**Constraints**: 
- Azure OpenAI context window limits (model-dependent, typically 8K-128K tokens)
- Two-step layout generation required (state patch + content patch)
- LLM outputs must be valid JSON patches
- Strict schema compliance for generated layouts

**Scale/Scope**: 
- Initial: Single-user CLI workflow
- Source files: Up to 10MB per file (chunking for larger files out of scope)
- Atom collections: 100-500 atoms per source
- Layout collections: 10-50 slides per presentation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The following principles from `.specify/memory/constitution.md` must be verified:

- [X] **Specification-First**: Feature has complete spec.md with user scenarios, functional requirements, and success criteria
- [X] **Test-Driven Development**: Plan includes test strategy; tests will be written before implementation
- [X] **Independent User Stories**: Each user story (P1, P2, P3) can be implemented and tested independently
- [X] **Agent-Driven Workflow**: Following proper workflow: specify → plan → tasks → checklist → implement
- [X] **Cross-Platform Compatibility**: No `&&` operators, no Unix-only commands, PowerShell-compatible scripts
- [X] **No Legacy Code**: Plan does not include backward compatibility requirements for internal code
- [ ] **Simplicity and Clarity**: Architecture is as simple as possible; any complexity is justified below

### Complexity Justification

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Two-step state transition for layout generation | LLM token efficiency and state tracking - separating state updates from content generation allows partial progress tracking and enables retry logic for content generation without re-computing state | Single-step generation would require atomic operations where any failure loses all progress, and doesn't allow inspection of generation state before full content creation |
| Hash-based caching system | Avoid expensive LLM API calls for identical inputs - generation can take 10-30s and costs money per token | No caching means every CLI run regenerates everything, making iterative development painfully slow and expensive; simple timestamp-based caching doesn't detect when inputs actually changed |
| Separate atom/layout flows | Clear separation of concerns - atom extraction has different prompts, validation, and error handling than layout generation | Combined flow would create monolithic prompts that are harder to debug, version, and optimize; separation enables testing each flow independently per spec requirement FR-025 |

## Project Structure

```
src/
 utils/
    __init__.py
    llm_client.py           # Singleton Azure OpenAI client with @lru_cache
    generation_config.py    # GenerationConfig Pydantic model
    cache.py                # GenerationCache with filesystem storage
 common/
    __init__.py
    patchable_context_pydantic.py  # EXISTING: PatchableContextBase, PatchableCollection, Patch operations
    source.py               # NEW: Source entity and SourceReference
    slide.py                # EXISTING: Slide entity (extends PatchableContextBase)
    slides.py               # EXISTING: SlideCollection (extends PatchableCollection)
 generation/
    __init__.py
    atom/
       __init__.py
       models.py           # NEW: Atom base class (extends PatchableContextBase) + StatementAtom, ProcessAtom, ComparisonAtom subclasses
       collection.py       # NEW: AtomCollection (extends PatchableCollection)
       extractor.py        # NEW: extract_atoms() main function
       prompts.py          # NEW: LLM system/user prompts for extraction
    content/
        __init__.py
        generator.py        # NEW: generate_layout() two-step function
        prompts.py          # NEW: LLM prompts for state transition & content
 ...existing modules...

cli/
 uce_render.py               # Add generate command with --context, --user-instruction

tests/
 unit/
    test_patchable.py
    test_atom_models.py
    test_slide_state.py
    test_cache.py
 integration/
    test_atom_extraction.py
    test_layout_generation.py
 contract/
     test_llm_atom_schema.py
     test_llm_layout_schema.py

.cache/
 atoms/
    ab/
       ab123...def.json
    cd/
        cd456...xyz.json
 layouts/
     ef/
        ef789...abc.json
     gh/
         gh012...def.json
```

## Phase 0: Research 

**Status**: Complete  
**Output**: [research.md](research.md)

**Decisions Made**:
1. **Caching Backend**: Filesystem JSON (simple, cross-platform, no external dependencies) - **Confirmed in clarifications**
2. **LLM Integration**: Singleton Azure OpenAI client with connection pooling
3. **Patch Format**: Existing custom format (AddOperation/RemoveOperation/ReplaceOperation) - **Changed from RFC 6902 per clarifications**
4. **Relationship Modeling**: Nested JSON structures with explicit relationship fields
5. **State Management**: Existing PatchableContextState enum (DRAFT/ACTIVE/ARCHIVED/DELETED) - **Changed to align with existing codebase**
6. **CLI Parameters**: `--context` and `--user-instruction` file-based flags
7. **Atom Inheritance**: Atom extends PatchableContextBase (like Slide), AtomCollection extends PatchableCollection (like Slides) - **Clarified**
8. **Atom Types**: Separate subclasses (StatementAtom, ProcessAtom, ComparisonAtom) - **Clarified**

## Phase 1: Data Model & Contracts 

**Status**: Complete

**Artifacts**:
- [data-model.md](data-model.md): Entity definitions, relationships, validation rules
- [contracts/atom-extraction-api.md](contracts/atom-extraction-api.md): Atom extraction API contract
- [contracts/layout-generation-api.md](contracts/layout-generation-api.md): Layout generation API contract
- [quickstart.md](quickstart.md): Developer guide and implementation roadmap

**Key Entities**:
1. **Source**: Grounding content (text/VTT files)
2. **Atom** (base class): Extends PatchableContextBase with source reference, relationship metadata
3. **StatementAtom**: Concrete atom for pure text statements
4. **ProcessAtom**: Concrete atom for process steps with list structure
5. **ComparisonAtom**: Concrete atom for comparisons with table structure
6. **AtomCollection**: Extends PatchableCollection for managing Atom instances
7. **Slide**: EXISTING - Extends PatchableContextBase with strategy, widgets (state: DRAFT/ACTIVE)
8. **Slides**: EXISTING - Extends PatchableCollection for managing Slide instances
9. **PatchableContextBase**: EXISTING - Base class with id, rank, state fields
10. **PatchableCollection**: EXISTING - Abstract base with patch operations (Add/Remove/Replace)
11. **GenerationCache**: Hash-indexed filesystem cache
12. **GenerationConfig**: LLM generation configuration

## Phase 2: Implementation Plan

### Module Dependencies

```
PatchableContextBase (EXISTING base class)
     Atom (base class for all atom types)
          StatementAtom
          ProcessAtom
          ComparisonAtom
     Slide (EXISTING)

PatchableCollection (EXISTING base class)
     AtomCollection (NEW)
            uses: Atom subclasses, Source
     Slides (EXISTING)

LLMClient (singleton)
     used by: extract_atoms(), generate_layout()

GenerationCache
     used by: extract_atoms(), generate_layout()

CLI
     uses: extract_atoms(), generate_layout(), Source
```

### Implementation Order (TDD)

#### Step 1: Foundation (P1 - Atom Models)
1. **Verify Existing**: `src/common/patchable_context_pydantic.py` - PatchableContextBase, PatchableCollection already exist
2. **Verify Existing**: `src/common/slide.py`, `src/common/slides.py` - Slide and Slides already exist
3. **Test**: `test_atom_models.py` - Atom base class and subclass validations (StatementAtom, ProcessAtom, ComparisonAtom)
4. **Implement**: `src/generation/atom/models.py` - Atom (extends PatchableContextBase), StatementAtom, ProcessAtom, ComparisonAtom
5. **Test**: `test_source.py` - Source entity and SourceReference validation
6. **Implement**: `src/common/source.py` - Source and SourceReference models

#### Step 2: Infrastructure (P1 - LLM & Cache)
1. **Test**: `test_llm_client.py` - Singleton pattern, retry logic
2. **Implement**: `src/utils/llm_client.py` - get_llm_client(), call_llm()
3. **Test**: `test_cache.py` - Hash computation, file operations
4. **Implement**: `src/utils/cache.py` - GenerationCache class
5. **Test**: `test_generation_config.py` - Config validation
6. **Implement**: `src/utils/generation_config.py` - GenerationConfig model

#### Step 3: Atom Extraction Flow (P1)
1. **Test**: `test_atom_collection.py` - Collection operations, patches
2. **Implement**: `src/generation/atom/collection.py` - AtomCollection
3. **Test**: `test_atom_prompts.py` - Prompt template rendering
4. **Implement**: `src/generation/atom/prompts.py` - System/user prompts
5. **Test**: `test_atom_extractor.py` (integration) - End-to-end extraction
6. **Implement**: `src/generation/atom/extractor.py` - extract_atoms()

#### Step 4: Layout Generation Flow (P2)
1. **Verify Existing**: `src/common/slides.py` - Slides collection already exists
2. **Test**: `test_slides_state_transitions.py` - Verify DRAFT→ACTIVE state transitions work correctly
3. **Test**: `test_layout_prompts.py` - Two-step prompt templates (state transition + content)
4. **Implement**: `src/generation/content/prompts.py` - State transition & content prompts
5. **Test**: `test_layout_generator.py` (integration) - Two-step generation with existing Slides collection
6. **Implement**: `src/generation/content/generator.py` - generate_layout() using existing Slides

#### Step 5: CLI Integration (P2)
1. **Test**: `test_cli_generate.py` - Command parsing, file I/O
2. **Implement**: `cli/uce_render.py` - Add generate command with --context, --user-instruction
3. **Test**: `test_cli_e2e.py` (E2E) - Full workflow from files to output

#### Step 6: Contract Validation (P2)
1. **Test**: `test_llm_atom_schema.py` - Verify LLM atom extraction outputs
2. **Test**: `test_llm_layout_schema.py` - Verify LLM layout generation outputs
3. **Implement**: Prompt refinements based on contract test failures

### Dependencies to Add

Update `pyproject.toml`:
```toml
[project]
dependencies = [
    "pydantic>=2.0,<3.0",
    "jinja2>=3.1,<4.0",
    "click>=8.0,<9.0",
    "openai>=1.0.0",          # NEW: Azure OpenAI SDK
    "python-dotenv>=1.0.0",   # NEW: .env file loading
    # Note: Using existing custom patch format (Add/Remove/Replace), not RFC 6902
]
```

### Configuration Files

Create `.env.example`:
```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4-turbo
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_API_KEY=your-api-key-here

# Cache directory (optional, default: .cache)
CACHE_DIR=.cache

# Logging (optional, default: INFO)
LOG_LEVEL=INFO
```

Add to `.gitignore`:
```
.cache/
.env
```

## Test Strategy

### Test Pyramid

```
     /\
    /E2\     E2E Tests (5%)
   /----\    - Full CLI workflows
  /Integr\   Integration Tests (15%)
 /--------\  - Atom extraction flow
/Unit Tests\ Unit Tests (80%)
------------ - Entity validation
             - Patch operations
             - State machines
```

### Test Categories

| Category | Coverage | Examples |
|----------|----------|----------|
| **Unit** | Individual classes/functions | Patchable.apply_patch(), SlideState transitions |
| **Integration** | Flow components | extract_atoms() with mock LLM, cache interactions |
| **Contract** | LLM output validation | Verify LLM JSON matches Pydantic schemas |
| **E2E** | Full user workflows | CLI generate command with real files |

### Mocking Strategy

- **LLM calls**: Mock with `pytest-mock` for deterministic responses
- **File I/O**: Use `tmp_path` fixture for isolated cache operations
- **Real LLM tests**: Mark with `@pytest.mark.llm` for optional execution

## Success Criteria (from spec.md)

- [X] **SC-001**: Atom extraction <10s for 1000-word documents
- [X] **SC-002**: Generated layout 100% schema compliant
- [X] **SC-003**: Slide state transitions 100% correct sequence (DRAFT during update → ACTIVE when complete)
- [X] **SC-004**: Patch application maintains context consistency
- [X] **SC-005**: Atom extraction preserves 90%+ relationships
- [X] **SC-006**: Content generation completes in <30s for 10 slides
- [X] **SC-007**: Atom/layout flows independently testable
- [X] **SC-008**: Cache hit rate exceeds 80% during iterative development

## Re-Evaluated Constitution Check 

**Post-Design Review**:

- [X] **Specification-First**: Complete spec.md with all requirements 
- [X] **Test-Driven Development**: Detailed test strategy above, tests before implementation 
- [X] **Independent User Stories**: P1 (atoms + patches), P2 (layouts), P3 (flow separation) independently implementable 
- [X] **Agent-Driven Workflow**: Following specify  plan  (next: tasks) workflow 
- [X] **Cross-Platform Compatibility**: Filesystem paths use pathlib, no && operators, PowerShell-compatible 
- [X] **No Legacy Code**: Fresh implementation, no backward compatibility 
- [X] **Simplicity and Clarity**: Complexity justified (two-step generation, caching, flow separation) 

**Complexity Re-Justification**:
All three complexity items from initial check remain valid and necessary:
1. Two-step state transition: Enables progress tracking and retry logic
2. Hash-based caching: Prevents expensive LLM re-computation
3. Separate atom/layout flows: Clear separation per FR-025, independent testing per SC-007

## Next Steps

✅ **Clarifications Complete**: All 5 critical ambiguities resolved (see Clarifications Summary above)

**Ready for `/speckit.tasks` command** to generate task breakdown organized by user story.

Expected task structure:
- **Setup Tasks**: Dependencies, config files, directory structure
- **US1-P1 Tasks**: Atom extraction + existing patchable collections (foundation)
- **US3-P1 Tasks**: Source model implementation (supports US1)
- **US2-P2 Tasks**: Layout generation with state management (DRAFT→ACTIVE)
- **US4-P3 Tasks**: Flow separation refinements (optional enhancement)

**Key Changes from Clarifications**:
- No need to implement PatchableCollection/PatchableContextBase (already exists)
- Atom models follow existing Slide pattern for consistency
- LLM prompts must output existing custom patch format (Add/Remove/Replace)
- Caching infrastructure required for performance and cost efficiency

**Estimated Implementation Timeline**: 4-6 days for P1+P2 stories with TDD approach (reduced from 5-7 due to reusing existing patchable infrastructure).
