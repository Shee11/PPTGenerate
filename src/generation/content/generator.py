"""Layout generation from atoms using LLM with unified single-step process.

This module generates complete presentations in a single LLM call, including:
- Narrative structure (story arc)
- Layout selection (visual variety)
- Widget population (content brevity)
- Deck-level coherence (widget distribution)
"""
import json
import hashlib
from typing import Any, List

from src.generation.atom.collection import AtomCollection
from src.generation.content.prompts import (
    render_slide_generation_prompt,
    render_refinement_prompt,
    get_slide_generation_config,
)
from src.common.slides import Slides
from src.common.patchable_context_pydantic import Patch
from src.utils.generation_config import GenerationConfig
from src.utils.llm_client import call_llm
from src.utils.cache import GenerationCache
from src.paged.layout.dummy.validation import LayoutValidator, LayoutIssue, format_issues_for_llm
from src.common.renderable_layout import RenderableLayout


# Module-level cache instance
_cache = GenerationCache()


def generate_layout(
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    use_cache: bool = True,
    intent_guidance: str = "",
    layout_engine: str = "slidev",
    themes: List = None
) -> Slides:
    """
    Generate presentation layout from atoms using LLM (single-step process).
    
    Creates a complete presentation in one LLM call with:
    - Narrative arc and story structure
    - Layout selection with deck-level variety
    - Widget population with content brevity
    - Deck-level coherence (widget distribution)
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions (e.g., "Create 5 slides")
        config: Generation configuration (model, temperature, prompts)
        use_cache: Whether to use cached results if available
        intent_guidance: Optional guidance from intent detection
        layout_engine: Layout engine to use ('dummy' or 'slidev', default: 'slidev')
        themes: List of available theme dicts (with 'id' field) for theme assignment
        
    Returns:
        Slides collection with active slides and content
        
    Raises:
        ValueError: If atoms is empty or instruction invalid
        json.JSONDecodeError: If LLM output is not valid JSON
        Exception: If LLM API call fails after retries
    """
    # Validate inputs
    if len(atoms) == 0:
        raise ValueError("Cannot generate layout from empty atom collection")
    
    if not user_instruction or not user_instruction.strip():
        raise ValueError("User instruction cannot be empty")
    
    # Check cache (include intent_guidance in cache key if provided)
    if use_cache:
        cache_key = _compute_cache_key(atoms, user_instruction, config, intent_guidance, layout_engine)
        cached_result = _cache.load(cache_key)
        if cached_result:
            # Reconstruct Slides from cached patch data
            cached_slides = Slides()
            cached_patch = Patch.from_json_str(cached_result["cached_data"])
            cached_slides.patch(cached_patch)
            print(f"✓ Using cached slide generation ({cached_result['metadata']['slide_count']} slides)")
            return cached_slides
    
    # Initialize empty slides collection
    slides = Slides(id="slides")
    
    print(f"⚙ Generating complete presentation via LLM...")
    
    # Map layout_engine to project type for prompt selection
    project = "react-mdx" if layout_engine in ("react", "react-mdx") else "slidev"
    
    # Single-step generation: create complete slides with layout + widgets
    patch_ops = _generate_slides(atoms, user_instruction, config, intent_guidance, themes, project=project)
    
    # Ensure it's a list (LLM might return single operation as dict)
    if isinstance(patch_ops, dict):
        patch_ops = [patch_ops]
    
    # Convert list of dicts to Patch object and apply
    patch = Patch.from_json_str(json.dumps(patch_ops))
    slides.patch(patch)
    
    # Save content for debugging
    from pathlib import Path
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    content_path = output_dir / "debug_content.json"
    content_path.write_text(slides.to_json(), encoding='utf-8')
    
    active_count = len(slides.get_active_slides())
    print(f"✓ Generated {active_count} active slides")
    
    # Cache result
    if use_cache:
        _cache.save(
            cache_key,
            {
                "cached_data": json.dumps(patch_ops),  # Store as JSON string
                "metadata": {
                    "atom_count": len(atoms),
                    "slide_count": len(slides),
                    "instruction": user_instruction,
                    "intent_guidance": intent_guidance
                }
            }
        )
    
    return slides


