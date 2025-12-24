<!--
  comparison.vue - Editorial Comparison Layout
  
  Slots:
    - title: Comparison title
    - left_title, left_content
    - right_title, right_content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="comparison">
      <!-- Title -->
      <div v-if="$slots.title" class="comparison-title">
        <slot name="title" />
      </div>
      
      <!-- Comparison content -->
      <div class="comparison-content">
        <!-- Left side -->
        <div class="compare-side side-left">
          <div class="side-header">
            <slot name="left_title">
              <span class="placeholder">Option A</span>
            </slot>
          </div>
          <div class="side-divider"></div>
          <div class="side-body">
            <slot name="left_content">
              <span class="placeholder">Left side content...</span>
            </slot>
          </div>
        </div>
        
        <!-- Center divider -->
        <div class="center-divider">
          <div class="divider-line"></div>
          <div class="divider-text">vs</div>
          <div class="divider-line"></div>
        </div>
        
        <!-- Right side -->
        <div class="compare-side side-right">
          <div class="side-header">
            <slot name="right_title">
              <span class="placeholder">Option B</span>
            </slot>
          </div>
          <div class="side-divider"></div>
          <div class="side-body">
            <slot name="right_content">
              <span class="placeholder">Right side content...</span>
            </slot>
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
  header?: string
  footer?: string
  dark?: boolean
}>(), {
  theme: 'editorial',
  vibe: 'classic'
})
</script>

<style scoped>
.comparison {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Title */
.comparison-title {
  text-align: center;
}

.comparison-title :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 2.2rem;
  font-weight: 400;
  color: var(--edit-text-dark);
}

/* Content */
.comparison-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 2rem;
  align-items: start;
}

/* Side */
.compare-side {
  padding: 1.5rem;
}

.side-header {
  font-family: var(--edit-font-display);
  font-size: 1.6rem;
  font-weight: 500;
  color: var(--edit-text-dark);
  margin-bottom: 1rem;
}

.side-divider {
  width: 50px;
  height: 1px;
  background: var(--edit-gold);
  margin-bottom: 1rem;
}

.side-body {
  font-family: var(--edit-font-body);
  font-size: 1rem;
  line-height: 1.7;
  color: var(--edit-text);
}

.side-body :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0;
}

.side-body :deep(li) {
  padding-left: 1.25rem;
  position: relative;
  margin-bottom: 0.5rem;
}

.side-body :deep(li::before) {
  content: '—';
  position: absolute;
  left: 0;
  color: var(--edit-gold);
}

/* Center divider */
.center-divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem 0;
}

.divider-line {
  width: 1px;
  height: 80px;
  background: var(--edit-light);
}

.divider-text {
  font-family: var(--edit-font-accent);
  font-style: italic;
  font-size: 0.9rem;
  color: var(--edit-text-light);
  text-transform: lowercase;
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
  font-size: 0.9rem;
}

/* Vibe: Modern */
.vibe-modern .side-divider {
  background: var(--edit-charcoal);
}

.vibe-modern .divider-line {
  background: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .divider-line {
  background: var(--edit-slate);
}

/* Vibe: Warm */
.vibe-warm .compare-side {
  background: var(--edit-cream);
}
</style>
