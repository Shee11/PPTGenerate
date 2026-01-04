<!--
  dashboard.vue - Cyberpunk Dashboard Layout
  
  Slots:
    - title: Dashboard title
    - widget1 through widget6: Dashboard widgets
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="dashboard-layout" :class="`vibe-${vibe}`">
      <!-- Title bar -->
      <div class="dashboard-header">
        <div class="header-left">
          <div class="system-indicator">
            <span class="indicator-dot"></span>
            <span class="indicator-text">SYS_ONLINE</span>
          </div>
          <div class="dashboard-title">
            <slot name="title">
              <span>DASHBOARD</span>
            </slot>
          </div>
        </div>
        <div class="header-right">
          <span class="timestamp">{{ currentTime }}</span>
        </div>
      </div>
      
      <!-- Widget grid -->
      <div class="widget-grid">
        <div 
          v-for="i in 6" 
          :key="i" 
          class="widget"
          :class="`widget-${i}`"
          :style="{ '--widget-index': i }"
        >
          <div class="widget-chrome">
            <div class="chrome-corner chrome-tl"></div>
            <div class="chrome-corner chrome-tr"></div>
            <div class="chrome-corner chrome-bl"></div>
            <div class="chrome-corner chrome-br"></div>
          </div>
          <div class="widget-header">
            <span class="widget-id">W0{{ i }}</span>
          </div>
          <div class="widget-content">
            <slot :name="`widget${i}`">
              <span class="placeholder">// WIDGET_{{ i }}</span>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
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

const currentTime = ref('00:00:00')

onMounted(() => {
  const updateTime = () => {
    const now = new Date()
    currentTime.value = now.toTimeString().slice(0, 8)
  }
  updateTime()
  setInterval(updateTime, 1000)
})
</script>

<style scoped>
.dashboard-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Header */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.3);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.system-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.indicator-dot {
  width: 8px;
  height: 8px;
  background: var(--cyber-green, #00FF41);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--cyber-green-glow);
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.8); }
}

.indicator-text {
  font-family: var(--cyber-font-mono);
  font-size: 0.75rem;
  color: var(--cyber-green, #00FF41);
  text-shadow: 0 0 5px var(--cyber-green-glow);
}

.dashboard-title {
  font-family: var(--cyber-font-display);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 3px;
}

.timestamp {
  font-family: var(--cyber-font-mono);
  font-size: 0.9rem;
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 5px var(--cyber-magenta-glow);
}

/* Widget grid */
.widget-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 1rem;
}

.widget {
  position: relative;
  background: rgba(18, 18, 26, 0.85);
  border: 1px solid rgba(0, 255, 255, 0.2);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  animation: widget-enter 0.4s ease-out backwards;
  animation-delay: calc(var(--widget-index) * 0.08s);
}

@keyframes widget-enter {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
}

.widget:hover {
  border-color: var(--cyber-cyan, #00FFFF);
  box-shadow: 
    0 0 20px var(--cyber-cyan-glow),
    inset 0 0 30px rgba(0, 255, 255, 0.03);
}

/* Widget chrome */
.widget-chrome {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.chrome-corner {
  position: absolute;
  width: 12px;
  height: 12px;
}

.chrome-tl {
  top: 0; left: 0;
  border-top: 2px solid var(--cyber-cyan, #00FFFF);
  border-left: 2px solid var(--cyber-cyan, #00FFFF);
}

.chrome-tr {
  top: 0; right: 0;
  border-top: 2px solid var(--cyber-cyan, #00FFFF);
  border-right: 2px solid var(--cyber-cyan, #00FFFF);
}

.chrome-bl {
  bottom: 0; left: 0;
  border-bottom: 2px solid var(--cyber-magenta, #FF00FF);
  border-left: 2px solid var(--cyber-magenta, #FF00FF);
}

.chrome-br {
  bottom: 0; right: 0;
  border-bottom: 2px solid var(--cyber-magenta, #FF00FF);
  border-right: 2px solid var(--cyber-magenta, #FF00FF);
}

/* Widget header */
.widget-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.widget-id {
  font-family: var(--cyber-font-mono);
  font-size: 0.7rem;
  color: var(--cyber-text-dim);
  background: rgba(0, 255, 255, 0.1);
  padding: 0.15rem 0.4rem;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

/* Widget content */
.widget-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.widget-content :deep(h3) {
  font-family: var(--cyber-font-display);
  font-size: 1rem;
  font-weight: 600;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.widget-content :deep(.value) {
  font-family: var(--cyber-font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 15px var(--cyber-magenta-glow);
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.8rem;
}

/* Vibe modifiers */
.vibe-minimal .widget-chrome,
.vibe-minimal .widget-header {
  display: none;
}

.vibe-intense .chrome-corner {
  width: 20px;
  height: 20px;
  border-width: 3px;
}

.vibe-glitch .widget:nth-child(even) {
  animation: widget-enter 0.4s ease-out backwards, widget-glitch 4s ease-in-out infinite;
}

@keyframes widget-glitch {
  0%, 100% { filter: none; }
  20% { filter: hue-rotate(5deg); }
  40% { filter: hue-rotate(-5deg); }
}
</style>
