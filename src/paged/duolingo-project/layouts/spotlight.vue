<!--
  spotlight.vue - Duolingo Style Cinematic Spotlight Layout
  
  Purpose: Dramatic center-focused layout with Duolingo's vibrant style
  Perfect for key announcements, achievements, or featured content
  
  Slots: default, subtitle (EXACTLY same as slidev-project)
  Parameters: align: "left" | "center" | "right", intensity: "soft" | "medium" | "strong"
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="spotlight-layout" :class="[`intensity-${intensity}`, `vibe-${vibe}`]">
      <!-- Celebration effect layer -->
      <div class="spotlight-effect"></div>
      
      <!-- Achievement badge background -->
      <div class="achievement-glow"></div>
      
      <!-- Main content area -->
      <div class="content-wrapper">
        <div class="main-content">
          <slot />
        </div>
        <div v-if="$slots.subtitle" class="subtitle-content">
          <slot name="subtitle" />
        </div>
      </div>
      
      <!-- Decorative elements -->
      <div class="decorative-elements">
        <div class="sparkle sparkle-1">✨</div>
        <div class="sparkle sparkle-2">⭐</div>
        <div class="sparkle sparkle-3">🌟</div>
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
  intensity?: 'soft' | 'medium' | 'strong'
}>(), {
  theme: 'duolingo',
  vibe: 'playful',
  intensity: 'medium'
})
</script>

<style scoped>
.spotlight-layout {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 2rem;
  background: var(--theme-bg-base);
}

/* Duolingo-style radial gradient spotlight */
.spotlight-effect {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 60% 60% at center,
    color-mix(in srgb, var(--theme-primary) 15%, transparent),
    transparent
  );
  pointer-events: none;
}

/* Achievement glow ring */
.achievement-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    color-mix(in srgb, var(--theme-golden) 20%, transparent),
    transparent 70%
  );
  pointer-events: none;
}

.content-wrapper {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 80%;
}

.main-content {
  margin-bottom: 1.5rem;
}

.main-content :deep(h1) {
  font-size: 4rem;
  font-weight: 900;
  color: var(--theme-text);
  margin: 0;
  line-height: 1.1;
}

.main-content :deep(h2) {
  font-size: 3rem;
  font-weight: 800;
  color: var(--theme-primary);
  margin: 0;
}

.main-content :deep(p) {
  font-size: 1.5rem;
  color: var(--theme-text-muted);
  font-weight: 600;
}

.subtitle-content {
  background: var(--theme-bg-surface);
  border: 2px solid var(--theme-border);
  border-radius: var(--radius-full);
  padding: 1rem 2rem;
  display: inline-block;
  box-shadow: var(--shadow-card);
}

.subtitle-content :deep(p) {
  margin: 0;
  font-weight: 600;
  color: var(--theme-text-muted);
}

/* Decorative sparkles */
.decorative-elements {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.sparkle {
  position: absolute;
  font-size: 2rem;
  opacity: 0.6;
}

.sparkle-1 { top: 15%; left: 15%; }
.sparkle-2 { top: 20%; right: 20%; }
.sparkle-3 { bottom: 25%; left: 25%; }

/* Intensity variations */
.intensity-soft .spotlight-effect {
  background: radial-gradient(
    ellipse 70% 70% at center,
    color-mix(in srgb, var(--theme-primary) 8%, transparent),
    transparent
  );
}

.intensity-soft .achievement-glow {
  width: 200px;
  height: 200px;
  opacity: 0.5;
}

.intensity-strong .spotlight-effect {
  background: radial-gradient(
    ellipse 50% 50% at center,
    color-mix(in srgb, var(--theme-primary) 25%, transparent),
    transparent
  );
}

.intensity-strong .achievement-glow {
  width: 400px;
  height: 400px;
}

/* === VIBE: MINIMAL === */
.vibe-minimal .spotlight-effect,
.vibe-minimal .achievement-glow,
.vibe-minimal .decorative-elements {
  display: none;
}

.vibe-minimal .content-wrapper {
  max-width: 70%;
}

.vibe-minimal .main-content :deep(h1) {
  font-size: 3rem;
}

.vibe-minimal .subtitle-content {
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 0.5rem 1rem;
}

/* === VIBE: CLEAN === */
.vibe-clean .decorative-elements {
  display: none;
}

.vibe-clean .achievement-glow {
  opacity: 0.3;
}

.vibe-clean .spotlight-effect {
  opacity: 0.5;
}

/* === VIBE: PLAYFUL === */
.vibe-playful .sparkle {
  font-size: 2.5rem;
  opacity: 0.8;
}

.vibe-playful .main-content :deep(h1) {
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.vibe-playful .subtitle-content {
  background: var(--theme-primary);
  color: white;
  border-color: var(--theme-primary-dark);
  box-shadow: 0 4px 0 var(--theme-primary-dark);
}

.vibe-playful .subtitle-content :deep(p) {
  color: white;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive .spotlight-effect {
  background: radial-gradient(
    ellipse 50% 50% at center,
    color-mix(in srgb, var(--theme-primary) 20%, transparent),
    color-mix(in srgb, var(--theme-accent) 10%, transparent) 50%,
    transparent
  );
}

.vibe-expressive .achievement-glow {
  width: 450px;
  height: 450px;
  background: radial-gradient(
    circle,
    color-mix(in srgb, var(--theme-golden) 30%, transparent),
    color-mix(in srgb, var(--theme-warning) 10%, transparent) 50%,
    transparent 70%
  );
}

.vibe-expressive .main-content :deep(h1) {
  font-size: 5rem;
  background: linear-gradient(135deg, 
    var(--theme-primary), 
    var(--theme-accent),
    var(--theme-premium)
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.vibe-expressive .sparkle {
  font-size: 3rem;
}

.vibe-expressive .subtitle-content {
  background: linear-gradient(135deg, var(--theme-golden), var(--theme-warning));
  border: none;
  box-shadow: 0 6px 0 color-mix(in srgb, var(--theme-warning) 70%, black);
  padding: 1.25rem 2.5rem;
}

.vibe-expressive .subtitle-content :deep(p) {
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
</style>
