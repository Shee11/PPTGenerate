"""Quick test of SlidevRenderer with sample slide JSON."""
from src.paged.render.slidev.markdown_renderer import SlidevRenderer

# Create renderer
renderer = SlidevRenderer()

# Sample slide JSON - smart-grid layout with mixed widgets
slide_json = {
    "layout": "smart-grid",
    "theme": {
        "primary_color": "#2563eb"  # Business theme
    },
    "parameters": {
        "cols": 3
    },
    "widgets": {
        "header": {
            "type": "Type.Heading",
            "text": "AI Career Journey",
            "level": 1
        },
        "col1": {
            "type": "Type.Body",
            "text": "**Early Days**\n\nStarted in traditional software development before AI revolution"
        },
        "col2": {
            "type": "Data.BigNum",
            "label": "YEARS",
            "value": "10+",
            "variant": "primary"
        },
        "col3": {
            "type": "Type.List",
            "items": [
                "Machine Learning",
                "Deep Learning",
                "Large Language Models"
            ]
        }
    }
}

# Render to markdown
markdown_output = renderer.render(slide_json)

# Print result
print("=" * 80)
print("SLIDEV MARKDOWN OUTPUT")
print("=" * 80)
print(markdown_output)
print("=" * 80)

# Save to file
output_path = "output/career_talk_slidev_test.md"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(markdown_output)

print(f"\n✓ Saved to: {output_path}")
