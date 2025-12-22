"""Prompt templates for unified slide generation with LLM.

This module provides prompt templates for the single-step slide generation system.
The generation creates a complete presentation from atoms in one LLM call.
"""
import os
import json
from typing import Any, List, Dict

from src.generation.atom.collection import AtomCollection
from src.common.slides import Slides
from src.utils.generation_config import GenerationConfig
from src.paged.layout.engine_registry import LayoutEngineRegistry


# ========== JSON Schema Helpers ==========


def _get_patch_schema_for_add() -> str:
    """Get JSON schema for patch 'add' operations (storyline generation only).
    
    Note: Theme, style, preset are now handled separately in visual generation.
    
    Returns:
        JSON schema string for add operations
    """
    return """{
  "type": "array",
  "description": "Array of add operations to create draft slides with story and atom references",
  "items": {
    "type": "object",
    "properties": {
      "add": {
        "type": "object",
        "description": "Add operation to create a new draft slide",
        "properties": {
          "id": {"type": "string", "description": "Unique slide identifier (e.g., 'slide_001')"},
          "rank": {"type": "integer", "description": "Slide order position (1-based)"},
          "state": {"type": "string", "enum": ["draft"], "description": "Slide state (always 'draft' in storyline)"},
          "story": {"type": "string", "description": "Narrative description of slide purpose and content"},
          "atoms": {"type": "array", "items": {"type": "string"}, "description": "List of atom IDs used in this slide"},
          "density": {"type": "string", "enum": ["minimal", "moderate", "dense"], "description": "Information density"},
          "layout": {"type": "string", "description": "Layout name (empty in draft, populated later)"},
          "widgets": {"type": "object", "description": "Widget assignments (empty {} in draft state)"},
          "header": {"type": "object", "description": "Optional header widget"},
          "footer": {"type": "object", "description": "Optional footer widget"},
          "parameters": {"type": "object", "description": "Layout-specific parameters"}
        },
        "required": ["id", "rank", "state", "story", "atoms", "density", "layout", "widgets", "parameters"]
      }
    },
    "required": ["add"]
  }
}"""


def _get_patch_schema_for_replace() -> str:
    """Get JSON schema for patch 'replace' operations.
    
    Returns:
        JSON schema string for replace operations (without presets)
    """
    # Build widgets schema (simplified, no preset)
    widgets_schema = """{
                "type": "object",
                "description": "Widget assignments mapping slot roles to widget configs. DO NOT include 'atom_id' field - only include 'type' and 'parameters'.",
                "patternProperties": {
                  ".*": {
                    "type": "object",
                    "properties": {
                      "type": {"type": "string", "description": "Widget type (e.g., 'Type.Display')"},
                      "parameters": {"type": "object", "description": "Widget-specific parameters"}
                    },
                    "required": ["type", "parameters"]
                  }
                }
              }"""
    
    return f"""{{
  "type": "array",
  "description": "Array of patch operations to replace/update slides",
  "items": {{
    "type": "object",
    "description": "Replace slide operation",
    "properties": {{
      "replace": {{
        "type": "object",
        "description": "Replace operation to update an existing slide",
        "properties": {{
          "id": {{"type": "string", "description": "Existing slide identifier to replace"}},
          "rank": {{"type": "integer", "description": "Slide order position"}},
          "state": {{"type": "string", "enum": ["draft", "active"], "description": "Updated slide state"}},
          "layout": {{"type": "string", "description": "Layout name"}},
          "widgets": {widgets_schema},
          "header": {{"type": "object", "description": "Optional header widget"}},
          "footer": {{"type": "object", "description": "Optional footer widget"}},
          "parameters": {{"type": "object", "description": "Layout-specific parameters"}}
        }},
        "required": ["id", "rank", "state", "layout", "widgets", "parameters"]
      }}
    }},
    "required": ["replace"]
  }}
}}"""


# ========== Refinement Prompts ==========


