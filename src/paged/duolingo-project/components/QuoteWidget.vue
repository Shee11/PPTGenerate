<template>
  <div class="quote-widget" :class="variant">
    <div class="quote-bubble">
      <div class="quote-icon" v-if="showIcon">
        <span class="icon-emoji">💬</span>
      </div>
      <blockquote class="quote-content">
        <p class="quote-text">{{ text }}</p>
        <footer v-if="author || attribution" class="quote-footer">
          <cite>
            <span class="author-avatar">🦉</span>
            <span v-if="author" class="quote-author">{{ author }}</span>
            <span v-if="attribution" class="quote-attribution">{{ attribution }}</span>
          </cite>
        </footer>
      </blockquote>
    </div>
    <div class="bubble-tail"></div>
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
  accentColor: {
    type: String,
    default: 'green', // green, blue, orange, purple
  },
})
</script>

<style scoped>
.quote-widget {
  position: relative;
  padding-bottom: 20px;
}

.quote-bubble {
  padding: 2rem;
  background: white;
  border-radius: 24px;
  box-shadow: 
    0 4px 0 var(--duo-green-dark, #46a302),
    0 8px 20px rgba(88, 204, 2, 0.15);
  border: 3px solid var(--duo-green, #58CC02);
  position: relative;
}

.bubble-tail {
  position: absolute;
  bottom: 8px;
  left: 40px;
  width: 0;
  height: 0;
  border-left: 16px solid transparent;
  border-right: 16px solid transparent;
  border-top: 20px solid white;
  filter: drop-shadow(0 4px 0 var(--duo-green-dark, #46a302));
}

.bubble-tail::before {
  content: '';
  position: absolute;
  top: -24px;
  left: -19px;
  width: 0;
  height: 0;
  border-left: 19px solid transparent;
  border-right: 19px solid transparent;
  border-top: 24px solid var(--duo-green, #58CC02);
}

.quote-icon {
  position: absolute;
  top: -20px;
  right: 24px;
  width: 48px;
  height: 48px;
  background: var(--duo-green, #58CC02);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 0 var(--duo-green-dark, #46a302);
}

.icon-emoji {
  font-size: 1.5rem;
}

.quote-content {
  margin: 0;
  position: relative;
}

.quote-text {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 1.35rem;
  line-height: 1.6;
  font-weight: 700;
  color: var(--duo-text, #4B4B4B);
  margin: 0 0 1rem 0;
  position: relative;
}

.quote-text::before {
  content: '"';
  position: absolute;
  left: -1.5rem;
  top: -0.5rem;
  font-size: 4rem;
  color: var(--duo-green, #58CC02);
  opacity: 0.3;
  font-family: Georgia, serif;
  line-height: 1;
}

.quote-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 3px dashed var(--duo-gray-light, #E5E5E5);
}

.quote-footer cite {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-style: normal;
}

.author-avatar {
  font-size: 2rem;
  background: var(--duo-gray-light, #F7F7F7);
  padding: 0.5rem;
  border-radius: 50%;
}

.quote-author {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
}

.quote-attribution {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--duo-gray-dark, #777);
}

.quote-attribution::before {
  content: '• ';
}

/* Variant: minimal */
.quote-widget.minimal .quote-bubble {
  border: none;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.quote-widget.minimal .bubble-tail {
  display: none;
}

.quote-widget.minimal .quote-icon {
  background: var(--duo-gray-light, #F7F7F7);
}

/* Variant: boxed */
.quote-widget.boxed .quote-bubble {
  border-radius: 8px;
  border-width: 4px;
  border-left-width: 8px;
}

.quote-widget.boxed .bubble-tail {
  display: none;
}

.quote-widget.boxed {
  padding-bottom: 0;
}

/* Variant: accent */
.quote-widget.accent .quote-bubble {
  background: linear-gradient(135deg, 
    rgba(88, 204, 2, 0.1) 0%, 
    rgba(28, 176, 246, 0.1) 100%);
}

/* Variant: large */
.quote-widget.large .quote-bubble {
  padding: 3rem;
}

.quote-widget.large .quote-text {
  font-size: 1.75rem;
}

.quote-widget.large .quote-icon {
  width: 64px;
  height: 64px;
  top: -28px;
}

.quote-widget.large .icon-emoji {
  font-size: 2rem;
}

/* Color variants */
.quote-widget[data-accent="blue"] .quote-bubble {
  border-color: var(--duo-blue, #1CB0F6);
  box-shadow: 
    0 4px 0 var(--duo-blue-dark, #1899D6),
    0 8px 20px rgba(28, 176, 246, 0.15);
}

.quote-widget[data-accent="blue"] .quote-icon {
  background: var(--duo-blue, #1CB0F6);
  box-shadow: 0 3px 0 var(--duo-blue-dark, #1899D6);
}

.quote-widget[data-accent="blue"] .bubble-tail {
  filter: drop-shadow(0 4px 0 var(--duo-blue-dark, #1899D6));
}

.quote-widget[data-accent="blue"] .bubble-tail::before {
  border-top-color: var(--duo-blue, #1CB0F6);
}

.quote-widget[data-accent="orange"] .quote-bubble {
  border-color: var(--duo-orange, #FF9600);
  box-shadow: 
    0 4px 0 #E68600,
    0 8px 20px rgba(255, 150, 0, 0.15);
}

.quote-widget[data-accent="orange"] .quote-icon {
  background: var(--duo-orange, #FF9600);
  box-shadow: 0 3px 0 #E68600;
}

.quote-widget[data-accent="purple"] .quote-bubble {
  border-color: var(--duo-purple, #CE82FF);
  box-shadow: 
    0 4px 0 #B86EE6,
    0 8px 20px rgba(206, 130, 255, 0.15);
}

.quote-widget[data-accent="purple"] .quote-icon {
  background: var(--duo-purple, #CE82FF);
  box-shadow: 0 3px 0 #B86EE6;
}
</style>
