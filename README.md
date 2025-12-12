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

## Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### 1. Create a Configuration File

`dashboard.json`:
```json
{
  "strategy": "Bento.Standard",
  "theme": {
    "primary_color": "#2563eb",
    "accent_color": "#7c3aed",
    "font_family": "Inter, sans-serif"
  },
  "style": {
    "theme_name": "default",
    "gap": "24px",
    "padding": "32px"
  },
  "widgets": {
    "cell_1": {
      "type": "Type.Display",
      "parameters": {
        "text": "Dashboard",
        "style": "bold",
        "align": "center"
      }
    },
    "cell_2": {
      "type": "Data.BigNum",
      "parameters": {
        "value": 1247,
        "label": "Total Users",
        "color": "accent"
      }
    }
  }
}
```

### 2. Render to HTML

```bash
# Render to stdout
uce-render dashboard.json

# Render to file
uce-render dashboard.json --output dashboard.html

# Validate only
uce-render dashboard.json --validate-only

# Verbose mode
uce-render dashboard.json --output result.html --verbose
```

### 3. Python API

```python
from src.layout.layout_engine import LayoutEngine
from src.layout.theme import Theme
from src.layout.style import Style
from src.render.html_renderer import HTMLRenderer

# Define theme and style
theme = Theme(
    primary_color="#2563eb",
    accent_color="#7c3aed",
)

style = Style(
    theme_name="default",
    gap="24px",
    padding="32px"
)

# Configure widgets
widgets = {
    "cell_1": {
        "type": "Type.Display",
        "parameters": {"text": "Hello World", "style": "bold"}
    },
    "cell_2": {
        "type": "Data.BigNum",
        "parameters": {"value": 42, "label": "Answer"}
    }
}

# Calculate layout
renderable = LayoutEngine.calculate(
    strategy_name="Bento.Standard",
    widget_assignments=widgets,
    theme=theme,
    style=style
)

# Render to HTML
renderer = HTMLRenderer()
html = renderer.render(renderable)
```

## Project Structure

```
gggg/
├── src/
│   ├── common/           # Shared models (SizeClass, Slot, exceptions)
│   ├── layout/           # Layout engine and strategies
│   │   └── strategies/   # Bento, Swiss, Cinematic strategies
│   └── render/           # HTML renderer and widgets
│       ├── templates/    # Jinja2 templates
│       └── widgets/      # Widget implementations
├── cli/                  # Command-line interface
├── tests/
│   ├── contract/         # Schema validation tests
│   ├── integration/      # End-to-end tests
│   └── unit/             # Component tests
├── examples/             # Example configurations
└── specs/                # Feature specifications
    └── 001-uce-render/   # UCE render specification
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test categories
python -m pytest tests/contract/ -v      # Contract tests
python -m pytest tests/integration/ -v   # Integration tests
python -m pytest tests/unit/ -v          # Unit tests
```

## Development Status

### ✅ Phase 1-7: MVP COMPLETE
- [X] Project setup and dependencies
- [X] Foundation infrastructure (SizeClass, Theme, Style, Slot, BaseWidget)
- [X] US1: Basic Layout Rendering (3 strategies, 6 widgets, templates)
- [X] US2: T-Shirt Size Validation (constraint checking, error messages)
- [X] US3: Widget Parameter Application (style, align, color, format, level parameters)
- [X] US4: Multi-Variant Layout Support (10 strategies across 3 families)
- [X] CLI Implementation (uce-render command with validation mode)
- [X] Essential Widgets (TypeList, TypeQuote)
- [X] **131 tests passing** with 70% coverage

### ⏳ Future Enhancements (Post-MVP)
- [ ] US5: Chart Data Binding (Bar, Line, Pie, Radar, Sankey widgets)
- [ ] Media widgets (MediaFrame, MediaCode, MediaIcon)
- [ ] Performance optimization (template caching, memoization)
- [ ] Additional examples (executive-dashboard, product-launch, comparison-view)
- [ ] 90%+ test coverage target

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
