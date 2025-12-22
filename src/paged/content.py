"""Content Tool - Generate slide content from atoms.

DirectTool: Delegates to src.generation.content.generator for sophisticated generation.
Uses LLM internally via the generator module with proper prompts and story arc.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List, Dict, Any, ClassVar
from pydantic import Field

from src.common.tool_protocol import DirectTool, ToolContext, ToolPatch, register_tool

if TYPE_CHECKING:
    from src.generation.state import PipelineState


class ContentContext(ToolContext):
    """Context for content generation - holds references, not content."""
    # Use Any to avoid Pydantic forward reference issues
    atoms_collection: Optional[Any] = Field(default=None, description="AtomCollection for generation")
    theme_id: Optional[str] = None
    themes: Optional[List[Dict]] = Field(default=None, description="Available themes")
    intent_guidance: str = Field(default="", description="Guidance from constitution")


class ContentPatch(ToolPatch):
    """Patch containing the Slides collection."""
    slides_collection: Optional[Any] = Field(default=None, description="Generated Slides collection")
    
    class Config:
        arbitrary_types_allowed = True


@register_tool
class ContentTool(DirectTool[ContentContext, ContentPatch]):
    """Generates slide content from atoms using the content generator.
    
    This is a DirectTool that delegates to src.generation.content.generator
    which has sophisticated generation with:
    - Story arc planning
    - Layout selection with variety
    - Widget population with brevity
    - Deck-level coherence
    - Validation and refinement
    """
    
    # Self-description
    name: ClassVar[str] = "content"
    description: ClassVar[str] = "Generate slide content and layout from atoms. Uses sophisticated story-arc generation with layout documentation."
    query_description: ClassVar[str] = "Runs after atoms are extracted. Generates slides based on content and constitution rules."
    args_description: ClassVar[List[str]] = [
        "slide_count (target number of slides)",
        "audience (who the slides are for)",
        "focus_areas (specific topics to emphasize)",
    ]
    requires: ClassVar[List[str]] = ["constitution", "atoms", "theme"]
    produces: ClassVar[List[str]] = ["slides"]
    
    def slice(self, state: "PipelineState") -> ContentContext:
        """Extract context from state."""
        # Build intent guidance from constitution
        intent_guidance = ""
        constitution = state.get_constitution()
        if constitution:
            if hasattr(constitution, 'style_rules') and constitution.style_rules:
                intent_guidance = "\n".join(constitution.style_rules)
        
        # Get available themes (themes in state can be dicts or objects)
        themes = None
        if state.themes:
            themes = []
            for t in state.themes.values():
                if isinstance(t, dict):
                    themes.append({"id": t.get("id", "unknown"), "name": t.get("name", t.get("id", "unknown"))})
                else:
                    themes.append({"id": t.id, "name": getattr(t, 'name', t.id)})
        
        return ContentContext(
            atoms_collection=state.get_atoms(),
            theme_id=state.active_theme_id,
            themes=themes,
            intent_guidance=intent_guidance,
        )
    
    def transform(
        self,
        context: ContentContext,
        user_instruction: str,
    ) -> ContentPatch:
        """Execute content generation via the generator module."""
        from src.generation.content.generator import generate_layout
        from src.generation.content.prompts import get_slide_generation_config
        
        if not context.atoms_collection:
            raise ValueError("No atoms in context")
        
        # Build full guidance
        full_guidance = context.intent_guidance
        if user_instruction:
            if full_guidance:
                full_guidance += f"\n\nUser instruction: {user_instruction}"
            else:
                full_guidance = f"User instruction: {user_instruction}"
        
        atom_count = len(context.atoms_collection.list_contexts())
        self._log(f"Generating slides from {atom_count} atoms")
        if full_guidance:
            self._log(f"With guidance: {full_guidance[:100]}...")
        
        # Get config
        config = get_slide_generation_config()
        
        # Delegate to the sophisticated generator
        slides_collection = generate_layout(
            atoms=context.atoms_collection,
            user_instruction=user_instruction,
            config=config,
            use_cache=self.use_cache,
            intent_guidance=full_guidance,
            layout_engine="slidev",
            themes=context.themes
        )
        
        active_count = len(slides_collection.get_active_slides())
        self._log(f"Generated {active_count} active slides")
        
        return ContentPatch(slides_collection=slides_collection)
    
    def apply(self, state: "PipelineState", patch: ContentPatch) -> None:
        """Apply the slides collection to state."""
        if patch.slides_collection:
            # Convert Slides collection to list of dicts for state
            active_slides = patch.slides_collection.get_active_slides()
            slides_data = [s.model_dump() for s in active_slides]
            state.set_slides(slides_data)
            self._log(f"Applied: {len(slides_data)} slides")