def refine_slides(
    existing_slides: List[dict],
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    intent_guidance: str = "",
    themes: List = None
) -> Slides:
    """
    Refine existing slides based on user instruction using Patch format.
    
    Instead of regenerating all slides from scratch, this function:
    1. Analyzes what needs to change based on instruction
    2. Generates <Patch> elements targeting specific widget IDs
    3. Applies patches to modify MDX content in-place
    
    This is more efficient for instructions like:
    - "update the revenue stat" → patches one BigNum element
    - "change the chart data" → patches one Chart element
    - "make titles shorter" → patches Heading elements
    
    Args:
        existing_slides: Current slides as list of dicts (with mdx field)
        atoms: AtomCollection for reference
        user_instruction: User's refinement instruction
        config: Generation configuration
        intent_guidance: Constitution guidance (exclusions, requirements, etc.)
        themes: List of available theme dicts
        
    Returns:
        Refined Slides collection with patches applied
    """
    from src.paged.layout.react.mdx_parser import parse_patches, apply_patches
    from src.generation.content.prompts import render_slide_refinement_prompt
    
    print(f"⚙ Refining {len(existing_slides)} slides based on instruction...")
    
    # Generate refinement prompt with current MDX
    refinement_prompt = render_slide_refinement_prompt(
        existing_slides=existing_slides,
        atoms=atoms,
        user_instruction=user_instruction,
        intent_guidance=intent_guidance,
        themes=themes
    )
    
    # Call LLM for patch generation
    response = call_llm(
        system_prompt=_get_refinement_system_prompt(),
        user_prompt=refinement_prompt,
        deployment=config.model,
        temperature=0.3,  # Lower temperature for more precise edits
        max_tokens=config.max_tokens,
    )
    
    # Parse <Patch> elements from response
    patches = parse_patches(response)
    
    if patches:
        # Apply patches to slide MDX content
        updated_slides = apply_patches(existing_slides, patches)
        print(f"✓ Applied {len(patches)} patch operations")
    else:
        updated_slides = existing_slides
        print("✓ No patches needed")
    
    # Convert to Slides collection
    slides = Slides(id="slides")
    for slide_data in updated_slides:
        add_op = {"add": slide_data}
        patch = Patch.from_json_str(json.dumps([add_op]))
        slides.patch(patch)
    
    return slides


def _get_refinement_system_prompt() -> str:
    """Get system prompt for slide refinement using Patch format."""
    return """You are a presentation refinement assistant. Make targeted changes to MDX slides using <Patch> elements.

OUTPUT FORMAT:
Output <Patch> elements that target specific widget IDs:

```mdx
<Patch id="stat_001">
  <BigNum value="95%" label="Updated Stat" trend="+10%"/>
</Patch>

<Patch id="list_001">
  <SmartList items={["New item 1", "New item 2", "New item 3"]}/>
</Patch>
```

RULES:
1. Each <Patch> targets an element by its id attribute
2. The patch content replaces the entire original element
3. Only output patches for elements that need to change
4. If no changes needed, output nothing

IMPORTANT:
- Match the original element's component type unless changing it intentionally
- Preserve element IDs in the replacement content
- Keep the same structure/props unless the change requires modification"""


def _generate_slides(
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    intent_guidance: str = "",
    themes: List = None,
    project: str = "slidev"
) -> Any:
    """
    Generate complete slides in a single LLM call.
    
    Creates slides with:
    - Story field describing narrative purpose
    - Layout selection for visual variety
    - MDX content (react-mdx) or widget definitions (slidev)
    - State set to 'active'
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions
        config: Generation configuration
        intent_guidance: Optional guidance from intent detection
        themes: List of available theme dicts (with 'id' field)
        project: Project type for prompts ('react-mdx')
        
    Returns:
        List of patch operations to create complete slides
        
    Raises:
        ValueError: If MDX parsing fails
        Exception: If LLM API call fails
    """
    from src.paged.layout.react.mdx_parser import parse_slides_from_mdx
    
    # Get configuration for slide generation with correct project type
    slide_config = get_slide_generation_config(project=project)
    
    # Render prompts
    system_prompt = slide_config.system_prompt
    user_prompt = render_slide_generation_prompt(atoms, user_instruction, intent_guidance, themes)
    
    # Call LLM
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        deployment=config.model,
        temperature=slide_config.temperature,
        max_tokens=slide_config.max_tokens,
        max_reasoning_tokens=slide_config.max_reasoning_tokens
    )
    
    # Parse MDX output
    parsed_slides = parse_slides_from_mdx(response)
    
    if not parsed_slides:
        print(f"  ⚠ No slides parsed from MDX response")
        print(f"    Response (first 500 chars): {response[:500]}")
        return []
    
    # Convert ParsedSlide objects to patch operations
    patch_operations = []
    for slide in parsed_slides:
        patch_operations.append({
            "add": {
                "id": slide.id,
                "rank": slide.rank,
                "state": "active",
                "story": slide.story,
                "atoms": slide.atoms,
                "mdx": slide.mdx,
            }
        })
    
    return patch_operations


