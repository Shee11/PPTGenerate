# Implementation Plan: Extended Chart Types with Intelligent Selection

**Branch**: `003-extended-chart-types` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-extended-chart-types/spec.md`

## Summary

Extend the React-based slide generation system to support 8 chart types (area, bar, barStats, bubble, doughnut, pie, polarArea, radar) with LLM-based intelligent chart type selection. The LLM will analyze data patterns during content generation to automatically choose the most effective visualization for attendees.

## Technical Context

**Language/Version**: TypeScript 5.x (React components), Python 3.11 (content generation)  
**Primary Dependencies**: Recharts (already in use), React 18, Python LLM generation pipeline  
**Storage**: N/A (stateless rendering)  
**Testing**: Jest/React Testing Library (components), pytest (Python generation)  
**Target Platform**: Web (Next.js SSR/SSG)
**Project Type**: web (monorepo with React renderer + Python generation)  
**Performance Goals**: Chart rendering < 100ms for datasets < 50 points  
**Constraints**: Must integrate with existing MDX output format and Recharts patterns  
**Scale/Scope**: 8 new chart components, 1 chart selector module

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Specification-First**: Feature has complete spec.md with user scenarios, functional requirements, and success criteria
- [x] **Test-Driven Development**: Plan includes test strategy; tests will be written before implementation
- [x] **Independent User Stories**: Each user story (P1, P2, P3) can be implemented and tested independently
- [x] **Agent-Driven Workflow**: Following proper workflow: specify → plan → tasks → checklist → implement
- [x] **Cross-Platform Compatibility**: No `&&` operators, no Unix-only commands, PowerShell-compatible scripts
- [x] **No Legacy Code**: Plan does not include backward compatibility requirements for internal code
- [x] **Simplicity and Clarity**: Architecture is as simple as possible; each chart is a standalone component

### Complexity Justification

No complexity violations. Design follows existing patterns:
- Each chart type is a separate React component (matches existing ChartBar, ChartLine, ChartPie)
- LLM chart selection integrates into existing content generation pipeline
- All components use Recharts (already a dependency)

## Project Structure

```
src/
├── paged/
│   ├── render/
│   │   └── react/
│   │       └── components/
│   │           └── blocks/
│   │               ├── ChartBar.tsx      # Existing - extend with barStats variant
│   │               ├── ChartLine.tsx     # Existing - extend with area variant
│   │               ├── ChartPie.tsx      # Existing - already has donut variant
│   │               ├── ChartArea.tsx     # NEW - area chart
│   │               ├── ChartBubble.tsx   # NEW - bubble chart
│   │               ├── ChartRadar.tsx    # NEW - radar/spider chart
│   │               ├── ChartPolar.tsx    # NEW - polar area chart
│   │               └── index.ts          # Update exports
│   └── layout/
│       └── react/
│           └── layout_engine.py          # Update chart documentation
└── generation/
    └── content/
        ├── chart_selector.py             # NEW - LLM chart type selection
        ├── prompts.py                    # Update with chart selection prompts
        └── layout_generator.py           # Integrate chart selector

specs/003-extended-chart-types/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    ├── chart-components.tsx              # Component interfaces
    └── chart-selector.py                 # Selector interface
```

## Phase 0: Research

### Research Tasks

1. **Recharts Capabilities**: Verify Recharts supports all 8 chart types natively
   - Decision: Use Recharts for all charts (Radar, PolarAngle, Area, Scatter/Bubble all supported)
   - Rationale: Already a dependency, consistent API, good React integration
   - Alternatives: Chart.js (rejected - requires wrapper), D3 (rejected - too low-level)

2. **Data Format Patterns**: Define unified data format for all chart types
   - Decision: Extend existing `ChartDataPoint` type with optional fields
   - Rationale: Backward compatible, single source of truth
   - Base format: `{label: string, value: number, color?: string}`
   - Extended fields: `x?, y?, size?` for bubble; `category?` for radar axes

3. **LLM Chart Selection Strategy**: Determine selection integration point
   - Decision: Integrate during MDX generation in `layout_generator.py`
   - Rationale: LLM already generates MDX; add chart selection as pre-processing step
   - Pattern: Analyze atom visual hints + data structure → select chart type → generate MDX

## Phase 1: Data Model & Contracts

### Data Model (data-model.md)

```typescript
// Extended ChartDataPoint (extends existing)
interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
  // Extended fields for specific chart types
  x?: number;        // Bubble chart X position
  y?: number;        // Bubble chart Y position  
  size?: number;     // Bubble chart bubble size
  before?: number;   // Clustered bar comparison
  after?: number;    // Clustered bar comparison
}

