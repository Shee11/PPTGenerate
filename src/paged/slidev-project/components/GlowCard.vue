<!--
  GlowCard.vue - Glowing Card Component with Hover Effects
  
  A versatile card with customizable glow effects, perfect for
  highlighting features, services, or important content blocks.
  
  Props:
    - glowColor: Color of the glow effect (default: primary)
    - variant: Card style (default, gradient, glass, neon)
    - hoverScale: Scale on hover (1.0-1.1)
    - rounded: Border radius size (sm, md, lg, full)
-->
<template>
  <div 
    class="glow-card"
    :class="[`variant-${variant}`, `rounded-${rounded}`]"
    :style="cardStyles"
  >
    <div class="glow-effect" :style="glowStyles"></div>
    <div class="card-border"></div>
    <div class="card-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  glowColor?: string
  variant?: 'default' | 'gradient' | 'glass' | 'neon'
  hoverScale?: number
  rounded?: 'sm' | 'md' | 'lg' | 'full'
}>(), {
  glowColor: 'var(--c-primary)',
  variant: 'default',
  hoverScale: 1.02,
  rounded: 'md'
})

const cardStyles = computed(() => ({
  '--hover-scale': props.hoverScale,
  '--glow-color': props.glowColor
}))

const glowStyles = computed(() => ({
  background: `radial-gradient(ellipse at center, ${props.glowColor}, transparent 70%)`
}))
</script>

<style scoped>
.glow-card {
  position: relative;
  background: var(--c-bg-surface);
  padding: 1.5rem;
  transition: all 0.3s ease;
  overflow: hidden;
}

.glow-card:hover {
  transform: scale(var(--hover-scale));
}

/* Glow effect */
.glow-effect {
  position: absolute;
  inset: -50%;
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
  filter: blur(40px);
}

.glow-card:hover .glow-effect {
  opacity: 0.15;
}

/* Border effect */
.card-border {
  position: absolute;
  inset: 0;
  border: 1px solid transparent;
  border-radius: inherit;
  transition: border-color 0.3s ease;
  pointer-events: none;
}

.glow-card:hover .card-border {
  border-color: var(--glow-color);
  opacity: 0.5;
}

/* Content */
.card-content {
  position: relative;
  z-index: 1;
}

.card-content :deep(h3) {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--c-text-main);
  margin: 0 0 0.75rem;
}

.card-content :deep(p) {
  color: var(--c-text-muted);
  margin: 0;
  line-height: 1.6;
}

/* Rounded variants */
.rounded-sm { border-radius: 0.375rem; }
.rounded-md { border-radius: 0.75rem; }
.rounded-lg { border-radius: 1.25rem; }
.rounded-full { border-radius: 2rem; }

/* Style variants */
.variant-gradient {
  background: linear-gradient(135deg, var(--c-bg-surface), rgba(255,255,255,0.02));
}

.variant-glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.variant-glass .card-border {
  display: none;
}

.variant-neon {
  background: transparent;
  border: 1px solid var(--glow-color);
}

.variant-neon .glow-effect {
  opacity: 0.1;
}

.variant-neon:hover .glow-effect {
  opacity: 0.25;
}

.variant-neon .card-border {
  display: none;
}
</style>
