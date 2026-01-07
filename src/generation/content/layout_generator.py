"""Layout generator - Orchestrates layout generation for draft slides.

Takes draft slides with story, atoms, visual_design and generates:
- layout: Appropriate layout name based on visual_design
- widgets: Widget content populated from atoms  
- mdx: MDX markup for react-mdx projects
- state: "active"

This module is an ORCHESTRATOR - it composes prompts from:
- src/generation/content/prompts.py (content/storytelling prompts)
- src/paged/layout/react/layout_engine.py (layout/widget prompts)

NO actual prompt text should be defined in this file.
"""
from __future__ import annotations

import json
import os
import re
import warnings
from typing import List, Dict, Any, Optional

from src.generation.atom.collection import AtomCollection
from src.utils.llm_client import call_llm


def _get_atom_content(atom) -> str:
    """Extract displayable content from any atom type."""
    if hasattr(atom, 'text') and atom.text:
        return atom.text
    if hasattr(atom, 'quote') and atom.quote:
        return atom.quote
    if hasattr(atom, 'description') and atom.description:
        return atom.description
    if hasattr(atom, 'name') and atom.name:
        parts = [atom.name]
        if hasattr(atom, 'role') and atom.role:
            parts.append(atom.role)
        if hasattr(atom, 'affiliation') and atom.affiliation:
            parts.append(atom.affiliation)
        return " - ".join(parts)
    if hasattr(atom, 'value') and hasattr(atom, 'label'):
        return f"{atom.value} ({atom.label})"
    if hasattr(atom, 'abstract') and atom.abstract:
        return atom.abstract
    return str(atom.id)


def _get_atom_type(atom) -> str:
    """Get the type name of an atom."""
    return type(atom).__name__


def generate_layouts(
    draft_slides: List[Dict],
    context_before: List[Dict],
    context_after: List[Dict],
    atoms: Optional[AtomCollection],
    theme_id: Optional[str] = None,
    intent_guidance: str = "",
    project: str = "react-mdx",
) -> List[Dict[str, Any]]:
    """Generate layouts and widgets for draft slides.
    
    Args:
        draft_slides: Slides with story/atoms/visual_design OR story/content/visual_design
        context_before: Up to 2 active slides before for context
        context_after: Up to 2 active slides after for context
        atoms: AtomCollection for widget content (can be None if slides have embedded content)
        theme_id: Active theme ID
        intent_guidance: Additional guidance
        project: Project type - 'react-mdx' (default), 'slidev' is DEPRECATED
        
    Returns:
        List of active slides with layout and widgets populated (and mdx field for react-mdx)
    """
    if not draft_slides:
        return []
    
    # Check if ANY slide has embedded content or atoms
    has_any_content = any(slide.get("content") or slide.get("atoms") for slide in draft_slides)
    
    if not atoms and not has_any_content:
        # No atoms and no embedded content - can't populate widgets meaningfully
        # Return drafts with minimal layouts
        return _fallback_layouts(draft_slides)
    
    # Slidev is deprecated - warn and redirect to react-mdx
    if project == "slidev":
        warnings.warn(
            "slidev project type is DEPRECATED. Use 'react-mdx' instead. "
            "Automatically using react-mdx.",
            DeprecationWarning,
            stacklevel=2
        )
        project = "react-mdx"
    
    # Use MDX generation for react-mdx projects
    if project in ("react-mdx", "react"):
        return _generate_mdx_layouts(
            draft_slides, context_before, context_after,
            atoms, theme_id, intent_guidance
        )
    
    # Unknown project type - fallback to react-mdx
    warnings.warn(
        f"Unknown project type '{project}'. Using 'react-mdx'.",
        UserWarning,
        stacklevel=2
    )
    return _generate_mdx_layouts(
        draft_slides, context_before, context_after,
        atoms, theme_id, intent_guidance
    )


def _fallback_layouts(draft_slides: List[Dict]) -> List[Dict]:
    """Generate minimal layouts when no atoms available."""
    result = []
    for slide in draft_slides:
        active = dict(slide)
        active["state"] = "active"
        active["layout"] = "center"  # Simple default
        active["widgets"] = {
            "default": {
                "type": "Type.Body",
                "parameters": {"text": slide.get("story", "Slide content")}
            }
        }
        result.append(active)
    return result


