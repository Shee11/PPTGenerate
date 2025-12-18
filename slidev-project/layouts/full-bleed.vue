<script setup lang="ts">
import { computed } from 'vue'

// Props from frontmatter
const props = defineProps<{
  align?: 'top' | 'center' | 'bottom'
}>()

// Map align parameter to flexbox alignment
const alignmentStyle = computed(() => {
  const align = props.align || 'center'
  
  const alignMap = {
    top: 'flex-start',
    center: 'center',
    bottom: 'flex-end'
  }
  
  return {
    justifyContent: alignMap[align] || 'center'
  }
})
</script>

<template>
  <div class="full-bleed-layout" :style="alignmentStyle">
    <div class="content-wrapper">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.full-bleed-layout {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 3rem;
  background: linear-gradient(135deg, 
    var(--c-bg-base) 0%, 
    color-mix(in srgb, var(--c-bg-base) 92%, var(--slidev-theme-primary, #3b82f6)) 100%);
  color: var(--c-text-main);
  position: relative;
  overflow: hidden;
}

/* Vignette overlay */
.full-bleed-layout::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, 
    transparent 0%, 
    transparent 40%,
    rgba(0, 0, 0, 0.15) 100%);
  pointer-events: none;
  z-index: 1;
}

/* Decorative gradient shape */
.full-bleed-layout::after {
  content: '';
  position: absolute;
  top: -20%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, 
    rgba(59, 130, 246, 0.08) 0%, 
    transparent 60%);
  border-radius: 50%;
  pointer-events: none;
}

.content-wrapper {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem;
  background: linear-gradient(145deg,
    color-mix(in srgb, var(--c-bg-base) 70%, white) 0%,
    color-mix(in srgb, var(--c-bg-base) 65%, white) 100%);
  border-radius: 20px;
  backdrop-filter: blur(20px);
  border: 1px solid color-mix(in srgb, white 20%, transparent);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.12),
    0 16px 64px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 2;
}

/* Corner accents */
.content-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, 
    var(--slidev-theme-primary, #3b82f6) 0%, 
    transparent 70%);
  opacity: 0.15;
  border-radius: 20px 0 20px 0;
}

.content-wrapper::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 80px;
  height: 80px;
  background: linear-gradient(-135deg, 
    var(--slidev-theme-primary, #3b82f6) 0%, 
    transparent 70%);
  opacity: 0.15;
  border-radius: 0 20px 20px 0;
}
</style>
