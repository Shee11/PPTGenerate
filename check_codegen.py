
import re
import os

def _extract_invent_components_from_mdx(mdx_text: str):
    """Extract all InventComponent specs from MDX text (content step output)."""
    components = []
    
    if not mdx_text:
        return components
    
    # Strip markdown code fences if present - logic from codegen.py
    text = mdx_text.strip()
    # The regex in codegen.py:
    fence_match = re.search(r'^```(?:mdx|jsx|xml|html)?\s*\n?(.*?)\n?```$', text, flags=re.DOTALL | re.IGNORECASE)
    
    print(f"DEBUG: Input length: {len(text)}")
    if fence_match:
        print("DEBUG: Regex ^...$ matched, stripping fences.")
        text = fence_match.group(1).strip()
    else:
        print("DEBUG: Regex ^...$ did NOT match. Using text as is.")

    # Check for number of slide blocks
    slide_pattern = r'<Slide\s+[^>]*id\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</Slide>'
    
    slides = list(re.finditer(slide_pattern, text, re.DOTALL | re.IGNORECASE))
    print(f"DEBUG: Found {len(slides)} slides.")

    for slide_match in slides:
        slide_id = slide_match.group(1)
        slide_body = slide_match.group(2)
        
        # Find InventComponent tags within this slide
        invent_pattern = r'<InventComponent\s+([\s\S]*?)(?:/>|>\s*</InventComponent>)'
        
        matches = list(re.finditer(invent_pattern, slide_body))
        # print(f"DEBUG: Slide {slide_id} has {len(matches)} InventComponents")

        for match in matches:
            attrs_str = match.group(1)
            
            component = {
                "slide_id": slide_id,
                "raw": match.group(0),
            }
            
            # Extract id attribute
            id_match = re.search(r'id\s*=\s*["\']([^"\']+)["\']', attrs_str)
            if id_match:
                component["id"] = id_match.group(1)
            else:
                component["id"] = f"invented_{slide_id}_{len(components)}"
            
            components.append(component)
    
    return components

# Read the file
file_path = "content step response.xml"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"Reading {file_path}")
    components = _extract_invent_components_from_mdx(content)
    print(f"Total InventComponents matches found: {len(components)}")
    for c in components:
        print(f"  - {c.get('id')} (Slide: {c.get('slide_id')})")

except FileNotFoundError:
    print(f"File {file_path} not found.")

