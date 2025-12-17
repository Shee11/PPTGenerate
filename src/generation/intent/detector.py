"""Intent detection for user instructions to guide content generation.

This module interprets user instructions to:
1. Detect presentation intent and audience
2. Determine appropriate slide patterns
3. Guide atom extraction and content generation
4. Output stage-specific changes for conditional pipeline execution
"""
from typing import Optional, Dict, Any, List
from pathlib import Path
from pydantic import BaseModel, Field

from src.utils.llm_client import call_llm
from src.utils.generation_config import GenerationConfig
from src.utils.cache import GenerationCache


class SourceChange(BaseModel):
    """Represents a new source extracted from user instruction."""
    
    source_ref: str = Field(
        ...,
        description="Reference ID for this new source (e.g., 'user_provided_points', 'embedded_agenda')"
    )
    source_type: str = Field(
        ...,
        description="Type of source: 'user_instruction_embedded', 'external_reference', 'structured_input'"
    )
    content: str = Field(
        ...,
        description="Extracted content from user instruction to be used as a new source"
    )
    content_format: str = Field(
        default="text/plain",
        description="Format of content: 'text/plain', 'text/markdown', 'application/json'"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (e.g., {'origin': 'user_instruction', 'line_range': '1-5'})"
    )
    should_create: bool = Field(
        default=True,
        description="Whether this source should be created in the pipeline"
    )


class AtomExtractionTask(BaseModel):
    """Task specification for atom extraction from a specific source."""
    
    source_ref: str = Field(
        ...,
        description="Reference to the source (e.g., 'main_transcript', 'supplementary_doc_1', 'user_provided_points')"
    )
    source_summary: str = Field(
        ...,
        description="Brief summary of what this source contains (not full content)"
    )
    extraction_prompt: str = Field(
        ...,
        description="Specific extraction guidance for this source based on user intent"
    )
    priority: int = Field(
        default=1,
        description="Priority level (1=highest, 3=lowest). Higher priority sources processed first."
    )
    requires_source_creation: bool = Field(
        default=False,
        description="True if this task depends on a source from source_changes (user-provided content)"
    )


class StageChange(BaseModel):
    """Specification of changes needed for a specific generation stage."""
    
    stage_name: str = Field(
        ...,
        description="Name of the stage (atom_extraction, storyline, slide_generation, visual)"
    )
    should_execute: bool = Field(
        default=True,
        description="Whether this stage should execute (False to skip)"
    )
    guidance: str = Field(
        default="",
        description="Stage-specific guidance derived from user intent"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Stage-specific parameters (e.g., {'focus': 'learning', 'density': 'minimal'})"
    )


class VisualChange(BaseModel):
    """Specification of visual styling changes (theme, style, preset)."""
    
    should_generate: bool = Field(
        default=True,
        description="Whether to generate new visual styling"
    )
    visual_guidance: str = Field(
        default="",
        description="Guidance for visual generation (colors, typography, effects)"
    )
    tone: str = Field(
        default="professional",
        description="Visual tone (professional, casual, technical, creative, etc.)"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional visual parameters"
    )


class PresentationIntent(BaseModel):
    """Detected presentation intent from user instruction."""
    
    audience: str = Field(
        ...,
        description="Target audience (e.g., 'technical engineers', 'business executives', 'general public')"
    )
    purpose: str = Field(
        ...,
        description="Presentation purpose (e.g., 'educate', 'persuade', 'inform', 'entertain')"
    )
    pattern: str = Field(
        ...,
        description="Recommended slide pattern (e.g., 'story', 'tutorial', 'showcase', 'pitch', 'report')"
    )
    tone: str = Field(
        ...,
        description="Recommended tone (e.g., 'professional', 'casual', 'energetic', 'authoritative')"
    )
    visual_density: str = Field(
        ...,
        description="Visual density preference (e.g., 'minimal', 'balanced', 'rich')"
    )
    atom_extraction_guidance: str = Field(
        ...,
        description="Specific guidance for atom extraction based on intent"
    )
    content_generation_guidance: str = Field(
        ...,
        description="Specific guidance for content generation based on intent"
    )
    theme_guidance: str = Field(
        ...,
        description="Recommended theme colors and style (e.g., 'Dark tech theme with blue/orange accents' or 'Professional corporate with navy/gold')"
    )
    preset_guidance: str = Field(
        ...,
        description="Recommended preset style (e.g., 'TechTuber: Elevated+Rounded+Gradient+Glow' or 'Professional: Flat+Sharp+Solid')"
    )
    reasoning: str = Field(
        default="",
        description="Brief explanation of detected intent"
    )
    
    # New fields for stage-specific control
    source_changes: List[SourceChange] = Field(
        default_factory=list,
        description="New sources extracted from user instruction (e.g., embedded bullet points, agenda). These should be created before atom extraction."
    )
    atom_extraction_tasks: List[AtomExtractionTask] = Field(
        default_factory=list,
        description="List of atom extraction tasks with source-specific prompts. If empty, use default extraction. May include tasks for user-provided sources."
    )
    stage_changes: List[StageChange] = Field(
        default_factory=list,
        description="Stage-specific changes. Downstream stages consume these to conditionally execute or modify behavior."
    )
    visual_change: Optional[VisualChange] = Field(
        default=None,
        description="Visual styling change specification. If present, triggers visual generation (theme, style, preset)."
    )


