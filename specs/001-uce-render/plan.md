# Implementation Plan: Universal Content Engine - Rendering System

**Branch**: `001-uce-render` | **Date**: 2025-12-11 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-uce-render/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a Python-based rendering system for the Universal Content Engine that converts layout configurations (Bento, Swiss, Cinematic strategies) with widget placements into HTML output. The system enforces T-Shirt size constraints (S/M/L/XL), applies themes and styles via a patchable configuration pattern, and provides both CLI and programmatic interfaces. Core components include LayoutEngine for position calculation, HTMLRenderer for output generation, and a comprehensive widget library (Typography, Data, Media, Charts).

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: Pydantic 2.x (validation), Jinja2 3.x (templating), Click 8.x (CLI)  
**Storage**: N/A (stateless rendering, JSON input/output)  
**Testing**: pytest 7.x with contract/integration/unit hierarchy  
**Target Platform**: Cross-platform (Windows, Linux, macOS) via Python  
**Project Type**: Single project (library + CLI)  
**Performance Goals**: <100ms for simple layouts (≤6 widgets), <500ms for complex layouts (10+ widgets, charts)  
**Constraints**: <50MB memory per render, pure Python (no JavaScript required), offline-capable  
**Scale/Scope**: Support 100+ widgets per layout, 50+ layout variants, extensible widget registry

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The following principles from `.specify/memory/constitution.md` must be verified:

- [X] **Specification-First**: Feature has complete spec.md with user scenarios, functional requirements, and success criteria
- [X] **Test-Driven Development**: Plan includes test strategy; tests will be written before implementation
- [X] **Independent User Stories**: Each user story (P1, P2, P3) can be implemented and tested independently
- [X] **Agent-Driven Workflow**: Following proper workflow: specify → plan → tasks → checklist → implement
- [X] **Cross-Platform Compatibility**: No `&&` operators, no Unix-only commands, PowerShell-compatible scripts
- [X] **No Legacy Code**: Plan does not include backward compatibility requirements for internal code
- [X] **Simplicity and Clarity**: Architecture is as simple as possible; any complexity is justified below

### Complexity Justification

No violations - architecture follows simplicity principles:
- Direct pipeline: Layouts + Styles → LayoutEngine → RenderableLayout → HTMLRenderer → HTML
- Strategy pattern for layout variants is the simplest approach for 10+ variants
- Widget registry pattern is simpler than manual imports for 20+ widget types
- Pydantic for validation is industry standard, not custom solution

## Project Structure

### Documentation (this feature)

```
specs/001-uce-render/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── cli-contract.md
│   └── python-api.md
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
src/
├── common/
│   └── patchable_context_pydantic.py  # Base class for Layouts/Styles collections
├── layout/
│   ├── __init__.py
│   ├── theme.py                        # Theme configuration (fonts, colors)
│   ├── style.py                        # Style definitions (rounded corners, shadows)
│   ├── layout_engine.py                # Core engine: position calculation + validation
│   └── strategies/                     # Layout strategy implementations
│       ├── __init__.py
│       ├── base.py                     # LayoutStrategy protocol
│       ├── bento.py                    # Bento variants (Standard, HeroLeft, HeroTop, Quarter)
│       ├── swiss.py                    # Swiss variants (Poster, Asymmetry, SplitTypo)
│       └── cinematic.py                # Cinematic variants (FullBleed, Split_30_70, Split_50_50)
└── render/
    ├── __init__.py
    ├── html_renderer.py                # HTML generation from RenderableLayout
    ├── widgets/                        # Widget implementations
    │   ├── __init__.py
    │   ├── base.py                     # BaseWidget + WidgetRegistry
    │   ├── typography.py               # Type.Display, Heading, Body, List, Quote
    │   ├── data.py                     # Data.BigNum, Trend, Progress
    │   ├── media.py                    # Media.Frame, Code, Icon
    │   └── charts.py                   # Chart.Bar, Line, Pie, Radar, Sankey
    └── templates/                      # Jinja2 templates
        ├── base.html.j2                # HTML document wrapper
        ├── layouts/                    # Layout-specific templates
        │   ├── bento.html.j2
        │   ├── swiss.html.j2
        │   └── cinematic.html.j2
        └── widgets/                    # Widget-specific templates
            ├── typography.html.j2
            ├── data.html.j2
            ├── media.html.j2
            └── charts.html.j2

tests/
├── contract/
│   ├── test_layout_schema.py           # JSON schema validation for Layouts
│   ├── test_style_schema.py            # JSON schema validation for Styles
│   ├── test_renderable_schema.py       # RenderableLayout structure validation
│   └── test_cli_contract.py            # CLI exit codes, error messages, output format
├── integration/
│   ├── test_bento_rendering.py         # Full pipeline: Bento layouts → HTML
│   ├── test_swiss_rendering.py         # Full pipeline: Swiss layouts → HTML
│   ├── test_cinematic_rendering.py     # Full pipeline: Cinematic layouts → HTML
│   ├── test_size_validation_e2e.py     # Size constraint enforcement across pipeline
│   └── test_style_application.py       # Theme + Style → CSS output
└── unit/
    ├── test_layout_engine.py           # Position calculation logic
    ├── test_size_validation.py         # SizeClass comparison, constraint checking
    ├── test_patchable_context.py       # PatchableContextPydantic.patch() behavior
    ├── test_strategy_slots.py          # Each layout strategy's slot definitions
    └── test_widgets/                   # Widget-specific tests
        ├── test_typography_widgets.py
        ├── test_data_widgets.py
        ├── test_media_widgets.py
        └── test_chart_widgets.py

cli/
└── uce_render.py                       # Click CLI entry point

examples/                               # Working examples for documentation
├── executive-dashboard/
│   ├── layout.json
│   ├── styles.json
│   ├── atom-data.json
│   ├── output.html
│   └── README.md
├── product-launch/
│   └── ...
└── comparison-view/
    └── ...
```

