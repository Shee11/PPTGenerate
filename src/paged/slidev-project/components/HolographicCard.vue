<template>
  <div class="holographic-card" :class="{ animated: shimmer }">
    <div class="holo-gradient"></div>
    <div class="holo-scanlines"></div>
    <div class="holo-content">
      <slot />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  shimmer: {
    type: Boolean,
    default: true,
  },
})
</script>

<style scoped>
.holographic-card {
  position: relative;
  padding: 2rem;
  background: linear-gradient(
    135deg,
    rgba(10, 10, 30, 0.9) 0%,
    rgba(20, 20, 50, 0.85) 100%
  );
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(0, 255, 255, 0.3);
  box-shadow: 
    0 8px 32px rgba(0, 255, 255, 0.2),
    0 0 60px rgba(139, 92, 246, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

/* Iridescent gradient overlay */
.holo-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    45deg,
    transparent 0%,
    rgba(255, 0, 128, 0.1) 20%,
    rgba(0, 255, 255, 0.15) 40%,
    rgba(128, 0, 255, 0.1) 60%,
    rgba(0, 255, 128, 0.15) 80%,
    transparent 100%
  );
  opacity: 0.6;
  pointer-events: none;
}

.holographic-card.animated .holo-gradient {
  animation: shimmer 3s linear infinite;
  background-size: 200% 200%;
}

@keyframes shimmer {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 200% 200%;
  }
}

/* Scanlines */
.holo-scanlines {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 255, 255, 0.03) 2px,
    rgba(0, 255, 255, 0.03) 4px
  );
  pointer-events: none;
}

.holo-content {
  position: relative;
  z-index: 1;
  color: rgba(255, 255, 255, 0.95);
}

/* Edge glow */
.holographic-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(
    45deg,
    #00ffff,
    #ff00ff,
    #00ffff,
    #ff00ff
  );
  border-radius: 12px;
  z-index: -1;
  opacity: 0.3;
  filter: blur(8px);
  animation: rotate-hue 4s linear infinite;
}

@keyframes rotate-hue {
  0% {
    filter: blur(8px) hue-rotate(0deg);
  }
  100% {
    filter: blur(8px) hue-rotate(360deg);
  }
}

/* Corner accents */
.holographic-card::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 60px;
  height: 60px;
  background: radial-gradient(
    circle at top right,
    rgba(0, 255, 255, 0.4) 0%,
    transparent 70%
  );
  pointer-events: none;
}
</style>
