"""Test if headers/footers work in the slide model."""
from src.common.slides import Slides
from src.common.patchable_context_pydantic import Patch
import json

# Create slides
slides = Slides()

# Add a slide with header and footer
patch_json = '''[{
  "add": {
    "id": "test_slide",
    "rank": 0,
    "state": "active",
    "strategy": "Bento.Standard",
    "widgets": {"cell_1": {"type": "Type.Display", "parameters": {"text": "Main Content"}}},
    "header": {"type": "Type.Caption", "parameters": {"text": "Header Text"}},
    "footer": {"type": "Type.Caption", "parameters": {"text": "Footer Text"}},
    "parameters": {}
  }
}]'''

patch = Patch.from_json_str(patch_json)
slides.patch(patch)

# Check if header/footer are stored
slide = list(slides.get_by_rank())[0]
print(f"Slide ID: {slide.id}")
print(f"Header: {slide.header}")
print(f"Footer: {slide.footer}")
print(f"\nHeader exists: {slide.header is not None}")
print(f"Footer exists: {slide.footer is not None}")
