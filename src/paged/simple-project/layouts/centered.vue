<!--
  centered.vue - Centered Content Layout
  
  Purpose: Single centered content area for big numbers, quotes, or focal content
  
  Slots:
    - header: Optional header
    - default: Main centered content
    - supporting: Supporting text below main content
-->
<template>
  <SlideShell :theme="theme" :header="header" :footer="footer">
    <div class="centered-layout">
      <!-- Header section -->
      <div v-if="$slots.header" class="header-section">
        <slot name="header" />
      </div>
      
      <!-- Main centered content -->
      <div class="main-content">
        <slot />
      </div>
      
      <!-- Supporting content -->
      <div v-if="$slots.supporting" class="supporting-content">
        <slot name="supporting" />
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import SlideShell from './SlideShell.vue'

withDefaults(defineProps<{
  theme?: string
  header?: string
  footer?: string
}>(), {
  theme: 'default'
})
</script>

<style scoped>
.centered-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.header-section {
  margin-bottom: 32px;
}

.header-section :deep(h1),
.header-section :deep(h2) {
  font-size: 2rem;
  font-weight: 600;
  color: var(--c-text);
  margin: 0;
}

.main-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.main-content :deep(.big-number) {
  font-size: 8rem;
  font-weight: 800;
  color: var(--c-primary);
  line-height: 1;
}

.main-content :deep(.number-label) {
  font-size: 1.5rem;
  color: var(--c-text-muted);
  margin-top: 8px;
}

.supporting-content {
  margin-top: 48px;
  max-width: 600px;
  font-size: 1.125rem;
  color: var(--c-text-muted);
  line-height: 1.6;
}
</style>
