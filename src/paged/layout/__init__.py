"""Layout engine and strategies."""
from src.paged.layout.layout_engine_protocol import LayoutEngine
from src.paged.layout.layout_protocol import LayoutStrategy, LayoutContext, WidgetLayoutInput
from src.paged.layout.theme_protocol import Theme
from src.paged.layout.style_protocol import Style, WidgetStyle
from src.paged.layout.engine_registry import LayoutEngineRegistry

# Import engine modules to trigger auto-registration
import src.paged.layout.dummy  # Registers "dummy" engine
import src.paged.layout.slidev  # Registers "slidev" engine

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
