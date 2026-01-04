<!--
  StatNumber.vue - Business Stat Number Component
  
  Large stat number display with optional prefix/suffix.
  
  Props:
    - value: The number or value to display
    - prefix: Prefix text (e.g., "$", "+")
    - suffix: Suffix text (e.g., "%", "K")
    - label: Description label
    - size: Size variant (sm, md, lg, xl)
-->
<template>
  <div class="stat-number" :class="[`size-${size}`]">
    <div class="stat-value">
      <span v-if="prefix" class="stat-prefix">{{ prefix }}</span>
      <span class="stat-main">{{ value }}</span>
      <span v-if="suffix" class="stat-suffix">{{ suffix }}</span>
    </div>
    <div v-if="label" class="stat-label">{{ label }}</div>
    <div v-if="$slots.default" class="stat-extra">
      <slot />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  value: {
    type: [String, Number],
    required: true,
  },
  prefix: String,
  suffix: String,
  label: String,
  size: {
    type: String,
    default: 'md',
  },
})
</script>

<style scoped>
.stat-number {
  text-align: center;
}

.stat-value {
  font-weight: 700;
  color: var(--c-text-primary, #1a1a1a);
  font-family: var(--font-display, 'Inter', sans-serif);
  line-height: 1;
}

.stat-prefix,
.stat-suffix {
  opacity: 0.7;
}

.stat-label {
  color: var(--c-text-secondary, #6b7280);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
  margin-top: 0.5rem;
}

.stat-extra {
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: var(--c-text-secondary, #6b7280);
}

/* Size: Small */
.size-sm .stat-value {
  font-size: 2rem;
}

.size-sm .stat-label {
  font-size: 0.75rem;
}

/* Size: Medium */
.size-md .stat-value {
  font-size: 3rem;
}

.size-md .stat-label {
  font-size: 0.85rem;
}

/* Size: Large */
.size-lg .stat-value {
  font-size: 4rem;
}

.size-lg .stat-label {
  font-size: 0.9rem;
}

/* Size: Extra Large */
.size-xl .stat-value {
  font-size: 5rem;
}

.size-xl .stat-label {
  font-size: 1rem;
}
</style>
