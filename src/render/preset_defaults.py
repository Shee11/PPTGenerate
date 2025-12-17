"""
Default preset token values extracted from presets.css.
These values are used as fallbacks when no custom preset config is provided.
"""

PRESET_DEFAULTS = {
    # Surface presets - Control visual depth and layering
    "surface": {
        "Flat": {
            "bg": "transparent",
            "border": "none",
            "shadow": "none",
        },
        "Elevated": {
            "bg": "var(--color-surface, rgba(255, 255, 255, 0.05))",
            "shadow": "0 4px 6px rgba(0, 0, 0, 0.3), 0 2px 4px rgba(0, 0, 0, 0.2)",
        },
        "Outline": {
            "bg": "transparent",
            "border": "2px solid var(--color-primary, #00ff9f)",
        },
        "Glass": {
            "bg": "rgba(255, 255, 255, 0.05)",
            "blur": "10px",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
        },
        "Sunken": {
            "bg": "rgba(0, 0, 0, 0.3)",
            "shadow": "inset 0 2px 4px rgba(0, 0, 0, 0.4), inset 0 0 0 1px rgba(0, 0, 0, 0.2)",
        },
        "NeoBrutal": {
            "bg": "var(--color-surface, #ffffff)",
            "border_width": "3px",
            "border_color": "currentColor",
            "shadow_offset": "6px",
            "shadow_color": "currentColor",
        },
    },
    
    # Shape presets - Control border radius and corner styles
    "shape": {
        "Sharp": {
            "radius": "0",
        },
        "Rounded": {
            "radius": "12px",
        },
        "Curve": {
            "radius": "20px",
        },
        "Pill": {
            "radius": "9999px",
        },
        "Squircle": {
            "radius": "20%",
        },
        "Organic": {
            "radius": "30% 70% 70% 30% / 30% 30% 70% 70%",
        },
    },
    
    # Fill presets - Control background patterns and fills
    "fill": {
        "Solid_Brand": {
            "bg": "var(--color-primary, #00ff9f)",
            "color": "#ffffff",
        },
        "Solid_Surface": {
            "bg": "var(--color-background, #ffffff)",
            "color": "var(--color-text, #000000)",
        },
        "Subtle": {
            "bg": "rgba(255, 255, 255, 0.03)",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "color": "var(--color-text, #e0e7ff)",
        },
        "Gradient_Linear": {
            "bg": "linear-gradient(135deg, var(--color-primary, #00ff9f) 0%, var(--color-secondary, #00d4ff) 100%)",
            "color": "#ffffff",
        },
        "Gradient_Mesh": {
            "bg": "radial-gradient(at 20% 30%, var(--color-primary, #00ff9f) 0%, transparent 50%), radial-gradient(at 80% 70%, var(--color-secondary, #00d4ff) 0%, transparent 50%), radial-gradient(at 50% 50%, var(--color-accent, #ff00ff) 0%, transparent 50%), rgba(10, 14, 39, 0.8)",
            "blend": "screen, screen, screen, normal",
            "color": "var(--color-text, #e0e7ff)",
        },
        "Pattern_Dot": {
            "image": "radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px)",
            "size": "20px 20px",
            "bg": "rgba(255, 255, 255, 0.02)",
            "color": "var(--color-text, #e0e7ff)",
        },
        "Noise": {
            "bg": "rgba(255, 255, 255, 0.03)",
            "texture": "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E\")",
            "opacity": "0.5",
            "color": "var(--color-text, #e0e7ff)",
        },
    },
    
    # Effect presets - Control visual treatments and filters
    "effect": {
        "Duotone": {
            "filter": "contrast(1.2) saturate(1.5)",
        },
        "Glitch": {
            "duration": "3s",
            "x": "-2px",
            "y": "1px",
        },
        "Glow": {
            "shadow": "0 0 20px var(--color-primary, #00ff9f), 0 0 40px var(--color-primary, #00ff9f), 0 0 60px var(--color-primary, #00ff9f)",
            "brightness": "1.2",
        },
        "Tape": {
            "top": "-12px",
            "rotation": "-2deg",
            "width": "80px",
            "height": "25px",
            "bg": "linear-gradient(135deg, rgba(255, 220, 100, 0.7) 0%, rgba(255, 235, 150, 0.6) 50%, rgba(255, 220, 100, 0.7) 100%)",
            "border": "1px solid rgba(255, 200, 50, 0.4)",
            "shadow": "0 2px 8px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.3)",
            "radius": "2px",
            "opacity": "0.85",
        },
    },
}