// Chart types enum
type ChartType = 
  | 'area'       // Area chart (filled line)
  | 'bar'        // Vertical bar chart
  | 'barStats'   // Horizontal bar chart
  | 'bubble'     // Bubble/scatter chart
  | 'doughnut'   // Doughnut (ring) chart
  | 'pie'        // Pie chart
  | 'polarArea'  // Polar area chart
  | 'radar';     // Radar/spider chart

// Chart selection input
interface ChartSelectionInput {
  data: ChartDataPoint[];
  atomVisualHint?: string;  // From atom.visual field
  dataDescription?: string; // Context about what data represents
}

// Chart selection output
interface ChartSelectionResult {
  chartType: ChartType;
  confidence: number;       // 0-1 confidence score
  reasoning: string;        // Why this chart type was selected
}
```

### Contracts

#### React Components (contracts/chart-components.tsx)

```typescript
// ChartArea props
interface ChartAreaProps {
  data: ChartDataPoint[];
  title?: string;
  subtitle?: string;
  height?: Size;
  gradient?: boolean;      // Soft gradient fill
  curve?: 'linear' | 'smooth';
}

// ChartBubble props
interface ChartBubbleProps {
  data: Array<{label: string; x: number; y: number; size: number; color?: string}>;
  title?: string;
  subtitle?: string;
  size?: Size;
  xLabel?: string;
  yLabel?: string;
}

// ChartRadar props
interface ChartRadarProps {
  data: ChartDataPoint[];   // Each point is an axis
  title?: string;
  subtitle?: string;
  size?: Size;
  fillOpacity?: number;     // Soft fill opacity (0-1)
}

// ChartPolar props
interface ChartPolarProps {
  data: ChartDataPoint[];
  title?: string;
  subtitle?: string;
  size?: Size;
  innerRadius?: number;     // 0 = full pie, >0 = ring
}

// Extended ChartBar for barStats variant
interface ChartBarProps {
  // ... existing props
  orientation?: 'vertical' | 'horizontal';  // horizontal = barStats
}
```

#### Python Chart Selector (contracts/chart-selector.py)

```python
from dataclasses import dataclass
from typing import Literal

ChartType = Literal['area', 'bar', 'barStats', 'bubble', 'doughnut', 'pie', 'polarArea', 'radar']

@dataclass
class ChartSelectionInput:
    data: list[dict]           # Chart data points
    atom_visual_hint: str      # From atom.visual field
    data_description: str      # Context about data meaning
    
@dataclass
class ChartSelectionResult:
    chart_type: ChartType
    confidence: float          # 0.0-1.0
    reasoning: str

def select_chart_type(input: ChartSelectionInput) -> ChartSelectionResult:
    """LLM-based chart type selection."""
    ...
