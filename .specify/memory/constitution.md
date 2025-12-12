<!--
Sync Impact Report - Version 1.0.0 (Initial Constitution)
==========================================================
Version Change: Template → 1.0.0
Modified Principles: All principles newly defined from template
Added Sections:
  - I. Specification-First Development
  - II. Test-Driven Development (TDD)
  - III. Independent User Stories
  - IV. Agent-Driven Workflow
  - V. Cross-Platform Compatibility
  - VI. No Legacy Code
  - VII. Simplicity and Clarity
  - Development Workflow
  - Quality Gates
Removed Sections: None (initial creation)
Templates Status:
  ✅ .specify/templates/spec-template.md - Aligned with Principle III (Independent User Stories)
  ✅ .specify/templates/plan-template.md - Aligned with Principles I, III, V (Constitution Check section)
  ✅ .specify/templates/tasks-template.md - Aligned with Principles II, III (TDD and Story-based organization)
  ✅ .github/agents/speckit.*.agent.md - All agents support the workflow defined here
Follow-up TODOs: None
==========================================================
-->

# SpecKit Constitution

## Core Principles

### I. Specification-First Development

Every feature begins with a clear, testable specification before any code is written. The specification must:

- Define user scenarios with Given-When-Then acceptance criteria
- Identify functional requirements (FR-001, FR-002, etc.)
- Establish measurable success criteria
- Prioritize user stories independently (P1, P2, P3)
- Be technology-agnostic (no implementation details in spec.md)

**Rationale**: Specifications prevent scope creep, enable clear communication, and serve as executable contracts between stakeholders and developers. User stories MUST be independently testable to enable incremental delivery.

### II. Test-Driven Development (TDD)

TDD is **NON-NEGOTIABLE** for all feature development. The mandatory cycle is:

1. **RED**: Write tests that fail (contract tests, integration tests, unit tests)
2. **Approval**: User/stakeholder reviews and approves tests as acceptance criteria
3. **Verify**: Confirm tests fail for the right reasons
4. **GREEN**: Implement minimum code to make tests pass
5. **REFACTOR**: Improve code while keeping tests green

**Enforcement**:
- Tests MUST be written before implementation begins
- Tests MUST fail initially (proves they test real behavior)
- Implementation tasks may NOT begin until test tasks are complete
- All tests must pass before feature is considered complete

**Rationale**: TDD ensures code correctness, prevents regressions, provides living documentation, and enforces the Red-Green-Refactor discipline that produces maintainable code.

### III. Independent User Stories

User stories MUST be independently implementable and testable. Each story must:

- Deliver standalone value that can be demonstrated in isolation
- Have its own set of tests (contract, integration, unit)
- Be prioritized explicitly (P1 = highest priority, MVP-critical)
- Be implementable without completing other stories
- Have clear acceptance scenarios for independent verification

**Organization**: Tasks are grouped by user story (US1, US2, US3) to enable parallel development and incremental delivery. Each story represents a vertical slice of functionality.

**Rationale**: Independent stories enable true agile delivery, reduce risk, allow early user feedback, and support parallel development across team members.

### IV. Agent-Driven Workflow

Development follows a structured agent workflow with clear handoffs:

1. **specify**: Create feature specification from natural language
2. **plan**: Research and design technical implementation
3. **tasks**: Break plan into executable tasks organized by user story
4. **checklist**: Generate quality gates (UX, testing, security, etc.)
5. **implement**: Execute tasks in phases (Setup → Foundation → User Stories)

**Agent Responsibilities**:
- Each agent has a single, well-defined responsibility
- Agents produce specific artifacts (spec.md, plan.md, tasks.md, etc.)
- Agent handoffs are explicit and documented
- All artifacts use templates from `.specify/templates/`

**Rationale**: Agent-driven workflow ensures consistency, reduces cognitive load, enforces best practices, and makes complex projects manageable through clear separation of concerns.

### V. Cross-Platform Compatibility

All scripts, commands, and tooling MUST work on both Unix-like systems and Windows:

- **PowerShell**: Primary scripting language for cross-platform support
- **Command Chaining**: Use semicolons (`;`) for sequential commands, NEVER `&&`
- **Path Separators**: Use platform-agnostic path handling
- **Scripts**: Maintain parallel implementations in `.specify/scripts/powershell/` and `.specify/scripts/bash/`

**Forbidden Patterns**:
- `command1 && command2` (Windows incompatible)
- Unix-only shell constructs (`$(command)`, backticks)
- Hardcoded forward slashes in paths (use path joining functions)

