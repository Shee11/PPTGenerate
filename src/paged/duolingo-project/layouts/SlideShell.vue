<script setup lang="ts">
/**
 * SlideShell - Duolingo-styled Base Wrapper Component
 * 
 * Features:
 * - Playful, gamified visual design inspired by Duolingo
 * - Chunky rounded corners, vibrant colors
 * - Bottom-shadow "stacked" card effect
 * - Clean white backgrounds with accent colors
 * 
 * Usage in layouts:
 * <SlideShell v-bind="$props">
 *   <YourLayoutContent />
 * </SlideShell>
 */
import { computed, provide } from 'vue'

const props = defineProps<{
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'playful' | 'expressive'
  background?: string
}>()

// Provide vibe to child components
provide('vibe', computed(() => props.vibe || 'playful'))
provide('theme', computed(() => props.theme || 'duolingo'))

// Duolingo Theme CSS variables
const themeVars = computed(() => {
  const baseTheme = {
    // Backgrounds
    '--theme-bg-base': '#ffffff',
    '--theme-bg-surface': '#F7F7F7',
    '--theme-bg-elevated': '#ffffff',
    '--theme-bg-card': '#ffffff',
    
    // Primary colors - Duolingo Green
    '--theme-primary': '#58CC02',
    '--theme-primary-dark': '#4CAD02',
    '--theme-primary-light': '#89E219',
    
    // Accent colors
    '--theme-accent': '#1CB0F6',
    '--theme-accent-dark': '#1899D6',
    
    // Semantic colors
    '--theme-success': '#58CC02',
    '--theme-warning': '#FF9600',
    '--theme-danger': '#FF4B4B',
    '--theme-info': '#1CB0F6',
    
    // Special Duolingo colors
    '--theme-streak': '#FF9600',
    '--theme-xp': '#1CB0F6',
    '--theme-premium': '#CE82FF',
    '--theme-golden': '#FFC800',
    
    // Text colors
    '--theme-text': '#3C3C3C',
    '--theme-text-muted': '#777777',
    '--theme-text-dim': '#AFAFAF',
    '--theme-text-inverse': '#ffffff',
    
    // Borders
    '--theme-border': '#E5E5E5',
    '--theme-border-subtle': '#F0F0F0',
    '--theme-border-strong': '#CDCDCD',
    
    // Typography
    '--font-body': "'Nunito', 'DIN Round', system-ui, sans-serif",
    '--font-heading': "'Nunito', 'DIN Round', system-ui, sans-serif",
    '--font-mono': "'JetBrains Mono', monospace",
    
    // Shadows - Duolingo's signature "stacked" shadow
    '--shadow-sm': '0 2px 0 #E5E5E5',
    '--shadow-md': '0 4px 0 #E5E5E5',
    '--shadow-lg': '0 6px 0 #E5E5E5',
    '--shadow-glow': '0 0 20px rgba(88, 204, 2, 0.3)',
    '--shadow-card': '0 2px 0 #E5E5E5',
    '--shadow-button': '0 4px 0 var(--theme-primary-dark)',
    
    // Border radius - Duolingo loves chunky rounded corners
    '--radius-sm': '12px',
    '--radius-md': '16px',
    '--radius-lg': '20px',
    '--radius-xl': '24px',
    '--radius-full': '9999px',
  }
  
  // Apply custom background if provided
  if (props.background) {
    return { ...baseTheme, '--theme-bg-base': props.background }
  }
  
  return baseTheme
})

// Compute vibe class
const vibeClass = computed(() => {
  const vibe = props.vibe || 'playful'
  return `vibe-${vibe}`
})
</script>

<template>
  <div 
    class="slide-shell duolingo-theme" 
    :class="vibeClass"
    :style="themeVars"
  >
    <!-- Decorative top bar with Duolingo green -->
    <div class="duo-accent-bar"></div>
    
    <!-- Header bar -->
    <header v-if="header" class="slide-header">
      <div class="header-badge">
        <span class="header-icon">📖</span>
        <span class="header-text">{{ header }}</span>
      </div>
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

/* Duolingo's signature green accent bar at top */
.duo-accent-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-primary-light));
}

/* Header styles - Duolingo badge style */
.slide-header {
  flex-shrink: 0;
  padding: 1rem 1.5rem;
  padding-top: 1.25rem; /* Account for accent bar */
  display: flex;
  align-items: center;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--theme-bg-surface);
  padding: 8px 16px;
  border-radius: var(--radius-full);
  border: 2px solid var(--theme-border);
  box-shadow: var(--shadow-sm);
}

.header-icon {
  font-size: 1rem;
}

.header-text {
  font-weight: 700;
  font-size: 0.875rem;
  color: var(--theme-text);
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
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--theme-bg-surface);
  border-top: 2px solid var(--theme-border);
}

.footer-text {
  font-weight: 600;
  font-size: 0.8rem;
  color: var(--theme-text-muted);
}

/* === VIBE MODIFIERS === */

/* Minimal: Simple, no frills */
.vibe-minimal .duo-accent-bar {
  height: 2px;
}

.vibe-minimal .slide-header,
.vibe-minimal .slide-footer {
  padding: 0.5rem 1rem;
}

.vibe-minimal .header-badge {
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 4px 8px;
}

/* Clean: Subtle but present */
.vibe-clean .duo-accent-bar {
  height: 3px;
}

.vibe-clean .slide-header {
  padding: 0.75rem 1.25rem;
}

/* Balanced: Standard look */
/* (uses base styles above) */

/* Playful: More Duolingo personality */
.vibe-playful .duo-accent-bar {
  height: 6px;
  background: linear-gradient(90deg, 
    var(--theme-primary), 
    var(--theme-accent), 
    var(--theme-warning),
    var(--theme-primary)
  );
}

.vibe-playful .header-badge {
  background: var(--theme-primary-light);
  background: linear-gradient(135deg, #E8FFE0, #DFFFCC);
  border-color: var(--theme-primary);
}

.vibe-playful .header-icon {
  font-size: 1.25rem;
}

/* Expressive: Maximum Duolingo energy */
.vibe-expressive .duo-accent-bar {
  height: 8px;
  background: linear-gradient(90deg, 
    var(--theme-primary), 
    var(--theme-accent),
    var(--theme-premium),
    var(--theme-warning),
    var(--theme-primary)
  );
}

.vibe-expressive .slide-header {
  padding: 1.25rem 2rem;
  background: linear-gradient(180deg, var(--theme-bg-surface), transparent);
}

.vibe-expressive .header-badge {
  background: var(--theme-primary);
  color: white;
  border: none;
  box-shadow: 0 4px 0 var(--theme-primary-dark);
  padding: 10px 20px;
}

.vibe-expressive .header-text {
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.vibe-expressive .slide-footer {
  background: linear-gradient(0deg, var(--theme-bg-surface), transparent);
  padding: 1rem 2rem;
}
</style>
