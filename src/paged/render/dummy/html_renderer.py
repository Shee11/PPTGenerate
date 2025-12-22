"""HTML renderer for converting RenderableLayout to HTML."""
import re
from pathlib import Path
from typing import List, Optional, Union, Dict, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.common.renderable_layout import RenderableLayout
from src.common.spacing_utils import parse_spacing
from src.paged.render.dummy.preset_defaults import PRESET_DEFAULTS, generate_preset_css_variables, generate_preset_css


class HTMLRenderer:
    """Renderer that converts RenderableLayout to HTML using Jinja2 templates.
    
    Supports both single-slide and multi-slide rendering with navigation.
    """

    def __init__(self, template_dir: Optional[Path] = None, presets: Optional[Dict[str, Any]] = None):
        """Initialize HTML renderer.
        
        Args:
            template_dir: Directory containing Jinja2 templates.
                         Defaults to src/render/templates/
            presets: Custom preset configuration. Merged with PRESET_DEFAULTS.
        """
        if template_dir is None:
            # Default to templates directory relative to this file
            current_file = Path(__file__)
            template_dir = current_file.parent / "templates"

        self.template_dir = template_dir
        
        # Merge custom presets with defaults (custom overrides defaults)
        self.presets = self._merge_presets(PRESET_DEFAULTS, presets or {})

        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # Register custom filters
        self.env.filters['markdown_format'] = self._markdown_format
        
        # Generate preset CSS content in-memory (no file dependency)
        self.presets_css_content = generate_preset_css()

    @staticmethod
    def _markdown_format(text: str) -> str:
        """Convert markdown-style formatting to HTML with theme styling.
        
        Converts:
        - ==highlight== to <mark style="background-color: var(--color-accent); color: var(--color-text); padding: 0 0.2em;">highlight</mark>
        - **bold** to <strong style="color: var(--color-accent); font-weight: bold;">bold</strong>
        
        Args:
            text: Text with markdown formatting
            
        Returns:
            HTML string with styled spans
        """
        if text is None:
            return ""
        
        # Convert to string if not already (handles int, float, etc.)
        if not isinstance(text, str):
            text = str(text)
        
        # Convert ==highlight== to styled mark
        text = re.sub(
            r'==(.*?)==',
            r'<mark style="background-color: var(--color-accent); color: var(--color-text); padding: 0 0.2em; border-radius: 3px;">\1</mark>',
            text
        )
        
        # Convert **bold** to styled strong
        text = re.sub(
            r'\*\*(.*?)\*\*',
            r'<strong style="color: var(--color-accent); font-weight: bold;">\1</strong>',
            text
        )
        
        return text

    @staticmethod
    def _merge_presets(defaults: Dict[str, Any], custom: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge custom preset configuration with defaults.
        
        Args:
            defaults: Default preset configuration (from PRESET_DEFAULTS)
            custom: Custom preset overrides from layout config
            
        Returns:
            Merged preset configuration (custom values override defaults)
        """
        import copy
        merged = copy.deepcopy(defaults)
        
        for category, variants in custom.items():
            if category not in merged:
                merged[category] = {}
            
            if isinstance(variants, dict):
                for variant, tokens in variants.items():
                    if variant not in merged[category]:
                        merged[category][variant] = {}
                    
                    if isinstance(tokens, dict):
                        # Merge tokens for this variant
                        merged[category][variant].update(tokens)
                    else:
                        # Replace entire variant
                        merged[category][variant] = tokens
            else:
                # Replace entire category
                merged[category] = variants
        
        return merged

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

    def render_single_slide(self, renderable: RenderableLayout, slide_index: int = None) -> str:
        """Render a single RenderableLayout to HTML.
        
        Args:
            renderable: Layout with all widget assignments and styling
            slide_index: Optional 1-based slide index for CSS scoping in multi-slide presentations
            
        Returns:
            Complete HTML string
        """
        # Select layout template based on strategy
        layout_template_name = self._get_layout_template(renderable.strategy_name)

        # Load template
        template = self.env.get_template(layout_template_name)

        # Prepare widget data for template
        widget_data = {}
        
        # Parse margin values (they are strings like "70px" or "5%")
        margin_x_value = parse_spacing(renderable.margin_x, reference=renderable.width)
        margin_y_value = parse_spacing(renderable.margin_y, reference=renderable.height)
        header_height_value = parse_spacing(renderable.header_height, reference=renderable.height)
        
        for assignment in renderable.widget_assignments:
            # Convert absolute bounds to relative bounds (relative to layout container)
            # Layout container is positioned at (margin_x, margin_y + header_height)
            relative_bounds = {
                "x": assignment.bounds.x - margin_x_value,
                "y": assignment.bounds.y - margin_y_value - header_height_value,
                "width": assignment.bounds.width,
                "height": assignment.bounds.height,
            }
            
            widget_data[assignment.role] = {
                "type": assignment.widget.get_widget_type(),
                "data": assignment.widget.render_data(),
                "size": str(assignment.slot.size),
                "applied_style": assignment.applied_style,  # Pass resolved styles
                "bounds": assignment.bounds,  # Keep absolute bounds for reference
                "relative_bounds": relative_bounds,  # Add relative bounds for positioning
                "preset": assignment.preset,  # Pass preset for template styling
            }

        # Prepare header/footer widget data
        header_widget_data = None
        if renderable.header_widget:
            header_widget_data = {
                "type": renderable.header_widget.get_widget_type(),
                "data": renderable.header_widget.render_data(),
                "preset": renderable.header_preset or {},
                "style": renderable.header_style or {},
            }

        footer_widget_data = None
        if renderable.footer_widget:
            footer_widget_data = {
                "type": renderable.footer_widget.get_widget_type(),
                "data": renderable.footer_widget.render_data(),
                "preset": renderable.footer_preset or {},
                "style": renderable.footer_style or {},
            }

        # Render template
        html = template.render(
            strategy=renderable.strategy_name,
            widgets=widget_data,
            header_widget=header_widget_data,
            footer_widget=footer_widget_data,
            theme_vars=renderable.theme_vars,
            preset_vars=generate_preset_css_variables(self.presets),  # Generate preset CSS variables
            presets_css=self.presets_css_content,  # Embed presets.css content
            style_props=renderable.style_props,
            canvas_width=renderable.width,
            canvas_height=renderable.height,
            slide_index=slide_index,
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
            # Strategy parameters
            parameters=getattr(renderable, 'parameters', {}),
        )

        return html

    def _extract_slide_parts(self, html: str) -> dict:
        """Extract CSS and body content from a single slide HTML.
        
        Args:
            html: Complete HTML document from render_single_slide
            
        Returns:
            Dict with 'layout_styles' (layout-specific CSS) and 'body_content' (layout-container div)
        """
        # Extract layout-specific styles (between {% block layout_styles %} markers)
        # These are the styles that come after typography definitions
        layout_styles_match = re.search(
            r'/\*.*?Typography tokens from theme.*?\*/.*?</style>',
            html,
            re.DOTALL
        )
        
        layout_styles = ''
        if layout_styles_match:
            # Extract everything after the caption style and before </style>
            after_caption = html[layout_styles_match.end() - 8:]  # -8 to go back before </style>
            # Find the actual layout styles (starts after "caption, small" block)
            caption_end = html.rfind('.caption, small', 0, layout_styles_match.end())
            if caption_end != -1:
                # Find the closing brace of caption block
                closing_brace = html.find('}', caption_end)
                if closing_brace != -1:
                    # Extract from after caption block to </style>
                    style_start = closing_brace + 1
                    style_end = html.find('</style>', style_start)
                    if style_end != -1:
                        layout_styles = html[style_start:style_end].strip()
        
        # Extract body content (the .layout-container div)
        body_match = re.search(
            r'<div class="layout-container"[^>]*>.*?</div>\s*</body>',
            html,
            re.DOTALL
        )
        
        body_content = ''
        if body_match:
            body_content = body_match.group(0)
            # Remove the closing </body> tag
            body_content = body_content.replace('</body>', '').strip()
        
        return {
            'layout_styles': layout_styles,
            'body_content': body_content,
        }

    def render_multi_slide(self, renderables: List[RenderableLayout]) -> str:
        """Render multiple slides with navigation.
        
        Args:
            renderables: List of RenderableLayout instances
            
        Returns:
            Complete HTML with slide deck and navigation
        """
        if not renderables:
            raise ValueError("Cannot render empty slide list")

        # Render each slide and extract CSS + body content
        slides_data = []
        all_slide_styles = []  # Collect all layout-specific CSS
        
        for i, renderable in enumerate(renderables):
            # Render complete HTML for this slide
            slide_html = self.render_single_slide(renderable, slide_index=i+1)
            
            # Extract CSS and body content
            parts = self._extract_slide_parts(slide_html)
            
            slides_data.append({
                'index': i,
                'body_content': parts['body_content'],
                'id': renderable.slide_id or f"slide-{i+1}",
                'strategy': renderable.strategy_name,
                'background': renderable.background_override,
            })
            
            # Collect layout-specific CSS
            if parts['layout_styles']:
                all_slide_styles.append(parts['layout_styles'])

        # Load multi-slide template
        template = self.env.get_template("multi_slide.html.j2")

        # Render with navigation
        html = template.render(
            slides=slides_data,
            all_slide_styles='\n'.join(all_slide_styles),
            total_slides=len(renderables),
            canvas_width=renderables[0].width,
            canvas_height=renderables[0].height,
            theme_vars=renderables[0].theme_vars,  # Use first slide's theme
            preset_vars=generate_preset_css_variables(self.presets),  # Generate preset CSS variables
            presets_css=self.presets_css_content,  # Embed presets.css content
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
