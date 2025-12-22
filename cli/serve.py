"""Simple HTTP server for Slidev presentations.

Usage:
    python -m cli.serve                    # List available presentations
    python -m cli.serve <name>             # Serve specific presentation
    python -m cli.serve <name> --port 8080 # Serve on custom port
    python -m cli.serve --all              # Serve all with index page
"""
import http.server
import os
import socketserver
import sys
from pathlib import Path
from typing import Optional

import click


def get_output_dirs() -> dict[str, Path]:
    """Find all _dist directories in output/dsl_test."""
    output_dir = Path(__file__).parent.parent / "output" / "dsl_test"
    
    if not output_dir.exists():
        return {}
    
    presentations = {}
    for item in output_dir.iterdir():
        if item.is_dir() and item.name.endswith("_dist"):
            # Remove _dist suffix for display name
            name = item.name[:-5]  # Remove "_dist"
            presentations[name] = item
    
    return dict(sorted(presentations.items()))


def create_index_html(presentations: dict[str, Path]) -> str:
    """Create an index page listing all presentations."""
    items = []
    for name, path in presentations.items():
        # Count slides by checking md- files in assets
        assets_dir = path / "assets"
        slide_count = "?"
        if assets_dir.exists():
            md_files = list(assets_dir.glob("md-*.js"))
            slide_count = str(len(md_files) // 2)  # Rough estimate
        
        items.append(f'''
        <a href="/{name}/" class="card">
            <div class="card-title">{name.replace("_", " ").title()}</div>
            <div class="card-meta">📊 ~{slide_count} slides</div>
        </a>''')
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Slidev Presentations</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            margin: 0;
            padding: 2rem;
            color: #fff;
        }}
        h1 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #00ffa3, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .subtitle {{
            text-align: center;
            color: #888;
            margin-bottom: 2rem;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            text-decoration: none;
            color: inherit;
            transition: all 0.3s ease;
        }}
        .card:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-color: #00ffa3;
            transform: translateY(-4px);
            box-shadow: 0 10px 40px rgba(0, 255, 163, 0.2);
        }}
        .card-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        .card-meta {{
            font-size: 0.85rem;
            color: #888;
        }}
        .footer {{
            text-align: center;
            margin-top: 3rem;
            color: #666;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <h1>🎨 Slidev Presentations</h1>
    <p class="subtitle">{len(presentations)} presentations available</p>
    <div class="grid">
        {"".join(items)}
    </div>
    <div class="footer">
        Use arrow keys to navigate slides • Press 'o' for overview
    </div>
</body>
</html>'''


class MultiPresentationHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that serves multiple presentations with routing."""
    
    presentations: dict[str, Path] = {}
    
    def translate_path(self, path: str) -> str:
        """Route requests to appropriate presentation directory."""
        # Remove query string
        path = path.split('?')[0]
        
        # Root index
        if path == '/' or path == '/index.html':
            return '__index__'
        
        # Check if path starts with a presentation name
        parts = path.strip('/').split('/')
        if parts and parts[0] in self.presentations:
            pres_name = parts[0]
            pres_path = self.presentations[pres_name]
            
            # Get the rest of the path
            rest = '/'.join(parts[1:]) if len(parts) > 1 else 'index.html'
            if not rest:
                rest = 'index.html'
            
            return str(pres_path / rest)
        
        # Fallback
        return super().translate_path(path)
    
    def do_GET(self):
        """Handle GET requests."""
        translated = self.translate_path(self.path)
        
        if translated == '__index__':
            # Serve index page
            content = create_index_html(self.presentations)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(content.encode()))
            self.end_headers()
            self.wfile.write(content.encode())
            return
        
        # For regular files, use the parent class
        super().do_GET()
    
    def log_message(self, format, *args):
        """Suppress logging for cleaner output."""
        pass


@click.command()
@click.argument('name', required=False)
@click.option('--port', '-p', default=8080, help='Port to serve on (default: 8080)')
@click.option('--all', '-a', 'serve_all', is_flag=True, help='Serve all presentations with index')
@click.option('--list', '-l', 'list_only', is_flag=True, help='List available presentations')
def serve(name: Optional[str], port: int, serve_all: bool, list_only: bool):
    """Serve Slidev presentations.
    
    \b
    Examples:
        python -m cli.serve                    # List presentations
        python -m cli.serve 01_startup_pitch   # Serve one presentation
        python -m cli.serve --all              # Serve all with index
    """
    presentations = get_output_dirs()
    
    if not presentations:
        click.echo("❌ No presentations found in output/dsl_test/")
        click.echo("   Run: python -m cli.uce_render --render data/dsl/<file>.json ...")
        sys.exit(1)
    
    if list_only or (not name and not serve_all):
        click.echo("📊 Available presentations:\n")
        for i, (pname, ppath) in enumerate(presentations.items(), 1):
            click.echo(f"  {i:2}. {pname}")
        click.echo(f"\n💡 Usage:")
        click.echo(f"   python -m cli.serve <name>   # Serve specific presentation")
        click.echo(f"   python -m cli.serve --all    # Serve all with index page")
        return
    
    if serve_all:
        # Serve all presentations with index
        MultiPresentationHandler.presentations = presentations
        
        with socketserver.TCPServer(("", port), MultiPresentationHandler) as httpd:
            click.echo(f"🚀 Serving {len(presentations)} presentations at http://localhost:{port}")
            click.echo(f"   Press Ctrl+C to stop\n")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                click.echo("\n👋 Stopped")
    else:
        # Serve single presentation
        if name not in presentations:
            # Try partial match
            matches = [p for p in presentations if name in p]
            if len(matches) == 1:
                name = matches[0]
            elif len(matches) > 1:
                click.echo(f"❌ Ambiguous name '{name}'. Matches: {', '.join(matches)}")
                sys.exit(1)
            else:
                click.echo(f"❌ Presentation '{name}' not found")
                click.echo(f"   Available: {', '.join(presentations.keys())}")
                sys.exit(1)
        
        pres_path = presentations[name]
        os.chdir(pres_path)
        
        handler = http.server.SimpleHTTPRequestHandler
        handler.log_message = lambda *args: None  # Suppress logging
        
        with socketserver.TCPServer(("", port), handler) as httpd:
            click.echo(f"🚀 Serving '{name}' at http://localhost:{port}")
            click.echo(f"   Press Ctrl+C to stop\n")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                click.echo("\n👋 Stopped")


if __name__ == '__main__':
    serve()
