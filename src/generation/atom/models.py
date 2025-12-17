"""Atom models for extracted content units."""
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
from src.common.patchable_context_pydantic import PatchableContextBase
from src.common.source import SourceReference


class Atom(PatchableContextBase):
    """
    Base class for all atom types.
    
    Inherits from PatchableContextBase to get id, rank, and state fields.
    All atoms must link back to their source via SourceReference.
    
    Attributes:
        id: Unique identifier (inherited from PatchableContextBase)
        rank: Ordering indicator (inherited from PatchableContextBase)
        state: Current state (inherited from PatchableContextBase)
        source_ref: Link to source location
        created_at: When atom was extracted
        metadata: LLM generation metadata (model, temperature, etc.)
    """
    
    source_ref: SourceReference = Field(..., description="Link to source location")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When atom was extracted"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="LLM generation metadata"
    )


class StatementAtom(Atom):
    """
    Atom representing a pure text statement.
    
    Used for key facts, quotes, or important declarations
    that don't fit process or comparison patterns.
    
    Attributes:
        text: The extracted statement
        related_to: List of atom IDs this relates to
        contradicts: List of atom IDs this contradicts
    """
    
    text: str = Field(..., min_length=1, description="The extracted statement")
    related_to: list[str] = Field(
        default_factory=list,
        description="Atom IDs this statement relates to"
    )
    contradicts: list[str] = Field(
        default_factory=list,
        description="Atom IDs this statement contradicts"
    )


class ProcessStep(BaseModel):
    """
    Single step in a process.
    
    Attributes:
        order: 1-indexed step number
        text: Step description
        dependencies: List of step orders this depends on
    """
    
    order: int = Field(..., gt=0, description="1-indexed step number")
    text: str = Field(..., min_length=1, description="Step description")
    dependencies: list[int] = Field(
        default_factory=list,
        description="Step orders this depends on"
    )


class ProcessAtom(Atom):
    """
    Atom representing a process with sequential steps.
    
    Used for procedures, workflows, or any sequential operations
    where order and dependencies matter.
    
    Attributes:
        title: Process name
        steps: Ordered list of process steps with dependencies
    """
    
    title: str = Field(..., min_length=1, description="Process name")
    steps: list[ProcessStep] = Field(
        ...,
        min_length=1,
        description="Ordered steps with dependencies"
    )


class ComparisonAtom(Atom):
    """
    Atom representing a comparison table.
    
    Used for comparing multiple entities across common dimensions.
    Structure preserves comparison relationships.
    
    Attributes:
        dimensions: List of comparison aspects (e.g., ["cost", "speed"])
        entities: Dict mapping entity name to dimension values
                  e.g., {"Option A": {"cost": "high", "speed": "fast"}}
    """
    
    dimensions: list[str] = Field(
        ...,
        min_length=1,
        description="Comparison aspects"
    )
    entities: dict[str, dict[str, str]] = Field(
        ...,
        description="Entity name -> dimension -> value mapping"
    )


class QuoteAtom(Atom):
    """
    Atom representing a quote from source material.
    
    Used for hard decisions, conclusions, meaningful comments, or
    significant statements from speakers or documents. Preserves
    attribution to maintain credibility.
    
    Attributes:
        quote_text: The exact quoted text
        speaker: Name of person who said it (e.g., "John Smith, CEO")
        source: Document or context where quote appears (e.g., "Q3 Review Meeting", "Strategic Plan.pdf")
        context: Optional surrounding context explaining the quote's significance
    """
    
    quote_text: str = Field(
        ...,
        min_length=1,
        description="The exact quoted text"
    )
    speaker: str = Field(
        ...,
        min_length=1,
        description="Name/title of person who said it (e.g., 'John Smith, CEO')"
    )
    source: str = Field(
        ...,
        min_length=1,
        description="Document or context where quote appears (e.g., 'Q3 Review', 'strategy.pdf')"
    )
    context: str = Field(
        default="",
        description="Optional context explaining significance"
    )


class ActionItem(BaseModel):
    """
    Single action item with assignee and state.
    
    Attributes:
        description: What needs to be done
        assignee: Person/team responsible (empty if unassigned)
        state: Current status (New, Update, Resolved)
        due_date: Optional deadline (ISO format string)
    """
    
    description: str = Field(
        ...,
        min_length=1,
        description="What needs to be done"
    )
    assignee: str = Field(
        default="",
        description="Person/team responsible (empty if unassigned)"
    )
    state: str = Field(
        default="New",
        pattern="^(New|Update|Resolved)$",
        description="Current status: New, Update, or Resolved"
    )
    due_date: str = Field(
        default="",
        description="Optional deadline in ISO format (YYYY-MM-DD)"
    )


class ActionItemAtom(Atom):
    """
    Atom representing a collection of action items.
    
    Used for tracking tasks, decisions that need follow-up, or
    next steps from meetings/documents. Each action item includes
    assignee and state tracking.
    
    Attributes:
        title: Action items category/context (e.g., "Q4 Launch Actions")
        items: List of action items with assignees and states
    """
    
    title: str = Field(
        ...,
        min_length=1,
        description="Action items category/context"
    )
    items: list[ActionItem] = Field(
        ...,
        min_length=1,
        description="List of action items with assignees and states"
    )


class TimelineEvent(BaseModel):
    """
    Single event in a timeline.
    
    Attributes:
        time_marker: Year, date, or time period (e.g., "2011", "Q4 2023", "Early 2020s")
        description: What happened at this point
        details: Optional additional context or specifics
    """
    
    time_marker: str = Field(
        ...,
        min_length=1,
        description="Year, date, or time period (e.g., '2011', 'Q4 2023', 'Early 2020s')"
    )
    description: str = Field(
        ...,
        min_length=1,
        description="What happened at this point"
    )
    details: str = Field(
        default="",
        description="Optional additional context or specifics"
    )


class TimelineAtom(Atom):
    """
    Atom representing a chronological sequence of events.
    
    Used for career journeys, product evolution, historical progression,
    or any narrative with clear temporal markers. Preserves chronological
    order and relationships between events.
    
    Attributes:
        title: Timeline category (e.g., "Career Journey", "Product Evolution")
        events: Ordered list of timeline events with time markers
    """
    
    title: str = Field(
        ...,
        min_length=1,
        description="Timeline category (e.g., 'Career Journey', 'Product Evolution')"
    )
    events: list[TimelineEvent] = Field(
        ...,
        min_length=2,
        description="Ordered list of timeline events (minimum 2 events for a meaningful timeline)"
    )
