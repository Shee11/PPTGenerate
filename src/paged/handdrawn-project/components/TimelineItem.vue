<!--
  TimelineItem.vue - Handdrawn Timeline Item Component
  
  Props:
    - title: Item title
    - date: Date/time text
    - icon: Emoji marker
    - position: up or down
-->
<template>
  <div class="timeline-item" :class="[`position-${position}`, `item-${color}`]">
    <!-- Marker -->
    <div class="item-marker">
      <span class="marker-icon">{{ icon }}</span>
    </div>
    
    <!-- Content card -->
    <div class="item-card">
      <div v-if="date" class="item-date">{{ date }}</div>
      <div v-if="title" class="item-title">{{ title }}</div>
      <div class="item-content">
        <slot>Details go here...</slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title?: string
  date?: string
  icon?: string
  position?: 'up' | 'down'
  color?: 'pink' | 'blue' | 'green' | 'yellow'
}>(), {
  icon: '🌸',
  position: 'down',
  color: 'pink'
})
</script>

<style scoped>
.timeline-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 150px;
}

.position-up {
  flex-direction: column-reverse;
}

/* Marker */
.item-marker {
  width: 45px;
  height: 45px;
  background: var(--hand-bg-cream);
  border: 3px solid var(--hand-text-light);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
}

.marker-icon {
  font-size: 1.3rem;
}

/* Card */
.item-card {
  background: var(--hand-bg-cream);
  padding: 1rem;
  border-radius: 8px;
  border: 2px solid;
  box-shadow: 3px 3px 0 var(--hand-shadow-color);
  text-align: center;
  max-width: 100%;
}

.position-down .item-card {
  margin-top: 1rem;
  transform: rotate(-1deg);
}

.position-up .item-card {
  margin-bottom: 1rem;
  transform: rotate(1deg);
}

.item-pink .item-card { border-color: var(--hand-pink); }
.item-blue .item-card { border-color: var(--hand-blue); }
.item-green .item-card { border-color: var(--hand-green); }
.item-yellow .item-card { border-color: var(--hand-yellow-dark); }

.item-date {
  font-family: var(--hand-font-handwriting);
  font-size: 0.85rem;
  color: var(--hand-text-light);
  margin-bottom: 0.25rem;
}

.item-title {
  font-family: var(--hand-font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  margin-bottom: 0.25rem;
}

.item-content {
  font-family: var(--hand-font-body);
  font-size: 0.85rem;
  line-height: 1.4;
  color: var(--hand-text);
}
</style>