def render_refinement_prompt(
    active_slides: Slides,
    atoms: AtomCollection,
    user_instruction: str,
    validation_feedback: str,
    intent_guidance: str = ""
) -> str:
    """
    Render refinement prompt for correcting validation issues in active slides.
    
    This is different from content_generation_prompt because:
    - Works with slides in 'active' state (not 'draft')
    - Includes validation feedback
    - Focuses on correcting specific issues (not initial population)
    
    Args:
        active_slides: Slides collection with slides in active state
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions
        validation_feedback: Formatted validation issues from LayoutValidator
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        Formatted refinement prompt string
        
    Raises:
        ValueError: If slides is empty or instruction empty
    """
    if len(active_slides) == 0:
        raise ValueError("Cannot render refinement prompt with empty slide collection")
    
    if not user_instruction or not user_instruction.strip():
        raise ValueError("User instruction cannot be empty")
    
    # Serialize active slides and atoms to JSON
    slides_json = json.dumps(active_slides.to_dict(), indent=2)
    atoms_json = atoms.to_json(indent=2)
    
    user_prompt = f"""Refine these slides to fix validation issues:

Current Slides (Active State):
{slides_json}

Available Atoms:
{atoms_json}

Original Instructions:
{user_instruction}"""
    
    if intent_guidance:
        user_prompt += f"\n\nIntent Guidance:\n{intent_guidance}"
    
    user_prompt += f"""

---

{validation_feedback}

Generate a JSON Patch with 'replace' operations to fix the issues. Focus on:
- If overlap issues: SHORTEN text in affected widgets by 40-60%
- If color contrast issues: ADJUST colors using theme variables
- If density issues: ADD more widgets or CHANGE layout strategy
- If consistency issues: APPLY same preset to all widgets of same type

Return ONLY the JSON array of patch operations."""
    
    return user_prompt


def render_user_refinement_prompt(
    existing_slides: 'Slides',
    atoms: 'AtomCollection',
    refinement_instruction: str,
    intent_guidance: str = ""
) -> str:
    """
    Render refinement prompt for applying user's refinement instruction to existing slides.
    
    This is different from validation-based refinement because:
    - User-driven changes (not fixing validation errors)
    - May require content/structure changes (not just layout fixes)
    - Can add/remove slides as needed
    
    Args:
        existing_slides: Current Slides collection
        atoms: AtomCollection with extracted content
        refinement_instruction: User's refinement request
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        Formatted refinement prompt string
        
    Raises:
        ValueError: If slides or instruction is empty
    """
    if len(existing_slides) == 0:
        raise ValueError("Cannot render refinement prompt with empty slide collection")
    
    if not refinement_instruction or not refinement_instruction.strip():
        raise ValueError("Refinement instruction cannot be empty")
    
    # Serialize existing slides and atoms to JSON
    slides_json = json.dumps(existing_slides.to_dict(), indent=2)
    atoms_json = atoms.to_json(indent=2)
    
    user_prompt = f"""Refine this presentation based on user's request:

Current Slides:
{slides_json}

Available Atoms:
{atoms_json}

User's Refinement Request:
{refinement_instruction}"""
    
    if intent_guidance:
        user_prompt += f"\n\nIntent Guidance:\n{intent_guidance}"
    
    user_prompt += """

---

Generate patch operations to refine the slides using our Patch model format.

IMPORTANT: When creating/replacing slides, include ALL required fields:
- id: Unique slide identifier (must match existing slide ID when replacing)
- rank: Integer for ordering (e.g., 100, 200, 300)
- state: MUST be "active" for slides to render (NOT "draft" or "archived")
- layout: Layout strategy name (check layout engine documentation)
- widgets: Object mapping slot roles to widget configurations
  **CRITICAL**: Only use slot roles that exist in the chosen layout strategy!
  Check layout documentation for available slot names - do NOT invent slot names!
- header: Optional header widget (can be empty object {})
- footer: Optional footer widget (can be empty object {})
- parameters: Layout-specific parameters (can be empty object {})

Available Operations:
1. AddOperation: {"add": <complete Slide object>} - adds new slide
2. ReplaceOperation: {"replace": <complete Slide object>} - replaces existing slide with matching ID
3. RemoveOperation: {"remove": {"id": "slide_id"}} - removes slide by ID

Example (replacing slide_01 with modified version):
{
  "operations": [
    {
      "replace": {
        "id": "slide_01",
        "rank": 1,
        "state": "active",
        "layout": "<layout_from_docs>",
        "widgets": {
          "<slot_from_layout_docs>": {
            "type": "<widget_type_from_docs>",
            "parameters": {"text": "Updated Title"}
          }
        },
        "header": {},
        "footer": {},
        "parameters": {}
      }
    }
  ]
}

CRITICAL: Widget objects should ONLY contain "type" and "parameters".
DO NOT include "atom_id" or any other fields in widget definitions.

Example (removing slide_04):
{
  "operations": [
    {
      "remove": {"id": "slide_04_two_eras_compared"}
    }
  ]
}

For different refinement types:
- Style changes: Use ReplaceOperation with modified widgets/text
- Content changes: Use ReplaceOperation or AddOperation
- Structure changes: Use RemoveOperation + AddOperation
- CRITICAL: When replacing, the new slide's ID must match the old slide's ID

Make incremental, focused changes."""
    
    return user_prompt


