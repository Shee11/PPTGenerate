<!--
  hero-split.vue - Cyberpunk Hero Split Layout
  
  Props:
    - theme, vibe, header, footer (passed to SlideShell)
  
  Slots:
    - left: Left panel content
    - right: Right panel content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="hero-split" :class="`vibe-${vibe}`">
      <!-- Divider line -->
      <div class="split-divider">
        <div class="divider-glow"></div>
      </div>
      
      <!-- Left panel -->
      <div class="panel panel-left">
        <div class="panel-content">
          <slot name="left">
            <div class="placeholder">// LEFT_PANEL</div>
          </slot>
        </div>
        <div class="panel-decoration panel-dec-left"></div>
      </div>
      
      <!-- Right panel -->
      <div class="panel panel-right">
        <div class="panel-content">
          <slot name="right">
            <div class="placeholder">// RIGHT_PANEL</div>
          </slot>
        </div>
        <div class="panel-decoration panel-dec-right"></div>
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
.hero-split {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  position: relative;
}

/* Divider line */
.split-divider {
  position: absolute;
  left: 50%;
  top: 10%;
  bottom: 10%;
  width: 2px;
  transform: translateX(-50%);
  background: linear-gradient(
    180deg,
    transparent,
    var(--cyber-cyan, #00FFFF) 20%,
    var(--cyber-magenta, #FF00FF) 80%,
    transparent
  );
  z-index: 10;
}

.divider-glow {
  position: absolute;
  inset: 0;
  background: inherit;
  filter: blur(8px);
  opacity: 0.6;
}

/* Panels */
.panel {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2rem;
}

.panel-content {
  position: relative;
  z-index: 5;
}

.panel-content :deep(h1) {
  font-family: var(--cyber-font-display);
  font-size: 3rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-shadow: 
    0 0 10px var(--cyber-cyan-glow, rgba(0, 255, 255, 0.5)),
    0 0 30px var(--cyber-cyan-glow, rgba(0, 255, 255, 0.3));
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.panel-content :deep(h2) {
  font-family: var(--cyber-font-display);
  font-size: 2rem;
  font-weight: 600;
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 10px var(--cyber-magenta-glow, rgba(255, 0, 255, 0.5));
  margin-bottom: 0.75rem;
}

.panel-content :deep(p) {
  font-family: var(--cyber-font-body);
  font-size: 1.25rem;
  line-height: 1.7;
  color: var(--cyber-text, #e0e0e0);
  margin-bottom: 0.75rem;
}

.panel-content :deep(ul) {
  list-style: none;
  padding: 0;
}

.panel-content :deep(li) {
  font-family: var(--cyber-font-body);
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--cyber-text, #e0e0e0);
  padding-left: 1.5rem;
  position: relative;
  margin-bottom: 0.5rem;
}

.panel-content :deep(li::before) {
  content: '>';
  position: absolute;
  left: 0;
  color: var(--cyber-cyan, #00FFFF);
  font-family: var(--cyber-font-mono);
  text-shadow: 0 0 5px var(--cyber-cyan-glow);
}

/* Panel decorations */
.panel-decoration {
  position: absolute;
  width: 60%;
  height: 60%;
  border: 1px solid;
  opacity: 0.15;
  pointer-events: none;
}

.panel-dec-left {
  top: 10%;
  left: -5%;
  border-color: var(--cyber-cyan, #00FFFF);
  box-shadow: 0 0 20px var(--cyber-cyan-glow);
}

.panel-dec-right {
  bottom: 10%;
  right: -5%;
  border-color: var(--cyber-magenta, #FF00FF);
  box-shadow: 0 0 20px var(--cyber-magenta-glow);
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.9rem;
}

/* Vibe modifiers */
.vibe-minimal .split-divider {
  opacity: 0.3;
}

.vibe-minimal .panel-decoration {
  display: none;
}

.vibe-intense .split-divider {
  width: 4px;
}

.vibe-intense .divider-glow {
  filter: blur(15px);
}

.vibe-glitch .panel-content {
  animation: panel-glitch 3s ease-in-out infinite;
}

@keyframes panel-glitch {
  0%, 100% { transform: translate(0); }
  10% { transform: translate(-2px, 0); }
  20% { transform: translate(2px, 0); }
  30% { transform: translate(0); }
}
</style>
