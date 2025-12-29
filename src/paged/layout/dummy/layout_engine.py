"""Layout engine for calculating widget positions and validating layouts."""
from typing import Any, Dict, List, Optional, Type

# Import widgets to ensure they are registered
import src.paged.widgets  # noqa: F401
from src.common.exceptions import MissingReferenceError, SizeConstraintError
from src.common.renderable_layout import RenderableLayout, WidgetAssignment
from src.common.slide import Slide
from src.common.slides import Slides
from src.common.slot import Slot
from src.paged.layout.dummy.strategies.bento import (
    BentoHeroLeftStrategy,
    BentoHeroTopStrategy,
    BentoQuarterStrategy,
    BentoStandardStrategy,
    BentoVerticalStackStrategy,
)
from src.paged.layout.dummy.strategies.cinematic import (
    CinematicFullBleedStrategy,
    CinematicSplit3070Strategy,
    CinematicSplit5050Strategy,
)
from src.paged.layout.dummy.strategies.data import DataKPIRowStrategy
from src.paged.layout.dummy.strategies.edit import (
    EditMagazineCollageStrategy,
    EditOverlapLeftStrategy,
    EditStaggeredStrategy,
)
from src.paged.layout.dummy.strategies.focus import (
    FocusOffsetTitleStrategy,
    FocusSolarSystemStrategy,
)
from src.paged.layout.dummy.strategies.swiss import (
    SwissAsymmetryStrategy,
    SwissPosterStrategy,
    SwissSplitTypoStrategy,
)
from src.paged.layout.dummy.strategies.comparison import (
    ComparisonTwoColumnStrategy,
    ComparisonThreeColumnStrategy,
)
from src.paged.layout.dummy.strategies.matrix import (
    MatrixGridStrategy,
    MatrixTimelineStrategy,
)
from src.paged.layout.dummy.style import Style
from src.paged.layout.dummy.theme import Theme
from src.paged.widgets.base import WidgetRegistry


