"""Theme Tool - Load or generate presentation themes.

DirectTool: Delegates to src.generation.theme.creator for sophisticated theme generation.
Can load existing themes or create new ones via LLM.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional, List, Dict, Any, ClassVar
from pydantic import Field

from src.common.tool_protocol import DirectTool, ToolContext, ToolPatch, register_tool

if TYPE_CHECKING:
    from src.generation.state import PipelineState


class ThemeContext(ToolContext):
    """Context for theme generation."""
    available_themes: List[str] = Field(default_factory=list)
    current_theme_id: Optional[str] = None
    intent_guidance: str = Field(default="", description="Style guidance from constitution")


class ThemePatch(ToolPatch):
    """Patch containing theme to apply."""
    theme: Optional[Any] = Field(default=None, description="Theme object or dict")
    theme_id: str = ""
    load_from_file: bool = False
    is_new_theme: bool = False


@register_tool
class ThemeTool(DirectTool[ThemeContext, ThemePatch]):
    """Generates or loads themes using the theme creator.
    
    This is a DirectTool that:
    - Loads existing themes by name (no LLM)
    - Delegates to src.generation.theme.creator for new themes
    """
    
    # Self-description
    name: ClassVar[str] = "theme"
    description: ClassVar[str] = "Load existing theme by name or generate new theme via LLM. Can customize colors, fonts, spacing."
    query_description: ClassVar[str] = "Triggered by theme name (corp_modern_v1, minimal_dark) or style keywords (dark, colorful, blue, professional)."
    args_description: ClassVar[List[str]] = [
        "theme_id (existing theme name to load)",
        "color_keywords (dark, light, colorful, monochrome)",
        "style_keywords (professional, creative, minimal, bold)",
    ]
    requires: ClassVar[List[str]] = ["constitution"]
    produces: ClassVar[List[str]] = ["themes", "active_theme_id"]
    
    def slice(self, state: "PipelineState", params: Optional[Dict[str, Any]] = None) -> ThemeContext:
        """Extract context from state."""
        # Build intent guidance from constitution
        intent_guidance = ""
        constitution = state.get_constitution()
        if constitution:
            if hasattr(constitution, 'style_rules') and constitution.style_rules:
                intent_guidance = "\n".join(constitution.style_rules)
            if hasattr(constitution, 'tone') and constitution.tone:
                intent_guidance += f"\nTone: {constitution.tone}"
        
        return ThemeContext(
            available_themes=list(state.themes.keys()),
            current_theme_id=state.active_theme_id,
            intent_guidance=intent_guidance,
        )
    
    def transform(
        self,
        context: ThemeContext,
        user_instruction: str,
    ) -> ThemePatch:
        """Determine whether to load existing theme or create new one."""
        instruction_lower = user_instruction.lower()
        
        # Check if specific theme requested by name
        for theme_id in context.available_themes:
            if theme_id.lower() in instruction_lower:
                self._log(f"Found matching theme: {theme_id}")
                return ThemePatch(
                    theme_id=theme_id,
                    load_from_file=True,
                )
        
        # Check for theme-related keywords that suggest creating a new theme
        create_keywords = ["create theme", "generate theme", "new theme", "custom theme", "make theme"]
        should_create = any(kw in instruction_lower for kw in create_keywords)
        
        # Also check for specific style descriptions
        style_keywords = ["dark theme", "light theme", "neon", "pastel", "vibrant", "colorful", "minimal"]
        has_style = any(kw in instruction_lower for kw in style_keywords)
        
        if should_create or has_style:
            # Generate new theme via creator
            return self._create_new_theme(user_instruction, context.intent_guidance)
        
        # Default: use first available theme or corp_modern
        default_theme = "corp_modern_v1" if "corp_modern_v1" in context.available_themes else (
            context.available_themes[0] if context.available_themes else "default"
        )
        self._log(f"Using default theme: {default_theme}")
        return ThemePatch(
            theme_id=default_theme,
            load_from_file=True,
        )
    
    def _create_new_theme(self, user_instruction: str, intent_guidance: str) -> ThemePatch:
        """Create a new theme via the theme creator."""
        from src.generation.theme.creator import create_theme
        
        self._log(f"Creating new theme: {user_instruction[:50]}...")
        
        # Determine if we should base on existing theme
        base_theme_id = None
        instruction_lower = user_instruction.lower()
        
        # Check for "based on" or "like" references
        if "based on" in instruction_lower or "like" in instruction_lower:
            for theme_name in ["corp_modern", "minimal_dark", "cyber_neon", "forest", "ocean", "royal", "slate", "sunset"]:
                if theme_name in instruction_lower:
                    base_theme_id = f"{theme_name}_v1" if not theme_name.endswith("_v1") else theme_name
                    break
        
        # Create theme
        theme = create_theme(
            user_instruction=user_instruction,
            base_theme_id=base_theme_id,
            intent_guidance=intent_guidance,
            use_cache=self.use_cache,
        )
        
        self._log(f"Created theme: {theme.id}")
        
        return ThemePatch(
            theme=theme.to_dict(),
            theme_id=theme.id,
            is_new_theme=True,
        )
    
    def apply(self, state: "PipelineState", patch: ThemePatch) -> None:
        """Apply theme to state."""
        if patch.is_new_theme and patch.theme:
            # Add new theme to state (theme dict must have 'id' key)
            theme_data = patch.theme
            if isinstance(theme_data, dict) and 'id' not in theme_data:
                theme_data['id'] = patch.theme_id
            state.add_theme(theme_data)
            state.set_active_theme(patch.theme_id)
            self._log(f"Added and activated new theme: {patch.theme_id}")
        elif patch.load_from_file:
            if patch.theme_id in state.themes:
                state.set_active_theme(patch.theme_id)
                self._log(f"Activated existing theme: {patch.theme_id}")
            else:
                # Try to load from file
                theme_data = self._load_theme_file(patch.theme_id)
                if theme_data:
                    state.add_theme(theme_data)
                    state.set_active_theme(patch.theme_id)
                    self._log(f"Loaded and activated theme: {patch.theme_id}")
                else:
                    self._log(f"Warning: Theme not found: {patch.theme_id}")
    
    def _load_theme_file(self, theme_id: str) -> Optional[Dict[str, Any]]:
        """Load theme from assets/themes directory."""
        import json
        
        themes_dir = Path(__file__).parent.parent / "assets" / "themes"
        
        # Try exact filename
        theme_file = themes_dir / f"{theme_id}.json"
        if theme_file.exists():
            return json.loads(theme_file.read_text(encoding='utf-8'))
        
        # Try without version suffix
        base_name = theme_id.replace("_v1", "").replace("_v2", "")
        theme_file = themes_dir / f"{base_name}.json"
        if theme_file.exists():
            return json.loads(theme_file.read_text(encoding='utf-8'))
        
        return None
