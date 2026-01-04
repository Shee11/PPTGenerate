<!--
  comparison.vue - Handdrawn Comparison Layout
  
  Slots:
    - title: Comparison title
    - left_title, left_content
    - right_title, right_content
    - vs: VS badge (optional)
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="comparison" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="comparison-title">
        <slot name="title" />
      </div>
      
      <!-- Comparison content -->
      <div class="comparison-content">
        <!-- Left side -->
        <div class="compare-side side-left">
          <div class="side-card card-pink">
            <div class="card-header">
              <span class="header-icon">👈</span>
              <div class="header-title">
                <slot name="left_title">
                  <span class="placeholder">Option A</span>
                </slot>
              </div>
            </div>
            <div class="card-body">
              <slot name="left_content">
                <span class="placeholder">Left side content...</span>
              </slot>
            </div>
          </div>
        </div>
        
        <!-- VS Badge -->
        <div class="vs-badge">
          <slot name="vs">
            <span class="vs-text">VS</span>
          </slot>
        </div>
        
        <!-- Right side -->
        <div class="compare-side side-right">
          <div class="side-card card-blue">
            <div class="card-header">
              <span class="header-icon">👉</span>
              <div class="header-title">
                <slot name="right_title">
                  <span class="placeholder">Option B</span>
                </slot>
              </div>
            </div>
            <div class="card-body">
              <slot name="right_content">
                <span class="placeholder">Right side content...</span>
              </slot>
            </div>
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
}>(), {
  theme: 'handdrawn',
  vibe: 'cozy'
})
</script>

<style scoped>
.comparison {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Title */
.comparison-title {
  text-align: center;
  font-family: var(--hand-font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

/* Content */
.comparison-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1.5rem;
  align-items: stretch;
}

/* Side cards */
.compare-side {
  display: flex;
}

.side-card {
  flex: 1;
  padding: 1.5rem;
  border-radius: 8px;
  border: 3px solid;
  box-shadow: 4px 4px 0 var(--hand-shadow-color);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card-pink {
  border-color: var(--hand-pink);
  background: linear-gradient(135deg, var(--hand-pink-light) 0%, var(--hand-bg-cream) 100%);
  transform: rotate(-1deg);
}

.card-blue {
  border-color: var(--hand-blue);
  background: linear-gradient(135deg, var(--hand-blue-light) 0%, var(--hand-bg-cream) 100%);
  transform: rotate(1deg);
}

/* Card header */
.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px dashed currentColor;
  opacity: 0.3;
}

.header-icon {
  font-size: 1.5rem;
}

.header-title {
  font-family: var(--hand-font-display);
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

/* Card body */
.card-body {
  flex: 1;
  font-family: var(--hand-font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--hand-text);
}

.card-body :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0;
}

.card-body :deep(li) {
  padding-left: 1.5rem;
  position: relative;
  margin-bottom: 0.5rem;
}

.card-pink .card-body :deep(li::before) {
  content: '✗';
  position: absolute;
  left: 0;
  color: var(--hand-pink);
  font-weight: bold;
}

.card-blue .card-body :deep(li::before) {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--hand-green);
  font-weight: bold;
}

/* VS Badge */
.vs-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  align-self: center;
}

.vs-text {
  font-family: var(--hand-font-display);
  font-size: 1.8rem;
  font-weight: 900;
  color: var(--hand-bg-cream);
  background: var(--hand-text-dark);
  padding: 0.75rem 1rem;
  border-radius: 50%;
  transform: rotate(-5deg);
  box-shadow: 3px 3px 0 var(--hand-pink);
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 0.9rem;
}

/* Vibe modifiers */
.vibe-minimal .side-card {
  transform: none;
  box-shadow: none;
  border-width: 1px;
  background: var(--hand-bg-cream);
}

.vibe-minimal .vs-text {
  background: transparent;
  color: var(--hand-text-light);
  box-shadow: none;
}

.vibe-playful .side-card:hover {
  transform: scale(1.02) rotate(0deg);
}

.vibe-decorated .side-card::before {
  content: '📋';
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.5rem;
}
</style>