def _compute_cache_key(
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    intent_guidance: str = "",
    layout_engine: str = "dummy"
) -> str:
    """
    Compute cache key for layout generation.
    
    Includes active layout engine name to automatically invalidate cache
    when switching between different layout engines.
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions
        config: Generation configuration
        intent_guidance: Optional guidance from intent detection
        layout_engine: Name of the layout engine being used
        
    Returns:
        str: SHA256 hash of inputs including active layout engine
    """
    # Use the passed layout_engine parameter for cache key
    # (No need to query registry - engine was already selected by caller)
    active_engine_name = layout_engine
    
    # Create deterministic string from inputs
    # Use atoms.to_json() for datetime serialization, then parse back for sorting
    atoms_data = json.loads(atoms.to_json())
    cache_input = json.dumps({
        "atoms": atoms_data,
        "instruction": user_instruction,
        "model": config.model,
        "temperature": config.temperature,
        "intent_guidance": intent_guidance,
        "layout_engine": active_engine_name  # Include engine in cache key
    }, sort_keys=True)
    
    # Compute SHA256 hash
    return hashlib.sha256(cache_input.encode()).hexdigest()


def refine_layout_with_validation(
    slides: Slides,
    rendered_layouts: List[RenderableLayout],
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    intent_guidance: str = "",
    maxiter: int = 3
) -> Slides:
    """
    Refine layout by validating rendered slides and correcting issues.
    
    Iteratively validates rendered layouts, detects issues (color contrast,
    overlap, density, style consistency), and sends feedback to LLM for
    correction via refinement patches.
    
    Args:
        slides: Current Slides collection
        rendered_layouts: List of RenderableLayout objects (one per active slide)
        atoms: Original AtomCollection
        user_instruction: User's generation instructions
        config: Generation configuration
        intent_guidance: Optional guidance from intent detection
        maxiter: Maximum refinement iterations (default: 3)
        
    Returns:
        Refined Slides collection
        
    Raises:
        json.JSONDecodeError: If LLM refinement patch is invalid JSON
        Exception: If LLM API call fails
    """
    iteration = 0
    current_slides = slides
    current_layouts = rendered_layouts
    
    while iteration < maxiter:
        iteration += 1
        
        # Validate all rendered layouts
        all_issues: List[LayoutIssue] = []
        for i, layout in enumerate(current_layouts):
            issues = LayoutValidator.validate(layout)
            if issues:
                # Tag issues with slide index for tracking
                for issue in issues:
                    issue.message = f"[Slide {i+1}] {issue.message}"
                all_issues.extend(issues)
        
        # If no issues found, refinement complete
        if not all_issues:
            print(f"✓ Validation passed on iteration {iteration}")
            break
        
        # Format issues as LLM feedback
        feedback = format_issues_for_llm(all_issues)
        print(f"⚠ Found {len(all_issues)} validation issue(s) - refining (iteration {iteration}/{maxiter})...")
        
        # Generate refinement patch
        refinement_patch_ops = _generate_refinement(
            current_slides,
            atoms,
            user_instruction,
            config,
            intent_guidance,
            feedback
        )
        
        # Ensure it's a list
        if isinstance(refinement_patch_ops, dict):
            refinement_patch_ops = [refinement_patch_ops]
        
        # Apply refinement patch
        refinement_patch = Patch.from_json_str(json.dumps(refinement_patch_ops))
        current_slides.patch(refinement_patch)
        
        # Re-render layouts for next validation
        # Note: This requires re-rendering, which happens in orchestrator
        # For now, we return refined slides and let orchestrator re-render
        break  # Exit after one refinement - orchestrator will call again if needed
    
    if iteration >= maxiter and all_issues:
        print(f"⚠ Max iterations ({maxiter}) reached with {len(all_issues)} remaining issue(s)")
    
    return current_slides


