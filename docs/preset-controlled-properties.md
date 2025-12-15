# Preset-Controlled CSS Properties

This document lists all CSS properties that are controlled by widget presets. These properties should **NOT** be set via inline styles to avoid conflicts.

## Surface Presets (6 variants)

Controls visual depth and layering:

- `background` / `background-color`
- `border` / `border-width` / `border-style` / `border-color`
- `box-shadow`
- `backdrop-filter` (Glass only)

**Variants:**
- Flat: transparent background, no border, no shadow
- Elevated: semi-transparent background, elevated shadow
- Outline: transparent background, colored border
- Glass: glassmorphism with backdrop blur
- Sunken: dark background, inset shadow
- NeoBrutal: solid background, thick border, offset shadow

## Shape Presets (6 variants)

Controls border radius and corner styles:

- `border-radius`

**Variants:**
- Sharp: 0px
- Rounded: 12px
- Curve: 20px
- Pill: 9999px (fully rounded)
- Squircle: 20% (CSS percentage)
- Organic: asymmetric radius values

## Fill Presets (6 variants)

Controls background patterns and fills:

- `background` / `background-color` / `background-image`
- `background-size` / `background-blend-mode`
- `color` (text color to ensure contrast)
- `border` (for Subtle variant)

**Variants:**
- Solid_Brand: primary color background, white text
- Subtle: very subtle background, thin border
- Gradient_Linear: linear gradient background
- Gradient_Mesh: radial gradient mesh
- Pattern_Dot: dotted pattern background
- Noise: noise texture overlay

## Effect Presets (4 variants)

Controls visual treatments and filters:

- `filter`
- `box-shadow` (for Glow)
- `animation` (for Glitch)
- `position` / `::before` pseudo-element (for Tape, Noise)

**Variants:**
- Duotone: contrast and saturation filters
- Glitch: shake animation
- Glow: colored glow shadows
- Tape: washi tape decoration overlay

## Summary

**All preset-controlled properties:**
- `background`
- `background-color`
- `background-image`
- `background-size`
- `background-blend-mode`
- `border`
- `border-width`
- `border-style`
- `border-color`
- `border-radius`
- `box-shadow`
- `backdrop-filter`
- `color` (when fill preset is active)
- `filter`
- `animation`

**Properties safe for inline styles** (not controlled by presets):
- `width` / `height`
- `display` / `flex-direction` / `align-items` / `justify-content`
- `padding` / `margin`
- `font-size` / `font-weight` / `line-height` / `text-align`
- `vertical-align`
- `overflow` / `position` (on inner elements, not widget container)
- `z-index`
- `opacity` (if not overriding preset opacity)
