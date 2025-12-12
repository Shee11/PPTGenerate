"""Layout engine for calculating widget positions and validating layouts."""
from typing import Any, Dict, List, Type

# Import widgets to ensure they are registered
import src.widgets  # noqa: F401
from src.common.exceptions import MissingReferenceError, SizeConstraintError
from src.common.renderable_layout import RenderableLayout, WidgetAssignment
from src.common.slide import Slide
from src.common.slides import Slides
from src.common.slot import Slot
from src.layout.strategies.bento import (
    BentoHeroLeftStrategy,
    BentoHeroTopStrategy,
    BentoQuarterStrategy,
    BentoStandardStrategy,
)
from src.layout.strategies.cinematic import (
    CinematicFullBleedStrategy,
    CinematicSplit3070Strategy,
    CinematicSplit5050Strategy,
)
from src.layout.strategies.swiss import (
    SwissAsymmetryStrategy,
    SwissPosterStrategy,
    SwissSplitTypoStrategy,
)
from src.layout.style import Style
from src.layout.theme import Theme
from src.widgets.base import WidgetRegistry


class LayoutEngine:
    """Engine for processing layout configurations and producing renderable layouts.
    
    Responsibilities:
    - Select layout strategy based on configuration
    - Validate widget-to-slot assignments (size constraints)
    - Create RenderableLayout with all necessary rendering data
    """

    # Strategy registry mapping strategy names to classes
    _strategies: Dict[str, Any] = {
        "Bento.Standard": BentoStandardStrategy,
        "Bento.HeroLeft": BentoHeroLeftStrategy,
        "Bento.HeroTop": BentoHeroTopStrategy,
        "Bento.Quarter": BentoQuarterStrategy,
        "Swiss.Poster": SwissPosterStrategy,
        "Swiss.Asymmetry": SwissAsymmetryStrategy,
        "Swiss.SplitTypo": SwissSplitTypoStrategy,
        "Cinematic.Split_50_50": CinematicSplit5050Strategy,
        "Cinematic.FullBleed": CinematicFullBleedStrategy,
        "Cinematic.Split_30_70": CinematicSplit3070Strategy,
    }

    @classmethod
    def register_strategy(cls, strategy_class: Type[Any]) -> None:
        """Register a new layout strategy.
        
        Args:
            strategy_class: Strategy class with get_strategy_name() and get_slots()
        """
        name = strategy_class.get_strategy_name()
        cls._strategies[name] = strategy_class

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
        """Calculate layout and validate widget assignments.

        Args:
            strategy_name: Name of layout strategy (e.g., "Bento.Standard")
            widget_assignments: Mapping of slot roles to widget configurations
                               Format: {"role": {"type": "Type.Display", "parameters": {...}}}
            theme: Theme configuration
            style: Style configuration
            width: Layout width in pixels (default: 1920)
            height: Layout height in pixels (default: 1080)

        Returns:
            RenderableLayout ready for HTML rendering

        Raises:
            MissingReferenceError: If strategy not found
            SizeConstraintError: If widget doesn't fit in slot
        """
        # Get strategy
        if strategy_name not in cls._strategies:
            raise MissingReferenceError(
                "strategy",
                strategy_name,
                "layout configuration"
            )

        strategy = cls._strategies[strategy_name]
        slots = strategy.get_slots()

        # Create slot lookup
        slot_map: Dict[str, Slot] = {slot.role: slot for slot in slots}

        # Create widget assignments with validation
        assignments: List[WidgetAssignment] = []

        for role, widget_config in widget_assignments.items():
            # Validate slot exists
            if role not in slot_map:
                raise MissingReferenceError(
                    "slot role",
                    role,
                    f"strategy {strategy_name}"
                )

            slot = slot_map[role]

            # Create widget instance
            widget_type = widget_config.get("type")
            if not widget_type:
                raise ValueError(f"Widget configuration for role '{role}' missing 'type' field")

            widget_class = WidgetRegistry.get(widget_type)
            if not widget_class:
                raise MissingReferenceError(
                    "widget type",
                    widget_type,
                    f"assignment to slot '{role}'"
                )

            # Create widget with parameters
            widget = widget_class(
                atom_id=widget_config.get("atom_id"),
                parameters=widget_config.get("parameters", {})
            )

            # Validate size constraint
            if widget.get_min_size() > slot.size:
                raise SizeConstraintError(
                    widget_type=widget_type,
                    widget_min_size=str(widget.get_min_size()),
                    slot_role=role,
                    slot_size=str(slot.size)
                )

            assignments.append(WidgetAssignment(
                role=role,
                widget=widget,
                slot=slot
            ))

        # Create renderable layout with theme-derived properties
        return RenderableLayout(
            strategy_name=strategy_name,
            widget_assignments=assignments,
            theme_vars=theme.to_css_vars(),
            style_props=style.to_css_props(),
            width=width,
            height=height,
            # Consume theme layout spacing
            margin_x=theme.margin_x,
            margin_y=theme.margin_y,
            gutter=theme.gutter,
            # Consume theme header/footer strategy
            header_height=theme.header_footer.header_height,
            footer_height=theme.header_footer.footer_height,
            header_position=theme.header_footer.header_position,
            footer_position=theme.header_footer.footer_position,
            header_decoration=theme.header_footer.header_decoration,
            footer_decoration=theme.header_footer.footer_decoration,
        )

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
        active_slides = slides.get_active_slides()
        renderable_layouts: List[RenderableLayout] = []

        for slide_index, slide in enumerate(active_slides):
            # Merge base style with slide-specific overrides
            slide_style = style
            if slide.style_override:
                # Create new style with overrides merged
                style_dict = style.model_dump()
                style_dict.update(slide.style_override)
                slide_style = Style.model_validate(style_dict)

            # Calculate layout for this slide
            layout = cls.calculate(
                strategy_name=slide.strategy,
                widget_assignments=slide.widgets,
                theme=theme,
                style=slide_style,
                width=width,
                height=height,
            )

            # Apply sequence pattern background if configured
            if theme.sequence_pattern:
                layout.background_override = theme.get_slide_background(slide_index)

            # Add slide metadata
            layout.slide_number = slide_index + 1
            layout.total_slides = len(active_slides)
            layout.slide_id = slide.id

            renderable_layouts.append(layout)

        return renderable_layouts
