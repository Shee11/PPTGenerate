<!--
  FloatingBadge.vue - Floating Badge/Tag Component
  
  Eye-catching badge with floating animation and glow.
  Perfect for labels, tags, status indicators, or highlights.
  
  Props:
    - variant: Visual style (solid, outline, gradient, glow)
    - color: Badge color
    - size: Badge size (sm, md, lg)
    - floating: Enable floating animation
    - pulse: Enable pulse animation
-->
<template>
  <span 
    class="floating-badge"
    :class="[
      `variant-${variant}`,
      `size-${size}`,
      { floating, pulse }
    ]"
    :style="badgeStyles"
  >
    <span class="badge-glow"></span>
    <span class="badge-content">
      <slot />
    </span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  variant?: 'solid' | 'outline' | 'gradient' | 'glow'
  color?: string
  size?: 'sm' | 'md' | 'lg'
  floating?: boolean
  pulse?: boolean
}>(), {
  variant: 'solid',
  color: 'var(--c-primary)',
  size: 'md',
  floating: false,
  pulse: false
})

const badgeStyles = computed(() => ({
  '--badge-color': props.color
}))
</script>

<style scoped>
.floating-badge {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

/* Sizes */
.size-sm {
  padding: 0.25rem 0.625rem;
  font-size: 0.625rem;
  border-radius: 0.375rem;
}

.size-md {
  padding: 0.375rem 0.875rem;
  font-size: 0.75rem;
  border-radius: 0.5rem;
}

.size-lg {
  padding: 0.5rem 1.125rem;
  font-size: 0.875rem;
  border-radius: 0.625rem;
}

/* Glow effect */
.badge-glow {
  position: absolute;
  inset: -3px;
  background: var(--badge-color);
  opacity: 0;
  filter: blur(8px);
  border-radius: inherit;
  transition: opacity 0.3s ease;
}

.floating-badge:hover .badge-glow {
  opacity: 0.3;
}

/* Content */
.badge-content {
  position: relative;
  z-index: 1;
}

/* Variants */
.variant-solid {
  background: var(--badge-color);
  color: white;
}

.variant-outline {
  background: transparent;
  border: 1.5px solid var(--badge-color);
  color: var(--badge-color);
}

.variant-gradient {
  background: linear-gradient(135deg, var(--badge-color), var(--c-accent, #10b981));
  color: white;
}

.variant-glow {
  background: rgba(255, 255, 255, 0.1);
  color: var(--badge-color);
  box-shadow: 0 0 15px var(--badge-color);
}

.variant-glow .badge-glow {
  opacity: 0.15;
}

/* Animations */
.floating {
  animation: badge-float 3s ease-in-out infinite;
}

@keyframes badge-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.pulse {
  animation: badge-pulse 2s ease-in-out infinite;
}

@keyframes badge-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.02); }
}

.floating.pulse {
  animation: badge-float-pulse 3s ease-in-out infinite;
}

@keyframes badge-float-pulse {
  0%, 100% { transform: translateY(0) scale(1); opacity: 1; }
  50% { transform: translateY(-4px) scale(1.02); opacity: 0.9; }
}
</style>
