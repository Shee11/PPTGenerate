"""Prompts for theme creation and customization."""
import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from src.utils.generation_config import GenerationConfig
from src.generation.theme.models import Theme, THEME_SCHEMA_REFERENCE


def get_builtin_themes() -> List[Dict[str, Any]]:
    """Load all built-in themes from assets/themes directory.
    
    Returns:
        List of theme dictionaries
    """
    themes_dir = Path(__file__).parent.parent.parent.parent / "assets" / "themes"
    themes = []
    
    if themes_dir.exists():
        for theme_file in themes_dir.glob("*.json"):
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    theme_data = json.load(f)
                    themes.append(theme_data)
            except (json.JSONDecodeError, IOError):
                continue
    
    return themes


def get_theme_examples() -> str:
    """Get formatted examples of built-in themes for LLM reference.
    
    Returns:
        Formatted string with 2-3 example themes
    """
    themes = get_builtin_themes()
    
    examples = []
    # Show a light theme and a dark theme as examples
    light_example = next((t for t in themes if "corp" in t.get("id", "").lower()), None)
    dark_example = next((t for t in themes if "dark" in t.get("id", "").lower()), None)
    
    if light_example:
        examples.append(f"Light Theme Example (corp_modern):\n{json.dumps(light_example, indent=2)}")
    if dark_example:
        examples.append(f"Dark Theme Example (minimal_dark):\n{json.dumps(dark_example, indent=2)}")
    
    return "\n\n".join(examples)


THEME_CREATION_SYSTEM_PROMPT = """You are an expert visual designer specializing in presentation themes.

Your task is to create cohesive, professional presentation themes based on user requirements.

## Design Principles

1. **Color Harmony**: Use color theory (complementary, analogous, triadic) for pleasing palettes
2. **Contrast**: Ensure sufficient contrast between text and background (WCAG AA minimum)
3. **Typography Hierarchy**: Clear size/weight progression from h1 to caption
4. **Consistency**: All colors should feel like they belong together

## Theme Types

- **Light themes**: Light background (#ffffff, #f8fafc), dark text (#1e293b, #0f172a)
- **Dark themes**: Dark background (#0f172a, #1e1e1e), light text (#f1f5f9, #ffffff)
- **Vibrant themes**: Bold primary colors with high contrast accents
- **Corporate themes**: Conservative, professional color choices
- **Creative themes**: More expressive typography and color choices

## Color Guidelines

For LIGHT themes:
- background_color: #ffffff or light gray (#f8fafc, #f1f5f9)
- text_color: Dark (#1e293b, #0f172a, #111827)
- primary_background: Slightly off-white (#f8fafc)
- secondary_background: White or very light (#ffffff, #fafafa)

For DARK themes:
- background_color: Dark (#0f172a, #1e1e1e, #111827)
- text_color: Light (#f1f5f9, #ffffff, #e5e7eb)
- primary_background: Slightly lighter dark (#1e293b, #27272a)
- secondary_background: Base dark or darker (#0f172a, #18181b)

## Typography Guidelines

- h1: 48-72px, bold/black weight
- h2: 36-48px, medium/bold weight
- h3: 24-32px, medium/semibold weight
- body: 16-20px, regular/light weight
- caption: 12-16px, regular/light weight

Return a complete, valid JSON theme object."""


def render_theme_creation_prompt(
    user_instruction: str,
    base_theme: Optional[Dict[str, Any]] = None,
    intent_guidance: str = ""
) -> str:
    """Render user prompt for theme creation.
    
    Args:
        user_instruction: What kind of theme the user wants
        base_theme: Optional existing theme to customize/modify
        intent_guidance: Optional guidance from constitution
        
    Returns:
        Formatted user prompt
    """
    parts = []
    
    # Schema reference
    parts.append(f"## Theme Schema\n{THEME_SCHEMA_REFERENCE}")
    
    # Examples
    examples = get_theme_examples()
    if examples:
        parts.append(f"## Built-in Theme Examples\n{examples}")
    
    # Base theme if customizing
    if base_theme:
        parts.append(f"## Base Theme to Customize\n```json\n{json.dumps(base_theme, indent=2)}\n```")
        parts.append("Modify the base theme according to the user's requirements. Keep unchanged values.")
    
    # Intent guidance
    if intent_guidance:
        parts.append(f"## Style Guidance\n{intent_guidance}")
    
    # User instruction
    parts.append(f"## User Request\n{user_instruction}")
    
    # Output format
    parts.append("""## Output Format
Return ONLY a valid JSON object with the complete theme.
Do not include markdown code fences or explanations.
Ensure all required fields are present.""")
    
    return "\n\n".join(parts)


