<script setup lang="ts">
/**
 * Feature Grid Layout - Duolingo Style
 * 
 * 3-column grid for up to 6 features.
 * Features Duolingo's playful card design with achievement icons.
 * 
 * Slots: title, feature1, feature2, feature3, feature4, feature5, feature6 (EXACTLY same as slidev-project)
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'playful' | 'expressive'
}>()

const injectedVibe = inject('vibe', computed(() => props.vibe || 'playful'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'playful')
const vibeClass = computed(() => `vibe-${currentVibe.value}`)

// Feature colors and icons
const featureColors = ['#58CC02', '#1CB0F6', '#FF9600', '#CE82FF', '#FF4B4B', '#FFC800']
const featureIcons = ['🎯', '⚡', '🔥', '💎', '🚀', '✨']
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="feature-grid" :class="vibeClass">
      <header v-if="$slots.title" class="feature-title">
        <slot name="title" />
      </header>
      
      <div class="features-container">
        <div v-if="$slots.feature1" class="feature-box" :style="{ '--feature-color': featureColors[0] }">
          <div class="feature-icon">{{ featureIcons[0] }}</div>
          <slot name="feature1" />
        </div>
        <div v-if="$slots.feature2" class="feature-box" :style="{ '--feature-color': featureColors[1] }">
          <div class="feature-icon">{{ featureIcons[1] }}</div>
          <slot name="feature2" />
        </div>
        <div v-if="$slots.feature3" class="feature-box" :style="{ '--feature-color': featureColors[2] }">
          <div class="feature-icon">{{ featureIcons[2] }}</div>
          <slot name="feature3" />
        </div>
        <div v-if="$slots.feature4" class="feature-box" :style="{ '--feature-color': featureColors[3] }">
          <div class="feature-icon">{{ featureIcons[3] }}</div>
          <slot name="feature4" />
        </div>
        <div v-if="$slots.feature5" class="feature-box" :style="{ '--feature-color': featureColors[4] }">
          <div class="feature-icon">{{ featureIcons[4] }}</div>
          <slot name="feature5" />
        </div>
        <div v-if="$slots.feature6" class="feature-box" :style="{ '--feature-color': featureColors[5] }">
          <div class="feature-icon">{{ featureIcons[5] }}</div>
          <slot name="feature6" />
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.feature-grid {
  height: 100%;
  width: 100%;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-title {
  text-align: center;
  font-weight: 800;
  color: var(--theme-text);
}

.feature-title :deep(h1),
.feature-title :deep(h2),
.feature-title :deep(h3) {
  color: var(--theme-text);
  margin: 0;
  font-weight: 800;
}

.features-container {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.feature-box {
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  background: var(--theme-bg-card);
  border: 2px solid var(--theme-border);
  box-shadow: var(--shadow-card);
  color: var(--theme-text);
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Feature icon */
.feature-icon {
  font-size: 2rem;
  width: 56px;
  height: 56px;
  background: color-mix(in srgb, var(--feature-color) 15%, var(--theme-bg-card));
  border: 3px solid var(--feature-color);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 0 color-mix(in srgb, var(--feature-color) 60%, black);
}

.feature-box :deep(h1),
.feature-box :deep(h2),
.feature-box :deep(h3),
.feature-box :deep(h4) {
  color: var(--feature-color, var(--theme-primary));
  font-weight: 700;
  margin: 0;
  font-size: 1.1rem;
}

.feature-box :deep(p) {
  color: var(--theme-text-muted);
  margin: 0;
  line-height: 1.5;
  font-size: 0.95rem;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
  gap: 1rem;
}

.vibe-minimal .features-container {
  gap: 0.75rem;
}

.vibe-minimal .feature-box {
  border-radius: var(--radius-sm);
  border-width: 1px;
  box-shadow: none;
  padding: 1rem;
  gap: 0.5rem;
}

.vibe-minimal .feature-icon {
  font-size: 1.25rem;
  width: 40px;
  height: 40px;
  border-width: 2px;
  border-radius: var(--radius-sm);
  box-shadow: none;
}

/* === VIBE: CLEAN === */
.vibe-clean .feature-box {
  border-width: 1px;
  box-shadow: 0 1px 0 var(--theme-border);
}

.vibe-clean .feature-icon {
  border-width: 2px;
  box-shadow: 0 2px 0 color-mix(in srgb, var(--feature-color) 50%, transparent);
}

/* === VIBE: PLAYFUL === */
.vibe-playful .feature-box {
  border-radius: var(--radius-xl);
  border-width: 3px;
  border-color: var(--feature-color, var(--theme-primary));
  box-shadow: 0 4px 0 color-mix(in srgb, var(--feature-color, var(--theme-primary)) 40%, transparent);
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--feature-color) 8%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-playful .feature-box:nth-child(odd) {
  transform: rotate(-0.5deg);
}

.vibe-playful .feature-box:nth-child(even) {
  transform: rotate(0.5deg);
}

.vibe-playful .feature-icon {
  font-size: 2.25rem;
  width: 64px;
  height: 64px;
  background: var(--feature-color);
  border: none;
  color: white;
  box-shadow: 0 4px 0 color-mix(in srgb, var(--feature-color) 60%, black);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2rem;
  gap: 2rem;
}

.vibe-expressive .features-container {
  gap: 1.5rem;
}

.vibe-expressive .feature-box {
  border-radius: var(--radius-xl);
  border-width: 4px;
  border-color: var(--feature-color, var(--theme-primary));
  box-shadow: 0 6px 0 color-mix(in srgb, var(--feature-color, var(--theme-primary)) 50%, transparent);
  padding: 2rem;
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--feature-color) 12%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-expressive .feature-box:nth-child(odd) {
  transform: rotate(-1deg);
}

.vibe-expressive .feature-box:nth-child(even) {
  transform: rotate(1deg);
}

.vibe-expressive .feature-icon {
  font-size: 2.5rem;
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, var(--feature-color), color-mix(in srgb, var(--feature-color) 70%, white));
  border: none;
  border-radius: var(--radius-xl);
  box-shadow: 0 6px 0 color-mix(in srgb, var(--feature-color) 50%, black);
}

.vibe-expressive .feature-box :deep(h1),
.vibe-expressive .feature-box :deep(h2),
.vibe-expressive .feature-box :deep(h3),
.vibe-expressive .feature-box :deep(h4) {
  font-size: 1.3rem;
}
</style>
