<script setup lang="ts">
/**
 * SlideShell - Base wrapper component for all Slidev layouts
 * 
 * Provides:
 * - Consistent header/footer rendering
 * - Theme CSS variable application
 * - Vibe class propagation for layout density control
 * 
 * Usage in layouts:
 * <SlideShell v-bind="$props">
 *   <YourLayoutContent />
 * </SlideShell>
 */
import { computed, provide } from 'vue'

const props = defineProps<{
  // Header text (from frontmatter)
  header?: string
  // Footer text (from frontmatter)
  footer?: string
  // Theme preset name
  theme?: 'dark-professional' | 'light-minimal' | 'cyber-neon' | 'warm-corporate' | string
  // Vibe controls layout density/complexity
  vibe?: 'minimal' | 'clean' | 'balanced' | 'decorative' | 'expressive'
  // Background override (backwards compatibility)
  background?: string
}>()

// Provide vibe to child components
provide('vibe', computed(() => props.vibe || 'balanced'))
provide('theme', computed(() => props.theme || 'dark-professional'))

// Theme presets - CSS variables
const themePresets: Record<string, Record<string, string>> = {
  'dark-professional': {
    '--theme-bg-base': '#0f172a',
    '--theme-bg-surface': '#1e293b',
    '--theme-bg-elevated': '#334155',
    '--theme-primary': '#3b82f6',
    '--theme-accent': '#8b5cf6',
    '--theme-text': '#f8fafc',
    '--theme-text-muted': '#94a3b8',
    '--theme-text-dim': '#64748b',
    '--theme-success': '#10b981',
    '--theme-warning': '#f59e0b',
    '--theme-danger': '#ef4444',
    '--theme-border': '#334155',
    '--theme-border-subtle': '#1e293b',
    '--font-body': "'Inter', system-ui, sans-serif",
    '--font-heading': "'Inter', system-ui, sans-serif",
    '--font-mono': "'JetBrains Mono', 'Fira Code', monospace",
    '--shadow-sm': '0 1px 2px rgba(0,0,0,0.2)',
    '--shadow-md': '0 4px 12px rgba(0,0,0,0.3)',
    '--shadow-lg': '0 8px 24px rgba(0,0,0,0.4)',
    '--shadow-glow': '0 0 20px rgba(59,130,246,0.3)',
    '--radius-sm': '4px',
    '--radius-md': '8px',
    '--radius-lg': '16px',
    '--radius-xl': '24px',
  },
  'light-minimal': {
    '--theme-bg-base': '#ffffff',
    '--theme-bg-surface': '#f8fafc',
    '--theme-bg-elevated': '#f1f5f9',
    '--theme-primary': '#2563eb',
    '--theme-accent': '#7c3aed',
    '--theme-text': '#0f172a',
    '--theme-text-muted': '#475569',
    '--theme-text-dim': '#94a3b8',
    '--theme-success': '#059669',
    '--theme-warning': '#d97706',
    '--theme-danger': '#dc2626',
    '--theme-border': '#e2e8f0',
    '--theme-border-subtle': '#f1f5f9',
    '--font-body': "'Inter', system-ui, sans-serif",
    '--font-heading': "'Inter', system-ui, sans-serif",
    '--font-mono': "'JetBrains Mono', 'Fira Code', monospace",
    '--shadow-sm': '0 1px 2px rgba(0,0,0,0.05)',
    '--shadow-md': '0 4px 12px rgba(0,0,0,0.08)',
    '--shadow-lg': '0 8px 24px rgba(0,0,0,0.12)',
    '--shadow-glow': '0 0 20px rgba(37,99,235,0.15)',
    '--radius-sm': '4px',
    '--radius-md': '8px',
    '--radius-lg': '16px',
    '--radius-xl': '24px',
  },
  'cyber-neon': {
    '--theme-bg-base': '#050505',
    '--theme-bg-surface': '#0a0a0a',
    '--theme-bg-elevated': '#141414',
    '--theme-primary': '#00ffa3',
    '--theme-accent': '#ff00ff',
    '--theme-text': '#e2e8f0',
    '--theme-text-muted': '#94a3b8',
    '--theme-text-dim': '#64748b',
    '--theme-success': '#00ff6e',
    '--theme-warning': '#ffff00',
    '--theme-danger': '#ff006e',
    '--theme-border': '#1e293b',
    '--theme-border-subtle': '#0f172a',
    '--font-body': "'Orbitron', 'Inter', sans-serif",
    '--font-heading': "'Orbitron', 'Inter', sans-serif",
    '--font-mono': "'JetBrains Mono', monospace",
    '--shadow-sm': '0 0 4px rgba(0,255,163,0.3)',
    '--shadow-md': '0 0 12px rgba(0,255,163,0.4)',
    '--shadow-lg': '0 0 24px rgba(0,255,163,0.5)',
    '--shadow-glow': '0 0 30px rgba(0,255,163,0.6)',
    '--radius-sm': '2px',
    '--radius-md': '4px',
    '--radius-lg': '8px',
    '--radius-xl': '12px',
  },
  'warm-corporate': {
    '--theme-bg-base': '#fffbeb',
    '--theme-bg-surface': '#fef3c7',
    '--theme-bg-elevated': '#fde68a',
    '--theme-primary': '#d97706',
    '--theme-accent': '#ea580c',
    '--theme-text': '#1c1917',
    '--theme-text-muted': '#57534e',
    '--theme-text-dim': '#a8a29e',
    '--theme-success': '#16a34a',
    '--theme-warning': '#ca8a04',
    '--theme-danger': '#dc2626',
    '--theme-border': '#fde68a',
    '--theme-border-subtle': '#fef3c7',
    '--font-body': "'Georgia', 'Times New Roman', serif",
    '--font-heading': "'Georgia', 'Times New Roman', serif",
    '--font-mono': "'Courier New', monospace",
    '--shadow-sm': '0 1px 2px rgba(0,0,0,0.05)',
    '--shadow-md': '0 4px 12px rgba(0,0,0,0.08)',
    '--shadow-lg': '0 8px 24px rgba(0,0,0,0.1)',
    '--shadow-glow': '0 0 20px rgba(217,119,6,0.2)',
    '--radius-sm': '6px',
    '--radius-md': '12px',
    '--radius-lg': '20px',
    '--radius-xl': '32px',
  },
}

