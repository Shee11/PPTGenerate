<!--
  stats-showcase.vue - Cyberpunk Stats Showcase Layout
  
  Slots:
    - title: Section title
    - stat1 through stat4: Individual stats
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="stats-showcase" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="stats-title">
        <span class="title-prefix">&gt;_</span>
        <slot name="title" />
      </div>
      
      <!-- Stats grid -->
      <div class="stats-grid">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="stat-card"
          :class="`stat-${i}`"
          :style="{ '--stat-index': i }"
        >
          <div class="stat-glow"></div>
          <div class="stat-frame">
            <div class="frame-top"></div>
            <div class="frame-bottom"></div>
          </div>
          <div class="stat-content">
            <slot :name="`stat${i}`">
              <div class="placeholder">
                <span class="stat-value">--</span>
                <span class="stat-label">STAT_{{ i }}</span>
              </div>
            </slot>
          </div>
          <div class="stat-pulse"></div>
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
.stats-showcase {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Title */
.stats-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: var(--cyber-font-display);
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 3px;
}

.title-prefix {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 10px var(--cyber-magenta-glow);
}

/* Stats grid */
.stats-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  align-items: stretch;
}

.stat-card {
  position: relative;
  background: rgba(18, 18, 26, 0.9);
  border: 1px solid rgba(0, 255, 255, 0.2);
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  animation: stat-enter 0.6s ease-out backwards;
  animation-delay: calc(var(--stat-index) * 0.15s);
  overflow: hidden;
}

@keyframes stat-enter {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
}

/* Stat colors */
.stat-1 { --stat-accent: var(--cyber-cyan, #00FFFF); }
.stat-2 { --stat-accent: var(--cyber-magenta, #FF00FF); }
.stat-3 { --stat-accent: var(--cyber-yellow, #FFFF00); }
.stat-4 { --stat-accent: var(--cyber-pink, #FF0080); }

/* Glow effect */
.stat-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--stat-accent);
  box-shadow: 0 0 30px var(--stat-accent);
}

/* Frame */
.stat-frame {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.frame-top,
.frame-bottom {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--stat-accent), transparent);
  opacity: 0.5;
}

.frame-top { top: 15px; }
.frame-bottom { bottom: 15px; }

/* Stat content */
.stat-content {
  position: relative;
  z-index: 5;
}

.stat-content :deep(.value),
.stat-content :deep(h2) {
  font-family: var(--cyber-font-display);
  font-size: 3rem;
  font-weight: 700;
  color: var(--stat-accent);
  text-shadow: 0 0 20px var(--stat-accent);
  margin-bottom: 0.5rem;
  line-height: 1;
}

.stat-content :deep(.label),
.stat-content :deep(p) {
  font-family: var(--cyber-font-mono);
  font-size: 0.9rem;
  color: var(--cyber-text, #e0e0e0);
  text-transform: uppercase;
  letter-spacing: 2px;
}

/* Pulse effect */
.stat-pulse {
  position: absolute;
  inset: 0;
  border: 2px solid var(--stat-accent);
  opacity: 0;
  pointer-events: none;
}

.stat-card:hover .stat-pulse {
  animation: pulse-effect 1s ease-out;
}

@keyframes pulse-effect {
  from {
    opacity: 0.6;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(1.1);
  }
}

.placeholder {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.placeholder .stat-value {
  font-family: var(--cyber-font-display);
  font-size: 3rem;
  font-weight: 700;
  color: var(--stat-accent);
  text-shadow: 0 0 20px var(--stat-accent);
}

.placeholder .stat-label {
  font-family: var(--cyber-font-mono);
  font-size: 0.8rem;
  color: var(--cyber-text-dim);
}

/* Vibe modifiers */
.vibe-minimal .stat-glow,
.vibe-minimal .stat-frame {
  display: none;
}

.vibe-intense .stat-glow {
  height: 6px;
}

.vibe-intense .stat-content :deep(.value) {
  animation: value-pulse 2s ease-in-out infinite alternate;
}

@keyframes value-pulse {
  from { text-shadow: 0 0 20px var(--stat-accent); }
  to { text-shadow: 0 0 40px var(--stat-accent), 0 0 60px var(--stat-accent); }
}

.vibe-glitch .stat-card:nth-child(even) {
  animation: stat-enter 0.6s ease-out backwards, stat-glitch 4s ease-in-out infinite;
}

@keyframes stat-glitch {
  0%, 100% { transform: translate(0); filter: none; }
  25% { transform: translate(-2px, 0); filter: hue-rotate(10deg); }
  50% { transform: translate(2px, 0); }
  75% { transform: translate(0); filter: none; }
}
</style>
