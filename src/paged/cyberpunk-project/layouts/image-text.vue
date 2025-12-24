<!--
  image-text.vue - Cyberpunk Image + Text Layout
  
  Slots:
    - image: Image/visual content
    - content: Text content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="image-text-layout" :class="`vibe-${vibe}`">
      <!-- Image area -->
      <div class="image-area">
        <div class="image-frame">
          <div class="frame-edge frame-top"></div>
          <div class="frame-edge frame-left"></div>
          <div class="frame-corner"></div>
        </div>
        <div class="image-container">
          <slot name="image">
            <div class="placeholder-image">
              <div class="placeholder-grid"></div>
              <span class="placeholder-text">// IMAGE</span>
            </div>
          </slot>
        </div>
        <div class="image-scanlines"></div>
      </div>
      
      <!-- Text area -->
      <div class="text-area">
        <div class="text-decorator">
          <span class="decorator-line"></span>
          <span class="decorator-dot"></span>
        </div>
        <div class="text-content">
          <slot name="content">
            <span class="placeholder">// CONTENT_DATA</span>
          </slot>
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
.image-text-layout {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2.5rem;
  align-items: center;
}

/* Image area */
.image-area {
  position: relative;
  aspect-ratio: 4/3;
  max-height: 100%;
}

/* Image frame */
.image-frame {
  position: absolute;
  inset: -8px;
  pointer-events: none;
  z-index: 10;
}

.frame-edge {
  position: absolute;
  background: var(--cyber-cyan, #00FFFF);
  box-shadow: 0 0 15px var(--cyber-cyan-glow);
}

.frame-top {
  top: 0;
  left: 20px;
  right: 0;
  height: 2px;
}

.frame-left {
  top: 0;
  left: 0;
  bottom: 20px;
  width: 2px;
}

.frame-corner {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 30px;
  height: 30px;
  border-bottom: 2px solid var(--cyber-magenta, #FF00FF);
  border-right: 2px solid var(--cyber-magenta, #FF00FF);
  box-shadow: 2px 2px 15px var(--cyber-magenta-glow);
}

/* Image container */
.image-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: rgba(18, 18, 26, 0.9);
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.image-container :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(0.8) contrast(1.1);
}

.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.05), rgba(255, 0, 255, 0.05));
}

.placeholder-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 30px 30px;
}

.placeholder-text {
  font-family: var(--cyber-font-mono);
  font-size: 1rem;
  color: var(--cyber-text-dim);
  z-index: 5;
}

/* Scanlines overlay */
.image-scanlines {
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

/* Text area */
.text-area {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.text-decorator {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.decorator-line {
  width: 40px;
  height: 2px;
  background: var(--cyber-magenta, #FF00FF);
  box-shadow: 0 0 10px var(--cyber-magenta-glow);
}

.decorator-dot {
  width: 8px;
  height: 8px;
  background: var(--cyber-magenta, #FF00FF);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--cyber-magenta-glow);
}

/* Text content */
.text-content :deep(h2) {
  font-family: var(--cyber-font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 0 0 15px var(--cyber-cyan-glow);
  margin-bottom: 1rem;
}

.text-content :deep(p) {
  font-family: var(--cyber-font-body);
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--cyber-text, #e0e0e0);
  margin-bottom: 0.75rem;
}

.text-content :deep(ul) {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

.text-content :deep(li) {
  padding-left: 1.5rem;
  position: relative;
  margin-bottom: 0.5rem;
  font-family: var(--cyber-font-body);
  font-size: 1rem;
  color: var(--cyber-text, #e0e0e0);
}

.text-content :deep(li::before) {
  content: '//';
  position: absolute;
  left: 0;
  color: var(--cyber-cyan, #00FFFF);
  font-family: var(--cyber-font-mono);
  font-size: 0.8rem;
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.9rem;
}

/* Vibe modifiers */
.vibe-minimal .image-frame,
.vibe-minimal .image-scanlines,
.vibe-minimal .text-decorator {
  display: none;
}

.vibe-intense .image-frame .frame-edge,
.vibe-intense .frame-corner {
  border-width: 3px;
}

.vibe-intense .decorator-dot {
  animation: dot-glow 1.5s ease-in-out infinite alternate;
}

@keyframes dot-glow {
  from { box-shadow: 0 0 10px var(--cyber-magenta-glow); }
  to { box-shadow: 0 0 20px var(--cyber-magenta-glow), 0 0 30px var(--cyber-magenta-glow); }
}

.vibe-glitch .image-container {
  animation: image-glitch 5s ease-in-out infinite;
}

@keyframes image-glitch {
  0%, 100% { transform: translate(0); filter: none; }
  15% { transform: translate(-2px, 0); filter: hue-rotate(5deg); }
  30% { transform: translate(2px, 0); }
  45% { transform: translate(0); filter: none; }
}
</style>
