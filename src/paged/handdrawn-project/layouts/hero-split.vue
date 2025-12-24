<!--
  hero-split.vue - Handdrawn Hero Split Layout
  
  Slots:
    - left: Left panel content
    - right: Right panel content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="hero-split" :class="`vibe-${vibe}`">
      <!-- Divider doodle -->
      <div class="split-divider">
        <svg viewBox="0 0 10 200" class="divider-squiggle">
          <path d="M5,0 Q0,25 5,50 T5,100 T5,150 T5,200" fill="none" stroke="currentColor" stroke-width="2"/>
        </svg>
      </div>
      
      <!-- Left panel -->
      <div class="panel panel-left">
        <div class="panel-inner sticky-style sticky-pink">
          <slot name="left">
            <span class="placeholder">✏️ Left content</span>
          </slot>
        </div>
      </div>
      
      <!-- Right panel -->
      <div class="panel panel-right">
        <div class="panel-inner sticky-style sticky-blue">
          <slot name="right">
            <span class="placeholder">✏️ Right content</span>
          </slot>
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import SlideShell from './SlideShell.vue'

withDefaults(defineProps<{
  theme?: string
  vibe?: string
  header?: string
  footer?: string
}>(), {
  theme: 'handdrawn',
  vibe: 'cozy'
})
</script>

<style scoped>
.hero-split {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  position: relative;
}

/* Divider */
.split-divider {
  position: absolute;
  left: 50%;
  top: 5%;
  bottom: 5%;
  transform: translateX(-50%);
  color: var(--hand-pink-light);
  z-index: 10;
}

.divider-squiggle {
  height: 100%;
  width: 20px;
}

/* Panels */
.panel {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.panel-inner {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1.5rem;
}

.sticky-style {
  border-radius: 3px;
  box-shadow: 4px 4px 0 var(--hand-shadow-color);
}

.sticky-pink {
  background: var(--hand-pink-light);
  transform: rotate(-1deg);
}

.sticky-blue {
  background: var(--hand-blue-light);
  transform: rotate(1deg);
}

.panel-inner :deep(h1) {
  font-family: var(--hand-font-display);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--hand-text-dark);
  margin-bottom: 0.75rem;
}

.panel-inner :deep(h2) {
  font-family: var(--hand-font-display);
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--hand-text);
  margin-bottom: 0.5rem;
}

.panel-inner :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--hand-text);
}

.panel-inner :deep(ul) {
  list-style: none;
  padding: 0;
}

.panel-inner :deep(li) {
  font-family: var(--hand-font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--hand-text);
  padding-left: 1.5rem;
  position: relative;
  margin-bottom: 0.4rem;
}

.panel-inner :deep(li::before) {
  content: '✦';
  position: absolute;
  left: 0;
  color: var(--hand-pink);
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 1rem;
}

/* Vibe modifiers */
.vibe-minimal .sticky-style {
  background: transparent;
  box-shadow: none;
  transform: none;
}

.vibe-minimal .split-divider {
  display: none;
}

.vibe-playful .sticky-pink {
  transform: rotate(-2deg);
}

.vibe-playful .sticky-blue {
  transform: rotate(2deg);
}

.vibe-decorated .panel-inner {
  position: relative;
}

.vibe-decorated .panel-inner::before {
  content: '📌';
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.5rem;
}
</style>
