"""Layout engine protocol for calculating widget positions."""
from typing import Protocol, Dict, Any, List
from src.common.renderable_layout import RenderableLayout
from src.common.slides import Slides
from src.layout.theme_protocol import Theme
from src.layout.style_protocol import Style


class LayoutEngine(Protocol):
    """Protocol for layout engine implementations.
    
    Layout engines process layout configurations and produce renderable layouts.
    They orchestrate the two-phase auto-layout process:
    1. Measurement: Calculate widget content sizes
    2. Layout: Calculate absolute positions using strategy algorithms
    """
    
    @classmethod
    def get_layout_documentation(cls) -> str:
        """Provide complete layout system documentation for content generation.
        
        This method returns formatted documentation about the entire layout system,
        including strategies, widgets, and presets. The output is used by content
        generation LLMs to understand all layout capabilities.
        
        Returns:
            Formatted string describing the complete layout system:
            - Layout strategies with slot structures and content guidance
            - Supported widget types with parameters
            - Available preset categories and variants
            - Layout-specific rules or constraints
            
        Example format:
            Available Layout Strategies:
            Bento Family: Grid-based layouts...
              - Bento.Standard: Slots: [cell_1 (size: M), cell_2 (size: M), ...]
            
            Supported Widget Types:
            - Type.Display: Large display text (parameters: text, align)
            - Data.BigNum: Numeric metric display (parameters: value, label, unit)
            
            Supported Preset Attributes:
            - surface: Flat, Elevated, Glass, ...
            - shape: Sharp, Rounded, Pill, ...
        """
        ...
    
    @classmethod
    def calculate(
        cls,
        strategy_name: str,
        widget_assignments: Dict[str, Dict[str, Any]],
        theme: Theme,
        style: Style,
        width: int = 1920,
        height: int = 1080,
    ) -> RenderableLayout:
        """Calculate layout for a single slide with two-phase auto-layout.

        This is the core auto-layout orchestrator that:
        1. Phase 1 (Measurement): Measures each widget's content size
        2. Creates LayoutContext with canvas dimensions and spacing
        3. Phase 2 (Layout): Calls strategy.calculate_layout() to get absolute bounds
        4. Creates WidgetAssignments with calculated bounds

        Args:
            strategy_name: Name of layout strategy (e.g., "Bento.Standard")
            widget_assignments: Mapping of slot roles to widget configurations
                               Format: {"role": {"type": "Type.Display", "parameters": {...}}}
            theme: Theme configuration
            style: Style configuration
            width: Layout width in pixels (default: 1920)
            height: Layout height in pixels (default: 1080)

        Returns:
            RenderableLayout with absolute widget positions ready for rendering

        Raises:
            MissingReferenceError: If strategy not found
            SizeConstraintError: If widget doesn't fit in slot
        """
        ...
    
    @classmethod
    def calculate_slides(
        cls,
        slides: Slides,
        theme: Theme,
        style: Style,
        width: int = 1920,
        height: int = 1080,
    ) -> List[RenderableLayout]:
        """Calculate layouts for multiple slides.

        Args:
            slides: Slides collection containing slide configurations
            theme: Theme configuration (shared across all slides)
            style: Base style configuration (can be overridden per slide)
            width: Layout width in pixels (default: 1920)
            height: Layout height in pixels (default: 1080)

        Returns:
            List of RenderableLayout instances, one per active slide

        Raises:
            MissingReferenceError: If strategy or widget type not found
            SizeConstraintError: If widget doesn't fit in slot
        """
        ...
