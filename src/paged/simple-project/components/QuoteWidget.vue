<!--
  QuoteWidget.vue - Quote/Vision Statement Display
  
  Props:
    - text: Quote text
    - attribution: Author/source
    - title: Optional title above quote
-->
<template>
  <div class="quote-widget">
    <div v-if="title" class="quote-title">{{ title }}</div>
    <blockquote class="quote-content">
      <div class="quote-mark">"</div>
      <p class="quote-text">{{ text }}</p>
      <footer v-if="attribution" class="quote-attribution">
        — {{ attribution }}
      </footer>
    </blockquote>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text: string
  attribution?: string
  title?: string
}>()
</script>

<style scoped>
.quote-widget {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.quote-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--c-text);
}

.quote-content {
  margin: 0;
  padding: 24px;
  background: var(--c-bg-surface);
  border-radius: 12px;
  border-left: 4px solid var(--c-primary);
  position: relative;
}

.quote-mark {
  position: absolute;
  top: 8px;
  left: 16px;
  font-size: 4rem;
  color: var(--c-primary);
  opacity: 0.2;
  font-family: Georgia, serif;
  line-height: 1;
}

.quote-text {
  font-size: 1.25rem;
  line-height: 1.6;
  color: var(--c-text);
  margin: 0;
  padding-left: 24px;
  font-style: italic;
}

.quote-attribution {
  margin-top: 16px;
  padding-left: 24px;
  font-size: 0.9375rem;
  color: var(--c-text-muted);
  font-style: normal;
}
</style>
