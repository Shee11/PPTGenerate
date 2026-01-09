"""Codegen Tool - Generate React code for invented components.

LLMTool: Uses LLM to generate React/TypeScript code for InventComponent placeholders.

This tool:
1. Extracts all <InventComponent> from content step MDX output
2. Generates React component code for each
3. Stores generated code in state.generated_components
"""
from __future__ import annotations

import os
import re
import json
from pathlib import Path
from typing import TYPE_CHECKING, Optional, List, Dict, Any, ClassVar
from pydantic import Field

from src.common.tool_protocol import LLMTool, ToolContext, ToolPatch, register_tool
from src.utils.llm_client import call_llm

if TYPE_CHECKING:
    from src.generation.state import PipelineState
    from src.generation.todo.models import ConstitutionPatch


class CodegenContext(ToolContext):
    """Context for code generation."""
    invented_components: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of InventComponent specs extracted from slides"
    )
    existing_components: List[str] = Field(
        default_factory=list,
        description="Names of existing components for reference"
    )


class CodegenPatch(ToolPatch):
    """Patch containing generated component code."""
    generated_components: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Map of component_id -> {name, code, props_interface}"
    )


def _extract_invent_components_from_mdx(mdx_text: str) -> List[Dict[str, Any]]:
    print("Shiyi DEBUG: _extract_invent_components_from_mdx called")
    """Extract all InventComponent specs from MDX text (content step output)."""
    if not mdx_text:
        return []
    
    text = mdx_text.strip()
    
    # 1. Handle code fences: find ALL fences and join them.
    #    This mirrors ui.py logic and handles cases with multiple blocks.
    fence_pattern = r'```(?:mdx|jsx|xml|html)?\s*\n([\s\S]*?)\n```'
    fence_matches = re.findall(fence_pattern, text, flags=re.IGNORECASE)
    if fence_matches:
        text = "\n".join(m.strip() for m in fence_matches)

    # 2. Extract slides and components
    #    Use a dict keyed by component ID to deduplicate (latest wins)
    #    This fixes issues with draft/history blocks being included
    components_map = {}
    
    slide_pattern = r'<Slide\b([^>]*)>(.*?)</Slide>'
    
    for slide_match in re.finditer(slide_pattern, text, re.DOTALL | re.IGNORECASE):
        slide_attrs = slide_match.group(1)
        slide_body = slide_match.group(2)
        
        # Extract slide ID
        m_sid = re.search(r"\bid\s*=\s*\"([^\"]+)\"", slide_attrs)
        slide_id = (m_sid.group(1) if m_sid else "unknown").strip()

        # Find InventComponent tags
        invent_pattern = r'<InventComponent\s+([\s\S]*?)(?:/>|>\s*</InventComponent>)'
        
        for match in re.finditer(invent_pattern, slide_body):
            attrs_str = match.group(1)
            
            # Extract id (REQUIRED)
            id_match = re.search(r'id\s*=\s*["\']([^"\']+)["\']', attrs_str)
            comp_id = id_match.group(1) if id_match else f"invented_{slide_id}_{len(components_map)}"
            
            component = {
                "slide_id": slide_id,
                "id": comp_id,
                "raw": match.group(0),
            }
            
            # Extract name (REQUIRED per new prompt)
            name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', attrs_str)
            if name_match:
                component["name"] = name_match.group(1)

            # Extract intent
            intent_match = re.search(r'intent\s*=\s*["\']([^"\']+)["\']', attrs_str)
            if intent_match:
                component["intent"] = intent_match.group(1)
            
            # Extract data
            data_match = re.search(r'data\s*=\s*\{\{([\s\S]*?)\}\}', attrs_str)
            if data_match:
                component["data"] = data_match.group(1).strip()

            # Extract visual_logic
            visual_logic_match = re.search(r'visual_logic\s*=\s*\{\{([\s\S]*?)\}\}', attrs_str)
            if visual_logic_match:
                component["visual_logic"] = visual_logic_match.group(1).strip()

            # Extract theme_mapping
            theme_mapping_match = re.search(r'theme_mapping\s*=\s*\{\{([\s\S]*?)\}\}', attrs_str)
            if theme_mapping_match:
                component["theme_mapping"] = theme_mapping_match.group(1).strip()
            
            # Extract notes
            notes_match = re.search(r'notes\s*=\s*["\']([^"\']+)["\']', attrs_str)
            if notes_match:
                component["notes"] = notes_match.group(1)
            
            # Upsert into map (latest occurrence wins)
            components_map[comp_id] = component
            
    return list(components_map.values())


