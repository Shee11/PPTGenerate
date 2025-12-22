"""Test script for new high-density layouts."""
import json
from pathlib import Path
from src.common.slides import Slides
from src.common.patchable_context_pydantic import Patch, AddOperation
from src.paged.layout.dummy.theme import Theme
from src.paged.layout.dummy.style import Style
from src.paged.layout.dummy.layout_engine import LayoutEngine
from src.paged.render.dummy.html_renderer import HTMLRenderer
from src.common.asset_manager import AssetManager

# Load test data
test_data_path = Path("data/test_high_density_layouts.json")
with open(test_data_path, 'r', encoding='utf-8') as f:
    test_data = json.load(f)

# Create Slides object using patches
slides_collection = Slides(id="test_slides")
operations = [AddOperation(add=slide_data) for slide_data in test_data["slides"]]
patch = Patch(operations=operations)
slides_collection.patch(patch)

# Load theme and style (load from data folder)
with open("data/corp_modern_theme.json", 'r', encoding='utf-8') as f:
    theme_data = json.load(f)
theme = Theme(**theme_data)

# Create a simple style (use flat surface for all widgets)
from src.paged.layout.dummy.style import Style, WidgetStyle
style = Style(
    theme_name="corp_modern",
    widgets={
        "Type.Heading": WidgetStyle(),
        "Type.Body": WidgetStyle(),
        "Type.List": WidgetStyle(),
        "Type.Display": WidgetStyle(),
    }
)

# Render each slide
renderer = HTMLRenderer()
renderable_layouts = []

for slide in slides_collection.get_active_slides():
    print(f"Rendering slide {slide.rank}: {slide.strategy}")
    
    # Build widget assignments
    widget_assignments = {}
    for role, widget_config in slide.widgets.items():
        if hasattr(widget_config, 'model_dump'):
            widget_assignments[role] = widget_config.model_dump()
        else:
            widget_assignments[role] = widget_config
    
    # Calculate layout
    renderable = LayoutEngine.calculate(
        strategy_name=slide.strategy,
        widget_assignments=widget_assignments,
        theme=theme,
        style=style,
        width=1920,
        height=1080,
    )
    
    # Add slide metadata
    renderable.slide_number = slide.rank
    renderable.total_slides = len(slides_collection.get_active_slides())
    renderable.slide_id = slide.id
    
    # Add header/footer if present
    if slide.header:
        from src.paged.widgets.base import WidgetRegistry
        header_type = slide.header.get('type') if isinstance(slide.header, dict) else slide.header.type
        header_params = slide.header.get('parameters') if isinstance(slide.header, dict) else slide.header.parameters
        header_class = WidgetRegistry.get(header_type)
        renderable.header_widget = header_class(**header_params)
    
    if slide.footer:
        from src.paged.widgets.base import WidgetRegistry
        footer_type = slide.footer.get('type') if isinstance(slide.footer, dict) else slide.footer.type
        footer_params = slide.footer.get('parameters') if isinstance(slide.footer, dict) else slide.footer.parameters
        footer_class = WidgetRegistry.get(footer_type)
        renderable.footer_widget = footer_class(**footer_params)
    
    renderable_layouts.append(renderable)

# Render multi-slide HTML
html = renderer.render_multi_slide(renderable_layouts)

# Save output
output_path = Path("output/test_high_density_layouts.html")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Successfully rendered {len(renderable_layouts)} slides")
print(f"📄 Output: {output_path}")
print(f"🎯 Strategies used:")
for slide in slides_collection.get_active_slides():
    print(f"   - Slide {slide.rank}: {slide.strategy}")
