<!--
  IconBox.vue - Editorial Icon Box Component
  
  Props:
    - icon: Icon character/emoji
    - title: Box title
    - description: Box description
-->
<template>
  <div class="icon-box">
    <div class="icon-container">
      <span class="icon">{{ icon }}</span>
    </div>
    <h3 class="box-title">{{ title }}</h3>
    <p v-if="description" class="box-description">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  icon: string
  title: string
  description?: string
}>(), {
  icon: '✦'
})
</script>

<style scoped>
.icon-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.75rem;
  padding: 1.5rem;
}

.icon-container {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--edit-gold);
  border-radius: 50%;
}

.icon {
  font-size: 1.25rem;
  color: var(--edit-gold);
}

.box-title {
  font-family: var(--edit-font-display);
  font-size: 1.1rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0;
}

.box-description {
  font-family: var(--edit-font-body);
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--edit-text);
  margin: 0;
}
</style>
