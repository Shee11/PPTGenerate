<!--
  full-bleed.vue - Cyberpunk Full Bleed Layout
  
  Slots:
    - background: Full-bleed background
    - overlay: Content overlay on top
    - caption: Optional bottom caption
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="full-bleed-layout" :class="`vibe-${vibe}`">
      <!-- Background -->
      <div class="bleed-background">
        <slot name="background">
          <div class="placeholder-bg">
            <div class="grid-pattern"></div>
          </div>
        </slot>
        <div class="bg-overlay"></div>
        <div class="scanline-overlay"></div>
      </div>
      
      <!-- Main overlay content -->
      <div v-if="$slots.overlay" class="bleed-overlay">
        <div class="overlay-frame">
          <div class="frame-corner frame-tl"></div>
          <div class="frame-corner frame-tr"></div>
          <div class="frame-corner frame-bl"></div>
          <div class="frame-corner frame-br"></div>
        </div>
        <div class="overlay-content">
          <slot name="overlay" />
        </div>
      </div>
      
      <!-- Caption -->
      <div v-if="$slots.caption" class="bleed-caption">
        <div class="caption-line"></div>
        <div class="caption-content">
          <slot name="caption" />
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
.full-bleed-layout {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Background */
.bleed-background {
  position: absolute;
  inset: 0;
}

.bleed-background :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(0.7) contrast(1.2);
}

.placeholder-bg {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0a0a12 0%, #1a1a2e 50%, #0a0a12 100%);
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

.bg-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(10, 10, 18, 0.7) 0%,
    rgba(10, 10, 18, 0.3) 50%,
    rgba(10, 10, 18, 0.8) 100%
  );
}

.scanline-overlay {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 0, 0, 0.1) 2px,
    rgba(0, 0, 0, 0.1) 4px
  );
  pointer-events: none;
}

/* Overlay content */
.bleed-overlay {
  position: relative;
  z-index: 10;
  max-width: 70%;
  padding: 2.5rem 3rem;
  background: rgba(10, 10, 18, 0.85);
  border: 1px solid rgba(0, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.overlay-frame {
  position: absolute;
  inset: -5px;
  pointer-events: none;
}

.frame-corner {
  position: absolute;
  width: 20px;
  height: 20px;
}

.frame-tl {
  top: 0; left: 0;
  border-top: 3px solid var(--cyber-cyan, #00FFFF);
  border-left: 3px solid var(--cyber-cyan, #00FFFF);
  box-shadow: -3px -3px 10px var(--cyber-cyan-glow);
}

.frame-tr {
  top: 0; right: 0;
  border-top: 3px solid var(--cyber-cyan, #00FFFF);
  border-right: 3px solid var(--cyber-cyan, #00FFFF);
  box-shadow: 3px -3px 10px var(--cyber-cyan-glow);
}

.frame-bl {
  bottom: 0; left: 0;
  border-bottom: 3px solid var(--cyber-magenta, #FF00FF);
  border-left: 3px solid var(--cyber-magenta, #FF00FF);
  box-shadow: -3px 3px 10px var(--cyber-magenta-glow);
}

.frame-br {
  bottom: 0; right: 0;
  border-bottom: 3px solid var(--cyber-magenta, #FF00FF);
  border-right: 3px solid var(--cyber-magenta, #FF00FF);
  box-shadow: 3px 3px 10px var(--cyber-magenta-glow);
}

.overlay-content {
  text-align: center;
}

.overlay-content :deep(h1) {
  font-family: var(--cyber-font-display);
  font-size: 3rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-shadow: 0 0 30px var(--cyber-cyan-glow);
  text-transform: uppercase;
  letter-spacing: 4px;
  margin-bottom: 1rem;
}

.overlay-content :deep(p) {
  font-family: var(--cyber-font-body);
  font-size: 1.25rem;
  line-height: 1.7;
  color: var(--cyber-text, #e0e0e0);
}

/* Caption */
.bleed-caption {
  position: absolute;
  bottom: 2rem;
  left: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 10;
}

.caption-line {
  width: 60px;
  height: 2px;
  background: var(--cyber-magenta, #FF00FF);
  box-shadow: 0 0 10px var(--cyber-magenta-glow);
}

.caption-content {
  font-family: var(--cyber-font-mono);
  font-size: 0.9rem;
  color: var(--cyber-text, #e0e0e0);
  letter-spacing: 1px;
}

/* Vibe modifiers */
.vibe-minimal .overlay-frame,
.vibe-minimal .scanline-overlay {
  display: none;
}

.vibe-minimal .bleed-overlay {
  background: rgba(10, 10, 18, 0.9);
}

.vibe-intense .frame-corner {
  width: 30px;
  height: 30px;
  border-width: 4px;
}

.vibe-intense .overlay-content :deep(h1) {
  animation: intense-glow 2s ease-in-out infinite alternate;
}

@keyframes intense-glow {
  from { text-shadow: 0 0 30px var(--cyber-cyan-glow); }
  to { text-shadow: 0 0 50px var(--cyber-cyan-glow), 0 0 80px var(--cyber-cyan-glow); }
}

.vibe-glitch .bleed-overlay {
  animation: overlay-glitch 5s ease-in-out infinite;
}

@keyframes overlay-glitch {
  0%, 100% { transform: translate(0); }
  10% { transform: translate(-3px, 0); }
  20% { transform: translate(3px, 0); }
  30% { transform: translate(0); }
}
</style>
