"""Layout generation from atoms using LLM with three-step process."""
import json
import hashlib
from typing import Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.generation.atom.collection import AtomCollection
from src.generation.content.prompts import (
    render_storyline_prompt,
    render_slide_generation_prompt,
    render_refinement_prompt,
    get_storyline_config,
    get_slide_generation_config,
)
from src.common.slides import Slides
from src.common.patchable_context_pydantic import Patch
from src.utils.generation_config import GenerationConfig
from src.utils.llm_client import call_llm
from src.utils.cache import GenerationCache
from src.layout.validation import LayoutValidator, LayoutIssue, format_issues_for_llm
from src.common.renderable_layout import RenderableLayout


# Module-level cache instance
_cache = GenerationCache()


def generate_layout(
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    use_cache: bool = True,
    intent_guidance: str = ""
) -> Slides:
    """
    Generate presentation layout from atoms using LLM (three-step process).
    
    Step 1: Generate storyline patch (create draft slides with story + atom references)
    Step 2: Batch generate individual slides in parallel (draft → active with layout + widgets)
    Step 3: Update internal state after parallel generation
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions (e.g., "Create 5 slides")
        config: Generation configuration (model, temperature, prompts)
        use_cache: Whether to use cached results if available
        intent_guidance: Optional guidance from intent detection
        
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
        cache_key = _compute_cache_key(atoms, user_instruction, config, intent_guidance)
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
    
    print(f"⚙ Generating slide storyline via LLM...")
    
    # Step 1: Storyline generation (create draft slides with story + atoms)
    storyline_patch_ops = _generate_storyline(atoms, user_instruction, config, intent_guidance)
    # Ensure it's a list (LLM might return single operation as dict)
    if isinstance(storyline_patch_ops, dict):
        storyline_patch_ops = [storyline_patch_ops]
    # Convert list of dicts to Patch object
    storyline_patch = Patch.from_json_str(json.dumps(storyline_patch_ops))
    slides.patch(storyline_patch)
    
    # Get draft slides
    draft_slides = [s for s in slides.list_contexts() if s.state == "draft"]
    print(f"✓ Storyline created: {len(draft_slides)} draft slides")
    
    # Save Phase 1 state for debugging
    from pathlib import Path
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    phase1_path = output_dir / "debug_phase1_storyline.json"
    phase1_path.write_text(slides.to_json(), encoding='utf-8')
    print(f"  📝 Debug: Saved Phase 1 state to {phase1_path.name}")
    
    # Step 2: Batch generate individual slides in parallel
    print(f"⚙ Generating {len(draft_slides)} slides in parallel...")
    slide_patches = _generate_slides_parallel(draft_slides, atoms, user_instruction, config, intent_guidance)
    
    # Save Phase 2 raw patches for debugging
    phase2_path = output_dir / "debug_phase2_patches.json"
    phase2_path.write_text(json.dumps(slide_patches, indent=2), encoding='utf-8')
    print(f"  📝 Debug: Saved Phase 2 patches to {phase2_path.name}")
    
    # Step 3: Update internal state with all slide patches
    print(f"⚙ Updating slides...")
    for patch_ops in slide_patches:
        if isinstance(patch_ops, dict):
            patch_ops = [patch_ops]
        patch = Patch.from_json_str(json.dumps(patch_ops))
        slides.patch(patch)
    
    # Save final state for debugging
    layout_json_path = output_dir / "intermediate_layout.json"
    layout_json_path.write_text(slides.to_json(), encoding='utf-8')
    print(f"✓ Saved intermediate layout JSON: {layout_json_path.absolute()}")
    
    # Save Phase 3 final state separately for debugging
    phase3_path = output_dir / "debug_phase3_final.json"
    phase3_path.write_text(slides.to_json(), encoding='utf-8')
    print(f"  📝 Debug: Saved Phase 3 final state to {phase3_path.name}")
    print(f"✓ Generated {len(slides.get_active_slides())} active slides")
    
    # Cache result (store combined patch operations)
    if use_cache:
        # Combine all patches into one for caching
        combined_ops = storyline_patch_ops.copy()
        for slide_patch in slide_patches:
            combined_ops.extend(slide_patch if isinstance(slide_patch, list) else [slide_patch])
        
        _cache.save(
            cache_key,
            {
                "cached_data": json.dumps(combined_ops),  # Store as JSON string
                "metadata": {
                    "atom_count": len(atoms),
                    "slide_count": len(slides),
                    "instruction": user_instruction,
                    "intent_guidance": intent_guidance
                }
            }
        )
    
    return slides


def _generate_storyline(
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    intent_guidance: str = ""
) -> Any:
    """
    Generate storyline patch (create draft slides with story + atom references).
    
    Creates slide entries with story descriptions and related atom IDs.
    Also generates theme/preset configuration if needed.
    Does NOT populate layout or widget content yet.
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions
        config: Generation configuration
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        List of patch operations to create draft slides with stories
        
    Raises:
        json.JSONDecodeError: If LLM output is not valid JSON
        Exception: If LLM API call fails
    """
    # Get configuration for storyline generation
    storyline_config = get_storyline_config()
    
    # Render prompts
    system_prompt = storyline_config.system_prompt
    user_prompt = render_storyline_prompt(atoms, user_instruction, intent_guidance)
    
    # Call LLM
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        deployment=config.model,
        temperature=storyline_config.temperature,
        max_tokens=storyline_config.max_tokens,
        max_reasoning_tokens=storyline_config.max_reasoning_tokens
    )
    
    # Parse JSON Patch
    patch_operations = json.loads(response)
    
    return patch_operations


def _generate_slides_parallel(
    draft_slides: List,
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    intent_guidance: str = "",
    max_workers: int = 5
) -> List[Any]:
    """
    Generate individual slides in parallel (draft → active).
    
    Each slide is generated independently based on its story and related atoms.
    Uses ThreadPoolExecutor for parallel LLM calls.
    
    Args:
        draft_slides: List of draft slides with story + atoms defined
        atoms: AtomCollection with all extracted content
        user_instruction: User's generation instructions
        config: Generation configuration
        intent_guidance: Optional guidance from intent detection
        max_workers: Maximum number of parallel LLM calls (default: 5)
        
    Returns:
        List of patch operations (one per slide)
        
    Raises:
        json.JSONDecodeError: If LLM output is not valid JSON
        Exception: If LLM API call fails
    """
    slide_patches = []
    
    # Use ThreadPoolExecutor for parallel generation
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all slide generation tasks
        future_to_slide = {
            executor.submit(
                _generate_single_slide,
                slide,
                atoms,
                user_instruction,
                config,
                intent_guidance
            ): slide
            for slide in draft_slides
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_slide):
            slide = future_to_slide[future]
            try:
                patch_ops = future.result()
                slide_patches.append(patch_ops)
                print(f"  ✓ Generated slide: {slide.id}")
            except Exception as exc:
                print(f"  ✗ Slide {slide.id} failed: {exc}")
                raise
    
    return slide_patches


def _generate_single_slide(
    draft_slide,
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    intent_guidance: str = ""
) -> Any:
    """
    Generate a single slide (draft → active).
    
    Populates layout and widget content based on the slide's story
    and using only the atoms referenced in the slide.
    
    Args:
        draft_slide: Draft slide with story and atoms defined
        atoms: AtomCollection with all extracted content
        user_instruction: User's generation instructions
        config: Generation configuration
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        Patch operations to populate layout/widgets and activate slide
        
    Raises:
        json.JSONDecodeError: If LLM output is not valid JSON
        Exception: If LLM API call fails
    """
    # Get configuration for slide generation
    slide_config = get_slide_generation_config()
    
    # Filter atoms to only those referenced by this slide
    related_atoms = {
        atom_id: atoms.get_atom(atom_id)
        for atom_id in draft_slide.atoms
        if atoms.get_atom(atom_id) is not None
    }
    
    # Render prompts
    system_prompt = slide_config.system_prompt
    user_prompt = render_slide_generation_prompt(
        draft_slide,
        related_atoms,
        user_instruction,
        intent_guidance
    )
    
    # Call LLM
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        deployment=config.model,
        temperature=slide_config.temperature,
        max_tokens=slide_config.max_tokens,
        max_reasoning_tokens=slide_config.max_reasoning_tokens
    )
    
    # Parse JSON Patch
    patch_operations = json.loads(response)
    
    return patch_operations


def _compute_cache_key(
    atoms: AtomCollection,
    user_instruction: str,
    config: GenerationConfig,
    intent_guidance: str = ""
) -> str:
    """
    Compute cache key for layout generation.
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions
        config: Generation configuration
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        str: SHA256 hash of inputs
    """
    # Create deterministic string from inputs
    # Use atoms.to_json() for datetime serialization, then parse back for sorting
    atoms_data = json.loads(atoms.to_json())
    cache_input = json.dumps({
        "atoms": atoms_data,
        "instruction": user_instruction,
        "model": config.model,
        "temperature": config.temperature,
        "intent_guidance": intent_guidance
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
