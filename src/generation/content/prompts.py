"""Prompt templates for layout generation with LLM."""
import os
import json
from typing import Any, List, Dict

from src.generation.atom.collection import AtomCollection
from src.common.slides import Slides
from src.utils.generation_config import GenerationConfig
from src.common.asset_manager import AssetManager


# ========== Helper Functions for Dynamic Prompt Generation ==========

def _format_strategies_for_prompt() -> str:
    """Format available layout strategies for LLM prompt.
    
    Returns:
        Formatted string listing all strategies with their slot structures and content guidance
    """
    strategies = AssetManager.list_strategies()
    
    # Layout family descriptions for content guidance
    family_descriptions = {
        "Bento": "Grid-based layouts with multiple content cells. Best for: data comparisons, feature highlights, multi-topic summaries. Content should be parallel in structure and concise.",
        "Cinematic": "Full-bleed dramatic layouts emphasizing visual impact. Best for: hero statements, key messages, emotional moments. Content should be bold and declarative.",
        "Swiss": "Typography-focused minimalist layouts. Best for: quotes, philosophical statements, core principles. Content should be distilled to essential truth.",
        "Data": "Metric-driven layouts with KPIs and numbers. Best for: statistics, performance metrics, quantitative insights. Content should be numeric facts with brief labels.",
        "Edit": "Magazine-style artistic layouts with overlapping elements. Best for: creative storytelling, visual narratives. Content should be evocative and layered.",
        "Focus": "Single-point emphasis layouts. Best for: key takeaways, central concepts, primary messages. Content should be the ONE thing that matters."
    }
    
    lines = ["Available Layout Strategies:"]
    
    # Group by family
    families = {}
    for strategy in strategies:
        family = strategy['family']
        if family not in families:
            families[family] = []
        families[family].append(strategy)
    
    for family, family_strategies in sorted(families.items()):
        # Add family description
        if family in family_descriptions:
            lines.append(f"\n{family} Family: {family_descriptions[family]}")
        
        for strategy in family_strategies:
            # Format each slot with both role and size
            slot_details = []
            for slot in strategy['slots']:
                slot_details.append(f"{slot['role']} (size: {slot['size']})")
            
            slot_info = ", ".join(slot_details)
            lines.append(f"  - {strategy['name']}: Slots: [{slot_info}]")
    
    return "\n".join(lines)


def _format_widgets_for_prompt() -> str:
    """Format available widget types for LLM prompt.
    
    Returns:
        Formatted string listing all widget types with their parameters
    """
    widgets = AssetManager.list_widgets()
    lines = ["Supported Widget Types:"]
    
    for widget in widgets:
        # Extract key parameters to include in prompt
        param_info = []
        if 'fields' in widget and 'parameters' in widget['fields']:
            param_field = widget['fields']['parameters']
            if 'parameters' in param_field:
                # Has structured parameter info
                params = param_field['parameters']
                param_names = [p['name'] for p in params[:3]]  # Show first 3 params
                param_info = [f"parameters: {', '.join(param_names)}"]
        
        # Format widget entry
        desc = widget.get('description', '')
        if param_info:
            lines.append(f"- {widget['type']}: {desc} ({'; '.join(param_info)})")
        else:
            lines.append(f"- {widget['type']}: {desc} (parameters: varies by widget)")
    
    return "\n".join(lines)


def _format_presets_for_prompt() -> str:
    """Format preset categories and variants for LLM prompt.
    
    Returns:
        Formatted string listing all preset categories and their variants
    """
    # Presets are hardcoded in CLI - replicate that structure here
    presets = {
        "Surface": {
            "description": "Visual depth and layering effects",
            "variants": ["Flat", "Elevated", "Outline", "Glass", "Sunken", "NeoBrutal", "Subtle"]
        },
        "Shape": {
            "description": "Border radius and corner styles",
            "variants": ["Sharp", "Rounded", "Curve", "Pill", "Squircle", "Organic"]
        },
        "Fill": {
            "description": "Background patterns and fills",
            "variants": ["Solid_Brand", "Solid_Surface", "Subtle", "Gradient_Linear", "Gradient_Mesh", "Pattern_Dot", "Noise"]
        },
        "Effect": {
            "description": "Visual treatments and filters",
            "variants": ["Duotone", "Glitch", "Glow", "Tape", "Shadow"]
        }
    }
    
    lines = ["Supported Preset Attributes (per widget):"]
    for category, info in presets.items():
        category_lower = category.lower()
        variants = ", ".join(info["variants"])
        lines.append(f"- {category_lower}: {variants}")
    
    return "\n".join(lines)


