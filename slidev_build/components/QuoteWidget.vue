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
  padding: 2.5rem;
  position: relative;
  background: linear-gradient(145deg,
    color-mix(in srgb, var(--c-bg-base) 98%, white) 0%,
    color-mix(in srgb, var(--c-bg-base) 95%, white) 100%);
  border-radius: 12px;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.06),
    0 1px 3px rgba(0, 0, 0, 0.08);
  border: 1px solid color-mix(in srgb, white 10%, transparent);
}

/* Decorative corner accent */
.quote-widget::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg,
    var(--slidev-theme-primary, #3b82f6) 0%,
    transparent 70%);
  opacity: 0.1;
  border-radius: 12px 0 12px 0;
}

.quote-icon {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  width: 4rem;
  height: 4rem;
  opacity: 0.12;
  background: linear-gradient(135deg,
    var(--slidev-theme-primary, #3b82f6) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 70%, #8b5cf6) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.quote-content {
  margin: 0;
  padding-left: 2.5rem;
  position: relative;
}

/* Decorative quote line */
.quote-content::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg,
    var(--slidev-theme-primary, #3b82f6) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 60%, #8b5cf6) 50%,
    transparent 100%);
  border-radius: 2px;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.3);
}

.quote-text {
  font-size: 1.5rem;
  line-height: 1.6;
  font-style: italic;
  color: var(--slidev-theme-text, #1f2937);
  margin: 0 0 1.5rem 0;
  position: relative;
}

.quote-footer {
  margin-top: 2rem;
  padding-top: 1.25rem;
  border-top: 3px solid transparent;
  background: linear-gradient(90deg,
    var(--slidev-theme-primary, #3b82f6) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 50%, transparent) 40%,
    transparent 100%) left top / 100% 3px no-repeat;
}

.quote-author {
  display: block;
  font-size: 1.1rem;
  font-weight: 700;
  font-style: normal;
  background: linear-gradient(135deg,
    var(--slidev-theme-primary, #3b82f6) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 70%, #8b5cf6) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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
  padding: 1.5rem;
  background: transparent;
  box-shadow: none;
  border: none;
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

.minimal .quote-content::before {
  display: none;
}

.minimal .quote-footer {
  border-top: none;
  background: none;
  padding-top: 0.75rem;
  margin-top: 1rem;
  padding-left: 1.5rem;
}

.boxed {
  background: linear-gradient(145deg,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 8%, var(--c-bg-base)) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 3%, var(--c-bg-base)) 100%);
  border: 2px solid var(--slidev-theme-primary, #3b82f6);
  box-shadow: 
    0 4px 16px rgba(59, 130, 246, 0.15),
    0 8px 32px rgba(59, 130, 246, 0.08);
}

.accent {
  background: linear-gradient(135deg, 
    var(--slidev-theme-primary, #3b82f6) 0%, 
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 85%, #8b5cf6) 100%);
  color: white;
  border: none;
  box-shadow: 
    0 8px 24px rgba(59, 130, 246, 0.4),
    0 4px 12px rgba(59, 130, 246, 0.3);
}

.accent .quote-text {
  color: white;
}

.accent .quote-author {
  color: white;
  background: none;
  -webkit-text-fill-color: white;
}

.accent .quote-attribution {
  color: rgba(255, 255, 255, 0.8);
}

.accent .quote-footer {
  background: linear-gradient(90deg,
    rgba(255, 255, 255, 0.4) 0%,
    rgba(255, 255, 255, 0.2) 40%,
    transparent 100%) left top / 100% 3px no-repeat;
}

.accent .quote-icon {
  color: white;
  opacity: 0.2;
  background: white;
  -webkit-text-fill-color: white;
}

.accent .quote-content::before {
  background: linear-gradient(180deg,
    rgba(255, 255, 255, 0.5) 0%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 100%);
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
