<!--
  QuoteWidget.vue - Handdrawn Quote Display Component
  
  Props:
    - quote: Quote text
    - author: Quote author
    - color: Color variant
-->
<template>
  <div class="quote-widget" :class="`quote-${color}`">
    <div class="quote-mark quote-open">❝</div>
    <div class="quote-text">
      <slot>{{ quote }}</slot>
    </div>
    <div class="quote-mark quote-close">❞</div>
    <div v-if="author" class="quote-author">
      <span class="author-dash">—</span>
      <span class="author-name">{{ author }}</span>
    </div>
    <div class="quote-deco">💬</div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  quote?: string
  author?: string
  color?: 'pink' | 'blue' | 'green' | 'yellow'
}>(), {
  quote: 'Your quote here...',
  color: 'pink'
})
</script>

<style scoped>
.quote-widget {
  position: relative;
  padding: 1.5rem;
  padding-top: 2rem;
  border-radius: 8px;
  background: var(--hand-bg-cream);
  border: 2px solid;
  box-shadow: 4px 4px 0 var(--hand-shadow-color);
}

.quote-pink { border-color: var(--hand-pink); }
.quote-blue { border-color: var(--hand-blue); }
.quote-green { border-color: var(--hand-green); }
.quote-yellow { border-color: var(--hand-yellow-dark); }

.quote-mark {
  font-family: serif;
  font-size: 2.5rem;
  line-height: 1;
  position: absolute;
}

.quote-open {
  top: 0.5rem;
  left: 0.75rem;
  color: var(--hand-pink-light);
}

.quote-close {
  bottom: 0.5rem;
  right: 0.75rem;
  color: var(--hand-pink-light);
}

.quote-text {
  font-family: var(--hand-font-handwriting);
  font-size: 1.2rem;
  line-height: 1.6;
  color: var(--hand-text-dark);
  text-align: center;
  padding: 0 1.5rem;
}

.quote-author {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-right: 1rem;
}

.author-dash {
  color: var(--hand-text-light);
}

.author-name {
  font-family: var(--hand-font-display);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--hand-text);
}

.quote-deco {
  position: absolute;
  top: -10px;
  right: -10px;
  font-size: 1.3rem;
}
</style>
