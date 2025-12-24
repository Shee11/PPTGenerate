<!--
  GradientText.vue - Duolingo Styled Gradient Text Component
  
  Apply playful Duolingo gradient effects to text content.
  Perfect for headings, XP counts, or call-to-actions.
  
  Props:
    - gradient: Gradient type (duo, streak, gems, rainbow, sunset, ocean)
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
  gradient?: 'duo' | 'streak' | 'gems' | 'rainbow' | 'sunset' | 'ocean'
  customGradient?: string
  animated?: boolean
  weight?: 'normal' | 'medium' | 'semibold' | 'bold' | 'extrabold'
}>(), {
  gradient: 'duo',
  animated: false,
  weight: 'extrabold'
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
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
}

/* Font weights */
.weight-normal { font-weight: 400; }
.weight-medium { font-weight: 500; }
.weight-semibold { font-weight: 600; }
.weight-bold { font-weight: 700; }
.weight-extrabold { font-weight: 800; }

/* Duolingo gradient presets */
.gradient-duo {
  background-image: linear-gradient(
    135deg,
    var(--duo-green, #58CC02) 0%,
    var(--duo-blue, #1CB0F6) 50%,
    var(--duo-green, #58CC02) 100%
  );
}

.gradient-streak {
  background-image: linear-gradient(
    135deg,
    var(--duo-orange, #FF9600) 0%,
    #FF4B4B 50%,
    var(--duo-orange, #FF9600) 100%
  );
}

.gradient-gems {
  background-image: linear-gradient(
    135deg,
    var(--duo-blue, #1CB0F6) 0%,
    var(--duo-purple, #CE82FF) 50%,
    var(--duo-blue, #1CB0F6) 100%
  );
}

.gradient-rainbow {
  background-image: linear-gradient(
    135deg,
    var(--duo-green, #58CC02) 0%,
    var(--duo-blue, #1CB0F6) 25%,
    var(--duo-purple, #CE82FF) 50%,
    var(--duo-orange, #FF9600) 75%,
    var(--duo-green, #58CC02) 100%
  );
}

.gradient-sunset {
  background-image: linear-gradient(
    135deg,
    var(--duo-orange, #FF9600) 0%,
    #FF6B6B 50%,
    var(--duo-purple, #CE82FF) 100%
  );
}

.gradient-ocean {
  background-image: linear-gradient(
    135deg,
    #2DBBC4 0%,
    var(--duo-blue, #1CB0F6) 50%,
    var(--duo-purple, #CE82FF) 100%
  );
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
