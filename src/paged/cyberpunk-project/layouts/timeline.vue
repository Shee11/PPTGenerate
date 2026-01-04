<!--
  timeline.vue - Cyberpunk Timeline Layout
  
  Slots:
    - title: Timeline title
    - item1 through item6: Timeline items
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="timeline-layout" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="timeline-title">
        <span class="title-bracket">[</span>
        <slot name="title" />
        <span class="title-bracket">]</span>
        <div class="title-underline"></div>
      </div>
      
      <!-- Timeline track -->
      <div class="timeline-track">
        <div class="track-line">
          <div class="track-glow"></div>
        </div>
        
        <!-- Timeline items -->
        <div class="timeline-items">
          <div 
            v-for="i in 6" 
            :key="i" 
            class="timeline-item"
            :style="{ '--item-index': i }"
          >
            <div class="item-node">
              <div class="node-ring"></div>
              <div class="node-core"></div>
            </div>
            <div class="item-content">
              <slot :name="`item${i}`">
                <span class="placeholder">NODE_{{ i }}</span>
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
  theme: 'cyberpunk',
  vibe: 'balanced'
})
</script>

<style scoped>
.timeline-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Title */
.timeline-title {
  font-family: var(--cyber-font-display);
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 3px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
}

.title-bracket {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-magenta, #FF00FF);
  font-size: 2rem;
}

.title-underline {
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 60%;
  height: 2px;
  background: linear-gradient(90deg, var(--cyber-cyan, #00FFFF), transparent);
  box-shadow: 0 0 10px var(--cyber-cyan-glow);
}

/* Timeline track */
.timeline-track {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.track-line {
  position: absolute;
  left: 1.25rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(
    180deg,
    transparent,
    var(--cyber-cyan, #00FFFF) 10%,
    var(--cyber-cyan, #00FFFF) 90%,
    transparent
  );
}

.track-glow {
  position: absolute;
  inset: 0;
  background: inherit;
  filter: blur(6px);
  opacity: 0.5;
}

/* Timeline items */
.timeline-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding-left: 3.5rem;
}

.timeline-item {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  animation: item-enter 0.5s ease-out backwards;
  animation-delay: calc(var(--item-index) * 0.1s);
}

@keyframes item-enter {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
}

/* Node */
.item-node {
  position: absolute;
  left: -2.5rem;
  top: 0.25rem;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.node-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid var(--cyber-cyan, #00FFFF);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--cyber-cyan-glow);
}

.node-core {
  width: 8px;
  height: 8px;
  background: var(--cyber-cyan, #00FFFF);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--cyber-cyan-glow);
  animation: core-pulse 2s ease-in-out infinite;
  animation-delay: calc(var(--item-index) * 0.3s);
}

@keyframes core-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.7); opacity: 0.6; }
}

/* Item content */
.item-content {
  flex: 1;
  background: rgba(18, 18, 26, 0.8);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-left: 3px solid var(--cyber-cyan, #00FFFF);
  padding: 1rem 1.25rem;
}

.item-content:hover {
  border-color: var(--cyber-cyan, #00FFFF);
  box-shadow: 0 0 15px var(--cyber-cyan-glow);
}

.item-content :deep(h4) {
  font-family: var(--cyber-font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.item-content :deep(p) {
  font-family: var(--cyber-font-body);
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--cyber-text, #e0e0e0);
}

.item-content :deep(.date),
.item-content :deep(.year) {
  font-family: var(--cyber-font-mono);
  font-size: 0.8rem;
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 5px var(--cyber-magenta-glow);
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.8rem;
}

/* Vibe modifiers */
.vibe-minimal .track-glow,
.vibe-minimal .node-ring {
  display: none;
}

.vibe-intense .track-line {
  width: 3px;
}

.vibe-intense .node-ring {
  border-width: 3px;
}

.vibe-glitch .item-content:nth-child(odd) {
  animation: item-enter 0.5s ease-out backwards, glitch-item 6s ease-in-out infinite;
}

@keyframes glitch-item {
  0%, 100% { transform: translate(0); }
  30% { transform: translate(-2px, 0); }
  60% { transform: translate(2px, 0); }
}
</style>
