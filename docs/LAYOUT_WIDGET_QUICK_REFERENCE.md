# Layout-Widget Quick Reference

## Widget → Layout Decision Tree

```
START: What widgets do you have?

├─ Quote widget (QuoteWidget or Type.Quote)?
│  └─ Use: full-bleed (best) | hero-split | center
│
├─ Table widget (TableWidget)?
│  └─ Use: full-bleed (best) | default
│
├─ Code widget (Type.Code)?
│  └─ Use: full-bleed (best) | two-cols
│
├─ 3-4 metrics (MetricWidget)?
│  └─ Use: smart-grid (best) | dashboard | feature-grid
│
├─ Timeline/steps (5-6 short points)?
│  └─ Use: timeline (best)
│
├─ Before/after comparison?
│  └─ Use: comparison (best) | two-cols
│
└─ Mixed content (short + long)?
   └─ Use: hero-split | two-cols-header
```

## Layout Constraints Quick Check

### ❌ NEVER Do This
| Widget       | DON'T Use Layout | Why                           |
|--------------|------------------|-------------------------------|
| QuoteWidget  | smart-grid       | Quotes need >600px width      |
| QuoteWidget  | timeline         | Steps are <300px wide         |
| TableWidget  | hero-split       | Tables need full width        |
| TableWidget  | smart-grid       | Columns too narrow for tables |
| Type.Code    | smart-grid       | Code needs wide display       |
| Type.List    | timeline         | Lists too long for steps      |

### ✅ ALWAYS Do This
| Widget Type   | Best Layout                     | Slot Width Needed |
|---------------|---------------------------------|-------------------|
| QuoteWidget   | full-bleed, hero-split, center  | wide (>600px)     |
| TableWidget   | full-bleed, default             | wide (>800px)     |
| MetricWidget  | smart-grid, dashboard           | narrow (200px)    |
| Type.Code     | full-bleed, two-cols            | wide (>700px)     |

## Pre-Submit Checklist

Before finalizing a slide, validate:

1. **Quote Check**:
   ```
   IF slide has QuoteWidget OR Type.Quote:
     THEN layout MUST BE: full-bleed | hero-split | center | default
     NEVER: smart-grid | timeline | feature-grid
   ```

2. **Grid Check**:
   ```
   IF layout == smart-grid:
     THEN ALL widgets MUST BE:
       - Type.Heading (short, 2-5 words)
       - Type.Body (brief, <150 chars)
       - MetricWidget
     NEVER: QuoteWidget | TableWidget | Type.Code | Type.List
   ```

3. **Table Check**:
   ```
   IF slide has TableWidget:
     THEN layout MUST BE: full-bleed | default
     NEVER: hero-split | smart-grid | timeline
   ```

4. **Timeline Check**:
   ```
   IF layout == timeline:
     THEN each step MUST have <100 chars
     NEVER: quotes, lists, or long paragraphs in steps
   ```

## Common Mistakes & Fixes

### Mistake 1: Quote in Grid
```json
// ❌ BAD
{
  "layout": "smart-grid",
  "widgets": {
    "col1": {"type": "Type.Heading", "text": "Problem"},
    "col2": {"type": "QuoteWidget", "text": "Long quote text..."}  // TOO LONG!
  }
}

// ✅ GOOD - Move quote to full-bleed
{
  "layout": "full-bleed",
  "widgets": {
    "default": {"type": "QuoteWidget", "text": "Long quote text..."}
  }
}
```

### Mistake 2: Table in Split
```json
// ❌ BAD
{
  "layout": "hero-split",
  "widgets": {
    "left": {"type": "Type.Body", "text": "Context"},
    "right": {"type": "TableWidget", "columns": [...]}  // CRAMPED!
  }
}

// ✅ GOOD - Use full-bleed for table
{
  "layout": "full-bleed",
  "widgets": {
    "default": {"type": "TableWidget", "columns": [...]}
  }
}
```

### Mistake 3: Long Text in Timeline Steps
```json
// ❌ BAD
{
  "layout": "timeline",
  "widgets": {
    "step1": {"type": "Type.Body", "text": "Very long explanation with multiple sentences that won't fit..."}
  }
}

// ✅ GOOD - Keep steps brief
{
  "layout": "timeline",
  "widgets": {
    "step1": {"type": "Type.Body", "text": "**Define problem** - user needs first"}
  }
}
```

## Width Reference
```
Layout Slot Widths (approximate):
┌─────────────────┬──────────────────┬──────────┐
│ Layout          │ Slot             │ Width    │
├─────────────────┼──────────────────┼──────────┤
│ full-bleed      │ default          │ ~1200px  │ ✅ Widest
│ default         │ default          │ ~900px   │
│ hero-split      │ left/right       │ ~450px   │
│ two-cols        │ left/right       │ ~450px   │
│ smart-grid      │ col1-4 (4 cols)  │ ~200px   │ ⚠️ Narrowest
│ timeline        │ step1-6          │ ~250px   │
└─────────────────┴──────────────────┴──────────┘

Widget Width Needs:
Quote: >600px → Use full-bleed, hero-split, center
Table: >800px → Use full-bleed, default
Code:  >700px → Use full-bleed, two-cols
List:  >400px → Use default, two-cols, hero-split
Metric: ~200px → Use smart-grid, dashboard ✅ Perfect fit!
```
