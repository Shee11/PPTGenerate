<!--
  quote-hero.vue - Cyberpunk Quote Hero Layout
  
  Slots:
    - quote: The quote text
    - author: Quote attribution
    - context: Additional context
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="quote-hero-layout" :class="`vibe-${vibe}`">
      <!-- Background decoration -->
      <div class="quote-bg">
        <div class="bg-glyph bg-glyph-1">"</div>
        <div class="bg-glyph bg-glyph-2">"</div>
      </div>
      
      <!-- Quote content -->
      <div class="quote-wrapper">
        <div class="quote-marks quote-open">[</div>
        <blockquote class="quote-text">
          <slot name="quote">
            <span class="placeholder">// INSERT_QUOTE_HERE</span>
          </slot>
        </blockquote>
        <div class="quote-marks quote-close">]</div>
      </div>
      
      <!-- Attribution -->
      <div v-if="$slots.author" class="quote-attribution">
        <div class="attr-line"></div>
        <div class="attr-content">
          <div class="attr-author">
            <slot name="author" />
          </div>
          <div v-if="$slots.context" class="attr-context">
            <slot name="context" />
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
  theme: 'cyberpunk',
  vibe: 'balanced'
})
</script>

<style scoped>
.quote-hero-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 3rem;
  position: relative;
}

/* Background glyphs */
.quote-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.bg-glyph {
  position: absolute;
  font-family: var(--cyber-font-display);
  font-size: 20rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  opacity: 0.03;
  line-height: 1;
}

.bg-glyph-1 {
  top: -5%;
  left: 5%;
}

.bg-glyph-2 {
  bottom: -15%;
  right: 5%;
  transform: rotate(180deg);
}

/* Quote wrapper */
.quote-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  max-width: 900px;
  margin-bottom: 2rem;
}

.quote-marks {
  font-family: var(--cyber-font-mono);
  font-size: 3rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-shadow: 0 0 20px var(--cyber-cyan-glow);
  line-height: 1;
  flex-shrink: 0;
}

.quote-open {
  align-self: flex-start;
}

.quote-close {
  align-self: flex-end;
}

/* Quote text */
.quote-text {
  font-family: var(--cyber-font-display);
  font-size: 2.25rem;
  font-weight: 500;
  line-height: 1.4;
  color: var(--cyber-text, #e0e0e0);
  margin: 0;
  padding: 0;
  border: none;
  text-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
}

.quote-text :deep(em),
.quote-text :deep(.highlight) {
  font-style: normal;
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 15px var(--cyber-magenta-glow);
}

/* Attribution */
.quote-attribution {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.attr-line {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, var(--cyber-magenta, #FF00FF), var(--cyber-cyan, #00FFFF));
  box-shadow: 0 0 10px var(--cyber-cyan-glow);
}

.attr-content {
  text-align: left;
}

.attr-author {
  font-family: var(--cyber-font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.attr-context {
  font-family: var(--cyber-font-mono);
  font-size: 0.85rem;
  color: var(--cyber-text-dim);
  margin-top: 0.25rem;
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 1rem;
}

/* Vibe modifiers */
.vibe-minimal .quote-bg,
.vibe-minimal .attr-line {
  display: none;
}

.vibe-minimal .quote-marks {
  font-size: 2rem;
  opacity: 0.5;
}

.vibe-intense .quote-text {
  font-size: 2.5rem;
}

.vibe-intense .quote-marks {
  font-size: 4rem;
  animation: mark-pulse 3s ease-in-out infinite alternate;
}

@keyframes mark-pulse {
  from { text-shadow: 0 0 20px var(--cyber-cyan-glow); }
  to { text-shadow: 0 0 40px var(--cyber-cyan-glow), 0 0 60px var(--cyber-cyan-glow); }
}

.vibe-glitch .quote-text {
  animation: quote-glitch 6s ease-in-out infinite;
}

@keyframes quote-glitch {
  0%, 100% { transform: translate(0); filter: none; }
  15% { transform: translate(-2px, 0); filter: hue-rotate(5deg); }
  30% { transform: translate(2px, 0); }
  45% { transform: translate(0); filter: none; }
}
</style>