def generate_preset_css_variables(presets: dict = None) -> str:
    """
    Generate CSS variable declarations for preset tokens.
    
    Args:
        presets: Custom preset configuration (optional). If None, uses PRESET_DEFAULTS.
        
    Returns:
        CSS variable declarations as a string (without :root {} wrapper)
    """
    if presets is None:
        presets = PRESET_DEFAULTS
    
    css_vars = []
    
    # Surface presets
    for variant, tokens in presets.get("surface", {}).items():
        prefix = f"--preset-{variant.lower()}"
        for key, value in tokens.items():
            css_vars.append(f"    {prefix}-{key}: {value};")
    
    # Shape presets
    for variant, tokens in presets.get("shape", {}).items():
        prefix = f"--preset-{variant.lower()}"
        for key, value in tokens.items():
            css_vars.append(f"    {prefix}-{key}: {value};")
    
    # Fill presets
    for variant, tokens in presets.get("fill", {}).items():
        prefix = f"--preset-{variant.lower().replace('_', '-')}"
        for key, value in tokens.items():
            css_vars.append(f"    {prefix}-{key}: {value};")
    
    # Effect presets
    for variant, tokens in presets.get("effect", {}).items():
        prefix = f"--preset-{variant.lower()}"
        for key, value in tokens.items():
            css_vars.append(f"    {prefix}-{key}: {value};")
    
    return "\n".join(css_vars)


