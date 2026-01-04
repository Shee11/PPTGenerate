"""Layout generator - Orchestrates layout generation for draft slides.

Takes draft slides with story, atoms, visual_design and generates:
- layout: Appropriate layout name based on visual_design
- widgets: Widget content populated from atoms  
- mdx: MDX markup for react-mdx projects
- state: "active"

This module is an ORCHESTRATOR - it composes prompts from:
- src/generation/content/prompts.py (content/storytelling prompts)
- src/paged/layout/react/layout_engine.py (layout/widget prompts)
- src/generation/content/chart_selector.py (LLM-based chart type selection)

NO actual prompt text should be defined in this file.
"""
from __future__ import annotations

import json
import logging
import os
import re
import warnings
from typing import List, Dict, Any, Optional

from src.generation.atom.collection import AtomCollection
from src.utils.llm_client import call_llm

logger = logging.getLogger(__name__)


def _apply_chart_type_selection(atoms: AtomCollection) -> None:
    """Apply LLM-based chart type selection to atoms with visual="chart".
    
    For atoms that have visual="chart" but no explicit chart_type,
    uses LLM to analyze the data and select the optimal chart type.
    
    This modifies the atoms in place.
    """
    from src.generation.content.chart_selector import (
        should_select_chart_type,
        select_chart_type,
        ChartSelectionContext,
    )
    
    if not atoms:
        return
    
    # Iterate through all atoms and apply chart selection where needed
    for atom in atoms.list_contexts():
        atom_dict = atom.to_dict() if hasattr(atom, 'to_dict') else atom.model_dump() if hasattr(atom, 'model_dump') else vars(atom)
        
        if should_select_chart_type(atom_dict):
            data = atom_dict.get("data") or atom_dict.get("chart_data") or []
            description = atom_dict.get("description") or atom_dict.get("text") or ""
            
            context = ChartSelectionContext(
                data=data,
                description=description,
                slide_context="",  # Could add surrounding context if needed
                suggested_type=atom_dict.get("chart_type") or atom_dict.get("chartType"),
            )
            
            try:
                result = select_chart_type(context)
                
                # Update the atom with selected chart type
                if hasattr(atom, 'chart_type'):
                    atom.chart_type = result.chart_type
                elif hasattr(atom, 'chartType'):
                    atom.chartType = result.chart_type
                else:
                    # Try to set as attribute
                    setattr(atom, 'chart_type', result.chart_type)
                
                logger.info(
                    f"Chart type selected for atom {atom_dict.get('id', 'unknown')}: "
                    f"{result.chart_type} (confidence: {result.confidence:.2f})"
                )
                logger.debug(f"Selection reasoning: {result.reasoning}")
                
            except Exception as e:
                logger.warning(f"Chart type selection failed for atom: {e}")
                # Atom keeps its original state, will use default in rendering


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
        draft_slides: Slides with story/atoms/visual_design but no layout/widgets
        context_before: Up to 2 active slides before for context
        context_after: Up to 2 active slides after for context
        atoms: AtomCollection for widget content
        theme_id: Active theme ID
        intent_guidance: Additional guidance
        project: Project type - 'react-mdx' (default), 'slidev' is DEPRECATED
        
    Returns:
        List of active slides with layout and widgets populated (and mdx field for react-mdx)
    """
    if not draft_slides:
        return []
    
    if not atoms:
        # No atoms - can't populate widgets meaningfully
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
    atoms: AtomCollection,
    theme_id: Optional[str],
    intent_guidance: str,
) -> List[Dict[str, Any]]:
    """Generate MDX layouts for react-mdx project.
    
    Uses the existing prompts from layout_engine and prompts.py.
    Returns slides with 'mdx' field containing raw MDX markup.
    
    Chart Type Selection:
    - Before generating MDX, applies LLM-based chart type selection
    - For atoms with visual="chart" and no explicit chart_type,
      the optimal chart type is automatically selected based on data patterns
    """
    from src.paged.layout.react.mdx_parser import parse_slides_from_mdx
    from src.generation.content.prompts import get_slide_generation_config, render_slide_generation_prompt
    
    # Apply LLM-based chart type selection to atoms (Feature: 003-extended-chart-types)
    _apply_chart_type_selection(atoms)
    
    # Get system prompt from prompts.py (uses layout_engine.get_layout_prompt())
    config = get_slide_generation_config(project="react-mdx")
    system_prompt = config.system_prompt
    
    # Build user prompt using existing function
    user_prompt = render_slide_generation_prompt(
        atoms=atoms,
        user_instruction=intent_guidance,
        intent_guidance="",
        themes=None
    )
    
    # Add draft slides context to the prompt
    drafts_summary = []
    for slide in draft_slides:
        drafts_summary.append({
            "id": slide.get("id"),
            "rank": slide.get("rank"),
            "story": slide.get("story", ""),
            "atoms": slide.get("atoms", []),
            "density": slide.get("density", "moderate"),
            "visual_design": slide.get("visual_design", ""),
        })
    
    user_prompt = f"""# DRAFT SLIDES (use these IDs, ranks, stories, atoms)
```json
{json.dumps(drafts_summary, indent=2)}
```

{user_prompt}"""

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
        # Find matching draft to preserve visual_design/density
        draft = next((d for d in draft_slides if d.get("id") == parsed.id), None)
        
        slide = {
            "id": parsed.id,
            "rank": parsed.rank,
            "state": "active",
            "story": parsed.story,
            "atoms": parsed.atoms,
            "mdx": parsed.mdx,
        }
        
        if draft:
            slide["density"] = draft.get("density", "moderate")
            slide["visual_design"] = draft.get("visual_design", "")
        
        active_slides.append(slide)
    
    return active_slides