def _get_theme_schema() -> str:
    """Get JSON schema for theme configuration.
    
    Returns:
        JSON schema string for theme
    """
    return """{
  "type": "object",
  "description": "Theme configuration for presentation styling",
  "properties": {
    "id": {"type": "string", "description": "Unique theme identifier"},
    "primary_color": {"type": "string", "description": "Primary brand color (hex)"},
    "secondary_color": {"type": "string", "description": "Secondary brand color (hex)"},
    "accent_color": {"type": "string", "description": "Accent/highlight color (hex)"},
    "background_color": {"type": "string", "description": "Default background color (hex)"},
    "text_color": {"type": "string", "description": "Default text color (hex)"},
    "font_family": {"type": "string", "description": "Primary font family"},
    "margin_x": {"type": "string", "description": "Horizontal margin (e.g., '40px')"},
    "margin_y": {"type": "string", "description": "Vertical margin (e.g., '30px')"},
    "gutter": {"type": "string", "description": "Spacing between widgets (e.g., '20px')"}
  }
}"""


def _get_preset_schema() -> str:
    """Get JSON schema for preset configuration (per-widget).
    
    Returns:
        JSON schema string for preset
    """
    return """{
  "type": "object",
  "description": "Visual preset for widget styling",
  "properties": {
    "surface": {
      "type": "string",
      "enum": ["Flat", "Elevated", "Outline", "Glass", "Sunken", "NeoBrutal", "Subtle"],
      "description": "Visual depth effect"
    },
    "shape": {
      "type": "string",
      "enum": ["Sharp", "Rounded", "Curve", "Pill", "Squircle", "Organic"],
      "description": "Border radius style"
    },
    "fill": {
      "type": "string",
      "enum": ["Solid_Brand", "Solid_Surface", "Subtle", "Gradient_Linear", "Gradient_Mesh", "Pattern_Dot", "Noise"],
      "description": "Background fill pattern"
    },
    "effect": {
      "type": "string",
      "enum": ["Duotone", "Glitch", "Glow", "Tape", "Shadow"],
      "description": "Visual effect/filter"
    }
  }
}"""


def _get_style_schema() -> str:
    """Get JSON schema for style configuration (widget-type defaults).
    
    Returns:
        JSON schema string for style
    """
    return """{
  "type": "object",
  "description": "Widget-type styling defaults that map widget types to theme tokens",
  "properties": {
    "theme_name": {"type": "string", "description": "Reference to theme ID"},
    "widgets": {
      "type": "object",
      "description": "Per widget-type styling (e.g., 'Type.Display', 'Data.BigNum')",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "font": {"type": "string", "description": "Theme typography token (h1, h2, h3, body, caption)"},
          "align": {"type": "string", "enum": ["left", "center", "right", "justify"], "description": "Text alignment"},
          "vertical_align": {"type": "string", "enum": ["top", "center", "bottom"], "description": "Vertical alignment"},
          "foreground": {"type": "string", "description": "Theme color token for text (primary_color, text_color, etc.)"},
          "background": {"type": "string", "description": "Theme color token for background"},
          "border_radius": {"type": "string", "description": "Border radius (e.g., '8px', '12px')"}
        }
      }
    }
  }
}"""


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
        JSON schema string for replace operations including slides, theme, and presets
    """
    theme_schema = _get_theme_schema()
    preset_schema = _get_preset_schema()
    
    # Build widgets schema separately to avoid f-string nesting issues
    widgets_schema = f"""{{
                "type": "object",
                "description": "Widget assignments mapping slot roles to widget configs. DO NOT include 'atom_id' field - only include 'type', 'parameters', and optionally 'preset'.",
                "patternProperties": {{
                  ".*": {{
                    "type": "object",
                    "properties": {{
                      "type": {{"type": "string", "description": "Widget type (e.g., 'Type.Display')"}},
                      "parameters": {{"type": "object", "description": "Widget-specific parameters"}},
                      "preset": {preset_schema}
                    }},
                    "required": ["type", "parameters"]
                  }}
                }}
              }}"""
    
    return f"""{{
  "type": "array",
  "description": "Array of patch operations to replace/update slides, theme, or presets",
  "items": {{
    "oneOf": [
      {{
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
      }},
      {{
        "type": "object",
        "description": "Set theme operation",
        "properties": {{
          "set_theme": {theme_schema}
        }},
        "required": ["set_theme"]
      }},
      {{
        "type": "object",
        "description": "Set global preset (applied to all widgets by default)",
        "properties": {{
          "set_preset": {preset_schema}
        }},
        "required": ["set_preset"]
      }}
    ]
  }}
}}"""


# ========== System Prompts ==========

def _build_state_transition_system_prompt() -> str:
    """Build state transition system prompt dynamically from AssetManager.
    
    Returns:
        Complete system prompt for state transition step
    """
    strategies_list = _format_strategies_for_prompt()
    patch_schema = _get_patch_schema_for_add()
    
    return f"""You are a presentation structure designer specializing in layout strategy selection.

