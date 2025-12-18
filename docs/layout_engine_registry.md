# Layout Engine Registry

The Layout Engine Registry provides runtime selection and management of layout engine implementations, enabling seamless switching between different layout systems without code changes.

## Overview

```python
from src.layout.engine_registry import LayoutEngineRegistry

# Register your engine
LayoutEngineRegistry.register("myengine", MyLayoutEngine)

# Switch at runtime
LayoutEngineRegistry.set_active_engine("myengine")

# Or use environment variable
# export LAYOUT_ENGINE=myengine

# Content generation automatically uses active engine
```

## Key Features

✅ **Multiple Engines** - Register and manage multiple layout implementations  
✅ **Runtime Switching** - Change engines without code modifications  
✅ **Environment Configuration** - Control via `LAYOUT_ENGINE` env var  
✅ **Auto-registration** - Dummy engine registered on import  
✅ **Protocol-based** - Works with any `LayoutEngine` implementation  
✅ **Priority System** - Env var → Programmatic → Default  

## Usage

### 1. Register an Engine

```python
from src.layout.engine_registry import LayoutEngineRegistry
from src.layout.layout_engine_protocol import LayoutEngine

class MyLayoutEngine:
    """Your layout engine implementation."""
    
    @classmethod
    def get_layout_documentation(cls) -> str:
        return "Your layout documentation..."
    
    @classmethod
    def calculate(cls, strategy_name, widget_assignments, theme, style, width, height):
        # Your calculation logic
        ...
    
    @classmethod
    def calculate_slides(cls, slides, theme, style, width, height):
        # Your slides calculation logic
        ...

# Register it
LayoutEngineRegistry.register("myengine", MyLayoutEngine)
```

### 2. List Available Engines

```python
engines = LayoutEngineRegistry.list_engines()
print(engines.keys())  # dict_keys(['dummy', 'myengine'])

active_name = LayoutEngineRegistry.get_active_engine_name()
print(f"Active: {active_name}")  # Active: dummy
```

### 3. Switch Engines

**Method A: Programmatic**
```python
LayoutEngineRegistry.set_active_engine("myengine")
```

**Method B: Environment Variable**
```bash
# Windows PowerShell
$env:LAYOUT_ENGINE = "myengine"

# Linux/Mac
export LAYOUT_ENGINE=myengine
```

**Method C: Default (First Registered)**
```python
# The first registered engine becomes the default
# Usually 'dummy' which is auto-registered
```

### 4. Get Active Engine

```python
# Get the active engine class
active_engine = LayoutEngineRegistry.get_active_engine()

# Use it for layout documentation
docs = active_engine.get_layout_documentation()

# Use it for calculations
renderable = active_engine.calculate(
    strategy_name="Bento.Standard",
    widget_assignments={...},
    theme=theme,
    style=style
)
```

## Integration with Content Generation

The registry is integrated into the content generation pipeline:

```python
# In src/generation/content/prompts.py

def _build_state_transition_system_prompt() -> str:
    # Get layout documentation from currently active layout engine
    active_engine = LayoutEngineRegistry.get_active_engine()
    layout_documentation = active_engine.get_layout_documentation()
    
    # Use in prompt template
    return f"""...
    {layout_documentation}
    ..."""
```

This means:
- **Prompt templates** are engine-agnostic
- **Switching engines** updates prompt content automatically
- **No code changes** required to use different layout systems

## CLI Integration

The CLI automatically uses the active engine:

```python
# In cli/uce_render.py

# Get active engine for rendering
active_engine = LayoutEngineRegistry.get_active_engine()
renderables = active_engine.calculate_slides(
    slides=slides,
    theme=theme,
    style=style,
    width=layout_width,
    height=layout_height
)
```

Use it from command line:

```bash
# Use default (dummy) engine
python -m cli.uce_render data/test.json

# Switch via environment variable
export LAYOUT_ENGINE=custom
python -m cli.uce_render data/test.json

# Back to default
unset LAYOUT_ENGINE
python -m cli.uce_render data/test.json
```

## Priority System

The active engine is determined by this priority order:

1. **Environment Variable** (`LAYOUT_ENGINE`) - Highest priority
   - Allows deployment-time configuration
   - No code changes required
   - Example: `export LAYOUT_ENGINE=production_engine`

