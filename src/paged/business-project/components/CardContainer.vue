<!--
  CardContainer.vue - Business Card Container Component
  
  Flexible card container for grouping content.
  
  Props:
    - title: Optional card title
    - variant: Style variant (default, elevated, bordered, flat)
    - padding: Padding size (sm, md, lg)
-->
<template>
  <div class="card-container" :class="[`variant-${variant}`, `padding-${padding}`]">
    <div v-if="title || $slots.header" class="card-header">
      <slot name="header">
        <h3 class="card-title">{{ title }}</h3>
      </slot>
    </div>
    <div class="card-body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  variant: {
    type: String,
    default: 'default',
  },
  padding: {
    type: String,
    default: 'md',
  },
})
</script>

<style scoped>
.card-container {
  background: var(--c-bg-surface, #ffffff);
  border-radius: var(--radius-card, 8px);
  border: 1px solid var(--c-border, #e5e7eb);
  overflow: hidden;
}

/* Padding variants */
.padding-sm {
  padding: 1rem;
}

.padding-md {
  padding: 1.5rem;
}

.padding-lg {
  padding: 2rem;
}

.card-header {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--c-border, #e5e7eb);
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--c-text-primary, #1a1a1a);
  margin: 0;
}

.card-body {
  color: var(--c-text-primary, #1a1a1a);
}

.card-footer {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--c-border, #e5e7eb);
}

/* Variant: Elevated */
.variant-elevated {
  border: none;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.variant-elevated:hover {
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Variant: Bordered */
.variant-bordered {
  border: 2px solid var(--c-primary, #0F4C81);
}

/* Variant: Flat */
.variant-flat {
  background: var(--c-bg-muted, #f9fafb);
  border: none;
}

/* Variant: Accent */
.variant-accent {
  border-top: 4px solid var(--c-primary, #0F4C81);
}
</style>
