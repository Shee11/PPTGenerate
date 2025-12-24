<!--
  GradientText.vue - Editorial Gradient Text Component
  
  Props:
    - text: Text to display
    - gradient: Gradient type
-->
<template>
  <span class="gradient-text" :class="`gradient-${gradient}`">{{ text }}</span>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  text: string
  gradient?: 'gold' | 'warm' | 'cool' | 'subtle'
}>(), {
  gradient: 'gold'
})
</script>

<style scoped>
.gradient-text {
  font-family: var(--edit-font-display);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-size: 100%;
}

.gradient-gold {
  background-image: linear-gradient(135deg, var(--edit-gold) 0%, #e6c984 50%, var(--edit-gold) 100%);
}

.gradient-warm {
  background-image: linear-gradient(135deg, var(--edit-burgundy) 0%, var(--edit-gold) 100%);
}

.gradient-cool {
  background-image: linear-gradient(135deg, var(--edit-navy) 0%, var(--edit-slate) 100%);
}

.gradient-subtle {
  background-image: linear-gradient(135deg, var(--edit-text-dark) 0%, var(--edit-text) 100%);
}
</style>