def detect_intent(
    user_instruction: str,
    source_preview: str,
    source_refs: Optional[List[Dict[str, str]]] = None,
    existing_slides_summary: Optional[str] = None,
    config: Optional[GenerationConfig] = None,
    use_cache: bool = True
) -> PresentationIntent:
    """Detect presentation intent from user instruction and source content.
    
    Args:
        user_instruction: User's instructions for presentation generation
        source_preview: Brief abstract/summary of source content (NOT full content)
        source_refs: Optional list of source references with summaries.
                     Each dict should have: {'ref': 'source_id', 'summary': 'brief abstract'}
                     If provided, atom_extraction_tasks will be generated per source.
        existing_slides_summary: Optional summary of existing slides (id, rank, story) for refinement
        config: Optional LLM configuration (uses default if not provided)
        use_cache: Enable caching for LLM calls
        
    Returns:
        PresentationIntent with detected audience, purpose, guidance, and stage-specific changes
        
    Raises:
        ValueError: If user instruction is empty
        Exception: If LLM call fails
    """
    if not user_instruction or not user_instruction.strip():
        raise ValueError("User instruction cannot be empty")
    
    # Use default config if not provided
    if config is None:
        config = _get_intent_detection_config()
    
    # Build prompt
    system_prompt = _build_intent_detection_system_prompt()
    user_prompt = _build_intent_detection_user_prompt(user_instruction, source_preview, source_refs, existing_slides_summary)
    
    # Setup cache
    cache = GenerationCache(Path(".cache/intent"))
    cache_key = None
    
    if use_cache:
        cache_key = cache.hash_key(system_prompt, user_prompt)
        cached_data = cache.load(cache_key)
        
        if cached_data is not None:
            print(f"✓ Using cached intent detection")
            import json
            return PresentationIntent.model_validate(cached_data["intent"])
    
    # Cache miss or cache disabled - call LLM
    print(f"⚙ Detecting presentation intent via LLM...")
    
    # Call LLM
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        deployment=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        max_reasoning_tokens=config.max_reasoning_tokens
    )
    
    # Parse response as JSON
    import json
    try:
        intent_data = json.loads(response)
        intent = PresentationIntent.model_validate(intent_data)
        
        # Save to cache if enabled
        if use_cache and cache_key is not None:
            cache.save(cache_key, {"intent": intent_data})
        
        return intent
    except (json.JSONDecodeError, ValueError) as e:
        raise Exception(f"Failed to parse intent detection response: {e}\nResponse: {response}")


