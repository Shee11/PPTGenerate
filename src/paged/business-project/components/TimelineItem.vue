<!--
  TimelineItem.vue - Business Timeline Item Component
  
  Timeline entry for roadmaps, milestones, and history.
  
  Props:
    - title: Item title
    - date: Date or time label
    - description: Optional description
    - status: Status indicator (pending, active, completed)
    - icon: Optional icon/emoji
-->
<template>
  <div class="timeline-item" :class="[`status-${status}`]">
    <div class="timeline-marker">
      <div class="marker-dot">
        <span v-if="icon" class="marker-icon">{{ icon }}</span>
        <span v-else-if="status === 'completed'" class="marker-check">✓</span>
      </div>
      <div class="marker-line"></div>
    </div>
    <div class="timeline-content">
      <div class="timeline-header">
        <h4 class="timeline-title">{{ title }}</h4>
        <span v-if="date" class="timeline-date">{{ date }}</span>
      </div>
      <p v-if="description" class="timeline-description">{{ description }}</p>
      <div v-if="$slots.default" class="timeline-body">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  date: String,
  description: String,
  status: {
    type: String,
    default: 'pending',
  },
  icon: String,
})
</script>

<style scoped>
.timeline-item {
  display: flex;
  gap: 1rem;
  position: relative;
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.marker-dot {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: var(--c-bg-muted, #e5e7eb);
  border: 2px solid var(--c-border, #d1d5db);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  z-index: 1;
}

.marker-icon {
  font-size: 1rem;
}

.marker-check {
  color: white;
  font-weight: bold;
  font-size: 0.8rem;
}

.marker-line {
  width: 2px;
  flex: 1;
  min-height: 2rem;
  background: var(--c-border, #e5e7eb);
  margin-top: 0.5rem;
}

.timeline-item:last-child .marker-line {
  display: none;
}

.timeline-content {
  flex: 1;
  padding-bottom: 1.5rem;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.timeline-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--c-text-primary, #1a1a1a);
  margin: 0;
}

.timeline-date {
  font-size: 0.8rem;
  color: var(--c-text-secondary, #6b7280);
  white-space: nowrap;
}

.timeline-description {
  font-size: 0.9rem;
  color: var(--c-text-secondary, #6b7280);
  line-height: 1.5;
  margin: 0;
}

.timeline-body {
  margin-top: 0.75rem;
}

/* Status: Active */
.status-active .marker-dot {
  background: color-mix(in srgb, var(--c-primary, #0F4C81) 15%, white);
  border-color: var(--c-primary, #0F4C81);
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--c-primary, #0F4C81) 15%, transparent);
}

.status-active .timeline-title {
  color: var(--c-primary, #0F4C81);
}

/* Status: Completed */
.status-completed .marker-dot {
  background: var(--c-primary, #0F4C81);
  border-color: var(--c-primary, #0F4C81);
}

.status-completed .marker-line {
  background: var(--c-primary, #0F4C81);
}

/* Status: Pending */
.status-pending .marker-dot {
  background: var(--c-bg-surface, #ffffff);
}

.status-pending .timeline-title {
  color: var(--c-text-secondary, #6b7280);
}
</style>
