"""Slide model for multi-slide layout configurations."""
from typing import Any, Dict

from pydantic import Field

from src.common.patchable_context_pydantic import PatchableContextBase


class Slide(PatchableContextBase):
    """Individual slide configuration extending PatchableContextBase.
    
    Each slide has:
    - id, rank, state (from PatchableContextBase)
    - strategy: Layout strategy name
    - widgets: Widget assignments for this slide
    - style_override: Optional style overrides specific to this slide
    """
    
    strategy: str = Field(..., description="Layout strategy name (e.g., 'Bento.Standard')")
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
        return f"Slide #{self.rank} [{self.state}]: {self.strategy} with {len(self.widgets)} widgets"
    
    def format_summary(self) -> str:
        """Format slide summary."""
        lines = [
            f"Slide #{self.rank} [{self.state}]",
            f"ID: {self.id}",
            f"Strategy: {self.strategy}",
            f"Widgets: {', '.join(self.widgets.keys())}"
        ]
        if self.style_override:
            lines.append(f"Style Overrides: {', '.join(self.style_override.keys())}")
        return "\n".join(lines)
