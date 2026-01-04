<!--
  feature-grid.vue - Handdrawn Feature Grid Layout
  
  Slots:
    - title: Grid title
    - feature1 through feature4: Feature content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="feature-grid" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="feature-title">
        <div class="title-bracket">[</div>
        <slot name="title" />
        <div class="title-bracket">]</div>
      </div>
      
      <!-- Features -->
      <div class="features-container">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="feature-box"
          :class="`feature-${i}`"
          :style="{ '--feature-index': i }"
        >
          <!-- Icon circle -->
          <div class="feature-icon">
            <span class="icon-emoji">{{ ['🌟', '🎯', '💎', '🚀'][i-1] }}</span>
          </div>
          
          <!-- Content -->
          <div class="feature-content">
            <slot :name="`feature${i}`">
              <h3>Feature {{ i }}</h3>
              <p>Description goes here...</p>
            </slot>
          </div>
          
          <!-- Connector line -->
          <div v-if="i < 4" class="feature-connector">
            <svg viewBox="0 0 50 20" class="connector-line">
              <path d="M0,10 Q25,5 50,10" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="4 2"/>
            </svg>
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
.feature-grid {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Title */
.feature-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-family: var(--hand-font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

.title-bracket {
  font-family: var(--hand-font-handwriting);
  font-size: 2.5rem;
  color: var(--hand-pink);
}

/* Features container */
.features-container {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.feature-box {
  position: relative;
  background: var(--hand-bg-cream);
  border: 2px solid var(--hand-text-light);
  border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  animation: feature-appear 0.5s ease-out backwards;
  animation-delay: calc(var(--feature-index) * 0.1s);
}

@keyframes feature-appear {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
}

.feature-1 {
  border-color: var(--hand-pink);
  transform: rotate(-0.5deg);
}

.feature-2 {
  border-color: var(--hand-blue);
  transform: rotate(0.5deg);
}

.feature-3 {
  border-color: var(--hand-green);
  transform: rotate(0.5deg);
}

.feature-4 {
  border-color: var(--hand-yellow-dark);
  transform: rotate(-0.5deg);
}

/* Icon */
.feature-icon {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  background: var(--hand-bg-cream);
  border: 3px solid currentColor;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-1 .feature-icon { border-color: var(--hand-pink); }
.feature-2 .feature-icon { border-color: var(--hand-blue); }
.feature-3 .feature-icon { border-color: var(--hand-green); }
.feature-4 .feature-icon { border-color: var(--hand-yellow-dark); }

.icon-emoji {
  font-size: 1.5rem;
}

/* Content */
.feature-content {
  flex: 1;
}

.feature-content :deep(h3) {
  font-family: var(--hand-font-display);
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  margin: 0 0 0.5rem 0;
}

.feature-content :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--hand-text);
  margin: 0;
}

.feature-content :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0 0;
}

.feature-content :deep(li) {
  font-family: var(--hand-font-body);
  font-size: 0.85rem;
  color: var(--hand-text);
  padding-left: 1.25rem;
  position: relative;
  margin-bottom: 0.25rem;
}

.feature-content :deep(li::before) {
  content: '•';
  position: absolute;
  left: 0.25rem;
  color: var(--hand-pink);
}

/* Connector */
.feature-connector {
  position: absolute;
  color: var(--hand-text-light);
  opacity: 0.5;
}

.feature-1 .feature-connector {
  right: -40px;
  top: 50%;
  transform: translateY(-50%);
}

.feature-2 .feature-connector {
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%) rotate(90deg);
}

.feature-3 .feature-connector {
  right: -40px;
  top: 50%;
  transform: translateY(-50%);
}

.connector-line {
  width: 40px;
  height: 20px;
}

/* Vibe modifiers */
.vibe-minimal .feature-box {
  border-radius: 8px;
  border-width: 1px;
  transform: none;
}

.vibe-minimal .feature-connector {
  display: none;
}

.vibe-playful .feature-box:hover {
  transform: scale(1.02) rotate(0deg);
}

.vibe-playful .feature-icon {
  animation: icon-wiggle 2s ease-in-out infinite;
  animation-delay: calc(var(--feature-index) * 0.3s);
}

@keyframes icon-wiggle {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-5deg); }
  75% { transform: rotate(5deg); }
}

.vibe-decorated .feature-box::before {
  content: '✨';
  position: absolute;
  top: -10px;
  right: 10px;
  font-size: 1rem;
}
</style>
