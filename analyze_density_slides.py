import re

content = open('output/career_talk_density_v2.html', encoding='utf-8').read()
slides = re.split(r'class="slide"', content)

print(f'Total slides: {len(slides)-1}\n')

for slide_num in [4, 5, 6]:
    if len(slides) > slide_num:
        slide_content = slides[slide_num]
        
        # Extract slide ID
        id_match = re.search(r'id="(slide_\d+_[^"]+)"', slide_content)
        slide_id = id_match.group(1) if id_match else f"slide_{slide_num}"
        
        # Extract header
        header_match = re.search(r'<h[124][^>]*>(.*?)</h[124]>', slide_content)
        header = header_match.group(1) if header_match else "No header"
        
        # Count list items
        list_items = len(re.findall(r'<li>', slide_content))
        
        # Count widgets
        widgets = len(re.findall(r'class="widget-type-', slide_content))
        
        # Extract layout type
        layout_match = re.search(r'<div class="([\w-]+)-layout">', slide_content)
        layout = layout_match.group(1) if layout_match else "unknown"
        
        print(f'=== SLIDE {slide_num}: {slide_id} ===')
        print(f'Header: {header}')
        print(f'Layout: {layout}')
        print(f'Widgets: {widgets}')
        print(f'List items: {list_items}')
        print()
