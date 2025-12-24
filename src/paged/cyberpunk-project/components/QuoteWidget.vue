<!--
  QuoteWidget.vue - Cyberpunk Quote Display Widget
  
  Props:
    - quote: The quote text
    - author: Attribution
    - source: Optional source/context
-->
<template>
  <div class="quote-widget">
    <div class="quote-marks quote-open">[</div>
    <blockquote class="quote-text">{{ quote }}</blockquote>
    <div class="quote-marks quote-close">]</div>
    <div class="quote-attribution">
      <span class="attr-line"></span>
      <span class="attr-author">{{ author }}</span>
      <span v-if="source" class="attr-source">// {{ source }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  quote: string
  author: string
  source?: string
}>()
</script>

<style scoped>
.quote-widget {
  position: relative;
  padding: 1.5rem 2rem;
  background: rgba(18, 18, 26, 0.8);
  border-left: 3px solid var(--cyber-magenta, #FF00FF);
}

.quote-marks {
  position: absolute;
  font-family: var(--cyber-font-mono);
  font-size: 2rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-shadow: 0 0 10px var(--cyber-cyan-glow);
  line-height: 1;
}

.quote-open {
  top: 0.5rem;
  left: 0.5rem;
}

.quote-close {
  bottom: 0.5rem;
  right: 0.5rem;
}

.quote-text {
  font-family: var(--cyber-font-body);
  font-size: 1.1rem;
  font-style: italic;
  line-height: 1.6;
  color: var(--cyber-text, #e0e0e0);
  margin: 0;
  padding: 0 1.5rem;
  border: none;
}

.quote-attribution {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1rem;
  padding-left: 1.5rem;
}

.attr-line {
  width: 30px;
  height: 2px;
  background: var(--cyber-magenta, #FF00FF);
  box-shadow: 0 0 5px var(--cyber-magenta-glow);
}

.attr-author {
  font-family: var(--cyber-font-display);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--cyber-magenta, #FF00FF);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.attr-source {
  font-family: var(--cyber-font-mono);
  font-size: 0.75rem;
  color: var(--cyber-text-dim);
}
</style>