```

## Phase 2: Implementation Tasks

### User Story 1: Render Extended Chart Types (P1)

#### US1-T1: Create ChartArea Component
- Create `ChartArea.tsx` using Recharts AreaChart
- Support gradient fills with soft colors
- Props: data, title, subtitle, height, gradient, curve
- Export from blocks/index.ts

#### US1-T2: Create ChartBubble Component  
- Create `ChartBubble.tsx` using Recharts ScatterChart
- Support variable bubble sizes with translucent fills
- Props: data (with x, y, size), title, xLabel, yLabel
- Export from blocks/index.ts

#### US1-T3: Create ChartRadar Component
- Create `ChartRadar.tsx` using Recharts RadarChart
- Support soft fill with configurable opacity
- Props: data, title, size, fillOpacity
- Export from blocks/index.ts

#### US1-T4: Create ChartPolar Component
- Create `ChartPolar.tsx` using Recharts RadialBarChart
- Support varying radii with equal angles
- Props: data, title, size, innerRadius
- Export from blocks/index.ts

#### US1-T5: Extend ChartBar for Horizontal Variant
- Add `orientation` prop to ChartBar.tsx
- horizontal = barStats visual style
- Maintain backward compatibility

#### US1-T6: Apply Soft Organic Styling
- Create shared chart CSS variables for earthy palette
- Apply rounded edges, soft shadows, gradient fills
- Ensure visual consistency across all chart types

### User Story 2: LLM-Based Chart Type Selection (P1)

#### US2-T1: Create Chart Selector Module
- Create `src/generation/content/chart_selector.py`
- Implement `select_chart_type()` function
- Define selection prompt with chart type guidelines

#### US2-T2: Define Chart Selection Prompt
- Create prompt template with data pattern rules:
  - Time-series → area/line
  - Categorical comparison → bar
  - Proportions → pie/doughnut
  - 3D data → bubble
  - Multivariate → radar
  - Cyclical → polarArea
  - Rankings → barStats

#### US2-T3: Integrate Selector into Layout Generator
- Modify `layout_generator.py` to call chart selector
- Trigger when atom.visual = "chart" and chartType not specified
- Pass selection result to MDX generation

#### US2-T4: Handle Fallback Cases
- Default to 'bar' when confidence < 0.5
- Honor explicit chart type in atoms
- Log selection reasoning for debugging

### User Story 3: Chart Type Documentation (P2)

#### US3-T1: Update Layout Engine Documentation
- Modify `layout_engine.py` `get_layout_documentation()`
- Add all 8 chart types with:
  - Data format specification
  - Best use cases
  - Example MDX syntax

#### US3-T2: Update Content Generation Prompts
- Modify `prompts.py` with chart selection guidance
- Add chart type examples to MDX output format section

### User Story 4: Consistent Visual Styling (P3)

#### US4-T1: Define Earthy Color Palette
- Create CSS custom properties for chart colors
- Warm, harmonious tones (terracotta, sage, sand)
- Ensure accessibility contrast ratios

#### US4-T2: Apply Styling to All Charts
- Soft border-radius on all chart containers
- Subtle shadows for depth
- Consistent typography for titles/labels

## Testing Strategy

### Contract Tests (test first)
- `test_chart_area_renders_with_data.tsx`
- `test_chart_bubble_handles_3d_data.tsx`
- `test_chart_radar_renders_multivariate.tsx`
- `test_chart_polar_renders_varying_radii.tsx`
- `test_chart_selector_time_series.py`
- `test_chart_selector_proportions.py`
- `test_chart_selector_fallback.py`

### Integration Tests
- `test_mdx_generation_with_chart_selection.py`
- `test_layout_documentation_includes_charts.py`

### Visual Regression Tests
- Snapshot tests for each chart type with sample data
- Verify soft styling applied consistently

## Dependencies

- **Recharts**: Already installed, supports all required chart types
- **React**: Already installed (18.x)
- **Python LLM Pipeline**: Existing infrastructure in `src/generation/`

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Recharts doesn't support polar area exactly | Use RadialBarChart with custom styling |
| LLM selection inconsistent | Define clear rules + confidence threshold + fallback |
| Performance with large datasets | Limit to 50 data points, show warning for more |

## Constitution Check - Post-Design

*Re-evaluated after Phase 1 design completion.*

- [x] **Specification-First**: Design aligns with spec.md user scenarios and functional requirements
- [x] **Test-Driven Development**: Testing strategy defined with contract tests first, implementation tests after
- [x] **Independent User Stories**: 
  - US1 (Render Charts) can be tested without US2 (LLM Selection)
  - US2 (LLM Selection) can be tested without US1 by mocking chart components
  - US3 (Documentation) independent of implementation
  - US4 (Styling) can be applied incrementally
- [x] **Agent-Driven Workflow**: Plan produces required artifacts (data-model.md, contracts/, quickstart.md)
- [x] **Cross-Platform Compatibility**: No platform-specific commands in plan; Python/TypeScript are cross-platform
- [x] **No Legacy Code**: Extending existing components without backward compatibility layers; existing ChartPie already supports donut variant
- [x] **Simplicity and Clarity**: 
  - Each chart is a standalone component (no complex inheritance)
  - Chart selector is a single function with clear inputs/outputs
  - Reuses existing Recharts patterns

### Design Quality Verification

| Gate | Status | Evidence |
|------|--------|----------|
| Data model complete | ✅ | `data-model.md` defines all entities and validation rules |
| Contracts defined | ✅ | `contracts/chart-types.ts` and `contracts/chart_selector.py` |
| Research resolved | ✅ | `research.md` documents all decisions with rationale |
| No NEEDS CLARIFICATION | ✅ | All unknowns resolved through research |
| Quickstart provided | ✅ | `quickstart.md` with test commands |

## Quickstart (quickstart.md)

```bash
# Install dependencies (if not already)
cd src/paged/render/react
npm install

# Run tests
npm test -- --testPathPattern=Chart

# Generate sample slides with charts
python -m cli.uce_render --input sample_data.json --output output/

# View generated MDX
cat output/slides.mdx
```