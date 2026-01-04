<script setup lang="ts">
/**
 * Timeline Layout - Business Project
 * 
 * Horizontal timeline with up to 5 steps.
 * 
 * Slots:
 *   - title: Timeline title
 *   - step1, step2, step3, step4, step5: Step content
 * 
 * Frontmatter:
 *   layout: timeline
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
    <div class="timeline" :class="vibeClass">
      <header v-if="$slots.title" class="timeline-title">
        <slot name="title" />
      </header>
      
      <div class="timeline-container">
        <div v-if="$slots.step1" class="timeline-step">
          <div class="step-marker">1</div>
          <div class="step-content">
            <slot name="step1" />
          </div>
        </div>
        
        <div v-if="$slots.step2" class="timeline-step">
          <div class="step-marker">2</div>
          <div class="step-content">
            <slot name="step2" />
          </div>
        </div>
        
        <div v-if="$slots.step3" class="timeline-step">
          <div class="step-marker">3</div>
          <div class="step-content">
            <slot name="step3" />
          </div>
        </div>
        
        <div v-if="$slots.step4" class="timeline-step">
          <div class="step-marker">4</div>
          <div class="step-content">
            <slot name="step4" />
          </div>
        </div>
        
        <div v-if="$slots.step5" class="timeline-step">
          <div class="step-marker">5</div>
          <div class="step-content">
            <slot name="step5" />
          </div>
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.timeline {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 2rem;
}

.timeline-title {
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 600;
  color: var(--theme-text);
}

.timeline-title :deep(h1),
.timeline-title :deep(h2),
.timeline-title :deep(h3) {
  color: var(--theme-primary);
  margin: 0;
}

.timeline-container {
  flex: 1;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 0.5rem;
  position: relative;
  padding-top: 1.5rem;
}

/* Connecting line */
.timeline-container::before {
  content: '';
  position: absolute;
  top: 2.25rem;
  left: 2rem;
  right: 2rem;
  height: 3px;
  background: linear-gradient(
    90deg,
    var(--theme-primary),
    var(--theme-accent)
  );
  z-index: 0;
}

.timeline-step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  position: relative;
  z-index: 1;
}

.step-marker {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
  background: var(--theme-primary);
  color: white;
  box-shadow: var(--shadow-md);
  border: 3px solid var(--theme-bg-base);
}

.step-content {
  text-align: center;
  padding: 1rem;
  background: var(--theme-bg-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--theme-border);
  width: 100%;
  box-shadow: var(--shadow-sm);
}

.step-content :deep(h4),
.step-content :deep(strong) {
  color: var(--theme-primary);
  display: block;
  margin-bottom: 0.5rem;
}

.step-content :deep(p) {
  font-size: 0.875rem;
  color: var(--theme-text-muted);
  margin: 0;
  line-height: 1.5;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1.5rem;
}

.vibe-minimal .timeline-container::before {
  height: 2px;
  background: var(--theme-border);
}

.vibe-minimal .step-marker {
  width: 2rem;
  height: 2rem;
  font-size: 0.875rem;
  box-shadow: none;
}

.vibe-minimal .step-content {
  padding: 0.75rem;
  border-radius: var(--radius-sm);
  box-shadow: none;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.75rem;
}

.vibe-clean .step-marker {
  width: 2.25rem;
  height: 2.25rem;
}

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 2.5rem;
}

.vibe-decorative .timeline-container::before {
  height: 4px;
  border-radius: 2px;
}

.vibe-decorative .step-marker {
  width: 3rem;
  height: 3rem;
  font-size: 1.125rem;
}

.vibe-decorative .step-content {
  padding: 1.25rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: none;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 3rem;
}

.vibe-expressive .timeline-container::before {
  height: 5px;
  background: linear-gradient(
    90deg,
    var(--theme-primary),
    var(--theme-accent),
    var(--theme-success)
  );
  border-radius: 3px;
}

.vibe-expressive .step-marker {
  width: 3.5rem;
  height: 3.5rem;
  font-size: 1.25rem;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
}

.vibe-expressive .step-content {
  padding: 1.5rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
}
</style>
