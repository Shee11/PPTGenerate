import json

data = json.load(open('output/debug_phase1_storyline.json'))
slides = [s for s in data['contexts'] if s.get('state') == 'draft']

print('V2 Density for slides 4, 5, 6:\n')
for i, s in enumerate(slides, 1):
    if i in [4, 5, 6]:
        print(f'Slide {i} ({s["id"]}): {s.get("density", "NOT SET")}')
        print(f'  Story: {s["story"][:100]}...')
        print()
