<script setup lang="ts">
import { computed } from 'vue'

// Props from frontmatter
const props = defineProps<{
  theme?: 'business' | 'cyber'
}>()

// Theme CSS variable mappings
const themeVariables = computed(() => {
  const theme = props.theme || 'business'
  
  if (theme === 'business') {
    return {
      '--c-bg-base': '#ffffff',
      '--c-bg-surface': '#f8fafc',
      '--c-primary': '#2563eb',
      '--c-accent': '#3b82f6',
      '--c-text-main': '#0f172a',
      '--c-text-muted': '#64748b',
      '--font-family': 'Inter, sans-serif',
      '--shadow-theme': '0 1px 3px rgba(0, 0, 0, 0.1)',
      '--c-success': '#10b981',
      '--c-danger': '#ef4444',
      '--border-theme': '#e2e8f0',
    }
  } else if (theme === 'cyber') {
    return {
      '--c-bg-base': '#050505',
      '--c-bg-surface': '#0a0a0a',
      '--c-primary': '#00ffa3',
      '--c-accent': '#00ff6e',
      '--c-text-main': '#e2e8f0',
      '--c-text-muted': '#94a3b8',
      '--font-family': 'Orbitron, monospace',
      '--shadow-theme': '0 0 20px var(--c-primary)',
      '--c-success': '#00ff6e',
      '--c-danger': '#ff006e',
      '--border-theme': '#1e293b',
    }
  }
  
  return {}
})

// Apply grid pattern for cyber theme
const backgroundStyle = computed(() => {
  if (props.theme === 'cyber') {
    return {
      backgroundImage: `
        linear-gradient(rgba(0, 255, 163, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 163, 0.1) 1px, transparent 1px)
      `,
      backgroundSize: '50px 50px',
    }
  }
  return {}
})
</script>

<template>
  <div 
    class="slidev-slide-shell" 
    :style="{ ...themeVariables, ...backgroundStyle }"
  >
    <slot />
  </div>
</template>

<style scoped>
.slidev-slide-shell {
  width: 100%;
  height: 100%;
  background-color: var(--c-bg-base);
  color: var(--c-text-main);
  font-family: var(--font-family);
  padding: 2rem;
}
</style>