# ========== Unified Slide Generation System ==========

def get_slide_generation_config() -> GenerationConfig:
    """Get GenerationConfig for unified slide generation.
    
    Returns:
        GenerationConfig with appropriate parameters for complete slide generation
    """
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo')
    return GenerationConfig(
        model=deployment,
        temperature=0.5,  # Balanced for structure + creativity
        max_tokens=16000,  # Full deck generation
        system_prompt=_build_slide_generation_system_prompt(),
        user_prompt_template=""  # Will be rendered by render_slide_generation_prompt
    )


# Keep for backward compatibility
def get_storyline_config() -> GenerationConfig:
    """Deprecated: Use get_slide_generation_config instead.
    
    Returns:
        GenerationConfig for unified slide generation
    """
    return get_slide_generation_config()


def _build_slide_generation_system_prompt() -> str:
    """Build unified slide generation system prompt.
    
    Returns:
        Complete system prompt for single-step slide generation
    """
    # Get layout documentation
    from src.paged.layout.engine_registry import LayoutEngineRegistry
    active_engine = LayoutEngineRegistry.get_active_engine()
    layout_docs = active_engine.get_layout_documentation()
    layout_constraints = active_engine.get_layout_constrain()
    
    return f"""You are a STORYTELLER who designs presentations. Your job is to create emotional journeys, not information dumps.

# THE GOLDEN RULE: LESS IS MORE

⚠️ **CRITICAL**: You do NOT need to use all atoms. A 10-15 slide deck using 30-40% of atoms is BETTER than a 25-slide deck using everything.

## Atom Selection Strategy
1. **Identify the ONE big idea** - What's the single takeaway?
2. **Pick 5-8 atoms max** that directly support that idea
3. **Ruthlessly cut** atoms that are:
   - Interesting but tangential
   - Detailed but not essential to the arc
   - Repetitive (pick the best example, skip the rest)
4. **Leave the audience wanting more** - Mystery is good

## What to CUT (even if interesting)
- Technical details that don't serve the emotional arc
- Multiple examples when one powerful example suffices
- Background context the audience can infer
- "Complete coverage" thinking - this isn't a textbook

## Ideal Slide Count
| Source Length | Target Slides | Atoms to Use |
|---------------|---------------|--------------|
| 10-15 atoms | 8-10 slides | 5-8 atoms |
| 20-30 atoms | 10-14 slides | 8-12 atoms |
| 30+ atoms | 12-16 slides | 10-15 atoms |

**If you're making more than 16 slides, you're probably covering too much.**

# STORYTELLING STRUCTURE

## The Presentation Arc
Every great presentation follows this emotional structure:

1. **HOOK** (1-2 slides): Grab attention with something unexpected
   - A surprising number ("14 years → 3 pivots")
   - A provocative question ("What if everything you learned is obsolete?")
   - A bold claim that demands proof
   
2. **TENSION** (1-2 slides): Create stakes and conflict
   - "The old way is dying"
   - "Here's what most people get wrong"
   - Show the gap between expectation and reality
   
3. **JOURNEY** (4-8 slides): Build understanding through progression
   - Pick 2-3 KEY moments, not every detail
   - Each slide should answer: "And then what happened?"
   - Show transformation: Before → Struggle → After
   
4. **REVELATION** (1-2 slides): The "aha moment"
   - Connect the dots
   - Reveal the pattern they couldn't see
   
5. **CALL TO ACTION** (1-2 slides): What should they DO?
   - Clear, actionable takeaway
   - Memorable closing phrase

## Tension Techniques
❌ BAD (boring summary): "Phase 1: Vision, Phase 2: Edge AI, Phase 3: LLMs"
✅ GOOD (creates tension): 
   - "2015: Everything I knew became obsolete"
   - "The skill that saved me → The skill that almost killed me"
   - "What they don't tell you about the AI pivot"

## Pacing Rules
- **Breathe**: After dense content, give a minimal "pause" slide
- **Punch**: Big claims need big typography (hero-split, center)
- **Cut**: If a slide doesn't advance the STORY, delete it
- **Trust**: The audience doesn't need every detail

## Emotional Beats Per Slide
Each slide should evoke ONE feeling:
- Curiosity: "Wait, what?"
- Recognition: "Yes, I've seen that!"
- Surprise: "I didn't expect that"
- Tension: "Uh oh, what happens next?"
- Relief: "Ah, that makes sense"
- Inspiration: "I want to do that"

# CONTENT TRANSFORMATION

## From Atoms to Story
Don't just present atoms—DRAMATIZE the BEST ones:

| Atom Content | ❌ Summary Style | ✅ Story Style |
|--------------|------------------|----------------|
| "Joined Microsoft 2011" | "Joined Microsoft in 2011" | "2011: Fresh PhD, no idea what's coming" |
| "Built Face API" | "Built Face API service" | "500M faces processed → one humbling lesson" |
| "Shifted to LLMs" | "Transitioned to LLM work" | "The pivot that changed everything" |
| "3 major career phases" | "Career had 3 phases" | "3 deaths, 3 rebirths" |

## Headlines That Hook
- Use contrast: "Old vs New", "Expected vs Reality"
- Use numbers with context: "14 years → 3 pivots"
- Use action verbs: "Killed", "Built", "Pivoted", "Survived"
- Create curiosity gaps: "The skill nobody talks about"

## Brevity WITH Punch
- ❌ "I have worked in artificial intelligence for fourteen years"
- ✅ "**14 years** in AI trenches"
- ❌ "The transition from traditional ML to LLMs was challenging"
- ✅ "ML → LLM: **Everything changed**"

{layout_docs}

{layout_constraints}

# LAYOUT FOR EMOTION

⚠️ **CRITICAL**: Use ONLY these exact layout names. NEVER invent names like "Cinematic.Split_50_50".

## Layout → Emotional Purpose
| Layout | Emotion | When to Use |
|--------|---------|-------------|
| `hero-split` | Impact, contrast | Opening hooks, key reveals, comparisons |
| `center` | Focus, importance | Single powerful statements, closings |
| `comparison` | Tension, choice | Before/after, old/new, problem/solution |
| `timeline` | Progress, journey | Evolution, process, transformation |
| `smart-grid` | Framework, clarity | Multiple related points, categories |
| `dashboard` | Evidence, proof | Data-heavy validation slides |
| `spotlight` | Drama, emphasis | Big reveals, emotional peaks |
| `quote-hero` | Wisdom, reflection | Memorable quotes, lessons |

✅ VALID layout names: hero-split, center, comparison, timeline, smart-grid, dashboard, spotlight, quote-hero, full-bleed, two-cols-header
❌ INVALID (will break): Cinematic.Split_50_50, Bento.Standard, Matrix.Timeline, etc.

## Slot Names (MANDATORY)
- `hero-split`: `left`, `right`
- `smart-grid`: `header`, `col1`, `col2`, `col3`, `col4`
- `timeline`: `title`, `step1`, `step2`, `step3`, `step4`, `step5`
- `comparison`: `title`, `beforeLabel`, `before`, `afterLabel`, `after`
- `dashboard`: `title`, `metric1`, `metric2`, `metric3`, `metric4`, `chart`
- `center`: `default` (single slot)
- `spotlight`: `title`, `subtitle`, `description`

# VARIETY & RHYTHM

## Visual Rhythm
- **Max 2** consecutive slides with same layout
- **Alternate** between dense and minimal
- **Punctuate** with single-point impact slides

## Widget Variety (Required)
- At least **1 Data.BigNum** (anchor number)
- At least **1 Type.Quote** or provocative statement
- At least **1 comparison** or timeline slide
- **No more than 40%** list-dominant slides

## Density Flow
```
Opening:  ▓░░░░░░░░░  (minimal - big impact)
Build:    ▓▓▓░░░░░░░  (moderate - context)
Middle:   ▓▓▓▓▓░░░░░  (can be dense - details)
Reveal:   ▓▓▓░░░░░░░  (moderate - connect)
Close:    ▓░░░░░░░░░  (minimal - memorable)
```

# OUTPUT FORMAT

Return a JSON array. Each slide needs a `story` field explaining its NARRATIVE PURPOSE:

```json
[
  {{
    "add": {{
      "id": "slide_01_hook",
      "rank": 1,
      "state": "active",
      "story": "HOOK: Surprise with career span + hint at transformation",
      "atoms": ["bio_001"],
      "density": "minimal",
      "layout": "hero-split",
      "widgets": {{
        "left": {{
          "type": "Data.BigNum",
          "parameters": {{ "value": "14", "label": "Years in AI", "sublabel": "3 pivots, 1 constant" }}
        }},
        "right": {{
          "type": "Type.Body",
          "parameters": {{ "text": "The skill that saved me **3 times**" }}
        }}
      }},
      "parameters": {{ "ratio": "40-60", "vibe": "aurora" }}
    }}
  }},
  {{
    "add": {{
      "id": "slide_02_tension",
      "rank": 2,
      "state": "active", 
      "story": "TENSION: Set up the conflict - skills become obsolete",
      "atoms": [],
      "density": "minimal",
      "layout": "center",
      "widgets": {{
        "default": {{
          "type": "Type.Display",
          "parameters": {{ "text": "Every 5 years,\\neverything I knew\\nbecame **obsolete**" }}
        }}
      }},
      "parameters": {{ "vibe": "waves" }}
    }}
  }}
]
```

# QUALITY CHECKLIST

Before outputting, verify:
✓ **Slide count**: 10-16 slides max (if more, you're covering too much)
✓ **Atom usage**: Using <50% of available atoms (be selective!)
✓ **Hook**: Does slide 1 create genuine curiosity?
✓ **Tension**: Is there real conflict in slides 2-3?
✓ **Focus**: Does every slide advance ONE story (not multiple threads)?
✓ **Cut test**: Could you remove any slide without hurting the story? If yes, remove it.
✓ **Ending**: Is it memorable and actionable?
"""


