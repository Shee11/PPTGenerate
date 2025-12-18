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
  @apply h-full w-full p-10 flex flex-col;
  background: linear-gradient(135deg, 
    var(--c-bg-base) 0%, 
    color-mix(in srgb, var(--c-bg-base) 96%, var(--slidev-theme-primary, #3b82f6)) 100%);
  position: relative;
}

/* Background decoration */
.feature-grid::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.03) 0%, transparent 50%);
  pointer-events: none;
}

.feature-title {
  @apply mb-8 text-center;
  position: relative;
  z-index: 1;
  font-weight: 600;
}

.features-container {
  @apply flex-1 grid grid-cols-3 gap-8;
  position: relative;
  z-index: 1;
}

.feature-box {
  @apply p-8 rounded-xl;
  background: linear-gradient(145deg,
    color-mix(in srgb, var(--c-bg-base) 98%, white) 0%,
    color-mix(in srgb, var(--c-bg-base) 95%, white) 100%);
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.06),
    0 8px 32px rgba(0, 0, 0, 0.04),
    0 1px 2px rgba(0, 0, 0, 0.08);
  position: relative;
  border: 1px solid color-mix(in srgb, white 10%, transparent);
  transition: transform 0.3s ease;
}

/* nth-child variations - dynamic positioning */
.feature-box:nth-child(odd) {
  transform: translateY(-8px) rotate(-0.5deg);
}

.feature-box:nth-child(even) {
  transform: translateY(8px) rotate(0.5deg);
}

.feature-box:nth-child(3n+1) {
  border-radius: 20px 8px 20px 8px;
}

.feature-box:nth-child(3n+2) {
  border-radius: 8px 20px 8px 20px;
}

.feature-box:nth-child(3n+3) {
  border-radius: 16px;
}

/* Gradient top border with position-based colors */
.feature-box:nth-child(3n+1)::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 12px 12px 0 0;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.feature-box:nth-child(3n+2)::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #8b5cf6 0%, #a78bfa 100%);
  border-radius: 12px 12px 0 0;
  box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
}

.feature-box:nth-child(3n+3)::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
  border-radius: 12px 12px 0 0;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

/* Corner accent decoration */
.feature-box::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 50px;
  height: 50px;
  background: radial-gradient(circle at bottom right, 
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 6%, transparent) 0%, 
    transparent 70%);
  border-radius: 0 0 12px 0;
  pointer-events: none;
}
</style>
