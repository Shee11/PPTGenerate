<!--
  info-boxes.vue - Duolingo Style Labeled Information Boxes
  
  Purpose: Display 2-4 labeled content boxes in a grid
  Each box has its own header/title and content area
  Features Duolingo's playful card design with accent colors
  
  Slots: title, box1_title, box1_content, box2_title, box2_content, 
         box3_title, box3_content, box4_title, box4_content
         (EXACTLY same as slidev-project)
  Parameters: boxes: 2 | 3 | 4
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
        <div v-if="$slots.box1_title || $slots.box1_content" class="info-box" :style="{ '--box-color': boxColors[0] }">
          <div class="box-number">1</div>
          <div class="box-header">
            <slot name="box1_title" />
          </div>
          <div class="box-content">
            <slot name="box1_content" />
          </div>
        </div>
        
        <!-- Box 2 -->
        <div v-if="$slots.box2_title || $slots.box2_content" class="info-box" :style="{ '--box-color': boxColors[1] }">
          <div class="box-number">2</div>
          <div class="box-header">
            <slot name="box2_title" />
          </div>
          <div class="box-content">
            <slot name="box2_content" />
          </div>
        </div>
        
        <!-- Box 3 -->
        <div v-if="boxCount >= 3 && ($slots.box3_title || $slots.box3_content)" class="info-box" :style="{ '--box-color': boxColors[2] }">
          <div class="box-number">3</div>
          <div class="box-header">
            <slot name="box3_title" />
          </div>
          <div class="box-content">
            <slot name="box3_content" />
          </div>
        </div>
        
        <!-- Box 4 -->
        <div v-if="boxCount >= 4 && ($slots.box4_title || $slots.box4_content)" class="info-box" :style="{ '--box-color': boxColors[3] }">
          <div class="box-number">4</div>
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
  theme: 'duolingo',
  vibe: 'playful',
  boxes: 2
})

const boxCount = computed(() => Math.max(2, Math.min(4, props.boxes || 2)))

// Duolingo accent colors for each box
const boxColors = ['#58CC02', '#1CB0F6', '#FF9600', '#CE82FF']
</script>

<style scoped>
.info-boxes-layout {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
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
  color: var(--theme-text);
  font-weight: 800;
}

.boxes-container {
  flex: 1;
  display: grid;
  gap: 1rem;
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
  background: var(--theme-bg-card);
  border: 2px solid var(--theme-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  position: relative;
  overflow: hidden;
}

/* Duolingo-style numbered badge */
.box-number {
  position: absolute;
  top: -2px;
  left: -2px;
  width: 36px;
  height: 36px;
  background: var(--box-color, var(--theme-primary));
  color: white;
  font-weight: 800;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0 0 var(--radius-md) 0;
  box-shadow: 0 2px 0 color-mix(in srgb, var(--box-color, var(--theme-primary)) 80%, black);
}

.box-header {
  padding-left: 2rem;
  color: var(--box-color, var(--theme-primary));
  font-weight: 700;
}

.box-header :deep(h1),
.box-header :deep(h2),
.box-header :deep(h3),
.box-header :deep(h4) {
  margin: 0;
  color: var(--box-color, var(--theme-primary));
  font-weight: 700;
  font-size: 1.1rem;
}

.box-content {
  flex: 1;
  color: var(--theme-text-muted);
  line-height: 1.6;
}

.box-content :deep(p) {
  margin: 0;
}

.box-content :deep(ul),
.box-content :deep(ol) {
  margin: 0;
  padding-left: 1.25rem;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
  gap: 1rem;
}

.vibe-minimal .boxes-container {
  gap: 0.75rem;
}

.vibe-minimal .info-box {
  border-radius: var(--radius-sm);
  border-width: 1px;
  box-shadow: none;
  padding: 1rem;
}

.vibe-minimal .box-number {
  width: 24px;
  height: 24px;
  font-size: 0.85rem;
}

/* === VIBE: CLEAN === */
.vibe-clean .info-box {
  border-width: 1px;
  box-shadow: 0 1px 0 var(--theme-border);
}

.vibe-clean .box-number {
  width: 30px;
  height: 30px;
  font-size: 1rem;
}

/* === VIBE: PLAYFUL === */
.vibe-playful .info-box {
  border-radius: var(--radius-xl);
  border-width: 3px;
  border-color: var(--box-color, var(--theme-primary));
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--box-color) 5%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-playful .box-number {
  width: 40px;
  height: 40px;
  font-size: 1.25rem;
  border-radius: 0 0 var(--radius-lg) 0;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2rem;
  gap: 2rem;
}

.vibe-expressive .boxes-container {
  gap: 1.5rem;
}

.vibe-expressive .info-box {
  border-radius: var(--radius-xl);
  border-width: 4px;
  border-color: var(--box-color, var(--theme-primary));
  box-shadow: 0 6px 0 color-mix(in srgb, var(--box-color, var(--theme-primary)) 60%, transparent);
  padding: 2rem;
}

.vibe-expressive .box-number {
  width: 48px;
  height: 48px;
  font-size: 1.5rem;
  border-radius: 0 0 var(--radius-xl) 0;
}

.vibe-expressive .box-header :deep(h1),
.vibe-expressive .box-header :deep(h2),
.vibe-expressive .box-header :deep(h3),
.vibe-expressive .box-header :deep(h4) {
  font-size: 1.4rem;
}
</style>
