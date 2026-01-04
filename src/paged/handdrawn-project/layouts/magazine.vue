<!--
  magazine.vue - Handdrawn Magazine Layout
  
  Slots:
    - headline: Main headline
    - main: Main content area
    - sidebar: Sidebar content
    - footer: Footer callout
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="magazine" :class="`vibe-${vibe}`">
      <!-- Headline banner -->
      <div v-if="$slots.headline" class="headline-banner">
        <div class="banner-tape tape-left"></div>
        <div class="banner-content">
          <slot name="headline" />
        </div>
        <div class="banner-tape tape-right"></div>
      </div>
      
      <!-- Main content area -->
      <div class="magazine-body">
        <!-- Main column -->
        <div class="main-column">
          <div class="main-paper">
            <slot name="main">
              <span class="placeholder">📰 Main content area</span>
            </slot>
          </div>
        </div>
        
        <!-- Sidebar -->
        <div class="sidebar-column">
          <div class="sidebar-sticky">
            <div class="sticky-pin">📌</div>
            <slot name="sidebar">
              <span class="placeholder">📋 Sidebar</span>
            </slot>
          </div>
        </div>
      </div>
      
      <!-- Footer callout -->
      <div v-if="$slots.footer" class="magazine-footer">
        <div class="footer-ribbon">
          <span class="ribbon-star">★</span>
          <slot name="footer" />
          <span class="ribbon-star">★</span>
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
}>(), {
  theme: 'handdrawn',
  vibe: 'cozy'
})
</script>

<style scoped>
.magazine {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Headline banner */
.headline-banner {
  position: relative;
  background: var(--hand-pink);
  padding: 0.75rem 2rem;
  text-align: center;
}

.banner-content {
  font-family: var(--hand-font-display);
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--hand-bg-cream);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.banner-tape {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 20px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.tape-left {
  left: -20px;
  transform: translateY(-50%) rotate(-10deg);
}

.tape-right {
  right: -20px;
  transform: translateY(-50%) rotate(10deg);
}

/* Magazine body */
.magazine-body {
  flex: 1;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.25rem;
}

/* Main column */
.main-column {
  display: flex;
}

.main-paper {
  flex: 1;
  background: var(--hand-bg-cream);
  border: 2px solid var(--hand-text-light);
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 4px 4px 0 var(--hand-shadow-color);
  transform: rotate(-0.5deg);
}

.main-paper :deep(h2) {
  font-family: var(--hand-font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--hand-text-dark);
  margin: 0 0 0.75rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px dashed var(--hand-pink-light);
}

.main-paper :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--hand-text);
  margin: 0 0 0.75rem 0;
}

.main-paper :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0.4rem;
}

.main-paper :deep(li) {
  font-family: var(--hand-font-body);
  font-size: 0.9rem;
  color: var(--hand-text);
  padding-left: 1.5rem;
  position: relative;
}

.main-paper :deep(li::before) {
  content: '➤';
  position: absolute;
  left: 0;
  color: var(--hand-pink);
  font-size: 0.8rem;
}

/* Sidebar */
.sidebar-column {
  display: flex;
}

.sidebar-sticky {
  flex: 1;
  position: relative;
  background: var(--hand-yellow);
  padding: 1.25rem;
  padding-top: 1.75rem;
  box-shadow: 3px 3px 0 var(--hand-shadow-color);
  transform: rotate(1deg);
}

.sticky-pin {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.3rem;
}

.sidebar-sticky :deep(h3) {
  font-family: var(--hand-font-display);
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  margin: 0 0 0.5rem 0;
}

.sidebar-sticky :deep(p) {
  font-family: var(--hand-font-handwriting);
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--hand-text);
  margin: 0;
}

.sidebar-sticky :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}

.sidebar-sticky :deep(li) {
  font-family: var(--hand-font-handwriting);
  font-size: 0.9rem;
  color: var(--hand-text);
  padding-left: 1.25rem;
  position: relative;
}

.sidebar-sticky :deep(li::before) {
  content: '☐';
  position: absolute;
  left: 0;
}

/* Footer */
.magazine-footer {
  text-align: center;
}

.footer-ribbon {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  font-family: var(--hand-font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  background: var(--hand-green-light);
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  box-shadow: 2px 2px 0 var(--hand-shadow-color);
  transform: rotate(-1deg);
}

.ribbon-star {
  color: var(--hand-yellow-dark);
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 0.9rem;
}

/* Vibe modifiers */
.vibe-minimal .headline-banner {
  background: transparent;
  border-bottom: 1px solid var(--hand-text-light);
}

.vibe-minimal .banner-content {
  color: var(--hand-text-dark);
}

.vibe-minimal .banner-tape {
  display: none;
}

.vibe-minimal .main-paper,
.vibe-minimal .sidebar-sticky {
  box-shadow: none;
  transform: none;
}

.vibe-minimal .sidebar-sticky {
  background: var(--hand-bg-cream);
  border: 1px solid var(--hand-text-light);
}

.vibe-minimal .sticky-pin {
  display: none;
}

.vibe-minimal .footer-ribbon {
  background: transparent;
  box-shadow: none;
  transform: none;
}

.vibe-playful .main-paper:hover {
  transform: rotate(0deg) scale(1.01);
}

.vibe-decorated .main-paper::before {
  content: '📰';
  position: absolute;
  top: -12px;
  left: 12px;
  font-size: 1.3rem;
}
</style>
