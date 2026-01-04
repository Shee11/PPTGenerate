<!--
  SlideShell.vue - Base wrapper for all layouts
  
  Provides:
  - Theme CSS variable application
  - Header/footer rendering
  - Consistent slide structure
-->
<template>
  <div class="slide-shell" :style="themeVars">
    <!-- Header -->
    <div v-if="header" class="slide-header">
      {{ header }}
    </div>
    
    <!-- Main content area -->
    <div class="slide-content">
      <slot />
    </div>
    
    <!-- Footer -->
    <div v-if="footer" class="slide-footer">
      {{ footer }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, provide } from 'vue'

const props = withDefaults(defineProps<{
  header?: string
  footer?: string
  theme?: string
}>(), {
  theme: 'default'
})

provide('theme', computed(() => props.theme))

// Theme presets
const themes: Record<string, Record<string, string>> = {
  default: {
    '--c-bg-base': '#0f172a',
    '--c-bg-surface': '#1e293b',
    '--c-bg-elevated': '#334155',
    '--c-primary': '#3b82f6',
    '--c-accent': '#8b5cf6',
    '--c-text': '#f8fafc',
    '--c-text-muted': '#cbd5e1',
    '--c-text-dim': '#94a3b8',
    '--c-border': '#334155',
    '--font-body': "'Inter', system-ui, sans-serif",
    '--font-heading': "'Inter', system-ui, sans-serif",
  },
  light: {
    '--c-bg-base': '#ffffff',
    '--c-bg-surface': '#f8fafc',
    '--c-bg-elevated': '#f1f5f9',
    '--c-primary': '#2563eb',
    '--c-accent': '#7c3aed',
    '--c-text': '#1e293b',
    '--c-text-muted': '#475569',
    '--c-text-dim': '#94a3b8',
    '--c-border': '#e2e8f0',
    '--font-body': "'Inter', system-ui, sans-serif",
    '--font-heading': "'Inter', system-ui, sans-serif",
  },
  dark: {
    '--c-bg-base': '#0a0a0a',
    '--c-bg-surface': '#171717',
    '--c-bg-elevated': '#262626',
    '--c-primary': '#22d3ee',
    '--c-accent': '#a78bfa',
    '--c-text': '#fafafa',
    '--c-text-muted': '#a1a1aa',
    '--c-text-dim': '#71717a',
    '--c-border': '#3f3f46',
    '--font-body': "'Inter', system-ui, sans-serif",
    '--font-heading': "'Inter', system-ui, sans-serif",
  },
}

const themeVars = computed(() => {
  return themes[props.theme] || themes.default
})
</script>

<style scoped>
.slide-shell {
  width: 100%;
  height: 100%;
  background: var(--c-bg-base);
  color: var(--c-text);
  font-family: var(--font-body);
  display: flex;
  flex-direction: column;
  padding: 48px 56px;
  box-sizing: border-box;
  overflow: hidden;
}

.slide-header {
  font-size: 0.875rem;
  color: var(--c-text-muted);
  padding-bottom: 16px;
  border-bottom: 1px solid var(--c-border);
  margin-bottom: 24px;
  flex-shrink: 0;
}

.slide-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.slide-footer {
  font-size: 0.75rem;
  color: var(--c-text-dim);
  padding-top: 16px;
  border-top: 1px solid var(--c-border);
  margin-top: 24px;
  flex-shrink: 0;
  text-align: center;
}
</style>
