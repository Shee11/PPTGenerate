import re

content = open('output/career_talk_density_test.html', encoding='utf-8').read()
slides = re.split(r'class="slide"', content)

for slide_num in [5, 6, 7]:
    if len(slides) > slide_num:
        slide_content = slides[slide_num][:3000]
        
        # Extract slide ID
        id_match = re.search(r'id="(slide_\d+_[^"]+)"', slide_content)
        slide_id = id_match.group(1) if id_match else f"slide_{slide_num}"
        
        print(f'\n{"="*80}')
        print(f'SLIDE {slide_num}: {slide_id}')
        print("="*80)
        
        # Extract all text content (strip HTML tags for readability)
        text_only = re.sub(r'<[^>]+>', '\n', slide_content)
        # Clean up whitespace
        text_only = re.sub(r'\n\s*\n', '\n', text_only)
        print(text_only[:1500])