class LayoutEngine:
    """Engine for processing layout configurations and producing renderable layouts.
    
    Responsibilities:
    - Select layout strategy based on configuration
    - Validate widget-to-slot assignments (size constraints)
    - Create RenderableLayout with all necessary rendering data
    - Provide layout documentation for content generation
    """

    # Strategy registry mapping strategy names to classes
    _strategies: Dict[str, Any] = {
        "Bento.Standard": BentoStandardStrategy,
        "Bento.HeroLeft": BentoHeroLeftStrategy,
        "Bento.HeroTop": BentoHeroTopStrategy,
        "Bento.Quarter": BentoQuarterStrategy,
        "Bento.VerticalStack": BentoVerticalStackStrategy,
        "Swiss.Poster": SwissPosterStrategy,
        "Swiss.Asymmetry": SwissAsymmetryStrategy,
        "Swiss.SplitTypo": SwissSplitTypoStrategy,
        "Cinematic.Split_50_50": CinematicSplit5050Strategy,
        "Cinematic.FullBleed": CinematicFullBleedStrategy,
        "Cinematic.Split_30_70": CinematicSplit3070Strategy,
        "Edit.Overlap_Left": EditOverlapLeftStrategy,
        "Edit.Magazine_Collage": EditMagazineCollageStrategy,
        "Edit.Staggered": EditStaggeredStrategy,
        "Data.KPI_Row": DataKPIRowStrategy,
        "Focus.Solar_System": FocusSolarSystemStrategy,
        "Focus.Offset_Title": FocusOffsetTitleStrategy,
        "Comparison.TwoColumn": ComparisonTwoColumnStrategy,
        "Comparison.ThreeColumn": ComparisonThreeColumnStrategy,
        "Matrix.Grid": MatrixGridStrategy,
        "Matrix.Timeline": MatrixTimelineStrategy,
    }

    # Default presets for each widget type
    # These are applied when no explicit preset is specified
    # Default is minimal styling (Flat surface = no visual treatment)
    _default_presets: Dict[str, Dict[str, str]] = {
        "Type.Display": {"surface": "Flat"},
        "Type.Heading": {"surface": "Flat"},
        "Type.Body": {"surface": "Flat"},
        "Type.List": {"surface": "Flat"},
        "Type.Quote": {"surface": "Flat"},
        "Data.BigNum": {"surface": "Flat"},
        "Data.Progress": {"surface": "Flat"},
        "Data.Trend": {"surface": "Flat"},
        "Data.Chart": {"surface": "Flat"},
        "Media.Image": {"surface": "Flat"},
        "Media.Video": {"surface": "Flat"},
        "Media.Icon": {"surface": "Flat"},
    }

    @classmethod
    def get_layout_prompt(cls) -> str:
        """Provide layout reference for LLM content generation prompts.
        
        Returns:
            Formatted string with layout system reference.
        """
        # Import here to avoid circular dependency
        from src.common.asset_manager import AssetManager
        
        # ========== LAYOUT STRATEGIES ==========
        strategies = AssetManager.list_strategies()
        
        # Layout family descriptions for content guidance
        family_descriptions = {
            "Bento": "Grid-based layouts with multiple content cells. Best for: data comparisons, feature highlights, multi-topic summaries. Content should be parallel in structure and concise.",
            "Cinematic": "Full-bleed dramatic layouts emphasizing visual impact. Best for: hero statements, key messages, emotional moments. Content should be bold and declarative.",
            "Swiss": "Typography-focused minimalist layouts. Best for: quotes, philosophical statements, core principles. Content should be distilled to essential truth.",
            "Data": "Metric-driven layouts with KPIs and numbers. Best for: statistics, performance metrics, quantitative insights. Content should be numeric facts with brief labels.",
            "Edit": "Magazine-style artistic layouts with overlapping elements. Best for: creative storytelling, visual narratives. Content should be evocative and layered.",
            "Focus": "Single-point emphasis layouts. Best for: key takeaways, central concepts, primary messages. Content should be the ONE thing that matters."
        }
        
        lines = ["Available Layout Strategies:"]
        
        # Group by family
        families = {}
        for strategy in strategies:
            family = strategy['family']
            if family not in families:
                families[family] = []
            families[family].append(strategy)
        
        for family, family_strategies in sorted(families.items()):
            # Add family description
            if family in family_descriptions:
                lines.append(f"\n{family} Family: {family_descriptions[family]}")
            
            for strategy in family_strategies:
                # Format each slot with both role and size
                slot_details = []
                for slot in strategy['slots']:
                    slot_details.append(f"{slot['role']} (size: {slot['size']})")
                
                slot_info = ", ".join(slot_details)
                lines.append(f"  - {strategy['name']}: Slots: [{slot_info}]")
        
        # ========== WIDGET TYPES ==========
        widgets = AssetManager.list_widgets()
        lines.append("\n\nSupported Widget Types:")
        
        for widget in widgets:
            # Extract key parameters
            param_info = []
            if 'fields' in widget and 'parameters' in widget['fields']:
                param_field = widget['fields']['parameters']
                if 'parameters' in param_field:
                    params = param_field['parameters']
                    param_names = [p['name'] for p in params[:3]]  # First 3 params
                    param_info = [f"parameters: {', '.join(param_names)}"]
            
            desc = widget.get('description', '')
            if param_info:
                lines.append(f"- {widget['type']}: {desc} ({'; '.join(param_info)})")
            else:
                lines.append(f"- {widget['type']}: {desc} (parameters: varies by widget)")
        
        # ========== PRESET ATTRIBUTES ==========
        presets = {
            "surface": ["Flat", "Elevated", "Outline", "Glass", "Sunken", "NeoBrutal", "Subtle"],
            "shape": ["Sharp", "Rounded", "Curve", "Pill", "Squircle", "Organic"],
            "fill": ["Solid_Brand", "Solid_Surface", "Subtle", "Gradient_Linear", "Gradient_Mesh", "Pattern_Dot", "Noise"],
            "effect": ["Duotone", "Glitch", "Glow", "Tape", "Shadow"]
        }
        
        lines.append("\n\nSupported Preset Attributes (per widget):")
        for category, variants in presets.items():
            variants_str = ", ".join(variants)
            lines.append(f"- {category}: {variants_str}")
        
        return "\n".join(lines)

    @classmethod
    def register_strategy(cls, strategy_class: Type[Any]) -> None:
        """Register a new layout strategy.
        
        Args:
            strategy_class: Strategy class with get_strategy_name() and get_slots()
        """
        name = strategy_class.get_strategy_name()
        cls._strategies[name] = strategy_class

    @classmethod
    def _resolve_widget_style(cls, widget_style, theme: Theme, preset: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Resolve widget style by converting theme tokens to actual values.
        
        Only includes properties that are NOT controlled by presets to avoid conflicts.
        Preset-controlled properties (background, border, border-radius, box-shadow, color, filter)
        are handled entirely by preset CSS classes.
        
        Args:
            widget_style: WidgetStyle from Style config with theme token references
            theme: Theme containing actual values
            preset: Optional preset configuration (e.g., {"fill": "Solid_Brand", "shape": "Rounded"})
            
        Returns:
            Dictionary with resolved CSS properties (excluding preset-controlled ones)
        """
        resolved = {}
        preset = preset or {}
        
        # Check which preset categories are active
        has_surface = "surface" in preset
        has_shape = "shape" in preset
        has_fill = "fill" in preset
        has_effect = "effect" in preset
        
        # Resolve font (typography token) to CSS properties
        # SAFE: Typography is not controlled by presets
        if widget_style.font:
            typo_token = getattr(theme.typography, widget_style.font, None)
            if typo_token:
                resolved["font-size"] = f"{typo_token.size}px"
                # Map weight names to CSS values
                weight_map = {
                    "thin": "100",
                    "light": "300",
                    "regular": "400",
                    "medium": "500",
                    "semibold": "600",
                    "bold": "700",
                    "black": "900",
                }
                resolved["font-weight"] = weight_map.get(typo_token.weight, "400")
                if typo_token.line_height:
                    resolved["line-height"] = str(typo_token.line_height)
        
        # Resolve text alignment
        # SAFE: Text alignment is not controlled by presets
        if widget_style.align:
            resolved["text-align"] = widget_style.align
        
        # Resolve vertical alignment
        # SAFE: Vertical alignment is not controlled by presets
        if widget_style.vertical_align:
            resolved["vertical-align"] = widget_style.vertical_align
        
        # Resolve foreground color (theme color token)
        # SKIP if fill preset is active - fill presets control color
        if widget_style.foreground and not has_fill:
            color_value = getattr(theme, widget_style.foreground, None)
            if color_value:
                resolved["color"] = color_value
        
        # Resolve background color (theme color token)
        # SKIP if surface OR fill preset is active - they control background
        if widget_style.background and not (has_surface or has_fill):
            bg_value = getattr(theme, widget_style.background, None)
            if bg_value:
                resolved["background-color"] = bg_value
        
        # Apply border radius if specified
        # SKIP if shape preset is active - shape presets control border-radius
        if widget_style.border_radius and not has_shape:
            resolved["border-radius"] = widget_style.border_radius
        
        return resolved

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
        """Calculate layout with two-phase auto-layout: measurement → position calculation.

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
        from src.common.spacing_utils import parse_spacing
        from src.paged.layout.layout_protocol import LayoutContext, WidgetLayoutInput
        
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

        # ===== PHASE 1: WIDGET MEASUREMENT =====
        # Measure each widget's content size and prepare for layout
        widget_layout_inputs: List[WidgetLayoutInput] = []
        widget_instances: Dict[str, Any] = {}  # Store for later assignment creation

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

            # VALIDATE: Widget type must have a style defined in Style config
            widget_style = style.get_widget_style(widget_type)
            if widget_style is None:
                from src.common.exceptions import UCERenderError
                raise UCERenderError(
                    f"No style defined for widget type '{widget_type}'. "
                    f"All widget types must be explicitly styled in the Style config."
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

            # Resolve widget style from Style config and Theme tokens
            # Apply default preset if none specified
            preset = widget_config.get("preset")
            if not preset:
                preset = cls._default_presets.get(widget_type, {"surface": "Flat"})
            
            resolved_style = cls._resolve_widget_style(widget_style, theme, preset)

            # MEASURE: Calculate widget content size
            # This is where auto-layout measurement happens
            measured_size = widget.measure(
                style=resolved_style,
                max_width=float(width),
                max_height=float(height)
            )

            # Create layout input for Phase 2
            widget_layout_inputs.append(WidgetLayoutInput(
                role=role,
                measured_size=measured_size,
                slot=slot,
                style=resolved_style
            ))

            # Store for later
            widget_instances[role] = {
                "widget": widget,
                "slot": slot,
                "resolved_style": resolved_style,
                "preset": preset  # Pass through preset for template rendering
            }

        # ===== CREATE LAYOUT CONTEXT =====
        # Parse spacing values from theme to pixels
        margin_x_px = parse_spacing(theme.margin_x, reference=width)
        margin_y_px = parse_spacing(theme.margin_y, reference=height)
        gutter_px = parse_spacing(theme.gutter, reference=width)
        
        # Parse header/footer heights (support both px and %)
        header_height_px = parse_spacing(theme.header_footer.header_height, reference=height)
        footer_height_px = parse_spacing(theme.header_footer.footer_height, reference=height)

        context = LayoutContext(
            canvas_width=float(width),
            canvas_height=float(height),
            margin_x=margin_x_px,
            margin_y=margin_y_px,
            gutter=gutter_px,
            header_height=header_height_px,
            footer_height=footer_height_px
        )

        # ===== PHASE 2: LAYOUT CALCULATION =====
        # Call strategy's calculate_layout() to get absolute bounds
        bounds_map = strategy.calculate_layout(
            widgets=widget_layout_inputs,
            context=context
        )

        # ===== CREATE WIDGET ASSIGNMENTS WITH BOUNDS =====
        assignments: List[WidgetAssignment] = []

        for role, instance_data in widget_instances.items():
            # Get calculated bounds from Phase 2
            if role not in bounds_map:
                raise ValueError(f"Strategy {strategy_name} did not calculate bounds for role '{role}'")
            
            bounds = bounds_map[role]

            assignments.append(WidgetAssignment(
                role=role,
                widget=instance_data["widget"],
                slot=instance_data["slot"],
                applied_style=instance_data["resolved_style"],
                bounds=bounds,  # Absolute position from auto-layout
                preset=instance_data["preset"]  # Pass through preset for template rendering
            ))

        # Create renderable layout with theme-derived properties
        return RenderableLayout(
            strategy_name=strategy_name,
            widget_assignments=assignments,
            theme_vars=theme.to_css_vars(),
            style_props={},  # Style properties now applied per-widget via applied_style
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
                strategy_name=slide.layout,
                widget_assignments=slide.widgets,
                theme=theme,
                style=slide_style,
                width=width,
                height=height,
            )

            # Process header widget if provided
            if slide.header:
                header_widget_type = slide.header.get("type")
                if header_widget_type:
                    header_widget_class = WidgetRegistry.get(header_widget_type)
                    if header_widget_class:
                        # Apply default preset if none specified
                        header_preset = slide.header.get("preset")
                        if not header_preset:
                            header_preset = cls._default_presets.get(header_widget_type, {"surface": "Flat"})
                        
                        # Resolve style with preset awareness
                        header_widget_style = slide_style.get_widget_style(header_widget_type)
                        header_resolved_style = cls._resolve_widget_style(header_widget_style, theme, header_preset) if header_widget_style else {}
                        
                        layout.header_widget = header_widget_class(
                            atom_id=slide.header.get("atom_id"),
                            parameters=slide.header.get("parameters", {})
                        )
                        # Store preset and style for rendering
                        layout.header_preset = header_preset
                        layout.header_style = header_resolved_style

            # Process footer widget if provided
            if slide.footer:
                footer_widget_type = slide.footer.get("type")
                if footer_widget_type:
                    footer_widget_class = WidgetRegistry.get(footer_widget_type)
                    if footer_widget_class:
                        # Apply default preset if none specified
                        footer_preset = slide.footer.get("preset")
                        if not footer_preset:
                            footer_preset = cls._default_presets.get(footer_widget_type, {"surface": "Flat"})
                        
                        # Resolve style with preset awareness
                        footer_widget_style = slide_style.get_widget_style(footer_widget_type)
                        footer_resolved_style = cls._resolve_widget_style(footer_widget_style, theme, footer_preset) if footer_widget_style else {}
                        
                        layout.footer_widget = footer_widget_class(
                            atom_id=slide.footer.get("atom_id"),
                            parameters=slide.footer.get("parameters", {})
                        )
                        # Store preset and style for rendering
                        layout.footer_preset = footer_preset
                        layout.footer_style = footer_resolved_style

            # Apply sequence pattern background if configured
            if theme.sequence_pattern:
                layout.background_override = theme.get_slide_background(slide_index)

            # Add slide metadata
            layout.slide_number = slide_index + 1
            layout.total_slides = len(active_slides)
            layout.slide_id = slide.id
            
            # Pass strategy-specific parameters
            layout.parameters = slide.parameters

            renderable_layouts.append(layout)

        return renderable_layouts

    @classmethod
    def get_layout_constrain(cls) -> str:
        """Provide dummy layout-widget compatibility constraints.
        
        Returns:
            Formatted string describing widget-layout compatibility rules.
            For the dummy engine, returns basic placeholder constraints.
        """
        return """LAYOUT-WIDGET COMPATIBILITY:

Widget Space Requirements:
- All widgets fit in all slots (dummy engine has no constraints)

Layout Slot Constraints:
- All slots can accommodate any widget type
- No character limits or width restrictions

Compatibility Rules:
- ✅ All widget-layout combinations are allowed
- No validation performed in dummy engine

Note: This is a placeholder for the dummy layout engine. Real engines
(like Slidev) provide specific constraints based on their layout implementations.
"""
