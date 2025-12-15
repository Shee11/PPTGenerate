# gggg Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-11

## Active Technologies
- Python 3.11 + Pydantic 2.x (for data models), Jinja2 (for templates) (001-uce-render)
- N/A (stateless rendering) (001-uce-render)

- Python 3.11+ + Pydantic 2.x, Jinja2 3.x, Click 8.x (001-uce-render)

## Project Structure

```text
src/
  common/
  layout/
  render/
tests/
  contract/
  integration/
  unit/
cli/
examples/
```

## Commands

pytest; ruff check src; mypy src

## Code Style

Python 3.11+: Follow PEP 8, use type hints, prefer Pydantic for validation

## Recent Changes
- 001-uce-render: Added Python 3.11 + Pydantic 2.x (for data models), Jinja2 (for templates)

- 001-uce-render: Added Python 3.11+ with Pydantic 2.x (validation), Jinja2 3.x (templating), Click 8.x (CLI)

<!-- MANUAL ADDITIONS START -->

## CLI Usage

### Basic Rendering

```bash
# Render to stdout
python -m cli examples/cyber-tech.json

# Render to file (automatically deploys static/presets.css)
python -m cli examples/cyber-tech.json --output presentation.html

# Validate configuration only
python -m cli examples/cyber-tech.json --validate-only

# Verbose output
python -m cli examples/cyber-tech.json --output result.html --verbose
```

### Listing Available Assets

```bash
# List all layout strategies
python -m cli --list-strategies

# List all widget types
python -m cli --list-widgets

# List all preset variants (Surface, Shape, Fill, Effect)
python -m cli --list-presets

# List all themes
python -m cli --list-themes

# List all styles
python -m cli --list-styles

# Get JSON format for programmatic use
python -m cli --list-presets --format json
python -m cli --list-widgets --format json
```

### Output Formats

```bash
# HTML output (default)
python -m cli config.json --output presentation.html

# JSON output (for debugging/inspection)
python -m cli config.json --format json --output data.json
```

### Custom Dimensions

```bash
# Override width/height from config
python -m cli config.json --width 1280 --height 720 --output slide.html
```

## Widget Presets

Widget presets provide inline styling through 4 categories:

**Surface** (depth/layering): `Flat`, `Elevated`, `Outline`, `Glass`, `Sunken`, `NeoBrutal`
**Shape** (border radius): `Sharp`, `Rounded`, `Curve`, `Pill`, `Squircle`, `Organic`
**Fill** (backgrounds): `Solid_Brand`, `Subtle`, `Gradient_Linear`, `Gradient_Mesh`, `Pattern_Dot`, `Noise`
**Effect** (visual fx): `Duotone`, `Glitch`, `Glow`, `Tape`

### Usage in JSON

```json
{
  "type": "Type.Display",
  "parameters": {"text": "Hello World"},
  "preset": {
    "surface": "Elevated",
    "shape": "Rounded",
    "fill": "Gradient_Linear",
    "effect": "Glow"
  }
}
```

Presets apply to the outer `.widget` container, ensuring effects like `Outline` properly border the entire widget including padding.

## Layout Strategies

Available strategies (use `--list-strategies` for full details):
- **Bento**: Standard, HeroLeft, HeroTop, Quarter
- **Swiss**: Poster, Asymmetry, SplitTypo
- **Cinematic**: FullBleed
- **Data**: KPI_Row, Magazine_Collage, Split, Grid_Masonry
- **Edit**: Left_Right, Solar_System
- **Focus**: Feature_Focus, Hero

## Configuration Structure

```json
{
  "width": 1920,
  "height": 1080,
  "theme": {
    "colors": {
      "primary": "#00ff9f",
      "secondary": "#00d4ff",
      "background": "#0a0e27"
    }
  },
  "style": {
    "theme_name": "cyber-tech",
    "typography": {
      "h1": {"size": "56px", "weight": "bold"}
    }
  },
  "slides": [
    {
      "id": "slide-1",
      "rank": 0,
      "strategy": "Bento.Standard",
      "widgets": {
        "cell_1": {
          "type": "Type.Display",
          "parameters": {"text": "Title"},
          "preset": {"surface": "Elevated", "shape": "Rounded"}
        }
      }
    }
  ]
}
```

## Static File Deployment

When using `--output`, the CLI automatically:
1. Creates output directory if needed
2. Creates `static/` subdirectory
3. Copies `presets.css` to `{output_dir}/static/presets.css`

<!-- MANUAL ADDITIONS END -->
