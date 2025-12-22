"""Generate Slidev presentation from source content using SlidevRenderer.

This script demonstrates the new Slidev engine workflow:
1. Generate slide JSON using existing content pipeline
2. Transform to Slidev markdown using SlidevRenderer
3. Output .md file ready for Slidev CLI
"""
import sys
import json
from pathlib import Path

from src.generation.orchestrator import GenerationOrchestrator
from src.paged.render.slidev.markdown_renderer import SlidevRenderer


def generate_slidev_presentation(
    source_path: Path,
    output_path: Path,
    user_instruction: str = None,
    verbose: bool = False
):
    """Generate Slidev presentation from source content.
    
    Args:
        source_path: Path to source content file (.txt or .vtt)
        output_path: Path to output .md file
        user_instruction: Optional user guidance for generation
        verbose: Enable verbose output
    """
    if verbose:
        print(f"📄 Source: {source_path}")
        print(f"📝 Output: {output_path}")
        if user_instruction:
            print(f"💬 Instructions: {user_instruction}")
        print()
    
    # Step 1: Generate slides using orchestrator
    if verbose:
        print("🎨 Generating slide content...")
    
    orchestrator = GenerationOrchestrator(use_cache=True)
    slides = orchestrator.generate_from_source(
        source_path=source_path,
        user_instruction=user_instruction
    )
    
    if verbose:
        print(f"✓ Generated {slides.count()} slides")
        print()
    
    # Step 2: Convert slides to Slidev-compatible JSON
    if verbose:
        print("🔄 Converting to Slidev format...")
    
    # Create renderer
    renderer = SlidevRenderer()
    
    # Convert each slide to Slidev JSON format
    slidev_slides = []
    
    for i, slide in enumerate(slides.slides):
        if verbose:
            print(f"  Processing slide {i+1}/{slides.count()}...")
        
        # Build slide JSON from Slide object
        slide_json = {
            "layout": _map_layout(slide.layout_type if hasattr(slide, 'layout_type') else "smart-grid"),
            "theme": {
                "primary_color": _extract_primary_color(slide)
            },
            "parameters": _extract_layout_parameters(slide),
            "widgets": _extract_widgets(slide)
        }
        
        slidev_slides.append(slide_json)
    
    if verbose:
        print(f"✓ Converted {len(slidev_slides)} slides")
        print()
    
    # Step 3: Render to Slidev markdown
    if verbose:
        print("📝 Rendering to Slidev markdown...")
    
    markdown_content = renderer.render(slidev_slides)
    
    # Step 4: Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_content, encoding='utf-8')
    
    if verbose:
        print(f"✓ Saved to: {output_path}")
        print()
        print("🚀 Next steps:")
        print(f"   1. cd {output_path.parent}")
        print(f"   2. npx slidev {output_path.name}")
        print()
    
    return markdown_content


def _map_layout(layout_type: str) -> str:
    """Map dummy engine layout type to Slidev layout name."""
    # Map common layout types
    layout_map = {
        "bento": "smart-grid",
        "swiss": "hero-split",
        "cinematic": "full-bleed",
        # Add more mappings as needed
    }
    
    return layout_map.get(layout_type.lower(), "smart-grid")


def _extract_primary_color(slide) -> str:
    """Extract primary color from slide theme."""
    # Try to get from slide's theme object
    if hasattr(slide, 'theme') and slide.theme:
        if hasattr(slide.theme, 'primary_color'):
            return slide.theme.primary_color
        # Try alternative attribute names
        if hasattr(slide.theme, 'color_primary'):
            return slide.theme.color_primary
    
    # Default to business theme blue
    return "#2563eb"


def _extract_layout_parameters(slide) -> dict:
    """Extract layout parameters from slide."""
    params = {}
    
    # Try to extract cols for grid layouts
    if hasattr(slide, 'layout') and hasattr(slide.layout, 'cols'):
        params['cols'] = slide.layout.cols
    
    # Try to extract ratio for split layouts
    if hasattr(slide, 'layout') and hasattr(slide.layout, 'ratio'):
        params['ratio'] = slide.layout.ratio
    
    # Try to extract alignment for full-bleed layouts
    if hasattr(slide, 'layout') and hasattr(slide.layout, 'align'):
        params['align'] = slide.layout.align
    
    return params


def _extract_widgets(slide) -> dict:
    """Extract widgets from slide."""
    widgets = {}
    
    # Try to get widgets from slide object
    if hasattr(slide, 'widgets') and slide.widgets:
        for slot_name, widget_obj in slide.widgets.items():
            # Convert widget object to dict format
            if hasattr(widget_obj, 'widget_type'):
                widget_dict = {
                    "type": widget_obj.widget_type
                }
                
                # Add parameters
                if hasattr(widget_obj, 'parameters'):
                    widget_dict.update(widget_obj.parameters)
                
                widgets[slot_name] = widget_dict
            else:
                # Assume it's already a dict
                widgets[slot_name] = widget_obj
    
    # Fallback: create simple heading widget if no widgets found
    if not widgets:
        widgets = {
            "header": {
                "type": "Type.Heading",
                "text": "Generated Slide",
                "level": 1
            }
        }
    
    return widgets


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python generate_slidev.py <source_file> [output_file] [instruction]")
        print()
        print("Example:")
        print("  python generate_slidev.py data/context/career_talk.txt")
        print("  python generate_slidev.py data/context/career_talk.txt output/slides.md")
        print("  python generate_slidev.py data/context/career_talk.txt output/slides.md 'Focus on technical details'")
        sys.exit(1)
    
    source_file = Path(sys.argv[1])
    
    # Default output path
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output") / (source_file.stem + "_slides.md")
    
    # Optional user instruction
    instruction = sys.argv[3] if len(sys.argv) > 3 else "Create a clear and engaging presentation"
    
    # Verify source exists
    if not source_file.exists():
        print(f"Error: Source file not found: {source_file}")
        sys.exit(1)
    
    # Generate presentation
    try:
        generate_slidev_presentation(
            source_path=source_file,
            output_path=output_file,
            user_instruction=instruction,
            verbose=True
        )
        
        print("✅ SUCCESS!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
