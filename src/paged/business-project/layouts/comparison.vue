<script setup lang="ts">
/**
 * Comparison Layout - Business Project
 * 
 * Before/After comparison with VS divider.
 * 
 * Slots:
 *   - title: Comparison title
 *   - beforeLabel: Label for "before" side
 *   - before: Before content
 *   - afterLabel: Label for "after" side
 *   - after: After content
 * 
 * Frontmatter:
 *   layout: comparison
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
  border: 1px solid var(--theme-border);
}

.before {
  border-left: 4px solid var(--theme-danger);
}

.after {
  border-right: 4px solid var(--theme-success);
}

.side-label {
  font-weight: 600;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--theme-text-muted);
}

.before .side-label::before {
  content: '●';
  margin-right: 0.5rem;
  color: var(--theme-danger);
}

.after .side-label::before {
  content: '●';
  margin-right: 0.5rem;
  color: var(--theme-success);
}

.side-content {
  flex: 1;
  overflow: hidden;
}

.side-content :deep(ul),
.side-content :deep(ol) {
  padding-left: 1.25rem;
  margin: 0;
}

.side-content :deep(li) {
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.comparison-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.divider-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  background: var(--theme-primary);
  color: white;
  box-shadow: var(--shadow-md);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1.5rem;
}

.vibe-minimal .comparison-container {
  gap: 1rem;
}

.vibe-minimal .comparison-side {
  padding: 1rem;
  border-radius: var(--radius-sm);
  border-left-width: 3px;
  border-right-width: 3px;
}

.vibe-minimal .divider-icon {
  width: 2.5rem;
  height: 2.5rem;
  font-size: 0.75rem;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.75rem;
}

.vibe-clean .comparison-container {
  gap: 1.25rem;
}

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
  box-shadow: var(--shadow-md);
  border: none;
}

.vibe-decorative .before {
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-danger) 5%, var(--theme-bg-surface)),
    var(--theme-bg-surface)
  );
  border-left: 5px solid var(--theme-danger);
}

.vibe-decorative .after {
  background: linear-gradient(
    -135deg,
    color-mix(in srgb, var(--theme-success) 5%, var(--theme-bg-surface)),
    var(--theme-bg-surface)
  );
  border-right: 5px solid var(--theme-success);
}

.vibe-decorative .divider-icon {
  width: 3.5rem;
  height: 3.5rem;
  font-size: 1rem;
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
  box-shadow: var(--shadow-lg);
}

.vibe-expressive .divider-icon {
  width: 4rem;
  height: 4rem;
  font-size: 1.125rem;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
}
</style>
