<!--
  TimelineItem.vue - Styled Timeline Entry Component
  
  Individual timeline entry with connector and marker.
  Use within a flex container for vertical timelines.
  
  Props:
    - title: Item title
    - subtitle: Item subtitle (e.g., date)
    - markerIcon: Emoji or text for marker
    - markerColor: Marker background color
    - position: Marker position (left, right)
    - active: Highlight as active/current
    - last: Is this the last item (hides connector)
-->
<template>
  <div 
    class="timeline-item"
    :class="[`position-${position}`, { active, last }]"
    :style="itemStyles"
  >
    <!-- Connector line -->
    <div class="connector">
      <div class="connector-line"></div>
    </div>
    
    <!-- Marker -->
    <div class="marker">
      <div class="marker-glow"></div>
      <div class="marker-inner">
        <slot name="marker">
          <span class="marker-icon">{{ markerIcon }}</span>
        </slot>
      </div>
      <div class="marker-ring"></div>
    </div>
    
    <!-- Content -->
    <div class="content">
      <div v-if="subtitle" class="subtitle">{{ subtitle }}</div>
      <div v-if="title" class="title">{{ title }}</div>
      <div class="description">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  title?: string
  subtitle?: string
  markerIcon?: string
  markerColor?: string
  position?: 'left' | 'right'
  active?: boolean
  last?: boolean
}>(), {
  markerIcon: '●',
  markerColor: 'var(--c-primary)',
  position: 'left',
  active: false,
  last: false
})

const itemStyles = computed(() => ({
  '--marker-color': props.markerColor
}))
</script>

<style scoped>
.timeline-item {
  position: relative;
  display: flex;
  gap: 1.25rem;
  padding-bottom: 2rem;
}

/* Connector */
.connector {
  position: absolute;
  top: 0;
  width: 2px;
  height: 100%;
  z-index: 0;
}

.position-left .connector {
  left: 19px;
}

.position-right .connector {
  right: 19px;
}

.connector-line {
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, var(--marker-color), rgba(255,255,255,0.1));
  opacity: 0.3;
}

.last .connector-line {
  height: 50%;
}

/* Marker */
.marker {
  position: relative;
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.marker-glow {
  position: absolute;
  inset: -5px;
  background: var(--marker-color);
  opacity: 0;
  filter: blur(10px);
  border-radius: 50%;
  transition: opacity 0.3s ease;
}

.timeline-item:hover .marker-glow,
.active .marker-glow {
  opacity: 0.3;
}

.marker-inner {
  width: 40px;
  height: 40px;
  background: var(--marker-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  color: white;
  transition: all 0.3s ease;
}

.marker-icon {
  filter: brightness(0) invert(1);
}

.marker-ring {
  position: absolute;
  inset: -4px;
  border: 2px solid var(--marker-color);
  border-radius: 50%;
  opacity: 0;
  transition: all 0.3s ease;
}

.timeline-item:hover .marker-ring,
.active .marker-ring {
  opacity: 0.5;
  inset: -8px;
}

/* Content */
.content {
  flex: 1;
  padding-top: 0.25rem;
}

.subtitle {
  font-size: 0.75rem;
  color: var(--marker-color);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--c-text-main);
  margin-bottom: 0.5rem;
}

.description {
  font-size: 0.9rem;
  color: var(--c-text-muted);
  line-height: 1.6;
}

.description :deep(p) {
  margin: 0;
}

.description :deep(ul) {
  margin: 0.5rem 0 0;
  padding-left: 1.25rem;
}

.description :deep(li) {
  margin-bottom: 0.25rem;
}

/* Active state */
.active .marker-inner {
  transform: scale(1.1);
  box-shadow: 0 0 20px var(--marker-color);
}

.active .title {
  color: var(--marker-color);
}

/* Position right */
.position-right {
  flex-direction: row-reverse;
  text-align: right;
}

.position-right .content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
</style>
