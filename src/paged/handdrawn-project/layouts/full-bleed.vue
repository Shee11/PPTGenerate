<!--
  full-bleed.vue - Handdrawn Full Bleed Layout
  
  Slots:
    - background: Background content/image
    - content: Overlay content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="full-bleed" :class="`vibe-${vibe}`">
      <!-- Background layer -->
      <div class="bleed-bg">
        <slot name="background">
          <div class="default-bg">
            <!-- Hand-drawn pattern -->
            <svg class="bg-pattern" viewBox="0 0 100 100">
              <defs>
                <pattern id="hand-dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                  <circle cx="10" cy="10" r="2" fill="currentColor"/>
                </pattern>
              </defs>
              <rect width="100" height="100" fill="url(#hand-dots)"/>
            </svg>
          </div>
        </slot>
      </div>
      
      <!-- Overlay content -->
      <div class="bleed-overlay">
        <div class="content-card">
          <!-- Tape decorations -->
          <div class="tape tape-left"></div>
          <div class="tape tape-right"></div>
          
          <div class="content-inner">
            <slot name="content">
              <span class="placeholder">✨ Content overlay</span>
            </slot>
          </div>
        </div>
      </div>
      
      <!-- Corner doodles -->
      <div class="doodle doodle-tl">🌸</div>
      <div class="doodle doodle-br">🌿</div>
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
  theme: 'handdrawn',
  vibe: 'cozy'
})
</script>

<style scoped>
.full-bleed {
  height: 100%;
  position: relative;
  overflow: hidden;
}

/* Background */
.bleed-bg {
  position: absolute;
  inset: 0;
}

.bleed-bg :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.default-bg {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--hand-pink-light) 0%, var(--hand-blue-light) 100%);
  position: relative;
}

.bg-pattern {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  color: var(--hand-text-light);
  opacity: 0.3;
}

/* Overlay */
.bleed-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.content-card {
  background: var(--hand-bg-cream);
  border: 3px solid var(--hand-text-light);
  border-radius: 8px;
  padding: 2rem;
  padding-top: 2.5rem;
  position: relative;
  box-shadow: 6px 6px 0 var(--hand-shadow-color);
  transform: rotate(-1deg);
  max-width: 70%;
}

/* Tape */
.tape {
  position: absolute;
  width: 50px;
  height: 20px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.tape-left {
  top: -10px;
  left: 20px;
  transform: rotate(-5deg);
}

.tape-right {
  top: -10px;
  right: 20px;
  transform: rotate(5deg);
}

/* Content */
.content-inner :deep(h1) {
  font-family: var(--hand-font-display);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--hand-text-dark);
  margin-bottom: 1rem;
  text-align: center;
}

.content-inner :deep(h2) {
  font-family: var(--hand-font-display);
  font-size: 1.6rem;
  color: var(--hand-text);
  margin-bottom: 0.75rem;
  text-align: center;
}

.content-inner :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 1.2rem;
  line-height: 1.7;
  color: var(--hand-text);
  text-align: center;
}

/* Doodles */
.doodle {
  position: absolute;
  font-size: 2.5rem;
  z-index: 10;
}

.doodle-tl {
  top: 1rem;
  left: 1rem;
}

.doodle-br {
  bottom: 1rem;
  right: 1rem;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 1rem;
}

/* Vibe modifiers */
.vibe-minimal .content-card {
  box-shadow: none;
  transform: none;
  border-width: 1px;
}

.vibe-minimal .tape,
.vibe-minimal .doodle {
  display: none;
}

.vibe-playful .content-card:hover {
  transform: rotate(0deg) scale(1.02);
}

.vibe-playful .doodle {
  animation: doodle-float 3s ease-in-out infinite;
}

@keyframes doodle-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.vibe-decorated .content-card::before {
  content: '★';
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 2rem;
  color: var(--hand-yellow-dark);
}
</style>
