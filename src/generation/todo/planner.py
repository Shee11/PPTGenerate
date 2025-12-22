"""Todo-based pipeline planner.

Converts user instruction + current state into a TodoQueue.

Architecture:
    todos = planner(state, user_instruction)
    for todo in todos:
        patch = executor.do(todo)
        state.apply(patch)

The planner is pure function - it doesn't modify state, just produces todos.

Intent parsing is built into the planner (no separate module, no LLM).
"""
from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING, Optional, List
from pathlib import Path
from pydantic import BaseModel, Field

from src.generation.todo.models import (
    TodoItem, TodoQueue, TodoType, TodoStatus,
    ConstitutionPatch, AtomsParams, ThemeParams, ContentParams, ExportParams
)

if TYPE_CHECKING:
    from src.generation.state import PipelineState


# =============================================================================
# INTENT MODELS (built into planner, no separate module)
# =============================================================================

class IntentAction(str, Enum):
    """What the user wants to do."""
    CREATE = "create"        # New presentation
    REFINE = "refine"        # Modify existing
    REGENERATE = "regenerate"  # Start over


class ToneStyle(str, Enum):
    """Presentation tone."""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    ACADEMIC = "academic"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    MARKETING = "marketing"
    MINIMAL = "minimal"
    NEUTRAL = "neutral"


class ParsedIntent(BaseModel):
    """Parsed intent from user instruction (no LLM, pattern matching only)."""
    action: IntentAction = IntentAction.CREATE
    tone_style: Optional[ToneStyle] = None
    slide_count: Optional[int] = None
    density: Optional[str] = None  # sparse, normal, dense
    theme_id: Optional[str] = None
    color_keywords: List[str] = Field(default_factory=list)
    layout_constraints: Optional[List[str]] = None
    forbidden_layouts: Optional[List[str]] = None


def parse_intent(user_instruction: str) -> ParsedIntent:
    """Parse intent from user instruction using pattern matching (NO LLM).
    
    This is a simple, fast parser that extracts:
    - Action: create/refine/regenerate
    - Tone: professional/casual/etc.
    - Slide count: numbers followed by "slides" or "pages"
    - Density: sparse/normal/dense
    - Theme: known theme names
    - Colors: color keywords
    """
    instruction_lower = user_instruction.lower()
    
    # Action detection
    action = IntentAction.CREATE
    if any(word in instruction_lower for word in ["refine", "improve", "update", "modify", "change"]):
        action = IntentAction.REFINE
    elif any(word in instruction_lower for word in ["regenerate", "redo", "start over", "recreate"]):
        action = IntentAction.REGENERATE
    
    # Tone detection
    tone_style = None
    tone_patterns = {
        ToneStyle.PROFESSIONAL: ["professional", "business", "corporate", "formal"],
        ToneStyle.CASUAL: ["casual", "informal", "friendly", "relaxed"],
        ToneStyle.ACADEMIC: ["academic", "scholarly", "research", "educational"],
        ToneStyle.CREATIVE: ["creative", "artistic", "innovative", "bold"],
        ToneStyle.TECHNICAL: ["technical", "engineering", "developer", "code"],
        ToneStyle.MARKETING: ["marketing", "sales", "pitch", "promotional"],
        ToneStyle.MINIMAL: ["minimal", "minimalist", "simple", "clean"],
        ToneStyle.NEUTRAL: ["neutral", "balanced", "standard"],
    }
    for tone, keywords in tone_patterns.items():
        if any(kw in instruction_lower for kw in keywords):
            tone_style = tone
            break
    
    # Slide count detection (e.g., "10 slides", "about 15 pages")
    slide_count = None
    slide_match = re.search(r'(\d+)\s*(?:slides?|pages?)', instruction_lower)
    if slide_match:
        slide_count = int(slide_match.group(1))
    
    # Density detection
    density = None
    if any(word in instruction_lower for word in ["sparse", "minimal content", "one idea per slide"]):
        density = "sparse"
    elif any(word in instruction_lower for word in ["dense", "packed", "detailed", "comprehensive"]):
        density = "dense"
    else:
        density = "normal"
    
    # Theme ID detection (known theme names)
    theme_id = None
    known_themes = ["corp_modern_v1", "minimal_dark", "tech_blue", "nature_green"]
    for theme in known_themes:
        if theme in instruction_lower:
            theme_id = theme
            break
    
    # Color keywords
    color_keywords = []
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", 
              "dark", "light", "colorful", "monochrome", "neon", "pastel"]
    for color in colors:
        if color in instruction_lower:
            color_keywords.append(color)
    
    return ParsedIntent(
        action=action,
        tone_style=tone_style,
        slide_count=slide_count,
        density=density,
        theme_id=theme_id,
        color_keywords=color_keywords,
    )


# =============================================================================
# PLANNER
# =============================================================================

