<!--
  HeadingWidget.vue - Section/Slide Title
  
  Props:
    - text: Heading text
    - level: Heading level (1-4)
-->
<template>
  <component :is="tag" class="heading-widget" :class="`level-${level}`">
    {{ text }}
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  text: string
  level?: 1 | 2 | 3 | 4
}>(), {
  level: 2
})

const tag = computed(() => `h${props.level}`)
</script>

<style scoped>
.heading-widget {
  color: var(--c-text);
  font-family: var(--font-heading);
  font-weight: 600;
  line-height: 1.2;
  margin: 0;
}

.level-1 {
  font-size: 2.5rem;
}

.level-2 {
  font-size: 2rem;
}

.level-3 {
  font-size: 1.5rem;
}

.level-4 {
  font-size: 1.25rem;
}
</style>