def _build_intent_detection_system_prompt() -> str:
    """Build system prompt for intent detection.
    
    Returns:
        System prompt string
    """
    return """You are a presentation design consultant specializing in audience analysis and content strategy.

Your task: Analyze user instructions and source content to detect:
1. Target audience and their needs
2. Presentation purpose and desired outcome
3. Optimal slide pattern for content delivery
4. Appropriate tone and visual style
5. Specific guidance for atom extraction and content generation

**Common Slide Patterns**:

1. **Story Pattern** (Narrative flow)
   - Audience: General public, stakeholders
   - Best for: Career journeys, product evolution, case studies
   - Structure: Beginning → Journey → Climax → Resolution
   - Visual: Hero images, timeline layouts, emotional moments

2. **Tutorial Pattern** (Step-by-step learning)
   - Audience: Technical users, learners
   - Best for: How-to guides, feature demos, training
   - Structure: Overview → Steps → Practice → Summary
   - Visual: Clear headings, numbered steps, code snippets

3. **Showcase Pattern** (Feature highlights)
   - Audience: Product users, decision makers
   - Best for: Product launches, feature announcements
   - Structure: Problem → Solution → Benefits → Call-to-action
   - Visual: Big visuals, metrics, comparison tables

4. **Pitch Pattern** (Persuasion)
   - Audience: Investors, executives
   - Best for: Fundraising, proposals, sales
   - Structure: Hook → Problem → Solution → Traction → Ask
   - Visual: Bold statements, key metrics, competitive advantages

5. **Report Pattern** (Data-driven insights)
   - Audience: Analysts, managers
   - Best for: Analytics, research findings, status updates
   - Structure: Summary → Methodology → Findings → Recommendations
   - Visual: Charts, tables, KPIs, trends

6. **TechTuber Pattern** (Energetic walkthrough)
   - Audience: Tech enthusiasts, developers
   - Best for: Tech reviews, tutorials, breakdowns
   - Structure: Hook → Overview → Deep dive → Key takeaways
   - Visual: Dynamic layouts, code snippets, callouts, personality

**Content Focus Detection** - CRITICAL:
Determine if the presentation should focus on:
- **Learning/Takeaways**: What the audience should learn, actionable insights, skills to develop
  - Example: "Career talk for mid-level engineers" → Focus on lessons learned, career paths, skills to develop
  - NOT the speaker's personal story, but what others can LEARN from it
- **Personal Story**: The speaker's journey, experiences, achievements
  - Only when explicitly requested or for inspirational/motivational purposes

For LEARNING-focused content:
- Extract actionable insights, not narrative details
- Focus on "what to learn" not "what happened"
- Emphasize skills, principles, and takeaways
- Minimize biographical details unless they illustrate a lesson

**Audience-First Principles**:
- **Technical engineers**: Precision, details, code examples, architecture diagrams, **actionable skills**
- **Business executives**: ROI, strategic impact, high-level insights, metrics
- **General public**: Clarity, simplicity, relatable examples, minimal jargon
- **Designers**: Visual hierarchy, aesthetics, creative freedom
- **Educators**: Structured learning, progressive complexity, exercises

**Tone Guidelines**:
- **Professional**: Formal language, conservative visuals, structured flow
- **Casual**: Conversational tone, friendly visuals, flexible structure
- **Energetic**: Bold statements, dynamic layouts, engaging hooks
- **Authoritative**: Data-driven, research-backed, credible sources

**Visual Density**:
- **Minimal**: One key idea per slide, lots of whitespace, Swiss/Cinematic strategies
- **Balanced**: 2-3 ideas per slide, moderate content, Bento strategies
- **Rich**: Multiple data points, detailed info, Data/Edit strategies

**Theme & Preset Recommendations**:
Based on audience, tone, and pattern, recommend:
- **Theme**: Color palette and branding (e.g., "Dark tech: #0a0a0a bg, #0066ff primary, #ff4400 accent, #ffffff text")
- **Preset**: Visual style combination (surface+shape+fill+effect)
  - **TechTuber**: Elevated + Rounded + Gradient_Linear + Glow (energetic, modern)
  - **Professional**: Flat + Sharp + Solid_Brand + (no effect) (clean, corporate)
  - **Creative**: Glass + Organic + Gradient_Mesh + Duotone (artistic, expressive)

**Stage-Specific Changes** (NEW):
Based on user intent, determine what changes each pipeline stage needs:

1. **atom_extraction Stage**:
   - should_execute: true ONLY if this is initial generation OR user explicitly requests new content extraction
   - For refinements: default to false (reuse existing atoms) unless explicitly needed
   - guidance: What to focus on extracting (e.g., "Focus on actionable lessons, not biographical details")
   - parameters: {"focus": "learning|narrative|data", "granularity": "high|medium|low"}
   - Set to false for: visual-only changes, refinements without new content, layout-only changes

2. **storyline Stage**:
   - should_execute: true (generate storyline) or false (skip if simple linear flow OR visual-only change)
   - guidance: How to structure the narrative arc
   - parameters: {"pattern": "story|tutorial|showcase|pitch|report", "arc": "hero|problem-solution|chronological"}
   - Set to false for: visual-only changes, minor refinements that don't change story

3. **slide_generation Stage**:
   - should_execute: true (always needed) or false (visual-only change)
   - guidance: Content generation strategy
   - parameters: {"density": "minimal|moderate|dense", "emphasis": "visual|text|data"}
   - Set to false for: visual-only changes that don't modify slide content

4. **theme Stage**:
   - should_execute: true (generate custom theme) or false (use default)
   - guidance: Theme requirements from user
   - parameters: {"palette": "dark|light|colorful", "brand_colors": ["#hex1", "#hex2"]}

5. **preset Stage**:
   - should_execute: true (generate custom preset) or false (use default)
   - guidance: Visual style requirements
   - parameters: {"surface": "flat|elevated|glass", "shape": "sharp|rounded|organic", "fill": "solid|gradient", "effect": "none|glow|duotone"}

**Source Changes** (NEW - CRITICAL):
Detect if user instruction contains EMBEDDED CONTENT that should become new sources:

**Common Patterns to Detect**:
1. **Explicit Lists/Points**: "Create slides about: 1) AI safety, 2) Ethics, 3) Regulation"
2. **Structured Agenda**: "Cover these topics: Introduction, Problem, Solution, Demo"
3. **Inline Data**: "Show Q1: $2M, Q2: $3.5M, Q3: $4.1M, Q4: $5M"
4. **Direct Content**: "Include this quote: 'Innovation distinguishes...'"
5. **Requirements List**: "Must include: team structure, roadmap, budget"

**When to Create source_changes**:
- User provides structured content directly in instruction (not just describing what they want)
- Content is concrete/specific enough to extract atoms from
- Content is separate from the style/tone/audience guidance

**When NOT to Create source_changes** (CRITICAL):
- Visual/styling instructions only: "change to dark theme", "make it colorful", "use rounded corners"
- General refinement instructions: "make it more technical", "simplify for beginners"
- Layout/structure changes: "use different layouts", "make slides shorter"
- Tone/style changes: "be more casual", "add humor"
- These should set visual_change and stage_changes, but NOT create source_changes

**Example source_change**:
```json
{
  "source_ref": "user_provided_topics",
  "source_type": "user_instruction_embedded",
  "content": "1. AI Safety - ensuring systems behave as intended\n2. Ethics - moral implications of AI\n3. Regulation - government oversight",
  "content_format": "text/plain",
  "metadata": {"origin": "user_instruction", "extraction_type": "explicit_list"},
  "should_create": true
}
```

**Atom Extraction Tasks** (NEW - CRITICAL):
For EVERY source, create an extraction task:

1. **Original source** (from source_refs parameter):
   - Always create task with requires_source_creation=false
   - Use source_ref from source_refs list
   - Even if user provides embedded content, still extract from original source

2. **User-provided sources** (from source_changes you detected):
   - Create task with requires_source_creation=true
   - Use source_ref matching the source_change.source_ref
   - Higher priority (1) than original source if user explicitly provided content

**Priority Guidelines**:
- User-provided content (from instruction): priority 1 (they explicitly told you what to include)
- Main source file: priority 1 or 2 (depending on if it complements user content)
- Supplementary sources: priority 2 or 3

**Example Scenario**:
User instruction: "Create slides about: 1) AI Safety, 2) Ethics. Use professional tone."
Source: transcript about AI developments

You should create:
```json
[
  {
    "source_ref": "user_provided_topics",
    "source_summary": "Two explicit topics from user: AI Safety and Ethics",
    "extraction_prompt": "Extract atoms for each topic. Create heading and body atoms for: 1) AI Safety - systems behaving as intended, 2) Ethics - moral implications. Treat as distinct concepts.",
    "priority": 1,
    "requires_source_creation": true
  },
  {
    "source_ref": "source_transcript",
    "source_summary": "Transcript about AI developments (from source file)",
    "extraction_prompt": "Extract supporting details, examples, and context that relate to AI Safety and Ethics topics. Focus on concrete examples and real-world implications.",
    "priority": 2,
    "requires_source_creation": false
  }
]
```

For each task:
- source_ref: ID of the source
- source_summary: What the source contains
- extraction_prompt: Source-specific extraction guidance based on user intent
- priority: 1 (critical), 2 (important), 3 (optional)
- requires_source_creation: true if from source_changes, false if from source_refs

For each task:
- source_ref: ID of the source (e.g., "main_transcript", "user_provided_topics")
- source_summary: What the source contains
- extraction_prompt: Source-specific extraction guidance based on user intent
- priority: 1 (critical), 2 (important), 3 (optional)
- requires_source_creation: true if task depends on a source_change, false for existing sources

Example with user-provided source:
```json
{
  "source_ref": "user_provided_topics",
  "source_summary": "Three main topics from user: AI Safety, Ethics, Regulation",
  "extraction_prompt": "Extract atoms for each topic. For each: create heading atom, body atom explaining the concept, and any examples/implications mentioned. Treat each numbered item as a distinct concept.",
  "priority": 1,
  "requires_source_creation": true
}
```

**Output Format**: Return a JSON object with these fields:
{
  "audience": "string - target audience",
  "purpose": "string - presentation purpose",
  "pattern": "string - recommended slide pattern (story/tutorial/showcase/pitch/report/techtuber)",
  "tone": "string - recommended tone",
  "visual_density": "string - visual density (minimal/balanced/rich)",
  "atom_extraction_guidance": "string - specific guidance for atom extractor. CRITICAL: specify if focus should be on learning/takeaways vs. personal narrative. For career talks, focus on 'what to learn' not 'what the speaker did'.",
  "content_generation_guidance": "string - specific guidance for content generator. CRITICAL: emphasize extracting actionable lessons and skills, not biographical timeline.",
  "theme_guidance": "string - recommended theme (describe colors and style, e.g., 'Dark tech with blue/orange accents' or 'Professional corporate navy/gold')",
  "preset_guidance": "string - recommended preset style (e.g., 'TechTuber: Elevated+Rounded+Gradient+Glow' or 'Professional: Flat+Sharp+Solid')",
  "reasoning": "string - brief explanation (2-3 sentences)",
  "source_changes": [
    {
      "source_ref": "string - ID for new source (e.g., 'user_provided_topics')",
      "source_type": "user_instruction_embedded|external_reference|structured_input",
      "content": "string - extracted content from user instruction",
      "content_format": "text/plain|text/markdown|application/json",
      "metadata": {"origin": "user_instruction", ...},
      "should_create": true|false
    }
  ],
  "atom_extraction_tasks": [
    {
      "source_ref": "string - source ID (existing or from source_changes)",
      "source_summary": "string - brief summary",
      "extraction_prompt": "string - source-specific extraction guidance",
      "priority": 1-3,
      "requires_source_creation": true|false
    }
  ],
  "stage_changes": [
    {
      "stage_name": "atom_extraction|storyline|slide_generation",
      "should_execute": true|false,
      "guidance": "string - stage-specific guidance",
      "parameters": {"key": "value"}
    }
  ],
  "visual_change": {
    "should_generate": true|false,
    "visual_guidance": "string - ONLY if should_generate=true, combine theme_guidance and preset_guidance into comprehensive visual instructions. Example: 'Dark tech theme: #0a0a0a bg, #0066ff primary, #ff4400 accent. Use Elevated+Rounded+Gradient_Linear+Glow for modern energetic feel.'",
    "tone": "string - ONLY if should_generate=true, visual tone (professional/casual/energetic/technical/creative)",
    "parameters": {}
  }
}

**EXAMPLE - Visual-only instruction:**
User: "change to green theme"
{
  "source_changes": [],
  "stage_changes": [
    {"stage_name": "atom_extraction", "should_execute": false},
    {"stage_name": "storyline", "should_execute": false},
    {"stage_name": "slide_generation", "should_execute": false}
  ],
  "visual_change": {
    "should_generate": true,
    "visual_guidance": "Green theme: Use green as primary color #00aa00, with dark bg #0f0f0f",
    "tone": "professional"
  }
}

**CRITICAL - visual_change field**:
- ALWAYS include visual_change in your output
- Set should_generate=true to trigger custom visual generation
- Combine theme_guidance and preset_guidance into detailed visual_guidance
- visual_guidance should include: color palette (hex codes), surface style, shape, fill, effects
- Default should_generate to true unless user explicitly wants default styling"""


