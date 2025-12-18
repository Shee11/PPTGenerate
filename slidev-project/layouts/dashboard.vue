<template>
  <div class="slidev-layout dashboard">
    <header v-if="$slots.title" class="dashboard-title">
      <slot name="title" />
    </header>
    
    <div class="dashboard-grid">
      <div v-if="$slots.metric1" class="metric-card large">
        <slot name="metric1" />
      </div>
      <div v-if="$slots.metric2" class="metric-card large">
        <slot name="metric2" />
      </div>
      <div v-if="$slots.metric3" class="metric-card small">
        <slot name="metric3" />
      </div>
      <div v-if="$slots.metric4" class="metric-card small">
        <slot name="metric4" />
      </div>
      <div v-if="$slots.chart" class="chart-area">
        <slot name="chart" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  @apply h-full w-full p-8 flex flex-col;
}

.dashboard-title {
  @apply mb-6 text-center;
}

.dashboard-grid {
  @apply flex-1 grid grid-cols-4 grid-rows-3 gap-4;
}

.metric-card {
  @apply bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex flex-col justify-center items-center;
}

.metric-card.large {
  @apply col-span-2 row-span-1;
}

.metric-card.small {
  @apply col-span-1 row-span-1;
}

.chart-area {
  @apply col-span-4 row-span-2 bg-white dark:bg-gray-800 rounded-lg shadow-md p-6;
}
</style>
