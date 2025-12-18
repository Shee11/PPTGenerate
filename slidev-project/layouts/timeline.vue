<template>
  <div class="slidev-layout timeline">
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
</template>

<style scoped>
.timeline {
  @apply h-full w-full p-10 flex flex-col;
  background: linear-gradient(135deg, var(--c-bg-base) 0%, color-mix(in srgb, var(--c-bg-base) 98%, var(--slidev-theme-primary, #3b82f6)) 100%);
  position: relative;
}

/* Background decorative gradient */
.timeline::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.03) 0%, transparent 50%);
  pointer-events: none;
}

.timeline-title {
  @apply mb-10 text-center;
  font-weight: 600;
  position: relative;
  z-index: 1;
}

.timeline-container {
  @apply flex-1 flex flex-col justify-around relative;
  padding-left: 2rem;
}

.timeline-step {
  @apply flex items-start gap-6 relative;
  margin-bottom: 1.5rem;
}

/* Gradient progress line */
.timeline-step:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 1.5rem;
  top: 3rem;
  width: 3px;
  height: calc(100% + 1.5rem);
  background: linear-gradient(180deg, 
    var(--slidev-theme-primary, #3b82f6) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 60%, transparent) 100%);
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.3);
}

.step-marker {
  @apply w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg flex-shrink-0;
  background: linear-gradient(135deg, var(--slidev-theme-primary, #3b82f6) 0%, color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 80%, #8b5cf6) 100%);
  color: white;
  box-shadow: 
    0 4px 12px rgba(59, 130, 246, 0.3),
    0 0 0 4px color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 10%, transparent),
    inset 0 -2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
}

/* Glow effect on markers */
.step-marker::after {
  content: '';
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
  z-index: -1;
}

.step-content {
  @apply flex-1 pt-1;
  padding: 1.5rem;
  background: linear-gradient(145deg, 
    color-mix(in srgb, var(--c-bg-base) 98%, white) 0%, 
    color-mix(in srgb, var(--c-bg-base) 95%, white) 100%);
  border-radius: 12px;
  border-left: 3px solid var(--slidev-theme-primary, #3b82f6);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.06),
    0 4px 16px rgba(0, 0, 0, 0.04);
  position: relative;
  transition: transform 0.3s ease;
}

/* Alternating positioning for visual rhythm */
.timeline-step:nth-child(odd) .step-content {
  transform: translateX(5px);
  border-radius: 12px 20px 12px 4px;
}

.timeline-step:nth-child(even) .step-content {
  transform: translateX(-5px);
  border-radius: 20px 12px 4px 12px;
}

/* Corner accent */
.step-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, var(--slidev-theme-primary, #3b82f6) 0%, transparent 70%);
  opacity: 0.1;
  border-radius: 12px 0 12px 0;
}
</style>
