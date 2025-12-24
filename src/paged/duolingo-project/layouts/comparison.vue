<script setup lang="ts">
/**
 * Comparison Layout - Duolingo Style
 * 
 * Before/After comparison with VS divider.
 * Features Duolingo's playful design with color-coded sides.
 * 
 * Slots: title, beforeLabel, before, afterLabel, after (EXACTLY same as slidev-project)
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'playful' | 'expressive'
}>()

const injectedVibe = inject('vibe', computed(() => props.vibe || 'playful'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'playful')
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
          <div class="side-badge">❌</div>
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
          <div class="side-badge">✅</div>
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
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comparison-title {
  text-align: center;
  font-weight: 800;
  color: var(--theme-text);
}

.comparison-title :deep(h1),
.comparison-title :deep(h2),
.comparison-title :deep(h3) {
  color: var(--theme-text);
  margin: 0;
  font-weight: 800;
}

.comparison-container {
  flex: 1;
  display: flex;
  align-items: stretch;
  gap: 1rem;
}

.comparison-side {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  background: var(--theme-bg-card);
  color: var(--theme-text);
  border: 2px solid var(--theme-border);
  box-shadow: var(--shadow-card);
  position: relative;
}

.side-badge {
  position: absolute;
  top: -12px;
  right: 16px;
  font-size: 1.5rem;
  background: var(--theme-bg-card);
  padding: 0 8px;
  border-radius: var(--radius-full);
}

.before {
  border-color: var(--theme-danger);
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-danger) 5%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.after {
  border-color: var(--theme-success);
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-success) 5%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.side-label {
  padding-bottom: 0.75rem;
  margin-bottom: 0.75rem;
  border-bottom: 2px dashed var(--theme-border);
}

.side-label :deep(h1),
.side-label :deep(h2),
.side-label :deep(h3) {
  margin: 0;
  font-weight: 700;
}

.before .side-label :deep(h1),
.before .side-label :deep(h2),
.before .side-label :deep(h3) {
  color: var(--theme-danger);
}

.after .side-label :deep(h1),
.after .side-label :deep(h2),
.after .side-label :deep(h3) {
  color: var(--theme-success);
}

.side-content {
  flex: 1;
  color: var(--theme-text-muted);
}

.side-content :deep(ul),
.side-content :deep(ol) {
  margin: 0;
  padding-left: 1.25rem;
}

.side-content :deep(li) {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

/* VS Divider */
.comparison-divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 60px;
  flex-shrink: 0;
}

.divider-icon {
  background: var(--theme-warning);
  color: white;
  font-weight: 800;
  font-size: 1rem;
  padding: 12px 16px;
  border-radius: var(--radius-full);
  box-shadow: 0 4px 0 color-mix(in srgb, var(--theme-warning) 70%, black);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
  gap: 0.75rem;
}

.vibe-minimal .comparison-container {
  gap: 0.75rem;
}

.vibe-minimal .comparison-side {
  border-radius: var(--radius-sm);
  border-width: 1px;
  padding: 1rem;
  box-shadow: none;
}

.vibe-minimal .side-badge {
  font-size: 1rem;
  top: -8px;
}

.vibe-minimal .divider-icon {
  font-size: 0.75rem;
  padding: 8px 12px;
  box-shadow: 0 2px 0 color-mix(in srgb, var(--theme-warning) 70%, black);
}

/* === VIBE: CLEAN === */
.vibe-clean .comparison-side {
  border-width: 1px;
  box-shadow: 0 1px 0 var(--theme-border);
}

.vibe-clean .divider-icon {
  box-shadow: 0 2px 0 color-mix(in srgb, var(--theme-warning) 70%, black);
}

/* === VIBE: PLAYFUL === */
.vibe-playful .comparison-side {
  border-radius: var(--radius-xl);
  border-width: 3px;
  box-shadow: 0 4px 0 var(--theme-border);
}

.vibe-playful .before {
  box-shadow: 0 4px 0 color-mix(in srgb, var(--theme-danger) 40%, transparent);
  transform: rotate(-0.5deg);
}

.vibe-playful .after {
  box-shadow: 0 4px 0 color-mix(in srgb, var(--theme-success) 40%, transparent);
  transform: rotate(0.5deg);
}

.vibe-playful .side-badge {
  font-size: 2rem;
  top: -16px;
}

.vibe-playful .divider-icon {
  font-size: 1.1rem;
  padding: 14px 18px;
  box-shadow: 0 6px 0 color-mix(in srgb, var(--theme-warning) 60%, black);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2rem;
  gap: 1.5rem;
}

.vibe-expressive .comparison-container {
  gap: 1.5rem;
}

.vibe-expressive .comparison-side {
  border-radius: var(--radius-xl);
  border-width: 4px;
  padding: 2rem;
}

.vibe-expressive .before {
  box-shadow: 0 6px 0 color-mix(in srgb, var(--theme-danger) 50%, transparent);
  transform: rotate(-1deg);
}

.vibe-expressive .after {
  box-shadow: 0 6px 0 color-mix(in srgb, var(--theme-success) 50%, transparent);
  transform: rotate(1deg);
}

.vibe-expressive .side-badge {
  font-size: 2.5rem;
  top: -20px;
}

.vibe-expressive .divider-icon {
  font-size: 1.25rem;
  padding: 16px 22px;
  box-shadow: 0 8px 0 color-mix(in srgb, var(--theme-warning) 50%, black);
  background: linear-gradient(135deg, var(--theme-warning), var(--theme-golden));
}
</style>
