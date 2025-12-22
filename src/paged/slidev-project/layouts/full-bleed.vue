<script setup lang="ts">
/**
 * Full Bleed Layout
 * 
 * Edge-to-edge content with optional alignment.
 * Inherits from SlideShell for consistent header/footer/theme/vibe.
 * 
 * Frontmatter:
 *   layout: full-bleed
 *   align: center     # top, center, bottom
 *   header: "..."     # Optional header text
 *   footer: "..."     # Optional footer text
 *   theme: dark-professional
 *   vibe: balanced
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  align?: 'top' | 'center' | 'bottom'
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'decorative' | 'expressive'
}>()

// Get vibe from SlideShell injection or props
const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')

// Map align parameter to flexbox alignment
const alignmentStyle = computed(() => {
  const align = props.align || 'center'
  const alignMap = {
    top: 'flex-start',
    center: 'center',
    bottom: 'flex-end'
  }
  return {
    justifyContent: alignMap[align] || 'center'
  }
})

// Vibe class
const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="full-bleed" :class="vibeClass" :style="alignmentStyle">
      <div class="content-wrapper">
        <slot />
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.full-bleed {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 2rem;
  color: var(--theme-text);
}

.content-wrapper {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  background: var(--theme-bg-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--theme-border-subtle);
  box-shadow: var(--shadow-md);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
}

.vibe-minimal .content-wrapper {
  padding: 1rem;
  max-width: 100%;
  background: transparent;
  border: none;
  border-radius: 0;
  box-shadow: none;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.5rem;
}

.vibe-clean .content-wrapper {
  padding: 1.5rem;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
}

/* === VIBE: BALANCED (default) === */
/* Base styles above */

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 2.5rem;
}

.vibe-decorative .content-wrapper {
  padding: 2.5rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-elevated) 50%, var(--theme-bg-surface))
  );
  border: none;
  position: relative;
}

/* Corner accents */
.vibe-decorative .content-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--theme-primary) 0%, transparent 70%);
  opacity: 0.15;
  border-radius: var(--radius-lg) 0 var(--radius-lg) 0;
}

.vibe-decorative .content-wrapper::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 60px;
  height: 60px;
  background: linear-gradient(-45deg, var(--theme-accent) 0%, transparent 70%);
  opacity: 0.15;
  border-radius: 0 var(--radius-lg) 0 var(--radius-lg);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 3rem;
}

.vibe-expressive .content-wrapper {
  padding: 3rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-elevated) 70%, var(--theme-primary))
  );
  border: none;
  backdrop-filter: blur(20px);
  position: relative;
}

/* Vignette overlay */
.vibe-expressive::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at center,
    transparent 0%,
    transparent 40%,
    color-mix(in srgb, var(--theme-bg-base) 20%, transparent) 100%
  );
  pointer-events: none;
}

/* Corner accents */
.vibe-expressive .content-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, var(--theme-primary) 0%, transparent 70%);
  opacity: 0.2;
  border-radius: var(--radius-xl) 0 var(--radius-xl) 0;
}

.vibe-expressive .content-wrapper::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: linear-gradient(-45deg, var(--theme-accent) 0%, transparent 70%);
  opacity: 0.2;
  border-radius: 0 var(--radius-xl) 0 var(--radius-xl);
}
</style>
