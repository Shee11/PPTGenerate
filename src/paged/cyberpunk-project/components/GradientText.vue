<!--
  GradientText.vue - Cyberpunk Gradient Text Widget
  
  Props:
    - text: Text to display
    - gradient: Gradient preset (cyan-magenta, magenta-yellow, rainbow)
    - size: Font size (sm, md, lg, xl)
    - glow: Enable glow effect
-->
<template>
  <span 
    class="gradient-text" 
    :class="[`gradient-${gradient}`, `size-${size}`, { 'with-glow': glow }]"
  >
    {{ text }}
  </span>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  text: string
  gradient?: 'cyan-magenta' | 'magenta-yellow' | 'rainbow'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  glow?: boolean
}>(), {
  gradient: 'cyan-magenta',
  size: 'md',
  glow: true
})
</script>

<style scoped>
.gradient-text {
  font-family: var(--cyber-font-display);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

/* Gradients */
.gradient-cyan-magenta {
  background-image: linear-gradient(
    90deg, 
    var(--cyber-cyan, #00FFFF), 
    var(--cyber-magenta, #FF00FF)
  );
}

.gradient-magenta-yellow {
  background-image: linear-gradient(
    90deg, 
    var(--cyber-magenta, #FF00FF), 
    var(--cyber-yellow, #FFFF00)
  );
}

.gradient-rainbow {
  background-image: linear-gradient(
    90deg, 
    var(--cyber-cyan, #00FFFF),
    var(--cyber-green, #00FF41),
    var(--cyber-yellow, #FFFF00),
    var(--cyber-magenta, #FF00FF),
    var(--cyber-pink, #FF0080)
  );
}

/* Sizes */
.size-sm {
  font-size: 1rem;
}

.size-md {
  font-size: 1.5rem;
}

.size-lg {
  font-size: 2.5rem;
}

.size-xl {
  font-size: 4rem;
}

/* Glow effect */
.with-glow {
  filter: drop-shadow(0 0 10px currentColor);
}

.gradient-cyan-magenta.with-glow {
  filter: drop-shadow(0 0 15px var(--cyber-cyan-glow)) 
          drop-shadow(0 0 30px var(--cyber-magenta-glow));
}

.gradient-magenta-yellow.with-glow {
  filter: drop-shadow(0 0 15px var(--cyber-magenta-glow)) 
          drop-shadow(0 0 30px var(--cyber-yellow-glow));
}

.gradient-rainbow.with-glow {
  filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.3));
}
</style>