Your task: Analyze atoms and user instructions to determine:
1. Theme and preset configuration (generate FIRST)
2. Number of slides needed (7-15 MAXIMUM, target 8-12)
3. Layout strategy for each slide
4. Logical slide ordering

{strategies_list}

IMPORTANT RULES:
1. **START with theme/preset operations**: Generate "set_theme" and "set_preset" operations FIRST (before any slide operations)
2. Create slide entries with strategy assignments
3. Set ALL slides to "draft" state
4. Do NOT populate widget content yet (widgets should be empty dict)
5. Include: id, rank, state="draft", strategy, widgets=(empty dict), parameters=(empty dict)
6. **CRITICAL**: Do NOT create slides with strategies "Theme.Set" or "Preset.Set" - use patch operations instead
7. **ONLY use strategies from the Available Layout Strategies list above** for actual content slides
8. **SLIDE COUNT LIMIT**: Create 7-15 slides MAXIMUM. If you have more atoms, merge them into fewer slides with richer layouts (Bento.Standard, Matrix.Grid, etc.)

**Theme/Preset Configuration** (Required):
- Generate "set_theme" operation with theme colors, typography, spacing
- Generate "set_preset" operation with visual style keywords
- These operations apply to the entire presentation, not individual slides

**Example Patch Output**:
[
  {{"set_theme": {{"id": "tech_blue", "primary_color": "#0066ff", "accent_color": "#00ccff", "background_color": "#ffffff", "text_color": "#1a1a1a"}}}},
  {{"set_preset": {{"surface": "Elevated", "shape": "Rounded", "fill": "Solid_Brand", "effect": "Shadow"}}}},
  {{"add": {{"id": "slide_001", "rank": 1, "state": "draft", "layout": "Swiss.Poster", "widgets": {{}}, "parameters": {{}}}}}},
  {{"add": {{"id": "slide_002", "rank": 2, "state": "draft", "layout": "Bento.Standard", "widgets": {{}}, "parameters": {{}}}}}}
]

**Output Format**: Return a JSON array where each element is an object with an 'add' key.

**Output JSON Schema**:
{patch_schema}

**Example Output**:
[{{"add": {{"id": "slide_001", "rank": 1, "state": "draft", "layout": "Bento.Standard", "widgets": {{}}, "parameters": {{}}}}}}]"""


def _build_content_generation_system_prompt() -> str:
    """Build content generation system prompt dynamically from AssetManager.
    
    Returns:
        Complete system prompt for content generation step
    """
    strategies_list = _format_strategies_for_prompt()
    widgets_list = _format_widgets_for_prompt()
    presets_list = _format_presets_for_prompt()
    patch_schema = _get_patch_schema_for_replace()
    
    return f"""You are a presentation content designer transforming atoms into slides.

**CORE RULES**:
1. **Extreme brevity**: Display (1-6 words), Body (10-15 words), List bullets (3-7 words each, max 5)
2. **Preserve specifics**: Keep numbers ("38x/sec"), tech terms ("C++", "intrinsics"), years ("2011→2021")
3. **Use provided atoms only** - synthesize, don't hallucinate
4. **Merge atoms**: 3-6 atoms per slide, group by theme
5. **Slide limit**: 7-15 slides maximum (target 8-12)
6. **No duplication**: Each atom used exactly once
7. **Include header/footer** on every slide

**TEXT LENGTH BY WIDGET**:
- Display/Heading: 1-6 words (prefer 2-3)
- Body: 10-15 words max
- List bullets: 3-7 words, 3-5 bullets total
- Quote: 15-25 words max
- Caption: 3-5 words

**MARKDOWN FORMATTING**:
Use markdown syntax in widget text for emphasis:
- ==highlight== for key terms, metrics, technical names (will render with theme accent color background)
- **bold** for strong emphasis, important concepts (will render with theme accent color)
- Examples:
  - "Scale to ==1M requests/sec== with **zero downtime**"
  - "==C++ intrinsics== optimize performance **38x faster**"
  - "From ==2011== to ==2021==: **AI revolution**"

**ABSTRACTION EXAMPLES**:
- ❌ "This architecture provides better performance" → ✅ "Better Performance"
- ❌ "Significant Performance Improvement" → ✅ "==10x Faster=="
- ❌ "increased by" → ✅ "↑"
- ❌ Remove: "the", "a", "very", "really", "quite", "some", "many"

**LAYOUT SELECTION**:
- **1 hero point**: Swiss.Poster, Cinematic.FullBleed, Focus.Gradient
- **1 hero + 2-3 supporting**: Bento.HeroLeft, Bento.HeroTop, Cinematic.Split_30_70
- **4 equal points**: Bento.Quarter, Bento.Standard
- **Timeline/sequence**: Matrix.Timeline, Bento.VerticalStack, Edit.Timeline_3
- **Comparisons**: Data.Comparison_2Col, Type.Comparison widget with Bento layouts
- **Data-heavy**: Data.KPI_Row, Matrix.Grid, Data.Table_4x3

