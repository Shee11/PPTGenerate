"""HTML renderer for converting RenderableLayout to HTML."""
from pathlib import Path
from typing import List, Optional, Union

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.common.renderable_layout import RenderableLayout


class HTMLRenderer:
    """Renderer that converts RenderableLayout to HTML using Jinja2 templates.
    
    Supports both single-slide and multi-slide rendering with navigation.
    """

    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize HTML renderer.
        
        Args:
            template_dir: Directory containing Jinja2 templates.
                         Defaults to src/render/templates/
        """
        if template_dir is None:
            # Default to templates directory relative to this file
            current_file = Path(__file__)
            template_dir = current_file.parent / "templates"

        self.template_dir = template_dir

        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, renderable: Union[RenderableLayout, List[RenderableLayout]]) -> str:
        """Render layout(s) to HTML.
        
        Args:
            renderable: Single RenderableLayout or list of RenderableLayouts for multi-slide
            
        Returns:
            Complete HTML string (single slide or multi-slide with navigation)
        """
        if isinstance(renderable, list):
            return self.render_multi_slide(renderable)
        else:
            return self.render_single_slide(renderable)

    def render_single_slide(self, renderable: RenderableLayout) -> str:
        """Render a single RenderableLayout to HTML.
        
        Args:
            renderable: Layout with all widget assignments and styling
            
        Returns:
            Complete HTML string
        """
        # Select layout template based on strategy
        layout_template_name = self._get_layout_template(renderable.strategy_name)

        # Load template
        template = self.env.get_template(layout_template_name)

        # Prepare widget data for template
        widget_data = {}
        for assignment in renderable.widget_assignments:
            widget_data[assignment.role] = {
                "type": assignment.widget.get_widget_type(),
                "data": assignment.widget.render_data(),
                "size": str(assignment.slot.size),
            }

        # Render template
        html = template.render(
            strategy=renderable.strategy_name,
            widgets=widget_data,
            theme_vars=renderable.theme_vars,
            style_props=renderable.style_props,
            canvas_width=renderable.width,
            canvas_height=renderable.height,
            # Pass theme-derived layout properties
            margin_x=renderable.margin_x,
            margin_y=renderable.margin_y,
            gutter=renderable.gutter,
            # Pass header/footer configuration
            header_height=renderable.header_height,
            footer_height=renderable.footer_height,
            header_position=renderable.header_position,
            footer_position=renderable.footer_position,
            header_decoration=renderable.header_decoration,
            footer_decoration=renderable.footer_decoration,
            # Slide metadata
            slide_number=renderable.slide_number,
            total_slides=renderable.total_slides,
            slide_id=renderable.slide_id,
            background_override=renderable.background_override,
        )

        return html

    def render_multi_slide(self, renderables: List[RenderableLayout]) -> str:
        """Render multiple slides with navigation.
        
        Args:
            renderables: List of RenderableLayout instances
            
        Returns:
            Complete HTML with slide deck and navigation
        """
        if not renderables:
            raise ValueError("Cannot render empty slide list")

        # Render each slide
        slides_html = []
        for i, renderable in enumerate(renderables):
            slide_html = self.render_single_slide(renderable)
            slides_html.append({
                'index': i,
                'html': slide_html,
                'id': renderable.slide_id or f"slide-{i+1}",
                'strategy': renderable.strategy_name,
            })

        # Load multi-slide template
        template = self.env.get_template("multi_slide.html.j2")

        # Render with navigation
        html = template.render(
            slides=slides_html,
            total_slides=len(renderables),
            canvas_width=renderables[0].width,
            canvas_height=renderables[0].height,
            theme_vars=renderables[0].theme_vars,  # Use first slide's theme
        )

        return html

    def _get_layout_template(self, strategy_name: str) -> str:
        """Map strategy name to template file.
        
        Args:
            strategy_name: Strategy name (e.g., "Bento.Standard")
            
        Returns:
            Template file path relative to template_dir
        """
        # Extract strategy family and variant
        if "." in strategy_name:
            family, variant = strategy_name.split(".", 1)
            family_lower = family.lower()

            # Map to template file
            return f"layouts/{family_lower}.html.j2"

        # Fallback to base template
        return "base.html.j2"
