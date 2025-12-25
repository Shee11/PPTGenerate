<script setup lang="ts">
/**
 * Spotlight Layout - Business Project
 * 
 * Center-focused dramatic layout for key announcements and feature content.
 * 
 * Slots:
 *   - default: Main content in spotlight
 *   - subtitle: Secondary text below main content
 * 
 * Frontmatter:
 *   layout: spotlight
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
    <div class="spotlight" :class="vibeClass">
      <div class="spotlight-effect"></div>
      <div class="content-wrapper">
        <div class="main-content">
          <slot />
        </div>
        <div v-if="$slots.subtitle" class="subtitle-content">
          <slot name="subtitle" />
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.spotlight {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  position: relative;
  overflow: hidden;
}

.spotlight-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120%;
  height: 120%;
  background: radial-gradient(
    ellipse 50% 50% at center,
    color-mix(in srgb, var(--theme-primary) 8%, transparent),
    transparent
  );
  pointer-events: none;
}

.content-wrapper {
  text-align: center;
  max-width: 80%;
  z-index: 1;
}

.main-content {
  color: var(--theme-text);
}

.main-content :deep(h1),
.main-content :deep(h2) {
  color: var(--theme-primary);
  font-family: var(--font-heading);
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.1;
  margin: 0;
}

.main-content :deep(p) {
  font-size: 1.5rem;
  margin-top: 1rem;
  color: var(--theme-text-muted);
}

.subtitle-content {
  margin-top: 2rem;
  font-size: 1.25rem;
  color: var(--theme-text-muted);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 2rem;
}

.vibe-minimal .spotlight-effect {
  opacity: 0.3;
}

.vibe-minimal .main-content :deep(h1),
.vibe-minimal .main-content :deep(h2) {
  font-size: 2.5rem;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 2.5rem;
}

.vibe-clean .main-content :deep(h1),
.vibe-clean .main-content :deep(h2) {
  font-size: 3rem;
}

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 4rem;
}

.vibe-decorative .spotlight-effect {
  background: radial-gradient(
    ellipse 60% 60% at center,
    color-mix(in srgb, var(--theme-primary) 12%, transparent),
    color-mix(in srgb, var(--theme-accent) 5%, transparent),
    transparent
  );
}

.vibe-decorative .main-content :deep(h1),
.vibe-decorative .main-content :deep(h2) {
  font-size: 4rem;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 5rem;
}

.vibe-expressive .spotlight-effect {
  background: radial-gradient(
    ellipse 70% 70% at center,
    color-mix(in srgb, var(--theme-primary) 15%, transparent),
    color-mix(in srgb, var(--theme-accent) 8%, transparent),
    transparent
  );
}

.vibe-expressive .main-content :deep(h1),
.vibe-expressive .main-content :deep(h2) {
  font-size: 4.5rem;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
