<!--
  TimelineItem.vue - Duolingo Styled Timeline Entry Component
  
  Playful timeline entry with colorful markers and connectors.
  Use within a flex container for vertical timelines.
  
  Props:
    - title: Item title
    - subtitle: Item subtitle (e.g., date)
    - markerIcon: Emoji for marker
    - markerColor: Color theme (green, blue, orange, purple)
    - position: Marker position (left, right)
    - active: Highlight as active/current
    - last: Is this the last item (hides connector)
-->
<template>
  <div 
    class="timeline-item"
    :class="[`position-${position}`, `color-${markerColor}`, { active, last }]"
  >
    <!-- Connector line -->
    <div class="connector">
      <div class="connector-line"></div>
      <div class="connector-dots">
        <span v-for="i in 3" :key="i" class="dot"></span>
      </div>
    </div>
    
    <!-- Marker -->
    <div class="marker">
      <div class="marker-shadow"></div>
      <div class="marker-inner">
        <slot name="marker">
          <span class="marker-icon">{{ markerIcon }}</span>
        </slot>
      </div>
      <div class="marker-shine"></div>
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
const props = withDefaults(defineProps<{
  title?: string
  subtitle?: string
  markerIcon?: string
  markerColor?: 'green' | 'blue' | 'orange' | 'purple'
  position?: 'left' | 'right'
  active?: boolean
  last?: boolean
}>(), {
  markerIcon: '⭐',
  markerColor: 'green',
  position: 'left',
  active: false,
  last: false
})
</script>

<style scoped>
.timeline-item {
  position: relative;
  display: flex;
  gap: 1.5rem;
  padding-bottom: 2rem;
  font-family: var(--duo-font, 'Nunito', sans-serif);
}

/* Connector */
.connector {
  position: absolute;
  top: 0;
  width: 4px;
  height: 100%;
  z-index: 0;
}

.position-left .connector {
  left: 22px;
}

.position-right .connector {
  right: 22px;
}

.connector-line {
  width: 100%;
  height: 100%;
  background: var(--duo-gray-light, #E5E5E5);
  border-radius: 2px;
}

.connector-dots {
  position: absolute;
  top: 56px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  background: var(--duo-gray, #AFAFAF);
  border-radius: 50%;
  opacity: 0.5;
}

.last .connector {
  display: none;
}

/* Marker */
.marker {
  position: relative;
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  z-index: 1;
}

.marker-shadow {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  transform: translateY(4px);
}

.marker-inner {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.marker-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.marker-shine {
  position: absolute;
  top: 4px;
  left: 8px;
  right: 8px;
  height: 40%;
  background: linear-gradient(180deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 100%);
  border-radius: 50% 50% 0 0;
  pointer-events: none;
}

/* Color variants */
.color-green .marker-shadow {
  background: var(--duo-green-dark, #46a302);
}

.color-green .marker-inner {
  background: var(--duo-green, #58CC02);
}

.color-green .connector-line {
  background: linear-gradient(180deg, var(--duo-green, #58CC02) 0%, var(--duo-gray-light, #E5E5E5) 100%);
}

.color-blue .marker-shadow {
  background: var(--duo-blue-dark, #1899D6);
}

.color-blue .marker-inner {
  background: var(--duo-blue, #1CB0F6);
}

.color-blue .connector-line {
  background: linear-gradient(180deg, var(--duo-blue, #1CB0F6) 0%, var(--duo-gray-light, #E5E5E5) 100%);
}

.color-orange .marker-shadow {
  background: #E68600;
}

.color-orange .marker-inner {
  background: var(--duo-orange, #FF9600);
}

.color-orange .connector-line {
  background: linear-gradient(180deg, var(--duo-orange, #FF9600) 0%, var(--duo-gray-light, #E5E5E5) 100%);
}

.color-purple .marker-shadow {
  background: #B86EE6;
}

.color-purple .marker-inner {
  background: var(--duo-purple, #CE82FF);
}

.color-purple .connector-line {
  background: linear-gradient(180deg, var(--duo-purple, #CE82FF) 0%, var(--duo-gray-light, #E5E5E5) 100%);
}

/* Content */
.content {
  flex: 1;
  padding-top: 0.25rem;
}

.subtitle {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--duo-gray-dark, #777);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.title {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
  margin-bottom: 0.5rem;
}

.description {
  font-size: 1rem;
  font-weight: 600;
  color: var(--duo-text, #4B4B4B);
  line-height: 1.5;
}

.description :deep(p) {
  margin: 0;
}

/* Active state */
.active .marker {
  animation: marker-bounce 1s ease-in-out infinite;
}

@keyframes marker-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.active .marker-inner {
  box-shadow: 0 0 0 4px rgba(88, 204, 2, 0.3);
}

.active .content {
  background: rgba(88, 204, 2, 0.1);
  padding: 1rem;
  border-radius: 16px;
  margin-left: -1rem;
}

/* Position right */
.position-right {
  flex-direction: row-reverse;
  text-align: right;
}

.position-right .content {
  padding-right: 0.25rem;
  padding-left: 0;
}

.position-right.active .content {
  margin-left: 0;
  margin-right: -1rem;
}
</style>