def render_theme_customization_prompt(
    base_theme: Dict[str, Any],
    modifications: str,
    intent_guidance: str = ""
) -> str:
    """Render prompt for customizing an existing theme.
    
    Args:
        base_theme: The theme to modify
        modifications: What to change (e.g., "make it darker", "use green instead of blue")
        intent_guidance: Optional guidance
        
    Returns:
        Formatted prompt for theme customization
    """
    parts = []
    
    parts.append(f"## Current Theme\n```json\n{json.dumps(base_theme, indent=2)}\n```")
    
    parts.append(f"## Requested Modifications\n{modifications}")
    
    if intent_guidance:
        parts.append(f"## Style Guidance\n{intent_guidance}")
    
    parts.append("""## Instructions
1. Start with the current theme as base
2. Apply the requested modifications
3. Ensure color harmony is maintained after changes
4. Keep the same structure - only change values
5. Generate a new unique ID for the modified theme (e.g., original_id + "_custom")

Return ONLY the complete modified theme as valid JSON.""")
    
    return "\n\n".join(parts)


# JSON Schema for structured output
THEME_JSON_SCHEMA = {
    "name": "theme_response",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "margin_x": {"type": "string"},
            "margin_y": {"type": "string"},
            "gutter": {"type": "string"},
            "header_footer": {
                "type": "object",
                "properties": {
                    "header_height": {"type": "string"},
                    "footer_height": {"type": "string"},
                    "header_position": {"type": "string"},
                    "footer_position": {"type": "string"},
                    "header_decoration": {"type": "string"},
                    "footer_decoration": {"type": "string"}
                },
                "required": ["header_height", "footer_height", "header_position", "footer_position", "header_decoration", "footer_decoration"],
                "additionalProperties": False
            },
            "sequence_pattern": {"type": "string"},
            "typography": {
                "type": "object",
                "properties": {
                    "h1": {
                        "type": "object",
                        "properties": {
                            "size": {"type": "integer"},
                            "weight": {"type": "string"},
                            "line_height": {"type": "number"}
                        },
                        "required": ["size", "weight", "line_height"],
                        "additionalProperties": False
                    },
                    "h2": {
                        "type": "object",
                        "properties": {
                            "size": {"type": "integer"},
                            "weight": {"type": "string"},
                            "line_height": {"type": "number"}
                        },
                        "required": ["size", "weight", "line_height"],
                        "additionalProperties": False
                    },
                    "h3": {
                        "type": "object",
                        "properties": {
                            "size": {"type": "integer"},
                            "weight": {"type": "string"},
                            "line_height": {"type": "number"}
                        },
                        "required": ["size", "weight", "line_height"],
                        "additionalProperties": False
                    },
                    "body": {
                        "type": "object",
                        "properties": {
                            "size": {"type": "integer"},
                            "weight": {"type": "string"},
                            "line_height": {"type": "number"}
                        },
                        "required": ["size", "weight", "line_height"],
                        "additionalProperties": False
                    },
                    "caption": {
                        "type": "object",
                        "properties": {
                            "size": {"type": "integer"},
                            "weight": {"type": "string"},
                            "line_height": {"type": "number"}
                        },
                        "required": ["size", "weight", "line_height"],
                        "additionalProperties": False
                    }
                },
                "required": ["h1", "h2", "h3", "body", "caption"],
                "additionalProperties": False
            },
            "primary_color": {"type": "string"},
            "secondary_color": {"type": "string"},
            "accent_color": {"type": "string"},
            "background_color": {"type": "string"},
            "text_color": {"type": "string"},
            "primary_background": {"type": "string"},
            "secondary_background": {"type": "string"},
            "font_family": {"type": "string"},
            "heading_font": {"type": "string"}
        },
        "required": [
            "id", "margin_x", "margin_y", "gutter", "header_footer",
            "sequence_pattern", "typography", "primary_color", "secondary_color",
            "accent_color", "background_color", "text_color", "primary_background",
            "secondary_background", "font_family", "heading_font"
        ],
        "additionalProperties": False
    }
}


def get_theme_creation_config(
    temperature: float = 0.7,
    max_tokens: int = 4000
) -> GenerationConfig:
    """Get GenerationConfig for theme creation.
    
    Args:
        temperature: Sampling temperature (0.7 for creative variety)
        max_tokens: Maximum tokens in response
        
    Returns:
        GenerationConfig for theme creation
    """
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4-turbo')
    return GenerationConfig(
        model=deployment,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=THEME_CREATION_SYSTEM_PROMPT,
        user_prompt_template="{content}",
        response_format="json_schema",
        json_schema=THEME_JSON_SCHEMA
    )
