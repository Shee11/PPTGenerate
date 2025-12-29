# Implementation Plan: React MDX Presentation Renderer

**Branch**: `001-react-mdx-renderer` | **Date**: 2025-12-25 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `/specs/001-react-mdx-renderer/spec.md`

## Summary

Build a **Strictly Semantic** React/MDX presentation system where AI agents generate MDX using only semantic components (no HTML/CSS). The system uses a 4-layer architecture (L0 forbidden → L3 atoms) with Compound Components for layouts. MVP delivers E2E pipeline: `state.json → MDX generation → HTML export`.

**Technical Approach**: 
- React 18+ with Next.js 14+ for SSG/export
- MDX 3.x for JSX-in-Markdown
- Tailwind CSS (internal only, hidden from Agent output)
- Compound Components pattern for semantic slots
- Python MDX generator extending existing SlidevRenderer pattern

## Technical Context

**Language/Version**: TypeScript 5.x (React components), Python 3.11+ (MDX generator/CLI)  
**Primary Dependencies**:  
- Frontend: React 18, Next.js 14, MDX 3.x, Tailwind CSS 3.x, Recharts 2.x
- Backend: Python 3.11+, Jinja2 (MDX templates)

**Storage**: N/A (file-based: state.json → MDX → HTML)  
**Testing**: 
- React: Vitest + React Testing Library
- Python: pytest (existing test infrastructure)

**Target Platform**: Browser (Chrome, Firefox, Safari), Static HTML export  
**Project Type**: web (Next.js static export)  
**Performance Goals**: 
- Render 20-slide deck in <2s
- Theme switch in <100ms
- Export 50-slide deck in <30s

**Constraints**: 
- Exported HTML <500KB (excl. images)
- No runtime server required for viewing
- Desktop 16:9 aspect ratio only

**Scale/Scope**: 
- 6 layouts, 9 blocks, 3 atoms (core set)
- 7 theme presets
- 5 vibe levels

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The following principles from `.specify/memory/constitution.md` must be verified:

- [x] **Specification-First**: Feature has complete spec.md with 5 user scenarios, 25+ functional requirements, and 7 success criteria
- [x] **Test-Driven Development**: Plan includes test strategy for both React (Vitest) and Python (pytest); tests first
- [x] **Independent User Stories**: Each story delivers standalone value:
  - US1 (P1): MDX generation works without rendering
  - US2 (P1): Rendering works with hand-written MDX
  - US3 (P2): Themes work with any valid MDX
  - US4 (P2): Export works with any rendered presentation
  - US5 (P3): CLI wraps existing functionality
- [x] **Agent-Driven Workflow**: Following specify → plan → tasks → checklist → implement
- [x] **Cross-Platform Compatibility**: Using PowerShell scripts, semicolons for command chaining
- [x] **No Legacy Code**: New implementation in `src/paged/render/react/`, no backward compat needed
- [x] **Simplicity and Clarity**: Architecture justified below

### Complexity Justification

| Complexity | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Compound Components | Required for semantic slots (`LayoutSplit.Left`) per spec FR-003 | Simple props would expose layout internals to Agent |
| Two Languages (TS+Python) | React for rendering, Python for CLI integration with existing pipeline | Pure TS would require rewriting existing CLI infrastructure |
| 4-Layer Architecture | Enforces L0 forbidden rule per spec FR-001, FR-002 | Without layers, Agents would inject HTML/CSS |

## Project Structure

