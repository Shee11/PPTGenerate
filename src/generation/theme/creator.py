"""Theme creator - generates and customizes themes via LLM."""
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from src.generation.theme.models import Theme
from src.generation.theme.prompts import (
    render_theme_creation_prompt,
    render_theme_customization_prompt,
    get_theme_creation_config,
    get_builtin_themes,
)
from src.utils.llm_client import call_llm
from src.utils.cache import GenerationCache

logger = logging.getLogger(__name__)

# Module-level cache
_cache = GenerationCache(Path(".cache/themes"))


def create_theme(
    user_instruction: str,
    base_theme_id: Optional[str] = None,
    intent_guidance: str = "",
    use_cache: bool = True,
) -> Theme:
    """Create a new theme based on user instruction.
    
    This function generates a complete theme using LLM, guided by:
    - User instruction (e.g., "create a dark theme with purple accents")
    - Optional base theme to start from
    - Intent guidance from constitution
    
    Args:
        user_instruction: Description of desired theme
        base_theme_id: Optional ID of existing theme to use as base
        intent_guidance: Optional style guidance
        use_cache: Whether to use cached results
        
    Returns:
        Generated Theme object
        
    Raises:
        ValueError: If theme generation fails
        
    Example:
        >>> theme = create_theme("professional dark theme with blue accents")
        >>> print(theme.id)  # e.g., "dark_blue_professional_v1"
        >>> print(theme.primary_color)  # e.g., "#3b82f6"
    """
    # Get base theme if specified
    base_theme = None
    if base_theme_id:
        base_theme = _get_builtin_theme(base_theme_id)
    
    # Check cache
    cache_key = None
    if use_cache:
        cache_input = f"{str(base_theme)}|{intent_guidance}"
        cache_key = _cache.hash_key(user_instruction, cache_input)
        cached = _cache.load(cache_key)
        if cached:
            logger.info(f"Cache hit for theme creation")
            print("✓ Using cached theme")
            return Theme.from_dict(cached)
    
    # Get config
    config = get_theme_creation_config()
    
    # Render prompt
    user_prompt = render_theme_creation_prompt(
        user_instruction=user_instruction,
        base_theme=base_theme,
        intent_guidance=intent_guidance,
    )
    
    logger.info(f"Creating theme via LLM: {user_instruction[:50]}...")
    print(f"⚙ Creating theme via LLM...")
    
    # Call LLM
    response = call_llm(
        system_prompt=config.system_prompt,
        user_prompt=user_prompt,
        deployment=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        response_format=config.response_format,
        json_schema=config.json_schema,
    )
    
    # Parse response
    try:
        theme_data = json.loads(response)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse theme JSON: {e}")
        logger.error(f"Response: {response[:500]}")
        raise ValueError(f"Invalid theme JSON from LLM: {e}")
    
    # Validate and create Theme
    theme = Theme.from_dict(theme_data)
    
    logger.info(f"Created theme: {theme.id}")
    print(f"✓ Created theme: {theme.id}")
    
    # Cache result
    if use_cache and cache_key:
        _cache.save(cache_key, theme_data)
    
    return theme


def customize_theme(
    base_theme_id: str,
    modifications: str,
    intent_guidance: str = "",
    use_cache: bool = True,
) -> Theme:
    """Customize an existing theme with specific modifications.
    
    This function takes an existing theme and applies modifications using LLM.
    Useful for quick adjustments like:
    - "make it darker"
    - "use green instead of blue"
    - "increase heading sizes"
    
    Args:
        base_theme_id: ID of the theme to customize
        modifications: What to change
        intent_guidance: Optional style guidance
        use_cache: Whether to use cached results
        
    Returns:
        Modified Theme object
        
    Raises:
        ValueError: If base theme not found or customization fails
        
    Example:
        >>> theme = customize_theme("corp_modern_v1", "make the accent color red")
        >>> print(theme.accent_color)  # e.g., "#ef4444"
    """
    # Get base theme
    base_theme = _get_builtin_theme(base_theme_id)
    if not base_theme:
        raise ValueError(f"Base theme not found: {base_theme_id}")
    
    # Check cache
    cache_key = None
    if use_cache:
        cache_input = f"{base_theme_id}|{modifications}|{intent_guidance}"
        cache_key = _cache.hash_key("customize_theme", cache_input)
        cached = _cache.load(cache_key)
        if cached:
            logger.info(f"Cache hit for theme customization")
            print("✓ Using cached customized theme")
            return Theme.from_dict(cached)
    
    # Get config
    config = get_theme_creation_config()
    
    # Render prompt
    user_prompt = render_theme_customization_prompt(
        base_theme=base_theme,
        modifications=modifications,
        intent_guidance=intent_guidance,
    )
    
    logger.info(f"Customizing theme {base_theme_id}: {modifications[:50]}...")
    print(f"⚙ Customizing theme {base_theme_id}...")
    
    # Call LLM
    response = call_llm(
        system_prompt=config.system_prompt,
        user_prompt=user_prompt,
        deployment=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        response_format=config.response_format,
        json_schema=config.json_schema,
    )
    
    # Parse response
    try:
        theme_data = json.loads(response)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse customized theme JSON: {e}")
        raise ValueError(f"Invalid theme JSON from LLM: {e}")
    
    # Validate and create Theme
    theme = Theme.from_dict(theme_data)
    
    logger.info(f"Customized theme: {theme.id}")
    print(f"✓ Customized theme: {theme.id}")
    
    # Cache result
    if use_cache and cache_key:
        _cache.save(cache_key, theme_data)
    
    return theme


def _get_builtin_theme(theme_id: str) -> Optional[Dict[str, Any]]:
    """Get a built-in theme by ID.
    
    Args:
        theme_id: Theme ID to look up
        
    Returns:
        Theme dictionary or None if not found
    """
    themes = get_builtin_themes()
    
    # Try exact match first
    for theme in themes:
        if theme.get("id") == theme_id:
            return theme
    
    # Try partial match (without version suffix)
    for theme in themes:
        tid = theme.get("id", "")
        if theme_id in tid or tid.startswith(theme_id.replace("_v1", "")):
            return theme
    
    return None


def save_theme(theme: Theme, output_dir: Optional[Path] = None) -> Path:
    """Save a theme to a JSON file.
    
    Args:
        theme: Theme to save
        output_dir: Directory to save to (defaults to assets/themes)
        
    Returns:
        Path to saved file
    """
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent.parent / "assets" / "themes"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename from ID (strip version suffix for filename)
    base_name = theme.id.replace("_v1", "").replace("_v2", "")
    output_path = output_dir / f"{base_name}.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(theme.to_dict(), f, indent=2)
    
    logger.info(f"Saved theme to: {output_path}")
    return output_path


def list_builtin_themes() -> list[str]:
    """List all available built-in theme IDs.
    
    Returns:
        List of theme IDs
    """
    themes = get_builtin_themes()
    return [t.get("id", "unknown") for t in themes]
