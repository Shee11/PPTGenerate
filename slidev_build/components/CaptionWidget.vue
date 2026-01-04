<!--
  CaptionWidget.vue - Caption/Small Text
  
  Props:
    - text: Caption text
-->
<template>
  <span class="caption-widget">{{ text }}</span>
</template>

<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>

<style scoped>
.caption-widget {
  font-size: 0.875rem;
  color: var(--c-text-dim);
  line-height: 1.4;
}
</style>
