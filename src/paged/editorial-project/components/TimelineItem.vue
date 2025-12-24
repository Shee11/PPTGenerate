<!--
  TimelineItem.vue - Editorial Timeline Item Component
  
  Props:
    - date: Date/time label
    - title: Event title
    - description: Event description
    - position: Item position (up or down)
-->
<template>
  <div class="timeline-item" :class="`position-${position}`">
    <div class="item-marker"></div>
    <div class="item-content">
      <span class="item-date">{{ date }}</span>
      <h4 class="item-title">{{ title }}</h4>
      <p v-if="description" class="item-description">{{ description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  date: string
  title: string
  description?: string
  position?: 'up' | 'down'
}>(), {
  position: 'up'
})
</script>

<style scoped>
.timeline-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.position-up {
  flex-direction: column;
}

.position-down {
  flex-direction: column-reverse;
}

.item-marker {
  width: 12px;
  height: 12px;
  background: var(--edit-gold);
  border-radius: 50%;
  z-index: 1;
}

.item-content {
  padding: 1rem;
  text-align: center;
  max-width: 180px;
}

.position-up .item-content {
  padding-bottom: 1.5rem;
}

.position-down .item-content {
  padding-top: 1.5rem;
}

.item-date {
  font-family: var(--edit-font-accent);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--edit-gold);
  display: block;
  margin-bottom: 0.5rem;
}

.item-title {
  font-family: var(--edit-font-display);
  font-size: 1rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0 0 0.25rem;
}

.item-description {
  font-family: var(--edit-font-body);
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--edit-text);
  margin: 0;
}
</style>
