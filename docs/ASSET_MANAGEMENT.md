# Asset Management

The UCE Rendering System includes a comprehensive asset management system for themes, styles, widgets, and layout strategies.

## Directory Structure

```
assets/
├── themes/         # Theme JSON files
├── styles/         # Style JSON files
└── schemas/        # JSON schemas for validation
```

## CLI Discovery Commands

The `uce-render` command provides built-in options to discover all available assets:

### List Themes

```bash
uce-render --list-themes [--format table|json]
```

Displays all available themes with:
- Theme name and ID
- File location
- Typography configuration

Example output:
```
Available Themes:
================================================================================

Name: corp_modern
  File: C:\...\assets\themes\corp_modern.json
  Typography: Inter, system-ui, sans-serif

Name: minimal_dark
  File: C:\...\assets\themes\minimal_dark.json
  Typography: Helvetica Neue, Arial, sans-serif

================================================================================
Total: 2 themes
```

### List Styles

```bash
uce-render --list-styles [--format table|json]
```

Displays all available styles with:
- Style name
- Associated theme
- Border radius configuration
- File location

### List Widgets

```bash
uce-render --list-widgets [--format table|json]
```

Displays all registered widget types with:
- Widget type identifier (e.g., "Type.Display", "Data.BigNum")
- Widget category (Type, Data, Media, Chart)
- Allowed size classes (S, M, L, XL)

Example output:
```
Available Widgets:
================================================================================

Type: Data.BigNum
  Category: Data
  Allowed Sizes: S, M, L, XL

Type: Type.Display
  Category: Type
  Allowed Sizes: S, M, L, XL

================================================================================
Total: 8 widgets
```

### List Layout Strategies

```bash
uce-render --list-strategies [--format table|json]
```

Displays all available layout strategies with:
- Strategy name (e.g., "Bento.HeroLeft", "Swiss.Poster")
- Strategy family (Bento, Swiss, Cinematic)
- Slot definitions (role and size)

Example output:
```
Available Layout Strategies:
================================================================================

Strategy: Bento.HeroLeft
  Family: Bento
  Slots:
    - hero: L
    - side_1: S
    - side_2: S
    - side_3: S
    - side_4: S

Strategy: Swiss.Poster
  Family: Swiss
  Slots:
    - headline: XL

================================================================================
Total: 10 strategies
```

## Output Formats

All list commands support two output formats:

- `table` (default): Human-readable table format
- `json`: Machine-readable JSON format for scripting

Example:
```bash
uce-render --list-widgets --format json
uce-render --list-strategies --format json
```

## AssetManager API

The `AssetManager` class provides programmatic access to asset management:

### Theme Management

```python
from src.common.asset_manager import AssetManager
from src.layout.theme import Theme

# Save a theme
theme = Theme(id="my_theme", ...)
AssetManager.save_theme(theme, "my_theme.json")

# Load a theme
theme = AssetManager.load_theme("my_theme.json")

# List all themes
themes = AssetManager.list_themes()
```

### Style Management

```python
from src.common.asset_manager import AssetManager
from src.layout.style import Style

# Save a style
style = Style(theme_name="my_theme", ...)
AssetManager.save_style(style, "my_style.json")

# Load a style
style = AssetManager.load_style("my_style.json")

# List all styles
styles = AssetManager.list_styles()
```

### Widget Discovery

```python
# List all registered widgets
widgets = AssetManager.list_widgets()

# Get JSON schema for a specific widget
schema = AssetManager.get_widget_schema("Type.Display")
```

### Layout Strategy Discovery

```python
# List all available layout strategies
strategies = AssetManager.list_strategies()
```

### Schema Generation

```python
# Generate JSON schemas for all asset types
schemas = AssetManager.generate_schemas()
# Returns: {"theme": Path(...), "style": Path(...), "widget_*": Path(...)}
```

## JSON Schemas

The system automatically generates JSON schemas for:
- Themes (`theme.schema.json`)
- Styles (`style.schema.json`)
- Widgets (`widget_type_*.schema.json`, `widget_data_*.schema.json`)

Schemas include:
- Field definitions and types
- Validation rules
- Widget-specific metadata (type, allowed sizes)

Use these schemas to validate JSON files before loading them into the system.

## Asset Persistence

All Pydantic models can be serialized to JSON and persisted:

```python
# Generic model persistence
AssetManager.save_model(model, filepath)
loaded_model = AssetManager.load_model(ModelClass, filepath)
```

This works with any Pydantic model in the system:
- Theme
- Style
- Slide
- Slides
- Widget instances
- Layout configurations