**NARRATIVE ARC** (structure slides as):
1. **Hook** (1-2 slides): Bold opener, problem statement
2. **Body** (5-8 slides): Evidence, concepts, how-to
3. **Climax** (1-2 slides): Results, vision, call-to-action

**PACING**: Alternate layout density - no 2+ dense slides (Bento.Standard, Data.KPI_Row, Benton.VerticalStack) in sequence. Mix with breathers (Swiss.Poster, Cinematic.FullBleed).

**ATOM MERGING** (mandatory):
- Group atoms by theme FIRST
- Select layout with enough slots for all atoms in group
- Synthesize content across widgets
- Example: 6 feature atoms → 1 Bento.Standard slide with 6 cells

**SPECIAL ATOMS**:
- QuoteAtom: Use Type.Quote widget with quote_text → text, speaker → attribution
- ActionItemAtom: Use Type.List with items formatted as "[State] Task - Assignee (Due)"
- TimelineAtom: Use Matrix.Timeline layout with events as stage titles/details

{strategies_list}

{widgets_list}

{presets_list}

**OUTPUT**: JSON array with add operations for draft slides (visual styling handled separately).

Example:
[
  {{"add": {{"id": "slide_001", "rank": 1, "state": "draft", "story": "Bold opener introducing the problem", "atoms": ["stmt_001", "stmt_002"], "density": "minimal", "layout": "", "widgets": {{}}, "parameters": {{}}}}}},
  {{"add": {{"id": "slide_002", "rank": 2, "state": "draft", "story": "Key evidence with data points", "atoms": ["metric_001", "stmt_003"], "density": "moderate", "layout": "", "widgets": {{}}, "parameters": {{}}}}}}
]

{patch_schema}"""


# Cache the built prompts (they're expensive to build with AssetManager calls)
STATE_TRANSITION_SYSTEM_PROMPT = _build_state_transition_system_prompt()
CONTENT_GENERATION_SYSTEM_PROMPT = _build_content_generation_system_prompt()


def render_state_transition_prompt(
    atoms: AtomCollection,
    user_instruction: str,
    intent_guidance: str = ""
) -> str:
    """Render user prompt for state transition step.
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions (e.g., "Create 5 slides")
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        Formatted user prompt string
        
    Raises:
        ValueError: If atoms is empty or instruction is empty
    """
    if len(atoms) == 0:
        raise ValueError("Cannot render prompt with empty atom collection")
    
    if not user_instruction or not user_instruction.strip():
        raise ValueError("User instruction cannot be empty")
    
    # Serialize atoms to JSON for LLM context (use to_json() for datetime handling)
    atoms_json = atoms.to_json(indent=2)
    
    user_prompt = f"""Create slides based on these atoms and instructions:

Atoms:
{atoms_json}

Instructions:
{user_instruction}
"""
    
    # Add intent guidance if provided
    if intent_guidance:
        user_prompt += f"""
Presentation Guidance (for context only):
{intent_guidance}

"""
    
    user_prompt += """
Output JSON Patch operations to initialize slides in "draft" state.
"""
    
    return user_prompt


def render_content_generation_prompt(
    draft_slides: Slides,
    atoms: AtomCollection,
    user_instruction: str,
    intent_guidance: str = ""
) -> str:
    """Render user prompt for content generation step.
    
    Args:
        draft_slides: Slides collection with slides in draft state
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        Formatted user prompt string
        
    Raises:
        ValueError: If slides is empty, slides not in draft state, or instruction empty
    """
    if len(draft_slides) == 0:
        raise ValueError("Cannot render prompt with empty slide collection")
    
    # Verify all slides are in draft state
    for slide in draft_slides.get_by_rank():
        if slide.state != "draft":
            raise ValueError(f"All slides must be in 'draft' state, but slide {slide.id} is in '{slide.state}' state")
    
    if not user_instruction or not user_instruction.strip():
        raise ValueError("User instruction cannot be empty")
    
    # Serialize draft slides and atoms to JSON (use to_json() for datetime handling)
    slides_json = json.dumps(draft_slides.to_dict(), indent=2)  # Slides doesn't have to_json() method
    atoms_json = atoms.to_json(indent=2)  # AtomCollection has custom to_json() with datetime support
    
    user_prompt = f"""Populate content for these draft slides using atoms:

Current Slides (Draft State):
{slides_json}

Atoms:
{atoms_json}

Instructions:
{user_instruction}
"""
    
    # Add intent guidance if provided
    if intent_guidance:
        user_prompt += f"""
