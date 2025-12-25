<!--
  IconBox.vue - Business Icon Box Component
  
  Simple icon container with optional label for features/services.
  
  Props:
    - icon: Emoji or icon character
    - label: Text label below icon
    - variant: Style variant (default, outlined, filled, subtle)
    - size: Size variant (sm, md, lg)
-->
<template>
  <div class="icon-box" :class="[`variant-${variant}`, `size-${size}`]">
    <div class="icon-container">
      <slot name="icon">{{ icon }}</slot>
    </div>
    <div v-if="label || $slots.default" class="icon-label">
      <slot>{{ label }}</slot>
    </div>
    <div v-if="$slots.description" class="icon-description">
      <slot name="description" />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  icon: {
    type: String,
    default: '📊',
  },
  label: String,
  variant: {
    type: String,
    default: 'default',
  },
  size: {
    type: String,
    default: 'md',
  },
})
</script>

<style scoped>
.icon-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1.25rem;
  border-radius: var(--radius-card, 8px);
  transition: all 0.2s ease;
}

.icon-box:hover {
  transform: translateY(-2px);
}

.icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 8px;
  background: color-mix(in srgb, var(--c-primary, #0F4C81) 10%, transparent);
  margin-bottom: 0.75rem;
}

.icon-label {
  font-weight: 600;
  color: var(--c-text-primary, #1a1a1a);
  font-size: 0.95rem;
}

.icon-description {
  font-size: 0.85rem;
  color: var(--c-text-secondary, #6b7280);
  margin-top: 0.5rem;
  line-height: 1.5;
}

/* Size variants */
.size-sm .icon-container {
  width: 2.5rem;
  height: 2.5rem;
  font-size: 1.25rem;
}

.size-sm .icon-label {
  font-size: 0.85rem;
}

.size-md .icon-container {
  font-size: 1.75rem;
}

.size-lg .icon-container {
  width: 4.5rem;
  height: 4.5rem;
  font-size: 2.25rem;
}

.size-lg .icon-label {
  font-size: 1.1rem;
}

/* Variant: Outlined */
.variant-outlined {
  border: 1px solid var(--c-border, #e5e7eb);
  background: var(--c-bg-surface, #ffffff);
}

.variant-outlined .icon-container {
  background: transparent;
  border: 2px solid var(--c-primary, #0F4C81);
}

/* Variant: Filled */
.variant-filled {
  background: var(--c-primary, #0F4C81);
}

.variant-filled .icon-container {
  background: rgba(255, 255, 255, 0.2);
}

.variant-filled .icon-label {
  color: white;
}

.variant-filled .icon-description {
  color: rgba(255, 255, 255, 0.8);
}

/* Variant: Subtle */
.variant-subtle {
  background: var(--c-bg-muted, #f9fafb);
}

.variant-subtle:hover {
  background: var(--c-bg-surface, #ffffff);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
</style>