def plan(state: "PipelineState", user_instruction: str) -> TodoQueue:
    """Plan todos from state + user instruction.
    
    This is the main entry point for the planner.
    
    Args:
        state: Current pipeline state
        user_instruction: User's natural language instruction
    
    Returns:
        TodoQueue: Queue of todos to execute
    """
    queue = TodoQueue()
    
    # Step 1: Parse intent from instruction (no LLM, pattern matching)
    intent = parse_intent(user_instruction)
    
    # Step 2: Create constitution todo (no LLM, direct extraction)
    constitution_patch = derive_constitution(intent, user_instruction)
    constitution_todo = TodoItem(
        id="constitution",
        type=TodoType.CONSTITUTION,
        params=constitution_patch,
        status=TodoStatus.PENDING
    )
    queue.add(constitution_todo)
    
    # Step 3: Create atoms todo (if source is available)
    if state.source:
        atoms_params = AtomsParams(
            source_path=state.source.path,
            content_type=state.source.content_type
        )
        atoms_todo = TodoItem(
            id="atoms",
            type=TodoType.ATOMS,
            params=atoms_params,
            depends_on=["constitution"],
            status=TodoStatus.PENDING
        )
        queue.add(atoms_todo)
    
    # Step 4: Create theme todo (if theme requested or not stable)
    if should_create_theme_todo(state, intent):
        theme_params = create_theme_params(intent, user_instruction, state)
        theme_todo = TodoItem(
            id="theme",
            type=TodoType.THEME,
            params=theme_params,
            depends_on=["constitution"],
            status=TodoStatus.PENDING
        )
        queue.add(theme_todo)
    
    # Step 5: Create content todo
    content_deps = ["constitution", "atoms"] if state.source else ["constitution"]
    if should_create_theme_todo(state, intent):
        content_deps.append("theme")
    
    content_params = create_content_params(intent, state)
    content_todo = TodoItem(
        id="content",
        type=TodoType.CONTENT,
        params=content_params,
        depends_on=content_deps,
        status=TodoStatus.PENDING
    )
    queue.add(content_todo)
    
    # Step 6: Create export todo
    export_params = create_export_params(intent)
    export_todo = TodoItem(
        id="export",
        type=TodoType.EXPORT,
        params=export_params,
        depends_on=["content"],
        status=TodoStatus.PENDING
    )
    queue.add(export_todo)
    
    return queue


def derive_constitution(intent: ParsedIntent, user_instruction: str) -> ConstitutionPatch:
    """Derive constitution from intent (NO LLM - direct extraction).
    
    Constitution captures:
    - Tone from instruction
    - Slide count constraints
    - Style rules from keywords
    - Density preferences
    """
    # Extract tone
    tone = None
    if intent.tone_style:
        tone = intent.tone_style.value
    
    # Extract slide count
    target_slides = intent.slide_count
    
    # Build style rules from intent
    style_rules = []
    
    if intent.action == IntentAction.CREATE:
        style_rules.append("Start with a title slide")
    
    if intent.density:
        density_map = {
            "sparse": "Use minimal content per slide, prefer larger fonts",
            "normal": "Balance content density",
            "dense": "Pack more content per slide, use smaller fonts"
        }
        if intent.density in density_map:
            style_rules.append(density_map[intent.density])
    
    # Parse keywords from instruction
    instruction_lower = user_instruction.lower()
    
    if "no animation" in instruction_lower or "no animations" in instruction_lower:
        style_rules.append("No animations")
    
    if "minimalist" in instruction_lower or "clean" in instruction_lower:
        style_rules.append("Minimalist design, plenty of whitespace")
    
    if "bold" in instruction_lower or "impactful" in instruction_lower:
        style_rules.append("Use bold typography for impact")
    
    if "data" in instruction_lower or "chart" in instruction_lower:
        style_rules.append("Include data visualizations where appropriate")
    
    return ConstitutionPatch(
        tone=tone,
        target_slides=target_slides,
        style_rules=style_rules,
    )


def should_create_theme_todo(state: "PipelineState", intent: ParsedIntent) -> bool:
    """Determine if we need to generate/update theme.
    
    Theme todo is needed when:
    1. No active theme in state
    2. Intent explicitly requests a theme
    3. Intent has color keywords
    """
    # No active theme - need one
    if not state.active_theme_id:
        return True
    
    # Intent explicitly requests theme
    if intent.theme_id and intent.theme_id != state.active_theme_id:
        return True
    
    # Intent has color keywords
    if intent.color_keywords:
        return True
    
    return False


def create_theme_params(intent: ParsedIntent, user_instruction: str, state: "PipelineState") -> ThemeParams:
    """Create parameters for theme generation."""
    base_theme_id = intent.theme_id or state.active_theme_id
    
    return ThemeParams(
        base_theme_id=base_theme_id,
        color_keywords=intent.color_keywords if intent.color_keywords else None,
        generate_new=base_theme_id is None
    )


def create_content_params(intent: ParsedIntent, state: "PipelineState") -> ContentParams:
    """Create parameters for content generation."""
    return ContentParams(
        slide_count=intent.slide_count,
        audience=None,
        focus_areas=None
    )


def create_export_params(intent: ParsedIntent) -> ExportParams:
    """Create parameters for export."""
    return ExportParams(
        output_dir="output",
        format="slidev"
    )
