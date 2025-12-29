"""Export Tool - Render slides to output format.

DirectTool: No LLM needed, uses layout engine renderer.

DEPENDENCY: Layout Engine Render
- SlidevRenderer: Converts slide JSON to Slidev markdown and builds HTML
- ReactMDXRenderer: Converts slide JSON to MDX and exports to HTML
- render_to_markdown(): Generates slides.md
- render_to_html(): Runs Slidev build or exports React HTML
"""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Optional, List, Dict, Any, ClassVar
from pydantic import Field

from src.common.tool_protocol import DirectTool, ToolContext, ToolPatch, register_tool

if TYPE_CHECKING:
    from src.generation.state import PipelineState


class ExportContext(ToolContext):
    """Context for export."""
    slides: List[Dict[str, Any]] = Field(default_factory=list)
    theme: Optional[Dict[str, Any]] = None
    project: str = Field(default="slidev", description="Project style: slidev, duolingo, or react-mdx")
    mdx_theme: str = Field(default="business", description="MDX theme for react-mdx export")


class ExportPatch(ToolPatch):
    """Patch containing export result."""
    output_path: str = ""
    format: str = "slidev"  # slidev, react-mdx, json
    build_html: bool = True  # Whether to run HTML build


@register_tool
class ExportTool(DirectTool[ExportContext, ExportPatch]):
    """Exports slides to target format (NO LLM).
    
    DEPENDS ON: Layout Engine Render
    - Uses SlidevRenderer for Slidev markdown and HTML builds
    - Uses ReactMDXRenderer for MDX and HTML exports
    - Can output to JSON for debugging
    """
    
    # Self-description
    name: ClassVar[str] = "export"
    description: ClassVar[str] = "Export slides to Slidev/React-MDX, then build to HTML. Also supports JSON for debugging."
    query_description: ClassVar[str] = "Runs last. Format determined by project setting (slidev, react-mdx) or instruction keywords (json)."
    args_description: ClassVar[List[str]] = [
        "output_dir (directory for output files)",
        "format (slidev, react-mdx, json)",
        "build_html (whether to run HTML build, default true)",
    ]
    requires: ClassVar[List[str]] = ["content"]
    produces: ClassVar[List[str]] = ["output_files", "dist"]
    examples: ClassVar[List[str]] = [
        '{"id": "export", "type": "export", "params": {}, "depends_on": ["content"]}',
        '{"id": "export", "type": "export", "params": {"project": "react-mdx"}, "depends_on": ["content"]}',
    ]
    
    def __init__(self, output_dir: Path = Path("output"), **kwargs):
        super().__init__(**kwargs)
        self.output_dir = output_dir
    
    def slice(self, state: "PipelineState", params: Optional[Dict[str, Any]] = None) -> ExportContext:
        """Extract slides and theme for export.
        
        Theme resolution priority:
        1. First slide's parameters.theme (set during content generation)
        2. Fallback to AssetManager.get_theme()
        """
        params = params or {}
        slides = state.slides or []
        
        # Get theme from first slide's parameters.theme
        theme = None
        theme_id = None
        if slides:
            params_theme = slides[0].get("parameters", {}).get("theme")
            if params_theme:
                theme_id = params_theme
        
        # Load full theme data from AssetManager
        if theme_id:
            from src.common.asset_manager import AssetManager
            theme = AssetManager.get_theme(theme_id)
        
        # Get MDX theme from params, state, or default to "business"
        mdx_theme = params.get("mdx_theme") or getattr(state, "mdx_theme", "business")
        
        return ExportContext(
            slides=slides,
            theme=theme,
            project=state.project or "slidev",
            mdx_theme=mdx_theme,
        )
    
    def transform(
        self,
        context: ExportContext,
        user_instruction: str,
    ) -> ExportPatch:
        """Determine export format from context and instruction."""
        instruction_lower = user_instruction.lower()
        
        # Determine format based on project or instruction
        if context.project in ("react-mdx", "react"):
            fmt = "react-mdx"
            build_html = True
            ext = "mdx"
        elif "json" in instruction_lower:
            fmt = "json"
            build_html = False
            ext = "json"
        elif "markdown only" in instruction_lower or "md only" in instruction_lower or "no build" in instruction_lower:
            fmt = "slidev"
            build_html = False
            ext = "md"
        else:
            fmt = "slidev"
            build_html = True
            ext = "md"
        
        output_path = str(self.output_dir / f"slides.{ext}")
        
        return ExportPatch(output_path=output_path, format=fmt, build_html=build_html)
    
    def apply(self, state: "PipelineState", patch: ExportPatch) -> None:
        """Apply export using appropriate renderer."""
        context = self.slice(state)
        
        output_path = Path(patch.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if patch.format == "react-mdx":
            self._export_react_mdx(context, output_path, patch.build_html)
        elif patch.format == "slidev":
            self._export_slidev(context, output_path, patch.build_html)
        elif patch.format == "json":
            self._export_json(context, output_path)
        
        self._log(f"Exported to {output_path}")
    
    def _export_slidev(self, context: ExportContext, output_path: Path, build_html: bool = True) -> None:
        """Export to Slidev markdown and optionally build HTML.
        
        Steps:
        1. Generate slides.md using SlidevRenderer
        2. Copy to output directory
        3. If build_html, run Slidev build to generate dist/
        4. Copy dist/ to output directory
        """
        from src.paged.render import SlidevRenderer
        
        # Pass output directory and project to renderer
        renderer = SlidevRenderer(output_dir=self.output_dir, project=context.project)
        
        # Generate markdown with theme from context
        markdown = renderer.render_to_markdown(context.slides, theme=context.theme)
        output_path.write_text(markdown, encoding='utf-8')
        self._log(f"Generated {output_path.name} ({len(markdown)} chars)")
        
        if not build_html:
            self._log("Skipping Slidev build (markdown only)")
            return
        
        # Determine base path for assets
        # Use /static/{session_folder}/ for FastAPI static mount
        output_dir = output_path.parent
        session_folder = output_dir.name  # e.g., "slide_20251222_56"
        # base_path = f"/static/{session_folder}/"
        base_path = f"/output/{session_folder}/"
        
        # Run Slidev build
        self._log(f"Running Slidev build with base={base_path}...")
        try:
            html_content = renderer.render_to_html(markdown, base_path=base_path)
            
            # Copy dist contents directly to output_dir (no extra dist folder)
            build_dist = renderer.build_dir / "dist"
            output_dir = output_path.parent
            
            if build_dist.exists():
                # Copy contents of dist/ directly to output folder
                for item in build_dist.iterdir():
                    dest = output_dir / item.name
                    if item.is_dir():
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
                    else:
                        shutil.copy2(item, dest)
                self._log(f"Copied HTML build to {output_dir}")
                
                # Save slides.json alongside
                slides_json_path = output_dir / "slides.json"
                import json
                with open(slides_json_path, 'w', encoding='utf-8') as f:
                    json.dump(context.slides, f, indent=2, ensure_ascii=False)
                self._log(f"Saved slides.json")
                
                # Print viewing instructions
                print(f"\n[export] Slidev build complete!")
                print(f"  To view: python -m http.server 8080 --directory \"{output_dir}\"")
                print(f"  Then open: http://localhost:8080/")
            else:
                self._log("Warning: Slidev build did not produce dist/")
                
        except Exception as e:
            self._log(f"Slidev build failed: {e}")
            self._log("Markdown exported successfully, but HTML build failed")
            # Don't raise - markdown export succeeded
    
    def _export_react_mdx(self, context: ExportContext, output_path: Path, build_html: bool = True) -> None:
        """Export to React MDX and optionally build HTML.
        
        Steps:
        1. Generate MDX using ReactMDXRenderer
        2. Save MDX to output directory
        3. React TSX components handle rendering (no Python HTML export)
        """
        from src.paged.render.react.mdx_renderer import ReactMDXRenderer
        import json
        
        # Build state dict for renderer
        state_dict = {"slides": context.slides, "presentation": {"theme": context.mdx_theme}}
        
        # Create renderer with theme
        renderer = ReactMDXRenderer(output_dir=output_path.parent, theme=context.mdx_theme)
        
        # Generate MDX
        mdx_content = renderer.render_state(state_dict)
        output_path.write_text(mdx_content, encoding='utf-8')
        self._log(f"Generated {output_path.name} ({len(mdx_content)} chars)")
        
        # Run whitespace validation on generated MDX
        from src.paged.layout.react.layout_validator import validate_mdx_content
        print("\n[export] Layout Whitespace Analysis:")
        ws_result = validate_mdx_content(mdx_content, verbose=True)
        
        # Save state.json alongside
        state_json_path = output_path.parent / "state.json"
        with open(state_json_path, 'w', encoding='utf-8') as f:
            json.dump(state_dict, f, indent=2, ensure_ascii=False)
        self._log(f"Saved state.json")
        
        if not build_html:
            self._log("Skipping HTML build (MDX only)")
            return
        
        # React TSX components handle HTML rendering
        # Use: cd src/paged/render/react && npm run build && npm run export
        print(f"\n[export] React MDX export complete!")
        print(f"  MDX saved to: {output_path}")
        print(f"  State saved to: {state_json_path}")
        print(f"\n  To render HTML:")
        print(f"    cd src/paged/render/react")
        print(f"    npm run dev    # for development preview")
        print(f"    npm run build  # for production build")
    
    def _export_json(self, context: ExportContext, output_path: Path) -> None:
        """Export raw slide JSON for debugging."""
        import json
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(context.slides, f, indent=2, ensure_ascii=False)
