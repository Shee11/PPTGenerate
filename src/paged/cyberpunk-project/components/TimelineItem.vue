<!--
  TimelineItem.vue - Cyberpunk Timeline Item Widget
  
  Props:
    - date: Date/time label
    - title: Event title
    - description: Event description
    - status: Optional status (complete, active, pending)
-->
<template>
  <div class="timeline-item" :class="`status-${status}`">
    <div class="item-node">
      <div class="node-outer"></div>
      <div class="node-inner"></div>
    </div>
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
  status?: 'complete' | 'active' | 'pending'
}>(), {
  status: 'pending'
})
</script>

<style scoped>
.timeline-item {
  display: flex;
  gap: 1rem;
  padding: 0.75rem 0;
  position: relative;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: 9px;
  top: 2.5rem;
  bottom: -0.75rem;
  width: 2px;
  background: rgba(0, 255, 255, 0.2);
}

.timeline-item:last-child::before {
  display: none;
}

.item-node {
  position: relative;
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.node-outer {
  position: absolute;
  inset: 0;
  border: 2px solid var(--cyber-cyan, #00FFFF);
  border-radius: 50%;
  opacity: 0.5;
}

.node-inner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: var(--cyber-cyan, #00FFFF);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--cyber-cyan-glow);
}

.item-content {
  flex: 1;
  padding-bottom: 0.5rem;
}

.item-date {
  font-family: var(--cyber-font-mono);
  font-size: 0.75rem;
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 5px var(--cyber-magenta-glow);
  display: block;
  margin-bottom: 0.25rem;
}

.item-title {
  font-family: var(--cyber-font-display);
  font-size: 1rem;
  font-weight: 600;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  margin: 0 0 0.25rem 0;
}

.item-description {
  font-family: var(--cyber-font-body);
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--cyber-text, #e0e0e0);
  margin: 0;
}

/* Status modifiers */
.status-complete .node-inner {
  background: var(--cyber-green, #00FF41);
  box-shadow: 0 0 10px var(--cyber-green-glow);
}

.status-complete .node-outer {
  border-color: var(--cyber-green, #00FF41);
}

.status-active .node-inner {
  animation: node-pulse 1.5s ease-in-out infinite;
}

@keyframes node-pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.3); }
}

.status-pending .node-inner {
  background: var(--cyber-text-dim);
  box-shadow: none;
}

.status-pending .node-outer {
  border-color: var(--cyber-text-dim);
}

.status-pending .item-title {
  color: var(--cyber-text-dim);
}
</style>