**Structure Decision**: Single project structure selected because:
- Pure Python library with CLI wrapper (no frontend/backend split needed)
- All rendering happens server-side in Python
- HTML output is static (no JavaScript runtime required)
- Tests, source, and CLI coexist naturally in single project

## Phase 0: Research & Decisions

**Status**: ✅ Complete - See [research.md](research.md)

**Key Decisions**:
1. **HTML Rendering**: Jinja2 template-based (separation of concerns, security, testability)
2. **Validation**: Pydantic v2 with ConfigDict for runtime validation and JSON schema
3. **Layout Calculation**: Strategy Pattern with CSS Grid coordinate system
4. **Widget Registry**: Type-based registry with factory pattern for dynamic loading
5. **Size Representation**: IntEnum with ordering support (`SizeClass.M < SizeClass.L`)
6. **CLI Framework**: Click for robust CLI with JSON output support
7. **Testing**: pytest with contract/integration/unit hierarchy and snapshot testing

## Phase 1: Design

**Status**: ✅ Complete

### Data Model

See [data-model.md](data-model.md) for complete entity definitions.

**Core Entities**:
- `SizeClass` (Enum): S/M/L/XL with ordering
- `Theme`: Color and typography configuration
- `Style`: Theme + geometric properties (border-radius, shadow, spacing)
- `Slot`: Positioned region with size class
- `Layout`: Screen division strategy with slots
- `Widget` (Abstract): Base for all renderable components
- `WidgetAssignment`: Binds widget + style to slot
- `Layouts` (Collection): PatchableContextPydantic for layout configurations
- `Styles` (Collection): PatchableContextPydantic for theme/style configurations
- `RenderableLayout`: Intermediate representation after calculation

### API Contracts

See [contracts/](contracts/) for complete specifications.

**CLI Contract**: `uce-render LAYOUTS_FILE STYLES_FILE [OPTIONS]`
- Exit codes: 0 (success), 1 (invalid args), 2 (validation), 3 (rendering)
- Output formats: HTML (default), JSON (debug)
- Validation mode: `--validate-only` flag

**Python API**:
- `LayoutEngine.calculate(layouts, styles) -> RenderableLayout`
- `HTMLRenderer.render(renderable) -> str`
- `PatchableContextPydantic.patch(updates) -> Self`
- Widget registry: `@WidgetRegistry.register("Type.Display")`

### Architecture

**Data Flow**:
```
┌─────────┐    ┌─────────┐
│ Layouts │    │ Styles  │
│  .json  │    │  .json  │
└────┬────┘    └────┬────┘
     │              │
     └──────┬───────┘
            ↓
     ┌──────────────┐
     │LayoutEngine  │  ← Validates sizes, calculates positions
     └──────┬───────┘
            ↓
   ┌─────────────────┐
   │RenderableLayout │  ← Intermediate representation
   └────────┬────────┘
            ↓
     ┌──────────────┐
     │HTMLRenderer  │  ← Jinja2 templating
     └──────┬───────┘
            ↓
        ┌──────┐
        │ HTML │
        └──────┘
```

**Key Patterns**:
- **Strategy Pattern**: Layout variants (Bento.Standard, Swiss.Poster, etc.)
- **Factory Pattern**: Widget creation via registry
- **Template Method**: BaseWidget.render_html() uses Jinja2 templates
- **Immutable Pipeline**: Each stage produces new immutable objects

## Testing Strategy

### Test Hierarchy

**Contract Tests** (Schema Validation):
- Layouts JSON schema matches Pydantic model
- Styles JSON schema matches Pydantic model
- CLI exit codes and error message formats
- Minimum coverage: 100% of public API contracts

