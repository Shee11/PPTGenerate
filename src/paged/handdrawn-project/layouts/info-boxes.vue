<!--
  info-boxes.vue - Handdrawn Info Boxes Layout
  
  Slots:
    - title: Section title
    - box1_title, box1_content through box4
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="info-boxes" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="section-title">
        <span class="title-deco">✿</span>
        <slot name="title" />
        <span class="title-deco">✿</span>
      </div>
      
      <!-- Boxes grid -->
      <div class="boxes-grid">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="info-box"
          :class="`box-${i}`"
          :style="{ '--box-index': i }"
        >
          <div class="box-header">
            <span class="box-icon">{{ ['📝', '💡', '🎯', '⭐'][i-1] }}</span>
            <div class="box-title">
              <slot :name="`box${i}_title`">
                <span class="placeholder">Title {{ i }}</span>
              </slot>
            </div>
          </div>
          <div class="box-content">
            <slot :name="`box${i}_content`">
              <span class="placeholder">Content goes here...</span>
            </slot>
          </div>
          <div class="box-corner"></div>
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
.info-boxes {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Title */
.section-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-family: var(--hand-font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

.title-deco {
  color: var(--hand-pink);
  font-size: 1.5rem;
}

/* Boxes grid */
.boxes-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.info-box {
  position: relative;
  background: var(--hand-bg-cream);
  border: 2px solid var(--hand-text-light);
  border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  animation: box-appear 0.5s ease-out backwards;
  animation-delay: calc(var(--box-index) * 0.1s);
}

@keyframes box-appear {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
}

/* Box colors */
.box-1 { border-color: var(--hand-pink); }
.box-2 { border-color: var(--hand-blue); }
.box-3 { border-color: var(--hand-green); }
.box-4 { border-color: var(--hand-yellow-dark); }

/* Box header */
.box-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.box-icon {
  font-size: 1.5rem;
}

.box-title {
  font-family: var(--hand-font-display);
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--hand-text-dark);
}

/* Box content */
.box-content {
  flex: 1;
  font-family: var(--hand-font-body);
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--hand-text);
}

.box-content :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0;
}

.box-content :deep(li) {
  padding-left: 1.25rem;
  position: relative;
  margin-bottom: 0.3rem;
}

.box-content :deep(li::before) {
  content: '♦';
  position: absolute;
  left: 0;
  color: var(--hand-pink);
  font-size: 0.7rem;
}

/* Box corner fold */
.box-corner {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, transparent 50%, var(--hand-shadow-color) 50%);
  border-radius: 0 0 15px 0;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 0.9rem;
}

/* Vibe modifiers */
.vibe-minimal .box-corner,
.vibe-minimal .box-icon {
  display: none;
}

.vibe-minimal .info-box {
  border-radius: 8px;
  border-width: 1px;
}

.vibe-playful .info-box:hover {
  transform: rotate(-1deg) scale(1.02);
}

.vibe-decorated .info-box::before {
  content: '✨';
  position: absolute;
  top: -10px;
  right: 10px;
  font-size: 1rem;
}
</style>
