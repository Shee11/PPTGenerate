<script setup lang="ts">
/**
 * Quote Hero Layout - Business Project
 * 
 * Centered quote with attribution.
 * 
 * Slots:
 *   - default: Quote text
 *   - author: Attribution/author
 * 
 * Frontmatter:
 *   layout: quote-hero
 *   header: "..."
 *   footer: "..."
 *   theme: business_professional
 *   vibe: balanced
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'decorative' | 'expressive'
}>()

const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')
const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="quote-hero" :class="vibeClass">
      <div class="quote-mark open">"</div>
      <blockquote class="quote-content">
        <slot />
      </blockquote>
      <div class="quote-mark close">"</div>
      <div v-if="$slots.author" class="quote-author">
        <slot name="author" />
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.quote-hero {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  position: relative;
}

.quote-mark {
  font-size: 6rem;
  font-family: Georgia, serif;
  color: var(--theme-primary);
  opacity: 0.2;
  line-height: 1;
  position: absolute;
}

.quote-mark.open {
  top: 15%;
  left: 10%;
}

.quote-mark.close {
  bottom: 15%;
  right: 10%;
}

.quote-content {
  font-size: 2rem;
  font-weight: 500;
  line-height: 1.4;
  text-align: center;
  max-width: 80%;
  color: var(--theme-text);
  margin: 0;
  font-style: italic;
}

.quote-content :deep(p) {
  margin: 0;
}

.quote-author {
  margin-top: 2rem;
  font-size: 1rem;
  color: var(--theme-text-muted);
  text-align: center;
}

.quote-author::before {
  content: '— ';
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 2rem;
}

.vibe-minimal .quote-mark {
  font-size: 4rem;
  opacity: 0.1;
}

.vibe-minimal .quote-content {
  font-size: 1.5rem;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 2.5rem;
}

.vibe-clean .quote-content {
  font-size: 1.75rem;
}

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 4rem;
}

.vibe-decorative .quote-mark {
  font-size: 8rem;
  opacity: 0.15;
  color: var(--theme-accent);
}

.vibe-decorative .quote-content {
  font-size: 2.25rem;
  background: linear-gradient(
    180deg,
    var(--theme-text),
    var(--theme-text-muted)
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 5rem;
}

.vibe-expressive .quote-mark {
  font-size: 10rem;
  opacity: 0.1;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.vibe-expressive .quote-content {
  font-size: 2.5rem;
}

.vibe-expressive .quote-author {
  font-size: 1.125rem;
  color: var(--theme-primary);
}
</style>
