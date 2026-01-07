"""Prompt templates for slide generation with LLM."""
import os
import json
from typing import Any, List, Dict

from src.generation.atom.collection import AtomCollection
from src.common.slides import Slides
from src.utils.generation_config import GenerationConfig


def get_slide_generation_config(project: str = "slidev") -> GenerationConfig:
    """Get GenerationConfig for slide generation."""
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo')
    return GenerationConfig(
        model=deployment,
        temperature=0.5,
        max_tokens=32000,
        system_prompt=_build_system_prompt(project),
        user_prompt_template=""
    )


def _build_system_prompt(project: str = "slidev") -> str:
    """Build system prompt with layout docs from engine."""
    from src.paged.layout.engine_registry import LayoutEngineRegistry
    
    engine_name = "react" if project in ("react-mdx", "react") else "slidev"
    try:
        engine = LayoutEngineRegistry.get_engine(engine_name)
    except KeyError:
        engine = LayoutEngineRegistry.get_active_engine()
    
    layout_docs = engine.get_layout_prompt()
    layout_constraints = engine.get_layout_constrain()

    return f"""You are a LAYOUT DESIGNER. Convert story drafts into MDX slides.

# CORE PRINCIPLE
Follow the draft slide's `story` and `visual_design` fields exactly:
- `story` defines WHAT to say (HEADLINE, NARRATIVE, EVIDENCE, TAKEAWAY)
- `visual_design` defines HOW to show it (layout + content approach)
- `density` defines HOW MUCH (sparse=focused, moderate=balanced, dense=detailed)

# DENSITY → ELEMENTS
| Density | Meaning | Blocks | Coverage |
|---------|---------|--------|----------|
| sparse | Single focus, supporting context | 2-3 blocks (hero + support) | 40-60% |
| moderate | Balanced multi-element | 4-5 blocks | 60-80% |
| dense | Detailed breakdown | 5-7 blocks | 70-90% |

# PAGE COVERAGE RULE (CRITICAL)
- **Every page must have ≥70% content coverage** (no large empty areas)
- Dense pages need 5+ elements filling the space
- NO GAPS: content should flow continuously, not leave holes
- If a layout has multiple slots, ALL slots must have substantial content

# CONTENT MAPPING
- HEADLINE → `<Heading>`
- NARRATIVE → `<Text variant="lead">` or `<SmartList>`
- EVIDENCE (numbers) → `<MetricGroup>`, `<BigNum>`, `<ChartBar>`
- EVIDENCE (branching graphs) → `<NetworkGraph>` with JSX children (Node, Edge, Group)
- EVIDENCE (linear flows) → `<ProcessStrip>` for A→B→C sequences
- TAKEAWAY → `<Callout>` or `<Text variant="caption">`

# VISUAL SELECTION
- Use NetworkGraph when visual_design mentions branching "architecture", "network", "org chart" (nodes connect to multiple targets)
- Use ProcessStrip for "flow", "pipeline", "sequence", "stages" (linear A→B→C)
- Use Chart when visual_design mentions "chart", "comparison", "trend"
- Default to Text/SmartList for narrative content
- Each slide should combine text AND visual, but one leads

# NO REDUNDANT CONTENT (CRITICAL)
- NEVER show the same data twice on a slide in different formats
- If Left has MetricGroup with "71% → 80%", Right should NOT have BigNum with same numbers
- Each element must add NEW information, not repeat what's already visible
- BAD: MetricGroup(71%, 80%) + BigNum(80%) ← REDUNDANT
- GOOD: MetricGroup(71%, 80%) + SmartList(key actions) ← COMPLEMENTARY

# SMARTLIST GROUPING RULE (CRITICAL)
- **NEVER place two SmartList components consecutively without a Heading between them**
- If you have related list items, combine them into ONE SmartList with all items in the items array
- A SmartList without a preceding Heading looks like orphaned content (no context)
- BAD: SmartList followed by another SmartList without Heading between them
- GOOD: Single SmartList with all related items combined in one items array
- If lists represent different topics, each MUST have its own Heading before it

# SPACE MANAGEMENT (70% MINIMUM COVERAGE)
- **EVERY PAGE must fill ≥70% of vertical space** with content
- Split layouts: BOTH sides need 4+ elements EACH (Heading + visual + text + support)
- Both sides of split must span similar vertical height (visual overlap)
- Dashboard/Stacked: ALL slots need content, no empty or sparse slots
- Never leave gaps/holes - content should flow continuously
- AVOID: sparse pages that look like work-in-progress
- If content is limited, use simpler layout (LayoutStacked) rather than leave gaps

{layout_docs}

{layout_constraints}"""


