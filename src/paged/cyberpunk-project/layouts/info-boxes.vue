<!--
  info-boxes.vue - Cyberpunk Info Boxes Layout
  
  Slots:
    - title: Section title
    - box1_title, box1_content, box2_title, box2_content
    - box3_title, box3_content, box4_title, box4_content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="info-boxes" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="section-title">
        <span class="title-prefix">&lt;</span>
        <slot name="title" />
        <span class="title-suffix">/&gt;</span>
      </div>
      
      <!-- Boxes grid -->
      <div class="boxes-grid">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="info-box"
          :class="`box-${i}`"
          :style="{ '--box-index': i }"
        >
          <div class="box-glow"></div>
          <div class="box-header">
            <span class="box-number">{{ String(i).padStart(2, '0') }}</span>
            <div class="box-title">
              <slot :name="`box${i}_title`">
                <span class="placeholder">SYSTEM_{{ i }}</span>
              </slot>
            </div>
          </div>
          <div class="box-content">
            <slot :name="`box${i}_content`">
              <span class="placeholder">// Data pending...</span>
            </slot>
          </div>
          <div class="box-status">
            <span class="status-dot"></span>
            <span class="status-text">ONLINE</span>
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
.info-boxes {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Title */
.section-title {
  font-family: var(--cyber-font-display);
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 3px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.title-prefix,
.title-suffix {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 10px var(--cyber-magenta-glow);
}

/* Boxes grid */
.boxes-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.info-box {
  position: relative;
  background: rgba(18, 18, 26, 0.9);
  border: 1px solid rgba(0, 255, 255, 0.2);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  animation: box-enter 0.5s ease-out backwards;
  animation-delay: calc(var(--box-index) * 0.1s);
  overflow: hidden;
}

@keyframes box-enter {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
}

/* Box glow effect */
.box-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--box-accent), transparent);
  box-shadow: 0 0 20px var(--box-accent);
}

/* Box colors */
.box-1 { --box-accent: var(--cyber-cyan, #00FFFF); }
.box-2 { --box-accent: var(--cyber-magenta, #FF00FF); }
.box-3 { --box-accent: var(--cyber-yellow, #FFFF00); }
.box-4 { --box-accent: var(--cyber-pink, #FF0080); }

/* Box header */
.box-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.box-number {
  font-family: var(--cyber-font-mono);
  font-size: 0.8rem;
  color: var(--box-accent);
  background: rgba(0, 255, 255, 0.1);
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--box-accent);
}

.box-title {
  font-family: var(--cyber-font-display);
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--box-accent);
  text-shadow: 0 0 10px currentColor;
  text-transform: uppercase;
}

/* Box content */
.box-content {
  flex: 1;
  font-family: var(--cyber-font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--cyber-text, #e0e0e0);
}

.box-content :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0;
}

.box-content :deep(li) {
  padding-left: 1.25rem;
  position: relative;
  margin-bottom: 0.4rem;
}

.box-content :deep(li::before) {
  content: '//';
  position: absolute;
  left: 0;
  color: var(--box-accent);
  font-family: var(--cyber-font-mono);
  font-size: 0.8rem;
}

/* Box status */
.box-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--cyber-font-mono);
  font-size: 0.7rem;
  color: var(--cyber-green, #00FF41);
}

.status-dot {
  width: 6px;
  height: 6px;
  background: var(--cyber-green, #00FF41);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--cyber-green-glow);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.8rem;
}

/* Vibe modifiers */
.vibe-minimal .box-glow,
.vibe-minimal .box-status {
  display: none;
}

.vibe-intense .box-glow {
  height: 4px;
}

.vibe-intense .info-box {
  border-width: 2px;
}

.vibe-glitch .info-box:nth-child(even) {
  animation: box-enter 0.5s ease-out backwards, glitch-box 5s ease-in-out infinite;
}

@keyframes glitch-box {
  0%, 100% { transform: translate(0); filter: none; }
  20% { transform: translate(-2px, 0); }
  40% { transform: translate(2px, 0); filter: hue-rotate(10deg); }
  60% { transform: translate(0); }
}
</style>