// Compute theme CSS variables
const themeVars = computed(() => {
  const themeName = props.theme || 'dark-professional'
  const preset = themePresets[themeName] || themePresets['dark-professional']
  
  // Allow background override
  if (props.background) {
    return { ...preset, '--theme-bg-base': props.background }
  }
  
  return preset
})

// Compute vibe class
const vibeClass = computed(() => {
  const vibe = props.vibe || 'balanced'
  return `vibe-${vibe}`
})

// Compute theme class for styling hooks
const themeClass = computed(() => {
  const theme = props.theme || 'dark-professional'
  // Normalize theme name to CSS-safe class
  return `theme-${theme.replace(/[^a-zA-Z0-9-]/g, '-')}`
})
</script>

<template>
  <div 
    class="slide-shell" 
    :class="[themeClass, vibeClass]"
    :style="themeVars"
  >
    <!-- Header bar -->
    <header v-if="header" class="slide-header">
      <span class="header-text">{{ header }}</span>
    </header>
    
    <!-- Main content area -->
    <main class="slide-content">
      <slot />
    </main>
    
    <!-- Footer bar -->
    <footer v-if="footer" class="slide-footer">
      <span class="footer-text">{{ footer }}</span>
    </footer>
  </div>
</template>

<style scoped>
.slide-shell {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--theme-bg-base);
  color: var(--theme-text);
  font-family: var(--font-body);
  position: relative;
  overflow: hidden;
}

/* Header styles */
.slide-header {
  flex-shrink: 0;
  padding: 0.5rem 1.5rem;
  font-size: 0.75rem;
  color: var(--theme-text-muted);
  border-bottom: 1px solid var(--theme-border-subtle);
  display: flex;
  align-items: center;
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--theme-bg-surface) 50%, transparent),
    transparent
  );
}

.header-text {
  opacity: 0.8;
  font-weight: 500;
  letter-spacing: 0.02em;
}

/* Content area */
.slide-content {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  position: relative;
}

/* Footer styles */
.slide-footer {
  flex-shrink: 0;
  padding: 0.5rem 1.5rem;
  font-size: 0.75rem;
  color: var(--theme-text-dim);
  border-top: 1px solid var(--theme-border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(
    0deg,
    color-mix(in srgb, var(--theme-bg-surface) 50%, transparent),
    transparent
  );
}

.footer-text {
  opacity: 0.6;
  font-style: italic;
}

/* === VIBE MODIFIERS === */

/* Minimal: Tight, no frills */
.vibe-minimal .slide-header,
.vibe-minimal .slide-footer {
  padding: 0.25rem 1rem;
  font-size: 0.65rem;
  border: none;
  background: none;
}

/* Clean: Subtle, professional */
.vibe-clean .slide-header,
.vibe-clean .slide-footer {
  padding: 0.375rem 1.25rem;
  font-size: 0.7rem;
}

/* Balanced: Default, comfortable */
/* (base styles above) */

/* Decorative: More presence */
.vibe-decorative .slide-header {
  padding: 0.75rem 2rem;
  font-size: 0.8rem;
  border-bottom-width: 2px;
  border-image: linear-gradient(90deg, transparent, var(--theme-primary), transparent) 1;
}

.vibe-decorative .slide-footer {
  padding: 0.75rem 2rem;
  font-size: 0.8rem;
  border-top-width: 2px;
  border-image: linear-gradient(90deg, transparent, var(--theme-primary), transparent) 1;
}

/* Expressive: Maximum impact */
.vibe-expressive .slide-header {
  padding: 1rem 2.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  background: linear-gradient(
    90deg,
    color-mix(in srgb, var(--theme-primary) 10%, var(--theme-bg-base)),
    var(--theme-bg-base),
    color-mix(in srgb, var(--theme-accent) 10%, var(--theme-bg-base))
  );
  border-bottom: 2px solid var(--theme-primary);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.vibe-expressive .slide-footer {
  padding: 1rem 2.5rem;
  font-size: 0.875rem;
  background: linear-gradient(
    90deg,
    color-mix(in srgb, var(--theme-accent) 10%, var(--theme-bg-base)),
    var(--theme-bg-base),
    color-mix(in srgb, var(--theme-primary) 10%, var(--theme-bg-base))
  );
  border-top: 2px solid var(--theme-accent);
  box-shadow: 0 -2px 8px rgba(0,0,0,0.1);
}

.vibe-expressive .header-text,
.vibe-expressive .footer-text {
  opacity: 1;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* === THEME-SPECIFIC ADJUSTMENTS === */

/* Cyber theme: Add scan line effect */
.theme-cyber-neon::after {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 255, 163, 0.02) 2px,
    rgba(0, 255, 163, 0.02) 4px
  );
  pointer-events: none;
  z-index: 100;
}

.theme-cyber-neon .slide-header,
.theme-cyber-neon .slide-footer {
  text-shadow: 0 0 10px var(--theme-primary);
}
</style>