def _build_intent_detection_user_prompt(
    user_instruction: str, 
    source_preview: str, 
    source_refs: Optional[List[Dict[str, str]]] = None,
    existing_slides_summary: Optional[str] = None
) -> str:
    """Build user prompt for intent detection.
    
    Args:
        user_instruction: User's instructions
        source_preview: Brief abstract/summary of source (NOT full content)
        source_refs: Optional list of source references with summaries
        existing_slides_summary: Optional summary of existing slides for refinement
        
    Returns:
        User prompt string
    """
    # Build source references section
    source_refs_text = ""
    if source_refs and len(source_refs) > 0:
        source_refs_text = "\n\n**Available Sources**:\n"
        for i, src in enumerate(source_refs, 1):
            ref = src.get('ref', f'source_{i}')
            summary = src.get('summary', 'No summary provided')
            source_refs_text += f"{i}. **{ref}**: {summary}\n"
        source_refs_text += "\nGenerate atom_extraction_tasks for each source with appropriate extraction guidance.\n"
    else:
        source_refs_text = "\n\n**Note**: Single source provided. Leave atom_extraction_tasks as empty array [].\n"
    
    # Build existing slides context if provided
    slides_context = ""
    if existing_slides_summary:
        slides_context = f"""

**Existing Slides** (for refinement):
{existing_slides_summary}
"""
    
    return f"""Analyze this presentation request and detect the optimal approach:

**User Instruction**:
{user_instruction}

**Source Content Summary** (abstract only, NOT full content):
{source_preview}{slides_context}{source_refs_text}

Based on the instruction and content, determine:
1. **CRITICAL - Check if this is a VISUAL-ONLY or STYLE-ONLY instruction**:
   - Visual/theme changes: "change to dark/green/blue theme", "make it colorful", "use rounded corners"
   - If YES: Set source_changes=[], ALL stage_changes.should_execute=false (including atom_extraction), visual_change.should_generate=true
   - If NO visual request: Set visual_change.should_generate=false (reuse cached visual)
   - If YES: Skip questions 3-10 below, just set visual_change and return
   
2. **CRITICAL - Check if atoms need to be extracted**:
   - If this is a REFINEMENT (existing slides provided): Default atom_extraction.should_execute=false (reuse cached atoms)
   - Only set atom_extraction.should_execute=true if user explicitly requests new content extraction
   - If this is INITIAL GENERATION (no existing slides): Set atom_extraction.should_execute=true
   
3. **CRITICAL**: Does the user instruction contain EMBEDDED CONTENT (lists, topics, data, quotes, requirements)?
   - If YES: Extract to source_changes with appropriate content and metadata
   - Create atom_extraction_tasks with requires_source_creation=true for these sources
   - If NO and not visual-only: Set source_changes=[]
   
4. Who is the target audience? (Consider their expertise, needs, and preferences)
4. What is the main purpose? (Educate, persuade, inform, entertain?)
5. Which slide pattern fits best? (Story, tutorial, showcase, pitch, report, techtuber)
6. What tone should we use? (Professional, casual, energetic, authoritative)
7. What visual density is appropriate? (Minimal, balanced, rich)
8. What should the atom extractor focus on? (Key concepts, technical details, metrics, quotes?)
9. How should content be generated? (Narrative flow, logical steps, data-driven, emotional appeal?)
10. What changes are needed for each pipeline stage? (Provide stage_changes for content stages)
11. Create atom_extraction_tasks for:
    - Existing sources (from source_refs) with requires_source_creation=false
    - User-provided sources (from source_changes) with requires_source_creation=true

**IMPORTANT - Pattern Detection**:
- **Visual/Style Instructions**: "change theme", "make it colorful", "use different colors"
  → source_changes=[], stage_changes all false, visual_change.should_generate=true
  
- **Embedded Content**: Numbered/bulleted lists, "Include these topics", "Show this data", "Cover: A, B, C"
  → Create source_changes, atom_extraction_tasks with requires_source_creation=true
  
- **General Refinements**: "make it more technical", "simplify", "add examples"
  → source_changes=[], stage_changes as appropriate, may include visual_change

Return the analysis as JSON following the schema above."""


def _get_intent_detection_config() -> GenerationConfig:
    """Get default configuration for intent detection.
    
    Returns:
        GenerationConfig with defaults for intent detection
    """
    import os
    
    return GenerationConfig(
        model=os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo'),
        system_prompt="",  # Set dynamically
        user_prompt_template="",  # Set dynamically
        temperature=0.3,  # Lower temperature for consistent intent detection
        max_tokens=3000  # Increased for stage_changes and atom_extraction_tasks
    )
