"""
Renderer API Contract: React MDX Renderer

This file defines the Python API contract for the React MDX renderer.
It specifies the interface for converting state.json to MDX format.
"""

from typing import Protocol, TypedDict, Literal, NotRequired
from pathlib import Path


# =============================================================================
# TYPE DEFINITIONS (matching state.json schema)
# =============================================================================

class SlideParameters(TypedDict):
    """Slide styling parameters."""
    theme: str
    vibe: Literal['minimal', 'clean', 'balanced', 'decorative', 'expressive']
    background: NotRequired[str]


class WidgetParameters(TypedDict, total=False):
    """Common widget parameters (varies by type)."""
    text: str
    level: int
    items: list[str]
    src: str
    alt: str
    value: str
    label: str
    change: float
    changeLabel: str
    chartType: Literal['bar', 'line', 'pie', 'donut']
    title: str
    data: dict
    columns: list[str]
    rows: list[list[str]]


class Widget(TypedDict):
    """Widget definition in state.json."""
    type: str  # e.g., "Type.Display", "Type.List"
    parameters: WidgetParameters


class Slide(TypedDict):
    """Slide definition in state.json."""
    id: str
    rank: int
    layout: str
    widgets: dict[str, Widget]
    parameters: SlideParameters
    # Optional metadata
    state: NotRequired[str]
    story: NotRequired[str]
    density: NotRequired[str]


class StateJson(TypedDict):
    """Root state.json structure."""
    meta: dict
    constitution: dict
    themes: dict[str, dict]
    active_theme_id: str
    project: str
    slides: list[Slide]


# =============================================================================
# RENDERER PROTOCOL
# =============================================================================

class ReactMDXRendererProtocol(Protocol):
    """
    Protocol for React MDX renderer implementation.
    
    Converts state.json to MDX format that can be rendered
    by the React/Next.js frontend.
    """
    
    def render_state(
        self,
        state: StateJson,
        output_dir: Path | None = None,
    ) -> list[Path]:
        """
        Render complete state.json to MDX files.
        
        Args:
            state: Parsed state.json content
            output_dir: Directory for output files. If None, uses default.
            
        Returns:
            List of generated MDX file paths
            
        Raises:
            ValidationError: If state.json is invalid
            RenderError: If MDX generation fails
        """
        ...
    
    def render_slide(self, slide: Slide) -> str:
        """
        Render a single slide to MDX string.
        
        Args:
            slide: Slide definition from state.json
            
        Returns:
            MDX string for the slide
            
        Raises:
            ValidationError: If slide is invalid
        """
        ...
    
    def render_widget(
        self,
        widget_type: str,
        parameters: WidgetParameters,
    ) -> str:
        """
        Render a single widget to MDX component string.
        
        Args:
            widget_type: Widget type (e.g., "Type.Display")
            parameters: Widget parameters
            
        Returns:
            MDX component string (e.g., "<Heading level={1}>...</Heading>")
        """
        ...
    
    def validate_slide(self, slide: Slide) -> list[str]:
        """
        Validate a slide definition.
        
        Args:
            slide: Slide definition to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        ...
    
    def build(
        self,
        mdx_dir: Path,
        output_dir: Path,
    ) -> Path:
        """
        Build MDX files to static HTML.
        
        Args:
            mdx_dir: Directory containing MDX files
            output_dir: Directory for HTML output
            
        Returns:
            Path to output directory
            
        Raises:
            BuildError: If Next.js build fails
        """
        ...


# =============================================================================
# COMPONENT MAPPING
# =============================================================================

# Maps state.json widget types to React MDX components
COMPONENT_MAP: dict[str, tuple[str, dict]] = {
    # L3: Atoms (Typography)
    "Type.Display": ("Heading", {"level": 1}),
    "Type.Heading": ("Heading", {}),
    "Type.Body": ("Text", {"variant": "default"}),
    "Type.Caption": ("Text", {"variant": "caption"}),
    "Type.Note": ("Callout", {"intent": "info"}),
    
    # L2: Blocks (Content)
    "Type.List": ("SmartList", {}),
    "Type.Quote": ("QuoteBlock", {}),
    "Type.Image": ("ImageBlock", {}),
    
    # L2: Blocks (Data)
    "Type.Metric": ("MetricGroup", {}),
    "Type.BigNumber": ("MetricGroup", {}),
    "Type.Chart": ("ChartBar", {}),  # Default to bar
    "Type.Table": ("TableData", {}),
}

# Maps state.json layout types to React MDX layout components
LAYOUT_MAP: dict[str, str] = {
    "cover": "LayoutCover",
    "split": "LayoutSplit",
    "stacked": "LayoutGrid",
    "grid": "LayoutGrid",
    "full-bleed": "LayoutFullBleed",
    "timeline": "LayoutTimeline",
    "dashboard": "LayoutDashboard",
    "quote-hero": "LayoutCover",  # Map to cover with quote styling
    "spotlight": "LayoutFullBleed",
}

# Maps slot names to compound component slots
SLOT_MAP: dict[str, dict[str, str]] = {
    "LayoutSplit": {
        "left": "Left",
        "right": "Right",
    },
    "LayoutGrid": {
        "col1": "Col",
        "col2": "Col",
        "col3": "Col",
        "col4": "Col",
        "content": "Col",  # For stacked layout
    },
    "LayoutTimeline": {
        "header": "Header",
        "step1": "Step",
        "step2": "Step",
        "step3": "Step",
        "step4": "Step",
    },
    "LayoutDashboard": {
        "header": "Header",
        "stat1": "Metric",
        "stat2": "Metric",
        "stat3": "Metric",
        "stat4": "Metric",
        "chart": "Chart",
    },
}


# =============================================================================
# ERROR TYPES
# =============================================================================

class ValidationError(Exception):
    """Raised when state.json validation fails."""
    
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__(f"Validation failed: {', '.join(errors)}")


class RenderError(Exception):
    """Raised when MDX rendering fails."""
    
    def __init__(self, message: str, slide_id: str | None = None):
        self.slide_id = slide_id
        super().__init__(f"Render failed{f' for {slide_id}' if slide_id else ''}: {message}")


class BuildError(Exception):
    """Raised when Next.js build fails."""
    
    def __init__(self, message: str, stderr: str | None = None):
        self.stderr = stderr
        super().__init__(f"Build failed: {message}")


# =============================================================================
# CLI INTEGRATION
# =============================================================================

# CLI options for react-mdx renderer
CLI_OPTIONS = {
    "project": "react-mdx",
    "description": "React MDX presentation renderer",
    "flags": {
        "--validate-only": "Validate state.json without rendering",
        "--no-build": "Generate MDX files without building to HTML",
        "--theme": "Override theme for all slides",
        "--verbose": "Show detailed progress and debug info",
    },
}
