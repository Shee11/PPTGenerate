<!--
  two-cols-header.vue - Handdrawn Two Columns with Header Layout
  
  Slots:
    - header: Top header content
    - left: Left column
    - right: Right column
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="two-cols-header" :class="`vibe-${vibe}`">
      <!-- Header -->
      <div v-if="$slots.header" class="section-header">
        <div class="header-content">
          <slot name="header" />
        </div>
        <div class="header-doodle">
          <svg viewBox="0 0 200 10" class="squiggle">
            <path d="M0,5 Q25,0 50,5 T100,5 T150,5 T200,5" fill="none" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
      </div>
      
      <!-- Columns -->
      <div class="columns-container">
        <!-- Left column -->
        <div class="column column-left">
          <div class="column-paper paper-pink">
            <div class="paper-clip">📎</div>
            <div class="column-content">
              <slot name="left">
                <span class="placeholder">✏️ Left column content</span>
              </slot>
            </div>
          </div>
        </div>
        
        <!-- Divider -->
        <div class="column-divider">
          <div class="divider-dots">
            <span v-for="i in 5" :key="i">•</span>
          </div>
        </div>
        
        <!-- Right column -->
        <div class="column column-right">
          <div class="column-paper paper-blue">
            <div class="paper-clip">📎</div>
            <div class="column-content">
              <slot name="right">
                <span class="placeholder">✏️ Right column content</span>
              </slot>
            </div>
          </div>
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
.two-cols-header {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Header */
.section-header {
  text-align: center;
}

.header-content {
  font-family: var(--hand-font-display);
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

.header-content :deep(h1) {
  font-size: inherit;
  font-weight: inherit;
  margin: 0;
}

.header-content :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 1rem;
  color: var(--hand-text);
  margin: 0.25rem 0 0 0;
}

.header-doodle {
  color: var(--hand-pink);
  margin-top: 0.5rem;
}

.squiggle {
  width: 150px;
  height: 10px;
}

/* Columns */
.columns-container {
  flex: 1;
  display: flex;
  gap: 1rem;
}

.column {
  flex: 1;
  display: flex;
}

.column-paper {
  flex: 1;
  position: relative;
  padding: 1.5rem;
  padding-top: 2rem;
  border-radius: 8px;
  box-shadow: 4px 4px 0 var(--hand-shadow-color);
}

.paper-pink {
  background: linear-gradient(180deg, var(--hand-pink-light) 0%, var(--hand-bg-cream) 100%);
  border: 2px solid var(--hand-pink);
  transform: rotate(-1deg);
}

.paper-blue {
  background: linear-gradient(180deg, var(--hand-blue-light) 0%, var(--hand-bg-cream) 100%);
  border: 2px solid var(--hand-blue);
  transform: rotate(1deg);
}

/* Paper clip */
.paper-clip {
  position: absolute;
  top: -10px;
  left: 20px;
  font-size: 1.5rem;
  transform: rotate(-15deg);
}

/* Column content */
.column-content :deep(h2) {
  font-family: var(--hand-font-display);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  margin: 0 0 0.75rem 0;
}

.column-content :deep(h3) {
  font-family: var(--hand-font-display);
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  margin: 0.5rem 0;
}

.column-content :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--hand-text);
  margin: 0 0 0.5rem 0;
}

.column-content :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0;
}

.column-content :deep(li) {
  font-family: var(--hand-font-body);
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--hand-text);
  padding-left: 1.25rem;
  position: relative;
  margin-bottom: 0.3rem;
}

.column-content :deep(li::before) {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--hand-pink);
}

/* Divider */
.column-divider {
  display: flex;
  align-items: center;
}

.divider-dots {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  color: var(--hand-text-light);
  font-size: 0.8rem;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 0.9rem;
}

/* Vibe modifiers */
.vibe-minimal .column-paper {
  background: var(--hand-bg-cream);
  border-width: 1px;
  box-shadow: none;
  transform: none;
}

.vibe-minimal .paper-clip,
.vibe-minimal .header-doodle,
.vibe-minimal .column-divider {
  display: none;
}

.vibe-playful .column-paper:hover {
  transform: scale(1.02) rotate(0deg);
}

.vibe-decorated .column-paper::before {
  content: '✨';
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 1rem;
}
</style>
