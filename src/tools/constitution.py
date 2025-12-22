"""Constitution Tool - Extract global rules from user instruction.

DirectTool: No LLM needed, uses pattern matching.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List, ClassVar
from pydantic import Field

from src.common.tool_protocol import DirectTool, ToolContext, register_tool
from src.generation.todo.models import ConstitutionPatch
from src.generation.todo.planner import (
    parse_intent, IntentAction, ToneStyle
)

if TYPE_CHECKING:
    from src.generation.state import PipelineState


class ConstitutionContext(ToolContext):
    """Context for constitution - empty, derived from instruction only."""
    pass


@register_tool
class ConstitutionTool(DirectTool[ConstitutionContext, ConstitutionPatch]):
    """Derives constitution from user instruction (NO LLM)."""
    
    # Self-description
    name: ClassVar[str] = "constitution"
    description: ClassVar[str] = "Extract global rules and constraints from user instruction. No LLM - uses pattern matching."
    query_description: ClassVar[str] = "Always runs first. Triggered by any instruction to extract tone, slide count, style rules."
    args_description: ClassVar[List[str]] = [
        "tone (professional, casual, academic, etc.)",
        "slide_count (number of slides)",
        "density (sparse, normal, dense)",
        "style keywords (minimalist, bold, clean, etc.)",
    ]
    requires: ClassVar[List[str]] = []
    produces: ClassVar[List[str]] = ["constitution"]
    
    def slice(self, state: "PipelineState") -> ConstitutionContext:
        return ConstitutionContext()
    
    def transform(
        self,
        context: ConstitutionContext,
        user_instruction: str,
    ) -> ConstitutionPatch:
        """Extract constitution from instruction via pattern matching."""
        # Use planner's built-in intent parser (no LLM)
        intent = parse_intent(user_instruction)
        instruction_lower = user_instruction.lower()
        
        # Extract tone directly from enum value
        tone = intent.tone_style.value if intent.tone_style else None
        
        # Extract slide count
        target_slides = intent.slide_count
        
        # Build style rules
        style_rules = []
        
        if intent.action == IntentAction.CREATE:
            style_rules.append("Start with a title slide")
        
        if intent.density:
            density_map = {
                "sparse": "Use minimal content per slide, prefer larger fonts",
                "normal": "Balance content density",
                "dense": "Pack more content per slide, use smaller fonts"
            }
            if intent.density in density_map:
                style_rules.append(density_map[intent.density])
        
        # Parse keywords
        if "no animation" in instruction_lower:
            style_rules.append("No animations")
        if "minimalist" in instruction_lower or "clean" in instruction_lower:
            style_rules.append("Minimalist design, plenty of whitespace")
        if "bold" in instruction_lower or "impactful" in instruction_lower:
            style_rules.append("Use bold typography for impact")
        if "data" in instruction_lower or "chart" in instruction_lower:
            style_rules.append("Include data visualizations where appropriate")
        
        return ConstitutionPatch(
            tone=tone,
            target_slides=target_slides,
            style_rules=style_rules,
        )
    
    def apply(self, state: "PipelineState", patch: ConstitutionPatch) -> None:
        state.set_constitution(patch)
        self._log(f"Applied: {len(patch.style_rules)} rules, tone={patch.tone}")
