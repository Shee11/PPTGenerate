<!--
  stacked.vue - Stacked/Vertical Sections Layout
  
  Purpose: Vertical sections with primary content above and secondary below
  
  Slots:
    - header: Optional header
    - primary: Primary content section (top)
    - secondary: Secondary content section (bottom)
-->
<template>
  <SlideShell :theme="theme" :header="header" :footer="footer">
    <div class="stacked-layout">
      <!-- Header section -->
      <div v-if="$slots.header" class="header-section">
        <slot name="header" />
      </div>
      
      <!-- Primary content -->
      <div class="primary-section">
        <slot name="primary" />
      </div>
      
      <!-- Secondary content -->
      <div v-if="$slots.secondary" class="secondary-section">
        <slot name="secondary" />
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
.stacked-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.header-section {
  margin-bottom: 24px;
  flex-shrink: 0;
}

.header-section :deep(h1),
.header-section :deep(h2) {
  font-size: 2rem;
  font-weight: 600;
  color: var(--c-text);
  margin: 0;
}

.primary-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-height: 0;
}

.primary-section :deep(h3) {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--c-text);
  margin-bottom: 16px;
}

.primary-section :deep(ul),
.primary-section :deep(ol) {
  margin: 0;
  padding-left: 1.5em;
}

.primary-section :deep(li) {
  margin-bottom: 10px;
  line-height: 1.5;
}

.secondary-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--c-border);
  flex-shrink: 0;
}
</style>
