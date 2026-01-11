
import sys
from pathlib import Path
from typing import Dict, Any

# Mock the class to test just the method
class MockSlidesExporter:
    def _theme_to_typescript_object(self, obj: Any, indent: int = 0) -> str:
        """Convert theme object to TypeScript object literal."""
        ind = '  ' * indent
        next_ind = '  ' * (indent + 1)
        
        if isinstance(obj, dict):
            if not obj:
                return '{}'
            lines = ['{']
            for key, value in obj.items():
                ts_value = self._theme_to_typescript_object(value, indent + 1)
                # handle keys that might need quotes if they aren't valid identifiers, 
                # but for this test simple keys are fine.
                lines.append(f"{next_ind}{key}: {ts_value},")
            lines.append(f"{ind}}}")
            return '\n'.join(lines)
        elif isinstance(obj, str):
            return f"'{obj}'"
        else:
            return str(obj)

    def _export_theme_to_typescript(self, theme_data: Dict[str, Any], output_dir: Path) -> None:
        """Export theme as TypeScript file with type definitions.
        
        Args:
            theme_data: Theme dictionary from state
            output_dir: Output directory (same as slides.mdx parent)
        """
        theme_id = theme_data.get('id', 'custom_theme')
        theme_file = output_dir / f"{theme_id}.ts"
        
        # Check if theme_data is already in the new nested format (ThemeDefinition)
        if 'colors' in theme_data and isinstance(theme_data['colors'], dict):
            # Already in new format - use directly but ensure top-level metadata
            adapted_theme = theme_data.copy()
            # Ensure name matches filename ID
            adapted_theme['name'] = theme_id
            if 'displayName' not in adapted_theme:
                 adapted_theme['displayName'] = theme_data.get('name', theme_id)
        else:
            # Legacy Fallback would go here, but omitted for this specific test case
            print("Legacy path taken (unexpected for this test)")
            return
        
        ts_content = f"""/**
 * Generated Custom Theme: {theme_id}
 */

import type {{ ThemeDefinition }} from '@/utils/types';

export const {theme_id}: ThemeDefinition = {self._theme_to_typescript_object(adapted_theme, indent=0)};

export default {theme_id};
"""
        # Write to checking file
        with open("debug_export_output.txt", "w") as f:
            f.write(ts_content)

def test_export():
    exporter = MockSlidesExporter()
    
    # New format theme data
    new_theme_data = {
        "id": "theme_test_new",
        "name": "Test New Theme",
        "colors": {
            "bg": "#ffffff",
            "primary": "#000000"
        },
        "typography": {
            "fontDisplay": "Arial"
        }
    }
    
    # We are just printing to stdout to verify logic
    exporter._export_theme_to_typescript(new_theme_data, Path("."))

if __name__ == "__main__":
    test_export()