**Integration Tests** (End-to-End):
- Each layout strategy variant renders correctly
- Size violations detected before rendering
- Styles correctly applied to HTML output
- Minimum coverage: All layout variants, all widget types

**Unit Tests** (Component Isolation):
- LayoutEngine position calculations
- SizeClass comparisons and validations
- PatchableContextPydantic patch behavior
- Widget parameter validation
- Strategy slot definitions
- Minimum coverage: 90% line coverage

### Test-Driven Development Workflow

Per constitution Principle II:

1. **RED**: Write failing tests for user story acceptance criteria
2. **Approval**: Stakeholder reviews tests as acceptance criteria
3. **Verify**: Run tests, confirm they fail for right reasons
4. **GREEN**: Implement minimum code to pass tests
5. **REFACTOR**: Improve code while keeping tests green

**Example for US1 (Basic Rendering)**:
```python
# RED: Write test first
def test_bento_standard_renders_6_widgets():
    layout = create_bento_standard_layout()  # Fixture
    styles = create_default_styles()         # Fixture
    
    engine = LayoutEngine()
    renderable = engine.calculate(layout, styles)
    
    renderer = HTMLRenderer()
    html = renderer.render(renderable)
    
    # Verify all 6 slots rendered
    assert html.count('class="widget"') == 6
    assert 'grid-template-rows: 1fr 1fr' in html
    assert 'grid-template-columns: 1fr 1fr 1fr' in html

# Test FAILS (LayoutEngine not implemented yet)
# → Implement LayoutEngine.calculate()
# → Test PASSES
# → Refactor if needed
```

## Implementation Phases (from tasks.md)

**Phase 1: Setup**
- Initialize Python project structure
- Configure pytest, Pydantic, Click dependencies
- Setup Jinja2 template directories

**Phase 2: Foundation (Blocking)**
- Implement SizeClass enum
- Implement PatchableContextPydantic base class
- Implement Theme and Style models
- Implement Slot and Layout models
- Setup WidgetRegistry pattern

**Phase 3: User Story 1 (P1 MVP)**
- Implement layout strategies (Bento.Standard, Swiss.Poster, Cinematic.Split_50_50)
- Implement LayoutEngine with size validation
- Implement basic widgets (Type.Display, Type.Body, Data.BigNum)
- Implement HTMLRenderer with Jinja2
- CLI basic functionality

**Phase 4: User Story 2 (P1 Validation)**
- Enhanced size constraint error messages
- Cross-validation of widget assignments
- CLI validation mode

**Phase 5: User Story 3 (P2 Parameters)**
- Widget parameter schemas
- Parameter application in templates
- Style resolution and CSS generation

**Phase 6: User Story 4 (P2 Variants)**
- Complete all Bento variants (HeroLeft, HeroTop, Quarter)
- Complete all Swiss variants (Asymmetry, SplitTypo)
- Complete all Cinematic variants (FullBleed, Split_30_70)

**Phase 7: User Story 5 (P3 Charts)**
- Implement Chart.Bar, Chart.Line, Chart.Pie
- Implement Chart.Radar, Chart.Sankey
- Data binding for atom_data payloads

## Performance Targets

**Rendering Performance**:
- Simple layouts (≤6 widgets): <100ms
- Complex layouts (10+ widgets, charts): <500ms

**Memory Constraints**:
- Max 50MB per render operation
- No memory leaks (test with 1000 consecutive renders)

**Optimization Strategies**:
- Lazy Jinja2 template compilation (compile once, cache)
- Widget HTML memoization for repeated widget types
- Early size validation (fail fast before expensive rendering)

## Security Considerations

**Input Validation**:
- All JSON inputs validated via Pydantic schemas
- Size limits: Reject layouts with >100 widgets (DoS prevention)
- CSS value sanitization: Validate colors, lengths, URLs

**Output Safety**:
- Jinja2 auto-escaping prevents XSS
- No eval() or exec() usage
- File paths sanitized (no directory traversal)

**Safe Defaults**:
- Missing style → use default_style_name
- Invalid color → fallback to black/white
- Missing atom_data → display placeholder (don't crash)

## Open Questions / Risks

**None** - All critical decisions resolved in Phase 0 research.

**Future Enhancements** (Not in v1.0):
- PDF/SVG renderers (same RenderableLayout, different renderer)
- Custom widget loading from external modules
- Interactive widgets (requires JavaScript renderer)
- Server-side rendering API (FastAPI wrapper)
- Theme marketplace / sharing

## Next Steps

1. Run `/speckit.tasks` to generate task breakdown
2. Run `/speckit.checklist` to generate quality checklists
3. Begin implementation with Phase 1 (Setup) tasks
4. Follow TDD workflow for all user stories

## Project Structure