def _read_content_mdx_from_trace() -> str:
    """Read the content step MDX output from the LLM trace file."""
    trace_file = os.getenv("LLM_TRACE_FILE")
    if not trace_file:
        return ""
    
    trace_path = Path(trace_file)
    if not trace_path.exists():
        return ""
    
    try:
        content_responses = []
        with open(trace_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if record.get("step") == "content" and record.get("response"):
                        content_responses.append(record["response"])
                except json.JSONDecodeError:
                    continue
        
        # Return the last (most recent) content response
        return content_responses[-1] if content_responses else ""
    except Exception:
        return ""


def _get_existing_component_names() -> List[str]:
    """Get list of existing component names from the library."""
    # Standard components available in the system
    return [
        "Heading", "Text", "SmartList", "BigNum", "MetricGroup",
        "ChartBar", "ChartLine", "ChartPie", "NetworkGraph", "ProcessStrip",
        "Callout", "Quote", "Image", "Icon", "Badge", "Tag",
        "DataTable", "Timeline", "Comparison", "FeatureGrid"
    ]


def _validate_and_fix_component_code(
    code: str, 
    props_interface: str, 
    component_name: str
) -> tuple[str, str, list[str]]:
    """Validate and fix common issues in LLM-generated component code.
    
    Args:
        code: The component code (should be just the export const ... function)
        props_interface: The props interface definition
        component_name: Expected component name
        
    Returns:
        Tuple of (fixed_code, fixed_props_interface, list_of_fixes_applied)
    """
    fixes = []
    fixed_code = code.strip()
    fixed_props = props_interface.strip()

    # 1. Remove disallowed imports, keep only react / framer-motion / lucide-react
    allowed_modules = {"react", "framer-motion", "lucide-react"}
    import_line_re = re.compile(r'^\s*import\s+.*?from\s+["\']([^"\']+)["\'];?\s*$', re.MULTILINE)
    kept_lines: list[str] = []
    removed_count = 0
    for line in fixed_code.splitlines():
        m = import_line_re.match(line)
        if not m:
            kept_lines.append(line)
            continue
        module = m.group(1)
        if module in allowed_modules:
            kept_lines.append(line)
        else:
            removed_count += 1
    if removed_count:
        fixes.append(f"Removed {removed_count} disallowed import(s)")
    fixed_code = "\n".join(kept_lines).strip()

    # 1.1 Auto-inject missing allowed imports if referenced
    has_react_import = bool(re.search(r"^\s*import\s+.*from\s+['\"]react['\"]", fixed_code, re.MULTILINE))
    has_motion_import = bool(re.search(r"^\s*import\s+.*from\s+['\"]framer-motion['\"]", fixed_code, re.MULTILINE))
    has_lucide_import = bool(re.search(r"^\s*import\s+.*from\s+['\"]lucide-react['\"]", fixed_code, re.MULTILINE))

    needs_react = bool(re.search(r"\bReact\.", fixed_code))
    needs_motion = bool(re.search(r"<\s*motion\b|\bmotion\.", fixed_code))
    needs_lucide = bool(re.search(r"\bLucide\.", fixed_code))

    import_inserts: list[str] = []
    if needs_react and not has_react_import:
        import_inserts.append("import React from 'react';")
        fixes.append("Added missing react import")
    if needs_motion and not has_motion_import:
        import_inserts.append("import { motion } from 'framer-motion';")
        fixes.append("Added missing framer-motion import")
    if needs_lucide and not has_lucide_import:
        import_inserts.append("import * as Lucide from 'lucide-react';")
        fixes.append("Added missing lucide-react import")

    if import_inserts:
        fixed_code = "\n".join(import_inserts) + "\n\n" + fixed_code
    
    # 2. Remove duplicate interface definitions from code
    # Match interface definitions that appear in code but belong in props_interface
    interface_pattern = r'^(?:export\s+)?interface\s+\w+Props\s*\{[^}]*\}\s*\n?'
    interface_matches = re.findall(interface_pattern, fixed_code, re.MULTILINE | re.DOTALL)
    if interface_matches:
        # Keep only the component function in code
        fixed_code = re.sub(interface_pattern, '', fixed_code, flags=re.MULTILINE | re.DOTALL)
        fixes.append(f"Removed {len(interface_matches)} duplicate interface(s) from code")
    
    # 3. Remove duplicate type definitions from code
    type_pattern = r'^(?:export\s+)?type\s+\w+\s*=\s*[^;]+;\s*\n?'
    type_matches = re.findall(type_pattern, fixed_code, re.MULTILINE)
    if type_matches:
        fixed_code = re.sub(type_pattern, '', fixed_code, flags=re.MULTILINE)
        fixes.append(f"Removed {len(type_matches)} duplicate type definition(s) from code")
    
    # 4. Remove imports from props_interface (should only have interface)
    props_import_pattern = r'^\s*import\s+.*?\n'
    if re.search(props_import_pattern, fixed_props, re.MULTILINE):
        fixed_props = re.sub(props_import_pattern, '', fixed_props, flags=re.MULTILINE)
        fixes.append("Removed import statement(s) from props_interface")
    
    # 5. Ensure props_interface has export keyword
    if fixed_props and not fixed_props.strip().startswith('export'):
        # Check if it starts with 'interface' and add export
        if fixed_props.strip().startswith('interface'):
            fixed_props = 'export ' + fixed_props.strip()
            fixes.append("Added 'export' keyword to interface")
    
    # 6. Ensure code has export keyword for the component
    if fixed_code and 'export' not in fixed_code[:50]:
        # Check if it starts with 'const ComponentName'
        const_pattern = rf'^const\s+{re.escape(component_name)}\s*'
        if re.match(const_pattern, fixed_code.strip()):
            fixed_code = 'export ' + fixed_code.strip()
            fixes.append("Added 'export' keyword to component")
    
    # 7. Clean up excessive whitespace
    fixed_code = re.sub(r'\n{3,}', '\n\n', fixed_code).strip()
    fixed_props = re.sub(r'\n{3,}', '\n\n', fixed_props).strip()
    
    # 8. Validate component name matches expected
    expected_export = f"export const {component_name}"
    if expected_export not in fixed_code:
        # Try to find what was actually exported
        actual_match = re.search(r'export\s+const\s+(\w+)', fixed_code)
        if actual_match and actual_match.group(1) != component_name:
            actual_name = actual_match.group(1)
            fixes.append(f"Warning: Component name mismatch - expected '{component_name}', found '{actual_name}'")
    
    return fixed_code, fixed_props, fixes


@register_tool
class CodegenTool(LLMTool[CodegenContext, CodegenPatch]):
    """Generates React components for InventComponent placeholders.
    
    Takes invented component specs and generates TypeScript/React code.
    """
    
    # Self-description
    name: ClassVar[str] = "codegen"
    description: ClassVar[str] = "Generate React/TypeScript code for invented components found in slide MDX."
    query_description: ClassVar[str] = "Runs after content step if any <InventComponent> tags exist in slides."
    args_description: ClassVar[List[str]] = [
        "component_ids (specific components to generate, empty = all)",
    ]
    requires: ClassVar[List[str]] = ["content"]
    produces: ClassVar[List[str]] = ["generated_components"]
    examples: ClassVar[List[str]] = [
        '{"id": "codegen", "type": "codegen", "params": {}, "depends_on": ["content"]}',
    ]
    
    system_prompt: ClassVar[str] = """Role: Expert UI Engineering & Design System Implementer
You are a React/TypeScript component generator specialized in Generative UI. Your goal is to translate abstract design intents into pixel-perfect, professional-grade React components that look like they were built by a top-tier design team.

# INPUT SCHEMA
You will receive an <InventComponent> definition containing:
- data: Raw content.
- visual_logic: Composition and animation instructions.
- theme_mapping: Color and spacing intent.
- notes: Specific functional requirements.

# STYLE DICTIONARY (THE "CONSTITUTION")
To ensure consistency with predefined components, you MUST use these standard tokens via Tailwind CSS:

- Spacing: Use p-6 or p-8 for containers. Gap between items should be gap-4 or gap-6.
- Radius: Large containers use rounded-2xl or rounded-3xl.
- Typography:
    - Value/Big Numbers: text-4xl font-bold tracking-tight.
    - Labels: text-sm font-medium uppercase tracking-wider text-slate-500.
- Shadows: Use shadow-xl shadow-slate-200/50 for cards.
- Borders: Use border border-slate-100.

# VISUAL LOGIC INTERPRETATION
Composition:
- radial: Use absolute positioning with sin/cos or CSS conic-gradient.
- split-comparison: Use grid-cols-2 with a center divider.
- hierarchical-tree: Use Flexbox with SVG lines for connectors.

Metaphor Handling:
- If the intent involves "Waves" or "Surfing," use framer-motion for fluid, organic path animations.

# THEME-AWARE COLORS
- Primary: text-blue-600 / bg-blue-500
- Success: text-emerald-600 / bg-emerald-500
- Warning: text-amber-600 / bg-amber-500
- Use theme_mapping to decide which color goes where.

# OUTPUT FORMAT
Return a JSON object with this structure:

{
  "components": [
    {
      "id": "component_id",
      "name": "ComponentName",
            "props_interface": "export interface ComponentNameProps { ... }",
            "code": "import React from 'react';\nimport { motion } from 'framer-motion';\nimport * as Lucide from 'lucide-react';\n\nexport const ComponentName: React.FC<ComponentNameProps> = ({ ... }) => { ... }"
    }
  ]
}

# RULES (STRICT)
1. No External Imports: Only use react, framer-motion, and lucide-react.
2. Accessibility: Add aria-label to interactive elements and icons.
3. Responsive: All components must be container-aware (use w-full h-full).
4. Empty States: If data is empty, return a graceful null or a minimal Skeleton loader.
5. Do NOT put the props interface in the code field; put it ONLY in props_interface.
6. Do NOT duplicate definitions between props_interface and code fields.

# CRITICAL: PROPS STRUCTURE
The MDX calls components using spread syntax: `<ComponentName {...{ key1: value1, key2: value2 }} />`
This means the data object keys become TOP-LEVEL props, NOT wrapped in a "data" prop.

WRONG (do NOT generate this):
```tsx
interface Props { data: { before: X; after: Y } }  // ❌ Wrapped in "data"
const Comp = ({ data }) => { ... data.before ... }
```

CORRECT (generate this instead):
```tsx
interface Props { before: X; after: Y; title?: string }  // ✅ Flat top-level props
const Comp = ({ before, after, title }) => { ... before ... }
```

Always destructure the data object keys directly as component props.

# COMPONENT RULES
1. Use TypeScript with proper typing
2. Use functional components with React.FC<PropsType>
3. Use Tailwind CSS for styling (assume it's available)
4. Keep components self-contained and reusable
5. Handle edge cases (empty data, missing props with defaults)
6. Use semantic HTML elements
7. Include basic accessibility attributes (aria-label, role, etc.)
8. Export the component as a named export
9. Props interface should DIRECTLY match the data={{...}} keys from the InventComponent (flat, not wrapped)

# STYLE GUIDELINES
- Use modern React patterns (hooks if needed)
- Prefer composition over complexity
- Keep rendering logic simple and readable
- Use consistent naming: PascalCase for components, camelCase for props
- Provide sensible default values for optional props

# EXAMPLE OUTPUT
Given an InventComponent with `data={{ before: {...}, after: {...} }}`:

{
  "components": [{
    "id": "comparison_01",
    "name": "BeforeAfterComparison",
    "props_interface": "export interface BeforeAfterComparisonProps {\\n  before: { focus: string; value: number };\\n  after: { focus: string; value: number };\\n  title?: string;\\n}",
    "code": "export const BeforeAfterComparison: React.FC<BeforeAfterComparisonProps> = ({ before, after, title = 'Comparison' }) => {\\n  if (!before || !after) return null;\\n  return (\\n    <div className=\\"p-6 rounded-2xl border border-slate-100\\">\\n      <h3>{title}</h3>\\n      <div className=\\"grid grid-cols-2 gap-4\\">\\n        <div>{before.focus}: {before.value}</div>\\n        <div>{after.focus}: {after.value}</div>\\n      </div>\\n    </div>\\n  );\\n};"
  }]
}
"""
    
    def slice(self, state: "PipelineState", params: Optional[Dict[str, Any]] = None) -> CodegenContext:
        print("Shiyi DEBUG: CodegenTool.slice called")
        """Extract invented components from content step MDX output."""
        params = params or {}
        
        # Read content MDX from trace file (preferred)
        content_mdx = _read_content_mdx_from_trace()
        invented = []
        
        if content_mdx:
            invented = _extract_invent_components_from_mdx(content_mdx)
            print(f"[codegen] Found {len(invented)} InventComponent(s) in content MDX")
        
        # Fallback: Check state.slides if trace missing or no components found
        if not invented and hasattr(state, "slides") and state.slides:
            print("[codegen] Checking state.slides for InventComponent...")
            for slide in state.slides:
                slide_id = slide.get("id", "unknown")
                # MDX content is in "mdx" field, not "content" (which is a dict with structured data)
                mdx_content = slide.get("mdx", "")
                if not isinstance(mdx_content, str):
                    continue
                
                # Regex to find <InventComponent ... />
                invent_pattern = r'<InventComponent\s+([\s\S]*?)(?:/>|>\s*</InventComponent>)'
                
                for match in re.finditer(invent_pattern, mdx_content):
                    attrs_str = match.group(1)
                    
                    # Extract id
                    id_match = re.search(r'id\s*=\s*["\']([^"\']+)["\']', attrs_str)
                    comp_id = id_match.group(1) if id_match else f"invented_{slide_id}_{len(invented)}"
                    
                    component = {
                        "slide_id": slide_id,
                        "id": comp_id,
                        "raw": match.group(0),
                    }
                    
                    # Extract name
                    name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', attrs_str)
                    if name_match:
                        component["name"] = name_match.group(1)

                    # Extract intent
                    intent_match = re.search(r'intent\s*=\s*["\']([^"\']+)["\']', attrs_str)
                    if intent_match:
                        component["intent"] = intent_match.group(1)
                        
                    # Extract data
                    data_match = re.search(r'data\s*=\s*\{\{([\s\S]*?)\}\}', attrs_str)
                    if data_match:
                        component["data"] = data_match.group(1).strip()

                    # Extract visual_logic
                    visual_logic_match = re.search(r'visual_logic\s*=\s*\{\{([\s\S]*?)\}\}', attrs_str)
                    if visual_logic_match:
                        component["visual_logic"] = visual_logic_match.group(1).strip()

                    # Extract theme_mapping
                    theme_mapping_match = re.search(r'theme_mapping\s*=\s*\{\{([\s\S]*?)\}\}', attrs_str)
                    if theme_mapping_match:
                        component["theme_mapping"] = theme_mapping_match.group(1).strip()
                        
                    invented.append(component)
            
            if invented:
                print(f"[codegen] Found {len(invented)} InventComponent(s) in state.slides")

        if not invented:
            print("[codegen] No invented components found in trace or slides")
            return CodegenContext(
                invented_components=[],
                existing_components=_get_existing_component_names(),
            )
        
        # Filter by specific IDs if provided
        component_ids = params.get("component_ids", [])
        if component_ids:
            invented = [c for c in invented if c.get("id") in component_ids]
        
        return CodegenContext(
            invented_components=invented,
            existing_components=_get_existing_component_names(),
        )
    
    def generate(
        self,
        constitution: "ConstitutionPatch",
        context: CodegenContext,
        user_instruction: str,
    ) -> CodegenPatch:
        """Generate React code for invented components - one LLM call per component."""
        if not context.invented_components:
            print("[codegen] No invented components found, skipping")
            return CodegenPatch(generated_components={})
        
        print(f"[codegen] Generating code for {len(context.invented_components)} components")
        
        import os
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
        
        generated = {}
        
        # Make one LLM call per component
        for i, comp in enumerate(context.invented_components, 1):
            comp_id = comp.get("id", f"component_{i}")
            print(f"[codegen] ({i}/{len(context.invented_components)}) Generating: {comp_id}")
            
            # Build component-specific user prompt
            user_prompt = self._build_single_component_prompt(comp, context.existing_components, user_instruction)
            
            try:
                response = call_llm(
                    system_prompt=self.system_prompt,
                    user_prompt=user_prompt,
                    deployment=deployment,
                    temperature=0.3,
                    max_tokens=4000,
                    response_format="json",
                )
                
                # Parse response
                data = json.loads(response)
                
                # Handle both single component and array format
                comp_data = data
                if "components" in data and isinstance(data["components"], list):
                    comp_data = data["components"][0] if data["components"] else {}
                
                if comp_data:
                    raw_code = comp_data.get("code", "")
                    raw_props = comp_data.get("props_interface", "")
                    comp_name = comp_data.get("name", comp_id)
                    
                    # Validate and fix common issues
                    fixed_code, fixed_props, fixes = _validate_and_fix_component_code(
                        raw_code, raw_props, comp_name
                    )
                    
                    if fixes:
                        print(f"[codegen] Fixes applied to {comp_name}:")
                        for fix in fixes:
                            print(f"[codegen]   - {fix}")
                    
                    generated[comp_id] = {
                        "name": comp_name,
                        "props_interface": fixed_props,
                        "code": fixed_code,
                    }
                    print(f"[codegen] Generated: {comp_name}")
                else:
                    print(f"[codegen] Warning: Empty response for {comp_id}")
                    
            except json.JSONDecodeError as e:
                print(f"[codegen] Failed to parse JSON for {comp_id}: {e}")
            except Exception as e:
                print(f"[codegen] Error generating {comp_id}: {e}")
        
        print(f"[codegen] Generated {len(generated)} components total")
        return CodegenPatch(generated_components=generated)
    
    def _build_single_component_prompt(
        self, 
        comp: Dict[str, Any], 
        existing_components: List[str],
        user_instruction: str
    ) -> str:
        """Build user prompt for a single component."""
        lines = [
            "Generate a React component for this specification:",
            "",
            f"## Component ID: {comp.get('id', 'unknown')}",
        ]
        
        if comp.get('name'):
            lines.append(f"## Target Component Name: {comp['name']}")

        lines.extend([
            f"- Intent: {comp.get('intent', 'N/A')}",
            "",
            "## InventComponent Input",
            "data:",
            comp.get('data', "{}"),
            "",
            "visual_logic:",
            comp.get('visual_logic', "{}"),
            "",
            "theme_mapping:",
            comp.get('theme_mapping', "{}"),
        ])
        
        if comp.get('notes'):
            lines.append(f"- Notes: {comp['notes']}")
        
        lines.append(f"- Slide context: {comp.get('slide_id', 'unknown')}")
        lines.append("")
        lines.append(f"Existing components for reference (don't duplicate): {', '.join(existing_components)}")
        
        if user_instruction:
            lines.append(f"\nAdditional guidance: {user_instruction}")
        
        lines.append("")
        
        if comp.get('name'):
            lines.append(f"CRITICAL: The component MUST be exported as named export '{comp['name']}'")
            
        lines.append("Return a JSON with: id, name, props_interface, code")
        
        return "\n".join(lines)
    
    def apply(self, state: "PipelineState", patch: CodegenPatch) -> None:
        """Store generated components in state."""
        if not hasattr(state, 'generated_components'):
            state.generated_components = {}
        
        state.generated_components.update(patch.generated_components)
        
        if self.verbose:
            for comp_id, comp_data in patch.generated_components.items():
                print(f"[codegen] Generated: {comp_data.get('name', comp_id)}")

    # === Abstract method implementations (required by LLMTool) ===
    # We override generate() directly, so these are not used but must be defined.
    
    def format_context(self, context: CodegenContext) -> str:
        """Format context for prompt. Not used - generate() is overridden."""
        return ""
    
    def call_llm(self, prompt: str) -> str:
        """Call LLM. Not used - generate() is overridden."""
        return ""
    
    def parse_response(self, response: str) -> CodegenPatch:
        """Parse response. Not used - generate() is overridden."""
        return CodegenPatch(generated_components={})
