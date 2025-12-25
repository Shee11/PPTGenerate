<!--
  BodyWidget.vue - Body Text Block
  
  Props:
    - text: Body text content
-->
<template>
  <p class="body-widget">{{ text }}</p>
</template>

<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>

<style scoped>
.body-widget {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--c-text);
  margin: 0;
}
</style>