def render_slide_generation_prompt(
    atoms: AtomCollection,
    user_instruction: str,
    intent_guidance: str = "",
    themes: List[Dict[str, Any]] = None
) -> str:
    """Render user prompt for unified slide generation.
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions
        intent_guidance: Optional guidance from intent detection
        themes: List of available theme objects with id field
        
    Returns:
        Formatted user prompt string
    """
    atoms_json = atoms.to_json(indent=2)
    
    user_prompt = f"""Generate a complete presentation from these atoms:

**Available Atoms**:
{atoms_json}

**User Instructions**:
{user_instruction}
"""
    
    if intent_guidance:
        user_prompt += f"""
**Presentation Guidance**:
{intent_guidance}
"""
    
    # Add themes information
    if themes and len(themes) > 0:
        themes_info = []
        for t in themes:
            theme_id = t.get("id", "default")
            theme_desc = t.get("description", "No description")
            themes_info.append(f'  - "{theme_id}": {theme_desc}')
        themes_list = "\n".join(themes_info)
        
        default_theme = themes[0].get("id", "default")
        user_prompt += f"""
**Available Themes**:
{themes_list}

Assign theme "{default_theme}" to all slides unless varying for emphasis.
"""
    
    user_prompt += """
**YOUR MISSION**:
Create a STORY, not a summary. The audience should feel:
1. **Hooked** in the first slide (surprise, intrigue)
2. **Tension** early (conflict, stakes, "what went wrong")
3. **Journey** through the middle (transformation, lessons)
4. **Revelation** near the end (the insight that ties it together)
5. **Inspired** at the close (clear takeaway, call to action)

**CRITICAL - BE SELECTIVE**:
- Use only 30-50% of atoms (pick the BEST ones for your story)
- Target 10-14 slides max (fewer is better)
- Cut anything that doesn't directly serve the main narrative
- Leave the audience wanting more, not exhausted

**AVOID**:
- Trying to cover ALL the atoms (this is the #1 mistake)
- Boring "overview" slides listing topics
- Every slide being a bullet list
- Chronological summary without drama

**TECHNICAL REQUIREMENTS**:
- Use ONLY layout names from the protocol (hero-split, smart-grid, timeline, comparison, etc.)
- Use ONLY exact slot names (left/right, col1/col2, step1/step2, etc.)
- Include at least 1 Data.BigNum, 1 comparison or quote
- Max 2 consecutive slides with same layout

Generate the complete JSON array of add operations.
"""
    
    return user_prompt


