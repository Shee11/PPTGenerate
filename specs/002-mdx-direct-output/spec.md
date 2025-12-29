# Feature Specification: MDX Direct Output

**Feature Branch**: `002-mdx-direct-output`  
**Created**: 2024-12-27  
**Status**: Draft  
**Input**: User description: "Refactor LLM content generation to output MDX/JSX directly instead of JSON, storing MDX in state.json, using Patch format for incremental updates"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate New Slides as MDX (Priority: P1)

As a presentation creator, I want the LLM to generate slide content directly as MDX markup so that rendering is immediate without JSON-to-MDX conversion.

**Why this priority**: This is the core value proposition - eliminating the conversion step simplifies the pipeline and allows LLMs to leverage their natural understanding of JSX/HTML-like syntax.

**Independent Test**: Run content generation with `project=react-mdx`, verify output is valid MDX that renders directly without transformation.

**Acceptance Scenarios**:

1. **Given** atoms and user instructions, **When** LLM generates slides, **Then** output contains MDX markup (JSX components) instead of JSON widget definitions
2. **Given** a generated slide, **When** saved to state.json, **Then** the `mdx` field contains the raw MDX string
3. **Given** MDX in state.json, **When** renderer loads it, **Then** it renders directly without JSON-to-MDX conversion

---

### User Story 2 - Incremental Patch Updates (Priority: P2)

As a user refining my presentation, I want to make targeted edits using Patch format so that only changed content is regenerated, preserving the rest.

**Why this priority**: Incremental refinement is essential for iterative editing - full regeneration is expensive and loses user customizations.

**Independent Test**: Request a change to one widget, verify only that widget's MDX is updated while others remain unchanged.

**Acceptance Scenarios**:

1. **Given** existing slides with MDX content, **When** user requests a refinement, **Then** LLM outputs `<Patch id="widget_id">...</Patch>` format
2. **Given** a Patch output, **When** applied to state.json, **Then** only the targeted widget's content is updated
3. **Given** multiple patches in one response, **When** applied, **Then** each patch updates its corresponding widget independently

---

### User Story 3 - Backward Compatibility with JSON Mode (Priority: P3)

As a developer using the Slidev engine, I want the existing JSON output to continue working so that migration to MDX is optional.

**Why this priority**: Allows incremental adoption - teams can migrate when ready without breaking existing workflows.

**Independent Test**: Run content generation with `project=slidev`, verify JSON output format is unchanged.

**Acceptance Scenarios**:

1. **Given** project type is `slidev`, **When** LLM generates content, **Then** output is JSON format (unchanged behavior)
2. **Given** project type is `react-mdx`, **When** LLM generates content, **Then** output is MDX format

---

### Edge Cases

- What happens when MDX contains syntax errors? Validation should catch malformed JSX before saving.
- How does system handle patches targeting non-existent widget IDs? Should warn and skip.
- What if user switches project type mid-session? State format should be consistent per project.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST generate MDX/JSX markup directly when project type is `react-mdx`
- **FR-002**: System MUST store slide content in a `mdx` field in state.json (string containing MDX markup)
- **FR-003**: System MUST use Patch format for refinement operations: `<Patch id="widget_id">...updated content...</Patch>`
- **FR-004**: System MUST preserve existing JSON output format when project type is `slidev`
- **FR-005**: Renderer MUST read MDX directly from state.json without JSON-to-MDX conversion
- **FR-006**: System MUST validate MDX syntax before saving to state
- **FR-007**: Patch operations MUST only update the targeted widget, preserving all other content

### Key Entities

- **Slide State**: Represents a single slide with metadata and content
  - `id`: Unique slide identifier
  - `rank`: Display order
  - `story`: Story arc position (HOOK, TENSION, etc.)
  - `atoms`: Referenced atom IDs
  - `mdx`: Raw MDX markup string (new field, replaces widgets for react-mdx)

- **Patch Operation**: Represents an incremental update
  - `id`: Target widget/element identifier
  - `content`: New MDX content for that element

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Content generation pipeline eliminates JSON-to-MDX conversion step for react-mdx projects
- **SC-002**: State.json correctly stores and retrieves MDX content without data loss
- **SC-003**: Patch-based refinements update only targeted content (diff shows minimal changes)
- **SC-004**: Existing slidev/JSON workflows continue functioning without modification
- **SC-005**: LLM prompt size reduced by removing JSON schema definitions when using MDX output

## Assumptions

- LLMs (GPT-4, Claude) have strong understanding of JSX/MDX syntax from training data
- MDX markup is more natural for LLMs to generate than nested JSON structures
- React MDX renderer can parse MDX strings directly without intermediate transformation
- Widget IDs in MDX can be expressed as element attributes (e.g., `<BigNum id="stat_001" .../>`)
