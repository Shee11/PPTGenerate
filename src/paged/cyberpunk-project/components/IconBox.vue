<!--
  IconBox.vue - Cyberpunk Icon Box Widget
  
  Props:
    - icon: Icon character or emoji
    - title: Box title
    - description: Box description
-->
<template>
  <div class="icon-box">
    <div class="icon-container">
      <span class="icon-glyph">{{ icon }}</span>
      <div class="icon-ring"></div>
    </div>
    <div class="icon-content">
      <h4 class="icon-title">{{ title }}</h4>
      <p v-if="description" class="icon-description">{{ description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon: string
  title: string
  description?: string
}>()
</script>

<style scoped>
.icon-box {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(18, 18, 26, 0.7);
  border: 1px solid rgba(0, 255, 255, 0.15);
  transition: all 0.3s ease;
}

.icon-box:hover {
  border-color: var(--cyber-cyan, #00FFFF);
  box-shadow: 0 0 20px var(--cyber-cyan-glow);
}

.icon-container {
  position: relative;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-glyph {
  font-size: 1.5rem;
  filter: drop-shadow(0 0 10px var(--cyber-cyan-glow));
  z-index: 5;
}

.icon-ring {
  position: absolute;
  inset: 0;
  border: 2px solid var(--cyber-cyan, #00FFFF);
  opacity: 0.5;
  animation: ring-pulse 2s ease-in-out infinite;
}

@keyframes ring-pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.3; }
}

.icon-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.icon-title {
  font-family: var(--cyber-font-display);
  font-size: 1rem;
  font-weight: 600;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  margin: 0 0 0.25rem 0;
}

.icon-description {
  font-family: var(--cyber-font-body);
  font-size: 0.85rem;
  line-height: 1.4;
  color: var(--cyber-text, #e0e0e0);
  margin: 0;
}
</style>
