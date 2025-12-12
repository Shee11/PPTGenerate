# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The following principles from `.specify/memory/constitution.md` must be verified:

- [ ] **Specification-First**: Feature has complete spec.md with user scenarios, functional requirements, and success criteria
- [ ] **Test-Driven Development**: Plan includes test strategy; tests will be written before implementation
- [ ] **Independent User Stories**: Each user story (P1, P2, P3) can be implemented and tested independently
- [ ] **Agent-Driven Workflow**: Following proper workflow: specify → plan → tasks → checklist → implement
- [ ] **Cross-Platform Compatibility**: No `&&` operators, no Unix-only commands, PowerShell-compatible scripts
- [ ] **No Legacy Code**: Plan does not include backward compatibility requirements for internal code
- [ ] **Simplicity and Clarity**: Architecture is as simple as possible; any complexity is justified below

### Complexity Justification

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Multiple services] | [specific technical requirement] | [why single service insufficient] |
| [e.g., Custom framework] | [specific problem it solves] | [why standard framework insufficient] |

## Project Structure