2. **Programmatic Selection** (`set_active_engine()`)
   - Set explicitly in code
   - Good for testing and development
   - Example: `LayoutEngineRegistry.set_active_engine("test_engine")`

3. **Default (First Registered)** - Lowest priority
   - Usually "dummy" (auto-registered on import)
   - Fallback when nothing else specified

## Auto-registration

The dummy engine is automatically registered when the registry module loads:

```python
# Happens automatically on import
from src.layout import LayoutEngineRegistry
# 'dummy' is now registered

LayoutEngineRegistry.get_active_engine_name()  # 'dummy'
```

You can auto-register your own engine similarly:

```python
# In your engine module's __init__.py
from src.layout.engine_registry import LayoutEngineRegistry
from .my_engine import MyEngine

LayoutEngineRegistry.register("myengine", MyEngine)
```

## Example: Multiple Engines

```python
from src.layout.engine_registry import LayoutEngineRegistry

# Register multiple engines
LayoutEngineRegistry.register("dummy", DummyEngine)
LayoutEngineRegistry.register("advanced", AdvancedEngine)
LayoutEngineRegistry.register("experimental", ExperimentalEngine)

# List them
print(LayoutEngineRegistry.list_engines().keys())
# dict_keys(['dummy', 'advanced', 'experimental'])

# Switch between them
LayoutEngineRegistry.set_active_engine("advanced")
# Content generation now uses AdvancedEngine layouts

LayoutEngineRegistry.set_active_engine("experimental")
# Content generation now uses ExperimentalEngine layouts
```

## Testing

For testing, you can reset the registry:

```python
import pytest
from src.layout.engine_registry import LayoutEngineRegistry

@pytest.fixture
def clean_registry():
    """Ensure clean registry for each test."""
    LayoutEngineRegistry.reset()
    # Register test engines
    LayoutEngineRegistry.register("test", TestEngine)
    yield
    # Clean up
    LayoutEngineRegistry.reset()

def test_engine_switching(clean_registry):
    LayoutEngineRegistry.set_active_engine("test")
    active = LayoutEngineRegistry.get_active_engine()
    assert active == TestEngine
```

## Error Handling

```python
# Attempting to register duplicate name
try:
    LayoutEngineRegistry.register("dummy", SomeOtherEngine)
except ValueError as e:
    print(e)  # Layout engine 'dummy' is already registered

# Attempting to get non-existent engine
try:
    LayoutEngineRegistry.get_engine("nonexistent")
except KeyError as e:
    print(e)  # Layout engine 'nonexistent' not found. Available: dummy

# Attempting to set non-existent engine as active
try:
    LayoutEngineRegistry.set_active_engine("nonexistent")
except KeyError as e:
    print(e)  # Cannot set active engine 'nonexistent' - not registered
```

## API Reference

### `register(name, engine_class)`
Register a layout engine implementation.

**Parameters:**
- `name` (str): Unique identifier for the engine
- `engine_class` (Type[LayoutEngine]): Engine class implementing LayoutEngine protocol

**Raises:**
- `ValueError`: If name already registered

### `get_engine(name)`
Get a specific engine by name.

**Parameters:**
- `name` (str): Engine identifier

**Returns:**
- `Type[LayoutEngine]`: Engine class

**Raises:**
- `KeyError`: If engine not found

### `get_active_engine()`
Get the currently active engine.

**Returns:**
- `Type[LayoutEngine]`: Active engine class

**Priority:** Environment var → Programmatic → First registered

**Raises:**
- `RuntimeError`: If no engines registered

### `set_active_engine(name)`
Set the active engine programmatically.

**Parameters:**
- `name` (str): Engine identifier

**Raises:**
- `KeyError`: If engine not found

### `get_active_engine_name()`
Get the name of the active engine.

**Returns:**
- `Optional[str]`: Active engine name or None

### `list_engines()`
List all registered engines.

**Returns:**
- `Dict[str, Type[LayoutEngine]]`: Engine name → Engine class mapping

### `reset()`
Reset registry (for testing).

Clears all registered engines and active selection.

## See Also

- [Layout Documentation Decoupling](../LAYOUT_DOCUMENTATION_DECOUPLING.md) - Architecture overview
- [Layout Engine Protocol](../src/layout/layout_engine_protocol.py) - Protocol definition
- [Example: Runtime Switching](../examples/layout_engine_switching.py) - Complete demo
