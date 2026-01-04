"""Story Tool - Plan narrative arc and assign atoms to slides.

Generates draft slides with:
- story: Narrative description of slide purpose
- atoms: List of atom IDs to use
- density: Information density level
- visual_design: Visual approach (hierarchical, grid, timeline, etc.)

Layout and widgets are empty - filled by ContentTool.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List, Dict, Any, ClassVar
from pydantic import Field

from src.common.tool_protocol import DirectTool, ToolContext, ToolPatch, register_tool

if TYPE_CHECKING:
    from src.generation.state import PipelineState


class StoryContext(ToolContext):
    """Context for story planning - holds atoms and existing slides."""
    atoms_collection: Optional[Any] = Field(default=None, description="AtomCollection for planning")
    source_content: Optional[str] = Field(default=None, description="Source content for direct generation")
    source_path: Optional[str] = Field(default=None, description="Source file path")
    existing_slides: Optional[List[Dict]] = Field(default=None, description="Existing slides for refinement")
    intent_guidance: str = Field(default="", description="Guidance from constitution")
    slide_count_target: Optional[int] = Field(default=None, description="Target slide count")


class StoryPatch(ToolPatch):
    """Patch containing draft slides with story/visual_design."""
    slides: List[Dict[str, Any]] = Field(default_factory=list, description="Draft slides")
    
    class Config:
        arbitrary_types_allowed = True


@register_tool
class StoryTool(DirectTool[StoryContext, StoryPatch]):
    """Plans the narrative arc and assigns atoms to slides.
    
    This is the first content generation step:
    1. Analyzes atoms to understand available content
    2. Plans a story arc across slides
    3. Assigns atoms to each slide
    4. Sets visual_design hints for each slide
    5. Outputs draft slides (layout/widgets empty)
    
    ContentTool depends on this to generate layouts/widgets.
    """
    
    name: ClassVar[str] = "story"
    description: ClassVar[str] = """Plan narrative arc and create draft slides.

OUTPUT: Draft slides with story, density, visual_design populated.
Layout and widgets are EMPTY (filled by content tool).

MODES:
1. mode="generate": Generate story directly from source content using SCQA framework
   - Uses source file directly (no atoms needed)
   - Creates slides with embedded content (headline, subtitle, sections, bullets)
   - Atoms field will be empty in generated slides
   - Runs in parallel with atoms extraction for future refinement capability

2. mode="refine": Modify existing story using atoms (merge/split/reorder slides)
   - Uses extracted atoms to restructure slides
   - Assigns atom IDs to slides
   - Requires atoms to be extracted first

WHEN TO USE GENERATE (no atoms dependency):
- No slides exist yet → create from source
- "regenerate", "start over", "create new"
- "create slides based on the content"
- Initial presentation creation

WHEN TO USE REFINE (requires atoms):
- "merge page 3 and 4"
- "split slide 2 into multiple"
- "remove the intro"
- "add a conclusion slide"
- "reorder slides"
- Any slide-level editing of existing presentation"""

    query_description: ClassVar[str] = """Triggers on:
