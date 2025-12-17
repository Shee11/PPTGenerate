import re

content = open('output/career_talk_markdown_fixed.html', encoding='utf-8').read()
slides = re.split(r'class="slide"', content)

print(f'Total slides: {len(slides)-1}')
print('\n=== SLIDE 4 ===')
print(slides[4][:2000] if len(slides) > 4 else 'N/A')
print('\n=== SLIDE 5 ===')
print(slides[5][:2000] if len(slides) > 5 else 'N/A')
print('\n=== SLIDE 6 ===')
print(slides[6][:2000] if len(slides) > 6 else 'N/A')
