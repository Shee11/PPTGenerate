<template>
  <div class="slidev-layout comparison">
    <header v-if="$slots.title" class="comparison-title">
      <slot name="title" />
    </header>
    
    <div class="comparison-container">
      <div class="comparison-side before">
        <div v-if="$slots.beforeLabel" class="side-label">
          <slot name="beforeLabel" />
        </div>
        <div class="side-content">
          <slot name="before" />
        </div>
      </div>
      
      <div class="comparison-divider">
        <div class="divider-icon">VS</div>
      </div>
      
      <div class="comparison-side after">
        <div v-if="$slots.afterLabel" class="side-label">
          <slot name="afterLabel" />
        </div>
        <div class="side-content">
          <slot name="after" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.comparison {
  @apply h-full w-full p-8 flex flex-col;
}

.comparison-title {
  @apply mb-6 text-center;
}

.comparison-container {
  @apply flex-1 flex items-stretch gap-4;
}

.comparison-side {
  @apply flex-1 flex flex-col;
}

.before {
  @apply bg-red-50 dark:bg-red-900/20 rounded-lg p-6;
}

.after {
  @apply bg-green-50 dark:bg-green-900/20 rounded-lg p-6;
}

.side-label {
  @apply font-bold text-lg mb-4 text-center;
}

.side-content {
  @apply flex-1;
}

.comparison-divider {
  @apply flex items-center justify-center w-16;
}

.divider-icon {
  @apply bg-gray-800 dark:bg-gray-200 text-white dark:text-gray-900 rounded-full w-12 h-12 flex items-center justify-center font-bold text-sm;
}
</style>
