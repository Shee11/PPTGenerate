<!--
  QuoteWidget.vue - Business Quote Component
  
  Professional quote/testimonial display for presentations.
  
  Props:
    - text: Quote text
    - author: Author name
    - attribution: Title, company, etc.
    - variant: Style variant
-->
<template>
  <div class="quote-widget" :class="variant">
    <div class="quote-mark" v-if="showIcon">"</div>
    <blockquote class="quote-content">
      <p class="quote-text">{{ text }}</p>
      <footer v-if="author || attribution" class="quote-footer">
        <cite>
          <span v-if="author" class="quote-author">{{ author }}</span>
          <span v-if="attribution" class="quote-attribution">{{ attribution }}</span>
        </cite>
      </footer>
    </blockquote>
  </div>
</template>

<script setup>
const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  author: String,
  attribution: String,
  variant: {
    type: String,
    default: 'default',
  },
  showIcon: {
    type: Boolean,
    default: true,
  },
})
</script>

<style scoped>
.quote-widget {
  position: relative;
  background: var(--c-bg-surface, #ffffff);
  border-radius: var(--radius-card, 8px);
  padding: 2rem;
  border: 1px solid var(--c-border, #e5e7eb);
  border-left: 4px solid var(--c-primary, #0F4C81);
}

.quote-mark {
  position: absolute;
  top: 0.5rem;
  left: 1.5rem;
  font-size: 4rem;
  font-family: Georgia, serif;
  color: var(--c-primary, #0F4C81);
  opacity: 0.15;
  line-height: 1;
}

.quote-content {
  margin: 0;
  padding-left: 2rem;
}

.quote-text {
  font-size: 1.25rem;
  line-height: 1.6;
  color: var(--c-text-primary, #1a1a1a);
  font-style: italic;
  margin: 0 0 1.25rem 0;
}

.quote-footer {
  margin-top: 1rem;
}

.quote-footer cite {
  font-style: normal;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.quote-author {
  font-weight: 600;
  color: var(--c-text-primary, #1a1a1a);
  font-size: 1rem;
}

.quote-attribution {
  color: var(--c-text-secondary, #6b7280);
  font-size: 0.9rem;
}

/* Variant: Boxed */
.variant-boxed {
  background: var(--c-bg-muted, #f9fafb);
  border: none;
  border-left: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.variant-boxed::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--c-primary, #0F4C81);
  border-radius: 8px 8px 0 0;
}

/* Variant: Minimal */
.variant-minimal {
  background: transparent;
  border: none;
  padding: 1rem 0;
}

.variant-minimal .quote-mark {
  left: 0;
}

/* Variant: Accent */
.variant-accent {
  background: linear-gradient(135deg, 
    color-mix(in srgb, var(--c-primary, #0F4C81) 8%, white),
    color-mix(in srgb, var(--c-primary, #0F4C81) 3%, white));
  border-color: var(--c-primary, #0F4C81);
}

/* Variant: Large */
.variant-large .quote-text {
  font-size: 1.5rem;
}

.variant-large .quote-mark {
  font-size: 6rem;
}
</style>
