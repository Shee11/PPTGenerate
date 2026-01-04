<!--
  GradientText.vue - Handdrawn Gradient/Styled Text Component
  
  Props:
    - variant: Style variant
    - size: Text size
-->
<template>
  <span class="gradient-text" :class="[`variant-${variant}`, `size-${size}`]">
    <span class="text-inner">
      <slot>Text</slot>
    </span>
    <span v-if="variant === 'highlight'" class="highlight-bg"></span>
    <span v-if="variant === 'underline'" class="underline-deco"></span>
    <span v-if="variant === 'circle'" class="circle-deco"></span>
  </span>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  variant?: 'rainbow' | 'highlight' | 'underline' | 'circle' | 'stamp'
  size?: 'sm' | 'md' | 'lg' | 'xl'
}>(), {
  variant: 'rainbow',
  size: 'md'
})
</script>

<style scoped>
.gradient-text {
  position: relative;
  display: inline-block;
  font-family: var(--hand-font-display);
  font-weight: 700;
}

/* Sizes */
.size-sm { font-size: 1rem; }
.size-md { font-size: 1.5rem; }
.size-lg { font-size: 2rem; }
.size-xl { font-size: 3rem; }

/* Text inner */
.text-inner {
  position: relative;
  z-index: 2;
}

/* Rainbow variant */
.variant-rainbow .text-inner {
  background: linear-gradient(
    90deg,
    var(--hand-pink) 0%,
    var(--hand-yellow-dark) 25%,
    var(--hand-green) 50%,
    var(--hand-blue) 75%,
    var(--hand-pink) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Highlight variant */
.variant-highlight {
  color: var(--hand-text-dark);
}

.highlight-bg {
  position: absolute;
  bottom: 0;
  left: -4px;
  right: -4px;
  height: 40%;
  background: var(--hand-yellow);
  z-index: 1;
  transform: rotate(-1deg);
}

/* Underline variant */
.variant-underline {
  color: var(--hand-text-dark);
}

.underline-deco {
  position: absolute;
  bottom: -4px;
  left: 0;
  right: 0;
  height: 4px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 10'%3E%3Cpath d='M0,5 Q25,0 50,5 T100,5' fill='none' stroke='%23FFB5BA' stroke-width='3'/%3E%3C/svg%3E") repeat-x;
  background-size: 50px 10px;
}

/* Circle variant */
.variant-circle {
  color: var(--hand-text-dark);
  padding: 0.25em 0.5em;
}

.circle-deco {
  position: absolute;
  inset: -0.2em;
  border: 3px solid var(--hand-pink);
  border-radius: 50%;
  transform: rotate(-2deg);
  z-index: 1;
}

/* Stamp variant */
.variant-stamp {
  color: var(--hand-pink);
  padding: 0.25em 0.75em;
  border: 3px solid currentColor;
  border-radius: 4px;
  transform: rotate(-3deg);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.variant-stamp::before {
  content: '';
  position: absolute;
  inset: 2px;
  border: 1px solid currentColor;
  border-radius: 2px;
}
</style>
