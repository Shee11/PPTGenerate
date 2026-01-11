# Check export logic
import json
import os

state_path = "/Users/zhang11/Work/gggg/output/ui_run_20260111_071630/state.json"
slides_path = "/Users/zhang11/Work/gggg/output/ui_run_20260111_071630/slides.mdx"

if os.path.exists(state_path):
    with open(state_path, 'r') as f:
        data = json.load(f)
        print(f"State active_theme: {data.get('active_theme')}")

if os.path.exists(slides_path):
    with open(slides_path, 'r') as f:
        content = f.read()
        print(f"Slides content sample:\n{content[:150]}")
