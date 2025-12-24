<!--
  two-cols-header.vue - Duolingo Style Two Column Layout with Header
  
  Purpose: Two-column content layout with prominent header section
  Features Duolingo's clean design with colorful columns
  
  Slots: header, left, right (EXACTLY same as slidev-project)
  Parameters: ratio: "50-50" | "40-60" | "60-40" | "30-70" | "70-30"
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="two-cols-header-layout" :class="`vibe-${vibe}`">
      <!-- Main title from ::header:: slot -->
      <div class="header-section">
        <slot name="header">
          <h1>Two Columns</h1>
        </slot>
      </div>

      <!-- Two columns content -->
      <div class="columns-container">
        <div class="column column-left" :style="leftColumnStyle">
          <slot name="left">
            <slot />
          </slot>
        </div>
        <div class="column column-right" :style="rightColumnStyle">
          <slot name="right" />
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
  ratio?: string
}>(), {
  theme: 'duolingo',
  vibe: 'playful',
  ratio: '50-50'
})

// Parse ratio into flex values
const ratioValues = computed(() => {
  const ratioMap: Record<string, [number, number]> = {
    '50-50': [1, 1],
    '40-60': [2, 3],
    '60-40': [3, 2],
    '30-70': [3, 7],
    '70-30': [7, 3]
  }
  return ratioMap[props.ratio] || [1, 1]
})

const leftColumnStyle = computed(() => ({
  flex: ratioValues.value[0]
}))

const rightColumnStyle = computed(() => ({
  flex: ratioValues.value[1]
}))
</script>

<style scoped>
.two-cols-header-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 1.5rem;
}

.header-section {
  text-align: center;
  flex-shrink: 0;
}

.header-section :deep(h1) {
  font-size: 2rem;
  font-weight: 800;
  color: var(--theme-text);
  margin: 0;
}

.header-section :deep(h2) {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--theme-primary);
  margin: 0;
}

.columns-container {
  flex: 1;
  display: flex;
  gap: 1rem;
  min-height: 0;
}

.column {
  background: var(--theme-bg-card);
  border: 2px solid var(--theme-border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.column-left {
  border-color: var(--theme-primary);
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--theme-primary) 5%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.column-right {
  border-color: var(--theme-accent);
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--theme-accent) 5%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.column :deep(h1),
.column :deep(h2),
.column :deep(h3),
.column :deep(h4) {
  font-weight: 700;
  margin: 0 0 0.75rem 0;
}

.column-left :deep(h1),
.column-left :deep(h2),
.column-left :deep(h3),
.column-left :deep(h4) {
  color: var(--theme-primary);
}

.column-right :deep(h1),
.column-right :deep(h2),
.column-right :deep(h3),
.column-right :deep(h4) {
  color: var(--theme-accent);
}

.column :deep(p) {
  color: var(--theme-text-muted);
  line-height: 1.6;
  margin: 0 0 0.75rem 0;
}

.column :deep(ul),
.column :deep(ol) {
  margin: 0;
  padding-left: 1.25rem;
}

.column :deep(li) {
  color: var(--theme-text-muted);
  margin-bottom: 0.5rem;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
  gap: 1rem;
}

.vibe-minimal .columns-container {
  gap: 0.75rem;
}

.vibe-minimal .column {
  border-radius: var(--radius-sm);
  border-width: 1px;
  padding: 1rem;
  box-shadow: none;
  background: var(--theme-bg-card);
}

.vibe-minimal .column-left,
.vibe-minimal .column-right {
  border-color: var(--theme-border);
}

.vibe-minimal .header-section :deep(h1) {
  font-size: 1.5rem;
}

/* === VIBE: CLEAN === */
.vibe-clean .column {
  border-width: 1px;
  box-shadow: 0 1px 0 var(--theme-border);
}

.vibe-clean .column-left,
.vibe-clean .column-right {
  background: var(--theme-bg-card);
}

/* === VIBE: PLAYFUL === */
.vibe-playful .header-section :deep(h1) {
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.vibe-playful .column {
  border-radius: var(--radius-xl);
  border-width: 3px;
  box-shadow: 0 4px 0 var(--theme-border);
}

.vibe-playful .column-left {
  box-shadow: 0 4px 0 color-mix(in srgb, var(--theme-primary) 30%, transparent);
  transform: rotate(-0.5deg);
}

.vibe-playful .column-right {
  box-shadow: 0 4px 0 color-mix(in srgb, var(--theme-accent) 30%, transparent);
  transform: rotate(0.5deg);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2rem;
  gap: 1.5rem;
}

.vibe-expressive .columns-container {
  gap: 1.5rem;
}

.vibe-expressive .header-section :deep(h1) {
  font-size: 2.5rem;
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-accent), var(--theme-premium));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.vibe-expressive .column {
  border-radius: var(--radius-xl);
  border-width: 4px;
  padding: 2rem;
}

.vibe-expressive .column-left {
  box-shadow: 0 6px 0 color-mix(in srgb, var(--theme-primary) 40%, transparent);
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-primary) 10%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
  transform: rotate(-1deg);
}

.vibe-expressive .column-right {
  box-shadow: 0 6px 0 color-mix(in srgb, var(--theme-accent) 40%, transparent);
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-accent) 10%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
  transform: rotate(1deg);
}
</style>
