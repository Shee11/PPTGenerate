<!--
  IconBox.vue - Styled Icon Container Component
  
  Elegant container for icons with multiple style variants.
  Use for feature icons, navigation items, or visual highlights.
  
  Props:
    - icon: Icon emoji or text
    - size: Box size (sm, md, lg, xl)
    - variant: Visual style (filled, outlined, gradient, glow)
    - color: Primary color
    - rounded: Border radius (sm, md, lg, full)
-->
<template>
  <div 
    class="icon-box"
    :class="[`size-${size}`, `variant-${variant}`, `rounded-${rounded}`]"
    :style="boxStyles"
  >
    <div class="icon-glow"></div>
    <div class="icon-content">
      <slot>
        <span class="icon-emoji">{{ icon }}</span>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  icon?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'filled' | 'outlined' | 'gradient' | 'glow'
  color?: string
  rounded?: 'sm' | 'md' | 'lg' | 'full'
}>(), {
  icon: '✨',
  size: 'md',
  variant: 'filled',
  color: 'var(--c-primary)',
  rounded: 'md'
})

const boxStyles = computed(() => ({
  '--icon-color': props.color
}))
</script>

<style scoped>
.icon-box {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

/* Sizes */
.size-sm {
  width: 40px;
  height: 40px;
  font-size: 1.25rem;
}

.size-md {
  width: 56px;
  height: 56px;
  font-size: 1.5rem;
}

.size-lg {
  width: 72px;
  height: 72px;
  font-size: 2rem;
}

.size-xl {
  width: 96px;
  height: 96px;
  font-size: 2.5rem;
}

/* Rounded */
.rounded-sm { border-radius: 0.375rem; }
.rounded-md { border-radius: 0.75rem; }
.rounded-lg { border-radius: 1rem; }
.rounded-full { border-radius: 50%; }

/* Glow effect */
.icon-glow {
  position: absolute;
  inset: -10%;
  background: var(--icon-color);
  opacity: 0;
  filter: blur(15px);
  transition: opacity 0.3s ease;
  border-radius: inherit;
}

.icon-box:hover .icon-glow {
  opacity: 0.2;
}

/* Content */
.icon-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-emoji {
  line-height: 1;
}

/* Variants */
.variant-filled {
  background: var(--icon-color);
}

.variant-filled .icon-content {
  color: white;
  filter: brightness(0) invert(1);
}

.variant-outlined {
  background: transparent;
  border: 2px solid var(--icon-color);
}

.variant-gradient {
  background: linear-gradient(135deg, var(--icon-color), var(--c-accent, var(--icon-color)));
}

.variant-gradient .icon-content {
  filter: brightness(0) invert(1);
}

.variant-glow {
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 20px var(--icon-color);
}

.variant-glow .icon-glow {
  opacity: 0.15;
}

.variant-glow:hover .icon-glow {
  opacity: 0.3;
}

/* Hover effects */
.icon-box:hover {
  transform: scale(1.05);
}

.variant-outlined:hover {
  background: var(--icon-color);
}

.variant-outlined:hover .icon-content {
  filter: brightness(0) invert(1);
}
</style>
