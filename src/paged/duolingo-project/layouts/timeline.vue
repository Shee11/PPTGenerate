<script setup lang="ts">
/**
 * Timeline Layout - Duolingo Style
 * 
 * Vertical timeline with up to 5 steps.
 * Features Duolingo's playful step indicators and progress style.
 * 
 * Slots: title, step1, step2, step3, step4, step5 (EXACTLY same as slidev-project)
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

// Duolingo step colors
const stepColors = ['#58CC02', '#1CB0F6', '#FF9600', '#CE82FF', '#FF4B4B']
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="timeline" :class="vibeClass">
      <header v-if="$slots.title" class="timeline-title">
        <slot name="title" />
      </header>
      
      <div class="timeline-container">
        <div v-if="$slots.step1" class="timeline-step" :style="{ '--step-color': stepColors[0] }">
          <div class="step-marker">
            <span class="step-number">1</span>
          </div>
          <div class="step-content">
            <slot name="step1" />
          </div>
        </div>
        
        <div v-if="$slots.step2" class="timeline-step" :style="{ '--step-color': stepColors[1] }">
          <div class="step-marker">
            <span class="step-number">2</span>
          </div>
          <div class="step-content">
            <slot name="step2" />
          </div>
        </div>
        
        <div v-if="$slots.step3" class="timeline-step" :style="{ '--step-color': stepColors[2] }">
          <div class="step-marker">
            <span class="step-number">3</span>
          </div>
          <div class="step-content">
            <slot name="step3" />
          </div>
        </div>
        
        <div v-if="$slots.step4" class="timeline-step" :style="{ '--step-color': stepColors[3] }">
          <div class="step-marker">
            <span class="step-number">4</span>
          </div>
          <div class="step-content">
            <slot name="step4" />
          </div>
        </div>
        
        <div v-if="$slots.step5" class="timeline-step" :style="{ '--step-color': stepColors[4] }">
          <div class="step-marker">
            <span class="step-number">5</span>
          </div>
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
  padding: 1.5rem;
  gap: 1rem;
}

.timeline-title {
  text-align: center;
  font-weight: 800;
  color: var(--theme-text);
}

.timeline-title :deep(h1),
.timeline-title :deep(h2),
.timeline-title :deep(h3) {
  color: var(--theme-text);
  margin: 0;
  font-weight: 800;
}

.timeline-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding-left: 1.5rem;
  position: relative;
}

/* Connecting line */
.timeline-container::before {
  content: '';
  position: absolute;
  left: 32px;
  top: 24px;
  bottom: 24px;
  width: 4px;
  background: var(--theme-border);
  border-radius: var(--radius-full);
}

.timeline-step {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  position: relative;
  z-index: 1;
}

.step-marker {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  background: var(--step-color, var(--theme-primary));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 0 color-mix(in srgb, var(--step-color, var(--theme-primary)) 70%, black);
  border: 3px solid white;
}

.step-number {
  color: white;
  font-weight: 800;
  font-size: 1.25rem;
  font-family: var(--font-heading);
}

.step-content {
  flex: 1;
  background: var(--theme-bg-card);
  border: 2px solid var(--theme-border);
  border-radius: var(--radius-lg);
  padding: 1rem 1.25rem;
  box-shadow: var(--shadow-card);
  border-left: 4px solid var(--step-color, var(--theme-primary));
}

.step-content :deep(h1),
.step-content :deep(h2),
.step-content :deep(h3),
.step-content :deep(h4) {
  color: var(--step-color, var(--theme-primary));
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.step-content :deep(p) {
  color: var(--theme-text-muted);
  margin: 0;
  line-height: 1.5;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
  gap: 0.75rem;
}

.vibe-minimal .timeline-container {
  gap: 0.5rem;
  padding-left: 1rem;
}

.vibe-minimal .timeline-container::before {
  left: 20px;
  width: 2px;
}

.vibe-minimal .step-marker {
  width: 32px;
  height: 32px;
  box-shadow: none;
  border-width: 2px;
}

.vibe-minimal .step-number {
  font-size: 0.9rem;
}

.vibe-minimal .step-content {
  border-radius: var(--radius-sm);
  border-width: 1px;
  border-left-width: 2px;
  box-shadow: none;
  padding: 0.75rem 1rem;
}

/* === VIBE: CLEAN === */
.vibe-clean .step-marker {
  width: 40px;
  height: 40px;
  box-shadow: 0 2px 0 color-mix(in srgb, var(--step-color, var(--theme-primary)) 70%, black);
  border-width: 2px;
}

.vibe-clean .step-content {
  border-width: 1px;
  border-left-width: 3px;
  box-shadow: 0 1px 0 var(--theme-border);
}

/* === VIBE: PLAYFUL === */
.vibe-playful .timeline-container::before {
  background: linear-gradient(180deg, 
    var(--theme-primary), 
    var(--theme-accent), 
    var(--theme-warning),
    var(--theme-premium)
  );
  width: 6px;
}

.vibe-playful .step-marker {
  width: 56px;
  height: 56px;
  box-shadow: 0 6px 0 color-mix(in srgb, var(--step-color, var(--theme-primary)) 60%, black);
  border-width: 4px;
}

.vibe-playful .step-number {
  font-size: 1.5rem;
}

.vibe-playful .step-content {
  border-radius: var(--radius-xl);
  border-width: 3px;
  border-left-width: 6px;
  background: linear-gradient(
    90deg,
    color-mix(in srgb, var(--step-color) 5%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2rem;
}

.vibe-expressive .timeline-container {
  gap: 1rem;
  padding-left: 2rem;
}

.vibe-expressive .timeline-container::before {
  width: 8px;
  background: linear-gradient(180deg, 
    var(--theme-primary), 
    var(--theme-accent), 
    var(--theme-warning),
    var(--theme-premium),
    var(--theme-danger)
  );
  border-radius: var(--radius-md);
}

.vibe-expressive .step-marker {
  width: 64px;
  height: 64px;
  box-shadow: 0 8px 0 color-mix(in srgb, var(--step-color, var(--theme-primary)) 50%, black);
  border-width: 5px;
}

.vibe-expressive .step-number {
  font-size: 1.75rem;
}

.vibe-expressive .step-content {
  border-radius: var(--radius-xl);
  border-width: 4px;
  border-left-width: 8px;
  box-shadow: 0 4px 0 var(--theme-border);
  padding: 1.5rem;
}

.vibe-expressive .step-content :deep(h1),
.vibe-expressive .step-content :deep(h2),
.vibe-expressive .step-content :deep(h3),
.vibe-expressive .step-content :deep(h4) {
  font-size: 1.3rem;
}
</style>
