<!--
  spotlight.vue - Handdrawn Spotlight Layout
  
  Slots:
    - title: Spotlight title
    - main: Main featured content
    - caption: Caption or description
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="spotlight" :class="`vibe-${vibe}`">
      <!-- Spotlight frame -->
      <div class="spotlight-frame">
        <!-- Corner decorations -->
        <div class="corner corner-tl">✿</div>
        <div class="corner corner-tr">✿</div>
        <div class="corner corner-bl">✿</div>
        <div class="corner corner-br">✿</div>
        
        <!-- Title -->
        <div v-if="$slots.title" class="spotlight-title">
          <div class="title-ribbon">
            <slot name="title" />
          </div>
        </div>
        
        <!-- Main content -->
        <div class="spotlight-main">
          <div class="main-paper">
            <slot name="main">
              <span class="placeholder">✨ Featured content</span>
            </slot>
          </div>
        </div>
        
        <!-- Caption -->
        <div v-if="$slots.caption" class="spotlight-caption">
          <div class="caption-label">
            <span class="label-icon">📝</span>
            <slot name="caption" />
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
  theme: 'handdrawn',
  vibe: 'cozy'
})
</script>

<style scoped>
.spotlight {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

/* Frame */
.spotlight-frame {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  border: 4px solid var(--hand-text-light);
  border-radius: 20px;
  padding: 2rem;
  background: var(--hand-bg-cream);
}

/* Corners */
.corner {
  position: absolute;
  font-size: 1.5rem;
  color: var(--hand-pink);
}

.corner-tl { top: -12px; left: -12px; }
.corner-tr { top: -12px; right: -12px; }
.corner-bl { bottom: -12px; left: -12px; }
.corner-br { bottom: -12px; right: -12px; }

/* Title */
.spotlight-title {
  text-align: center;
}

.title-ribbon {
  display: inline-block;
  font-family: var(--hand-font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--hand-bg-cream);
  background: var(--hand-pink);
  padding: 0.5rem 2rem;
  position: relative;
  clip-path: polygon(10% 0%, 90% 0%, 100% 50%, 90% 100%, 10% 100%, 0% 50%);
}

/* Main */
.spotlight-main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-paper {
  background: white;
  border: 2px solid var(--hand-text-light);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 5px 5px 0 var(--hand-shadow-color);
  transform: rotate(-0.5deg);
  max-width: 90%;
}

.main-paper :deep(h1) {
  font-family: var(--hand-font-display);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--hand-text-dark);
  margin-bottom: 1rem;
}

.main-paper :deep(h2) {
  font-family: var(--hand-font-display);
  font-size: 1.8rem;
  color: var(--hand-text);
  margin-bottom: 0.75rem;
}

.main-paper :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 1.2rem;
  line-height: 1.7;
  color: var(--hand-text);
}

.main-paper :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  border: 3px solid var(--hand-pink-light);
}

/* Caption */
.spotlight-caption {
  text-align: center;
}

.caption-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--hand-font-handwriting);
  font-size: 1.1rem;
  color: var(--hand-text);
  background: var(--hand-yellow);
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  box-shadow: 2px 2px 0 var(--hand-shadow-color);
  transform: rotate(1deg);
}

.label-icon {
  font-size: 1rem;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 1rem;
}

/* Vibe modifiers */
.vibe-minimal .spotlight-frame {
  border-width: 1px;
  border-radius: 8px;
}

.vibe-minimal .corner {
  display: none;
}

.vibe-minimal .title-ribbon {
  background: transparent;
  color: var(--hand-text-dark);
  clip-path: none;
}

.vibe-minimal .main-paper {
  box-shadow: none;
  transform: none;
}

.vibe-minimal .caption-label {
  background: transparent;
  box-shadow: none;
  transform: none;
}

.vibe-playful .spotlight-frame:hover {
  transform: scale(1.01);
}

.vibe-playful .corner {
  animation: corner-bounce 2s ease-in-out infinite;
}

@keyframes corner-bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.vibe-decorated .spotlight-frame::before {
  content: '✨';
  position: absolute;
  top: 50%;
  left: -25px;
  font-size: 1.5rem;
  transform: translateY(-50%);
}

.vibe-decorated .spotlight-frame::after {
  content: '✨';
  position: absolute;
  top: 50%;
  right: -25px;
  font-size: 1.5rem;
  transform: translateY(-50%);
}
</style>
