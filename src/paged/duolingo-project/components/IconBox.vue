<!--
  IconBox.vue - Duolingo Styled Icon Container Component
  
  Playful container for icons with chunky Duolingo styling.
  Use for feature icons, achievements, or visual highlights.
  
  Props:
    - icon: Icon emoji or text
    - size: Box size (sm, md, lg, xl)
    - variant: Visual style (filled, outlined, gradient, glow)
    - color: Color theme (green, blue, orange, purple)
    - rounded: Border radius (sm, md, lg, full)
-->
<template>
  <div 
    class="icon-box"
    :class="[`size-${size}`, `variant-${variant}`, `rounded-${rounded}`, `color-${color}`]"
  >
    <div class="icon-shadow"></div>
    <div class="icon-content">
      <slot>
        <span class="icon-emoji">{{ icon }}</span>
      </slot>
    </div>
    <div class="icon-shine"></div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{
  icon?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'filled' | 'outlined' | 'gradient' | 'glow'
  color?: 'green' | 'blue' | 'orange' | 'purple'
  rounded?: 'sm' | 'md' | 'lg' | 'full'
}>(), {
  icon: '⭐',
  size: 'md',
  variant: 'filled',
  color: 'green',
  rounded: 'lg'
})
</script>

<style scoped>
.icon-box {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  font-family: var(--duo-font, 'Nunito', sans-serif);
}

.icon-box:hover {
  transform: translateY(-2px) scale(1.05);
}

.icon-box:active {
  transform: translateY(1px) scale(0.98);
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
  font-size: 1.75rem;
}

.size-lg {
  width: 72px;
  height: 72px;
  font-size: 2.25rem;
}

.size-xl {
  width: 96px;
  height: 96px;
  font-size: 3rem;
}

/* Rounded */
.rounded-sm { border-radius: 8px; }
.rounded-md { border-radius: 12px; }
.rounded-lg { border-radius: 16px; }
.rounded-full { border-radius: 50%; }

/* Shadow (Duolingo bottom-shadow effect) */
.icon-shadow {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  transform: translateY(4px);
  z-index: -1;
}

/* Content */
.icon-content {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  border-radius: inherit;
  z-index: 1;
}

.icon-emoji {
  line-height: 1;
}

/* Shine effect */
.icon-shine {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  border-radius: inherit;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 100%);
  pointer-events: none;
}

/* Color variants */
.color-green .icon-shadow {
  background: var(--duo-green-dark, #46a302);
}

.color-green.variant-filled .icon-content {
  background: var(--duo-green, #58CC02);
  color: white;
}

.color-green.variant-outlined .icon-content {
  background: white;
  border: 3px solid var(--duo-green, #58CC02);
}

.color-green.variant-gradient .icon-content {
  background: linear-gradient(135deg, var(--duo-green, #58CC02) 0%, var(--duo-blue, #1CB0F6) 100%);
  color: white;
}

.color-blue .icon-shadow {
  background: var(--duo-blue-dark, #1899D6);
}

.color-blue.variant-filled .icon-content {
  background: var(--duo-blue, #1CB0F6);
  color: white;
}

.color-blue.variant-outlined .icon-content {
  background: white;
  border: 3px solid var(--duo-blue, #1CB0F6);
}

.color-blue.variant-gradient .icon-content {
  background: linear-gradient(135deg, var(--duo-blue, #1CB0F6) 0%, var(--duo-purple, #CE82FF) 100%);
  color: white;
}

.color-orange .icon-shadow {
  background: #E68600;
}

.color-orange.variant-filled .icon-content {
  background: var(--duo-orange, #FF9600);
  color: white;
}

.color-orange.variant-outlined .icon-content {
  background: white;
  border: 3px solid var(--duo-orange, #FF9600);
}

.color-orange.variant-gradient .icon-content {
  background: linear-gradient(135deg, var(--duo-orange, #FF9600) 0%, var(--duo-red, #FF4B4B) 100%);
  color: white;
}

.color-purple .icon-shadow {
  background: #B86EE6;
}

.color-purple.variant-filled .icon-content {
  background: var(--duo-purple, #CE82FF);
  color: white;
}

.color-purple.variant-outlined .icon-content {
  background: white;
  border: 3px solid var(--duo-purple, #CE82FF);
}

.color-purple.variant-gradient .icon-content {
  background: linear-gradient(135deg, var(--duo-purple, #CE82FF) 0%, var(--duo-blue, #1CB0F6) 100%);
  color: white;
}

/* Glow variant */
.variant-glow .icon-shadow {
  filter: blur(8px);
  opacity: 0.6;
  transform: translateY(0);
}

.variant-glow.color-green .icon-shadow {
  background: var(--duo-green, #58CC02);
}

.variant-glow.color-blue .icon-shadow {
  background: var(--duo-blue, #1CB0F6);
}

.variant-glow.color-orange .icon-shadow {
  background: var(--duo-orange, #FF9600);
}

.variant-glow.color-purple .icon-shadow {
  background: var(--duo-purple, #CE82FF);
}

.variant-glow .icon-content {
  background: white;
  border: 3px solid currentColor;
}

.variant-glow.color-green .icon-content {
  color: var(--duo-green, #58CC02);
  border-color: var(--duo-green, #58CC02);
}

.variant-glow.color-blue .icon-content {
  color: var(--duo-blue, #1CB0F6);
  border-color: var(--duo-blue, #1CB0F6);
}

.variant-glow.color-orange .icon-content {
  color: var(--duo-orange, #FF9600);
  border-color: var(--duo-orange, #FF9600);
}

.variant-glow.color-purple .icon-content {
  color: var(--duo-purple, #CE82FF);
  border-color: var(--duo-purple, #CE82FF);
}
</style>
