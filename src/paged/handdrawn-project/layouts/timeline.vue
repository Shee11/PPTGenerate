<!--
  timeline.vue - Handdrawn Timeline Layout
  
  Slots:
    - title: Timeline title
    - event1_title, event1_content through event4
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="timeline" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="timeline-title">
        <slot name="title" />
        <div class="title-underline"></div>
      </div>
      
      <!-- Timeline track -->
      <div class="timeline-track">
        <!-- Hand-drawn line -->
        <svg class="timeline-line" viewBox="0 0 800 20" preserveAspectRatio="none">
          <path d="M0,10 Q100,5 200,10 T400,10 T600,10 T800,10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="8 4"/>
        </svg>
        
        <!-- Events -->
        <div class="events">
          <div 
            v-for="i in 4" 
            :key="i" 
            class="event"
            :class="[`event-${i}`, i % 2 === 0 ? 'event-up' : 'event-down']"
            :style="{ '--event-index': i }"
          >
            <!-- Marker -->
            <div class="event-marker">
              <span class="marker-emoji">{{ ['🌸', '🌿', '🌼', '🌺'][i-1] }}</span>
            </div>
            
            <!-- Content card -->
            <div class="event-card" :class="`card-${['pink', 'green', 'yellow', 'blue'][i-1]}`">
              <div class="event-title">
                <slot :name="`event${i}_title`">
                  <span class="placeholder">Event {{ i }}</span>
                </slot>
              </div>
              <div class="event-content">
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
}>(), {
  theme: 'handdrawn',
  vibe: 'cozy'
})
</script>

<style scoped>
.timeline {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Title */
.timeline-title {
  text-align: center;
  font-family: var(--hand-font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

.title-underline {
  width: 100px;
  height: 4px;
  margin: 0.5rem auto 0;
  background: repeating-linear-gradient(
    90deg,
    var(--hand-pink) 0,
    var(--hand-pink) 8px,
    transparent 8px,
    transparent 12px
  );
}

/* Timeline track */
.timeline-track {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.timeline-line {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  width: 100%;
  height: 20px;
  transform: translateY(-50%);
  color: var(--hand-text-light);
}

/* Events */
.events {
  flex: 1;
  display: flex;
  justify-content: space-around;
  position: relative;
  z-index: 2;
}

.event {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 22%;
  animation: event-pop 0.4s ease-out backwards;
  animation-delay: calc(var(--event-index) * 0.15s);
}

@keyframes event-pop {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
}

/* Event positioning */
.event-down {
  flex-direction: column;
}

.event-up {
  flex-direction: column-reverse;
}

.event-down .event-card {
  margin-top: 1rem;
}

.event-up .event-card {
  margin-bottom: 1rem;
}

/* Marker */
.event-marker {
  width: 40px;
  height: 40px;
  background: var(--hand-bg-cream);
  border: 3px solid var(--hand-text-light);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
}

.marker-emoji {
  font-size: 1.3rem;
}

/* Event card */
.event-card {
  background: var(--hand-bg-cream);
  padding: 1rem;
  border-radius: 8px;
  border: 2px solid;
  box-shadow: 3px 3px 0 var(--hand-shadow-color);
  text-align: center;
  max-width: 160px;
}

.card-pink {
  border-color: var(--hand-pink);
  transform: rotate(-1deg);
}

.card-green {
  border-color: var(--hand-green);
  transform: rotate(1deg);
}

.card-yellow {
  border-color: var(--hand-yellow-dark);
  transform: rotate(-0.5deg);
}

.card-blue {
  border-color: var(--hand-blue);
  transform: rotate(1.5deg);
}

.event-title {
  font-family: var(--hand-font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  margin-bottom: 0.4rem;
}

.event-content {
  font-family: var(--hand-font-body);
  font-size: 0.85rem;
  line-height: 1.4;
  color: var(--hand-text);
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 0.8rem;
}

/* Vibe modifiers */
.vibe-minimal .event-marker {
  width: 12px;
  height: 12px;
  background: var(--hand-pink);
  border: none;
}

.vibe-minimal .marker-emoji {
  display: none;
}

.vibe-minimal .event-card {
  transform: none;
  box-shadow: none;
  border-width: 1px;
}

.vibe-playful .event:hover .event-card {
  transform: scale(1.05) rotate(0deg);
}

.vibe-decorated .event-card::before {
  content: '✏️';
  position: absolute;
  top: -8px;
  left: 8px;
  font-size: 0.8rem;
}
</style>
