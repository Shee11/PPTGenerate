<!--
  IconBox.vue - Handdrawn Icon Box Component
  
  Props:
    - icon: Emoji or icon
    - title: Box title
    - color: Color variant
-->
<template>
  <div class="icon-box" :class="`box-${color}`">
    <div class="icon-circle">
      <span class="icon-emoji">{{ icon }}</span>
    </div>
    <div class="box-content">
      <div v-if="title" class="box-title">{{ title }}</div>
      <div class="box-body">
        <slot>Description here...</slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  icon?: string
  title?: string
  color?: 'pink' | 'blue' | 'green' | 'yellow'
}>(), {
  icon: '⭐',
  color: 'pink'
})
</script>

<style scoped>
.icon-box {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background: var(--hand-bg-cream);
  border: 2px solid;
  border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;
  box-shadow: 3px 3px 0 var(--hand-shadow-color);
}

.box-pink { border-color: var(--hand-pink); }
.box-blue { border-color: var(--hand-blue); }
.box-green { border-color: var(--hand-green); }
.box-yellow { border-color: var(--hand-yellow-dark); }

.icon-circle {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 3px solid currentColor;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--hand-bg-cream);
}

.box-pink .icon-circle { border-color: var(--hand-pink); }
.box-blue .icon-circle { border-color: var(--hand-blue); }
.box-green .icon-circle { border-color: var(--hand-green); }
.box-yellow .icon-circle { border-color: var(--hand-yellow-dark); }

.icon-emoji {
  font-size: 1.5rem;
}

.box-content {
  flex: 1;
}

.box-title {
  font-family: var(--hand-font-display);
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  margin-bottom: 0.25rem;
}

.box-body {
  font-family: var(--hand-font-body);
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--hand-text);
}
</style>
