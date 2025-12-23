"""Story generator - Plans narrative arc and creates draft slides.

Generates draft slides with:
- story: Narrative description
- atoms: List of atom IDs
- density: Information density
- visual_design: Visual approach

Layout and widgets are empty (filled by ContentTool).
"""
from __future__ import annotations

import json
import os
import re
from typing import List, Dict, Any, Optional

from src.generation.atom.collection import AtomCollection
from src.utils.llm_client import call_llm


def _get_atom_content(atom) -> str:
    """Extract displayable content from any atom type."""
    # Try different field names based on atom type
    if hasattr(atom, 'text') and atom.text:
        return atom.text
    if hasattr(atom, 'quote') and atom.quote:
        return atom.quote
    if hasattr(atom, 'description') and atom.description:
        return atom.description
    if hasattr(atom, 'name') and atom.name:
        # BioAtom
        parts = [atom.name]
        if hasattr(atom, 'role') and atom.role:
            parts.append(atom.role)
        if hasattr(atom, 'affiliation') and atom.affiliation:
            parts.append(atom.affiliation)
        return " - ".join(parts)
    if hasattr(atom, 'value') and hasattr(atom, 'label'):
        # StatAtom
        return f"{atom.value} ({atom.label})"
    # Fallback to abstract
    if hasattr(atom, 'abstract') and atom.abstract:
        return atom.abstract
    return str(atom.id)


def _get_atom_type(atom) -> str:
    """Get the type name of an atom."""
    return type(atom).__name__


def _get_story_prompt(
    atoms: AtomCollection,
    user_instruction: str,
    slide_count: Optional[int],
    intent_guidance: str,
) -> str:
    """Build prompt for story generation."""
    # Create a compact atom summary for the prompt
    atom_summaries = []
    for atom in atoms.list_contexts():
        # Get content using helper function
        content = _get_atom_content(atom)
        content_preview = content[:200] if len(content) > 200 else content
        atom_summaries.append({
            "id": atom.id,
            "type": _get_atom_type(atom),
            "content": content_preview,
            "rank": atom.rank,
        })
    atoms_json = json.dumps(atom_summaries, indent=2)
    
    target_slides = slide_count or 10
    
    return f"""You are a STORYTELLER who designs presentation narratives.

# INPUT

## Atoms (content units to use)
```json
{atoms_json}
```

## User Instruction
{user_instruction or "Create a compelling presentation"}

## Guidance
{intent_guidance or "None"}

## Target Slides
{target_slides} slides

# OUTPUT

Create draft slides with story arc. Each slide needs:
- id: Unique ID (e.g., "slide_01_hook")
- rank: Order (1-based)
- state: "draft"
- story: Narrative purpose (what this slide accomplishes in the story)
- atoms: List of atom IDs to use (from input atoms)
- density: "minimal" (1-2 points) | "moderate" (3-4) | "dense" (5+)
- visual_design: FREE TEXT describing how to visualize. Include:
  - Desired elements (big number, quote, bullet list, chart, image placeholder, etc.)
  - Orientation/layout concept (left-heavy hero, centered, side-by-side comparison, grid of items, etc.)
  - Visual emphasis (what should stand out, what's supporting)
  - Rough spatial arrangement

Examples of visual_design:
- "Large stat on left (the key number), supporting context text on right"
- "Centered bold quote with author attribution below"
- "Side-by-side comparison: before state left, after state right"
- "Grid of 4 feature cards, each with icon placeholder and short label"
- "Timeline flowing left to right with 5 milestone markers"
- "Full-bleed dramatic single statement, minimal text"
- "Dashboard style: 3 metric cards on top, chart area below"

Leave layout and widgets EMPTY (filled later):
- layout: ""
- widgets: {{}}

# STORY ARC STRUCTURE

1. **HOOK** (1-2 slides): Grab attention with surprising fact or question
2. **CONTEXT** (2-3 slides): Set the scene, establish stakes
3. **JOURNEY** (3-5 slides): Main content, building tension/interest
4. **INSIGHT** (2-3 slides): Key revelations, "aha" moments
5. **CLOSE** (1-2 slides): Resolution, call to action, memorable end

# OUTPUT FORMAT

```json
[
  {{
    "id": "slide_01_hook",
    "rank": 1,
    "state": "draft",
    "story": "HOOK: Surprise with unexpected statistic to grab attention",
    "atoms": ["stat_001", "fact_002"],
    "density": "minimal",
    "visual_design": "Large dramatic number on left, brief context line on right",
    "layout": "",
    "widgets": {{}}
  }},
  ...
]
```

Return ONLY the JSON array, no other text."""