def generate_preset_css() -> str:
    """
    Generate complete preset CSS class rules using CSS variables.
    This eliminates the need for a static presets.css file.
    
    Returns:
        Complete CSS content with all preset classes
    """
    return """
/* ===== SURFACE PRESETS ===== */
.preset-surface-Flat {
    background: var(--preset-flat-bg, transparent) !important;
    border: var(--preset-flat-border, none) !important;
    box-shadow: var(--preset-flat-shadow, none) !important;
}

.preset-surface-Elevated {
    background: var(--preset-elevated-bg, var(--color-surface, rgba(255, 255, 255, 0.05))) !important;
    box-shadow: var(--preset-elevated-shadow, 0 4px 6px rgba(0, 0, 0, 0.3), 0 2px 4px rgba(0, 0, 0, 0.2)) !important;
}

.preset-surface-Outline {
    background: var(--preset-outline-bg, transparent) !important;
    border: var(--preset-outline-border, 2px solid var(--color-primary, #00ff9f)) !important;
}

.preset-surface-Glass {
    background: var(--preset-glass-bg, rgba(255, 255, 255, 0.05)) !important;
    backdrop-filter: blur(var(--preset-glass-blur, 10px)) !important;
    border: var(--preset-glass-border, 1px solid rgba(255, 255, 255, 0.1)) !important;
}

.preset-surface-Sunken {
    background: var(--preset-sunken-bg, rgba(0, 0, 0, 0.3)) !important;
    box-shadow: var(--preset-sunken-shadow, inset 0 2px 4px rgba(0, 0, 0, 0.4), inset 0 0 0 1px rgba(0, 0, 0, 0.2)) !important;
}

.preset-surface-NeoBrutal {
    background: var(--preset-neobrutal-bg, var(--color-surface, #ffffff)) !important;
    border: var(--preset-neobrutal-border_width, 3px) solid var(--preset-neobrutal-border_color, currentColor) !important;
    box-shadow: var(--preset-neobrutal-shadow_offset, 6px) var(--preset-neobrutal-shadow_offset, 6px) 0 var(--preset-neobrutal-shadow_color, currentColor) !important;
}

/* ===== SHAPE PRESETS ===== */
.preset-shape-Sharp {
    border-radius: var(--preset-sharp-radius, 0) !important;
}

.preset-shape-Rounded {
    border-radius: var(--preset-rounded-radius, 12px) !important;
}

.preset-shape-Curve {
    border-radius: var(--preset-curve-radius, 20px) !important;
}

.preset-shape-Pill {
    border-radius: var(--preset-pill-radius, 9999px) !important;
}

.preset-shape-Squircle {
    border-radius: var(--preset-squircle-radius, 20%) !important;
}

.preset-shape-Organic {
    border-radius: var(--preset-organic-radius, 30% 70% 70% 30% / 30% 30% 70% 70%) !important;
}

/* ===== FILL PRESETS ===== */
.preset-fill-Solid_Brand {
    background: var(--preset-solid-brand-bg, var(--color-primary, #00ff9f)) !important;
    color: var(--preset-solid-brand-color, #ffffff) !important;
}

.preset-fill-Solid_Surface {
    background: var(--preset-solid-surface-bg, var(--color-background, #ffffff)) !important;
    color: var(--preset-solid-surface-color, var(--color-text, #000000)) !important;
}

.preset-fill-Subtle {
    background: var(--preset-subtle-bg, rgba(255, 255, 255, 0.03)) !important;
    border: var(--preset-subtle-border, 1px solid rgba(255, 255, 255, 0.1)) !important;
    color: var(--preset-subtle-color, var(--color-text, #e0e7ff)) !important;
}

.preset-fill-Gradient_Linear {
    background: var(--preset-gradient-linear-bg, linear-gradient(135deg, var(--color-primary, #00ff9f) 0%, var(--color-secondary, #00d4ff) 100%)) !important;
    color: var(--preset-gradient-linear-color, #ffffff) !important;
}

.preset-fill-Gradient_Mesh {
    background: var(--preset-gradient-mesh-bg, radial-gradient(at 20% 30%, var(--color-primary, #00ff9f) 0%, transparent 50%), radial-gradient(at 80% 70%, var(--color-secondary, #00d4ff) 0%, transparent 50%), radial-gradient(at 50% 50%, var(--color-accent, #ff00ff) 0%, transparent 50%), rgba(10, 14, 39, 0.8)) !important;
    background-blend-mode: var(--preset-gradient-mesh-blend, screen, screen, screen, normal) !important;
    color: var(--preset-gradient-mesh-color, var(--color-text, #e0e7ff)) !important;
}

.preset-fill-Pattern_Dot {
    background-image: var(--preset-pattern-dot-image, radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px)) !important;
    background-size: var(--preset-pattern-dot-size, 20px 20px) !important;
    background-color: var(--preset-pattern-dot-bg, rgba(255, 255, 255, 0.02)) !important;
    color: var(--preset-pattern-dot-color, var(--color-text, #e0e7ff)) !important;
}

.preset-fill-Noise {
    background: var(--preset-noise-bg, rgba(255, 255, 255, 0.03)) !important;
    background-image: var(--preset-noise-texture, url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E")) !important;
    opacity: var(--preset-noise-opacity, 0.5) !important;
    color: var(--preset-noise-color, var(--color-text, #e0e7ff)) !important;
}

/* ===== EFFECT PRESETS ===== */
.preset-effect-Duotone {
    filter: var(--preset-duotone-filter, contrast(1.2) saturate(1.5)) !important;
}

.preset-effect-Glitch {
    animation: glitch var(--preset-glitch-duration, 3s) infinite !important;
}

@keyframes glitch {
    0%, 100% { transform: translate(0, 0); }
    33% { transform: translate(var(--preset-glitch-x, -2px), var(--preset-glitch-y, 1px)); }
    66% { transform: translate(calc(-1 * var(--preset-glitch-x, -2px)), calc(-1 * var(--preset-glitch-y, 1px))); }
}

.preset-effect-Glow {
    box-shadow: var(--preset-glow-shadow, 0 0 20px var(--color-primary, #00ff9f), 0 0 40px var(--color-primary, #00ff9f), 0 0 60px var(--color-primary, #00ff9f)) !important;
    filter: brightness(var(--preset-glow-brightness, 1.2)) !important;
}

.preset-effect-Tape {
    position: relative;
}

.preset-effect-Tape::before {
    content: '';
    position: absolute;
    top: var(--preset-tape-top, -12px);
    left: 50%;
    transform: translateX(-50%) rotate(var(--preset-tape-rotation, -2deg));
    width: var(--preset-tape-width, 80px);
    height: var(--preset-tape-height, 25px);
    background: var(--preset-tape-bg, linear-gradient(135deg, rgba(255, 220, 100, 0.7) 0%, rgba(255, 235, 150, 0.6) 50%, rgba(255, 220, 100, 0.7) 100%));
    border: var(--preset-tape-border, 1px solid rgba(255, 200, 50, 0.4));
    box-shadow: var(--preset-tape-shadow, 0 2px 8px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.3));
    border-radius: var(--preset-tape-radius, 2px);
    opacity: var(--preset-tape-opacity, 0.85);
    clip-path: polygon(
        0% 5%, 3% 0%, 6% 5%, 9% 0%, 12% 5%, 15% 0%, 18% 5%, 21% 0%, 24% 5%, 27% 0%,
        30% 5%, 33% 0%, 36% 5%, 39% 0%, 42% 5%, 45% 0%, 48% 5%, 51% 0%, 54% 5%, 57% 0%,
        60% 5%, 63% 0%, 66% 5%, 69% 0%, 72% 5%, 75% 0%, 78% 5%, 81% 0%, 84% 5%, 87% 0%,
        90% 5%, 93% 0%, 96% 5%, 100% 0%,
        100% 100%, 96% 95%, 93% 100%, 90% 95%, 87% 100%, 84% 95%, 81% 100%, 78% 95%,
        75% 100%, 72% 95%, 69% 100%, 66% 95%, 63% 100%, 60% 95%, 57% 100%, 54% 95%,
        51% 100%, 48% 95%, 45% 100%, 42% 95%, 39% 100%, 36% 95%, 33% 100%, 30% 95%,
        27% 100%, 24% 95%, 21% 100%, 18% 95%, 15% 100%, 12% 95%, 9% 100%, 6% 95%,
        3% 100%, 0% 95%
    );
}

/* Ensure effect presets can work together */
.preset-effect-Duotone,
.preset-effect-Glitch,
.preset-effect-Tape {
    position: relative;
}

/* Override text color for branded fills */
.preset-fill-Solid_Brand,
.preset-fill-Gradient_Linear {
    --text-color-override: var(--color-on-primary, #ffffff);
}
"""
