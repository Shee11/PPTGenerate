"""Example demonstrating how Python Protocols work.

Python Protocols enable "structural subtyping" - a class satisfies a Protocol
if it has the required methods, WITHOUT needing to inherit from it.

This is also called "duck typing with type checking".
"""

from typing import Protocol


# ============================================================================
# PROTOCOL DEFINITION (Interface)
# ============================================================================

class Renderer(Protocol):
    """Protocol defining what a renderer must do."""
    
    def render(self, data: str) -> str:
        """Render data to output format."""
        ...


# ============================================================================
# IMPLEMENTATIONS (No inheritance needed!)
# ============================================================================

class HTMLRenderer:
    """Renders to HTML - satisfies Renderer protocol WITHOUT inheriting."""
    
    def render(self, data: str) -> str:
        return f"<html>{data}</html>"


class MarkdownRenderer:
    """Renders to Markdown - also satisfies Renderer protocol."""
    
    def render(self, data: str) -> str:
        return f"# {data}"


class PDFRenderer:
    """Renders to PDF - also satisfies Renderer protocol."""
    
    def render(self, data: str) -> str:
        return f"PDF[{data}]"


# ============================================================================
# USAGE - Type checker knows these are valid Renderers
# ============================================================================

def process_with_renderer(renderer: Renderer, data: str) -> str:
    """This function accepts ANY object that has a render() method.
    
    Type checkers (mypy, pyright) will verify that the passed object
    has the required render() method.
    """
    return renderer.render(data)


# All of these work - type checker is happy!
html = HTMLRenderer()
result1 = process_with_renderer(html, "Hello")  # ✓ Valid

md = MarkdownRenderer()
result2 = process_with_renderer(md, "World")  # ✓ Valid

pdf = PDFRenderer()
result3 = process_with_renderer(pdf, "Test")  # ✓ Valid


# ============================================================================
# WHY USE PROTOCOLS?
# ============================================================================

"""
1. **No Inheritance Required**:
   - HTMLRenderer doesn't inherit from Renderer
   - It just has a render() method
   - This is "structural typing" vs "nominal typing"

2. **Type Safety**:
   - Type checkers verify methods exist
   - Catches errors at development time
   - Better IDE autocomplete

3. **Flexibility**:
   - Can work with third-party classes
   - Don't need to modify existing code
   - Multiple implementations without coupling

4. **Documentation**:
   - Protocol clearly documents the interface
   - Shows what methods are required
   - Serves as a contract

EXAMPLE IN OUR CODEBASE:
- LayoutEngine protocol defines: calculate(), calculate_slides()
- DummyLayoutEngine implements these methods
- No need to inherit - just match the signature
- Type checker verifies compliance
- Can add new layout engines without modifying protocol
"""

# ============================================================================
# COMPARE: Traditional Inheritance vs Protocol
# ============================================================================

# OLD WAY (Nominal Typing):
# class HTMLRenderer(Renderer):  # Must inherit
#     def render(self, data: str) -> str: ...

# NEW WAY (Structural Typing with Protocol):
# class HTMLRenderer:  # No inheritance needed!
#     def render(self, data: str) -> str: ...
# Type checker sees it has render() → treats it as a Renderer
