<template>
  <div class="glass-card" :class="[variant, { frosted: blur === 'heavy' }]">
    <div class="glass-shine"></div>
    <div class="glass-content">
      <slot />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  variant: {
    type: String,
    default: 'light', // light, dark, tinted
  },
  blur: {
    type: String,
    default: 'medium', // light, medium, heavy
  },
})
</script>

<style scoped>
.glass-card {
  position: relative;
  padding: 2rem;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.1),
    0 4px 16px rgba(0, 0, 0, 0.05);
}

/* Light variant */
.glass-card.light {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.7) 0%,
    rgba(255, 255, 255, 0.5) 100%
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* Dark variant */
.glass-card.dark {
  background: linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.6) 0%,
    rgba(0, 0, 0, 0.4) 100%
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-color: rgba(255, 255, 255, 0.1);
  color: white;
}

/* Tinted variant */
.glass-card.tinted {
  background: linear-gradient(
    135deg,
    rgba(59, 130, 246, 0.3) 0%,
    rgba(139, 92, 246, 0.2) 100%
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-color: rgba(255, 255, 255, 0.3);
}

/* Heavy blur */
.glass-card.frosted {
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}

/* Glass shine effect */
.glass-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle at 30% 30%,
    rgba(255, 255, 255, 0.3) 0%,
    transparent 50%
  );
  pointer-events: none;
  opacity: 0.5;
}

.glass-content {
  position: relative;
  z-index: 1;
}

/* Noise texture */
.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
  opacity: 0.5;
  pointer-events: none;
}

/* Border glow */
.glass-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  padding: 1px;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.4) 0%,
    transparent 50%,
    rgba(255, 255, 255, 0.2) 100%
  );
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
</style>
