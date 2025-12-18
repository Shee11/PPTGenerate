<template>
  <div class="quote-widget" :class="variant">
    <div class="quote-icon" v-if="showIcon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
        <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
      </svg>
    </div>
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
  attribution: String, // Role, company, etc.
  variant: {
    type: String,
    default: 'default', // default, minimal, boxed, accent, large
  },
  showIcon: {
    type: Boolean,
    default: true,
  },
})
</script>

<style scoped>
.quote-widget {
  padding: 2rem;
  position: relative;
}

.quote-icon {
  position: absolute;
  top: 1rem;
  left: 1rem;
  width: 3rem;
  height: 3rem;
  opacity: 0.15;
  color: var(--slidev-theme-primary, #3b82f6);
}

.quote-content {
  margin: 0;
  padding-left: 2rem;
}

.quote-text {
  font-size: 1.5rem;
  line-height: 1.6;
  font-style: italic;
  color: var(--slidev-theme-text, #1f2937);
  margin: 0 0 1rem 0;
}

.quote-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 2px solid var(--slidev-theme-primary, #3b82f6);
}

.quote-author {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  font-style: normal;
  color: var(--slidev-theme-text, #1f2937);
}

.quote-attribution {
  display: block;
  font-size: 0.95rem;
  font-style: normal;
  color: rgba(0, 0, 0, 0.6);
  margin-top: 0.25rem;
}

/* Variants */
.minimal {
  padding: 1rem;
  background: transparent;
}

.minimal .quote-icon {
  display: none;
}

.minimal .quote-content {
  padding-left: 0;
}

.minimal .quote-text {
  font-size: 1.25rem;
  border-left: 4px solid var(--slidev-theme-primary, #3b82f6);
  padding-left: 1.5rem;
}

.minimal .quote-footer {
  border-top: none;
  padding-top: 0.5rem;
  margin-top: 1rem;
  padding-left: 1.5rem;
}

.boxed {
  background: rgba(59, 130, 246, 0.05);
  border-radius: 0.5rem;
  border: 2px solid var(--slidev-theme-primary, #3b82f6);
}

.accent {
  background: linear-gradient(135deg, var(--slidev-theme-primary, #3b82f6) 0%, var(--slidev-theme-primary, #3b82f6) 100%);
  color: white;
  border-radius: 0.5rem;
}

.accent .quote-text {
  color: white;
}

.accent .quote-author {
  color: white;
}

.accent .quote-attribution {
  color: rgba(255, 255, 255, 0.8);
}

.accent .quote-footer {
  border-top-color: rgba(255, 255, 255, 0.3);
}

.accent .quote-icon {
  color: white;
  opacity: 0.2;
}

.large .quote-text {
  font-size: 2rem;
  line-height: 1.5;
}

.large .quote-author {
  font-size: 1.3rem;
}

.large .quote-attribution {
  font-size: 1.1rem;
}
</style>
