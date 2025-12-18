"""Slide model for multi-slide layout configurations."""
from typing import Any, Dict, List

from pydantic import Field

from src.common.patchable_context_pydantic import PatchableContextBase


class Slide(PatchableContextBase):
    """Individual slide configuration extending PatchableContextBase.
    
    Each slide has:
    - id, rank, state (from PatchableContextBase)
    - story: Narrative description of slide's purpose and content
    - atoms: List of atom IDs related to this slide
    - density: Information density level ('minimal', 'moderate', 'dense')
    - visual_design: Abstract visual design approach (hierarchical/symmetrical/asymmetrical/split/grid/timeline/full-canvas)
    - layout: Layout name (populated by layout engine, not by LLM)
    - widgets: Widget assignments for this slide
    - style_override: Optional style overrides specific to this slide
    
    Two-phase generation:
    1. Draft state: story + atoms + density + visual_design defined, layout/widgets empty
    2. Active state: layout + widgets populated by layout engine based on visual_design and density
    """
    
    story: str = Field(
        default="",
        description="Narrative description of what this slide conveys and why"
    )
    atoms: List[str] = Field(
        default_factory=list,
        description="List of atom IDs that are relevant to this slide's content"
    )
    density: str = Field(
        default="moderate",
        description="Information density level: 'minimal' (1-2 key points), 'moderate' (3-4 points), 'dense' (5+ points)"
    )
    visual_design: str = Field(
        default="",
        description="Visual design approach: hierarchical/symmetrical/asymmetrical/split/grid/timeline/full-canvas"
    )
    layout: str = Field(
        default="",
        description="Layout name (populated by layout engine based on visual_design)"
    )
    widgets: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Widget assignments mapping slot roles to widget configs"
    )
    header: Dict[str, Any] | None = Field(
        default=None,
        description="Optional header widget (rendered in reserved header area)"
    )
    footer: Dict[str, Any] | None = Field(
        default=None,
        description="Optional footer widget (rendered in reserved footer area)"
    )
    style_override: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional style overrides for this slide"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Strategy-specific parameters (e.g., connector for Solar_System)"
    )
    
    def format_abstract(self) -> str:
        """Format slide as abstract."""
        if self.state == "draft":
            design_info = f" [{self.visual_design}]" if self.visual_design else ""
            return f"Slide #{self.rank} [DRAFT]{design_info}: {self.story[:50]}... ({len(self.atoms)} atoms)"
        return f"Slide #{self.rank} [ACTIVE]: {self.layout} with {len(self.widgets)} widgets"
    
    def format_summary(self) -> str:
        """Format slide summary."""
        lines = [
            f"Slide #{self.rank} [{self.state}]",
            f"ID: {self.id}",
        ]
        if self.story:
            lines.append(f"Story: {self.story}")
        if self.atoms:
            lines.append(f"Atoms: {', '.join(self.atoms)}")
        if self.visual_design:
            lines.append(f"Visual Design: {self.visual_design}")
        if self.layout:
            lines.append(f"Layout: {self.layout}")
        if self.widgets:
            lines.append(f"Widgets: {', '.join(self.widgets.keys())}")
        if self.style_override:
            lines.append(f"Style Overrides: {', '.join(self.style_override.keys())}")
        return "\n".join(lines)
