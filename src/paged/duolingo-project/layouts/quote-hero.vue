<!--
  quote-hero.vue - Duolingo Style Quote Display Layout
  
  Purpose: Stunning quote display with Duolingo's playful typography
  Perfect for testimonials, motivational quotes, or impactful statements
  
  Slots: quote, author, context (EXACTLY same as slidev-project)
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="quote-hero-layout" :class="`vibe-${vibe}`">
      <!-- Decorative quote marks -->
      <div class="quote-marks">
        <span class="quote-mark quote-mark-open">❝</span>
        <span class="quote-mark quote-mark-close">❞</span>
      </div>
      
      <!-- Main quote content -->
      <div class="quote-wrapper">
        <blockquote class="quote-text">
          <slot name="quote" />
        </blockquote>
        
        <!-- Attribution -->
        <div v-if="$slots.author || $slots.context" class="quote-attribution">
          <div class="attribution-line"></div>
          <div class="author-wrapper">
            <div v-if="$slots.author" class="author-name">
              <slot name="author" />
            </div>
            <div v-if="$slots.context" class="author-context">
              <slot name="context" />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Decorative speech bubble accent -->
      <div class="bubble-accent"></div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import SlideShell from './SlideShell.vue'

const props = withDefaults(defineProps<{
  theme?: string
  vibe?: string
  header?: string
  footer?: string
}>(), {
  theme: 'duolingo',
  vibe: 'playful'
})
</script>

<style scoped>
.quote-hero-layout {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 3rem;
}

/* Quote marks */
.quote-marks {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.quote-mark {
  position: absolute;
  font-size: 8rem;
  color: var(--theme-primary);
  opacity: 0.15;
  font-family: var(--font-heading);
  line-height: 1;
}

.quote-mark-open {
  top: 2rem;
  left: 2rem;
}

.quote-mark-close {
  bottom: 2rem;
  right: 2rem;
}

/* Quote wrapper */
.quote-wrapper {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 85%;
  background: var(--theme-bg-card);
  border: 3px solid var(--theme-primary);
  border-radius: var(--radius-xl);
  padding: 3rem;
  box-shadow: 0 4px 0 var(--theme-primary-dark);
}

.quote-text {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--theme-text);
  line-height: 1.5;
  font-style: normal;
}

.quote-text :deep(p) {
  margin: 0;
  font-size: inherit;
  font-weight: inherit;
  line-height: inherit;
}

/* Attribution */
.quote-attribution {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.attribution-line {
  width: 60px;
  height: 4px;
  background: var(--theme-primary);
  border-radius: var(--radius-full);
}

.author-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.author-name {
  font-weight: 800;
  font-size: 1.1rem;
  color: var(--theme-primary);
}

.author-name :deep(p) {
  margin: 0;
}

.author-context {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--theme-text-muted);
}

.author-context :deep(p) {
  margin: 0;
}

/* Speech bubble accent */
.bubble-accent {
  position: absolute;
  bottom: calc(50% - 100px);
  left: 5%;
  width: 0;
  height: 0;
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  border-top: 30px solid var(--theme-primary);
  opacity: 0.3;
  transform: rotate(-15deg);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 2rem;
}

.vibe-minimal .quote-marks {
  display: none;
}

.vibe-minimal .quote-wrapper {
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 2rem;
}

.vibe-minimal .quote-text {
  font-size: 1.5rem;
}

.vibe-minimal .bubble-accent {
  display: none;
}

.vibe-minimal .attribution-line {
  height: 2px;
  width: 40px;
}

/* === VIBE: CLEAN === */
.vibe-clean .quote-marks {
  opacity: 0.1;
}

.vibe-clean .quote-marks .quote-mark {
  font-size: 6rem;
}

.vibe-clean .quote-wrapper {
  border-width: 2px;
  box-shadow: 0 2px 0 var(--theme-border);
  padding: 2.5rem;
}

.vibe-clean .bubble-accent {
  display: none;
}

/* === VIBE: PLAYFUL === */
.vibe-playful .quote-marks .quote-mark {
  opacity: 0.2;
  color: var(--theme-accent);
}

.vibe-playful .quote-wrapper {
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-primary) 5%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
  transform: rotate(-1deg);
}

.vibe-playful .quote-text {
  font-size: 2rem;
}

.vibe-playful .bubble-accent {
  opacity: 0.5;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2.5rem;
}

.vibe-expressive .quote-marks .quote-mark {
  font-size: 10rem;
  opacity: 0.25;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.vibe-expressive .quote-wrapper {
  border-width: 4px;
  box-shadow: 0 6px 0 var(--theme-primary-dark);
  padding: 3.5rem;
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-primary) 8%, var(--theme-bg-card)),
    var(--theme-bg-card),
    color-mix(in srgb, var(--theme-accent) 8%, var(--theme-bg-card))
  );
  transform: rotate(-0.5deg);
}

.vibe-expressive .quote-text {
  font-size: 2.25rem;
}

.vibe-expressive .author-name {
  font-size: 1.25rem;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.vibe-expressive .bubble-accent {
  border-top-width: 40px;
  border-left-width: 25px;
  border-right-width: 25px;
  opacity: 0.4;
}
</style>