**Rationale**: Cross-platform compatibility ensures all team members can contribute regardless of their operating system, and prevents "works on my machine" issues.

### VI. No Legacy Code

When refactoring or implementing new features:

- **MUST** remove obsolete code immediately
- **MUST NOT** maintain backward compatibility for internal code
- **MUST** refactor aggressively without preserving old patterns
- **MUST** update all references to changed interfaces

**Breaking Changes Are Expected**: Internal APIs and structures are fluid during active development. Clean, simple code takes precedence over compatibility.

**Rationale**: Legacy code accumulates technical debt, confuses developers, increases maintenance burden, and slows development. Clean breaks enable rapid evolution.

### VII. Simplicity and Clarity

YAGNI (You Aren't Gonna Need It) principles guide all development:

- Build only what the current specification requires
- Prefer simple, direct solutions over clever abstractions
- Document complexity only when it cannot be eliminated
- Each file, function, and module has a single, clear purpose

**Complexity Justification**: Any complexity beyond simple, direct implementation MUST be documented in the plan.md "Complexity Tracking" section with:
- Why the complexity is needed
- What simpler alternatives were rejected and why

**Rationale**: Simple code is easier to understand, test, maintain, and modify. Premature optimization and over-engineering are the enemy of progress.

## Development Workflow

### Feature Development Lifecycle

1. **Specification Phase** (`/speckit.specify`)
   - Input: Natural language feature description
   - Output: `specs/###-feature-name/spec.md`
   - Gate: All user scenarios have acceptance criteria

2. **Planning Phase** (`/speckit.plan`)
   - Input: `spec.md`
   - Output: `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`
   - Gate: Constitution Check passes or violations justified

3. **Task Breakdown** (`/speckit.tasks`)
   - Input: All planning documents
   - Output: `tasks.md` organized by user story
   - Gate: All user stories have test tasks AND implementation tasks

4. **Quality Checklist** (`/speckit.checklist`)
   - Input: `spec.md`, `plan.md`, `tasks.md`
   - Output: `checklists/` (ux.md, test.md, security.md, etc.)
   - Gate: Checklists exist for all relevant domains

5. **Implementation Phase** (`/speckit.implement`)
   - Input: All above documents
   - Output: Working code passing all tests
   - Gate: All checklists 100% complete, all tests green

### Branching and Versioning

- **Feature Branches**: `###-feature-name` (e.g., `001-user-auth`, `002-payment-api`)
- **Numbering**: Sequential, checked against remote, local, and specs directories
- **Specification Storage**: `specs/###-feature-name/` contains all feature documentation

## Quality Gates

### Constitution Check (from plan.md)

Every feature plan MUST pass these gates before implementation begins:

1. **Test-First Discipline**: Test tasks defined before implementation tasks
2. **Independent Stories**: Each user story can be tested in isolation
3. **Complexity Justification**: Any complexity beyond direct implementation is documented
4. **Cross-Platform**: No platform-specific commands (no `&&`, etc.)
5. **Specification Clarity**: No more than 3 `[NEEDS CLARIFICATION]` markers in spec.md

### Implementation Gates

Before code is considered complete:

1. **All Tests Pass**: Red → Green → Refactor cycle completed
2. **Checklists Complete**: All checklist items marked `[X]`
3. **No Legacy Code**: Old code removed, no backward compatibility layers
4. **Documentation Current**: All artifacts reflect actual implementation

## Governance

### Authority and Compliance

- This constitution **supersedes all other practices** and guidelines
- All agents, scripts, and templates MUST conform to these principles
- All PRs and code reviews MUST verify constitution compliance
- Complexity beyond simple, direct solutions MUST be justified in plan.md

### Amendment Process

1. **Documentation**: Proposed change with rationale and impact analysis
2. **Version Bump**: Semantic versioning (MAJOR.MINOR.PATCH)
   - MAJOR: Principle removal or incompatible governance change
   - MINOR: New principle or significant expansion
   - PATCH: Clarification or wording refinement
3. **Migration Plan**: Update all templates, agents, and in-flight features
4. **Ratification**: Update constitution.md with new version and amendment date

### Version Management

- **Version Format**: MAJOR.MINOR.PATCH
- **Ratification Date**: Date constitution first established
- **Last Amended**: Date of most recent change (today if amended)

**Version**: 1.0.0 | **Ratified**: 2025-12-11 | **Last Amended**: 2025-12-11
