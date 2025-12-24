<!--
  smart-grid.vue - Cyberpunk Responsive Grid Layout
  
  Slots:
    - header: Grid header
    - col1, col2, col3, col4: Column content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="smart-grid" :class="`vibe-${vibe}`">
      <!-- Header -->
      <div v-if="$slots.header" class="grid-header">
        <div class="header-bracket">[</div>
        <slot name="header" />
        <div class="header-bracket">]</div>
      </div>
      
      <!-- Grid columns -->
      <div class="grid-columns">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="grid-col"
          :class="`col-${i}`"
          :style="{ '--col-index': i }"
        >
          <div class="col-frame">
            <div class="frame-corner frame-tl"></div>
            <div class="frame-corner frame-br"></div>
          </div>
          <div class="col-content">
            <slot :name="`col${i}`">
              <div class="placeholder">// COL_{{ i }}</div>
            </slot>
          </div>
          <div class="col-index">0{{ i }}</div>
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
.smart-grid {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Header */
.grid-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-family: var(--cyber-font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 3px;
  text-shadow: 0 0 10px var(--cyber-cyan-glow);
}

.header-bracket {
  font-family: var(--cyber-font-mono);
  font-size: 2rem;
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 10px var(--cyber-magenta-glow);
}

/* Grid columns */
.grid-columns {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.grid-col {
  position: relative;
  background: rgba(18, 18, 26, 0.8);
  border: 1px solid rgba(0, 255, 255, 0.3);
  padding: 1.5rem;
  animation: col-enter 0.5s ease-out backwards;
  animation-delay: calc(var(--col-index) * 0.1s);
}

@keyframes col-enter {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
}

.grid-col:hover {
  border-color: var(--cyber-cyan, #00FFFF);
  box-shadow: 
    0 0 15px var(--cyber-cyan-glow),
    inset 0 0 30px rgba(0, 255, 255, 0.05);
}

/* Column frame corners */
.col-frame {
  position: absolute;
  inset: -1px;
  pointer-events: none;
}

.frame-corner {
  position: absolute;
  width: 15px;
  height: 15px;
}

.frame-tl {
  top: 0;
  left: 0;
  border-top: 2px solid var(--cyber-cyan, #00FFFF);
  border-left: 2px solid var(--cyber-cyan, #00FFFF);
}

.frame-br {
  bottom: 0;
  right: 0;
  border-bottom: 2px solid var(--cyber-magenta, #FF00FF);
  border-right: 2px solid var(--cyber-magenta, #FF00FF);
}

/* Column content */
.col-content {
  position: relative;
  z-index: 5;
}

.col-content :deep(h3) {
  font-family: var(--cyber-font-display);
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--cyber-cyan, #00FFFF);
  text-shadow: 0 0 8px var(--cyber-cyan-glow);
  margin-bottom: 0.75rem;
  text-transform: uppercase;
}

.col-content :deep(p) {
  font-family: var(--cyber-font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--cyber-text, #e0e0e0);
}

/* Column index */
.col-index {
  position: absolute;
  bottom: 0.5rem;
  right: 0.75rem;
  font-family: var(--cyber-font-mono);
  font-size: 0.7rem;
  color: var(--cyber-text-dim);
  opacity: 0.5;
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.8rem;
}

/* Alternating accent colors */
.col-1 { --col-accent: var(--cyber-cyan, #00FFFF); }
.col-2 { --col-accent: var(--cyber-magenta, #FF00FF); }
.col-3 { --col-accent: var(--cyber-yellow, #FFFF00); }
.col-4 { --col-accent: var(--cyber-pink, #FF0080); }

/* Vibe modifiers */
.vibe-minimal .col-frame,
.vibe-minimal .col-index {
  display: none;
}

.vibe-intense .grid-col {
  border-width: 2px;
}

.vibe-intense .frame-tl,
.vibe-intense .frame-br {
  width: 25px;
  height: 25px;
  border-width: 3px;
}

.vibe-glitch .grid-col:nth-child(odd) {
  animation: col-enter 0.5s ease-out backwards, glitch-subtle 4s ease-in-out infinite;
}

@keyframes glitch-subtle {
  0%, 100% { transform: translate(0); }
  25% { transform: translate(-1px, 0); }
  75% { transform: translate(1px, 0); }
}
</style>
