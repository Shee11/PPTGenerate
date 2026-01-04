<!--
  info-boxes.vue - Editorial Info Boxes Layout
  
  Slots:
    - title: Section title
    - box1_title, box1_content through box4
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="info-boxes">
      <!-- Title -->
      <div v-if="$slots.title" class="section-title">
        <slot name="title" />
      </div>
      
      <!-- Boxes grid -->
      <div class="boxes-grid">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="info-box"
          :style="{ '--box-index': i }"
        >
          <div class="box-number">{{ String(i).padStart(2, '0') }}</div>
          <div class="box-header">
            <slot :name="`box${i}_title`">
              <span class="placeholder">Title {{ i }}</span>
            </slot>
          </div>
          <div class="box-divider"></div>
          <div class="box-content">
            <slot :name="`box${i}_content`">
              <span class="placeholder">Content goes here...</span>
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
.info-boxes {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Title */
.section-title {
  text-align: center;
}

.section-title :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 2.2rem;
  font-weight: 400;
  color: var(--edit-text-dark);
}

/* Boxes grid */
.boxes-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.info-box {
  padding: 1.5rem;
  border: 1px solid var(--edit-light);
  background: var(--edit-bg);
  animation: fade-in 0.5s ease-out backwards;
  animation-delay: calc(var(--box-index) * 0.1s);
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Box number */
.box-number {
  font-family: var(--edit-font-display);
  font-size: 0.9rem;
  color: var(--edit-gold);
  margin-bottom: 1rem;
}

/* Box header */
.box-header {
  font-family: var(--edit-font-display);
  font-size: 1.4rem;
  font-weight: 500;
  color: var(--edit-text-dark);
  margin-bottom: 0.75rem;
}

/* Box divider */
.box-divider {
  width: 40px;
  height: 1px;
  background: var(--edit-gold);
  margin-bottom: 0.75rem;
}

/* Box content */
.box-content {
  font-family: var(--edit-font-body);
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--edit-text);
}

.box-content :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0;
}

.box-content :deep(li) {
  padding-left: 1rem;
  position: relative;
  margin-bottom: 0.4rem;
}

.box-content :deep(li::before) {
  content: '—';
  position: absolute;
  left: 0;
  color: var(--edit-gold);
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
  font-size: 0.9rem;
}

/* Vibe: Modern */
.vibe-modern .info-box {
  border-color: var(--edit-charcoal);
}

.vibe-modern .box-divider {
  background: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .info-box {
  background: var(--edit-charcoal);
  border-color: var(--edit-slate);
}

/* Vibe: Warm */
.vibe-warm .info-box {
  background: var(--edit-cream);
  border: none;
}
</style>