Content Generation Guidance:
{intent_guidance}

Ensure the content aligns with the recommended tone, audience, and presentation style.

"""
    
    user_prompt += """
Output JSON Patch operations to:
1. Populate all widget content (use "replace" on "/contexts/<slide_id>/widgets")
2. Add header/footer if appropriate (use "replace" to include "header" and "footer" fields)
3. Set state to "active" (use "replace" on "/contexts/<slide_id>/state")

Example with header/footer:
{
  "replace": {
    "id": "slide_001",
    "rank": 0,
    "state": "active",
    "strategy": "Bento.Standard",
    "widgets": {...},
    "header": {"type": "Type.Heading", "parameters": {"text": "Career Growth Guide"}, "preset": {"surface": "Flat"}},
    "footer": {"type": "Type.Caption", "parameters": {"text": "© 2025"}, "preset": {"surface": "Flat"}},
    "parameters": {}
  }
}
"""
    
    return user_prompt


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
- layout: Layout strategy name (e.g., "Bento.HeroLeft", "Matrix.Timeline")
- widgets: Object mapping slot roles to widget configurations
  **CRITICAL**: Only use slot roles that exist in the chosen layout strategy!
  Example: Bento.HeroLeft has slots: hero, side_1, side_2, side_3, side_4
  Do NOT invent slot names like "supporting", "main", "content" unless they exist in the strategy!
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
        "layout": "Bento.HeroLeft",
        "widgets": {
          "hero": {
            "type": "Type.Display",
            "parameters": {"text": "Updated Title"},
            "preset": {"surface": "Flat", "shape": "Sharp", "fill": "Solid_Brand"}
          }
        },
        "header": {},
        "footer": {},
        "parameters": {}
      }
    }
  ]
}

CRITICAL: Widget objects should ONLY contain "type", "parameters", and optionally "preset".
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


def get_state_transition_config() -> GenerationConfig:
    """Get GenerationConfig for state transition step.
    
    Returns:
        GenerationConfig with appropriate parameters for structure generation
    """
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo')
    return GenerationConfig(
        model=deployment,
        temperature=0.2,  # Low temperature for deterministic structure
        max_tokens=16000,  # High limit for reasoning models (gpt-5.1 uses ~2000 reasoning + output)
        system_prompt=STATE_TRANSITION_SYSTEM_PROMPT,
        user_prompt_template=""  # Will be rendered by render_state_transition_prompt
    )


def get_content_generation_config() -> GenerationConfig:
    """Get GenerationConfig for content generation step.
    
    Returns:
        GenerationConfig with appropriate parameters for content generation
    """
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo')
    return GenerationConfig(
        model=deployment,
        temperature=0.7,  # Higher temperature for creative content
        max_tokens=32000,  # High limit for reasoning models + widget content + headers/footers
        system_prompt=CONTENT_GENERATION_SYSTEM_PROMPT,
        user_prompt_template=""  # Will be rendered by render_content_generation_prompt
    )


# ========== New Three-Phase Generation System ==========

def get_storyline_config() -> GenerationConfig:
    """Get GenerationConfig for storyline generation step.
    
    Returns:
        GenerationConfig with appropriate parameters for storyline creation
    """
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo')
    return GenerationConfig(
        model=deployment,
        temperature=0.3,  # Low-medium temperature for coherent narrative structure
        max_tokens=16000,  # Enough for theme/preset + draft slides with stories
        system_prompt=_build_storyline_system_prompt(),
        user_prompt_template=""  # Will be rendered by render_storyline_prompt
    )


def get_slide_generation_config() -> GenerationConfig:
    """Get GenerationConfig for individual slide generation step.
    
    Returns:
        GenerationConfig with appropriate parameters for single slide content
    """
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo')
    return GenerationConfig(
        model=deployment,
        temperature=0.7,  # Higher temperature for creative widget content
        max_tokens=8000,  # Per-slide generation, smaller context
        system_prompt=_build_slide_generation_system_prompt(),
        user_prompt_template=""  # Will be rendered by render_slide_generation_prompt
    )


def _build_storyline_system_prompt() -> str:
    """Build storyline generation system prompt.
    
    Returns:
        Complete system prompt for storyline step
    """
    # Custom patch schema for storyline (add operations only for draft slides)
    storyline_patch_schema = """{
  "type": "array",
  "description": "Array of add operations for draft slides with story and atom references",
  "items": {
    "type": "object",
    "properties": {
      "add": {
        "type": "object",
        "description": "Add draft slide with story, atom references, and density level",
        "properties": {
          "id": {"type": "string", "description": "Unique slide identifier"},
          "rank": {"type": "integer", "description": "Slide order position (1-based)"},
          "state": {"type": "string", "enum": ["draft"], "description": "Must be 'draft'"},
          "story": {"type": "string", "description": "1-2 sentence narrative description of slide's purpose"},
          "atoms": {"type": "array", "items": {"type": "string"}, "description": "List of atom IDs relevant to this slide"},
          "density": {"type": "string", "enum": ["minimal", "moderate", "dense"], "description": "Information density: minimal (1-2 key points), moderate (3-4 points), dense (5+ points)"}
        },
        "required": ["id", "rank", "state", "story", "atoms", "density"]
      }
    },
    "required": ["add"]
  }
}"""
    
    return f"""You are a presentation storyteller specializing in narrative structure and content flow.