def _generate_mdx_layouts(
    draft_slides: List[Dict],
    context_before: List[Dict],
    context_after: List[Dict],
    atoms: Optional[AtomCollection],
    theme_id: Optional[str],
    intent_guidance: str,
) -> List[Dict[str, Any]]:
    """Generate MDX layouts for react-mdx project.
    
    Uses the existing prompts from layout_engine and prompts.py.
    Returns slides with 'mdx' field containing raw MDX markup.
    
    Handles slides with:
    - Only atoms (atom-based generation)
    - Only content (source-based generation)
    - Both atoms AND content (after story refinement attaches atoms)
    
    Args:
        draft_slides: Draft slides with story/atoms/visual_design and/or content
        context_before: Slides before for context
        context_after: Slides after for context
        atoms: AtomCollection for widget content
        theme_id: Active theme ID
        intent_guidance: Additional guidance
    """
    from src.paged.layout.react.mdx_parser import parse_slides_from_mdx
    from src.generation.content.prompts import get_slide_generation_config, render_slide_generation_prompt
    
    # Get system prompt from prompts.py (uses layout_engine.get_layout_prompt())
    config = get_slide_generation_config(project="react-mdx")
    system_prompt = config.system_prompt
    
    # Build draft slides context - include both atoms and content when present
    drafts_summary = []
    for slide in draft_slides:
        slide_summary = {
            "id": slide.get("id"),
            "rank": slide.get("rank"),
            "story": slide.get("story", ""),
            "density": slide.get("density", "moderate"),
            "visual_design": slide.get("visual_design", ""),
        }
        
        # Include content if present (from source-based generation)
        if slide.get("content"):
            slide_summary["content"] = slide.get("content")
        
        # Include atoms if present (from atom extraction or story refinement)
        if slide.get("atoms"):
            slide_summary["atoms"] = slide.get("atoms")
        
        drafts_summary.append(slide_summary)
    
    # Build user prompt - handle slides with atoms, content, or both
    has_any_content = any(slide.get("content") for slide in draft_slides)
    has_any_atoms = any(slide.get("atoms") for slide in draft_slides)
    
    # Always start with draft slides context
    user_prompt = f"""# DRAFT SLIDES
```json
{json.dumps(drafts_summary, indent=2)}
```

"""
    
    if has_any_atoms and atoms:
        # Include atom collection for reference
        user_prompt += render_slide_generation_prompt(
            atoms=atoms,
            user_instruction=intent_guidance if intent_guidance else "Generate presentation slides based on the draft slides above.",
            intent_guidance="",
            themes=None
        )
    elif has_any_content:
        # Content-only slides (no atoms available)
        user_prompt += render_slide_generation_prompt(
            atoms=None,
            user_instruction=intent_guidance if intent_guidance else "Generate presentation slides based on the draft slides above.",
            intent_guidance="",
            themes=None,
            use_content_field=True
        )
    else:
        # Fallback - shouldn't reach here if validation above works
        user_prompt += f"""Generate MDX slides based on the draft slides above.

Instructions: {intent_guidance or 'Create compelling presentation slides.'}
"""
    
    # Add note about handling both atoms and content if both are present
    if has_any_atoms and has_any_content:
        user_prompt += """\n\n**IMPORTANT**: Some slides have BOTH atoms and content fields.
- Use atoms for widget population where available
- Use embedded content as additional context and validation
- Ensure consistency between atoms and content when both are present
"""

    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        deployment=deployment,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    
    # Parse MDX slides using existing parser
    parsed_slides = parse_slides_from_mdx(response)
    
    if not parsed_slides:
        print(f"  [WARN] No MDX slides parsed, falling back to drafts")
        return _fallback_layouts(draft_slides)
    
    # Convert ParsedSlide to dict with mdx field
    active_slides = []
    for parsed in parsed_slides:
        # Find matching draft to preserve visual_design/density/content
        draft = next((d for d in draft_slides if d.get("id") == parsed.id), None)
        
        slide = {
            "id": parsed.id,
            "rank": parsed.rank,
            "state": "active",
            "story": parsed.story,
            "mdx": parsed.mdx,
        }
        
        # Preserve content and atoms from draft (can have both)
        if draft:
            slide["density"] = draft.get("density", "moderate")
            slide["visual_design"] = draft.get("visual_design", "")
            
            # Preserve both content and atoms if present
            if draft.get("content"):
                slide["content"] = draft.get("content")
            if draft.get("atoms"):
                slide["atoms"] = draft.get("atoms")
            
            # Ensure at least one is present for backward compatibility
            if not draft.get("content") and not draft.get("atoms"):
                slide["atoms"] = []
        else:
            # Fallback if no matching draft
            slide["content"] = parsed.content if hasattr(parsed, 'content') else {}
            slide["atoms"] = parsed.atoms if hasattr(parsed, 'atoms') else []
        
        active_slides.append(slide)
    
    return active_slides
