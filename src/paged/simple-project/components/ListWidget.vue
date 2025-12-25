<!--
  ListWidget.vue - Styled List with Optional Header
  
  Props:
    - header: Optional header text
    - items: Array of list items (strings)
    - ordered: Whether list is ordered
-->
<template>
  <div class="list-widget">
    <div v-if="header" class="list-header">{{ header }}</div>
    <component :is="ordered ? 'ol' : 'ul'" class="list-content">
      <li v-for="(item, index) in items" :key="index" class="list-item">
        {{ item }}
      </li>
    </component>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  header?: string
  items: string[]
  ordered?: boolean
}>(), {
  ordered: false
})
</script>

<style scoped>
.list-widget {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.list-header {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--c-text);
}

.list-content {
  margin: 0;
  padding-left: 1.5em;
}

.list-item {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--c-text);
  margin-bottom: 12px;
}

.list-item:last-child {
  margin-bottom: 0;
}
</style>