**YOUR TASK**: Create a compelling storyline with 7-12 draft slides that tells a cohesive story.

**STORYTELLING FIRST**:
- Focus on narrative arc: opening hook → body progression → closing synthesis
- Each slide should advance the story, not just dump information
- Use atoms selectively to support the narrative—NOT every atom needs a slide
- It's better to leave atoms unused than to force weak slide connections

**CRITICAL RULES**:
1. **NO DUPLICATE ATOMS**: Each atom can only appear in ONE slide's atoms array (scan and verify before submitting)
2. **Story quality over atom coverage**: Skip atoms that don't fit the narrative flow
3. Draft slides need: id, rank, state="draft", story (1-2 sentences), atoms (2-5 atom IDs), density ("minimal"/"moderate"/"dense")

**DENSITY ASSIGNMENT**:
Assign information density based on slide's narrative role:
- **minimal**: Opening/closing slides, transitions, conceptual intros (1-2 key points)
  - Use for: Setup slides, philosophical points, call-to-action conclusions
  - Example: "AI landscape shift" (single timeline), "What this means for you" (1 takeaway)
- **moderate**: Main content slides with focused narrative (3-4 points)
  - Use for: Most slides—allows depth without overwhelming (DEFAULT CHOICE)
  - Example: "Three key patterns in LLM work" (3 patterns), "Trade-offs in system design" (4 comparisons)
- **dense**: Technical deep-dives requiring 5-6 distinct points (USE VERY RARELY)
  - Use sparingly: Only when complexity is absolutely essential and cannot be split
  - Example: "Complete step-by-step debugging workflow", "All 6 optimization techniques compared"
  - WARNING: Dense slides fatigue audiences—prefer splitting content across 2 moderate slides

**DENSITY DEFAULTS**:
- Opening/closing slides: **minimal**
- Transition/conceptual slides: **minimal**
- Content slides: **moderate** (preferred for 80-90% of presentation)
- Comprehensive references/procedures: **dense** (max 1-2 slides per presentation)
- NEVER use consecutive dense slides—always interleave with minimal/moderate

**NARRATIVE ARC REQUIREMENT**:
Structure slides following classic storytelling patterns:
- **Setup** (1-2 slides): Context, historical background, problem statement
- **Development** (3-5 slides): Key concepts, transitions, tensions
- **Resolution** (2-4 slides): Solutions, actionable takeaways, future outlook

Each slide should answer: "Why does this come NOW in the story?"
Avoid: Random topic jumping, encyclopedic coverage without through-line

**AUDIENCE ANCHORING**:
For each slide, connect content to target audience level:
- Entry-level: Focus on "what" and "why", avoid assuming prior context
- Mid-level: Emphasize "how" and system thinking
- Senior: Strategic implications, trade-offs, organizational impact
Add footer callouts that translate slide content to audience-specific action.

**ATOM ALLOCATION**:
- Assign each atom to its MOST impactful slide only
- If a concept spans slides, write it in story text—don't reuse atoms
- TimelineAtom: Use once in opening for chronological context
- Typical: 2-5 atoms per slide, grouped thematically

**SLIDE SEQUENCING**:
Each slide should build on previous context. Check:
1. Does this slide assume knowledge from prior slides?
2. Does it introduce new concepts that later slides reference?
3. Could I reorder without breaking narrative logic?
If slide N can be removed or moved without breaking flow → reconsider inclusion.

**NARRATIVE QUALITY CHECKLIST**:
Before finalizing storyline, verify:
1. ✓ Clear story arc: Setup → Development → Resolution
2. ✓ Each slide has narrative purpose (not just topic coverage)
3. ✓ Audience-appropriate depth and examples
4. ✓ Smooth transitions between slides (no jarring topic jumps)
5. ✓ Footer callouts connect slides to audience actions
6. ✓ Technical specifics preserved (numbers, terms, tools)
7. ✓ Layout choices will reinforce narrative structure (plan ahead)

**NO DUPLICATE ATOMS - FINAL VALIDATION**:
Scan all "atoms" arrays—is any ID repeated? If yes, REVISE IMMEDIATELY.

