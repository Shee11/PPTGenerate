<!--
  ListItem.vue - Business List Item Component
  
  Styled list item with icon/bullet and content.
  
  Props:
    - icon: Icon/emoji to show
    - bullet: Use bullet instead of icon (circle, check, arrow, number)
    - number: Number for numbered lists
-->
<template>
  <li class="list-item" :class="[bullet ? `bullet-${bullet}` : '']">
    <span class="list-marker">
      <template v-if="icon">{{ icon }}</template>
      <template v-else-if="bullet === 'check'">✓</template>
      <template v-else-if="bullet === 'arrow'">→</template>
      <template v-else-if="bullet === 'number'">{{ number }}.</template>
      <template v-else-if="bullet === 'circle'">●</template>
    </span>
    <span class="list-content">
      <slot />
    </span>
  </li>
</template>

<script setup>
const props = defineProps({
  icon: String,
  bullet: {
    type: String,
    default: 'circle',
  },
  number: [String, Number],
})
</script>

<style scoped>
.list-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.5rem 0;
  list-style: none;
}

.list-marker {
  flex-shrink: 0;
  font-size: 1rem;
  color: var(--c-primary, #0F4C81);
  min-width: 1.25rem;
}

.list-content {
  flex: 1;
  color: var(--c-text-primary, #1a1a1a);
  line-height: 1.5;
}

/* Bullet: Circle */
.bullet-circle .list-marker {
  font-size: 0.5rem;
  margin-top: 0.5rem;
}

/* Bullet: Check */
.bullet-check .list-marker {
  color: #16a34a;
  font-weight: bold;
}

/* Bullet: Arrow */
.bullet-arrow .list-marker {
  font-weight: 500;
}

/* Bullet: Number */
.bullet-number .list-marker {
  font-weight: 600;
  color: var(--c-text-primary, #1a1a1a);
}
</style>
