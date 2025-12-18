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
  @apply h-full w-full p-8 flex flex-col;
}

.timeline-title {
  @apply mb-8 text-center;
}

.timeline-container {
  @apply flex-1 flex flex-col justify-around relative;
}

.timeline-step {
  @apply flex items-start gap-4 relative;
}

.timeline-step:not(:last-child)::after {
  content: '';
  @apply absolute left-6 top-12 bottom-0 w-0.5 bg-blue-300 dark:bg-blue-700 -translate-y-full;
}

.step-marker {
  @apply w-12 h-12 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold text-lg flex-shrink-0;
}

.step-content {
  @apply flex-1 pt-2;
}
</style>
