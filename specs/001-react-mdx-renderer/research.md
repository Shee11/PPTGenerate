# Research: React MDX Presentation Renderer

**Date**: 2025-12-25  
**Feature**: 001-react-mdx-renderer  
**Status**: Complete

## Research Questions

### 1. MDX 3.x Integration with Next.js 14+

**Decision**: Use `@mdx-js/react` v3 with `@next/mdx` for Next.js integration

**Rationale**:
- MDX 3.x offers better ESM support and smaller bundle size
- Next.js 14+ has first-class MDX support via `@next/mdx` plugin
- Allows custom component mapping via `MDXProvider`

**Alternatives Considered**:
- `mdx-bundler`: More flexible but adds complexity; rejected for YAGNI
- `next-mdx-remote`: Better for CMS use cases; overkill for static generation
- Raw React without MDX: Would require custom parser; rejected for complexity

**Configuration**:
```javascript
// next.config.mjs
import createMDX from '@next/mdx';

const withMDX = createMDX({
  extension: /\.mdx?$/,
  options: {
    remarkPlugins: [],
    rehypePlugins: [],
  },
});

export default withMDX({
  pageExtensions: ['js', 'jsx', 'ts', 'tsx', 'md', 'mdx'],
  output: 'export', // Static HTML export
});
```

---

### 2. Compound Components Pattern for React

**Decision**: Use React Context + named child components for compound pattern

**Rationale**:
- Enables semantic slot syntax: `<LayoutSplit.Left>...</LayoutSplit.Left>`
- Hides internal implementation from Agent output
- Well-established pattern (used by Radix, Headless UI, Reach UI)

**Alternatives Considered**:
- Render props: Exposes implementation details; rejected
- Children array inspection: Brittle and not type-safe; rejected
- Props-based slots: Would allow `leftContent={...}` but less semantic

**Implementation Pattern**:
```tsx
// LayoutSplit.tsx
import { createContext, useContext, ReactNode } from 'react';

interface LayoutSplitContextValue {
  ratio: string;
}

const LayoutSplitContext = createContext<LayoutSplitContextValue | null>(null);

interface LayoutSplitProps {
  ratio?: '1:1' | '2:1' | '1:2' | '3:1' | '1:3';
  children: ReactNode;
}

function LayoutSplit({ ratio = '1:1', children }: LayoutSplitProps) {
  const gridCols = {
    '1:1': 'grid-cols-2',
    '2:1': 'grid-cols-[2fr_1fr]',
    '1:2': 'grid-cols-[1fr_2fr]',
    '3:1': 'grid-cols-[3fr_1fr]',
    '1:3': 'grid-cols-[1fr_3fr]',
  }[ratio];

  return (
    <LayoutSplitContext.Provider value={{ ratio }}>
      <div className={`grid ${gridCols} h-full`}>
        {children}
      </div>
    </LayoutSplitContext.Provider>
  );
}

function Left({ children }: { children: ReactNode }) {
  return <div className="p-8 overflow-auto">{children}</div>;
}

function Right({ children }: { children: ReactNode }) {
  return <div className="p-8 overflow-auto">{children}</div>;
}

LayoutSplit.Left = Left;
LayoutSplit.Right = Right;

export { LayoutSplit };
```

---

### 3. Charting Library Selection

**Decision**: Use Recharts 2.x

**Rationale**:
- Built on React, integrates naturally with component architecture
- SVG-based, good for static export
- Tree-shakeable for bundle size optimization
- Simple declarative API matches our semantic approach

**Alternatives Considered**:
- **Chart.js + react-chartjs-2**: Canvas-based, harder to style with CSS variables; rejected
- **Victory**: Good but larger bundle size; rejected for MVP
- **Visx (Airbnb)**: Low-level, requires more code; rejected for simplicity
- **Nivo**: Feature-rich but larger bundle; potential Phase 3 upgrade

**Bundle Impact**:
- Full Recharts: ~150KB minified
- Tree-shaken (Bar + Line + Pie): ~80KB minified
- Acceptable for initial MVP, evaluate in Phase 3

**Usage Pattern**:
```tsx
// ChartBar.tsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface ChartBarProps {
  data: Array<{ label: string; value: number }>;
  title?: string;
  height?: 'sm' | 'md' | 'lg';
}

export function ChartBar({ data, title, height = 'md' }: ChartBarProps) {
  const heights = { sm: 200, md: 300, lg: 400 };
  
  return (
    <div>
      {title && <h3 className="text-lg font-semibold mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height={heights[height]}>
        <BarChart data={data}>
          <XAxis dataKey="label" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="var(--theme-primary)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
```

