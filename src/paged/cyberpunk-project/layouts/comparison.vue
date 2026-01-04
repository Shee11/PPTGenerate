<!--
  comparison.vue - Cyberpunk Comparison Layout
  
  Slots:
    - title: Section title
    - left_title, left_content: Left comparison panel
    - right_title, right_content: Right comparison panel
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="comparison-layout" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="section-title">
        <div class="title-text">
          <slot name="title" />
        </div>
        <div class="title-line"></div>
      </div>
      
      <!-- Comparison panels -->
      <div class="comparison-panels">
        <!-- Left panel -->
        <div class="panel panel-left">
          <div class="panel-accent"></div>
          <div class="panel-label">
            <span class="label-icon">&lt;</span>
            <span class="label-text">OPTION_A</span>
          </div>
          <div class="panel-title">
            <slot name="left_title">
              <span class="placeholder">SYSTEM_A</span>
            </slot>
          </div>
          <div class="panel-content">
            <slot name="left_content">
              <span class="placeholder">// Data loading...</span>
            </slot>
          </div>
        </div>
        
        <!-- VS divider -->
        <div class="vs-divider">
          <div class="vs-line vs-line-top"></div>
          <div class="vs-badge">VS</div>
          <div class="vs-line vs-line-bottom"></div>
        </div>
        
        <!-- Right panel -->
        <div class="panel panel-right">
          <div class="panel-accent"></div>
          <div class="panel-label">
            <span class="label-icon">&gt;</span>
            <span class="label-text">OPTION_B</span>
          </div>
          <div class="panel-title">
            <slot name="right_title">
              <span class="placeholder">SYSTEM_B</span>
            </slot>
          </div>
          <div class="panel-content">
            <slot name="right_content">
              <span class="placeholder">// Data loading...</span>
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
.comparison-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Title */
.section-title {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.title-text {
  font-family: var(--cyber-font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 3px;
  text-shadow: 0 0 10px var(--cyber-cyan-glow);
  white-space: nowrap;
}

.title-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--cyber-cyan, #00FFFF), transparent);
  box-shadow: 0 0 5px var(--cyber-cyan-glow);
}

/* Comparison panels */
.comparison-panels {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1.5rem;
  align-items: stretch;
}

.panel {
  position: relative;
  background: rgba(18, 18, 26, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: hidden;
}

.panel-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.panel-left .panel-accent {
  background: var(--cyber-cyan, #00FFFF);
  box-shadow: 0 0 20px var(--cyber-cyan-glow);
}

.panel-right .panel-accent {
  background: var(--cyber-magenta, #FF00FF);
  box-shadow: 0 0 20px var(--cyber-magenta-glow);
}

/* Panel label */
.panel-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--cyber-font-mono);
  font-size: 0.8rem;
}

.panel-left .panel-label {
  color: var(--cyber-cyan, #00FFFF);
}

.panel-right .panel-label {
  color: var(--cyber-magenta, #FF00FF);
}

.label-icon {
  font-size: 1rem;
  text-shadow: 0 0 5px currentColor;
}

/* Panel title */
.panel-title {
  font-family: var(--cyber-font-display);
  font-size: 1.5rem;
  font-weight: 700;
  text-transform: uppercase;
}

.panel-left .panel-title {
  color: var(--cyber-cyan, #00FFFF);
  text-shadow: 0 0 10px var(--cyber-cyan-glow);
}

.panel-right .panel-title {
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 10px var(--cyber-magenta-glow);
}

/* Panel content */
.panel-content {
  flex: 1;
  font-family: var(--cyber-font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--cyber-text, #e0e0e0);
}

.panel-content :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0;
}

.panel-content :deep(li) {
  padding-left: 1.5rem;
  position: relative;
  margin-bottom: 0.5rem;
}

.panel-left .panel-content :deep(li::before) {
  content: '+';
  position: absolute;
  left: 0;
  color: var(--cyber-cyan, #00FFFF);
  font-family: var(--cyber-font-mono);
}

.panel-right .panel-content :deep(li::before) {
  content: '+';
  position: absolute;
  left: 0;
  color: var(--cyber-magenta, #FF00FF);
  font-family: var(--cyber-font-mono);
}

/* VS Divider */
.vs-divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 2rem 0;
}

.vs-line {
  width: 2px;
  flex: 1;
  background: linear-gradient(180deg, var(--cyber-cyan, #00FFFF), var(--cyber-magenta, #FF00FF));
}

.vs-line-top {
  background: linear-gradient(180deg, transparent, var(--cyber-yellow, #FFFF00));
}

.vs-line-bottom {
  background: linear-gradient(180deg, var(--cyber-yellow, #FFFF00), transparent);
}

.vs-badge {
  font-family: var(--cyber-font-display);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--cyber-yellow, #FFFF00);
  background: rgba(18, 18, 26, 0.95);
  border: 2px solid var(--cyber-yellow, #FFFF00);
  padding: 0.5rem 0.75rem;
  text-shadow: 0 0 10px var(--cyber-yellow-glow);
  box-shadow: 0 0 15px var(--cyber-yellow-glow);
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.8rem;
}

/* Vibe modifiers */
.vibe-minimal .panel-accent,
.vibe-minimal .vs-line {
  display: none;
}

.vibe-intense .panel-accent {
  height: 5px;
}

.vibe-intense .vs-badge {
  border-width: 3px;
  font-size: 1.5rem;
}

.vibe-glitch .panel {
  animation: panel-glitch 5s ease-in-out infinite;
}

.vibe-glitch .panel-right {
  animation-delay: 0.5s;
}

@keyframes panel-glitch {
  0%, 100% { transform: translate(0); }
  25% { transform: translate(-1px, 0); }
  75% { transform: translate(1px, 0); }
}
</style>
