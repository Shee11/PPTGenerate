"""Constitution Tool - Extract global rules from user instruction.

DirectTool: No LLM needed, uses pattern matching.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List, ClassVar, Optional, Dict, Any
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
    description: ClassVar[str] = """Extract GLOBAL, LONG-LASTING rules from user instruction. No LLM - uses pattern matching.

Constitution is for PERSISTENT rules that should apply across multiple interactions.

GOOD - use constitution for these (persistent rules):
- "use professional tone" → tone rule
- "do not include user biography in slides" → content exclusion  
- "avoid technical jargon" → style rule
- "always include a call to action" → content requirement
- "target 10 slides maximum" → structural constraint
- User says "always", "never", "from now on" → rule change

BAD - do NOT use constitution for these (use content tool instead):
- "split page 3 into multiple pages" → one-time content edit
- "compress to 8 slides" → content tool with slide_count param
- "add more details to slide 2" → content refinement
- "make the intro shorter" → content edit
- Any one-time content changes
- Refinement requests
- Layout or formatting changes

WHEN TO INCLUDE constitution:
1. User explicitly asks to SET or CHANGE a persistent rule
2. User is starting fresh and specifies tone/style preferences
3. User says "always", "never", "from now on" suggesting a rule change

WHEN TO SKIP constitution:
- Refinement requests (merge/split/edit slides)
- One-time slide count changes (pass to content params instead)"""

    query_description: ClassVar[str] = """Triggers on:
- New presentation with tone/style preferences
- Explicit rule setting: "always use...", "never include...", "from now on..."
- Content exclusions: "do not include X in slides"
- Persistent style rules: "use professional tone", "avoid jargon"

Does NOT trigger on:
- Slide manipulation (merge, split, move)
- One-time edits to specific slides
- Refinement requests"""

    args_description: ClassVar[List[str]] = [
        "tone (professional, casual, academic, etc.)",
        "style_rules (list of persistent style guidelines)",
        "content_exclusions (list of content to never include)",
        "content_requirements (list of content that must be included)",
        "target_slides (maximum slide count constraint)",
    ]
    requires: ClassVar[List[str]] = []
    produces: ClassVar[List[str]] = ["constitution"]
    examples: ClassVar[List[str]] = [
        '{"id": "constitution", "type": "constitution", "params": {"tone": "professional", "style_rules": ["use formal language"]}}',
        '{"id": "constitution", "type": "constitution", "params": {"content_exclusions": ["do not include speaker biography"]}}',
    ]
    
    def slice(self, state: "PipelineState", params: Optional[Dict[str, Any]] = None) -> ConstitutionContext:
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
        
        # Audience-aware content rules
        audience = self._detect_audience(instruction_lower)
        if audience:
            style_rules.append(f"Target audience: {audience}")
            if audience in ("executive", "leadership", "c-suite", "board"):
                style_rules.append("Use business-impact quotes, avoid technical jargon")
                style_rules.append("Focus on ROI, risk, and strategic value")
            elif audience in ("technical", "engineering", "developer"):
                style_rules.append("Include technical details and architecture")
                style_rules.append("Use domain-specific terminology")
            elif audience in ("sales", "customer", "client"):
                style_rules.append("Focus on customer pain points and solutions")
                style_rules.append("Use customer success stories and testimonials")
        
        return ConstitutionPatch(
            tone=tone,
            target_slides=target_slides,
            style_rules=style_rules,
        )
    
    def apply(self, state: "PipelineState", patch: ConstitutionPatch) -> None:
        state.set_constitution(patch)
        self._log(f"Applied: {len(patch.style_rules)} rules, tone={patch.tone}")
    
    def _detect_audience(self, instruction: str) -> Optional[str]:
        """Detect target audience from instruction."""
        audience_keywords = {
            "executive": ["executive", "exec", "leadership", "c-suite", "ceo", "cfo", "cto", "cio", "vp", "director", "board"],
            "technical": ["technical", "engineering", "developer", "engineer", "architect", "devops", "sre"],
            "sales": ["sales", "customer", "client", "prospect", "account"],
            "general": ["team", "all-hands", "company", "stakeholder"],
        }
        for audience, keywords in audience_keywords.items():
            for kw in keywords:
                if kw in instruction:
                    return audience
        return None