---

### 4. L0 Validation Approach

**Decision**: AST-based validation using MDX parser + custom rules

**Rationale**:
- Parse MDX to AST before rendering
- Check for forbidden elements (div, span) and attributes (className, style)
- Provide line numbers in error messages
- Fail fast before rendering

**Alternatives Considered**:
- Runtime validation (render and inspect): Too late, bad UX; rejected
- Regex-based: Unreliable with JSX syntax; rejected
- ESLint plugin: Good for dev-time but doesn't block invalid input; complementary

**Implementation Approach**:
```typescript
// validator.ts
import { compile } from '@mdx-js/mdx';
import { visit } from 'unist-util-visit';

const FORBIDDEN_ELEMENTS = ['div', 'span', 'section', 'article', 'aside'];
const FORBIDDEN_ATTRIBUTES = ['className', 'style', 'dangerouslySetInnerHTML'];

interface ValidationError {
  line: number;
  column: number;
  message: string;
  suggestion: string;
}

export async function validateMDX(mdxContent: string): Promise<ValidationError[]> {
  const errors: ValidationError[] = [];
  
  // Parse MDX to AST
  const tree = await compile(mdxContent, {
    outputFormat: 'function-body',
    development: true,
  });
  
  visit(tree, 'mdxJsxFlowElement', (node) => {
    // Check forbidden elements
    if (FORBIDDEN_ELEMENTS.includes(node.name)) {
      errors.push({
        line: node.position?.start.line || 0,
        column: node.position?.start.column || 0,
        message: `L0 violation: <${node.name}> is forbidden`,
        suggestion: suggestReplacement(node.name),
      });
    }
    
    // Check forbidden attributes
    node.attributes?.forEach((attr) => {
      if (FORBIDDEN_ATTRIBUTES.includes(attr.name)) {
        errors.push({
          line: node.position?.start.line || 0,
          column: node.position?.start.column || 0,
          message: `L0 violation: ${attr.name} attribute is forbidden`,
          suggestion: `Remove ${attr.name} and use semantic props like size, variant, or intent`,
        });
      }
    });
  });
  
  return errors;
}

function suggestReplacement(element: string): string {
  const suggestions: Record<string, string> = {
    div: 'Use a Layout component (LayoutSplit, LayoutGrid) or remove wrapper',
    span: 'Use Text component with variant prop',
    section: 'Use a Layout component',
    article: 'Content should be inside Layout slots',
  };
  return suggestions[element] || 'Use a semantic component from the component library';
}
```

---

### 5. Theme System Architecture

**Decision**: CSS Custom Properties with TypeScript theme definitions

**Rationale**:
- CSS variables enable runtime theme switching without re-render
- TypeScript ensures type safety for theme definitions
- Matches existing Slidev theme structure for parity
- Can be injected via `<style>` tag in SlideWrapper

**Alternatives Considered**:
- Tailwind theme config: Would require build-time switch; rejected
- styled-components ThemeProvider: Adds runtime overhead; rejected
- CSS-in-JS (Emotion): Good but overkill for static themes; rejected

**Theme Structure**:
```typescript
// themes/types.ts
export interface Theme {
  id: string;
  name: string;
  colors: {
    bgBase: string;
    bgSurface: string;
    bgElevated: string;
    primary: string;
    accent: string;
    success: string;
    warning: string;
    danger: string;
    text: string;
    textMuted: string;
    textDim: string;
    border: string;
    borderSubtle: string;
  };
  typography: {
    fontBody: string;
    fontHeading: string;
    fontMono: string;
  };
  effects: {
    shadowSm: string;
    shadowMd: string;
    shadowLg: string;
    shadowGlow: string;
    radiusSm: string;
    radiusMd: string;
    radiusLg: string;
    radiusXl: string;
  };
}

// themes/business.ts
export const businessTheme: Theme = {
  id: 'business',
  name: 'Business',
  colors: {
    bgBase: '#0f172a',
    bgSurface: '#1e293b',
    bgElevated: '#334155',
    primary: '#3b82f6',
    accent: '#8b5cf6',
    success: '#22c55e',
    warning: '#eab308',
    danger: '#ef4444',
    text: '#f8fafc',
    textMuted: '#94a3b8',
    textDim: '#64748b',
    border: '#334155',
    borderSubtle: '#1e293b',
  },
  typography: {
    fontBody: 'Inter, system-ui, sans-serif',
    fontHeading: 'Inter, system-ui, sans-serif',
    fontMono: 'JetBrains Mono, monospace',
  },
  effects: {
    shadowSm: '0 1px 2px rgba(0,0,0,0.3)',
    shadowMd: '0 4px 6px rgba(0,0,0,0.3)',
    shadowLg: '0 10px 15px rgba(0,0,0,0.3)',
    shadowGlow: '0 0 20px rgba(59,130,246,0.3)',
    radiusSm: '0.25rem',
    radiusMd: '0.5rem',
    radiusLg: '0.75rem',
    radiusXl: '1rem',
  },
};
```

