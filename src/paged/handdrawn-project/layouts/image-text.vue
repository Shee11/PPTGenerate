<!--
  image-text.vue - Handdrawn Image + Text Layout
  
  Slots:
    - image: Image content
    - content: Text content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="image-text" :class="[`vibe-${vibe}`, `layout-${imagePosition}`]">
      <!-- Image side -->
      <div class="image-side">
        <div class="image-frame">
          <!-- Photo corners -->
          <div class="photo-corner corner-tl"></div>
          <div class="photo-corner corner-tr"></div>
          <div class="photo-corner corner-bl"></div>
          <div class="photo-corner corner-br"></div>
          
          <div class="image-wrapper">
            <slot name="image">
              <div class="image-placeholder">
                <span class="placeholder-icon">🖼️</span>
                <span class="placeholder-text">Image here</span>
              </div>
            </slot>
          </div>
          
          <!-- Caption tape -->
          <div class="image-caption-tape"></div>
        </div>
      </div>
      
      <!-- Text side -->
      <div class="text-side">
        <div class="text-paper">
          <!-- Notebook holes -->
          <div class="notebook-holes">
            <div v-for="i in 3" :key="i" class="hole"></div>
          </div>
          
          <div class="text-content">
            <slot name="content">
              <span class="placeholder">✏️ Your content here...</span>
            </slot>
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
  imagePosition?: 'left' | 'right'
}>(), {
  theme: 'handdrawn',
  vibe: 'cozy',
  imagePosition: 'left'
})
</script>

<style scoped>
.image-text {
  height: 100%;
  display: flex;
  gap: 2rem;
}

.layout-right {
  flex-direction: row-reverse;
}

/* Image side */
.image-side {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-frame {
  position: relative;
  padding: 1rem;
  background: var(--hand-bg-cream);
  border: 3px solid var(--hand-text-light);
  box-shadow: 5px 5px 0 var(--hand-shadow-color);
  transform: rotate(-2deg);
}

/* Photo corners */
.photo-corner {
  position: absolute;
  width: 20px;
  height: 20px;
  border: 3px solid var(--hand-text-light);
}

.corner-tl {
  top: -3px;
  left: -3px;
  border-right: none;
  border-bottom: none;
}

.corner-tr {
  top: -3px;
  right: -3px;
  border-left: none;
  border-bottom: none;
}

.corner-bl {
  bottom: -3px;
  left: -3px;
  border-right: none;
  border-top: none;
}

.corner-br {
  bottom: -3px;
  right: -3px;
  border-left: none;
  border-top: none;
}

.image-wrapper :deep(img) {
  max-width: 100%;
  max-height: 350px;
  display: block;
}

.image-placeholder {
  width: 280px;
  height: 200px;
  background: var(--hand-pink-light);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.placeholder-icon {
  font-size: 3rem;
}

.placeholder-text {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
}

/* Caption tape */
.image-caption-tape {
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%) rotate(2deg);
  width: 80px;
  height: 20px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

/* Text side */
.text-side {
  flex: 1;
  display: flex;
  align-items: center;
}

.text-paper {
  position: relative;
  background: var(--hand-bg-cream);
  border: 2px solid var(--hand-blue);
  border-radius: 8px;
  padding: 1.5rem;
  padding-left: 2.5rem;
  box-shadow: 4px 4px 0 var(--hand-shadow-color);
  transform: rotate(1deg);
  background-image: repeating-linear-gradient(
    transparent,
    transparent 28px,
    var(--hand-blue-light) 28px,
    var(--hand-blue-light) 29px
  );
}

/* Notebook holes */
.notebook-holes {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.hole {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: white;
  border: 2px solid var(--hand-text-light);
}

/* Text content */
.text-content :deep(h1) {
  font-family: var(--hand-font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--hand-text-dark);
  margin: 0 0 0.75rem 0;
}

.text-content :deep(h2) {
  font-family: var(--hand-font-display);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--hand-text);
  margin: 0 0 0.5rem 0;
}

.text-content :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 1rem;
  line-height: 1.8;
  color: var(--hand-text);
  margin: 0 0 0.75rem 0;
}

.text-content :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}

.text-content :deep(li) {
  font-family: var(--hand-font-body);
  font-size: 0.95rem;
  line-height: 1.8;
  color: var(--hand-text);
  padding-left: 1.5rem;
  position: relative;
}

.text-content :deep(li::before) {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--hand-green);
  font-weight: bold;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 0.9rem;
}

/* Vibe modifiers */
.vibe-minimal .image-frame {
  border: 1px solid var(--hand-text-light);
  box-shadow: none;
  transform: none;
}

.vibe-minimal .photo-corner,
.vibe-minimal .image-caption-tape,
.vibe-minimal .notebook-holes {
  display: none;
}

.vibe-minimal .text-paper {
  border-width: 1px;
  box-shadow: none;
  transform: none;
  background-image: none;
  padding-left: 1.5rem;
}

.vibe-playful .image-frame:hover {
  transform: rotate(0deg) scale(1.02);
}

.vibe-decorated .image-frame::before {
  content: '📷';
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.5rem;
}
</style>