def render_slide_generation_prompt(
    atoms: AtomCollection = None,
    user_instruction: str = "",
    intent_guidance: str = "",
    themes: List[Dict[str, Any]] = None,
    use_content_field: bool = False
) -> str:
    """Render user prompt for slide generation.
    
    Args:
        atoms: AtomCollection (required unless use_content_field=True)
        user_instruction: User's instruction
        intent_guidance: Additional guidance
        themes: List of theme dicts
        use_content_field: If True, slide attributes use 'content' instead of 'atoms'
    """
    prompt = ""
    
    if atoms:
        atoms_json = atoms.to_json(indent=2)
        prompt = f"**Atoms**: {atoms_json}\n"
    
    prompt += f"**Instructions**: {user_instruction}\n"
    
    if intent_guidance:
        prompt += f"**Guidance**: {intent_guidance}\n"
    
    if themes:
        theme_ids = [t.get("id", "default") for t in themes]
        prompt += f"**Themes**: {', '.join(theme_ids)}\n"
    
    # Rule 6 changes based on whether using atoms or content field
    if use_content_field:
        rule_6 = "6. Each <Slide> has id, rank, story, content attributes. Use content.sections as REFERENCE for slide content—you may refactor, condense, or omit details to fit the layout beautifully. Prioritize visual balance over exhaustive coverage. Also consider content.headline, content.subtitle, content.category, and content.speaker_intent if present"
    else:
        rule_6 = "6. Each <Slide> has id, rank, story, atoms attributes"
    
    prompt += f"""
**RULES**:
1. Follow each slide's `visual_design` field for layout and content approach
2. Follow each slide's `density` field (sparse=2-3 blocks, moderate=3-4, dense=5+)
3. Each slide tells its own story from the `story` field
4. Use Diagram ONLY when visual_design explicitly mentions it
5. ≥4 different layouts across deck, no consecutive repeats
{rule_6}
7. Combine text AND visual on each slide (one leads, other supports)
8. Fill space appropriate to density (sparse≠empty)
9. **CONTENT FLEXIBILITY**: You may refactor, shorten, or selectively omit content details to achieve a clean, well-balanced layout. Visual appeal and readability trump exhaustive completeness.

Generate MDX slides wrapped in <Slide> elements."""
    
    return prompt


def render_refinement_prompt(
    active_slides: Slides,
    atoms: AtomCollection,
    user_instruction: str,
    validation_feedback: str,
    intent_guidance: str = ""
) -> str:
    """Render prompt for validation-based refinement using Patch format."""
    # Format slides with their MDX content
    slides_mdx = []
    for slide in active_slides.get_active_slides():
        slide_dict = slide.model_dump()
        mdx_content = slide_dict.get("mdx", "")
        slides_mdx.append(f"""<Slide id="{slide_dict['id']}" rank={{{slide_dict['rank']}}} story="{slide_dict.get('story', '')}">
{mdx_content}
</Slide>""")
    
    current_mdx = "\n\n".join(slides_mdx)
    atoms_json = atoms.to_json(indent=2)
    
    prompt = f"""Current Slides (MDX):
```mdx
{current_mdx}
```

Atoms:
{atoms_json}

Instructions: {user_instruction}
"""
    if intent_guidance:
        prompt += f"Guidance: {intent_guidance}\n"
    
    prompt += f"""
---
Validation Issues:
{validation_feedback}

Fix issues by outputting <Patch> elements. Each patch targets an element by id:

```mdx
<Patch id="stat_001">
  <BigNum value="95%" label="Fixed Value"/>
</Patch>
```

Output ONLY <Patch> elements for changes needed."""
    
    return prompt


def render_user_refinement_prompt(
    existing_slides: Slides,
    atoms: AtomCollection,
    refinement_instruction: str,
    intent_guidance: str = ""
) -> str:
    """Render prompt for user-requested refinement using Patch format."""
    # Format slides with their MDX content
    slides_mdx = []
    for slide in existing_slides.get_active_slides():
        slide_dict = slide.model_dump()
        mdx_content = slide_dict.get("mdx", "")
        slides_mdx.append(f"""<Slide id="{slide_dict['id']}" rank={{{slide_dict['rank']}}} story="{slide_dict.get('story', '')}">
{mdx_content}
</Slide>""")
    
    current_mdx = "\n\n".join(slides_mdx)
    atoms_json = atoms.to_json(indent=2)
    
    prompt = f"""Current Slides (MDX):
```mdx
{current_mdx}
```

Atoms:
{atoms_json}

Request: {refinement_instruction}
"""
    if intent_guidance:
        prompt += f"Guidance: {intent_guidance}\n"
    
    prompt += """
---
Output <Patch> elements to modify specific widgets by id:

```mdx
<Patch id="element_id">
  <NewComponent ...props/>
</Patch>
```

Only output patches for elements that need to change."""
    
    return prompt


def render_slide_refinement_prompt(
    existing_slides: List[Dict],
    atoms: Any,
    user_instruction: str,
    intent_guidance: str = "",
    themes: List = None
) -> str:
    """Render prompt for constitution-based refinement."""
    slides_summary = [{
        "id": s.get("id"),
        "rank": s.get("rank"),
        "layout": s.get("layout"),
        "slots": list(s.get("widgets", {}).keys()),
    } for s in existing_slides]
    
    prompt = f"""Slides: {json.dumps(slides_summary)}

Instruction: {user_instruction}
"""
    if intent_guidance:
        prompt += f"Rules: {intent_guidance}\n"
    
    prompt += f"""
Full data:
{json.dumps(existing_slides, indent=2)}

Return JSON array: replace/remove operations only."""
    
    return prompt
