<!--
  GlassPanel.vue - Frosted Glass Effect Panel Component
  
  Modern glassmorphism panel with blur and transparency effects.
  Ideal for overlays, floating content, or modern UI elements.
  
  Props:
    - blur: Blur intensity (sm, md, lg)
    - opacity: Background opacity (0-1)
    - borderOpacity: Border opacity (0-1)
    - rounded: Border radius (sm, md, lg, xl)
    - padding: Inner padding (sm, md, lg)
    - glow: Enable subtle glow effect
    - glowColor: Color for glow effect
-->
<template>
  <div 
    class="glass-panel"
    :class="[
      `blur-${blur}`,
      `rounded-${rounded}`,
      `padding-${padding}`,
      { 'has-glow': glow }
    ]"
    :style="panelStyles"
  >
    <div class="glass-glow" v-if="glow"></div>
    <div class="glass-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  blur?: 'sm' | 'md' | 'lg'
  opacity?: number
  borderOpacity?: number
  rounded?: 'sm' | 'md' | 'lg' | 'xl'
  padding?: 'sm' | 'md' | 'lg'
  glow?: boolean
  glowColor?: string
}>(), {
  blur: 'md',
  opacity: 0.1,
  borderOpacity: 0.2,
  rounded: 'lg',
  padding: 'md',
  glow: false,
  glowColor: 'var(--c-primary)'
})

const panelStyles = computed(() => ({
  '--glass-opacity': props.opacity,
  '--border-opacity': props.borderOpacity,
  '--glow-color': props.glowColor
}))
</script>

<style scoped>
.glass-panel {
  position: relative;
  background: rgba(255, 255, 255, var(--glass-opacity, 0.1));
  border: 1px solid rgba(255, 255, 255, var(--border-opacity, 0.2));
  transition: all 0.3s ease;
}

/* Blur levels */
.blur-sm { backdrop-filter: blur(8px); }
.blur-md { backdrop-filter: blur(16px); }
.blur-lg { backdrop-filter: blur(24px); }

/* Rounded corners */
.rounded-sm { border-radius: 0.5rem; }
.rounded-md { border-radius: 0.75rem; }
.rounded-lg { border-radius: 1rem; }
.rounded-xl { border-radius: 1.5rem; }

/* Padding */
.padding-sm { padding: 1rem; }
.padding-md { padding: 1.5rem; }
.padding-lg { padding: 2rem; }

/* Glow effect */
.glass-glow {
  position: absolute;
  inset: -2px;
  background: var(--glow-color);
  opacity: 0;
  filter: blur(20px);
  border-radius: inherit;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.has-glow:hover .glass-glow {
  opacity: 0.15;
}

/* Content */
.glass-content {
  position: relative;
  z-index: 1;
}

.glass-content :deep(h1),
.glass-content :deep(h2),
.glass-content :deep(h3) {
  color: var(--c-text-main);
  margin: 0 0 0.75rem;
}

.glass-content :deep(p) {
  color: var(--c-text-muted);
  margin: 0;
  line-height: 1.6;
}

/* Hover effect */
.glass-panel:hover {
  background: rgba(255, 255, 255, calc(var(--glass-opacity, 0.1) + 0.03));
  border-color: rgba(255, 255, 255, calc(var(--border-opacity, 0.2) + 0.1));
}
</style>
