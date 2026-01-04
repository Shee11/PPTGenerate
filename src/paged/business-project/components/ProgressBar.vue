<!--
  ProgressBar.vue - Business Progress Bar Component
  
  Clean progress/completion bar for metrics and goals.
  
  Props:
    - value: Current progress value (0-100)
    - label: Label text
    - showValue: Show percentage value
    - variant: Style variant (default, thin, thick, segmented)
-->
<template>
  <div class="progress-bar" :class="[`variant-${variant}`]">
    <div class="progress-header" v-if="label || showValue">
      <span v-if="label" class="progress-label">{{ label }}</span>
      <span v-if="showValue" class="progress-value">{{ value }}%</span>
    </div>
    <div class="progress-track">
      <div 
        class="progress-fill" 
        :style="{ width: `${value}%`, backgroundColor: color }"
      ></div>
    </div>
    <div v-if="$slots.footer" class="progress-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  value: {
    type: Number,
    default: 0,
  },
  label: String,
  showValue: {
    type: Boolean,
    default: true,
  },
  variant: {
    type: String,
    default: 'default',
  },
  color: {
    type: String,
    default: 'var(--c-primary, #0F4C81)',
  },
})
</script>

<style scoped>
.progress-bar {
  width: 100%;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.progress-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--c-text-primary, #1a1a1a);
}

.progress-value {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--c-primary, #0F4C81);
}

.progress-track {
  height: 8px;
  background: var(--c-bg-muted, #e5e7eb);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.progress-footer {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: var(--c-text-secondary, #6b7280);
}

/* Variant: Thin */
.variant-thin .progress-track {
  height: 4px;
}

/* Variant: Thick */
.variant-thick .progress-track {
  height: 16px;
  border-radius: 8px;
}

.variant-thick .progress-fill {
  border-radius: 8px;
}

/* Variant: Segmented */
.variant-segmented .progress-track {
  display: flex;
  gap: 3px;
  background: transparent;
}

.variant-segmented .progress-fill {
  border-radius: 2px;
}
</style>
