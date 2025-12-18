# Slidev Layout Engine

The Slidev layout engine transforms slide content into Slidev-compatible markdown, which is then built into an interactive Vue-based presentation using the Slidev framework.

## Overview

Slidev is a modern presentation framework that uses Markdown + Vue components. When using `--layout-engine slidev`, your slides are:

1. Converted to Slidev markdown with frontmatter and slots
2. Built into a Vue SPA using Vite
3. Output as a self-contained web application with assets

## Available Layouts

### Slidev Built-in Layouts

These are native Slidev layouts with pre-designed styling and slot configurations:

#### **cover**
Full-screen title slide with centered content. Perfect for opening slides.
- **Slots**: Default content area
- **Use case**: Title slide, section opener
- **Example**:
  ```yaml
  layout: cover
  ```

#### **intro**  
Introduction slide with author/presenter info
- **Slots**: Default content area
- **Use case**: Speaker introduction, agenda overview

#### **default**
Standard content slide with title and body
- **Slots**: Default content area  
- **Use case**: General content, bullet points, paragraphs

#### **center**
Centered content on slide
- **Slots**: Default centered area
- **Use case**: Single quote, key message, centered list

#### **two-cols**
Two-column layout with left and right sections
- **Slots**: `::left::` and `::right::`
- **Use case**: Comparisons, side-by-side content, before/after
- **Example**:
  ```markdown
  ---
  layout: two-cols
  ---
  
  ::left::
  ## Left Column
  Content here
  
  ::right::
  ## Right Column  
  Content here
  ```

#### **two-cols-header**
Two columns with shared header
- **Slots**: `::header::`, `::left::`, `::right::`
- **Use case**: Comparison with common title

#### **quote**
Large quotation display
- **Slots**: Default for quote text
- **Use case**: Pull quotes, testimonials, key statements

#### **statement**
Bold statement or key message
- **Slots**: Default for statement
- **Use case**: Key takeaway, thesis statement

#### **fact**
Single fact or number highlight
- **Slots**: Default for fact/number
- **Use case**: Statistics, key metrics, data points

#### **section**
Section divider slide
- **Slots**: Default for section title
- **Use case**: Chapter breaks, topic transitions

#### **image**
Full-image slide
- **Props**: `image` URL
- **Use case**: Photo showcase, visual break

#### **image-left**
Image on left, content on right
- **Slots**: `::left::` (image), `::right::` (content)
- **Use case**: Product showcase, visual + text

#### **image-right**
Image on right, content on left  
- **Slots**: `::left::` (content), `::right::` (image)
- **Use case**: Reverse image-left

#### **end**
Closing/thank you slide
- **Slots**: Default for closing message
- **Use case**: Final slide, contact info, Q&A

### Custom Layout Mappings

Our system layouts map to Slidev layouts for compatibility:

| Custom Layout | Maps to Slidev | Best for |
|--------------|----------------|----------|
| `Swiss.SplitTypo` | `two-cols` | Typography-heavy comparisons |
| `Swiss.Asymmetry` | `two-cols` | Unbalanced column layouts |
| `Swiss.Poster` | `cover` | Bold title slides |
| `Cinematic.Split_50_50` | `two-cols` | Equal split content |
| `Cinematic.Split_30_70` | `two-cols` | Asymmetric emphasis |
| `Cinematic.FullBleed` | `cover` | Full-screen hero images |
| `Bento.Standard` | `default` | Standard grid content |
| `Bento.HeroLeft` | `image-left` | Hero image + content |
| `Bento.HeroTop` | `cover` | Hero at top |
| `Comparison.TwoColumn` | `two-cols` | Side-by-side comparison |
| `Comparison.SideBySide` | `two-cols-header` | Comparison with header |
| `Matrix.Grid` | `default` | Grid-based layouts |

## Widget Types

Slidev supports standard markdown widgets that render beautifully:

### Typography Widgets

- **Type.Display**: Large title text → `# Heading`
- **Type.Heading**: Section heading → `## Heading`  
- **Type.Subhead**: Subsection → `### Subheading`
- **Type.Body**: Paragraph → Plain text
- **Type.Caption**: Small text → `*Caption text*`
- **Type.List**: Bullet list → `- Item`
- **Type.Quote**: Blockquote → `> Quote text`
- **Type.Code**: Code block → ` ```language\ncode\n``` `

### Data Widgets

Currently mapped to markdown equivalents:

- **Data.BigNum**: Rendered as heading with number
- **Data.Metric**: Rendered as formatted text
- **Data.Table**: Rendered as markdown table
- **Data.Chart**: Rendered as description (charts need Vue components)

## Themes

Slidev supports theming through:

1. **Built-in themes**: `default`, `seriph`, `apple-basic`, etc.
2. **Custom themes**: Via npm packages
3. **CSS variables**: Color customization

### Available Themes

