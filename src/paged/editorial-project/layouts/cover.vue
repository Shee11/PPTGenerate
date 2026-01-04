<!--
  cover.vue - Editorial Cover Layout
  
  Slots:
    - title: Main title
    - subtitle: Subtitle
    - meta: Meta information (date, author)
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :dark="dark">
    <div class="cover-layout">
      <!-- Decorative frame -->
      <div class="cover-frame">
        <div class="frame-corner frame-tl"></div>
        <div class="frame-corner frame-tr"></div>
        <div class="frame-corner frame-bl"></div>
        <div class="frame-corner frame-br"></div>
        
        <!-- Content -->
        <div class="cover-content">
          <!-- Top ornament -->
          <div class="cover-ornament">
            <span class="ornament-line"></span>
            <span class="ornament-diamond">◆</span>
            <span class="ornament-line"></span>
          </div>
          
          <!-- Title -->
          <div class="cover-title">
            <slot name="title">
              <h1>Presentation Title</h1>
            </slot>
          </div>
          
          <!-- Subtitle -->
          <div v-if="$slots.subtitle" class="cover-subtitle">
            <slot name="subtitle" />
          </div>
          
          <!-- Divider -->
          <div class="cover-divider"></div>
          
          <!-- Meta -->
          <div v-if="$slots.meta" class="cover-meta">
            <slot name="meta" />
          </div>
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
  dark?: boolean
}>(), {
  theme: 'editorial',
  vibe: 'classic'
})
</script>

<style scoped>
.cover-layout {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

/* Frame */
.cover-frame {
  position: relative;
  width: 100%;
  max-width: 700px;
  padding: 3rem;
}

.frame-corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border-color: var(--edit-gold);
  border-style: solid;
}

.frame-tl { top: 0; left: 0; border-width: 1px 0 0 1px; }
.frame-tr { top: 0; right: 0; border-width: 1px 1px 0 0; }
.frame-bl { bottom: 0; left: 0; border-width: 0 0 1px 1px; }
.frame-br { bottom: 0; right: 0; border-width: 0 1px 1px 0; }

/* Content */
.cover-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1.5rem;
}

/* Ornament */
.cover-ornament {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.ornament-line {
  width: 60px;
  height: 1px;
  background: var(--edit-gold);
}

.ornament-diamond {
  color: var(--edit-gold);
  font-size: 0.6rem;
}

/* Title */
.cover-title :deep(h1) {
  font-family: var(--edit-font-display);
  font-size: 3rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  line-height: 1.15;
  margin: 0;
}

/* Subtitle */
.cover-subtitle :deep(p),
.cover-subtitle :deep(h2) {
  font-family: var(--edit-font-accent);
  font-size: 1.25rem;
  font-style: italic;
  color: var(--edit-text);
  margin: 0;
}

/* Divider */
.cover-divider {
  width: 40px;
  height: 1px;
  background: var(--edit-border);
}

/* Meta */
.cover-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.cover-meta :deep(p),
.cover-meta :deep(span) {
  font-family: var(--edit-font-accent);
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--edit-text-light);
  margin: 0;
}

.cover-meta :deep(.author) {
  color: var(--edit-gold);
}

/* Vibe: Modern */
.vibe-modern .frame-corner {
  border-color: var(--edit-charcoal);
}

.vibe-modern .cover-ornament {
  display: none;
}

.vibe-modern .ornament-line {
  background: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .cover-title :deep(h1) {
  color: var(--edit-white);
}

.vibe-luxe .cover-subtitle :deep(p) {
  color: var(--edit-light);
}

.vibe-luxe .cover-divider {
  background: rgba(201, 169, 98, 0.5);
}

/* Vibe: Warm */
.vibe-warm .frame-corner {
  border-color: var(--edit-burgundy);
}

.vibe-warm .ornament-line {
  background: var(--edit-burgundy);
}

.vibe-warm .ornament-diamond {
  color: var(--edit-burgundy);
}
</style>
