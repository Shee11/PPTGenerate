"""Slide model for multi-slide layout configurations."""
from typing import Any, Dict, List

from pydantic import Field, field_validator

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
    
    @field_validator('widgets', mode='before')
    @classmethod
    def normalize_widgets(cls, v):
        """Convert various LLM output formats to expected dict format.
        
        Expected: {"slot": {"type": "...", "parameters": {...}}}
        
        LLM may output:
        1. List at top level: [{...}, {...}] → {"slot_0": {...}, ...}
        2. List per slot: {"default": [{...}, {...}]} → {"default": {...}} (first item)
        3. Wrong param name: {"content": "..."} → {"parameters": {"text": "..."}}
        """
        if isinstance(v, list):
            # Case 1: Top-level list
            if len(v) == 1:
                return {"default": cls._normalize_widget(v[0])}
            return {f"slot_{i}": cls._normalize_widget(w) for i, w in enumerate(v)}
        
        if isinstance(v, dict):
            normalized = {}
            for slot, widget in v.items():
                # Skip None values (LLM sometimes outputs null for optional slots)
                if widget is None:
                    continue
                if isinstance(widget, list):
                    # Case 2: List per slot - take first item only
                    if widget:
                        normalized[slot] = cls._normalize_widget(widget[0])
                elif isinstance(widget, dict):
                    normalized[slot] = cls._normalize_widget(widget)
                else:
                    normalized[slot] = widget
            return normalized
        
        return v
    
    @staticmethod
    def _normalize_widget(w: dict) -> dict:
        """Normalize a single widget dict."""
        if not isinstance(w, dict):
            return w
        
        result = dict(w)
        
        # Case 3: Convert "content" to "parameters.text"
        if "content" in result and "parameters" not in result:
            content = result.pop("content")
            if isinstance(content, str):
                result["parameters"] = {"text": content}
            elif isinstance(content, dict):
                # QuoteWidget: {text, author, attribution}
                result["parameters"] = content
            elif isinstance(content, list):
                # List widget: items
                result["parameters"] = {"items": content}
        
        return result
    header: Dict[str, Any] | None = Field(
        default=None,
        description="Optional header widget (rendered in reserved header area)"
    )
    footer: Dict[str, Any] | None = Field(
        default=None,
        description="Optional footer widget (rendered in reserved footer area)"
    )
    theme: str | None = Field(
        default=None,
        description="Theme name/ID for this slide (references entry in themes array)"
    )
    style_override: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional style overrides for this slide"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Strategy-specific parameters (e.g., connector for Solar_System)"
    )
    mdx: str | None = Field(
        default=None,
        description="Raw MDX markup for react-mdx project (bypasses widget-based rendering)"
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
        if self.theme:
            lines.append(f"Theme: {self.theme}")
        if self.widgets:
            lines.append(f"Widgets: {', '.join(self.widgets.keys())}")
        if self.style_override:
            lines.append(f"Style Overrides: {', '.join(self.style_override.keys())}")
        return "\n".join(lines)
