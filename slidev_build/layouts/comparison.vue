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
  @apply h-full w-full p-10 flex flex-col;
  background: linear-gradient(135deg, 
    color-mix(in srgb, var(--c-bg-base) 100%, transparent) 0%, 
    color-mix(in srgb, var(--c-bg-base) 97%, var(--slidev-theme-primary, #3b82f6)) 100%);
  position: relative;
}

/* Background decorative overlay */
.comparison::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 0%, rgba(59, 130, 246, 0.03) 0%, transparent 60%);
  pointer-events: none;
}

.comparison-title {
  @apply mb-8 text-center;
  position: relative;
  z-index: 1;
  font-weight: 600;
}

.comparison-container {
  @apply flex-1 flex items-stretch gap-6;
  position: relative;
  z-index: 1;
}

.comparison-side {
  @apply flex-1 flex flex-col;
  border-radius: 16px;
  padding: 2.5rem;
  position: relative;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.08),
    0 8px 32px rgba(0, 0, 0, 0.04);
}

/* Before side with gradient and pattern */
.before {
  background: linear-gradient(145deg,
    color-mix(in srgb, #ef4444 8%, var(--c-bg-base)) 0%,
    color-mix(in srgb, #ef4444 3%, var(--c-bg-base)) 100%);
  border-left: 4px solid #ef4444;
}

.before::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    -45deg,
    transparent,
    transparent 60px,
    rgba(239, 68, 68, 0.02) 60px,
    rgba(239, 68, 68, 0.02) 120px
  );
  border-radius: 16px;
  pointer-events: none;
}

/* After side with gradient and pattern */
.after {
  background: linear-gradient(145deg,
    color-mix(in srgb, #10b981 8%, var(--c-bg-base)) 0%,
    color-mix(in srgb, #10b981 3%, var(--c-bg-base)) 100%);
  border-right: 4px solid #10b981;
}

.after::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 60px,
    rgba(16, 185, 129, 0.02) 60px,
    rgba(16, 185, 129, 0.02) 120px
  );
  border-radius: 16px;
  pointer-events: none;
}

.side-label {
  @apply font-bold text-lg mb-6 text-center;
  position: relative;
  z-index: 1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.875rem;
  opacity: 0.7;
}

/* Icon badges for labels */
.before .side-label::before {
  content: '';
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 8px;
  vertical-align: middle;
  background: #ef4444;
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.5);
}

.after .side-label::before {
  content: '';
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 8px;
  vertical-align: middle;
  background: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
}

.side-content {
  @apply flex-1;
  position: relative;
  z-index: 1;
}

.comparison-divider {
  @apply flex items-center justify-center w-20;
  position: relative;
}

/* Enhanced VS badge */
.divider-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, 
    var(--slidev-theme-primary, #3b82f6) 0%, 
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 70%, #8b5cf6) 100%);
  color: white;
  font-weight: 800;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 8px 24px rgba(59, 130, 246, 0.4),
    0 0 0 8px color-mix(in srgb, var(--c-bg-base) 90%, white),
    0 0 0 12px color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 20%, transparent);
  position: relative;
}

/* Glow around VS badge */
.divider-icon::before {
  content: '';
  position: absolute;
  inset: -12px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, transparent 70%);
}
</style>
