<!--
  magazine.vue - Cyberpunk Magazine Style Layout
  
  Slots:
    - headline: Main headline
    - lead: Lead paragraph
    - col1, col2: Column content
    - sidebar: Sidebar content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="magazine-layout" :class="`vibe-${vibe}`">
      <!-- Header area -->
      <div class="magazine-header">
        <div class="header-decoration">
          <span class="deco-line"></span>
          <span class="deco-text">DATASTREAM</span>
          <span class="deco-line"></span>
        </div>
        
        <h1 class="headline">
          <slot name="headline">
            <span class="placeholder">// HEADLINE</span>
          </slot>
        </h1>
        
        <div v-if="$slots.lead" class="lead">
          <slot name="lead" />
        </div>
      </div>
      
      <!-- Content grid -->
      <div class="magazine-content">
        <!-- Main columns -->
        <div class="main-columns">
          <div class="column column-1">
            <div class="column-header">
              <span class="col-marker">01</span>
            </div>
            <div class="column-body">
              <slot name="col1">
                <span class="placeholder">// COL_1</span>
              </slot>
            </div>
          </div>
          
          <div class="column column-2">
            <div class="column-header">
              <span class="col-marker">02</span>
            </div>
            <div class="column-body">
              <slot name="col2">
                <span class="placeholder">// COL_2</span>
              </slot>
            </div>
          </div>
        </div>
        
        <!-- Sidebar -->
        <div v-if="$slots.sidebar" class="sidebar">
          <div class="sidebar-header">
            <span class="sidebar-icon">[!]</span>
            <span class="sidebar-title">INTEL</span>
          </div>
          <div class="sidebar-content">
            <slot name="sidebar" />
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
.magazine-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Header */
.magazine-header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.header-decoration {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.deco-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--cyber-cyan, #00FFFF), transparent);
}

.deco-text {
  font-family: var(--cyber-font-mono);
  font-size: 0.75rem;
  color: var(--cyber-cyan, #00FFFF);
  letter-spacing: 4px;
  text-shadow: 0 0 5px var(--cyber-cyan-glow);
}

.headline {
  font-family: var(--cyber-font-display);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 3px;
  line-height: 1.1;
  text-shadow: 0 0 20px var(--cyber-cyan-glow);
  margin: 0;
}

.lead {
  font-family: var(--cyber-font-body);
  font-size: 1.15rem;
  line-height: 1.6;
  color: var(--cyber-text, #e0e0e0);
  border-left: 3px solid var(--cyber-magenta, #FF00FF);
  padding-left: 1rem;
}

/* Content grid */
.magazine-content {
  flex: 1;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

/* Main columns */
.main-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.column-header {
  display: flex;
  align-items: center;
}

.col-marker {
  font-family: var(--cyber-font-mono);
  font-size: 0.8rem;
  color: var(--cyber-magenta, #FF00FF);
  background: rgba(255, 0, 255, 0.1);
  padding: 0.2rem 0.5rem;
  border: 1px solid rgba(255, 0, 255, 0.3);
}

.column-body {
  font-family: var(--cyber-font-body);
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--cyber-text, #e0e0e0);
}

.column-body :deep(p) {
  margin-bottom: 0.75rem;
}

.column-body :deep(strong) {
  color: var(--cyber-cyan, #00FFFF);
}

/* Sidebar */
.sidebar {
  background: rgba(18, 18, 26, 0.9);
  border: 1px solid rgba(255, 255, 0, 0.3);
  border-left: 3px solid var(--cyber-yellow, #FFFF00);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sidebar-icon {
  font-family: var(--cyber-font-mono);
  font-size: 0.9rem;
  color: var(--cyber-yellow, #FFFF00);
  text-shadow: 0 0 10px var(--cyber-yellow-glow);
}

.sidebar-title {
  font-family: var(--cyber-font-display);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--cyber-yellow, #FFFF00);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.sidebar-content {
  font-family: var(--cyber-font-body);
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--cyber-text, #e0e0e0);
}

.sidebar-content :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-content :deep(li) {
  padding-left: 1rem;
  position: relative;
  margin-bottom: 0.4rem;
}

.sidebar-content :deep(li::before) {
  content: '•';
  position: absolute;
  left: 0;
  color: var(--cyber-yellow, #FFFF00);
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.8rem;
}

/* Vibe modifiers */
.vibe-minimal .header-decoration,
.vibe-minimal .column-header {
  display: none;
}

.vibe-intense .headline {
  font-size: 3rem;
  animation: headline-glow 2s ease-in-out infinite alternate;
}

@keyframes headline-glow {
  from { text-shadow: 0 0 20px var(--cyber-cyan-glow); }
  to { text-shadow: 0 0 40px var(--cyber-cyan-glow), 0 0 60px var(--cyber-cyan-glow); }
}

.vibe-glitch .headline {
  animation: headline-glitch 5s ease-in-out infinite;
}

@keyframes headline-glitch {
  0%, 100% { transform: translate(0); filter: none; }
  10% { transform: translate(-3px, 0); filter: hue-rotate(10deg); }
  20% { transform: translate(3px, 0); }
  30% { transform: translate(0); filter: none; }
}
</style>
