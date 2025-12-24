<!--
  spotlight.vue - Editorial Spotlight Layout
  
  Slots:
    - title: Spotlight title
    - main: Main featured content
    - caption: Caption or description
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="spotlight">
      <!-- Frame -->
      <div class="spotlight-frame">
        <!-- Title -->
        <div v-if="$slots.title" class="spotlight-title">
          <div class="title-ornament">◆</div>
          <slot name="title" />
          <div class="title-ornament">◆</div>
        </div>
        
        <!-- Main content -->
        <div class="spotlight-main">
          <slot name="main">
            <span class="placeholder">Featured content</span>
          </slot>
        </div>
        
        <!-- Caption -->
        <div v-if="$slots.caption" class="spotlight-caption">
          <div class="caption-line"></div>
          <slot name="caption" />
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
.spotlight {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

/* Frame */
.spotlight-frame {
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

/* Title */
.spotlight-title {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  text-align: center;
}

.spotlight-title :deep(h1),
.spotlight-title :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 2.5rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0;
}

.title-ornament {
  color: var(--edit-gold);
  font-size: 0.7rem;
}

/* Main */
.spotlight-main {
  width: 100%;
  text-align: center;
}

.spotlight-main :deep(h1) {
  font-family: var(--edit-font-display);
  font-size: 3rem;
  font-weight: 400;
  line-height: 1.2;
  color: var(--edit-text-dark);
  margin-bottom: 1rem;
}

.spotlight-main :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 1.2rem;
  line-height: 1.8;
  color: var(--edit-text);
  max-width: 600px;
  margin: 0 auto;
}

.spotlight-main :deep(img) {
  max-width: 100%;
  max-height: 350px;
  object-fit: cover;
}

/* Caption */
.spotlight-caption {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}

.caption-line {
  width: 60px;
  height: 1px;
  background: var(--edit-gold);
}

.spotlight-caption :deep(p) {
  font-family: var(--edit-font-accent);
  font-size: 0.9rem;
  font-style: italic;
  color: var(--edit-text-light);
  margin: 0;
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
}

/* Vibe: Modern */
.vibe-modern .title-ornament {
  display: none;
}

.vibe-modern .caption-line {
  background: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .spotlight-main :deep(h1) {
  color: var(--edit-white);
}
</style>