```
src/paged/
├── render/
│   └── react/
│       ├── package.json              # Next.js dependencies
│       ├── next.config.js            # Static export config
│       ├── tailwind.config.js        # Internal styling
│       ├── tsconfig.json
│       │
│       ├── components/
│       │   ├── layouts/              # L1 - Layout components
│       │   │   ├── LayoutCover.tsx
│       │   │   ├── LayoutSplit.tsx   # With .Left, .Right
│       │   │   ├── LayoutGrid.tsx
│       │   │   ├── LayoutFullBleed.tsx
│       │   │   ├── LayoutTimeline.tsx
│       │   │   └── LayoutDashboard.tsx
│       │   │
│       │   ├── blocks/               # L2 - Block components
│       │   │   ├── ChartBar.tsx
│       │   │   ├── ChartLine.tsx
│       │   │   ├── ChartPie.tsx
│       │   │   ├── MetricGroup.tsx
│       │   │   ├── TableData.tsx
│       │   │   ├── SmartList.tsx
│       │   │   ├── QuoteBlock.tsx
│       │   │   ├── ImageBlock.tsx
│       │   │   └── CardGroup.tsx
│       │   │
│       │   ├── atoms/                # L3 - Atom components
│       │   │   ├── Heading.tsx
│       │   │   ├── Text.tsx
│       │   │   └── Callout.tsx
│       │   │
│       │   └── core/                 # Infrastructure
│       │       ├── SlideWrapper.tsx  # Theme/vibe provider
│       │       ├── SlideNavigation.tsx
│       │       └── MDXProvider.tsx   # Component mapping
│       │
│       ├── themes/                   # Theme definitions
│       │   ├── index.ts              # Theme registry
│       │   ├── business.ts
│       │   ├── cyber.ts
│       │   ├── minimal.ts
│       │   ├── academic.ts
│       │   ├── creative.ts
│       │   ├── duolingo.ts
│       │   └── dark.ts
│       │
│       ├── utils/
│       │   ├── validator.ts          # L0 validation
│       │   └── types.ts              # Shared types
│       │
│       ├── pages/                    # Next.js pages
│       │   └── [...slide].tsx        # Dynamic slide routes
│       │
│       └── __tests__/                # Vitest tests
│           ├── layouts.test.tsx
│           ├── blocks.test.tsx
│           ├── atoms.test.tsx
│           └── validator.test.ts
│
└── render/
    └── react/
        └── mdx_renderer.py           # Python MDX generator

cli/
└── uce_render.py                     # Add --project react-mdx
```

## Architecture

### Layer Enforcement (L0-L3)

```
┌─────────────────────────────────────────────────────────────┐
│  L0: FORBIDDEN (Agent cannot use)                           │
│  div, span, className, style, dangerouslySetInnerHTML       │
└─────────────────────────────────────────────────────────────┘
                              ↓ BLOCKED
┌─────────────────────────────────────────────────────────────┐
│  L1: LAYOUTS (Agent uses for page structure)                │
│  LayoutCover, LayoutSplit, LayoutGrid, LayoutFullBleed,     │
│  LayoutTimeline, LayoutDashboard                            │
│  └── Compound slots: .Left, .Right, .Header, .Main, .Footer │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  L2: BLOCKS (Agent uses for content grouping)               │
│  ChartBar, ChartLine, ChartPie, MetricGroup, TableData,     │
│  SmartList, QuoteBlock, ImageBlock, CardGroup               │
│  └── Props: data, size, variant, intent                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  L3: ATOMS (Agent uses for text content)                    │
│  Heading, Text, Callout                                     │
│  └── Props: level, variant, intent                          │
└─────────────────────────────────────────────────────────────┘
```

### Rendering Pipeline

```
state.json → MDX Generator (Python) → .mdx files → Next.js build → Static HTML
     │                                      │              │
     │                                      ↓              │
     │                              MDX Validation         │
     │                              (L0 check)             │
     │                                      │              │
     └──────────────────────────────────────┴──────────────┘
                                                           ↓
                                               HTML + CSS + JS bundle
```

### Compound Component Pattern

```tsx
// Agent writes:
<LayoutSplit ratio="2:1">
  <LayoutSplit.Left>
    <ChartBar data={[...]} />
  </LayoutSplit.Left>
  <LayoutSplit.Right>
    <SmartList items={[...]} />
  </LayoutSplit.Right>
</LayoutSplit>

// Internally renders:
<div className="grid grid-cols-[2fr_1fr]">
  <div className="p-8">{left}</div>
  <div className="p-8">{right}</div>
</div>
```

## Implementation Phases

### Phase 0: Setup & Research (This Plan)
- [x] Create spec.md
- [x] Research React/MDX patterns (see research.md)
- [x] Define data model (see data-model.md)
- [x] Define contracts (see contracts/)
- [x] Create quickstart.md

### Phase 1: MVP Foundation (E2E Pipeline)
**Goal**: Render a single slide from state.json to HTML

