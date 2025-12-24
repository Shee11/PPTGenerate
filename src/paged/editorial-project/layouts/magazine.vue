<!--
  magazine.vue - Editorial Magazine Style Layout
  
  Slots:
    - headline: Main headline
    - subtitle: Subtitle text
    - lead: Lead paragraph
    - body: Main body text
    - sidebar: Sidebar content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="magazine-layout">
      <!-- Top section: headline -->
      <div class="mag-header">
        <div v-if="$slots.subtitle" class="mag-subtitle">
          <slot name="subtitle" />
        </div>
        <div class="mag-headline">
          <slot name="headline">
            <h1>Magazine Headline</h1>
          </slot>
        </div>
        <div class="headline-rule"></div>
      </div>
      
      <!-- Content area -->
      <div class="mag-content">
        <!-- Main column -->
        <div class="mag-main">
          <div v-if="$slots.lead" class="mag-lead">
            <div class="drop-cap-container">
              <slot name="lead" />
            </div>
          </div>
          <div class="mag-body">
            <slot name="body">
              <p>Magazine body content...</p>
            </slot>
          </div>
        </div>
        
        <!-- Sidebar -->
        <div v-if="$slots.sidebar" class="mag-sidebar">
          <slot name="sidebar" />
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import SlideShell from './SlideShell.vue'

withDefaults(defineProps<{
  theme?: string
  vibe?: string
  header?: string
  footer?: string
  dark?: boolean
}>(), {
  theme: 'editorial',
  vibe: 'classic'
})
</script>

<style scoped>
.magazine-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
}

/* Header */
.mag-header {
  text-align: center;
}

.mag-subtitle :deep(p),
.mag-subtitle :deep(span) {
  font-family: var(--edit-font-accent);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.25em;
  color: var(--edit-gold);
  margin: 0 0 0.75rem;
}

.mag-headline :deep(h1) {
  font-family: var(--edit-font-display);
  font-size: 2.5rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  line-height: 1.2;
  margin: 0;
}

.headline-rule {
  width: 80%;
  max-width: 500px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--edit-gold), transparent);
  margin: 1rem auto 0;
}

/* Content area */
.mag-content {
  display: flex;
  gap: 2rem;
  flex: 1;
}

/* Main column */
.mag-main {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Lead paragraph with drop cap */
.mag-lead {
  font-family: var(--edit-font-body);
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--edit-text-dark);
}

.drop-cap-container :deep(p::first-letter) {
  font-family: var(--edit-font-display);
  font-size: 3.5rem;
  float: left;
  line-height: 0.8;
  padding-right: 0.15em;
  color: var(--edit-gold);
  font-weight: 400;
}

/* Body */
.mag-body {
  column-count: 2;
  column-gap: 2rem;
}

.mag-body :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--edit-text);
  margin: 0 0 0.75rem;
  text-align: justify;
}

/* Sidebar */
.mag-sidebar {
  flex: 1;
  padding-left: 1.5rem;
  border-left: 1px solid var(--edit-border);
}

.mag-sidebar :deep(h3) {
  font-family: var(--edit-font-display);
  font-size: 1.1rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0 0 0.75rem;
}

.mag-sidebar :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--edit-text);
  margin: 0 0 1rem;
}

.mag-sidebar :deep(blockquote) {
  font-family: var(--edit-font-accent);
  font-style: italic;
  font-size: 1rem;
  color: var(--edit-text-dark);
  margin: 1rem 0;
  padding-left: 1rem;
  border-left: 2px solid var(--edit-gold);
}

.mag-sidebar :deep(.sidebar-stat) {
  font-family: var(--edit-font-display);
  font-size: 2rem;
  color: var(--edit-gold);
  display: block;
  margin-bottom: 0.25rem;
}

/* Vibe: Modern */
.vibe-modern .headline-rule {
  background: var(--edit-charcoal);
}

.vibe-modern .drop-cap-container :deep(p::first-letter) {
  color: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .mag-headline :deep(h1) {
  color: var(--edit-white);
}

.vibe-luxe .mag-sidebar {
  border-color: rgba(201, 169, 98, 0.3);
}
</style>
