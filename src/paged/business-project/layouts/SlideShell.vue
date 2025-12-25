<script setup lang="ts">
/**
 * SlideShell - Base wrapper component for Business Project layouts
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
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'decorative' | 'expressive'
  background?: string
}>()

// Provide vibe to child components
provide('vibe', computed(() => props.vibe || 'balanced'))
provide('theme', computed(() => props.theme || 'business_professional'))

// Theme presets - Business-focused themes
const themePresets: Record<string, Record<string, string>> = {
  // Business Professional - Navy blue corporate theme
  'business_professional': {
    '--theme-bg-base': '#FAFBFC',
    '--theme-bg-surface': '#FFFFFF',
    '--theme-bg-elevated': '#F5F7F9',
    '--theme-primary': '#0F4C81',
    '--theme-accent': '#E67E22',
    '--theme-text': '#1A202C',
    '--theme-text-muted': '#4A5568',
    '--theme-text-dim': '#718096',
    '--theme-success': '#27AE60',
    '--theme-warning': '#F39C12',
    '--theme-danger': '#E74C3C',
    '--theme-border': '#E1E5E9',
    '--theme-border-subtle': '#EDF2F7',
    '--font-body': "'Inter', 'Segoe UI', system-ui, sans-serif",
    '--font-heading': "'Inter', 'Segoe UI', system-ui, sans-serif",
    '--font-mono': "'JetBrains Mono', 'Consolas', monospace",
    '--shadow-sm': '0 1px 3px rgba(0,0,0,0.08)',
    '--shadow-md': '0 4px 12px rgba(0,0,0,0.1)',
    '--shadow-lg': '0 8px 24px rgba(0,0,0,0.12)',
    '--shadow-glow': '0 0 20px rgba(15,76,129,0.15)',
    '--radius-sm': '4px',
    '--radius-md': '8px',
    '--radius-lg': '12px',
    '--radius-xl': '16px',
  },
  // Executive Dark - Dark mode for executive presentations
  'executive_dark': {
    '--theme-bg-base': '#0D1117',
    '--theme-bg-surface': '#161B22',
    '--theme-bg-elevated': '#21262D',
    '--theme-primary': '#58A6FF',
    '--theme-accent': '#F78166',
    '--theme-text': '#F0F6FC',
    '--theme-text-muted': '#C9D1D9',
    '--theme-text-dim': '#8B949E',
    '--theme-success': '#3FB950',
    '--theme-warning': '#D29922',
    '--theme-danger': '#F85149',
    '--theme-border': '#30363D',
    '--theme-border-subtle': '#21262D',
    '--font-body': "'Inter', 'Segoe UI', system-ui, sans-serif",
    '--font-heading': "'Inter', 'Segoe UI', system-ui, sans-serif",
    '--font-mono': "'JetBrains Mono', 'Consolas', monospace",
    '--shadow-sm': '0 1px 3px rgba(0,0,0,0.3)',
    '--shadow-md': '0 4px 12px rgba(0,0,0,0.4)',
    '--shadow-lg': '0 8px 24px rgba(0,0,0,0.5)',
    '--shadow-glow': '0 0 20px rgba(88,166,255,0.2)',
    '--radius-sm': '4px',
    '--radius-md': '8px',
    '--radius-lg': '12px',
    '--radius-xl': '16px',
  },
  // Consulting - Clean consulting firm style
  'consulting': {
    '--theme-bg-base': '#FFFFFF',
    '--theme-bg-surface': '#F7F9FC',
    '--theme-bg-elevated': '#EEF2F7',
    '--theme-primary': '#003366',
    '--theme-accent': '#0066CC',
    '--theme-text': '#1A1A2E',
    '--theme-text-muted': '#4A4A6A',
    '--theme-text-dim': '#7A7A8A',
    '--theme-success': '#00875A',
    '--theme-warning': '#FF8B00',
    '--theme-danger': '#DE350B',
    '--theme-border': '#DFE1E6',
    '--theme-border-subtle': '#EBECF0',
    '--font-body': "'Inter', 'Helvetica Neue', Arial, sans-serif",
    '--font-heading': "'Inter', 'Helvetica Neue', Arial, sans-serif",
    '--font-mono': "'SF Mono', 'Monaco', monospace",
    '--shadow-sm': '0 1px 2px rgba(0,0,0,0.06)',
    '--shadow-md': '0 4px 8px rgba(0,0,0,0.08)',
    '--shadow-lg': '0 8px 16px rgba(0,0,0,0.1)',
    '--shadow-glow': '0 0 16px rgba(0,51,102,0.1)',
    '--radius-sm': '3px',
    '--radius-md': '6px',
    '--radius-lg': '10px',
    '--radius-xl': '14px',
  },
  // Finance - Traditional finance/banking style
  'finance': {
    '--theme-bg-base': '#F8F9FA',
    '--theme-bg-surface': '#FFFFFF',
    '--theme-bg-elevated': '#F1F3F5',
    '--theme-primary': '#0A3D62',
    '--theme-accent': '#38A169',
    '--theme-text': '#212529',
    '--theme-text-muted': '#495057',
    '--theme-text-dim': '#6C757D',
    '--theme-success': '#28A745',
    '--theme-warning': '#FFC107',
    '--theme-danger': '#DC3545',
    '--theme-border': '#DEE2E6',
    '--theme-border-subtle': '#E9ECEF',
    '--font-body': "'Georgia', 'Times New Roman', serif",
    '--font-heading': "'Inter', 'Helvetica Neue', sans-serif",
    '--font-mono': "'Courier New', monospace",
    '--shadow-sm': '0 1px 2px rgba(0,0,0,0.05)',
    '--shadow-md': '0 3px 8px rgba(0,0,0,0.08)',
    '--shadow-lg': '0 6px 16px rgba(0,0,0,0.1)',
    '--shadow-glow': '0 0 12px rgba(10,61,98,0.1)',
    '--radius-sm': '2px',
    '--radius-md': '4px',
    '--radius-lg': '8px',
    '--radius-xl': '12px',
  },
  // Tech Startup - Modern tech startup style
  'tech_startup': {
    '--theme-bg-base': '#FAFAFA',
    '--theme-bg-surface': '#FFFFFF',
    '--theme-bg-elevated': '#F4F4F5',
    '--theme-primary': '#6366F1',
    '--theme-accent': '#EC4899',
    '--theme-text': '#18181B',
    '--theme-text-muted': '#3F3F46',
    '--theme-text-dim': '#71717A',
    '--theme-success': '#22C55E',
    '--theme-warning': '#EAB308',
    '--theme-danger': '#EF4444',
    '--theme-border': '#E4E4E7',
    '--theme-border-subtle': '#F4F4F5',
    '--font-body': "'Inter', system-ui, sans-serif",
    '--font-heading': "'Inter', system-ui, sans-serif",
    '--font-mono': "'JetBrains Mono', 'Fira Code', monospace",
    '--shadow-sm': '0 1px 2px rgba(0,0,0,0.05)',
    '--shadow-md': '0 4px 12px rgba(0,0,0,0.08)',
    '--shadow-lg': '0 8px 24px rgba(0,0,0,0.12)',
    '--shadow-glow': '0 0 24px rgba(99,102,241,0.2)',
    '--radius-sm': '6px',
    '--radius-md': '10px',
    '--radius-lg': '16px',
    '--radius-xl': '24px',
  },
}

// Compute current theme styles
const themeStyles = computed(() => {
  const themeName = props.theme || 'business_professional'
  const preset = themePresets[themeName] || themePresets['business_professional']
  return preset
})

// Vibe class for density control
const vibeClass = computed(() => `vibe-${props.vibe || 'balanced'}`)

// Background style
const bgStyle = computed(() => {
  if (props.background) {
    return { background: props.background }
  }
  return {}
})
</script>

<template>
  <div class="slide-shell business-layout" :class="vibeClass" :style="[themeStyles, bgStyle]">
    <!-- Header -->
    <div v-if="header" class="shell-header">
      <div class="header-content">{{ header }}</div>
      <div class="header-accent"></div>
    </div>
    
    <!-- Main content area -->
    <div class="shell-content" :class="{ 'has-header': header, 'has-footer': footer }">
      <slot />
    </div>
    
    <!-- Footer -->
    <div v-if="footer" class="shell-footer">
      <div class="footer-content">{{ footer }}</div>
    </div>
  </div>
</template>

<style scoped>
.slide-shell {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--theme-bg-base);
  color: var(--theme-text);
  font-family: var(--font-body);
  position: relative;
  overflow: hidden;
}

/* Header */
.shell-header {
  padding: 1rem 2rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--theme-text-muted);
  background: var(--theme-bg-surface);
  border-bottom: 1px solid var(--theme-border-subtle);
  flex-shrink: 0;
  position: relative;
}

