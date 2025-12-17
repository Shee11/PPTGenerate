# Neutral Tone & Visual Abstraction Feature

## Overview

The content generation system now produces **presentation-ready content** with neutral, fact-based tone and visual abstraction appropriate for slides.

## Key Changes

### 1. Neutral Declarative Tone

**Before** (Quotation/Reported Speech):
- ❌ "The speaker mentioned that AI has transformed the industry"
- ❌ "They talked about how Face API works"
- ❌ "According to the presentation, deep learning changed everything"

**After** (Neutral Facts):
- ✅ "AI has transformed the industry"
- ✅ "Face API turns raw pixels into usable data"
- ✅ "Deep learning changed everything"

**Implementation**: Added explicit instructions in content generation prompt:
```
**Content Writing Style - CRITICAL**:
1. **Neutral, fact-based tone**: Write as declarative statements, NOT as quotations from the source
   - Present information as established facts, not reported speech
```

### 2. Visual Abstraction

**Before** (Document-style):
- ❌ Long detailed paragraphs explaining everything
- ❌ Complete sentences with all context
- ❌ Comprehensive coverage of topics

**After** (Presentation-style):
- ✅ "Traditional ML" (2 words for small widget)
- ✅ "Deep learning" (essence only)
- ✅ "Domain: computer vision and perception models" (distilled fact)

**Implementation**: Added designer mindset to prompt:
```
2. **Visual abstraction**: Think like a designer - slides are NOT documents
   - Extract the ESSENCE, not the details
   - Use impactful words and phrases that work visually
   - Favor clarity and memorability over completeness
```

### 3. Layout Family Content Guidance

Each layout family now has specific content style recommendations:

**Bento Family**: Grid-based layouts
- Best for: data comparisons, feature highlights, multi-topic summaries
- Content style: Parallel structure, concise

**Cinematic Family**: Full-bleed dramatic layouts
- Best for: hero statements, key messages, emotional moments
- Content style: Bold and declarative

**Swiss Family**: Typography-focused minimalist
- Best for: quotes, philosophical statements, core principles
- Content style: Distilled to essential truth

**Data Family**: Metric-driven layouts
- Best for: statistics, performance metrics, quantitative insights
- Content style: Numeric facts with brief labels

**Edit Family**: Magazine-style artistic
- Best for: creative storytelling, visual narratives
- Content style: Evocative and layered

**Focus Family**: Single-point emphasis
- Best for: key takeaways, central concepts, primary messages
- Content style: The ONE thing that matters

## Updated Rules Priority

The IMPORTANT RULES section now prioritizes neutral tone and abstraction:

```
5. **WRITE IN NEUTRAL DECLARATIVE TONE** - never use quotations or "speaker said" constructions
6. **ABSTRACT TO PRESENTATION LEVEL** - extract visual essentials, not full details
...
10. **MATCH CONTENT TO LAYOUT FAMILY** - use family descriptions to guide content style
```

## Code Changes

### File: `src/generation/content/prompts.py`

**Function `_format_strategies_for_prompt()`**:
- Added `family_descriptions` dictionary with content guidance for each layout family
- Groups strategies by family and includes family-level content descriptions
- Output now includes contextual guidance like:
  ```
  Bento Family: Grid-based layouts with multiple content cells. Best for: data comparisons...
    - Bento.Standard: Slots: [cell_1 (size: S), cell_2 (size: S), ...]
    - Bento.HeroLeft: Slots: [hero (size: L), side_1 (size: S), ...]
  ```

**Function `_build_content_generation_system_prompt()`**:
- Changed role from "presentation content generator" to "visual presentation designer"
- Added comprehensive content writing style section with examples
- Emphasized neutral tone, visual abstraction, and presentation-appropriate content
- Updated rules to prioritize tone and abstraction requirements

## Verified Results

### Example Output (career_neutral_tone.html)

**✅ Neutral Tone Examples**:
- "From Face API to AI agents, this career tracks how each wave of AI reshapes how software is built"
- "Current work centers on large language models and AI agents"
- "The tech journey starts in 2011 at Microsoft in computer vision"

**✅ Visual Abstraction Examples**:
- Small widgets: "Traditional ML", "Deep learning"
- Medium widgets: "Today's chapter", "Rewind to 2011"
- Large widgets: Single focused sentence

**✅ No Reported Speech**:
- Searched for: "speaker", "mentioned", "said", "talked about", "described"
- **Result**: Zero matches ✓

## Testing

```bash
# Clear cache and regenerate
Remove-Item -Recurse -Force .cache

# Generate with neutral tone
python -m cli --source data/context/career_short.txt \
  --user-instruction "Create a TechTuber style presentation" \
  --output output/test_neutral.html --verbose

# Verify no reported speech
Select-String -Path output/test_neutral.html \
  -Pattern 'speaker|mentioned|said|talked about|described' -CaseSensitive:$false
# Should return: (no matches)
```

## Benefits

1. **Professional Quality**: Content reads like polished presentation slides, not source transcripts
2. **Visual Impact**: Abstracted content works better visually on slides
3. **Audience-Appropriate**: Neutral tone suitable for any professional setting
4. **Designer Mindset**: LLM thinks like a visual designer, not a transcriber
5. **Layout-Aware**: Content style matches layout purpose (data vs. dramatic vs. minimal)

## Integration with Existing Features

Works seamlessly with:
- ✅ Intent detection (audience, pattern, tone)
- ✅ Theme generation (contextual colors)
- ✅ Preset application (visual styling)
- ✅ Text sizing (S/M/L/XL matching)
- ✅ **Neutral tone** (NEW)
- ✅ **Visual abstraction** (NEW)
- ✅ **Layout-specific content guidance** (NEW)

## Complete Workflow

1. **Intent Detection** → Identifies TechTuber pattern, energetic tone, developer audience
2. **Atom Extraction** → Pulls key facts from source content
3. **State Transition** → Selects appropriate layout strategies (Cinematic for drama, Bento for data)
4. **Content Generation** → 
   - Writes in neutral declarative tone
   - Abstracts to visual essentials
   - Matches content to layout family
   - Sizes text to widget dimensions
5. **Theme/Preset** → Applies appropriate visual styling
6. **Rendering** → Produces polished presentation HTML

## Future Enhancements

- [ ] Per-family tone variation (Swiss = philosophical, Data = analytical)
- [ ] Industry-specific terminology abstraction
- [ ] Bullet point vs. sentence optimization per layout
- [ ] Dynamic abstraction level based on slide count
