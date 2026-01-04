<!--
  ImageWidget.vue - Image with Optional Caption
  
  Props:
    - src: Image URL
    - alt: Alt text
    - caption: Optional caption
-->
<template>
  <figure class="image-widget">
    <img :src="src" :alt="alt" class="image" />
    <figcaption v-if="caption" class="caption">{{ caption }}</figcaption>
  </figure>
</template>

<script setup lang="ts">
defineProps<{
  src: string
  alt?: string
  caption?: string
}>()
</script>

<style scoped>
.image-widget {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  object-fit: cover;
}

.caption {
  font-size: 0.875rem;
  color: var(--c-text-muted);
  text-align: center;
}
</style>