.header-accent {
  position: absolute;
  bottom: 0;
  left: 2rem;
  right: 2rem;
  height: 2px;
  background: linear-gradient(90deg, var(--theme-primary), transparent);
}

/* Content */
.shell-content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.shell-content.has-header {
  padding-top: 0;
}

.shell-content.has-footer {
  padding-bottom: 0;
}

/* Footer */
.shell-footer {
  padding: 0.75rem 2rem;
  font-size: 0.75rem;
  color: var(--theme-text-dim);
  background: var(--theme-bg-surface);
  border-top: 1px solid var(--theme-border-subtle);
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* === VIBE: MINIMAL === */
.vibe-minimal .shell-header {
  padding: 0.75rem 1.5rem;
  background: transparent;
  border-bottom: none;
}

.vibe-minimal .header-accent {
  display: none;
}

.vibe-minimal .shell-footer {
  padding: 0.5rem 1.5rem;
  background: transparent;
  border-top: none;
}

/* === VIBE: CLEAN === */
.vibe-clean .shell-header {
  padding: 1rem 1.75rem;
}

.vibe-clean .shell-footer {
  padding: 0.75rem 1.75rem;
}

/* === VIBE: BALANCED (default) === */
/* Base styles above */

/* === VIBE: DECORATIVE === */
.vibe-decorative .shell-header {
  padding: 1.25rem 2.5rem;
  background: linear-gradient(
    180deg,
    var(--theme-bg-surface),
    var(--theme-bg-base)
  );
}

.vibe-decorative .header-accent {
  height: 3px;
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-accent), transparent);
}

.vibe-decorative .shell-footer {
  padding: 1rem 2.5rem;
  background: linear-gradient(
    0deg,
    var(--theme-bg-surface),
    var(--theme-bg-base)
  );
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive .shell-header {
  padding: 1.5rem 3rem;
  background: linear-gradient(
    135deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-primary) 5%, var(--theme-bg-surface))
  );
}

.vibe-expressive .header-accent {
  height: 4px;
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-accent));
  border-radius: 2px;
}

.vibe-expressive .shell-footer {
  padding: 1.25rem 3rem;
}
</style>