```yaml
# In global frontmatter
theme: default  # Clean, modern default
theme: seriph   # Elegant serif theme  
theme: apple-basic  # Apple-style minimal
```

### Theme Configuration

The global frontmatter configures theme and styling:

```yaml
---
theme: default
background: https://source.unsplash.com/collection/94734566/1920x1080
highlighter: shiki
lineNumbers: true
fonts:
  sans: 'Avenir Next'
  serif: 'Georgia'
  mono: 'Fira Code'
colorSchema: auto  # auto, light, or dark
transition: slide-left  # fade-out, slide-left, slide-up, etc.
---
```

## Usage Examples

### Example 1: Title + Content Slides

```markdown
---
layout: cover
---

# My Presentation Title

Subtitle or tagline here

---
layout: default
---

## Introduction

- Point one
- Point two  
- Point three
```

### Example 2: Comparison Layout

```markdown
---
layout: two-cols
---

::left::
## Before

- Manual processes
- Slow iteration
- High cost

::right::
## After

- Automated workflows
- Fast deployment
- Cost effective
```

### Example 3: Quote Highlight

```markdown
---
layout: quote
---

"The best way to predict the future is to invent it."

— Alan Kay
```

### Example 4: Section Divider

```markdown
---
layout: section
background: '#2563eb'
---

# Part 2: Implementation
```

## Best Practices for LLM Generation

When generating Slidev slides:

1. **Use appropriate layouts**: Match layout to content structure
   - Comparisons → `two-cols` or `two-cols-header`
   - Quotes → `quote`
   - Key stats → `fact` or `statement`
   - Sections → `section` or `cover`

2. **Leverage markdown features**:
   - Use `==highlight==` for emphasis
   - Use `**bold**` for important terms
   - Use headers (`##`, `###`) for structure
   - Use code blocks with language syntax

3. **Structure content clearly**:
   - One main idea per slide
   - Use bullets for lists
   - Keep text concise
   - Use visual hierarchy (headers, emphasis)

4. **Vary layouts**: Don't use same layout for all slides
   - Start with `cover` or `intro`
   - Mix `default`, `two-cols`, `quote`
   - Use `section` for topic transitions
   - End with `end` layout

5. **Consider flow**:
   - Build narrative with layout progression
   - Use visual breaks (full-screen images, quotes)
   - Group related content with consistent layouts

## Output Format

Slidev presentations are output as:

1. **Markdown file** (`slides.md`): Source markdown with frontmatter
2. **Built SPA**: Complete Vue application in `dist/` folder
3. **Assets**: Bundled CSS, JS, fonts in `dist/assets/`

To view: Serve the `dist/` folder via HTTP server (Slidev uses ES modules which require HTTP protocol)

```bash
# Serve the presentation
python -m http.server 8000 --directory dist/

# Open in browser
http://localhost:8000/
```

## Advanced Features

Slidev supports many advanced features that can be leveraged:

- **Code highlighting**: Syntax highlighting via Shiki
- **Animations**: Click-based reveal animations with `v-click`
- **Drawing**: Draw on slides in presenter mode
- **Recording**: Record presentation with audio
- **PDF Export**: Export to PDF via CLI
- **Presenter mode**: Speaker notes and preview
- **Remote control**: Control from mobile device

These features work automatically with the generated slides.

## Technical Details

### Build Process

1. **Markdown Generation**: Python renderer creates Slidev markdown
2. **Slidev Build**: `npx @slidev/cli build` compiles to Vue SPA  
3. **Asset Bundling**: Vite bundles all CSS/JS/fonts
4. **Output**: Self-contained `dist/` folder

### Dependencies

- **Node.js**: Required for Slidev CLI
- **@slidev/cli**: Slidev build tools
- **@slidev/theme-default**: Default theme
- **Vue 3**: Component framework
- **Vite**: Build tool

All dependencies are installed once in `slidev_build/` directory and reused for subsequent builds.

### Performance

- **First build**: ~90s (includes npm install)
- **Subsequent builds**: ~30s (reuses node_modules)
- **Output size**: ~2-5MB (depends on content and assets)

## Troubleshooting

### CORS Errors

**Problem**: `Access to script blocked by CORS policy`

**Solution**: Serve via HTTP server, not file:// protocol
```bash
python -m http.server 8000 --directory output/presentation_dist/
```

### Missing Styles

**Problem**: Plain text on white background

**Solution**: Ensure global frontmatter is present at top of slides.md:
```yaml
---
theme: default
# ... other config
---
```

### Build Fails

**Problem**: `npx: command not found` or build timeout

**Solution**: 
1. Install Node.js (v16+)
2. Ensure npx is in PATH
3. Check `slidev_build/` directory has node_modules

### Unknown Layout Warning

**Problem**: "Unknown layout: X"  

**Solution**: Use only Slidev built-in layouts or mapped custom layouts from this documentation
