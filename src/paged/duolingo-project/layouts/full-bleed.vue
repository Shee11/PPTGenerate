<script setup lang="ts">
/**
 * Full Bleed Layout - Duolingo Style
 * 
 * Full-width content with optional alignment.
 * Features Duolingo's clean design with card-based content.
 * 
 * Slots: default (EXACTLY same as slidev-project)
 * Parameters: align: "top" | "center" | "bottom"
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  align?: 'top' | 'center' | 'bottom'
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'playful' | 'expressive'
}>()

const injectedVibe = inject('vibe', computed(() => props.vibe || 'playful'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'playful')

const alignmentStyle = computed(() => {
  const align = props.align || 'center'
  const alignMap = {
    top: 'flex-start',
    center: 'center',
    bottom: 'flex-end'
  }
  return {
    justifyContent: alignMap[align] || 'center'
  }
})

const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="full-bleed" :class="vibeClass" :style="alignmentStyle">
      <div class="content-wrapper">
        <slot />
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.full-bleed {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 2rem;
  color: var(--theme-text);
}

.content-wrapper {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  background: var(--theme-bg-card);
  border-radius: var(--radius-lg);
  border: 2px solid var(--theme-border);
  box-shadow: var(--shadow-card);
}

.content-wrapper :deep(h1) {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--theme-text);
  margin: 0 0 1rem 0;
}

.content-wrapper :deep(h2) {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--theme-primary);
  margin: 0 0 1rem 0;
}

.content-wrapper :deep(p) {
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--theme-text-muted);
  margin: 0 0 1rem 0;
}

.content-wrapper :deep(ul),
.content-wrapper :deep(ol) {
  margin: 0 0 1rem 0;
  padding-left: 1.5rem;
}

.content-wrapper :deep(li) {
  margin-bottom: 0.5rem;
  color: var(--theme-text-muted);
  line-height: 1.6;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
}

.vibe-minimal .content-wrapper {
  padding: 1.5rem;
  max-width: 100%;
  background: transparent;
  border: none;
  border-radius: 0;
  box-shadow: none;
}

.vibe-minimal .content-wrapper :deep(h1) {
  font-size: 2rem;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.5rem;
}

.vibe-clean .content-wrapper {
  padding: 1.75rem;
  border-radius: var(--radius-md);
  border-width: 1px;
  box-shadow: 0 1px 0 var(--theme-border);
}

/* === VIBE: PLAYFUL === */
.vibe-playful .content-wrapper {
  border-radius: var(--radius-xl);
  border-width: 3px;
  border-color: var(--theme-primary);
  box-shadow: 0 4px 0 color-mix(in srgb, var(--theme-primary) 30%, transparent);
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--theme-primary) 5%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-playful .content-wrapper :deep(h1) {
  color: var(--theme-primary);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2.5rem;
}

.vibe-expressive .content-wrapper {
  padding: 2.5rem;
  border-radius: var(--radius-xl);
  border-width: 4px;
  border-color: var(--theme-primary);
  box-shadow: 0 6px 0 color-mix(in srgb, var(--theme-primary) 40%, transparent);
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-primary) 8%, var(--theme-bg-card)),
    var(--theme-bg-card),
    color-mix(in srgb, var(--theme-accent) 8%, var(--theme-bg-card))
  );
}

.vibe-expressive .content-wrapper :deep(h1) {
  font-size: 3rem;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.vibe-expressive .content-wrapper :deep(h2) {
  font-size: 2rem;
}
</style>
