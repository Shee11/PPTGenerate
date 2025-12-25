<!--
  CardWidget.vue - Generic Card with Icon, Title, Text
  
  Props:
    - icon: Optional icon (emoji or text)
    - title: Card title
    - text: Card body text
-->
<template>
  <div class="card-widget">
    <div v-if="icon" class="card-icon">{{ icon }}</div>
    <div class="card-title">{{ title }}</div>
    <div class="card-text">{{ text }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon?: string
  title: string
  text: string
}>()
</script>

<style scoped>
.card-widget {
  background: var(--c-bg-surface);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-icon {
  font-size: 1.5rem;
  margin-bottom: 4px;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--c-text);
}

.card-text {
  font-size: 0.9375rem;
  color: var(--c-text-muted);
  line-height: 1.5;
}
</style>