---

### 6. Static Export Strategy

**Decision**: Use Next.js `output: 'export'` for fully static HTML

**Rationale**:
- Generates standalone HTML/CSS/JS that works without server
- All slides pre-rendered at build time
- Compatible with any static hosting (GitHub Pages, S3, etc.)

**Alternatives Considered**:
- SSR with hydration: Requires server; rejected per spec
- Client-side only: Would need runtime MDX compilation; rejected for performance
- Custom bundler (Vite): Would require significant infrastructure; rejected

**Export Configuration**:
```javascript
// next.config.mjs
export default {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true, // Required for static export
  },
  // Generate all slide pages at build time
  exportPathMap: async function () {
    // Will be populated by MDX files in pages/
    return {};
  },
};
```

---

### 7. Python MDX Generator Pattern

**Decision**: Extend existing SlidevRenderer pattern with Jinja2 templates

**Rationale**:
- Consistent with existing codebase architecture
- Jinja2 templates for MDX generation (like existing Markdown generation)
- Reuse widget type dispatching logic
- Easy integration with CLI

**Alternatives Considered**:
- Node.js generator: Would require separate process; rejected for simplicity
- Direct string building: Less maintainable; rejected
- JSON → React directly: Would bypass MDX intermediate; rejected per spec

**Generator Structure**:
```python
# mdx_renderer.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

class ReactMDXRenderer:
    """Renderer for transforming state.json to React MDX format."""
    
    COMPONENT_MAP = {
        "Type.Display": ("Heading", {"level": 1}),
        "Type.Heading": ("Heading", {}),
        "Type.Body": ("Text", {"variant": "default"}),
        "Type.Caption": ("Text", {"variant": "caption"}),
        "Type.List": ("SmartList", {}),
        "Type.Quote": ("QuoteBlock", {}),
        "Type.Image": ("ImageBlock", {}),
        "Type.Metric": ("MetricGroup", {}),
        "Type.Chart": ("ChartBar", {}),
    }
    
    LAYOUT_MAP = {
        "cover": "LayoutCover",
        "split": "LayoutSplit",
        "stacked": "LayoutGrid",
        "grid": "LayoutGrid",
        "full-bleed": "LayoutFullBleed",
        "timeline": "LayoutTimeline",
        "dashboard": "LayoutDashboard",
    }
    
    def render_slide(self, slide: dict) -> str:
        """Render a single slide to MDX format."""
        layout = self.LAYOUT_MAP.get(slide.get("layout", "cover"), "LayoutCover")
        widgets = slide.get("widgets", {})
        
        # Build MDX content
        mdx_parts = [f"<{layout}>"]
        
        for slot, widget in widgets.items():
            component, default_props = self.COMPONENT_MAP.get(
                widget["type"], ("Text", {})
            )
            props = {**default_props, **widget.get("parameters", {})}
            mdx_parts.append(self._render_component(component, props, slot))
        
        mdx_parts.append(f"</{layout}>")
        return "\n".join(mdx_parts)
```

---

## Summary of Decisions

| Area | Decision | Key Benefit |
|------|----------|-------------|
| MDX Integration | @mdx-js/react v3 + @next/mdx | First-class Next.js support |
| Compound Components | Context + named children | Semantic slot syntax |
| Charts | Recharts 2.x | React-native, SVG, tree-shakeable |
| L0 Validation | AST-based with mdx compiler | Accurate line numbers, fail fast |
| Theme System | CSS Custom Properties | Runtime switching, no re-render |
| Static Export | Next.js output: 'export' | Standalone HTML, no server |
| Python Generator | Jinja2 templates + SlidevRenderer pattern | Consistent with existing code |

---

## Open Questions (Resolved)

1. ~~How to handle MDX syntax errors?~~ → Use try-catch with helpful messages pointing to line
2. ~~How to share types between TS and Python?~~ → Manual sync; generate JSON schema as source of truth
3. ~~How to handle images in static export?~~ → Allow external URLs or base64 inline
