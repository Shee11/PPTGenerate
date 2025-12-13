# UCE Render CLI - Listing Assets

The UCE Render CLI provides comprehensive commands to list all available themes, layouts (strategies), widgets, and styles.

## Available List Commands

```bash
# List all available themes
uce-render --list-themes

# List all available styles
uce-render --list-styles

# List all available widget types
uce-render --list-widgets

# List all available layout strategies
uce-render --list-strategies
```

## Output Formats

All list commands support two output formats:

### Human-Readable Format (Default)

Formatted, easy-to-read output with descriptions and details:

```bash
uce-render --list-widgets
```

**Output:**
```
Available Widgets:
================================================================================

Type: Data.BigNum
  Category: Data
  Minimum Size: S
  Allowed Sizes: S, M, L, XL
  Description:
    Large numerical display for key metrics.
    
    Parameters:
    - number (int | float): Numerical value to display (required)
    - label (str): Label text for the metric (required)
    ...
```

### JSON Format

Machine-readable JSON output for programmatic use:

```bash
uce-render --list-widgets --format json
```

**Output:**
```json
[
  {
    "type": "Data.BigNum",
    "category": "Data",
    "allowed_sizes": ["S", "M", "L", "XL"],
    "description": "Large numerical display...",
    "fields": {
      "atom_id": {"type": "string", "description": "..."},
      "parameters": {"type": "object", "parameters": [...]}
    }
  },
  ...
]
```

## Example Usage

### 1. List All Widgets

```bash
python -m cli.uce_render --list-widgets
```

Shows all 8+ widget types with:
- Type name (e.g., `Type.Display`, `Data.BigNum`)
- Category (Type, Data, Media, Chart)
- Allowed sizes (S, M, L, XL)
- Required parameters
- Optional parameters with defaults
- Schema information

### 2. List All Layout Strategies

```bash
python -m cli.uce_render --list-strategies
```

Shows all 10 layout strategies across 3 families:

**Bento Family** (Fixed Grids):
- `Bento.Standard` - 3×2 grid (6 cells, size S)
- `Bento.HeroLeft` - Hero + 4 side cells (1 L + 4 S)
- `Bento.HeroTop` - Hero + 3 footer cells (1 L + 3 S)
- `Bento.Quarter` - 2×2 quadrants (4 cells, size M)

**Swiss Family** (Asymmetric):
- `Swiss.Poster` - Single full-screen (1 XL)
- `Swiss.Asymmetry` - Content with void space (1 L)
- `Swiss.SplitTypo` - Headline + body split (1 M + 1 L)

**Cinematic Family** (Proportional Splits):
- `Cinematic.Split_50_50` - 50/50 split (2 L)
- `Cinematic.FullBleed` - Full canvas (1 XL)
- `Cinematic.Split_30_70` - 30/70 split (1 M + 1 XL)

### 3. List All Themes

```bash
python -m cli.uce_render --list-themes
```

Shows:
- Available theme files
- Theme IDs
- File paths
- Complete schema with all supported fields

**Current Themes:**
- `corp_modern` - Corporate modern theme
- `minimal_dark` - Minimal dark theme

### 4. List All Styles

```bash
python -m cli.uce_render --list-styles
```

Shows:
- Available style files
- Associated theme names
- File paths
- Style schema

**Current Styles:**
- `corp_modern_default` (uses `corp_modern_v1` theme)
- `minimal_dark_default` (uses `minimal_dark_v1` theme)

## Programmatic Usage

### Parse JSON Output

```bash
# Get widgets as JSON
python -m cli.uce_render --list-widgets --format json > widgets.json

# Get strategies as JSON
python -m cli.uce_render --list-strategies --format json > strategies.json

# Get themes as JSON
python -m cli.uce_render --list-themes --format json > themes.json

# Get styles as JSON
python -m cli.uce_render --list-styles --format json > styles.json
```

### Use in Scripts

**PowerShell:**
```powershell
# Get all widget types
$widgets = python -m cli.uce_render --list-widgets --format json | ConvertFrom-Json
$widgets | ForEach-Object { Write-Host $_.type }

# Get all strategy names
$strategies = python -m cli.uce_render --list-strategies --format json | ConvertFrom-Json
$strategies | ForEach-Object { Write-Host "$($_.name) ($($_.family))" }
```

**Bash:**
```bash
# Get all widget types
uce-render --list-widgets --format json | jq '.[].type'

# Get all strategies in Bento family
uce-render --list-strategies --format json | jq '.[] | select(.family == "Bento") | .name'
```

## Quick Reference

| Command | Description | JSON Output |
|---------|-------------|-------------|
| `--list-widgets` | List all widget types with parameters | `--format json` |
| `--list-strategies` | List all layout strategies with slots | `--format json` |
| `--list-themes` | List all themes with schema | `--format json` |
| `--list-styles` | List all styles with theme mapping | `--format json` |

## Current Inventory

**Widgets**: 8 types
- Typography: Display, Heading, Body, List, Quote
- Data: BigNum, Trend, Progress
- Media: (Coming soon: Frame, Code, Icon)
- Charts: (Coming soon: Bar, Line, Pie, Radar, Sankey)

**Layout Strategies**: 10 strategies
- Bento: 4 variants
- Swiss: 3 variants
- Cinematic: 3 variants

**Themes**: 2 themes
- corp_modern
- minimal_dark

**Styles**: 2 styles
- corp_modern_default
- minimal_dark_default

## See Also

- Run `uce-render --help` for full CLI documentation
- See `examples/` directory for configuration examples
- See `assets/themes/` for theme JSON files
- See `assets/styles/` for style JSON files
