"""Slidev markdown renderer implementation."""
import yaml
import subprocess
import tempfile
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def resolve_theme(primary_color: str | None) -> str:
    """Resolve hex color to semantic theme name.
    
    Maps primary colors from slide JSON to Slidev theme names:
    - #2563eb (blue) → "business"
    - #00ffa3 (neon green) → "cyber"
    - Unknown/None → "business" (default)
    
    Args:
        primary_color: Hex color string (e.g., "#2563eb") or None
        
    Returns:
        str: Theme name ("business" or "cyber")
        
    Examples:
        >>> resolve_theme("#2563eb")
        'business'
        >>> resolve_theme("#00ffa3")
        'cyber'
        >>> resolve_theme(None)
        'business'
    """
    if not primary_color:
        return "business"
    
    # Normalize to lowercase for case-insensitive matching
    color_lower = primary_color.lower()
    
    # Theme color mappings
    THEME_COLORS = {
        "#2563eb": "business",  # Blue primary
        "#00ffa3": "cyber",     # Neon green primary
    }
    
    return THEME_COLORS.get(color_lower, "business")


class SlidevRenderer:
    """Renderer for transforming slide JSON to Slidev markdown format.
    
    Converts slide JSON (from content generation) to Slidev-compatible
    markdown with frontmatter and slot syntax.
    
    Architecture:
    - Source: slidev-project/ (layouts, components - source controlled)
    - Build: slidev_build/ (temporary directory, auto-generated)
    
    Supports:
    - Custom Vue layouts (slidev-project/layouts/*.vue):
      smart-grid, hero-split, full-bleed, feature-grid, comparison, timeline, dashboard
    
    - Custom Vue components (slidev-project/components/*.vue):
      ChartWidget, TableWidget, QuoteWidget, MetricWidget
    
    - Slidev built-in layouts:
      default, center, cover, end, fact, image, image-left, image-right,
      intro, quote, section, statement, two-cols, two-cols-header
    """
    
    def __init__(self):
        """Initialize renderer with Jinja2 templates and build directory."""
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            cache_size=100  # Performance optimization
        )
        
        # Load templates
        self.frontmatter_template = self.env.get_template("frontmatter.j2")
        self.slot_template = self.env.get_template("slot.j2")
        self.slide_template = self.env.get_template("slide.j2")
        
        # Setup persistent build directory
        self.build_dir = Path(__file__).parent.parent.parent.parent / "slidev_build"
        self._ensure_build_env()
        
        # Setup persistent build directory
        self.build_dir = Path(__file__).parent.parent.parent.parent / "slidev_build"
        self._ensure_build_env()
    
    def _ensure_build_env(self):
        """Ensure Slidev build environment is set up (run once)."""
        package_json = self.build_dir / "package.json"
        
        # Copy layouts and components from source (slidev-project) to build directory
        source_dir = Path(__file__).parent.parent.parent.parent / "slidev-project"
        self._copy_layouts_and_components(source_dir)
        
        # Skip npm install if already initialized
        if package_json.exists():
            return
        
        print(f"Setting up Slidev build environment in {self.build_dir}...")
        self.build_dir.mkdir(parents=True, exist_ok=True)
        
        # Create package.json with bundling tools
        package_data = {
            "name": "slidev-build-env",
            "type": "module",
            "dependencies": {
                "@slidev/cli": "latest",
                "@slidev/theme-default": "latest",
                "playwright-chromium": "latest",
                "vue": "^3"
            },
            "devDependencies": {
                "inline-source-cli": "latest"
            }
        }
        package_json.write_text(
            __import__('json').dumps(package_data, indent=2),
            encoding='utf-8'
        )
        
        # Install dependencies
        npm_cmd = "npm.cmd" if Path("C:\\Windows").exists() else "npm"
        print("Installing dependencies (this may take a minute)...")
        result = subprocess.run(
            [npm_cmd, "install"],
            cwd=self.build_dir,
            capture_output=True,
            timeout=300
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"npm install failed: {result.stderr.decode()}")
        
        print("Build environment ready")
    
    def _copy_layouts_and_components(self, source_dir: Path):
        """Copy layouts and components from slidev-project to build directory.
        
        Args:
            source_dir: Path to slidev-project directory
        """
        if not source_dir.exists():
            print(f"Warning: Source directory {source_dir} not found, skipping layout/component copy")
            return
        
        # Copy layouts
        source_layouts = source_dir / "layouts"
        if source_layouts.exists():
            dest_layouts = self.build_dir / "layouts"
            dest_layouts.mkdir(parents=True, exist_ok=True)
            
            for layout_file in source_layouts.glob("*.vue"):
                shutil.copy2(layout_file, dest_layouts / layout_file.name)
        
        # Copy components
        source_components = source_dir / "components"
        if source_components.exists():
            dest_components = self.build_dir / "components"
            dest_components.mkdir(parents=True, exist_ok=True)
            
            for component_file in source_components.glob("*.vue"):
                shutil.copy2(component_file, dest_components / component_file.name)
            
            # Also copy README if present
            readme = source_components / "README.md"
            if readme.exists():
                shutil.copy2(readme, dest_components / "README.md")
    
    def render(self, renderable):
        """Render slide JSON to full HTML via Slidev build process.
        
        Args:
            renderable: Single slide dict or list of slide dicts
            
        Returns:
            str: Complete HTML page built by Slidev/Vue
        """
        # Generate markdown content
        markdown_content = self.render_to_markdown(renderable)
        
        # Build HTML using Slidev toolchain
        return self.render_to_html(markdown_content)
    
    def render_to_markdown(self, renderable):
        """Render slide JSON to Slidev markdown (intermediate format).
        
        Args:
            renderable: Single slide dict or list of slide dicts
            
        Returns:
            str: Slidev markdown content
        """
        if isinstance(renderable, list):
            return self.render_multi_slide(renderable)
        else:
            return self.render_single_slide(renderable)
    
    def render_single_slide(self, slide: dict) -> str:
        """Render single slide to markdown.
        
        Args:
            slide: Slide JSON dict with layout, widgets, theme
            
        Returns:
            str: Markdown for one slide
        
        Raises:
            ValueError: If layout or widgets fields are missing
        """
        # Validation
        if "layout" not in slide:
            raise ValueError("Slide JSON must include 'layout' field")
        if "widgets" not in slide:
            raise ValueError("Slide JSON must include 'widgets' field")
        
        # Generate frontmatter
        frontmatter = self._generate_frontmatter(slide)
        
        # Render widgets - different handling based on layout
        widgets = slide.get("widgets", {})
        layout = slide.get("layout", "default")
        
        # Layouts with named slots (use slot syntax)
        SLOT_LAYOUTS = {
            "two-cols", "two-cols-header", "hero-split", 
            "smart-grid", "feature-grid", "comparison", "timeline", "dashboard"
        }
        
        if layout in SLOT_LAYOUTS:
            # Render each widget with its slot name
            slots_content = []
            for slot_name, widget_data in widgets.items():
                widget_content = self._render_widget(widget_data)
                
                # Use slot syntax (::slotname::) - note the blank line after
                slot_md = f"::{slot_name}::\n\n{widget_content}"
                slots_content.append(slot_md)
            
            # Join slots without extra separators (each already has ::slotname::)
            slots_combined = "\n\n".join(slots_content)
        else:
            # For layouts without slots (cover, quote, etc.), combine all widgets
            widget_contents = []
            for slot_name, widget_data in widgets.items():
                widget_content = self._render_widget(widget_data)
                widget_contents.append(widget_content)
            slots_combined = "\n\n".join(widget_contents)
        
        # Combine frontmatter + slots
        return f"{frontmatter}\n\n{slots_combined}"
    
    def render_multi_slide(self, slides: list) -> str:
        """Render multiple slides to markdown.
        
        Args:
            slides: List of slide JSON dicts
            
        Returns:
            str: Complete multi-slide markdown with slide separators
        """
        if not slides:
            return ""
        
        # Extract theme colors from first slide
        theme_data = slides[0].get("theme", {}) if slides else {}
        primary_color = theme_data.get("primary_color", "#2563eb")
        background_color = theme_data.get("background_color", "#ffffff")
        text_color = theme_data.get("text_color", "#1f2937")
        
        # Generate custom CSS for theme colors
        theme_css = f"""
<style>
:root {{
  --slidev-theme-primary: {primary_color};
  --slidev-theme-background: {background_color};
  --slidev-theme-text: {text_color};
}}

/* Apply theme colors */
.slidev-layout {{
  background-color: var(--slidev-theme-background);
  color: var(--slidev-theme-text);
}}

/* Primary color accents */
h1, h2, h3, h4, h5, h6 {{
  color: var(--slidev-theme-primary);
}}

/* Links */
a {{
  color: var(--slidev-theme-primary);
}}

/* Code blocks */
.shiki {{
  background-color: rgba(0, 0, 0, 0.05) !important;
}}

/* Custom layout backgrounds */
.smart-grid .grid-column,
.feature-grid .feature-box,
.comparison .comparison-side,
.timeline .step-marker,
.dashboard .metric-card {{
  border-color: var(--slidev-theme-primary);
}}

.timeline .step-marker {{
  background-color: var(--slidev-theme-primary);
}}
</style>
"""
        
        global_frontmatter = f"""---
theme: default
background: {background_color}
class: text-center
highlighter: shiki
lineNumbers: true
info: |
  ## Presentation
  Generated by UCE Render
drawings:
  persist: false
transition: slide-left
title: Presentation
mdc: true
fonts:
  sans: 'Avenir Next'
  serif: 'Georgia'
  mono: 'Fira Code'
colorSchema: auto
---

{theme_css}

"""
        
        # Render each slide individually
        rendered_slides = [self.render_single_slide(slide) for slide in slides]
        
        # Join slides - each already ends with --- from frontmatter, so just use blank lines
        # Slidev separates slides with "---" on its own line, which is the closing of one
        # frontmatter and works as separator to the next slide's opening "---"
        slides_content = "\n\n".join(rendered_slides)
        
        # Combine global frontmatter with slides
        return global_frontmatter + slides_content
    
    def render_to_html(self, markdown_content: str) -> str:
        """Build HTML using Slidev/Vue toolchain.
        
        Uses persistent build environment, writes markdown to temp file,
        exports single HTML file, and returns the content.
        
        Args:
            markdown_content: Slidev markdown with frontmatter and slots
            
        Returns:
            str: Complete single-file HTML page built by Slidev/Vue
            
        Raises:
            RuntimeError: If Slidev build/export fails
        """
        # Write markdown to temp slides.md in build directory
        slides_md = self.build_dir / "slides.md"
        slides_md.write_text(markdown_content, encoding='utf-8')
        
        # Clean dist directory if exists
        dist_dir = self.build_dir / "dist"
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        
        try:
            # Use npx.cmd on Windows, npx on Unix
            npx_cmd = "npx.cmd" if Path("C:\\Windows").exists() else "npx"
            
            print(f"Building slides with Slidev...")
            # Build SPA with base path ./
            result = subprocess.run(
                [npx_cmd, "@slidev/cli", "build", "slides.md", "--base", "./", "--out", "dist"],
                cwd=self.build_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                print(f"Slidev build stderr: {result.stderr}")
                raise RuntimeError(f"Slidev build failed with exit code {result.returncode}")
            
            # Read built HTML from dist/index.html
            index_html = dist_dir / "index.html"
            if not index_html.exists():
                raise RuntimeError("Slidev build did not produce dist/index.html")
            
            # Inline all assets into single HTML file
            print("Inlining assets into single HTML file...")
            inlined_html = dist_dir / "index.inlined.html"
            
            # Slidev uses dynamic ES module imports (code splitting) which cannot be fully inlined
            # We need to copy the entire dist directory for the imports to work
            
            # Option 1: Try inline-source (will inline CSS/JS but not dynamic imports)
            # node_cmd = "node.exe" if Path("C:\\Windows").exists() else "node"
            # inline_script = self.build_dir / "inline.mjs"
            
            # For now, just use the built dist directory as-is
            # User must serve via HTTP server or copy entire dist folder
            
            html_content = index_html.read_text(encoding='utf-8')
            print(f"Generated Slidev HTML ({len(html_content)} chars)")
            print(f"Note: Slidev uses ES modules and requires serving via HTTP server")
            print(f"   To view: python -m http.server 8000 --directory '{dist_dir}' then open http://localhost:8000/")
            print(f"   Or copy entire '{dist_dir}' folder to web server")
            
            return html_content
            
        except FileNotFoundError:
            raise RuntimeError(
                "npx not found. Please install Node.js and ensure npx is in PATH."
            )
    
    def _generate_frontmatter(self, slide: dict) -> str:
        """Generate YAML frontmatter from slide JSON.
        
        Args:
            slide: Slide JSON dict
            
        Returns:
            str: YAML frontmatter wrapped in ---
        """
        frontmatter_data = {}
        
        # Use layout name directly - supports both custom Vue layouts and Slidev built-ins
        layout = slide.get("layout", "default")
        frontmatter_data["layout"] = layout
        # Don't add theme to frontmatter - Slidev interprets it as theme package name
        # Instead, we'll use default theme and CSS variables for styling
        
        # Add parameters (cols, ratio, align, etc.)
        if "parameters" in slide:
            frontmatter_data.update(slide["parameters"])
        
        # Convert to YAML
        yaml_content = yaml.dump(frontmatter_data, default_flow_style=False, sort_keys=False)
        return f"---\n{yaml_content}---"
    
    def _render_widget(self, widget_data) -> str:
        """Dispatch widget rendering based on type.
        
        Args:
            widget_data: Widget object or dict
            
        Returns:
            str: Rendered markdown or Vue component
        """
        # Handle widget objects (from existing codebase)
        if hasattr(widget_data, "widget_type"):
            widget_type = widget_data.widget_type
            parameters = widget_data.parameters if hasattr(widget_data, "parameters") else {}
        # Handle plain dicts (for testing)
        elif isinstance(widget_data, dict):
            widget_type = widget_data.get("type", "")
            parameters = widget_data
        else:
            return str(widget_data)
        
        # Dispatch based on type prefix
        if widget_type.startswith("Type."):
            return self._render_typography_widget(widget_type, parameters, widget_data)
        elif widget_type.startswith("Data."):
            return self._render_data_widget(widget_type, parameters, widget_data)
        else:
            # Fallback: return text if available
            return parameters.get("text", str(widget_data))
    
    def _render_typography_widget(self, widget_type: str, parameters: dict, widget_data) -> str:
        """Render typography widgets as markdown.
        
        Args:
            widget_type: Widget type string (e.g., "Type.Display")
            parameters: Widget parameters dict
            widget_data: Original widget object
            
        Returns:
            str: Markdown text
        """
        text = parameters.get("text", "")
        
        if widget_type == "Type.Display":
            # Plain text for display
            return text
        
        elif widget_type == "Type.Heading":
            # Markdown heading
            level = parameters.get("level", 1)
            prefix = "#" * level
            return f"{prefix} {text}"
        
        elif widget_type == "Type.Body":
            # Paragraph with markdown preserved
            return text
        
        elif widget_type == "Type.List":
            # Bullet list
            items = parameters.get("items", [])
            return "\n".join([f"- {item}" for item in items])
        
        elif widget_type == "Type.Quote":
            # Blockquote
            return f"> {text}"
        
        elif widget_type == "Type.Code":
            # Code block
            code = parameters.get("code", text)
            language = parameters.get("language", "")
            return f"```{language}\n{code}\n```"
        
        else:
            # Fallback
            return text
    
    def _render_data_widget(self, widget_type: str, parameters: dict, widget_data) -> str:
        """Render data widgets as Vue components.
        
        Args:
            widget_type: Widget type string (e.g., "Data.BigNum")
            parameters: Widget parameters dict
            widget_data: Original widget object
            
        Returns:
            str: Vue component tag
        """
        if widget_type == "Data.BigNum":
            label = parameters.get("label", "")
            value = parameters.get("value", "")
            variant = parameters.get("variant", "primary")
            return f'<MetricCard label="{label}" value="{value}" variant="{variant}" />'
        
        elif widget_type == "Data.Progress":
            label = parameters.get("label", "")
            value = parameters.get("value", 0)
            status = parameters.get("status", "success")
            return f'<ProgressBar label="{label}" :value="{value}" status="{status}" />'
        
        elif widget_type == "Data.Trend":
            status = parameters.get("status", "success")
            text = parameters.get("text", "")
            return f'<StatusBadge status="{status}" text="{text}" />'
        
        else:
            # Fallback
            return parameters.get("text", str(widget_data))
