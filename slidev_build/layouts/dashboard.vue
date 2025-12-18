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
  @apply h-full w-full p-10 flex flex-col;
  background: linear-gradient(135deg, 
    var(--c-bg-base) 0%, 
    color-mix(in srgb, var(--c-bg-base) 95%, var(--slidev-theme-primary, #3b82f6)) 100%);
  position: relative;
  overflow: hidden;
}

/* Floating accent shapes */
.dashboard::before {
  content: '';
  position: absolute;
  top: -10%;
  right: -5%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.dashboard::after {
  content: '';
  position: absolute;
  bottom: -15%;
  left: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.06) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.dashboard-title {
  @apply mb-8 text-center;
  position: relative;
  z-index: 2;
  font-weight: 600;
}

.dashboard-grid {
  @apply flex-1 grid grid-cols-4 grid-rows-3 gap-6;
  position: relative;
  z-index: 1;
}

.metric-card {
  @apply rounded-xl p-6 flex flex-col justify-center items-center;
  background: linear-gradient(145deg,
    color-mix(in srgb, var(--c-bg-base) 60%, white) 0%,
    color-mix(in srgb, var(--c-bg-base) 50%, white) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid color-mix(in srgb, white 15%, transparent);
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.08),
    0 8px 32px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

/* Position-based top accent bars */
.metric-card:nth-child(1)::before,
.metric-card:nth-child(2)::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.metric-card:nth-child(3)::before,
.metric-card:nth-child(4)::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #8b5cf6 0%, #a78bfa 100%);
  box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
}

/* Corner decoration for metric cards */
.metric-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 60px;
  height: 60px;
  background: radial-gradient(circle at bottom right, 
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 8%, transparent) 0%, 
    transparent 70%);
  pointer-events: none;
}

.metric-card.large {
  @apply col-span-2 row-span-1;
}

.metric-card.small {
  @apply col-span-1 row-span-1;
}

.chart-area {
  @apply col-span-4 row-span-2 rounded-xl p-6;
  background: linear-gradient(145deg,
    color-mix(in srgb, var(--c-bg-base) 60%, white) 0%,
    color-mix(in srgb, var(--c-bg-base) 50%, white) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid color-mix(in srgb, white 15%, transparent);
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.08),
    0 8px 32px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.chart-area::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}
</style>
