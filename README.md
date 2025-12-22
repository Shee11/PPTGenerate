# UCE Render - Universal Content Engine Rendering System

A specification-driven rendering system for creating beautiful, constraint-based layouts with widgets.

## Features

✅ **MVP Complete** - 131 tests passing, 70% coverage, 10 layout strategies, 8 widget types

### Layout Strategies (10 Total)

**Bento Family** (Grid-based layouts):
- **Bento.Standard**: 3x2 grid of equal-sized cells (6 S slots)
- **Bento.HeroLeft**: Hero left + 4 side slots (1 L + 4 S slots)
- **Bento.HeroTop**: Hero top + 3 footer slots (1 L + 3 S slots)
- **Bento.Quarter**: Four quadrants (4 M slots)

**Swiss Family** (Minimalist typography-focused):
- **Swiss.Poster**: Single full-screen slot (1 XL slot)
- **Swiss.Asymmetry**: Large content with void area (1 L slot)
- **Swiss.SplitTypo**: Headline + body split (1 M + 1 L slots)

**Cinematic Family** (Widescreen splits):
- **Cinematic.Split_50_50**: Equal left-right split (2 L slots)
- **Cinematic.FullBleed**: Single stage (1 XL slot)
- **Cinematic.Split_30_70**: Sidebar + main stage (1 M + 1 XL slots)

### Widget Library (8 Types)

**Typography Widgets** (min size: S):
- `Type.Display`: Large display typography for headlines
  - Parameters: `text`, `style` (normal/bold/italic/bold-italic), `align` (left/center/right/justify)
- `Type.Heading`: Section headings with levels 1-6
  - Parameters: `text`, `level` (1-6), `align`
- `Type.Body`: Body text paragraphs
  - Parameters: `text`, `align`
- `Type.List`: Bullet or numbered lists
  - Parameters: `items` (list), `list_type` (ordered/unordered)
- `Type.Quote`: Blockquotes with citations
  - Parameters: `text`, `citation` (optional), `align`

**Data & Metrics Widgets** (min size: S):
- `Data.BigNum`: Large numerical metrics display
  - Parameters: `value`, `label`, `color` (primary/accent/success/warning/danger), `format` (number/currency/percentage)
- `Data.Trend`: Trend indicators with direction
  - Parameters: `value`, `change`, `direction` (up/down/flat), `label`, `color`
- `Data.Progress`: Progress bars with percentages
  - Parameters: `value`, `max`, `label`, `show_percentage` (bool), `color`

### T-Shirt Sizing

All widgets and slots use T-Shirt sizing (S/M/L/XL) with automatic constraint validation:
- **S** (Small): Basic content, minimal space
- **M** (Medium): Standard content
- **L** (Large): Emphasized content
- **XL** (Extra Large): Hero content, full-bleed

## Quick Start

### 0. Code
```bash
git clone https://github.com/wcpeter19882/gggg.git
cd gggg
```

### 1. Set Up Virtual Environment

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install CLI tool
pip install -e .
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install CLI tool
pip install -e .
```

### 2. Verify Installation

```bash
# Check CLI is installed
uce-render --help

# List available resources
uce-render --list-strategies
uce-render --list-widgets
uce-render --list-themes
```

### 3. Run Sample Commands

**CLI Mode:**
```bash
# Render slides from source file
uce-render --source "data/context/career_talk.txt" \
  --user-instruction "Generate slides for entry-level developers" \
  --output "output/career_talk" \
  --verbose

# List available resources
uce-render --list-strategies
uce-render --list-widgets
uce-render --list-themes
```

**Gradio Web UI:**
```bash
# Start the Gradio app (includes static file server)
python app.py

# Open in browser: http://127.0.0.1:7860
```

**With ngrok (for remote access):**
```bash
# Start the app
python app.py

# In another terminal, start ngrok
ngrok start --config ngrok.yml --all
```

## Architecture

**Pipeline**: `Configuration → LayoutEngine → RenderableLayout → Renderer → HTML`

1. **LayoutEngine**: Validates configuration, selects strategy, creates widget assignments
2. **RenderableLayout**: Intermediate representation with all rendering data
3. **Renderer**: Renders to HTML (HTMLRenderer for static, SlidevRenderer for presentations)

### Layout Engines

**HTML Engine** (Default):
- Static HTML rendering with Jinja2 templates
- Best for: Single slides, dashboards, static content
- Output: Single HTML file with embedded CSS

**Slidev Engine**:
- Vue-based presentation framework
- Best for: Multi-slide presentations, interactive content
- Output: Standalone HTML with Slidev/Vite build
- Documentation: See `docs/SLIDEV_DEVELOPMENT_GUIDE.md`

Quick differences:
- `slidev-project/`: SOURCE directory (edit here, version controlled)
- `slidev_build/`: BUILD directory (temporary, auto-generated, gitignored)

**TDD Approach**: All features implemented test-first following RED-GREEN-REFACTOR cycle

## Documentation

- **Slidev Development**: `docs/SLIDEV_DEVELOPMENT_GUIDE.md` - Complete guide for custom layouts/widgets
- **Slidev Quick Reference**: `docs/SLIDEV_QUICK_REFERENCE.md` - Quick commands and directory structure
- **LLM Pipeline**: `docs/LLM_PIPELINE_DIAGRAM.md` - Content generation flow
- **Refactoring Plans**: `LAYOUT_ENGINE_REFACTOR_PLAN.md`, `STYLE_SYSTEM_REFACTORING.md`

## License

MIT

## Contributing

This project follows specification-driven development using the SpecKit workflow. See `.specify/memory/constitution.md` for development principles.
