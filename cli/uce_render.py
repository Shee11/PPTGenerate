"""CLI for UCE Render - uce-render command."""
import json
import shutil
import sys
from pathlib import Path
from typing import Optional

import click

from src.common.asset_manager import AssetManager
from src.common.exceptions import UCERenderError
from src.common.patchable_context_pydantic import Patch
from src.common.slide import Slide
from src.common.slides import Slides
from src.layout.layout_engine import LayoutEngine
from src.layout.style import Style
from src.layout.theme import Theme
from src.render.html_renderer import HTMLRenderer


@click.command()
@click.argument('config_file', type=click.Path(exists=True, path_type=Path), required=False)
@click.option(
    '--output', '-o',
    type=click.Path(path_type=Path),
    help='Output HTML file path (default: stdout)'
)
@click.option(
    '--format', '-f',
    type=click.Choice(['html', 'json', 'table'], case_sensitive=False),
    default='html',
    help='Output format (default: html)'
)
@click.option(
    '--validate-only', '--validate',
    is_flag=True,
    help='Validate configuration without rendering'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose logging'
)
@click.option(
    '--width', '-w',
    type=int,
    default=None,
    help='Layout width in pixels (default: 1920 or from config)'
)
@click.option(
    '--height', '-h',
    type=int,
    default=None,
    help='Layout height in pixels (default: 1080 or from config)'
)
@click.option(
    '--list-themes',
    is_flag=True,
    help='List all available themes'
)
@click.option(
    '--list-styles',
    is_flag=True,
    help='List all available styles'
)
@click.option(
    '--list-widgets',
    is_flag=True,
    help='List all available widget types'
)
@click.option(
    '--list-strategies',
    is_flag=True,
    help='List all available layout strategies'
)
@click.option(
    '--list-presets',
    is_flag=True,
    help='List all available widget preset variants'
)
def cli(
    config_file: Optional[Path],
    output: Optional[Path],
    format: str,
    validate_only: bool,
    verbose: bool,
    width: Optional[int],
    height: Optional[int],
    list_themes: bool,
    list_styles: bool,
    list_widgets: bool,
    list_strategies: bool,
    list_presets: bool,
) -> None:
    """Render layouts using the Universal Content Engine.
    
    CONFIG_FILE: Path to JSON configuration file with layout specification.
    
    Examples:
    
        # Render to stdout
        uce-render config.json
        
        # Render to file
        uce-render config.json --output result.html
        
        # Validate configuration only
        uce-render config.json --validate-only
        
        # Output JSON format
        uce-render config.json --format json
        
        # List available assets
        uce-render --list-themes
        uce-render --list-styles
        uce-render --list-widgets
        uce-render --list-strategies
        uce-render --list-presets
        uce-render --list-themes --format json
    """
    try:
        # Handle list commands
        if list_themes:
            result = AssetManager.list_themes()
            if format == 'json':
                click.echo(json.dumps(result, indent=2))
            else:
                themes = result['available_themes']
                schema_fields = result['schema']['fields']
                
                click.echo("\nAvailable Themes:")
                click.echo("=" * 80)
                for theme in themes:
                    click.echo(f"\nName: {theme['name']}")
                    click.echo(f"  ID: {theme['id']}")
                    click.echo(f"  File: {theme['file']}")
                
                click.echo("\n" + "=" * 80)
                click.echo(f"Total: {len(themes)} themes\n")
                
                click.echo("\nTheme Schema (Supported Fields):")
                click.echo("=" * 80)
                for field_name, field_info in sorted(schema_fields.items()):
                    required = " [REQUIRED]" if field_info.get('required') else ""
                    click.echo(f"\n{field_name}{required}:")
                    click.echo(f"  Type: {field_info['type']}")
                    if field_info.get('description'):
                        click.echo(f"  Description: {field_info['description']}")
                    if 'default' in field_info:
                        click.echo(f"  Default: {field_info['default']}")
                click.echo("\n" + "=" * 80 + "\n")
            sys.exit(0)
        
        if list_styles:
            result = AssetManager.list_styles()
            if format == 'json':
                click.echo(json.dumps(result, indent=2))
            else:
                styles = result['available_styles']
                schema_fields = result['schema']['fields']
                
                click.echo("\nAvailable Styles:")
                click.echo("=" * 80)
                for style in styles:
                    click.echo(f"\nName: {style['name']}")
                    click.echo(f"  Theme: {style['theme_name']}")
                    click.echo(f"  File: {style['file']}")
                
                click.echo("\n" + "=" * 80)
                click.echo(f"Total: {len(styles)} styles\n")
                
                click.echo("\nStyle Schema (Supported Fields):")
                click.echo("=" * 80)
                for field_name, field_info in sorted(schema_fields.items()):
                    required = " [REQUIRED]" if field_info.get('required') else ""
                    click.echo(f"\n{field_name}{required}:")
                    click.echo(f"  Type: {field_info['type']}")
                    if field_info.get('description'):
                        click.echo(f"  Description: {field_info['description']}")
                    if 'default' in field_info:
                        click.echo(f"  Default: {field_info['default']}")
                click.echo("\n" + "=" * 80 + "\n")
            sys.exit(0)
        
        if list_widgets:
            widgets = AssetManager.list_widgets()
            if format == 'json':
                click.echo(json.dumps(widgets, indent=2))
            else:
                click.echo("\nAvailable Widgets:")
                click.echo("=" * 80)
                for widget in widgets:
                    click.echo(f"\nType: {widget['type']}")
                    click.echo(f"  Category: {widget['category']}")
                    click.echo(f"  Minimum Size: {widget['allowed_sizes'][0]}")
                    click.echo(f"  Allowed Sizes: {', '.join(widget['allowed_sizes'])}")
                    
                    if widget.get('description'):
                        # Multi-line description formatting
                        desc_lines = widget['description'].strip().split('\n')
                        click.echo(f"  Description:")
                        for line in desc_lines:
                            click.echo(f"    {line.strip()}")
                    
                    if widget.get('fields'):
                        click.echo("  Schema Fields:")
                        for field_name, field_info in sorted(widget['fields'].items()):
                            field_type = field_info['type']
                            field_desc = field_info.get('description', '')
                            default_val = field_info.get('default', '')
                            
                            click.echo(f"    - {field_name}:")
                            click.echo(f"        Type: {field_type}")
                            if field_desc:
                                click.echo(f"        Description: {field_desc}")
                            if default_val:
                                click.echo(f"        Default: {default_val}")
                            
                            # Expand parameters if available
                            if field_name == 'parameters' and 'parameters' in field_info:
                                params = field_info['parameters']
                                if params:
                                    click.echo(f"        Accepted Parameters:")
                                    for param in params:
                                        click.echo(f"          - {param['name']} ({param['type']}): {param['description']}")
                
                click.echo("\n" + "=" * 80)
                click.echo(f"Total: {len(widgets)} widgets\n")
            sys.exit(0)
        
        if list_presets:
            presets = {
                "categories": [
                    {
                        "name": "Surface",
                        "description": "Visual depth and layering effects",
                        "variants": [
                            {"name": "Flat", "description": "No elevation, flat appearance"},
                            {"name": "Elevated", "description": "Subtle shadow, raised appearance"},
                            {"name": "Outline", "description": "Transparent with border"},
                            {"name": "Glass", "description": "Frosted glass effect with blur"},
                            {"name": "Sunken", "description": "Inset appearance, pressed look"},
                            {"name": "NeoBrutal", "description": "Bold border with offset shadow"}
                        ]
                    },
                    {
                        "name": "Shape",
                        "description": "Border radius and corner styles",
                        "variants": [
                            {"name": "Sharp", "description": "No border radius, 90° corners"},
                            {"name": "Rounded", "description": "8px border radius"},
                            {"name": "Curve", "description": "16px border radius"},
                            {"name": "Pill", "description": "Fully rounded ends"},
                            {"name": "Squircle", "description": "Smooth squircle shape"},
                            {"name": "Organic", "description": "Irregular organic shape"}
                        ]
                    },
                    {
                        "name": "Fill",
                        "description": "Background patterns and fills",
                        "variants": [
                            {"name": "Solid_Brand", "description": "Solid brand color background"},
                            {"name": "Subtle", "description": "Light neutral background"},
                            {"name": "Gradient_Linear", "description": "Linear gradient (primary to secondary)"},
                            {"name": "Gradient_Mesh", "description": "Radial mesh gradient"},
                            {"name": "Pattern_Dot", "description": "Dotted pattern background"},
                            {"name": "Noise", "description": "Subtle noise texture overlay"}
                        ]
                    },
                    {
                        "name": "Effect",
                        "description": "Visual treatments and filters",
                        "variants": [
                            {"name": "Duotone", "description": "Two-tone color filter"},
                            {"name": "Glitch", "description": "Digital glitch animation effect"},
                            {"name": "Glow", "description": "Colored glow/halo effect"},
                            {"name": "Tape", "description": "Washi tape decoration on top"}
                        ]
                    }
                ],
                "usage": {
                    "example": {
                        "type": "Type.Display",
                        "parameters": {"text": "Hello World"},
                        "preset": {
                            "surface": "Elevated",
                            "shape": "Rounded",
                            "fill": "Gradient_Linear",
                            "effect": "Glow"
                        }
                    },
                    "notes": [
                        "All preset fields are optional",
                        "Presets are applied via CSS classes",
                        "Multiple categories can be combined",
                        "Presets work with all widget types"
                    ]
                },
                "total_variants": 22
            }
            
            if format == 'json':
                click.echo(json.dumps(presets, indent=2))
            else:
                click.echo("\nAvailable Widget Presets:")
                click.echo("=" * 80)
                
                for category in presets['categories']:
                    click.echo(f"\n{category['name']} Presets ({len(category['variants'])} variants)")
                    click.echo(f"  {category['description']}")
                    click.echo("  " + "-" * 76)
                    for variant in category['variants']:
                        click.echo(f"    • {variant['name']:<20} - {variant['description']}")
                
                click.echo("\n" + "=" * 80)
                click.echo(f"Total: {presets['total_variants']} preset variants across 4 categories\n")
                
                click.echo("\nUsage Example:")
                click.echo("=" * 80)
                example = presets['usage']['example']
                click.echo(json.dumps(example, indent=2))
                
                click.echo("\n" + "=" * 80)
                click.echo("\nNotes:")
                for note in presets['usage']['notes']:
                    click.echo(f"  • {note}")
                click.echo("\n" + "=" * 80 + "\n")
            sys.exit(0)
        
        if list_strategies:
            strategies = AssetManager.list_strategies()
            if format == 'json':
                click.echo(json.dumps(strategies, indent=2))
            else:
                click.echo("\nAvailable Layout Strategies:")
                click.echo("=" * 80)
                for strategy in strategies:
                    click.echo(f"\nStrategy: {strategy['name']}")
                    click.echo(f"  Family: {strategy['family']}")
                    click.echo(f"  Slots:")
                    for slot in strategy['slots']:
                        click.echo(f"    - {slot['role']}: {slot['size']}")
                click.echo("\n" + "=" * 80)
                click.echo(f"Total: {len(strategies)} strategies\n")
            sys.exit(0)
        
        # Require config_file if not listing assets
        if not config_file:
            click.echo("Error: CONFIG_FILE is required when not using --list-* options", err=True)
            sys.exit(1)
        
        # Load configuration
        if verbose:
            click.echo(f"Loading configuration from {config_file}", err=True)

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            click.echo(f"Error: Invalid JSON in configuration file: {e}", err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(f"Error: Could not read configuration file: {e}", err=True)
            sys.exit(1)

        # Multi-slide format required
        if 'slides' not in config:
            click.echo("Error: Configuration must contain 'slides' array", err=True)
            sys.exit(1)
        
        # Extract common configuration
        theme_data = config.get('theme', {})
        style_data = config.get('style', {})
        layout_width = width if width is not None else config.get('width', 1920)
        layout_height = height if height is not None else config.get('height', 1080)

        # Ensure style has theme_name
        if 'theme_name' not in style_data:
            style_data['theme_name'] = 'default'

        # Create theme and style models
        try:
            theme = Theme(**theme_data)
            style = Style(**style_data)
        except Exception as e:
            click.echo(f"Error: Invalid theme or style configuration: {e}", err=True)
            sys.exit(1)

        if verbose:
            click.echo("Processing multi-slide configuration", err=True)

        slides_data = config.get('slides', [])
        
        # Create Slides collection
        slides = Slides()
        
        # Add slides using patch operations
        operations = []
        for slide_data in slides_data:
            # Ensure required fields
            if 'id' not in slide_data:
                slide_data['id'] = f"slide-{slide_data.get('rank', len(operations) + 1)}"
            if 'rank' not in slide_data:
                slide_data['rank'] = len(operations)
            if 'state' not in slide_data:
                slide_data['state'] = 'active'
            
            # Create Slide instance for validation
            try:
                slide = Slide(**slide_data)
                operations.append({"add": slide})
            except Exception as e:
                click.echo(f"Error: Invalid slide configuration: {e}", err=True)
                sys.exit(1)
        
        # Apply patch to add all slides
        if operations:
            patch = Patch(operations=operations)
            slides.patch(patch)

        if verbose:
            click.echo(f"Loaded {slides.count()} slides", err=True)
            click.echo(f"Size: {layout_width}x{layout_height}", err=True)

        # Calculate layouts for all slides
        try:
            renderables = LayoutEngine.calculate_slides(
                slides=slides,
                theme=theme,
                style=style,
                width=layout_width,
                height=layout_height
            )
        except UCERenderError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)

        if validate_only:
            click.echo(f"✓ Configuration is valid ({len(renderables)} slides)", err=True)
            sys.exit(0)

        # Render multi-slide output
        if format.lower() == 'html':
            renderer = HTMLRenderer()
            html_output = renderer.render(renderables)  # Pass list for multi-slide

            if output:
                if verbose:
                    click.echo(f"Writing multi-slide HTML to {output}", err=True)
                
                # Create output directory if it doesn't exist
                output.parent.mkdir(parents=True, exist_ok=True)
                
                output.write_text(html_output, encoding='utf-8')
                
                # Copy static CSS files to output directory
                output_dir = output.parent
                static_dir = output_dir / 'static'
                static_dir.mkdir(exist_ok=True)
                
                # Copy presets.css from src/render/static/ to output/static/
                source_css = Path(__file__).parent.parent / 'src' / 'render' / 'static' / 'presets.css'
                dest_css = static_dir / 'presets.css'
                
                if source_css.exists():
                    shutil.copy2(source_css, dest_css)
                    if verbose:
                        click.echo(f"Copied {source_css} -> {dest_css}", err=True)
                else:
                    click.echo(f"Warning: presets.css not found at {source_css}", err=True)
            else:
                click.echo(html_output)

        elif format.lower() == 'json':
            json_output = {
                "total_slides": len(renderables),
                "width": layout_width,
                "height": layout_height,
                "slides": [
                    {
                        "slide_number": r.slide_number,
                        "slide_id": r.slide_id,
                        "strategy": r.strategy_name,
                        "widgets": [
                            {
                                "role": assignment.role,
                                "type": assignment.widget.get_widget_type(),
                                "size": str(assignment.slot.size),
                            }
                            for assignment in r.widget_assignments
                        ],
                    }
                    for r in renderables
                ],
            }

            if output:
                if verbose:
                    click.echo(f"Writing JSON to {output}", err=True)
                output.write_text(json.dumps(json_output, indent=2), encoding='utf-8')
            else:
                click.echo(json.dumps(json_output, indent=2))

        if verbose:
            click.echo("✓ Rendering complete", err=True)

        sys.exit(0)

    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    cli()
