# Slidev Engine - Quick Reference

## Directory Structure

```
slidev-project/  ← EDIT HERE (source, version controlled)
  ├── layouts/      Custom Vue layout components
  ├── components/   Custom Vue widgets
  └── package.json  Dependencies

slidev_build/    ← DON'T EDIT (temporary, auto-generated)
  └── [recreated on each render]
```

## Key Difference

| Aspect | slidev-project/ | slidev_build/ |
|--------|----------------|---------------|
| **Purpose** | Source of truth | Build workspace |
| **Lifespan** | Permanent | Temporary |
| **Git** | Committed | Gitignored |
| **Edit** | ✅ Yes | ❌ Never |
| **Contains** | Vue source files | Vue + generated slides.md |
| **Usage** | Development | Build process only |

## Workflow

```
1. Edit: slidev-project/layouts/my-layout.vue
         ↓
2. Document: src/layout/slidev/layout_engine.py
         ↓
3. Render: uce_render --layout-engine slidev
         ↓
4. Build: slidev-project/ → slidev_build/ → dist/
```

## Adding a Layout

1. **Create**: `slidev-project/layouts/my-layout.vue`
2. **Document**: Add to `get_layout_documentation()` with design characteristics
3. **Test**: Run uce_render and check if LLM discovers it

## Adding a Widget

1. **Create**: `slidev-project/components/MyWidget.vue`
2. **Document**: Add to widget documentation section
3. **Map**: Add case in `_widget_to_vue_component()` in markdown_renderer.py

## Visual Design → Layout Matching

LLM uses abstract terms in storyline:
- `hierarchical` → layouts with clear top-down structure
- `split` → two-panel layouts (hero-split, comparison)
- `grid` → multi-item layouts (smart-grid, feature-grid)
- `timeline` → sequential layouts
- `full-canvas` → immersive single-element layouts

No hardcoded mapping - LLM reads documentation and chooses best match.

## Debug Files

After rendering, check `output/`:
- `debug_phase1_storyline.json` - Draft slides with visual_design
- `debug_phase2_patches.json` - Layout selections
- `debug_phase3_final.json` - Final active slides

## Common Commands

```bash
# Clear cache and generate fresh
Remove-Item -Recurse .uce_cache -Force
python -m cli.uce_render --source data/context/career_talk.txt \
  --layout-engine slidev --output output/test.html

# Test Slidev directly
cd slidev-project
npm run dev  # Dev server
npm run build  # Production build

# Check documentation
python -c "from src.layout.engine_registry import LayoutEngineRegistry; \
  LayoutEngineRegistry.set_active_engine('slidev'); \
  print(LayoutEngineRegistry.get_active_engine().get_layout_documentation())"
```

## File Locations

- **Layout documentation**: `src/layout/slidev/layout_engine.py`
- **Markdown renderer**: `src/render/slidev/markdown_renderer.py`
- **Widget components**: `slidev-project/components/`
- **Layout components**: `slidev-project/layouts/`
- **Full guide**: `docs/SLIDEV_DEVELOPMENT_GUIDE.md`
