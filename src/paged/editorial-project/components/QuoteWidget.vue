<!--
  QuoteWidget.vue - Editorial Quote Widget
  
  Props:
    - quote: Quote text
    - author: Quote author
    - source: Optional source/context
-->
<template>
  <div class="quote-widget">
    <div class="quote-mark">"</div>
    <p class="quote-text">{{ quote }}</p>
    <div class="quote-attribution">
      <span class="author">{{ author }}</span>
      <span v-if="source" class="source">{{ source }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  quote: string
  author: string
  source?: string
}>(), {})
</script>

<style scoped>
.quote-widget {
  position: relative;
  padding-left: 2rem;
}

.quote-mark {
  position: absolute;
  top: -0.5rem;
  left: 0;
  font-family: var(--edit-font-display);
  font-size: 4rem;
  line-height: 1;
  color: var(--edit-gold);
  opacity: 0.4;
}

.quote-text {
  font-family: var(--edit-font-accent);
  font-size: 1.1rem;
  font-style: italic;
  line-height: 1.6;
  color: var(--edit-text-dark);
  margin: 0 0 1rem;
}

.quote-attribution {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding-left: 1rem;
  border-left: 2px solid var(--edit-gold);
}

.author {
  font-family: var(--edit-font-accent);
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--edit-text);
}

.source {
  font-family: var(--edit-font-body);
  font-size: 0.8rem;
  color: var(--edit-text-light);
}
</style>
