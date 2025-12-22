<script setup lang="ts">
/**
 * Comparison Layout
 * 
 * Before/After comparison with VS divider.
 * Inherits from SlideShell for consistent header/footer/theme/vibe.
 * 
 * Frontmatter:
 *   layout: comparison
 *   header: "..."    # Optional header text
 *   footer: "..."    # Optional footer text
 *   theme: dark-professional
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

// Get vibe from SlideShell injection or props
const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')

// Vibe class
const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="comparison" :class="vibeClass">
      <header v-if="$slots.title" class="comparison-title">
        <slot name="title" />
      </header>
      
      <div class="comparison-container">
        <div class="comparison-side before">
          <div v-if="$slots.beforeLabel" class="side-label">
            <slot name="beforeLabel" />
          </div>
          <div class="side-content">
            <slot name="before" />
          </div>
        </div>
        
        <div class="comparison-divider">
          <div class="divider-icon">VS</div>
        </div>
        
        <div class="comparison-side after">
          <div v-if="$slots.afterLabel" class="side-label">
            <slot name="afterLabel" />
          </div>
          <div class="side-content">
            <slot name="after" />
          </div>
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.comparison {
  height: 100%;
  width: 100%;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.comparison-title {
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 600;
  color: var(--theme-text);
}

.comparison-title :deep(h1),
.comparison-title :deep(h2),
.comparison-title :deep(h3) {
  color: var(--theme-primary);
  margin: 0;
}

.comparison-container {
  flex: 1;
  display: flex;
  align-items: stretch;
  gap: 1.5rem;
}

.comparison-side {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-md);
  padding: 1.5rem;
  background: var(--theme-bg-surface);
  color: var(--theme-text);
}

.before {
  border-left: 3px solid var(--theme-danger);
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-danger) 5%, var(--theme-bg-surface)),
    var(--theme-bg-surface)
  );
}

.after {
  border-right: 3px solid var(--theme-success);
  background: linear-gradient(
    -135deg,
    color-mix(in srgb, var(--theme-success) 5%, var(--theme-bg-surface)),
    var(--theme-bg-surface)
  );
}

.side-label {
  font-weight: 600;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  opacity: 0.8;
}

.before .side-label::before {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
  vertical-align: middle;
  background: var(--theme-danger);
}

.after .side-label::before {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
  vertical-align: middle;
  background: var(--theme-success);
}

.side-content {
  flex: 1;
}

.comparison-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
}

.divider-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
  color: var(--theme-bg-base);
  font-weight: 700;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
}

.vibe-minimal .comparison-container {
  gap: 0.75rem;
}

.vibe-minimal .comparison-side {
  padding: 1rem;
  border-radius: var(--radius-sm);
  background: transparent;
  border-width: 1px;
}

.vibe-minimal .divider-icon {
  width: 2rem;
  height: 2rem;
  font-size: 0.625rem;
  background: var(--theme-border);
  color: var(--theme-text);
  box-shadow: none;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.5rem;
}

.vibe-clean .comparison-container {
  gap: 1rem;
}

.vibe-clean .comparison-side {
  padding: 1.25rem;
  border-width: 2px;
}

.vibe-clean .divider-icon {
  width: 2.5rem;
  height: 2.5rem;
  font-size: 0.675rem;
}

/* === VIBE: BALANCED (default) === */
/* Base styles above */

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 2.5rem;
}

.vibe-decorative .comparison-container {
  gap: 2rem;
}

.vibe-decorative .comparison-side {
  padding: 2rem;
  border-radius: var(--radius-lg);
  border-width: 4px;
  box-shadow: var(--shadow-md);
}

.vibe-decorative .before {
  background: linear-gradient(
    145deg,
    color-mix(in srgb, var(--theme-danger) 8%, var(--theme-bg-surface)),
    color-mix(in srgb, var(--theme-danger) 3%, var(--theme-bg-surface))
  );
}

.vibe-decorative .after {
  background: linear-gradient(
    145deg,
    color-mix(in srgb, var(--theme-success) 8%, var(--theme-bg-surface)),
    color-mix(in srgb, var(--theme-success) 3%, var(--theme-bg-surface))
  );
}

.vibe-decorative .divider-icon {
  width: 4rem;
  height: 4rem;
  font-size: 1rem;
  box-shadow: 
    var(--shadow-lg),
    0 0 0 6px color-mix(in srgb, var(--theme-bg-base) 90%, white);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 3rem;
}

.vibe-expressive .comparison-container {
  gap: 2.5rem;
}

.vibe-expressive .comparison-side {
  padding: 2.5rem;
  border-radius: var(--radius-xl);
  border-width: 0;
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
}

.vibe-expressive .before {
  background: linear-gradient(
    145deg,
    color-mix(in srgb, var(--theme-danger) 12%, var(--theme-bg-surface)),
    color-mix(in srgb, var(--theme-danger) 5%, var(--theme-bg-surface))
  );
}

.vibe-expressive .before::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    -45deg,
    transparent,
    transparent 40px,
    color-mix(in srgb, var(--theme-danger) 3%, transparent) 40px,
    color-mix(in srgb, var(--theme-danger) 3%, transparent) 80px
  );
  pointer-events: none;
}

.vibe-expressive .after {
  background: linear-gradient(
    145deg,
    color-mix(in srgb, var(--theme-success) 12%, var(--theme-bg-surface)),
    color-mix(in srgb, var(--theme-success) 5%, var(--theme-bg-surface))
  );
}

.vibe-expressive .after::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 40px,
    color-mix(in srgb, var(--theme-success) 3%, transparent) 40px,
    color-mix(in srgb, var(--theme-success) 3%, transparent) 80px
  );
  pointer-events: none;
}

.vibe-expressive .divider-icon {
  width: 5rem;
  height: 5rem;
  font-size: 1.25rem;
  font-weight: 800;
  box-shadow: 
    var(--shadow-lg),
    var(--shadow-glow),
    0 0 0 8px color-mix(in srgb, var(--theme-bg-base) 85%, white),
    0 0 0 12px color-mix(in srgb, var(--theme-primary) 20%, transparent);
}

/* Glow around VS */
.vibe-expressive .divider-icon::after {
  content: '';
  position: absolute;
  inset: -12px;
  border-radius: 50%;
  background: radial-gradient(circle, color-mix(in srgb, var(--theme-primary) 20%, transparent) 0%, transparent 70%);
}
</style>
