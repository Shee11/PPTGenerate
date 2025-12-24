<!--
  SlideShell.vue - Handdrawn Base Wrapper Component
  
  Provides:
    - Paper/notebook background
    - Sketchy border frame
    - Doodle decorations
    - Friendly pastel aesthetic
  
  Props:
    - theme: Theme name (default: 'handdrawn')
    - vibe: Visual intensity (playful, cozy, minimal, decorated)
    - header: Optional header text
    - footer: Optional footer text
-->
<template>
  <div 
    class="slide-shell"
    :class="[`vibe-${vibe}`, themeClass]"
  >
    <!-- Paper background -->
    <div class="paper-layer">
      <div class="paper-texture"></div>
      <div v-if="vibe !== 'minimal'" class="notebook-lines"></div>
    </div>
    
    <!-- Corner doodles -->
    <div v-if="vibe === 'decorated' || vibe === 'playful'" class="corner-doodles">
      <span class="doodle doodle-tl">✿</span>
      <span class="doodle doodle-tr">★</span>
      <span class="doodle doodle-bl">♪</span>
      <span class="doodle doodle-br">♥</span>
    </div>
    
    <!-- Sketchy frame -->
    <div class="sketchy-frame">
      <svg class="frame-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <path class="frame-path" d="M2,2 Q1,50 2,98 Q50,99 98,98 Q99,50 98,2 Q50,1 2,2" fill="none"/>
      </svg>
    </div>
    
    <!-- Header -->
    <header v-if="header" class="shell-header">
      <span class="header-text">{{ header }}</span>
      <span class="header-doodle">~</span>
    </header>
    
    <!-- Main content -->
    <main class="shell-content">
      <slot />
    </main>
    
    <!-- Footer -->
    <footer v-if="footer" class="shell-footer">
      <span class="footer-squiggle">〰</span>
      <span class="footer-text">{{ footer }}</span>
    </footer>
    
    <!-- Tape decoration -->
    <div v-if="vibe === 'decorated'" class="tape-decorations">
      <div class="tape tape-top"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  theme?: string
  vibe?: string
  header?: string
  footer?: string
}>(), {
  theme: 'handdrawn',
  vibe: 'cozy'
})

const themeClass = computed(() => `theme-${props.theme}`)
</script>

<style scoped>
@import '../styles/index.css';

.slide-shell {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 2.5rem;
  box-sizing: border-box;
  overflow: hidden;
  background: var(--hand-bg);
}

/* Paper background layer */
.paper-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.paper-texture {
  position: absolute;
  inset: 0;
  background: var(--hand-bg-paper);
  opacity: 0.7;
}

.notebook-lines {
  position: absolute;
  inset: 0;
  background-image: 
    repeating-linear-gradient(
      transparent,
      transparent 29px,
      rgba(168, 216, 234, 0.25) 29px,
      rgba(168, 216, 234, 0.25) 30px
    );
  background-position: 0 15px;
}

/* Sketchy frame */
.sketchy-frame {
  position: absolute;
  inset: 12px;
  pointer-events: none;
}

.frame-svg {
  width: 100%;
  height: 100%;
}

.frame-path {
  stroke: var(--hand-text-light);
  stroke-width: 0.3;
  stroke-linecap: round;
  opacity: 0.4;
}

/* Corner doodles */
.corner-doodles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 10;
}

.doodle {
  position: absolute;
  font-size: 1.5rem;
  opacity: 0.4;
  animation: wobble 4s ease-in-out infinite;
}

.doodle-tl { top: 1rem; left: 1rem; color: var(--hand-pink); }
.doodle-tr { top: 1rem; right: 1rem; color: var(--hand-yellow-dark); animation-delay: 0.5s; }
.doodle-bl { bottom: 1rem; left: 1rem; color: var(--hand-blue-dark); animation-delay: 1s; }
.doodle-br { bottom: 1rem; right: 1rem; color: var(--hand-pink); animation-delay: 1.5s; }

@keyframes wobble {
  0%, 100% { transform: rotate(-5deg) scale(1); }
  50% { transform: rotate(5deg) scale(1.1); }
}

/* Header */
.shell-header {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px dashed var(--hand-pink-light);
}

.header-text {
  font-family: var(--hand-font-handwriting);
  font-size: 1rem;
  color: var(--hand-text-light);
}

.header-doodle {
  font-family: var(--hand-font-display);
  color: var(--hand-pink);
}

/* Main content */
.shell-content {
  position: relative;
  z-index: 5;
  height: calc(100% - 2rem);
}

/* Footer */
.shell-footer {
  position: absolute;
  bottom: 1rem;
  left: 2.5rem;
  right: 2.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.5rem;
  border-top: 2px dashed var(--hand-blue-light);
}

.footer-squiggle {
  color: var(--hand-blue);
}

.footer-text {
  font-family: var(--hand-font-handwriting);
  font-size: 0.85rem;
  color: var(--hand-text-light);
}

/* Tape decorations */
.tape-decorations {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 15;
}

.tape {
  position: absolute;
  width: 70px;
  height: 22px;
  background: rgba(255, 234, 167, 0.7);
  border: 1px solid rgba(0,0,0,0.05);
}

.tape-top {
  top: 5px;
  left: 50%;
  transform: translateX(-50%) rotate(-2deg);
}

/* Vibe modifiers */
.vibe-minimal .corner-doodles,
.vibe-minimal .sketchy-frame,
.vibe-minimal .notebook-lines {
  display: none;
}

.vibe-minimal {
  background: var(--hand-bg);
}

.vibe-cozy .doodle {
  opacity: 0.3;
}

.vibe-playful .doodle {
  opacity: 0.6;
  font-size: 1.8rem;
}

.vibe-decorated .corner-doodles .doodle {
  opacity: 0.7;
  font-size: 2rem;
}
</style>
