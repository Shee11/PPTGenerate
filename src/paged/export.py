"""Export Tool - Render slides to output format.

DirectTool: No LLM needed, uses layout engine renderer.

DEPENDENCY: Layout Engine Render
- SlidevRenderer: Converts slide JSON to Slidev markdown and builds HTML
- render_to_markdown(): Generates slides.md
- render_to_html(): Runs Slidev build to generate dist/
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


class ExportPatch(ToolPatch):
    """Patch containing export result."""
    output_path: str = ""
    format: str = "slidev"
    build_html: bool = True  # Whether to run Slidev build


@register_tool
class ExportTool(DirectTool[ExportContext, ExportPatch]):
    """Exports slides to target format (NO LLM).
    
    DEPENDS ON: Layout Engine Render
    - Uses SlidevRenderer to convert slides to Slidev markdown
    - Runs Slidev build to generate HTML dist
    - Can output to JSON for debugging
    """
    
    # Self-description
    name: ClassVar[str] = "export"
    description: ClassVar[str] = "Export slides to Slidev markdown, then build to HTML. Also supports JSON for debugging."
    query_description: ClassVar[str] = "Runs last. Format determined by instruction keywords (json, markdown-only) or defaults to full Slidev build."
    args_description: ClassVar[List[str]] = [
        "output_dir (directory for output files)",
        "format (slidev, json)",
        "build_html (whether to run Slidev build, default true)",
    ]
    requires: ClassVar[List[str]] = ["content"]
    produces: ClassVar[List[str]] = ["output_files", "dist"]
    
    def __init__(self, output_dir: Path = Path("output"), **kwargs):
        super().__init__(**kwargs)
        self.output_dir = output_dir
    
    def slice(self, state: "PipelineState", params: Optional[Dict[str, Any]] = None) -> ExportContext:
        return ExportContext(
            slides=state.slides or [],
            theme=state.get_active_theme(),
        )
    
    def transform(
        self,
        context: ExportContext,
        user_instruction: str,
    ) -> ExportPatch:
        """Determine export format from instruction."""
        instruction_lower = user_instruction.lower()
        
        fmt = "slidev"
        build_html = True
        
        if "json" in instruction_lower:
            fmt = "json"
            build_html = False
        elif "markdown only" in instruction_lower or "md only" in instruction_lower or "no build" in instruction_lower:
            build_html = False
        
        ext = "md" if fmt == "slidev" else fmt
        output_path = str(self.output_dir / f"slides.{ext}")
        
        return ExportPatch(output_path=output_path, format=fmt, build_html=build_html)
    
    def apply(self, state: "PipelineState", patch: ExportPatch) -> None:
        """Apply export using layout engine renderer."""
        context = self.slice(state)
        
        output_path = Path(patch.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if patch.format == "slidev":
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
        
        # Pass output directory to renderer for slidev_build location
        renderer = SlidevRenderer(output_dir=self.output_dir)
        
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
        base_path = f"/static/{session_folder}/"
        
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
                print(f"\n✓ Slidev build complete!")
                print(f"  To view: python -m http.server 8080 --directory \"{output_dir}\"")
                print(f"  Then open: http://localhost:8080/")
            else:
                self._log("Warning: Slidev build did not produce dist/")
                
        except Exception as e:
            self._log(f"Slidev build failed: {e}")
            self._log("Markdown exported successfully, but HTML build failed")
            # Don't raise - markdown export succeeded
    
    def _export_json(self, context: ExportContext, output_path: Path) -> None:
        """Export raw slide JSON for debugging."""
        import json
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(context.slides, f, indent=2, ensure_ascii=False)
