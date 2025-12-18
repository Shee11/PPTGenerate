<script setup lang="ts">
import { computed } from 'vue'

// Props from frontmatter
const props = defineProps<{
  align?: 'top' | 'center' | 'bottom'
}>()

// Map align parameter to flexbox alignment
const alignmentStyle = computed(() => {
  const align = props.align || 'center'
  
  const alignMap = {
    top: 'flex-start',
    center: 'center',
    bottom: 'flex-end'
  }
  
  return {
    justifyContent: alignMap[align] || 'center'
  }
})
</script>

<template>
  <div class="full-bleed-layout" :style="alignmentStyle">
    <div class="content-wrapper">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.full-bleed-layout {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 3rem;
  background-color: var(--c-bg-base);
  color: var(--c-text-main);
}

.content-wrapper {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
