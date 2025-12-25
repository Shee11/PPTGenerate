<!--
  cover.vue - Cover/Title Slide Layout
  
  Purpose: Title slide with centered content
  
  Slots:
    - default: Main title content
    - subtitle: Subtitle below title
    - footer: Footer content (author, date)
-->
<template>
  <SlideShell :theme="theme">
    <div class="cover-layout">
      <div class="cover-content">
        <div class="title-area">
          <slot />
        </div>
        <div v-if="$slots.subtitle" class="subtitle-area">
          <slot name="subtitle" />
        </div>
      </div>
      <div v-if="$slots.footer" class="footer-area">
        <slot name="footer" />
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import SlideShell from './SlideShell.vue'

withDefaults(defineProps<{
  theme?: string
}>(), {
  theme: 'default'
})
</script>

<style scoped>
.cover-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.cover-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 24px;
  max-width: 80%;
}

.title-area {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.1;
  color: var(--c-text);
}

.title-area :deep(h1) {
  font-size: inherit;
  font-weight: inherit;
  line-height: inherit;
  margin: 0;
}

.subtitle-area {
  font-size: 1.25rem;
  color: var(--c-text-muted);
  line-height: 1.5;
  max-width: 600px;
}

.footer-area {
  padding-top: 32px;
  font-size: 0.875rem;
  color: var(--c-text-dim);
}
</style>
