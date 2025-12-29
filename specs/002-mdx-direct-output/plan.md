# Implementation Plan: MDX Direct Output

**Branch**: `002-mdx-direct-output` | **Date**: 2024-12-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-mdx-direct-output/spec.md`

## Summary

Refactor LLM content generation to output MDX/JSX markup directly instead of JSON widget definitions. Store raw MDX in state.json `mdx` field, use `<Patch id="...">` format for incremental refinements. Eliminates JSON-to-MDX conversion step in rendering pipeline.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: React MDX renderer, existing generator infrastructure  
**Storage**: state.json (file-based)  
**Testing**: pytest  
**Target Platform**: Cross-platform (Windows, macOS, Linux)
**Project Type**: single  
**Performance Goals**: N/A (generation latency dominated by LLM)  
**Constraints**: Backward compatible with slidev JSON mode  
**Scale/Scope**: Same as current (10-15 slides per deck)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Specification-First**: Feature has complete spec.md with user scenarios, functional requirements, and success criteria
- [x] **Test-Driven Development**: Plan includes test strategy; tests will be written before implementation
- [x] **Independent User Stories**: Each user story (P1, P2, P3) can be implemented and tested independently
- [x] **Agent-Driven Workflow**: Following proper workflow: specify → plan → tasks → checklist → implement
- [x] **Cross-Platform Compatibility**: No `&&` operators, no Unix-only commands, PowerShell-compatible scripts
- [x] **No Legacy Code**: Plan removes JSON-to-MDX conversion code for react-mdx mode
- [x] **Simplicity and Clarity**: Architecture simplified by removing conversion layer

### Complexity Justification

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Dual output modes (JSON/MDX) | External slidev compatibility | Removing JSON mode would break slidev users |

## Project Structure

```
src/
├── generation/content/
│   ├── prompts.py          # UPDATE: MDX prompt format for react-mdx
│   ├── generator.py        # UPDATE: MDX parser, patch parser
│   └── mdx_parser.py       # NEW: Extract slides from MDX output
├── paged/
│   ├── layout/react/
│   │   └── layout_engine.py  # UPDATE: MDX component reference
│   └── render/react/
│       └── mdx_renderer.py   # UPDATE: Read mdx field directly
└── common/
    └── slides.py           # UPDATE: Add mdx field, patch logic
```

## Architecture

### Data Flow (react-mdx mode)

```
User Input → Atoms
     ↓
LLM Prompt (MDX format instructions)
     ↓
LLM Output: <Slide id="...">MDX content</Slide>
     ↓
MDX Parser → Extract slides + mdx content
     ↓
State.json: { id, rank, story, atoms, mdx }
     ↓
Renderer: Read mdx field directly → React
```

### Refinement Flow

```
Existing Slides + User Instruction
     ↓
LLM Prompt (include current MDX)
     ↓
LLM Output: <Patch id="widget_id">new content</Patch>
     ↓
Patch Parser → Extract patches
     ↓
Apply patches to slide.mdx
     ↓
Updated State.json
```

## Key Design Decisions

### Decision 1: MDX-in-JSON vs Pure MDX Files
**Choice**: MDX-in-JSON (store MDX string in `mdx` field)
**Rationale**: 
- Preserves JSON structure for metadata (rank, story, atoms)
- Simpler migration path
- JSON patch still works for non-content fields

### Decision 2: Patch Format
**Choice**: XML-style `<Patch id="...">` blocks
**Rationale**:
- Matches MDX output format (consistency)
- Easy to parse with regex
- Clear boundaries between patches

### Decision 3: Element IDs
**Choice**: Require `id` attribute on all patchable elements
**Rationale**:
- Enables targeted updates
- Simple string matching for patch application
- Human-readable identifiers

## Test Strategy

### Unit Tests
- MDX parser: Extract slides from LLM output
- Patch parser: Extract patches from refinement output  
- Patch application: Update MDX content correctly

### Integration Tests
- Full generation flow with `project=react-mdx`
- Refinement flow with patch application
- Backward compatibility with `project=slidev`

### Contract Tests
- Validate MDX output against component inventory
- Validate patch format

## References

- [research.md](research.md) - Current architecture analysis
- [data-model.md](data-model.md) - Slide state and patch schemas
- [contracts/mdx-output.md](contracts/mdx-output.md) - LLM output format
- [contracts/patch-format.md](contracts/patch-format.md) - Patch specification
- [quickstart.md](quickstart.md) - Usage guide
