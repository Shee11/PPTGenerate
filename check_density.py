import json

data = json.load(open('output/debug_phase1_storyline.json'))
slides = [s for s in data['contexts'] if s.get('state') == 'draft']

print('Slide Density Assignments:\n')
for s in slides:
    density = s.get('density', 'NOT SET')
    story_preview = s['story'][:80]
    print(f'{s["id"]}: density={density}')
    print(f'  Story: {story_preview}...')
    print()
