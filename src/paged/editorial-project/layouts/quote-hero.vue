<!--
  quote-hero.vue - Editorial Quote Hero Layout
  
  Slots:
    - quote: Main quote text
    - author: Quote author
    - context: Additional context
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="quote-hero">
      <!-- Opening quote mark -->
      <div class="quote-mark quote-open">"</div>
      
      <!-- Quote content -->
      <div class="quote-content">
        <div class="quote-text">
          <slot name="quote">
            <span class="placeholder">Your inspiring quote here...</span>
          </slot>
        </div>
        
        <!-- Attribution -->
        <div class="quote-attribution">
          <div class="attribution-line"></div>
          <div class="attribution-info">
            <span class="author-name">
              <slot name="author">
                <span class="placeholder">Author Name</span>
              </slot>
            </span>
            <span v-if="$slots.context" class="author-context">
              <slot name="context" />
            </span>
          </div>
        </div>
      </div>
      
      <!-- Closing quote mark -->
      <div class="quote-mark quote-close">"</div>
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
  dark?: boolean
}>(), {
  theme: 'editorial',
  vibe: 'classic'
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
  padding: 2rem 4rem;
}

/* Quote marks */
.quote-mark {
  font-family: var(--edit-font-display);
  font-size: 8rem;
  line-height: 1;
  color: var(--edit-gold);
  opacity: 0.3;
  position: absolute;
}

.quote-open {
  top: 1rem;
  left: 2rem;
}

.quote-close {
  bottom: 1rem;
  right: 2rem;
}

/* Quote content */
.quote-content {
  max-width: 800px;
  text-align: center;
  z-index: 1;
}

.quote-text {
  font-family: var(--edit-font-display);
  font-size: 2rem;
  font-weight: 400;
  font-style: italic;
  line-height: 1.5;
  color: var(--edit-text-dark);
  margin-bottom: 2rem;
}

.quote-text :deep(em) {
  font-style: normal;
  color: var(--edit-gold);
}

/* Attribution */
.quote-attribution {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.attribution-line {
  width: 60px;
  height: 1px;
  background: var(--edit-gold);
}

.attribution-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.author-name {
  font-family: var(--edit-font-accent);
  font-size: 1rem;
  font-weight: 500;
  color: var(--edit-text);
  text-transform: uppercase;
  letter-spacing: 0.15em;
}

.author-context {
  font-family: var(--edit-font-body);
  font-size: 0.9rem;
  font-style: italic;
  color: var(--edit-text-light);
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
}

/* Vibe: Modern */
.vibe-modern .quote-mark {
  color: var(--edit-charcoal);
}

.vibe-modern .attribution-line {
  background: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .quote-text {
  color: var(--edit-white);
}

.vibe-luxe .author-name {
  color: var(--edit-light);
}
</style>
