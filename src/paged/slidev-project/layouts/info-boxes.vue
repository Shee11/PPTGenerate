<!--
  info-boxes.vue - Labeled Information Boxes Layout
  
  Purpose: Display 2-4 labeled content boxes in a grid
  Each box has its own header/title and content area
  Perfect for: principles, features, categories with explanations
  
  Props:
    - theme: Theme name (business, cyber, minimal, academic, creative, dark)
    - vibe: Vibe name (none, calm, dynamic, playful, professional, minimal, dramatic)
    - header: Slide header text
    - footer: Slide footer text
    - boxes: Number of boxes (2, 3, or 4)
  
  Slots:
    - title: Optional section title spanning full width
    - box1_title, box1_content: First box
    - box2_title, box2_content: Second box
    - box3_title, box3_content: Third box (if boxes >= 3)
    - box4_title, box4_content: Fourth box (if boxes >= 4)
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="info-boxes-layout" :class="[`boxes-${boxCount}`, `vibe-${vibe}`]">
      <!-- Section title -->
      <div v-if="$slots.title" class="section-title">
        <slot name="title" />
      </div>
      
      <!-- Boxes grid -->
      <div class="boxes-container">
        <!-- Box 1 -->
        <div v-if="$slots.box1_title || $slots.box1_content" class="info-box">
          <div class="box-header">
            <slot name="box1_title" />
          </div>
          <div class="box-content">
            <slot name="box1_content" />
          </div>
        </div>
        
        <!-- Box 2 -->
        <div v-if="$slots.box2_title || $slots.box2_content" class="info-box">
          <div class="box-header">
            <slot name="box2_title" />
          </div>
          <div class="box-content">
            <slot name="box2_content" />
          </div>
        </div>
        
        <!-- Box 3 -->
        <div v-if="boxCount >= 3 && ($slots.box3_title || $slots.box3_content)" class="info-box">
          <div class="box-header">
            <slot name="box3_title" />
          </div>
          <div class="box-content">
            <slot name="box3_content" />
          </div>
        </div>
        
        <!-- Box 4 -->
        <div v-if="boxCount >= 4 && ($slots.box4_title || $slots.box4_content)" class="info-box">
          <div class="box-header">
            <slot name="box4_title" />
          </div>
          <div class="box-content">
            <slot name="box4_content" />
          </div>
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SlideShell from './SlideShell.vue'

const props = withDefaults(defineProps<{
  theme?: string
  vibe?: string
  header?: string
  footer?: string
  boxes?: 2 | 3 | 4
}>(), {
  theme: 'business',
  vibe: 'none',
  boxes: 2
})

const boxCount = computed(() => Math.max(2, Math.min(4, props.boxes || 2)))
</script>

<style scoped>
.info-boxes-layout {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 2rem;
  gap: 1.5rem;
}

.section-title {
  text-align: center;
  flex-shrink: 0;
}

.section-title :deep(h1),
.section-title :deep(h2),
.section-title :deep(h3) {
  margin: 0;
  color: var(--theme-primary, #3b82f6);
}

.boxes-container {
  flex: 1;
  display: grid;
  gap: 1.5rem;
  min-height: 0;
}

/* 2 boxes: side by side */
.boxes-2 .boxes-container {
  grid-template-columns: 1fr 1fr;
}

/* 3 boxes: top 2, bottom 1 centered */
.boxes-3 .boxes-container {
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}

.boxes-3 .info-box:nth-child(3) {
  grid-column: 1 / -1;
  max-width: 60%;
  justify-self: center;
}

/* 4 boxes: 2x2 grid */
.boxes-4 .boxes-container {
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}

.info-box {
  background: var(--theme-surface, rgba(255, 255, 255, 0.03));
  border: 1px solid var(--theme-border, rgba(255, 255, 255, 0.1));
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow: hidden;
  transition: all 0.3s ease;
}

.info-box:hover {
  border-color: var(--theme-primary, #3b82f6);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.box-header {
  flex-shrink: 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--theme-primary, #3b82f6);
}

.box-header :deep(h3),
.box-header :deep(h4),
.box-header :deep(h5) {
  margin: 0;
  color: var(--theme-primary, #3b82f6);
  font-size: 1.1rem;
  font-weight: 600;
}

.box-content {
  flex: 1;
  overflow: auto;
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--theme-text, #e2e8f0);
}

.box-content :deep(p) {
  margin: 0 0 0.5rem 0;
}

.box-content :deep(ul),
.box-content :deep(ol) {
  margin: 0;
  padding-left: 1.2rem;
}

.box-content :deep(li) {
  margin-bottom: 0.25rem;
}

/* Vibe variations */
.vibe-dynamic .info-box {
  transform: translateY(0);
}

.vibe-dynamic .info-box:hover {
  transform: translateY(-4px);
}

.vibe-playful .info-box:nth-child(odd) {
  transform: rotate(-0.5deg);
}

.vibe-playful .info-box:nth-child(even) {
  transform: rotate(0.5deg);
}

.vibe-minimal .info-box {
  background: transparent;
  border-radius: 0;
  border: none;
  border-left: 3px solid var(--theme-primary, #3b82f6);
}

.vibe-dramatic .info-box {
  background: linear-gradient(135deg, 
    rgba(var(--theme-primary-rgb, 59, 130, 246), 0.1) 0%,
    transparent 100%
  );
}
</style>
