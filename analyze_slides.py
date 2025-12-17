import re

with open('examples/career_talk_concise.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Count total slides
slides = re.findall(r'id="slide_\d+"', content)
print(f'Total slides: {len(slides)}\n')

# Find slide 3 specifically
for i in [3]:
    slide_id = f'slide_00{i}'
    
    # Find the entire slide block
    pattern = f'id="{slide_id}".*?</div>\\s*</div>\\s*<div class="slide"'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        # Last slide
        pattern = f'id="{slide_id}".*?</body>'
        match = re.search(pattern, content, re.DOTALL)
    
    if match:
        slide_content = match.group(0)
        
        # Extract header
        header_match = re.search(r'<h[234][^>]*>(.*?)</h[234]>', slide_content)
        header = header_match.group(1) if header_match else "No header"
        
        # Extract layout type
        layout_match = re.search(r'<div class="([\w-]+)-layout">', slide_content)
        layout = layout_match.group(1) if layout_match else "unknown"
        
        # Count widgets
        widgets = len(re.findall(r'class="widget-type-', slide_content))
        
        # Extract footer to see the description
        footer_match = re.search(r'<div class="layout-footer.*?<p[^>]*>(.*?)</p>', slide_content, re.DOTALL)
        footer = footer_match.group(1) if footer_match else "No footer"
        
        print(f"Slide {i}: {header}")
        print(f"  Layout: {layout}")
        print(f"  Widgets: {widgets}")
        print(f"  Footer: {footer}")
        print()
