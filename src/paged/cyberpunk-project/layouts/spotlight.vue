<!--
  spotlight.vue - Cyberpunk Spotlight Layout
  
  Slots:
    - badge: Category/label badge
    - heading: Main spotlight heading
    - description: Supporting description
    - visual: Image/visual element
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="spotlight-layout" :class="`vibe-${vibe}`">
      <!-- Background effects -->
      <div class="spotlight-bg">
        <div class="bg-beam bg-beam-1"></div>
        <div class="bg-beam bg-beam-2"></div>
      </div>
      
      <!-- Content area -->
      <div class="spotlight-content">
        <!-- Badge -->
        <div v-if="$slots.badge" class="spotlight-badge">
          <span class="badge-brackets">[</span>
          <slot name="badge" />
          <span class="badge-brackets">]</span>
        </div>
        
        <!-- Heading -->
        <div class="spotlight-heading">
          <slot name="heading">
            <span class="placeholder">// MAIN_HEADING</span>
          </slot>
        </div>
        
        <!-- Description -->
        <div v-if="$slots.description" class="spotlight-description">
          <slot name="description" />
        </div>
      </div>
      
      <!-- Visual area -->
      <div v-if="$slots.visual" class="spotlight-visual">
        <div class="visual-frame">
          <div class="frame-line frame-top"></div>
          <div class="frame-line frame-right"></div>
          <div class="frame-line frame-bottom"></div>
          <div class="frame-line frame-left"></div>
        </div>
        <div class="visual-content">
          <slot name="visual" />
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
.spotlight-layout {
  height: 100%;
  display: flex;
  align-items: center;
  gap: 3rem;
  position: relative;
}

/* Background beams */
.spotlight-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.bg-beam {
  position: absolute;
  width: 150%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--cyber-cyan, #00FFFF), transparent);
  opacity: 0.2;
}

.bg-beam-1 {
  top: 30%;
  left: -25%;
  transform: rotate(-5deg);
  animation: beam-move 8s ease-in-out infinite;
}

.bg-beam-2 {
  bottom: 25%;
  left: -25%;
  transform: rotate(3deg);
  background: linear-gradient(90deg, transparent, var(--cyber-magenta, #FF00FF), transparent);
  animation: beam-move 10s ease-in-out infinite reverse;
}

@keyframes beam-move {
  0%, 100% { transform: translateY(0) rotate(-5deg); }
  50% { transform: translateY(20px) rotate(-5deg); }
}

/* Content */
.spotlight-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  z-index: 5;
}

/* Badge */
.spotlight-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--cyber-font-mono);
  font-size: 0.9rem;
  color: var(--cyber-magenta, #FF00FF);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.badge-brackets {
  color: var(--cyber-cyan, #00FFFF);
  text-shadow: 0 0 5px var(--cyber-cyan-glow);
}

/* Heading */
.spotlight-heading {
  font-family: var(--cyber-font-display);
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.1;
  color: var(--cyber-cyan, #00FFFF);
  text-shadow: 
    0 0 20px var(--cyber-cyan-glow),
    0 0 40px var(--cyber-cyan-glow);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.spotlight-heading :deep(span.highlight) {
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 
    0 0 20px var(--cyber-magenta-glow),
    0 0 40px var(--cyber-magenta-glow);
}

/* Description */
.spotlight-description {
  font-family: var(--cyber-font-body);
  font-size: 1.25rem;
  line-height: 1.7;
  color: var(--cyber-text, #e0e0e0);
  max-width: 600px;
}

/* Visual area */
.spotlight-visual {
  flex: 0.6;
  position: relative;
  aspect-ratio: 1;
  max-height: 80%;
  z-index: 5;
}

.visual-frame {
  position: absolute;
  inset: -10px;
  pointer-events: none;
}

.frame-line {
  position: absolute;
  background: var(--cyber-cyan, #00FFFF);
  box-shadow: 0 0 10px var(--cyber-cyan-glow);
}

.frame-top {
  top: 0;
  left: 20%;
  right: 0;
  height: 2px;
}

.frame-right {
  top: 0;
  right: 0;
  bottom: 20%;
  width: 2px;
}

.frame-bottom {
  bottom: 0;
  left: 0;
  right: 20%;
  height: 2px;
  background: var(--cyber-magenta, #FF00FF);
  box-shadow: 0 0 10px var(--cyber-magenta-glow);
}

.frame-left {
  top: 20%;
  left: 0;
  bottom: 0;
  width: 2px;
  background: var(--cyber-magenta, #FF00FF);
  box-shadow: 0 0 10px var(--cyber-magenta-glow);
}

.visual-content {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.visual-content :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(0.8) contrast(1.1);
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 1rem;
}

/* Vibe modifiers */
.vibe-minimal .spotlight-bg,
.vibe-minimal .visual-frame {
  display: none;
}

.vibe-intense .spotlight-heading {
  animation: text-glow 2s ease-in-out infinite alternate;
}

@keyframes text-glow {
  from { text-shadow: 0 0 20px var(--cyber-cyan-glow), 0 0 40px var(--cyber-cyan-glow); }
  to { text-shadow: 0 0 30px var(--cyber-cyan-glow), 0 0 60px var(--cyber-cyan-glow); }
}

.vibe-glitch .spotlight-heading {
  animation: heading-glitch 4s ease-in-out infinite;
}

@keyframes heading-glitch {
  0%, 100% { transform: translate(0); filter: none; }
  10% { transform: translate(-3px, 0); filter: hue-rotate(10deg); }
  20% { transform: translate(3px, 0); }
  30% { transform: translate(0); filter: none; }
}
</style>