def _generate_refinement(
    current_slides: Slides,
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    intent_guidance: str,
    validation_feedback: str
) -> Any:
    """
    Generate refinement patch based on validation feedback.
    
    Args:
        current_slides: Current Slides collection with issues
        atoms: Original AtomCollection
        user_instruction: User's generation instructions
        config: Generation configuration
        intent_guidance: Guidance from intent detection
        validation_feedback: Formatted validation issues
        
    Returns:
        Patch operations to fix issues
        
    Raises:
        json.JSONDecodeError: If LLM output is invalid JSON
        Exception: If LLM API call fails
    """
    # Use slide generation config for refinement (works with active slides)
    content_config = get_slide_generation_config()
    
    # Build refinement prompt (works with active slides, not draft)
    system_prompt = content_config.system_prompt + "\n\n**REFINEMENT MODE**: You are correcting validation issues in an existing layout. Generate 'replace' operations to fix the specific issues mentioned in the feedback."
    
    # Use refinement-specific prompt that accepts active slides
    user_prompt = render_refinement_prompt(
        active_slides=current_slides,
        atoms=atoms,
        user_instruction=user_instruction,
        validation_feedback=validation_feedback,
        intent_guidance=intent_guidance
    )
    
    # Call LLM
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        deployment=config.model,
        temperature=content_config.temperature,
        max_tokens=content_config.max_tokens,
        max_reasoning_tokens=content_config.max_reasoning_tokens
    )
    
    # Parse JSON Patch
    patch_operations = json.loads(response)
    
    return patch_operations


def refine_layout(
    existing_slides: Slides,
    atoms: AtomCollection,
    refinement_instruction: str,
    config: GenerationConfig,
    use_cache: bool = True,
    intent_guidance: str = ""
) -> Slides:
    """
    Incrementally refine existing slides based on user's refinement instruction.
    
    Uses LLM to generate patches that modify existing slides rather than 
    regenerating from scratch. This is faster and preserves slide structure
    while applying targeted changes.
    
    Args:
        existing_slides: Current Slides collection to refine
        atoms: AtomCollection with extracted content
        refinement_instruction: User's refinement request (e.g., "Make it more technical")
        config: Generation configuration
        use_cache: Whether to use cached results if available
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        Refined Slides collection with patches applied
        
    Raises:
        ValueError: If slides or instruction is empty
        json.JSONDecodeError: If LLM output is not valid JSON
    """
    # Validate inputs
    if len(existing_slides) == 0:
        raise ValueError("Cannot refine empty slide collection")
    
    if not refinement_instruction or not refinement_instruction.strip():
        raise ValueError("Refinement instruction cannot be empty")
    
    # Build refinement prompt
    from src.generation.content.prompts import render_user_refinement_prompt, get_slide_generation_config
    
    user_prompt = render_user_refinement_prompt(
        existing_slides=existing_slides,
        atoms=atoms,
        refinement_instruction=refinement_instruction,
        intent_guidance=intent_guidance
    )
    
    system_prompt = """You are an expert presentation designer. You refine existing presentations based on user feedback.

Given:
1. Current slide collection (with widgets, layouts, styling)
2. Available content atoms
3. User's refinement instruction

Generate a JSON Patch with operations to refine the slides:
- Use 'replace' to modify existing slides (change content, layout, styling)
- Use 'add' to insert new slides if needed
- Use 'remove' to delete slides if needed

Focus on incremental changes that address the user's refinement instruction.
Preserve existing structure where possible - only modify what's needed.

Output ONLY a valid JSON array of patch operations. No markdown, no explanations."""
    
    content_config = get_slide_generation_config()
    
    # Call LLM
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        deployment=config.model,
        temperature=content_config.temperature,
        max_tokens=content_config.max_tokens,
        max_reasoning_tokens=content_config.max_reasoning_tokens
    )
    
    # Parse and apply patches
    response_data = json.loads(response)
    
    # Handle both formats: {"operations": [...]} or just [...]
    if isinstance(response_data, dict) and "operations" in response_data:
        patch_operations = response_data["operations"]
    elif isinstance(response_data, list):
        patch_operations = response_data
    else:
        raise ValueError(f"Unexpected response format: {type(response_data)}")
    
    patch = Patch(operations=patch_operations)
    
    # Apply patches to existing slides
    existing_slides.patch(patch)
    
    print(f"✓ Applied {len(patch_operations)} refinement operation(s)")
    
    return existing_slides
