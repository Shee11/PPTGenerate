<!--
  two-cols-header.vue - Cyberpunk Two Columns with Header Layout
  
  Slots:
    - header: Top header section
    - left: Left column content
    - right: Right column content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="two-cols-header-layout" :class="`vibe-${vibe}`">
      <!-- Header section -->
      <div v-if="$slots.header" class="layout-header">
        <div class="header-content">
          <slot name="header" />
        </div>
        <div class="header-line"></div>
      </div>
      
      <!-- Columns -->
      <div class="columns-container">
        <!-- Left column -->
        <div class="column column-left">
          <div class="column-marker">
            <span class="marker-icon">&lt;</span>
            <span class="marker-text">COL_A</span>
          </div>
          <div class="column-content">
            <slot name="left">
              <span class="placeholder">// LEFT_CONTENT</span>
            </slot>
          </div>
        </div>
        
        <!-- Divider -->
        <div class="column-divider">
          <div class="divider-line"></div>
          <div class="divider-dot"></div>
          <div class="divider-line"></div>
        </div>
        
        <!-- Right column -->
        <div class="column column-right">
          <div class="column-marker">
            <span class="marker-icon">&gt;</span>
            <span class="marker-text">COL_B</span>
          </div>
          <div class="column-content">
            <slot name="right">
              <span class="placeholder">// RIGHT_CONTENT</span>
            </slot>
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
  theme: 'cyberpunk',
  vibe: 'balanced'
})
</script>

<style scoped>
.two-cols-header-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Header */
.layout-header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.header-content {
  font-family: var(--cyber-font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 3px;
  text-shadow: 0 0 15px var(--cyber-cyan-glow);
}

.header-content :deep(p) {
  font-family: var(--cyber-font-body);
  font-size: 1.1rem;
  font-weight: 400;
  color: var(--cyber-text, #e0e0e0);
  text-transform: none;
  letter-spacing: normal;
  text-shadow: none;
  margin-top: 0.5rem;
}

.header-line {
  height: 2px;
  background: linear-gradient(
    90deg, 
    var(--cyber-cyan, #00FFFF) 0%, 
    var(--cyber-magenta, #FF00FF) 50%,
    transparent 100%
  );
  box-shadow: 0 0 10px var(--cyber-cyan-glow);
}

/* Columns container */
.columns-container {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1.5rem;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Column marker */
.column-marker {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--cyber-font-mono);
  font-size: 0.8rem;
}

.column-left .column-marker {
  color: var(--cyber-cyan, #00FFFF);
}

.column-right .column-marker {
  color: var(--cyber-magenta, #FF00FF);
}

.marker-icon {
  font-size: 1rem;
  text-shadow: 0 0 5px currentColor;
}

/* Column content */
.column-content {
  flex: 1;
  background: rgba(18, 18, 26, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
}

.column-left .column-content {
  border-left: 3px solid var(--cyber-cyan, #00FFFF);
}

.column-right .column-content {
  border-left: 3px solid var(--cyber-magenta, #FF00FF);
}

.column-content :deep(h3) {
  font-family: var(--cyber-font-display);
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}

.column-right .column-content :deep(h3) {
  color: var(--cyber-magenta, #FF00FF);
}

.column-content :deep(p) {
  font-family: var(--cyber-font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--cyber-text, #e0e0e0);
  margin-bottom: 0.5rem;
}

.column-content :deep(ul) {
  list-style: none;
  padding: 0;
}

.column-content :deep(li) {
  padding-left: 1.25rem;
  position: relative;
  margin-bottom: 0.4rem;
  font-family: var(--cyber-font-body);
  font-size: 0.95rem;
  color: var(--cyber-text, #e0e0e0);
}

.column-content :deep(li::before) {
  content: '>';
  position: absolute;
  left: 0;
  font-family: var(--cyber-font-mono);
}

.column-left .column-content :deep(li::before) {
  color: var(--cyber-cyan, #00FFFF);
}

.column-right .column-content :deep(li::before) {
  color: var(--cyber-magenta, #FF00FF);
}

/* Divider */
.column-divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 0;
}

.divider-line {
  flex: 1;
  width: 1px;
  background: linear-gradient(180deg, transparent, rgba(255, 255, 255, 0.3), transparent);
}

.divider-dot {
  width: 8px;
  height: 8px;
  background: var(--cyber-yellow, #FFFF00);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--cyber-yellow-glow);
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.8rem;
}

/* Vibe modifiers */
.vibe-minimal .column-marker,
.vibe-minimal .column-divider {
  display: none;
}

.vibe-minimal .columns-container {
  grid-template-columns: 1fr 1fr;
}

.vibe-intense .header-line {
  height: 3px;
}

.vibe-intense .divider-dot {
  animation: dot-pulse 1.5s ease-in-out infinite;
}

@keyframes dot-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.3); opacity: 0.7; }
}

.vibe-glitch .column {
  animation: col-glitch 6s ease-in-out infinite;
}

.vibe-glitch .column-right {
  animation-delay: 0.3s;
}

@keyframes col-glitch {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-1px, 0); }
  40% { transform: translate(1px, 0); }
}
</style>
