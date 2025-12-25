<!--
  BigNumberWidget.vue - Large Focal Number Display
  
  Props:
    - value: The big number
    - label: Label below the number
-->
<template>
  <div class="big-number-widget">
    <div class="big-number">{{ value }}</div>
    <div class="number-label">{{ label }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  value: string | number
  label: string
}>()
</script>

<style scoped>
.big-number-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.big-number {
  font-size: 8rem;
  font-weight: 800;
  color: var(--c-primary);
  line-height: 1;
}

.number-label {
  font-size: 1.5rem;
  color: var(--c-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
</style>
