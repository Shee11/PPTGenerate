<template>
  <div class="slidev-layout feature-grid">
    <header v-if="$slots.title" class="feature-title">
      <slot name="title" />
    </header>
    
    <div class="features-container">
      <div v-if="$slots.feature1" class="feature-box">
        <slot name="feature1" />
      </div>
      <div v-if="$slots.feature2" class="feature-box">
        <slot name="feature2" />
      </div>
      <div v-if="$slots.feature3" class="feature-box">
        <slot name="feature3" />
      </div>
      <div v-if="$slots.feature4" class="feature-box">
        <slot name="feature4" />
      </div>
      <div v-if="$slots.feature5" class="feature-box">
        <slot name="feature5" />
      </div>
      <div v-if="$slots.feature6" class="feature-box">
        <slot name="feature6" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.feature-grid {
  @apply h-full w-full p-8 flex flex-col;
}

.feature-title {
  @apply mb-8 text-center;
}

.features-container {
  @apply flex-1 grid grid-cols-3 gap-6;
}

.feature-box {
  @apply p-6 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-900 rounded-xl shadow-md hover:shadow-xl transition-shadow;
}
</style>