**OUTPUT FORMAT**: JSON array of add operations only: [{{"add": {{"id", "rank", "state", "story", "atoms", "density"}}}}]
**DO NOT generate set_theme or set_preset operations - visual styling is handled separately.**

{storyline_patch_schema}
"""


def _build_slide_generation_system_prompt() -> str:
    """Build individual slide generation system prompt.
    
    Returns:
        Complete system prompt for slide generation step
    """
    strategies_list = _format_strategies_for_prompt()
    widgets_list = _format_widgets_for_prompt()
    presets_list = _format_presets_for_prompt()
    patch_schema = _get_patch_schema_for_replace()
    
    return f"""You are a slide content designer specializing in layout selection and widget population.

Your task: Transform a draft slide (with story + atoms) into an active slide with layout and widgets.

**CORE RULES**:
1. Follow the story (your guide to what this slide should communicate)
2. Use ONLY provided atoms (don't hallucinate content)
3. Preserve technical specifics: numbers ("38x/sec"), tech names ("C++", "intrinsics"), years ("2011→2021"), jargon
4. Extreme brevity: Display (1-6 words), Body (10-15 words), List bullets (3-7 words)
5. Match layout to atom count & story tone
6. **RESPECT DENSITY LEVEL**: Follow target density specified in draft slide

**DENSITY-AWARE CONTENT GENERATION**:
Adjust content amount and layout complexity based on slide's density level:
- **minimal** (1-2 key points):
  - Use simple layouts: Bento.Standard (1-2 widgets), Swiss.Poster, Cinematic.Split5050
  - Limit to 2-3 widgets maximum
  - List widgets: MAX 2 items
  - Focus on single concept or transition
  - Example: Display widget + 1 body text, or 1 comparison with 2 items each side
  
- **moderate** (3-4 points):
  - Standard layouts work well: Bento.Standard (3-4 widgets), Swiss.Asymmetry, Cinematic.FullBleed
  - Use 3-5 widgets
  - List widgets: MAX 4 items per list
  - This is the default—most slides should use moderate density
  - Example: Display + 2-3 body/list widgets, or comparison with 3-4 items
  
- **dense** (5-6 points MAX):
  - Complex layouts: Bento.Quarter (4 stages), Swiss.SplitTypo, vertical stacks
  - Use 5-7 widgets
  - List widgets: MAX 5-6 items per list (NEVER exceed 6)
  - Use ONLY when essential—dense slides are fatiguing
  - Example: Bento.Quarter with 4 list widgets (4-5 items each), or vertical stack with 6 sections
  - **HARD LIMIT**: Total information points across ALL widgets must stay under 8

**CRITICAL DENSITY RULES**:
- If slide has minimal density but many atoms → synthesize atoms into fewer, more powerful points
- If slide has dense density but few atoms → flag as mismatched, don't hallucinate content
- **NEVER create lists with >6 items** - this breaks readability even for "dense" slides
- If atoms require >6 points, prioritize the most impactful and drop the rest

**INFORMATION DENSITY vs CLARITY BALANCE**:
Target: 3-5 key points per slide, each substantive
- Prefer specific examples over generic statements ("38x/sec" not "frequently called")
- Use numbers, metrics, concrete scenarios from atoms
- Replace "important to know X" with "X enables Y, as shown in Z"
Avoid:
- Bullet lists with >6 items (indicates content should split across slides)
- Abstract concepts without grounding examples
- Redundant phrasing across widget text

**LAYOUT SELECTION - VISUAL-NARRATIVE ALIGNMENT**:
Choose layout that reinforces narrative structure, not just fits content:
- **Timeline layout**: Chronological progressions, career journeys, evolution (e.g., TimelineAtom)
- **Comparison layout**: Before/after, traditional vs modern, trade-offs (contrast atoms)
- **Bento grids**: Multi-faceted concepts, skill categories, parallel dimensions (4+ related atoms)
- **Vertical stack (Bento.VerticalStack)**: Simple sequential processes (max 3 S widgets OR 1 M + 1 S)

**CRITICAL SLOT ROLE VALIDATION** (violations cause render errors):
- ONLY use slot roles that exist in the chosen layout strategy
- Example: Bento.HeroLeft has slots: hero, side_1, side_2, side_3, side_4
- DO NOT invent slot names like "supporting", "main", "content" - check the Available Layout Strategies list
- Each strategy lists its exact slot roles - use ONLY those exact names
- Mismatch = immediate render failure with "Missing slot role" error

**CRITICAL WIDGET SIZE CONSTRAINTS** (violations cause render errors):
- Type.Comparison widget requires M or L slot → Use in hero, cell_1, main, focal, NOT in side_1/side_2/side_3/side_4
- Type.List, Type.Body, Type.Display work in any slot size (S, M, or L)
- Bento.HeroLeft side slots (side_1/side_2/side_3/side_4) are ALL size S → Can only fit Type.List, Type.Body, Type.Display, Type.Heading
- For comparison content in Bento.HeroLeft → Put Type.Comparison in 'hero' slot ONLY
- See layout schemas below for exact slot names and sizes

{strategies_list}

{widgets_list}

**CRITICAL - DO NOT CONFUSE LAYOUTS WITH WIDGETS**:
- Layout names (e.g., "Bento.VerticalStack", "Matrix.Timeline") go in the "layout" field
- Widget types (e.g., "Type.Display", "Type.List") go in the "widgets" object with type field
- NEVER use layout names as widget types (e.g., NO "Type.VerticalStack", NO "Type.Timeline")
- Valid widget types are ONLY those listed above in "Supported Widget Types"

**PRESET USAGE** (apply to each widget):
- surface: Flat (clean), Elevated (depth), Glass (modern), Outline (minimal)
- shape: Sharp (tech), Rounded (friendly), Pill (playful)
- fill: Solid_Brand (bold), Gradient_Linear (dynamic), Subtle (minimal)

**CONTENT SYNTHESIS**:
- Read story → extract key points from atoms → distribute across slots
- ✓ PRESERVE: "==38x/sec==", "==C++==", "==2011→2021==", "**planner-executor**"
- ✗ AVOID: "Frequently invoked", "over time", "optimized"
- Use ==highlight== for metrics, tech terms, years; **bold** for concepts, patterns

**OUTPUT**: Single replace operation: [{{"replace": {{"id", "rank", "state": "active", "layout", "widgets", "header", "footer", "parameters"}}}}]

{patch_schema}
"""


def render_storyline_prompt(
    atoms: AtomCollection,
    user_instruction: str,
    intent_guidance: str = ""
) -> str:
    """Render user prompt for storyline generation step.
    
    Args:
        atoms: AtomCollection with extracted content
        user_instruction: User's generation instructions
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        Formatted user prompt string
    """
    atoms_json = atoms.to_json(indent=2)
    
    user_prompt = f"""Create a storyline for the presentation based on these atoms:

**All Available Atoms**:
{atoms_json}

**User Instructions**:
{user_instruction}
"""
    
    if intent_guidance:
        user_prompt += f"""
**Presentation Guidance**:
{intent_guidance}

Use the theme/preset recommendations. Generate "set_theme" and "set_preset" FIRST.
"""
    
    user_prompt += """
Create 7-12 slides focusing on narrative flow. Not every atom needs to be used—prioritize story over coverage.
Each atom can only appear in ONE slide. Verify no duplicates before submitting.
"""
    
    return user_prompt


def render_slide_generation_prompt(
    draft_slide,
    related_atoms: dict,
    user_instruction: str,
    intent_guidance: str = ""
) -> str:
    """Render user prompt for individual slide generation step.
    
    Args:
        draft_slide: Draft slide with story and atoms defined
        related_atoms: Dict of {atom_id: Atom} for atoms referenced by this slide
        user_instruction: User's generation instructions
        intent_guidance: Optional guidance from intent detection
        
    Returns:
        Formatted user prompt string
    """
    from datetime import datetime
    
    # Format atoms for prompt with datetime handling
    def datetime_encoder(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
    
    atoms_text = json.dumps(
        [atom.model_dump() for atom in related_atoms.values()],
        indent=2,
        default=datetime_encoder
    )
    
    user_prompt = f"""Transform this draft slide into an active slide with layout and widgets:

**Draft Slide**:
- ID: {draft_slide.id}
- Rank: {draft_slide.rank}
- Story: {draft_slide.story}
- Density: {draft_slide.density} ({_get_density_description(draft_slide.density)})
- Atoms: {', '.join(draft_slide.atoms)}

**Related Atoms** (use ONLY these for content):
{atoms_text}

**User Instructions**:
{user_instruction}
"""
    
    if intent_guidance:
        user_prompt += f"""
**Presentation Guidance**:
{intent_guidance}
"""
    
    user_prompt += """
Generate a "replace" operation that:
1. Selects appropriate layout based on story, density, and atom count
2. Populates widgets respecting density constraints (minimal: 1-2 points, moderate: 3-4 points, dense: 5+ points)
3. Sets state to "active"
4. Includes header and footer
"""
    
    return user_prompt


def _get_density_description(density: str) -> str:
    """Get human-readable description of density level.
    
    Args:
        density: Density level ('minimal', 'moderate', 'dense')
        
    Returns:
        Description string
    """
    descriptions = {
        "minimal": "1-2 key points, simple layout",
        "moderate": "3-4 points, standard layout",
        "dense": "5+ points, complex layout"
    }
    return descriptions.get(density, "3-4 points, standard layout")
