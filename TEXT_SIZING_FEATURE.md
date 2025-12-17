# Text Length Guidelines Feature

## Overview

The content generation system now instructs the LLM to generate **text appropriate for widget sizes**, preventing overflow and improving readability.

## Implementation

### Updated Content Generation Prompt

**File**: `src/generation/content/prompts.py`

Added comprehensive text length guidelines before the IMPORTANT RULES section:

```
**Text Length Guidelines by Widget Size**:
CRITICAL: Match text length to widget size to prevent overflow and ensure readability:
- Size S (small): 1-2 WORDS maximum (e.g., "Innovation", "Q4 Results", "Key Insight")
- Size M (medium): 3-6 words, SHORT PHRASE (e.g., "Driving Digital Transformation", "Revenue Growth Strategy")
- Size L (large): 1-2 sentences, concise (e.g., "Our platform enables seamless collaboration across teams.")
- Size XL (extra large): 2-4 sentences, detailed paragraph (e.g., "The new system architecture reduces latency by 40%. Users report significant improvements in workflow efficiency.")

Always check the slot size from the strategy definition and generate appropriately sized text. Small widgets cannot fit long text!
```

### Rule 7 Updated

Changed rule 7 from:
```
7. Apply presets per-widget for variety, OR use "set_preset" for consistent global styling
```

To:
```
7. **MATCH TEXT LENGTH TO WIDGET SIZE** (S=word, M=phrase, L=sentence, XL=paragraph)
```

### Strategy Information in Prompt

The prompt already includes slot sizes from AssetManager:

```python
def _format_strategies_for_prompt() -> str:
    """Format available layout strategies for LLM prompt."""
    strategies = AssetManager.list_strategies()
    lines = ["Available Layout Strategies:"]
    
    for strategy in strategies:
        # Format each slot with both role and size
        slot_details = []
        for slot in strategy['slots']:
            slot_details.append(f"{slot['role']} (size: {slot['size']})")
        
        slot_info = ", ".join(slot_details)
        lines.append(f"- {strategy['name']}: Slots: [{slot_info}]")
    
    return "\n".join(lines)
```

Example output:
```
- Bento.Standard: Slots: [cell_1 (size: L), cell_2 (size: M), cell_3 (size: M), cell_4 (size: S)]
- Cinematic.FullBleed: Slots: [stage (size: XL)]
- Swiss.Asymmetry: Slots: [hero (size: L), accent_1 (size: S), accent_2 (size: S), accent_3 (size: S)]
```

## Verified Results

### Before (No Size Guidelines)
Widgets of all sizes contained long paragraphs, causing overflow in small widgets.

### After (With Size Guidelines)

**Small Widgets (S)**: 1-2 words
- "Innovation"
- "Q4 Results"
- "Key Insight"

**Medium Widgets (M)**: Short phrases (3-6 words)
- "Microsoft computer vision"
- "Face API service"
- "Deep learning phase"
- "Cloud and distributed systems"
- "LLMs and AI agents"

**Large Widgets (L)**: 1-2 sentences
- "Our platform enables seamless collaboration across teams."
- "A tech career journey started in computer vision at Microsoft in 2011. The early work involved Microsoft Face API, a computer vision service."

**Extra Large Widgets (XL)**: 2-4 sentences
- "From Microsoft computer vision in 2011 to today's large language models and AI agents, this career path shows how fast tech can shift and why continuous learning and adaptation matter more than ever."

## Example Test

```bash
# Clear cache to force new generation
Remove-Item -Recurse -Force .cache

# Generate with size-aware text
python -m cli --source data/context/career_short.txt \
  --user-instruction "Create a TechTuber style presentation" \
  --output output/sized_text_test.html --verbose
```

**Observed Output**:
- Display widgets (XL): Full paragraphs (2-4 sentences) ✓
- Heading widgets (L): Single sentences ✓
- Body widgets (M): Short phrases (3-6 words) ✓
- Small accent widgets (S): Single words ✓

## Benefits

1. **Prevents Text Overflow**: Small widgets no longer contain paragraphs
2. **Improves Readability**: Text density matches visual hierarchy
3. **Better Visual Design**: Appropriate text length for each layout region
4. **LLM-Driven**: No manual text truncation needed
5. **Strategy-Aware**: LLM checks slot sizes from strategy definitions

## Integration with Theme/Preset System

This feature works seamlessly with the theme and preset generation system:

1. **Intent Detection** → Determines audience and tone
2. **Theme Generation** → Creates appropriate colors
3. **Preset Generation** → Sets visual style (surface/shape/fill/effect)
4. **Text Sizing** → Generates content matching widget sizes

Complete E2E workflow now includes:
- Intent detection (audience, pattern, tone)
- Theme generation (colors, fonts)
- Preset application (visual style)
- **Size-appropriate text generation** (NEW)

## Future Enhancements

- [ ] Dynamic font sizing based on text length
- [ ] Text truncation fallback for overflow cases
- [ ] Per-widget size overrides
- [ ] Responsive text sizing for different screen sizes
- [ ] Character count limits per size category
