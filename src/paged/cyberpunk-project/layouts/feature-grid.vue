<!--
  feature-grid.vue - Cyberpunk Feature Grid Layout
  
  Slots:
    - title: Section title
    - feature1 through feature4: Individual features
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="feature-grid-layout" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="section-title">
        <div class="title-line title-line-left"></div>
        <span class="title-text">
          <slot name="title" />
        </span>
        <div class="title-line title-line-right"></div>
      </div>
      
      <!-- Feature grid -->
      <div class="feature-container">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="feature"
          :class="`feature-${i}`"
          :style="{ '--feature-index': i }"
        >
          <div class="feature-accent"></div>
          <div class="feature-number">
            <span class="number-value">0{{ i }}</span>
          </div>
          <div class="feature-content">
            <slot :name="`feature${i}`">
              <span class="placeholder">// FEATURE_{{ i }}</span>
            </slot>
          </div>
          <div class="feature-corner feature-corner-br"></div>
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
.feature-grid-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
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
  letter-spacing: 4px;
  text-shadow: 0 0 10px var(--cyber-cyan-glow);
  white-space: nowrap;
}

.title-line {
  flex: 1;
  height: 1px;
}

.title-line-left {
  background: linear-gradient(90deg, transparent, var(--cyber-cyan, #00FFFF));
}

.title-line-right {
  background: linear-gradient(90deg, var(--cyber-cyan, #00FFFF), transparent);
}

/* Feature container */
.feature-container {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 1.5rem;
}

.feature {
  position: relative;
  background: rgba(18, 18, 26, 0.85);
  border: 1px solid rgba(0, 255, 255, 0.2);
  padding: 1.75rem;
  display: flex;
  gap: 1.25rem;
  animation: feature-enter 0.5s ease-out backwards;
  animation-delay: calc(var(--feature-index) * 0.12s);
  overflow: hidden;
}

@keyframes feature-enter {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
}

.feature:hover {
  border-color: var(--feature-accent);
  box-shadow: 
    0 0 20px var(--feature-accent-glow),
    inset 0 0 30px rgba(0, 255, 255, 0.02);
}

/* Feature colors */
.feature-1 { 
  --feature-accent: var(--cyber-cyan, #00FFFF); 
  --feature-accent-glow: var(--cyber-cyan-glow);
}
.feature-2 { 
  --feature-accent: var(--cyber-magenta, #FF00FF); 
  --feature-accent-glow: var(--cyber-magenta-glow);
}
.feature-3 { 
  --feature-accent: var(--cyber-yellow, #FFFF00); 
  --feature-accent-glow: var(--cyber-yellow-glow);
}
.feature-4 { 
  --feature-accent: var(--cyber-pink, #FF0080); 
  --feature-accent-glow: var(--cyber-pink-glow);
}

/* Feature accent bar */
.feature-accent {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 4px;
  background: var(--feature-accent);
  box-shadow: 0 0 15px var(--feature-accent-glow);
}

/* Feature number */
.feature-number {
  display: flex;
  align-items: flex-start;
  flex-shrink: 0;
}

.number-value {
  font-family: var(--cyber-font-mono);
  font-size: 2rem;
  font-weight: 700;
  color: var(--feature-accent);
  text-shadow: 0 0 15px var(--feature-accent-glow);
  line-height: 1;
}

/* Feature content */
.feature-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.feature-content :deep(h3) {
  font-family: var(--cyber-font-display);
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--feature-accent);
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.feature-content :deep(p) {
  font-family: var(--cyber-font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--cyber-text, #e0e0e0);
}

/* Corner decoration */
.feature-corner-br {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 15px;
  height: 15px;
  border-bottom: 2px solid var(--feature-accent);
  border-right: 2px solid var(--feature-accent);
  opacity: 0.6;
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.8rem;
}

/* Vibe modifiers */
.vibe-minimal .feature-accent,
.vibe-minimal .feature-corner-br,
.vibe-minimal .feature-number {
  display: none;
}

.vibe-intense .feature-accent {
  width: 6px;
}

.vibe-intense .number-value {
  animation: number-pulse 2s ease-in-out infinite alternate;
}

@keyframes number-pulse {
  from { text-shadow: 0 0 15px var(--feature-accent-glow); }
  to { text-shadow: 0 0 30px var(--feature-accent-glow), 0 0 50px var(--feature-accent-glow); }
}

.vibe-glitch .feature:nth-child(even) {
  animation: feature-enter 0.5s ease-out backwards, feature-glitch 5s ease-in-out infinite;
}

@keyframes feature-glitch {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-2px, 0); }
  40% { transform: translate(2px, 0); }
  60% { transform: translate(0); }
}
</style>
