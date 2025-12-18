"""Demo: Generate Slidev presentation from career talk content.

This demonstrates the Slidev renderer with realistic slide content
based on the career_talk.txt transcript.
"""
from pathlib import Path
from src.render.slidev.markdown_renderer import SlidevRenderer

# Create renderer
renderer = SlidevRenderer()

# Slide 1: Title slide with career overview
slide1 = {
    "layout": "hero-split",
    "theme": {"primary_color": "#2563eb"},
    "parameters": {"ratio": "60-40"},
    "widgets": {
        "left": {
            "type": "Type.Display",
            "text": "# AI Career Journey\n\n**From Traditional Software to AI Innovation**\n\nChao Wang"
        },
        "right": {
            "type": "Data.BigNum",
            "label": "YEARS IN AI",
            "value": "10+",
            "variant": "primary"
        }
    }
}

# Slide 2: Career phases grid
slide2 = {
    "layout": "smart-grid",
    "theme": {"primary_color": "#2563eb"},
    "parameters": {"cols": 3},
    "widgets": {
        "header": {
            "type": "Type.Heading",
            "text": "Career Evolution",
            "level": 1
        },
        "col1": {
            "type": "Type.Body",
            "text": "## Phase 1: Foundation\n\n**Traditional Software Development**\n\nBuilding core engineering skills"
        },
        "col2": {
            "type": "Type.Body",
            "text": "## Phase 2: Transition\n\n**Machine Learning Era**\n\nAdopting ML frameworks and tools"
        },
        "col3": {
            "type": "Type.Body",
            "text": "## Phase 3: Innovation\n\n**LLM Revolution**\n\nBuilding with GPT-4 and beyond"
        }
    }
}

# Slide 3: Key technologies
slide3 = {
    "layout": "smart-grid",
    "theme": {"primary_color": "#2563eb"},
    "parameters": {"cols": 2},
    "widgets": {
        "header": {
            "type": "Type.Heading",
            "text": "Technology Stack Evolution",
            "level": 1
        },
        "col1": {
            "type": "Type.List",
            "items": [
                "Python & TensorFlow",
                "PyTorch & Deep Learning",
                "Transformers Architecture",
                "Fine-tuning Techniques"
            ]
        },
        "col2": {
            "type": "Type.List",
            "items": [
                "OpenAI GPT-4 API",
                "Prompt Engineering",
                "RAG Systems",
                "Agent Frameworks"
            ]
        }
    }
}

# Slide 4: Impact metrics
slide4 = {
    "layout": "smart-grid",
    "theme": {"primary_color": "#2563eb"},
    "parameters": {"cols": 4},
    "widgets": {
        "header": {
            "type": "Type.Heading",
            "text": "Impact & Achievements",
            "level": 1
        },
        "col1": {
            "type": "Data.BigNum",
            "label": "PROJECTS",
            "value": "50+",
            "variant": "primary"
        },
        "col2": {
            "type": "Data.BigNum",
            "label": "TEAM SIZE",
            "value": "15",
            "variant": "success"
        },
        "col3": {
            "type": "Data.BigNum",
            "label": "MODELS",
            "value": "20+",
            "variant": "primary"
        },
        "col4": {
            "type": "Data.BigNum",
            "label": "PRODUCTION",
            "value": "100%",
            "variant": "success"
        }
    }
}

# Slide 5: Key learnings
slide5 = {
    "layout": "full-bleed",
    "theme": {"primary_color": "#2563eb"},
    "parameters": {"align": "center"},
    "widgets": {
        "default": {
            "type": "Type.Body",
            "text": "# Key Learnings\n\n> The highest ROI in AI comes from:\n\n- **Understanding fundamentals** before jumping to latest trends\n- **Building practical systems** that solve real problems\n- **Continuous learning** as the field evolves rapidly\n- **Collaboration** with diverse teams and communities"
        }
    }
}

# Slide 6: Future with cyber theme
slide6 = {
    "layout": "hero-split",
    "theme": {"primary_color": "#00ffa3"},  # Cyber theme!
    "parameters": {"ratio": "50-50"},
    "widgets": {
        "left": {
            "type": "Type.Heading",
            "text": "Looking Forward",
            "level": 1
        },
        "right": {
            "type": "Type.List",
            "items": [
                "Multi-modal AI systems",
                "Autonomous agents",
                "AI-powered development tools",
                "Ethical AI practices"
            ]
        }
    }
}

# Combine all slides
slides = [slide1, slide2, slide3, slide4, slide5, slide6]

# Render to markdown (multi-slide)
print("🎨 Rendering Slidev presentation...")
print(f"   Slides: {len(slides)}")
print()

markdown_output = renderer.render(slides)

# Save to file
output_path = Path("output/career_talk_slidev.md")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(markdown_output, encoding='utf-8')

print("=" * 80)
print("SLIDEV MARKDOWN OUTPUT (first 500 chars)")
print("=" * 80)
print(markdown_output[:500])
print("...")
print("=" * 80)
print()
print(f"✅ SUCCESS!")
print(f"   Saved to: {output_path}")
print()
print("🚀 Next steps:")
print(f"   1. cd {output_path.parent.absolute()}")
print(f"   2. npx slidev {output_path.name}")
print()
print("💡 Theme switching demo:")
print("   - Slides 1-5 use 'business' theme (blue)")
print("   - Slide 6 uses 'cyber' theme (neon green)")
print("   - Themes switch instantly via CSS variables!")