# Backward compatibility alias
def render_storyline_prompt(
    atoms: AtomCollection,
    user_instruction: str,
    intent_guidance: str = "",
    themes: List[Dict[str, Any]] = None
) -> str:
    """Deprecated: Use render_slide_generation_prompt instead.
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions
        intent_guidance: Optional guidance from intent detection
        themes: List of available theme objects with id field
        
    Returns:
        Formatted user prompt string
    """
    return render_slide_generation_prompt(atoms, user_instruction, intent_guidance, themes)


def render_slide_refinement_prompt(
    existing_slides: List[Dict],
    atoms: Any,
    user_instruction: str,
    intent_guidance: str = "",
    themes: List = None
) -> str:
    """Render prompt for slide refinement (targeted changes to existing slides).
    
    Args:
        existing_slides: Current slides as list of dicts
        atoms: AtomCollection for reference
        user_instruction: User's refinement instruction
        intent_guidance: Constitution guidance (exclusions, requirements, style rules)
        themes: List of available themes
        
    Returns:
        Formatted user prompt for refinement
    """
    # Format existing slides summary (not full content to save tokens)
    slides_summary = []
    for i, slide in enumerate(existing_slides):
        summary = {
            "id": slide.get("id", f"slide_{i+1:03d}"),
            "rank": slide.get("rank", i + 1),
            "layout": slide.get("layout", "unknown"),
            "widgets": list(slide.get("widgets", {}).keys()),
        }
        # Extract title if available
        widgets = slide.get("widgets", {})
        for slot, widget in widgets.items():
            if widget and isinstance(widget, dict):
                params = widget.get("parameters", {})
                if "title" in params:
                    summary["title"] = params["title"][:50]
                    break
                elif "text" in params:
                    summary["preview"] = params["text"][:50]
                    break
        slides_summary.append(summary)
    
    prompt_parts = [
        "## Current Slides",
        f"You have {len(existing_slides)} existing slides:",
        "```json",
        json.dumps(slides_summary, indent=2),
        "```",
        "",
    ]
    
    # Add constitution guidance
    if intent_guidance:
        prompt_parts.extend([
            "## Content Rules (from Constitution)",
            intent_guidance,
            "",
        ])
    
    # Add user instruction
    prompt_parts.extend([
        "## User Instruction",
        user_instruction,
        "",
        "## Your Task",
        "Based on the content rules and user instruction, generate patch operations to refine the slides.",
        "- Use 'replace' to modify slide content (keep same id)",
        "- Use 'remove' to delete slides that violate rules",
        "- Only include operations for slides that need to change",
        "- If a rule says to exclude certain content, remove or replace that content",
        "",
        "Return ONLY a JSON array of patch operations. If no changes needed, return []",
    ])
    
    # Add full slide data for reference
    prompt_parts.extend([
        "",
        "## Full Slide Data (for reference when generating replace operations)",
        "```json",
        json.dumps(existing_slides, indent=2),
        "```",
    ])
    
    return "\n".join(prompt_parts)


def _get_density_description(density: str) -> str:
    """Get human-readable description of density level.
    
    Args:
        density: Density level ('minimal', 'moderate', 'dense')
        
    Returns:
        Description string
    """
    descriptions = {
        "minimal": "1-2 key points, large typography",
        "moderate": "3-4 points max, standard layout",
        "dense": "5 points max, compact layout"
    }
    return descriptions.get(density, "3-4 points max, standard layout")
