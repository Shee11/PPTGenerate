<!--
  DisplayWidget.vue - Large Display Text (for titles)
  
  Props:
    - text: Display text
-->
<template>
  <h1 class="display-widget">{{ text }}</h1>
</template>

<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>

<style scoped>
.display-widget {
  font-size: 3rem;
  font-weight: 700;
  color: var(--c-text);
  line-height: 1.1;
  margin: 0;
}
</style>
