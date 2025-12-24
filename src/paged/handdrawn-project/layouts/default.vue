<!--
  default.vue - Handdrawn Default Layout
  
  Slots:
    - default: Main content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="default-layout" :class="`vibe-${vibe}`">
      <div class="content-paper">
        <!-- Paper decorations -->
        <div class="paper-corner corner-fold"></div>
        
        <div class="content-inner">
          <slot>
            <span class="placeholder">✏️ Add your content here...</span>
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
  theme: 'handdrawn',
  vibe: 'cozy'
})
</script>

<style scoped>
.default-layout {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.content-paper {
  width: 100%;
  height: 100%;
  position: relative;
  background: var(--hand-bg-cream);
  border: 2px solid var(--hand-text-light);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 4px 4px 0 var(--hand-shadow-color);
}

/* Corner fold */
.corner-fold {
  position: absolute;
  top: 0;
  right: 0;
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, transparent 50%, var(--hand-shadow-color) 50%);
  border-radius: 0 8px 0 0;
}

/* Content styles */
.content-inner :deep(h1) {
  font-family: var(--hand-font-display);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--hand-text-dark);
  margin: 0 0 1rem 0;
}

.content-inner :deep(h2) {
  font-family: var(--hand-font-display);
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--hand-text);
  margin: 0 0 0.75rem 0;
}

.content-inner :deep(h3) {
  font-family: var(--hand-font-display);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--hand-text);
  margin: 0 0 0.5rem 0;
}

.content-inner :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--hand-text);
  margin: 0 0 1rem 0;
}

.content-inner :deep(ul),
.content-inner :deep(ol) {
  font-family: var(--hand-font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--hand-text);
  margin: 0 0 1rem 0;
  padding-left: 1.5rem;
}

.content-inner :deep(li) {
  margin-bottom: 0.4rem;
}

.content-inner :deep(code) {
  font-family: 'Fira Code', monospace;
  background: var(--hand-pink-light);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  font-size: 0.9em;
}

.content-inner :deep(pre) {
  background: var(--hand-text-dark);
  color: var(--hand-bg-cream);
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1rem 0;
}

.content-inner :deep(blockquote) {
  border-left: 4px solid var(--hand-pink);
  padding-left: 1rem;
  margin: 1rem 0;
  font-style: italic;
  color: var(--hand-text);
}

.content-inner :deep(strong) {
  font-weight: 700;
  color: var(--hand-text-dark);
}

.content-inner :deep(em) {
  font-style: italic;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 1rem;
}

/* Vibe modifiers */
.vibe-minimal .content-paper {
  box-shadow: none;
  border-width: 1px;
}

.vibe-minimal .corner-fold {
  display: none;
}

.vibe-playful .content-paper:hover {
  transform: rotate(-0.5deg);
}

.vibe-decorated .content-paper::before {
  content: '✨';
  position: absolute;
  top: 1rem;
  left: 1rem;
  font-size: 1.2rem;
}

.vibe-decorated .content-paper::after {
  content: '✨';
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  font-size: 1.2rem;
}
</style>
