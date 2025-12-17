"""Configuration for visual styling generation."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class VisualGenerationConfig:
    """Configuration for visual styling generation (theme, style, preset).
    
    Attributes:
        model: LLM model to use for generation
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens in response
        max_reasoning_tokens: Maximum reasoning tokens (o1 models)
        system_prompt: System prompt for visual generation
    """
    model: str
    temperature: float
    max_tokens: int
    max_reasoning_tokens: Optional[int]
    system_prompt: str


def get_visual_generation_config() -> VisualGenerationConfig:
    """Get visual generation configuration.
    
    Returns:
        VisualGenerationConfig with default settings
    """
    system_prompt = """You are an expert presentation designer specializing in visual styling and theming.

Your task: Generate cohesive visual styling (theme, style, preset) for a presentation.

Given:
1. Intent guidance with visual recommendations
2. Audience, tone, and purpose

Output a JSON object with three components:

**theme**: Color palette and typography
- Colors: primary, secondary, accent, background, text (hex codes)
- Ensure WCAG AA contrast (4.5:1 text/bg ratio)
- Match tone (Tech → dark bg #0a0a0a, Corporate → light #f5f5f5)

**style**: Widget-type styling defaults
- MUST include all 9 widget types: Data.BigNum, Data.Progress, Data.Trend, Type.Body, Type.Comparison, Type.Display, Type.Heading, Type.List, Type.Quote
- Map each widget type to theme tokens
- font: theme typography token (h1, h2, h3, body, caption)
- align: text alignment (left, center, right, justify)
- foreground: theme color token for text (text_color, primary_color, accent_color)
- background: optional theme color token for background
- Example widget styles:
  - "Type.Display": {"font": "h1", "align": "left", "foreground": "text_color"}
  - "Type.Heading": {"font": "h2", "align": "left", "foreground": "text_color"}
  - "Type.Body": {"font": "body", "align": "left", "foreground": "text_color"}
  - "Type.List": {"font": "body", "align": "left", "foreground": "text_color"}
  - "Type.Quote": {"font": "h3", "align": "left", "foreground": "accent_color"}
  - "Type.Comparison": {"font": "body", "align": "center", "foreground": "text_color"}
  - "Data.BigNum": {"font": "h1", "align": "center", "foreground": "primary_color"}
  - "Data.Progress": {"font": "body", "align": "left", "foreground": "text_color"}
  - "Data.Trend": {"font": "h2", "align": "center", "foreground": "primary_color"}

**preset**: Global visual style defaults
- surface: depth effect (Flat, Elevated, Glass, etc.)
- shape: border radius (Sharp, Rounded, Pill, etc.)
- fill: background pattern (Solid_Brand, Gradient_Linear, etc.)
- effect: optional visual filter (Glitch, Glow, etc.)

Output ONLY valid JSON. No markdown, no explanations."""

    return VisualGenerationConfig(
        model="gpt-4o",
        temperature=0.3,  # Lower temperature for consistent styling
        max_tokens=2000,
        max_reasoning_tokens=None,
        system_prompt=system_prompt
    )