1. **Setup Next.js project** (`src/paged/render/react/`)
2. **Core infrastructure**:
   - SlideWrapper (theme context)
   - MDXProvider (component mapping)
3. **3 minimal layouts** (LayoutCover, LayoutSplit, LayoutGrid)
4. **3 minimal blocks** (SmartList, ChartBar, MetricGroup)
5. **3 atoms** (Heading, Text, Callout)
6. **1 theme** (business - default)
7. **MDX generator** (Python: state.json → MDX)
8. **Static export** (Next.js build)

### Phase 2: Full Component Set
- Remaining 3 layouts (FullBleed, Timeline, Dashboard)
- Remaining 6 blocks (ChartLine, ChartPie, TableData, QuoteBlock, ImageBlock, CardGroup)
- L0 validator
- Slide navigation

### Phase 3: Themes & Polish
- 6 additional themes
- 5 vibe levels
- Cross-browser testing
- Error messages with suggestions

### Phase 4: CLI Integration
- Add `--project react-mdx` to CLI
- Verbose mode
- Error handling

## Testing Strategy

### React (Vitest + RTL)

```typescript
// layouts.test.tsx
describe('LayoutSplit', () => {
  it('renders left and right slots', () => {
    render(
      <LayoutSplit>
        <LayoutSplit.Left>Left content</LayoutSplit.Left>
        <LayoutSplit.Right>Right content</LayoutSplit.Right>
      </LayoutSplit>
    );
    expect(screen.getByText('Left content')).toBeInTheDocument();
    expect(screen.getByText('Right content')).toBeInTheDocument();
  });
  
  it('applies ratio prop correctly', () => {
    const { container } = render(<LayoutSplit ratio="2:1" />);
    expect(container.firstChild).toHaveClass(/grid-cols-\[2fr_1fr\]/);
  });
});

// validator.test.ts
describe('L0 Validator', () => {
  it('rejects div elements', () => {
    const mdx = '<div>content</div>';
    expect(validateMDX(mdx)).toContainError('L0 violation: div is forbidden');
  });
  
  it('rejects className prop', () => {
    const mdx = '<Heading className="foo">text</Heading>';
    expect(validateMDX(mdx)).toContainError('L0 violation: className is forbidden');
  });
});
```

### Python (pytest)

```python
# test_mdx_renderer.py
def test_render_cover_slide():
    slide = {
        "layout": "cover",
        "widgets": {
            "title": {"type": "Type.Display", "parameters": {"text": "Hello"}},
            "subtitle": {"type": "Type.Body", "parameters": {"text": "World"}}
        }
    }
    mdx = ReactMDXRenderer().render_slide(slide)
    assert "<LayoutCover>" in mdx
    assert '<Heading level={1}>Hello</Heading>' in mdx

def test_no_html_in_output():
    mdx = ReactMDXRenderer().render_state(state_json)
    assert "<div" not in mdx
    assert "className" not in mdx
```

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| MDX 3.x complexity | Use well-documented @mdx-js/react; fallback to raw React if needed |
| Chart library bundle size | Use Recharts tree-shaking; evaluate lightweight alternatives |
| Static export limitations | Design for SSG from start; no SSR/ISR features |
| Agent generates invalid MDX | Strict validation + helpful error messages |

## Dependencies

### npm packages
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "next": "^14.0.0",
    "@mdx-js/react": "^3.0.0",
    "@mdx-js/loader": "^3.0.0",
    "recharts": "^2.10.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "tailwindcss": "^3.4.0",
    "vitest": "^1.0.0",
    "@testing-library/react": "^14.0.0"
  }
}
```

### Python packages
- Jinja2 (existing)
- No new Python dependencies

## Success Metrics (from spec)

- [ ] SC-001: 95% valid MDX generation
- [ ] SC-002: Zero L0 violations in output
- [ ] SC-003: <2s render for 20 slides
- [ ] SC-004: <100ms theme switch
- [ ] SC-005: <500KB HTML export
- [ ] SC-006: 100% layout parity with Slidev
- [ ] SC-007: <30s CLI export for 50 slides

---

## Artifacts

- [research.md](research.md) - Phase 0 research findings
- [data-model.md](data-model.md) - Entity definitions
- [contracts/](contracts/) - API contracts
- [quickstart.md](quickstart.md) - Getting started guide
