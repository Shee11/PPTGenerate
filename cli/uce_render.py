"""CLI for UCE Render - uce-render command."""
import json
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
                    click.echo(f"  Allowed Sizes: {', '.join(widget['allowed_sizes'])}")
                    if widget.get('description'):
                        click.echo(f"  Description: {widget['description']}")
                    
                    if widget.get('fields'):
                        click.echo("  Fields:")
                        for field_name, field_info in widget['fields'].items():
                            click.echo(f"    - {field_name}: {field_info['type']}")
                            if field_info.get('description'):
                                click.echo(f"      {field_info['description']}")
                
                click.echo("\n" + "=" * 80)
                click.echo(f"Total: {len(widgets)} widgets\n")
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
                output.write_text(html_output, encoding='utf-8')
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
