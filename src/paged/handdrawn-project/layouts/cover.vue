<!--
  cover.vue - Handdrawn Cover/Title Slide Layout
  
  Slots:
    - title: Main title
    - subtitle: Subtitle
    - author: Author info
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="cover-layout" :class="`vibe-${vibe}`">
      <!-- Decorative frame -->
      <div class="cover-frame">
        <!-- Corner flowers -->
        <div class="corner-deco corner-tl">✿</div>
        <div class="corner-deco corner-tr">✿</div>
        <div class="corner-deco corner-bl">✿</div>
        <div class="corner-deco corner-br">✿</div>
        
        <!-- Sketchy border -->
        <svg class="frame-border" viewBox="0 0 400 300" preserveAspectRatio="none">
          <path d="M20,10 Q200,5 380,10 Q395,150 380,290 Q200,295 20,290 Q5,150 20,10" 
                fill="none" stroke="currentColor" stroke-width="3"/>
        </svg>
        
        <!-- Content -->
        <div class="cover-content">
          <!-- Top decoration -->
          <div class="top-deco">
            <span>★</span>
            <span>★</span>
            <span>★</span>
          </div>
          
          <!-- Title -->
          <div class="cover-title">
            <slot name="title">
              <span class="placeholder">Your Title Here</span>
            </slot>
          </div>
          
          <!-- Underline squiggle -->
          <svg class="title-squiggle" viewBox="0 0 200 20">
            <path d="M0,10 Q25,5 50,10 T100,10 T150,10 T200,10" fill="none" stroke="currentColor" stroke-width="3"/>
          </svg>
          
          <!-- Subtitle -->
          <div v-if="$slots.subtitle" class="cover-subtitle">
            <slot name="subtitle" />
          </div>
          
          <!-- Author -->
          <div v-if="$slots.author" class="cover-author">
            <div class="author-line"></div>
            <slot name="author" />
          </div>
          
          <!-- Bottom decoration -->
          <div class="bottom-deco">
            <span>🌸</span>
            <span>🌿</span>
            <span>🌸</span>
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
  vibe: 'decorated'
})
</script>

<style scoped>
.cover-layout {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

/* Frame */
.cover-frame {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.frame-border {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  color: var(--hand-pink);
}

/* Corner decorations */
.corner-deco {
  position: absolute;
  font-size: 2rem;
  color: var(--hand-pink);
  z-index: 10;
}

.corner-tl { top: 0; left: 0; }
.corner-tr { top: 0; right: 0; }
.corner-bl { bottom: 0; left: 0; }
.corner-br { bottom: 0; right: 0; }

/* Content */
.cover-content {
  text-align: center;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

/* Top decoration */
.top-deco {
  display: flex;
  gap: 1rem;
  font-size: 1.5rem;
  color: var(--hand-yellow-dark);
}

/* Title */
.cover-title {
  font-family: var(--hand-font-display);
  font-size: 3.5rem;
  font-weight: 700;
  color: var(--hand-text-dark);
  line-height: 1.2;
}

.cover-title :deep(span),
.cover-title :deep(h1) {
  font-family: inherit;
  font-size: inherit;
  font-weight: inherit;
  color: inherit;
  margin: 0;
}

/* Title squiggle */
.title-squiggle {
  width: 200px;
  height: 20px;
  color: var(--hand-pink);
}

/* Subtitle */
.cover-subtitle {
  font-family: var(--hand-font-handwriting);
  font-size: 1.5rem;
  color: var(--hand-text);
  max-width: 500px;
}

/* Author */
.cover-author {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--hand-font-body);
  font-size: 1.1rem;
  color: var(--hand-text);
}

.author-line {
  width: 50px;
  height: 2px;
  background: var(--hand-text-light);
}

/* Bottom decoration */
.bottom-deco {
  display: flex;
  gap: 1rem;
  font-size: 1.5rem;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
}

/* Vibe modifiers */
.vibe-minimal .frame-border,
.vibe-minimal .corner-deco,
.vibe-minimal .top-deco,
.vibe-minimal .bottom-deco,
.vibe-minimal .title-squiggle {
  display: none;
}

.vibe-cozy .corner-deco {
  font-size: 1.5rem;
}

.vibe-cozy .frame-border {
  opacity: 0.5;
}

.vibe-playful .corner-deco {
  animation: corner-spin 3s ease-in-out infinite;
}

@keyframes corner-spin {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(10deg); }
}

.vibe-decorated .cover-frame::before {
  content: '';
  position: absolute;
  inset: 20px;
  border: 2px dashed var(--hand-pink-light);
  border-radius: 20px;
  pointer-events: none;
}
</style>
