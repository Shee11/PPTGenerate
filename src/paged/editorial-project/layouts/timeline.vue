<!--
  timeline.vue - Editorial Timeline Layout
  
  Slots:
    - title: Timeline title
    - event1_title, event1_content through event4
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="timeline">
      <!-- Title -->
      <div v-if="$slots.title" class="timeline-title">
        <slot name="title" />
      </div>
      
      <!-- Timeline track -->
      <div class="timeline-track">
        <!-- Main line -->
        <div class="track-line"></div>
        
        <!-- Events -->
        <div class="events">
          <div 
            v-for="i in 4" 
            :key="i" 
            class="event"
            :style="{ '--event-index': i }"
          >
            <!-- Marker -->
            <div class="event-marker">
              <div class="marker-dot"></div>
            </div>
            
            <!-- Content -->
            <div class="event-content">
              <div class="event-title">
                <slot :name="`event${i}_title`">
                  <span class="placeholder">Event {{ i }}</span>
                </slot>
              </div>
              <div class="event-body">
                <slot :name="`event${i}_content`">
                  <span class="placeholder">Details...</span>
                </slot>
              </div>
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
  dark?: boolean
}>(), {
  theme: 'editorial',
  vibe: 'classic'
})
</script>

<style scoped>
.timeline {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Title */
.timeline-title {
  text-align: center;
}

.timeline-title :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 2.2rem;
  font-weight: 400;
  color: var(--edit-text-dark);
}

/* Timeline track */
.timeline-track {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.track-line {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--edit-light);
  transform: translateY(-50%);
}

/* Events */
.events {
  flex: 1;
  display: flex;
  justify-content: space-between;
  position: relative;
  z-index: 2;
}

.event {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 22%;
  animation: fade-in 0.5s ease-out backwards;
  animation-delay: calc(var(--event-index) * 0.15s);
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Event positioning - alternate up/down */
.event:nth-child(odd) {
  flex-direction: column;
}

.event:nth-child(even) {
  flex-direction: column-reverse;
}

.event:nth-child(odd) .event-content {
  margin-top: 1.5rem;
}

.event:nth-child(even) .event-content {
  margin-bottom: 1.5rem;
}

/* Marker */
.event-marker {
  display: flex;
  align-items: center;
  justify-content: center;
}

.marker-dot {
  width: 12px;
  height: 12px;
  background: var(--edit-gold);
  border-radius: 50%;
  border: 2px solid var(--edit-bg);
  box-shadow: 0 0 0 1px var(--edit-gold);
}

/* Event content */
.event-content {
  text-align: center;
  max-width: 160px;
}

.event-title {
  font-family: var(--edit-font-display);
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--edit-text-dark);
  margin-bottom: 0.5rem;
}

.event-body {
  font-family: var(--edit-font-body);
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--edit-text);
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
  font-size: 0.85rem;
}

/* Vibe: Modern */
.vibe-modern .marker-dot {
  background: var(--edit-charcoal);
  box-shadow: 0 0 0 1px var(--edit-charcoal);
}

.vibe-modern .track-line {
  background: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .track-line {
  background: var(--edit-slate);
}

.vibe-luxe .marker-dot {
  border-color: var(--edit-charcoal);
}
</style>