- Initial presentation creation: generate mode, directly from source
- Story refinement: refine mode, uses atoms to restructure slides
- Changing narrative flow or slide count"""

    args_description: ClassVar[List[str]] = [
        "mode: 'generate' (from source, no atoms) or 'refine' (uses atoms)",
        "instruction: user's request",
        "slide_count: target number of slides (for generate mode)",
        "atom_filter: filter criteria to select specific atoms (for refine mode)",
    ]
    requires: ClassVar[List[str]] = ["constitution (generate mode), atoms (refine mode only)"]
    produces: ClassVar[List[str]] = ["slides (draft state)"]
    examples: ClassVar[List[str]] = [
        '{"id": "story", "type": "story", "params": {"slide_count": 10, "mode": "generate"}, "depends_on": ["constitution"]}',
        '{"id": "story", "type": "story", "params": {"mode": "refine", "instruction": "merge page 3 and page 4"}, "depends_on": ["atoms"]}',
        '{"id": "story", "type": "story", "params": {"mode": "refine", "instruction": "add a conclusion slide"}, "depends_on": ["atoms"]}',
    ]
    
    def slice(self, state: "PipelineState", params: Optional[Dict[str, Any]] = None) -> StoryContext:
        """Extract context from state for story planning."""
        params = params or {}
        
        # Build intent guidance from constitution
        intent_guidance = ""
        constitution = state.get_constitution()
        if constitution:
            if hasattr(constitution, 'style_rules') and constitution.style_rules:
                intent_guidance = "\n".join(constitution.style_rules)
            if hasattr(constitution, 'content_exclusions') and constitution.content_exclusions:
                exclusions = "\n".join([f"- {e}" for e in constitution.content_exclusions])
                intent_guidance += f"\n\nContent to EXCLUDE:\n{exclusions}"
            if hasattr(constitution, 'content_requirements') and constitution.content_requirements:
                requirements = "\n".join([f"- {r}" for r in constitution.content_requirements])
                intent_guidance += f"\n\nContent REQUIRED:\n{requirements}"
        
        # Get slide count target
        slide_count_target = params.get("slide_count")
        if not slide_count_target and constitution:
            slide_count_target = getattr(constitution, 'slide_count_target', None)
        
        # Get existing slides for refinement
        existing_slides = None
        mode = params.get("mode", "generate")
        if mode == "refine" and state.slides:
            existing_slides = state.slides
        
        # Generate mode: use source content directly
        # Refine mode: use atoms
        source_content = None
        source_path = None
        atoms_collection = None
        
        if mode == "generate" and not existing_slides:
            # Direct generation from source
            if state.source:
                from pathlib import Path
                source_path_obj = Path(state.source.path)
                source_content = source_path_obj.read_text(encoding='utf-8')
                source_path = str(source_path_obj.absolute())
        else:
            # Refinement mode: use atoms
            atoms_collection = state.get_atoms()
            atom_filter = params.get("atom_filter")
            if atom_filter and atoms_collection:
                from src.generation.todo.models import AtomFilter
                if isinstance(atom_filter, dict):
                    atom_filter = AtomFilter(**atom_filter)
                
                all_atoms = atoms_collection.list_contexts()
                atom_dicts = [a.model_dump() if hasattr(a, 'model_dump') else a for a in all_atoms]
                filtered_atoms = atom_filter.apply(atom_dicts)
                
                filter_info = f"\n\nAtom filtering: {len(filtered_atoms)}/{len(atom_dicts)} atoms selected"
                intent_guidance += filter_info
        
        return StoryContext(
            atoms_collection=atoms_collection,
            source_content=source_content,
            source_path=source_path,
            existing_slides=existing_slides,
            intent_guidance=intent_guidance,
            slide_count_target=slide_count_target,
        )
    
    def transform(self, context: StoryContext, user_instruction: str) -> StoryPatch:
        """Execute story planning via LLM."""
        from src.generation.content.story_generator import generate_story, generate_story_from_source, refine_story
        
        # Build full guidance
        full_guidance = context.intent_guidance
        if user_instruction:
            if full_guidance:
                full_guidance += f"\n\nUser instruction: {user_instruction}"
            else:
                full_guidance = f"User instruction: {user_instruction}"
        
        if context.existing_slides:
            # Refinement mode - use atoms
            if not context.atoms_collection:
                raise ValueError("No atoms in context for story refinement")
            
            self._log(f"Refining story for {len(context.existing_slides)} existing slides")
            draft_slides = refine_story(
                existing_slides=context.existing_slides,
                atoms=context.atoms_collection,
                user_instruction=user_instruction,
                intent_guidance=full_guidance,
            )
        elif context.source_content:
            # Generate mode - direct from source
            self._log(f"Generating story from source ({len(context.source_content)} chars)")
            draft_slides = generate_story_from_source(
                source_content=context.source_content,
                user_instruction=user_instruction,
                slide_count=context.slide_count_target,
                intent_guidance=full_guidance,
            )
        elif context.atoms_collection:
            # Fallback: atoms-based generation
            atom_count = len(context.atoms_collection.list_contexts())
            self._log(f"Planning story from {atom_count} atoms")
            draft_slides = generate_story(
                atoms=context.atoms_collection,
                user_instruction=user_instruction,
                slide_count=context.slide_count_target,
                intent_guidance=full_guidance,
            )
        else:
            raise ValueError("No source content or atoms in context for story planning")
        
        self._log(f"Planned {len(draft_slides)} draft slides")
        return StoryPatch(slides=draft_slides)
    
    def apply(self, state: "PipelineState", patch: StoryPatch) -> None:
        """Apply draft slides to state (replaces existing slides)."""
        if patch.slides:
            # Post-processing: Fix consecutive same-layout issues
            from src.paged.layout.slidev.validate_slides import fix_consecutive_layouts
            fixed_slides, fix_report = fix_consecutive_layouts(patch.slides, verbose=True)
            fixes_applied = sum(1 for line in fix_report if "→" in line)
            if fixes_applied > 0:
                self._log(f"🔧 Fixed {fixes_applied} consecutive layout issue(s)")
            
            state.set_slides(fixed_slides)
            self._log(f"Applied: {len(patch.slides)} draft slides")
