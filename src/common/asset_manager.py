"""Asset management system for themes, styles, widgets, and layout strategies.

Provides:
- JSON serialization/deserialization for all asset types
- Schema generation and validation
- Asset discovery and listing
- File persistence under assets/ directory
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel

from src.common.size_class import SizeClass
from src.layout.style import Style
from src.layout.theme import Theme
from src.widgets.base import BaseWidget, WidgetRegistry

T = TypeVar('T', bound=BaseModel)


class AssetManager:
    """Manages serialization, persistence, and discovery of UCE assets."""
    
    @staticmethod
    def _get_assets_root() -> Path:
        """Get the default assets root directory."""
        return Path(__file__).parent.parent.parent / "assets"
    
    @staticmethod
    def _get_themes_dir() -> Path:
        """Get the themes directory."""
        themes_dir = AssetManager._get_assets_root() / "themes"
        themes_dir.mkdir(parents=True, exist_ok=True)
        return themes_dir
    
    @staticmethod
    def _get_styles_dir() -> Path:
        """Get the styles directory."""
        styles_dir = AssetManager._get_assets_root() / "styles"
        styles_dir.mkdir(parents=True, exist_ok=True)
        return styles_dir
    
    @staticmethod
    def _get_schemas_dir() -> Path:
        """Get the schemas directory."""
        schemas_dir = AssetManager._get_assets_root() / "schemas"
        schemas_dir.mkdir(parents=True, exist_ok=True)
        return schemas_dir
    
    # ========== Theme Management ==========
    
    @staticmethod
    def save_theme(theme: Theme, filename: Optional[str] = None) -> Path:
        """Save theme to JSON file.
        
        Args:
            theme: Theme instance to save
            filename: Output filename (default: {theme.id}.json)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            filename = f"{theme.id}.json"
        
        filepath = AssetManager._get_themes_dir() / filename
        
        # Serialize to JSON
        theme_dict = theme.model_dump(mode='json', exclude_none=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(theme_dict, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    @staticmethod
    def load_theme(filename: str) -> Theme:
        """Load theme from JSON file.
        
        Args:
            filename: Theme filename (e.g., "corp_modern.json")
            
        Returns:
            Theme instance
        """
        filepath = AssetManager._get_themes_dir() / filename
        
        with open(filepath, 'r', encoding='utf-8') as f:
            theme_dict = json.load(f)
        
        return Theme.model_validate(theme_dict)
    
    @staticmethod
    def list_themes() -> Dict[str, Any]:
        """List all available themes with schema information.
        
        Returns:
            Dictionary with available_themes list and schema fields
        """
        themes = []
        
        # Get the schema from the Theme model
        theme_schema = Theme.model_json_schema()
        properties = theme_schema.get('properties', {})
        required_fields = theme_schema.get('required', [])
        
        # List available theme files
        for filepath in AssetManager._get_themes_dir().glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    theme_dict = json.load(f)
                
                themes.append({
                    "name": filepath.stem,
                    "file": str(filepath),
                    "id": theme_dict.get("id", filepath.stem),
                })
            except Exception:
                continue
        
        # Build schema field information
        schema_fields = {}
        for field_name, field_info in properties.items():
            field_type = field_info.get('type', 'object')
            if 'anyOf' in field_info:
                field_type = field_info['anyOf'][0].get('type', 'object')
            
            schema_fields[field_name] = {
                "type": field_type,
                "description": field_info.get('description', ''),
                "required": field_name in required_fields,
            }
            if 'default' in field_info:
                schema_fields[field_name]["default"] = field_info['default']
        
        return {
            "available_themes": sorted(themes, key=lambda x: x["name"]),
            "schema": {
                "fields": schema_fields
            }
        }
    
    # ========== Style Management ==========
    
    @staticmethod
    def save_style(style: Style, filename: Optional[str] = None) -> Path:
        """Save style to JSON file.
        
        Args:
            style: Style instance to save
            filename: Output filename (default: {theme_name}_style.json)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            filename = f"{style.theme_name}_style.json"
        
        filepath = AssetManager._get_styles_dir() / filename
        
        style_dict = style.model_dump(mode='json', exclude_none=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(style_dict, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    @staticmethod
    def load_style(filename: str) -> Style:
        """Load style from JSON file.
        
        Args:
            filename: Style filename
            
        Returns:
            Style instance
        """
        filepath = AssetManager._get_styles_dir() / filename
        
        with open(filepath, 'r', encoding='utf-8') as f:
            style_dict = json.load(f)
        
        return Style.model_validate(style_dict)
    
    @staticmethod
    def list_styles() -> Dict[str, Any]:
        """List all available styles with schema information.
        
        Returns:
            Dictionary with available_styles list and schema fields
        """
        styles = []
        
        # Get the schema from the Style model
        style_schema = Style.model_json_schema()
        properties = style_schema.get('properties', {})
        required_fields = style_schema.get('required', [])
        
        for filepath in AssetManager._get_styles_dir().glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    style_dict = json.load(f)
                
                styles.append({
                    "name": filepath.stem,
                    "file": str(filepath),
                    "theme_name": style_dict.get("theme_name", "unknown"),
                })
            except Exception:
                continue
        
        # Build schema field information
        schema_fields = {}
        for field_name, field_info in properties.items():
            field_type = field_info.get('type', 'object')
            if 'anyOf' in field_info:
                field_type = field_info['anyOf'][0].get('type', 'object')
            
            schema_fields[field_name] = {
                "type": field_type,
                "description": field_info.get('description', ''),
                "required": field_name in required_fields,
            }
            if 'default' in field_info:
                schema_fields[field_name]["default"] = field_info['default']
        
        return {
            "available_styles": sorted(styles, key=lambda x: x["name"]),
            "schema": {
                "fields": schema_fields
            }
        }
    
    # ========== Widget Discovery ==========
    
    @staticmethod
    def list_widgets() -> List[Dict[str, Any]]:
        """List all registered widget types with schema information.
        
        Returns:
            List of widget metadata dictionaries with schema fields
        """
        widgets = []
        
        for widget_type, widget_class in WidgetRegistry._widgets.items():
            min_size = widget_class.get_min_size()
            # All sizes >= min_size are allowed
            all_sizes = [SizeClass.S, SizeClass.M, SizeClass.L, SizeClass.XL]
            allowed_sizes = [str(size) for size in all_sizes if size >= min_size]
            
            # Get widget schema
            widget_schema = widget_class.model_json_schema()
            properties = widget_schema.get('properties', {})
            
            # Build field information
            schema_fields = {}
            for field_name, field_info in properties.items():
                # Handle parameters field specially - extract from docstring
                if field_name == 'parameters':
                    # Try to parse parameter info from docstring
                    param_info = AssetManager._extract_parameters_from_docstring(
                        widget_schema.get('description', '')
                    )
                    schema_fields[field_name] = {
                        "type": field_info.get('type', 'object'),
                        "description": field_info.get('description', ''),
                        "parameters": param_info,
                    }
                else:
                    field_type = field_info.get('type', 'object')
                    if 'anyOf' in field_info:
                        field_type = field_info['anyOf'][0].get('type', 'object')
                    
                    schema_fields[field_name] = {
                        "type": field_type,
                        "description": field_info.get('description', ''),
                    }
                    if 'default' in field_info:
                        schema_fields[field_name]["default"] = field_info['default']
            
            widgets.append({
                "type": widget_type,
                "category": widget_type.split('.')[0],  # Type, Data, Media, Chart
                "allowed_sizes": allowed_sizes,
                "description": widget_schema.get('description', ''),
                "fields": schema_fields,
            })
        
        return sorted(widgets, key=lambda x: x["type"])
    
    @staticmethod
    def _extract_parameters_from_docstring(docstring: str) -> List[Dict[str, str]]:
        """Extract parameter information from widget docstring.
        
        Args:
            docstring: Widget class docstring
            
        Returns:
            List of parameter dictionaries with name and description
        """
        params = []
        lines = docstring.split('\n')
        in_params_section = False
        
        for line in lines:
            stripped = line.strip()
            
            # Check if we're entering the Parameters section
            if stripped.startswith('Parameters:'):
                in_params_section = True
                continue
            
            # Check if we're leaving the Parameters section
            if in_params_section and stripped.startswith('Styling'):
                break
            
            # Parse parameter lines (format: "- name (type): description")
            if in_params_section and stripped.startswith('- '):
                # Extract parameter info
                param_line = stripped[2:]  # Remove "- "
                if ':' in param_line:
                    name_type, description = param_line.split(':', 1)
                    # Extract name and type
                    if '(' in name_type and ')' in name_type:
                        name = name_type.split('(')[0].strip()
                        param_type = name_type.split('(')[1].split(')')[0].strip()
                        params.append({
                            "name": name,
                            "type": param_type,
                            "description": description.strip(),
                        })
        
        return params
    
    @staticmethod
    def get_widget_schema(widget_type: str) -> Dict[str, Any]:
        """Get JSON schema for a specific widget type.
        
        Args:
            widget_type: Widget type (e.g., "Type.Display")
            
        Returns:
            JSON schema dictionary
        """
        widget_class = WidgetRegistry.get(widget_type)
        if not widget_class:
            raise ValueError(f"Widget type '{widget_type}' not found")
        
        # Get Pydantic schema
        schema = widget_class.model_json_schema()
        
        # Add widget-specific metadata
        min_size = widget_class.get_min_size()
        all_sizes = [SizeClass.S, SizeClass.M, SizeClass.L, SizeClass.XL]
        allowed_sizes = [str(size) for size in all_sizes if size >= min_size]
        
        schema["widget_type"] = widget_type
        schema["allowed_sizes"] = allowed_sizes
        
        return schema
    
    # ========== Layout Strategy Discovery ==========
    
    @staticmethod
    def list_strategies() -> List[Dict[str, Any]]:
        """List all available layout strategies.
        
        Returns:
            List of strategy metadata dictionaries
        """
        from src.layout.layout_engine import LayoutEngine
        
        strategies = []
        
        for strategy_name, strategy_class in LayoutEngine._strategies.items():
            slots = strategy_class.get_slots()
            
            strategies.append({
                "name": strategy_name,
                "family": strategy_name.split('.')[0],  # Bento, Swiss, Cinematic
                "slots": [
                    {
                        "role": slot.role,
                        "size": str(slot.size),
                    }
                    for slot in slots
                ],
            })
        
        return sorted(strategies, key=lambda x: x["name"])
    
    # ========== Schema Generation ==========
    
    @staticmethod
    def generate_schemas() -> Dict[str, Path]:
        """Generate and save JSON schemas for all asset types.
        
        Returns:
            Dictionary mapping schema name to file path
        """
        schemas_saved = {}
        
        # Theme schema
        theme_schema = Theme.model_json_schema()
        theme_path = AssetManager._get_schemas_dir() / "theme.schema.json"
        with open(theme_path, 'w', encoding='utf-8') as f:
            json.dump(theme_schema, f, indent=2)
        schemas_saved["theme"] = theme_path
        
        # Style schema
        style_schema = Style.model_json_schema()
        style_path = AssetManager._get_schemas_dir() / "style.schema.json"
        with open(style_path, 'w', encoding='utf-8') as f:
            json.dump(style_schema, f, indent=2)
        schemas_saved["style"] = style_path
        
        # Widget schemas (all registered widgets)
        for widget_type in WidgetRegistry._widgets.keys():
            schema = AssetManager.get_widget_schema(widget_type)
            safe_name = widget_type.replace('.', '_').lower()
            widget_path = AssetManager._get_schemas_dir() / f"widget_{safe_name}.schema.json"
            with open(widget_path, 'w', encoding='utf-8') as f:
                json.dump(schema, f, indent=2)
            schemas_saved[f"widget_{safe_name}"] = widget_path
        
        return schemas_saved
    
    # ========== Generic Model Persistence ==========
    
    @staticmethod
    def save_model(
        model: BaseModel,
        filepath: Path,
    ) -> Path:
        """Save any Pydantic model to JSON file.
        
        Args:
            model: Pydantic model instance
            filepath: Output file path
            
        Returns:
            Path to saved file
        """
        model_dict = model.model_dump(mode='json', exclude_none=True)
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(model_dict, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    @staticmethod
    def load_model(
        model_class: Type[T],
        filepath: Path,
    ) -> T:
        """Load any Pydantic model from JSON file.
        
        Args:
            model_class: Pydantic model class
            filepath: Input file path
            
        Returns:
            Model instance
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            model_dict = json.load(f)
        
        return model_class.model_validate(model_dict)
