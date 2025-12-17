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

```bash
# Render a sample configuration
uce-render --source "data\context\career_talk.txt" --user-instruction "Generate slides, target audience is entry, mid level devs, high contrast style" --output "output\career_talk_density_test.html" --verbose

```

## Architecture

**Pipeline**: `Configuration → LayoutEngine → RenderableLayout → HTMLRenderer → HTML`

1. **LayoutEngine**: Validates configuration, selects strategy, creates widget assignments
2. **RenderableLayout**: Intermediate representation with all rendering data
3. **HTMLRenderer**: Jinja2-based template rendering to final HTML

**TDD Approach**: All features implemented test-first following RED-GREEN-REFACTOR cycle

## License

MIT

## Contributing

This project follows specification-driven development using the SpecKit workflow. See `.specify/memory/constitution.md` for development principles.