def _get_refine_prompt(
    existing_slides: List[Dict],
    atoms: AtomCollection,
    user_instruction: str,
    intent_guidance: str,
) -> str:
    """Build prompt for story refinement."""
    atoms_json = atoms.to_json(indent=2)
    slides_json = json.dumps(existing_slides, indent=2)
    
    return f"""You are refining an existing presentation story.

# CURRENT SLIDES
```json
{slides_json}
```

# AVAILABLE ATOMS
```json
{atoms_json}
```

# USER REQUEST
{user_instruction}

# GUIDANCE
{intent_guidance or "None"}

# TASK

Modify the story based on the user's request. Common operations:
- Merge slides: Combine story/atoms from multiple slides into one
- Split slide: Divide one slide's content into multiple
- Add slide: Insert new slide with atoms and story
- Remove slide: Delete slide (don't reassign its atoms elsewhere)
- Reorder: Change ranks to restructure flow

# OUTPUT RULES

1. For slides you DON'T change: Keep exactly as-is
2. For slides you CHANGE: Set state="draft" (they need new layout/widgets)
3. Return the COMPLETE slide list (not just changed ones)
4. Keep layout="" and widgets={{}} for all draft slides

# OUTPUT FORMAT

Return ONLY the JSON array of all slides:
```json
[
  {{"id": "slide_01_hook", "rank": 1, "state": "active", ...}},  // unchanged
  {{"id": "slide_02_merged", "rank": 2, "state": "draft", ...}},  // changed
  ...
]
```"""


def generate_story(
    atoms: AtomCollection,
    user_instruction: str,
    slide_count: Optional[int] = None,
    intent_guidance: str = "",
) -> List[Dict[str, Any]]:
    """Generate draft slides with story arc.
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions
        slide_count: Target number of slides
        intent_guidance: Optional guidance from constitution
        
    Returns:
        List of draft slide dicts with story, atoms, visual_design populated
    """
    prompt = _get_story_prompt(atoms, user_instruction, slide_count, intent_guidance)
    
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
    response = call_llm(
        system_prompt="You are a presentation storyteller. Output only valid JSON array.",
        user_prompt=prompt,
        deployment=deployment,
        temperature=0.7,
        max_tokens=8000,  # Need room for 10+ draft slides
    )
    
    # Parse JSON from response
    slides = _parse_json_array(response)
    
    # Validate and normalize
    for slide in slides:
        slide["state"] = "draft"
        slide.setdefault("layout", "")
        slide.setdefault("widgets", {})
        slide.setdefault("density", "moderate")
        slide.setdefault("visual_design", "hierarchical")
    
    return slides


def refine_story(
    existing_slides: List[Dict],
    atoms: AtomCollection,
    user_instruction: str,
    intent_guidance: str = "",
) -> List[Dict[str, Any]]:
    """Refine existing story based on user instruction.
    
    Args:
        existing_slides: Current slides to modify
        atoms: AtomCollection for reference
        user_instruction: What to change
        intent_guidance: Optional guidance
        
    Returns:
        Updated list of slides (mix of active and draft)
    """
    prompt = _get_refine_prompt(existing_slides, atoms, user_instruction, intent_guidance)
    
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
    response = call_llm(
        system_prompt="You are a presentation storyteller. Output only valid JSON array.",
        user_prompt=prompt,
        deployment=deployment,
        temperature=0.7,
        max_tokens=8000,
    )
    
    # Parse JSON from response
    slides = _parse_json_array(response)
    
    # Normalize
    for slide in slides:
        if slide.get("state") == "draft":
            slide.setdefault("layout", "")
            slide.setdefault("widgets", {})
    
    return slides


def _parse_json_array(response: str) -> List[Dict]:
    """Extract JSON array from LLM response."""
    # Try to find JSON array in response
    json_match = re.search(r'\[[\s\S]*\]', response)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    # Try direct parse
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse story response as JSON: {e}")
