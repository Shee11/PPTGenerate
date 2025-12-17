"""Visual styling generation using LLM."""
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass

from src.utils.llm_client import call_llm
from src.generation.visual.config import get_visual_generation_config


@dataclass
class Visual:
    """Visual styling container for theme, style, and preset.
    
    Attributes:
        theme: Theme configuration (colors, typography, spacing)
        style: Widget-type styling defaults (maps types to theme tokens)
        preset: Global preset defaults (visual styling)
    """
    theme: Dict[str, Any]
    style: Dict[str, Any]
    preset: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format.
        
        Returns:
            Dictionary with theme, style, preset
        """
        return {
            'theme': self.theme,
            'style': self.style,
            'preset': self.preset
        }


def generate_visual(
    intent_guidance: str,
    audience: str = "",
    tone: str = "",
    purpose: str = "",
    use_cache: bool = True
) -> Visual:
    """Generate visual styling (theme, style, preset) using LLM.
    
    Args:
        intent_guidance: Visual guidance from intent detection
        audience: Target audience description
        tone: Presentation tone (professional, casual, technical, etc.)
        purpose: Presentation purpose
        use_cache: Whether to use cached results if available
        
    Returns:
        Visual object with theme, style, and preset
        
    Raises:
        ValueError: If intent_guidance is empty
        json.JSONDecodeError: If LLM output is not valid JSON
        Exception: If LLM API call fails
    """
    if not intent_guidance or not intent_guidance.strip():
        raise ValueError("Intent guidance cannot be empty")
    
    # Get configuration
    config = get_visual_generation_config()
    
    # Build user prompt
    user_prompt = f"""Generate visual styling for this presentation:

**Visual Guidance**:
{intent_guidance}

**Context**:
- Audience: {audience or 'General'}
- Tone: {tone or 'Professional'}
- Purpose: {purpose or 'Informative'}

Generate a JSON object with:
{{
  "theme": {{
    "id": "unique_theme_id",
    "primary_color": "#hex",
    "secondary_color": "#hex",
    "accent_color": "#hex",
    "background_color": "#hex",
    "text_color": "#hex",
    "font_family": "font-name"
  }},
  "style": {{
    "theme_name": "theme_id",
    "widgets": {{
      "Type.Display": {{"font": "h1", "align": "left", "foreground": "text_color"}},
      "Type.Heading": {{"font": "h2", "align": "left", "foreground": "text_color"}},
      "Type.Body": {{"font": "body", "align": "left", "foreground": "text_color"}},
      "Type.List": {{"font": "body", "align": "left", "foreground": "text_color"}},
      "Type.Quote": {{"font": "h3", "align": "left", "foreground": "accent_color"}},
      "Type.Comparison": {{"font": "body", "align": "center", "foreground": "text_color"}},
      "Data.BigNum": {{"font": "h1", "align": "center", "foreground": "primary_color"}},
      "Data.Progress": {{"font": "body", "align": "left", "foreground": "text_color"}},
      "Data.Trend": {{"font": "h2", "align": "center", "foreground": "primary_color"}}
    }}
  }},
  "preset": {{
    "surface": "Flat|Elevated|Glass|...",
    "shape": "Sharp|Rounded|Pill|...",
    "fill": "Solid_Brand|Gradient_Linear|...",
    "effect": "Glow|Glitch|..." (optional)
  }}
}}

Ensure:
1. Theme colors have proper contrast (WCAG AA)
2. Style covers all common widget types
3. Preset matches the tone and purpose

**CRITICAL**: Output ONLY the JSON object, no markdown code blocks, no explanations."""
    
    # Call LLM with JSON response format
    try:
        response = call_llm(
            system_prompt=config.system_prompt,
            user_prompt=user_prompt,
            deployment=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            max_reasoning_tokens=config.max_reasoning_tokens,
            response_format="json"
        )
    except Exception as e:
        raise Exception(f"Visual generation LLM call failed: {str(e)}")
    
    # Parse JSON response
    try:
        visual_data = json.loads(response)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Failed to parse visual LLM response as JSON. Response: {response[:200]}", e.doc, e.pos)
    
    # Validate structure
    if 'theme' not in visual_data or 'style' not in visual_data or 'preset' not in visual_data:
        raise ValueError(f"Invalid visual response: missing theme, style, or preset")
    
    # Create Visual object
    visual = Visual(
        theme=visual_data['theme'],
        style=visual_data['style'],
        preset=visual_data['preset']
    )
    
    return visual
