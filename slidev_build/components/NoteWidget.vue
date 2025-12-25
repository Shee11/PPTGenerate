<!--
  NoteWidget.vue - Summary/Insight/Callout Note
  
  Props:
    - type: Note type (summary, insight, warning)
    - label: Optional label
    - content: Note content
-->
<template>
  <div class="note-widget" :class="`note-${type}`">
    <div v-if="label" class="note-label">{{ label }}</div>
    <div class="note-content">{{ content }}</div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  type?: 'summary' | 'insight' | 'warning' | 'default'
  label?: string
  content: string
}>(), {
  type: 'default'
})
</script>

<style scoped>
.note-widget {
  padding: 16px 20px;
  border-radius: 8px;
  background: var(--c-bg-surface);
  border-left: 4px solid var(--c-text-dim);
}

.note-summary {
  border-left-color: var(--c-primary);
}

.note-insight {
  border-left-color: var(--c-accent);
}

.note-warning {
  border-left-color: #f59e0b;
}

.note-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--c-text-muted);
  margin-bottom: 8px;
}

.note-content {
  font-size: 0.9375rem;
  line-height: 1.5;
  color: var(--c-text);
}
</style>
