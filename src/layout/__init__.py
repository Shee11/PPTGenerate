"""Layout engine and strategies."""
from src.layout.layout_engine_protocol import LayoutEngine
from src.layout.layout_protocol import LayoutStrategy, LayoutContext, WidgetLayoutInput
from src.layout.theme_protocol import Theme
from src.layout.style_protocol import Style, WidgetStyle
from src.layout.engine_registry import LayoutEngineRegistry

# Import engine modules to trigger auto-registration
import src.layout.dummy  # Registers "dummy" engine
import src.layout.slidev  # Registers "slidev" engine

__all__ = [
    "LayoutEngine",
    "LayoutStrategy",
    "LayoutContext",
    "WidgetLayoutInput",
    "Theme",
    "Style",
    "WidgetStyle",
    "LayoutEngineRegistry",
]
