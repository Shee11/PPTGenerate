<!--
  quote-hero.vue - Handdrawn Quote Hero Layout
  
  Slots:
    - quote: Main quote text
    - author: Quote author
    - context: Additional context
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="quote-hero" :class="`vibe-${vibe}`">
      <!-- Decorative elements -->
      <div class="quote-deco deco-left">❝</div>
      <div class="quote-deco deco-right">❞</div>
      
      <!-- Quote card -->
      <div class="quote-card">
        <!-- Notebook lines -->
        <div class="notebook-lines"></div>
        
        <!-- Quote content -->
        <div class="quote-content">
          <div class="quote-text">
            <slot name="quote">
              <span class="placeholder">Your inspiring quote here...</span>
            </slot>
          </div>
          
          <div class="quote-attribution">
            <div class="author-line"></div>
            <div class="author-info">
              <span class="author-dash">—</span>
              <span class="author-name">
                <slot name="author">
                  <span class="placeholder">Author Name</span>
                </slot>
              </span>
            </div>
          </div>
          
          <div v-if="$slots.context" class="quote-context">
            <slot name="context" />
          </div>
        </div>
        
        <!-- Sticky note accent -->
        <div class="sticky-accent">💭</div>
      </div>
      
      <!-- Bottom doodle -->
      <div class="bottom-doodle">
        <svg viewBox="0 0 200 30" class="squiggle">
          <path d="M0,15 Q25,5 50,15 T100,15 T150,15 T200,15" fill="none" stroke="currentColor" stroke-width="2"/>
        </svg>
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
.quote-hero {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 2rem;
}

/* Decorative quotes */
.quote-deco {
  position: absolute;
  font-size: 5rem;
  color: var(--hand-pink-light);
  font-family: serif;
  z-index: 0;
}

.deco-left {
  top: 10%;
  left: 5%;
}

.deco-right {
  bottom: 10%;
  right: 5%;
}

/* Quote card */
.quote-card {
  position: relative;
  background: var(--hand-bg-cream);
  border: 3px solid var(--hand-text-light);
  border-radius: 8px;
  padding: 2.5rem;
  max-width: 80%;
  box-shadow: 5px 5px 0 var(--hand-shadow-color);
  transform: rotate(-0.5deg);
  z-index: 1;
}

/* Notebook lines */
.notebook-lines {
  position: absolute;
  inset: 2rem;
  background-image: repeating-linear-gradient(
    transparent,
    transparent 28px,
    var(--hand-blue-light) 28px,
    var(--hand-blue-light) 29px
  );
  opacity: 0.5;
  pointer-events: none;
}

/* Quote content */
.quote-content {
  position: relative;
  z-index: 2;
}

.quote-text {
  font-family: var(--hand-font-handwriting);
  font-size: 1.8rem;
  line-height: 2;
  color: var(--hand-text-dark);
  text-align: center;
  margin-bottom: 1.5rem;
}

.quote-text :deep(em) {
  color: var(--hand-pink);
  font-style: normal;
  text-decoration: underline;
  text-decoration-style: wavy;
  text-decoration-color: var(--hand-pink);
}

/* Attribution */
.quote-attribution {
  text-align: right;
}

.author-line {
  width: 60px;
  height: 2px;
  background: var(--hand-pink);
  margin-left: auto;
  margin-bottom: 0.5rem;
}

.author-info {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
}

.author-dash {
  font-family: var(--hand-font-display);
  color: var(--hand-text-light);
}

.author-name {
  font-family: var(--hand-font-display);
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--hand-text);
}

/* Context */
.quote-context {
  margin-top: 1rem;
  text-align: center;
  font-family: var(--hand-font-body);
  font-size: 0.95rem;
  color: var(--hand-text-light);
}

/* Sticky accent */
.sticky-accent {
  position: absolute;
  top: -15px;
  right: -15px;
  font-size: 2rem;
}

/* Bottom squiggle */
.bottom-doodle {
  margin-top: 1.5rem;
  color: var(--hand-pink-light);
}

.squiggle {
  width: 150px;
  height: 20px;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: inherit;
}

/* Vibe modifiers */
.vibe-minimal .quote-deco,
.vibe-minimal .sticky-accent,
.vibe-minimal .bottom-doodle,
.vibe-minimal .notebook-lines {
  display: none;
}

.vibe-minimal .quote-card {
  box-shadow: none;
  transform: none;
  border-width: 1px;
}

.vibe-playful .quote-deco {
  animation: quote-pulse 3s ease-in-out infinite;
}

@keyframes quote-pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

.vibe-decorated .quote-card::before {
  content: '✨';
  position: absolute;
  top: 1rem;
  left: 1rem;
  font-size: 1.2rem;
}

.vibe-decorated .quote-card::after {
  content: '✨';
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  font-size: 1.2rem;
}
</style>
