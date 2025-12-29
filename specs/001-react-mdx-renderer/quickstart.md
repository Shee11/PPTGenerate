# Quickstart: React MDX Presentation Renderer

**Date**: 2025-12-25  
**Feature**: 001-react-mdx-renderer

This guide walks you through generating and viewing a presentation using the React MDX renderer.

## Prerequisites

- Node.js 18+
- Python 3.11+
- Git

## 1. Install Dependencies

### React Project
```powershell
cd src/paged/render/react
npm install
```

### Python CLI (if not already installed)
```powershell
pip install -e .
```

## 2. Create a State File

Create `my-presentation.json`:

```json
{
  "meta": {
    "id": "my-presentation",
    "version": "1.0"
  },
  "themes": {
    "business": {
      "id": "business",
      "primary_color": "#3b82f6",
      "background_color": "#0f172a",
      "text_color": "#f8fafc"
    }
  },
  "active_theme_id": "business",
  "project": "react-mdx",
  "slides": [
    {
      "id": "slide_01",
      "rank": 1,
      "layout": "cover",
      "widgets": {
        "title": {
          "type": "Type.Display",
          "parameters": { "text": "Welcome to My Presentation" }
        },
        "subtitle": {
          "type": "Type.Body",
          "parameters": { "text": "An introduction to React MDX slides" }
        }
      },
      "parameters": { "theme": "business", "vibe": "balanced" }
    },
    {
      "id": "slide_02",
      "rank": 2,
      "layout": "split",
      "widgets": {
        "title": {
          "type": "Type.Heading",
          "parameters": { "text": "Key Points", "level": 2 }
        },
        "left": {
          "type": "Type.List",
          "parameters": {
            "items": [
              "Semantic components only",
              "No HTML or CSS in MDX",
              "Theme-driven styling"
            ]
          }
        },
        "right": {
          "type": "Type.Chart",
          "parameters": {
            "chartType": "bar",
            "title": "Progress",
            "data": {
              "labels": ["Q1", "Q2", "Q3"],
              "values": [30, 60, 90]
            }
          }
        }
      },
      "parameters": { "theme": "business", "vibe": "balanced" }
    }
  ]
}
```

## 3. Generate MDX Files

```powershell
python -m cli.uce_render --render my-presentation.json --project react-mdx -o output/
```

This creates MDX files in `output/react-mdx/slides/`.

## 4. Build and Preview

### Development Mode
```powershell
cd src/paged/render/react
npm run dev
```

Open http://localhost:3000 in your browser.

### Production Build
```powershell
npm run build
npm run export
```

Output is in `out/` folder - these are static HTML files.

## 5. View the Presentation

- **Arrow keys**: Navigate between slides
- **Space**: Next slide
- **Escape**: Exit fullscreen

## Generated MDX Example

The CLI generates MDX like this:

```mdx
{/* slide_01.mdx */}
<LayoutCover>
  <Heading level={1}>Welcome to My Presentation</Heading>
  <Text>An introduction to React MDX slides</Text>
</LayoutCover>
```

```mdx
{/* slide_02.mdx */}
<LayoutSplit>
  <LayoutSplit.Left>
    <Heading level={2}>Key Points</Heading>
    <SmartList items={["Semantic components only", "No HTML or CSS in MDX", "Theme-driven styling"]} />
  </LayoutSplit.Left>
  <LayoutSplit.Right>
    <ChartBar 
      title="Progress"
      data={[
        { label: "Q1", value: 30 },
        { label: "Q2", value: 60 },
        { label: "Q3", value: 90 }
      ]}
    />
  </LayoutSplit.Right>
</LayoutSplit>
```

## Component Quick Reference

### Layouts (L1)
| Component | Purpose |
|-----------|---------|
| `<LayoutCover>` | Title slide |
| `<LayoutSplit>` | Two columns |
| `<LayoutGrid cols={3}>` | Multi-column |
| `<LayoutFullBleed>` | Full-screen image |
| `<LayoutTimeline>` | Step-by-step |
| `<LayoutDashboard>` | Metrics view |

### Blocks (L2)
| Component | Purpose |
|-----------|---------|
| `<ChartBar>` | Bar chart |
| `<ChartLine>` | Line chart |
| `<ChartPie>` | Pie chart |
| `<MetricGroup>` | KPI metrics |
| `<TableData>` | Data table |
| `<SmartList>` | Bullet list |
| `<QuoteBlock>` | Blockquote |
| `<ImageBlock>` | Image |
| `<CardGroup>` | Card grid |

### Atoms (L3)
| Component | Purpose |
|-----------|---------|
| `<Heading level={1}>` | H1-H6 headings |
| `<Text variant="lead">` | Paragraphs |
| `<Callout intent="info">` | Callout box |

## Themes

Available themes: `business`, `cyber`, `minimal`, `academic`, `creative`, `duolingo`, `dark`

Set theme in slide parameters:
```json
"parameters": { "theme": "cyber", "vibe": "expressive" }
```

## Vibes (Density Levels)

| Vibe | Style |
|------|-------|
| `minimal` | Tight, sparse |
| `clean` | Subtle, professional |
| `balanced` | Comfortable (default) |
| `decorative` | More visual flair |
| `expressive` | Bold, maximum impact |

## Troubleshooting

### "L0 violation" error
You're using forbidden HTML elements. Replace:
- `<div>` → Use a Layout component
- `<span>` → Use `<Text>`
- `className` → Remove, use `variant` or `intent` instead

### Build fails
1. Check Node.js version: `node --version` (should be 18+)
2. Delete `node_modules` and reinstall: `rm -rf node_modules ; npm install`

### Slides not rendering
1. Verify state.json is valid JSON
2. Check widget types match exactly (e.g., `Type.Display` not `type.display`)
3. Run with `--verbose` flag for detailed errors

## Next Steps

- See [data-model.md](data-model.md) for full entity definitions
- See [contracts/components.ts](contracts/components.ts) for all props
- See [research.md](research.md) for technical decisions
