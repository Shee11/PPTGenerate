<!--
  GradientText.vue - Text with Gradient Effect Component
  
  Apply beautiful gradient effects to text content.
  Perfect for headings, highlights, or call-to-actions.
  
  Props:
    - gradient: Gradient type (primary, rainbow, sunset, ocean, forest, neon)
    - customGradient: Custom CSS gradient string
    - animated: Animate the gradient
    - weight: Font weight (normal, medium, semibold, bold, extrabold)
-->
<template>
  <span 
    class="gradient-text"
    :class="[`gradient-${gradient}`, `weight-${weight}`, { animated }]"
    :style="textStyles"
  >
    <slot />
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  gradient?: 'primary' | 'rainbow' | 'sunset' | 'ocean' | 'forest' | 'neon'
  customGradient?: string
  animated?: boolean
  weight?: 'normal' | 'medium' | 'semibold' | 'bold' | 'extrabold'
}>(), {
  gradient: 'primary',
  animated: false,
  weight: 'bold'
})

const textStyles = computed(() => {
  if (props.customGradient) {
    return { backgroundImage: props.customGradient }
  }
  return {}
})
</script>

<style scoped>
.gradient-text {
  display: inline;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-size: 200% auto;
}

/* Font weights */
.weight-normal { font-weight: 400; }
.weight-medium { font-weight: 500; }
.weight-semibold { font-weight: 600; }
.weight-bold { font-weight: 700; }
.weight-extrabold { font-weight: 800; }

/* Gradient presets */
.gradient-primary {
  background-image: linear-gradient(135deg, var(--c-primary), var(--c-accent, #10b981));
}

.gradient-rainbow {
  background-image: linear-gradient(
    135deg,
    #ff0080,
    #ff8c00,
    #40e0d0,
    #7b68ee,
    #ff0080
  );
}

.gradient-sunset {
  background-image: linear-gradient(135deg, #ff512f, #f09819, #ff512f);
}

.gradient-ocean {
  background-image: linear-gradient(135deg, #667eea, #764ba2, #667eea);
}

.gradient-forest {
  background-image: linear-gradient(135deg, #11998e, #38ef7d, #11998e);
}

.gradient-neon {
  background-image: linear-gradient(135deg, #00f5ff, #ff00ff, #00f5ff);
}

/* Animation */
.animated {
  animation: gradient-shift 3s ease-in-out infinite;
}

@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% center;
  }
  50% {
    background-position: 100% center;
  }
}
</style>
