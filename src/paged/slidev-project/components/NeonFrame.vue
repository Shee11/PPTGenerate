<template>
  <div class="neon-frame" :class="[color, { animated: pulse }]">
    <div class="neon-border-top"></div>
    <div class="neon-border-right"></div>
    <div class="neon-border-bottom"></div>
    <div class="neon-border-left"></div>
    <div class="neon-corner neon-corner-tl"></div>
    <div class="neon-corner neon-corner-tr"></div>
    <div class="neon-corner neon-corner-bl"></div>
    <div class="neon-corner neon-corner-br"></div>
    <div class="neon-content">
      <slot />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  color: {
    type: String,
    default: 'cyan', // cyan, magenta, lime, orange
  },
  pulse: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.neon-frame {
  position: relative;
  padding: 2rem;
  background: rgba(0, 0, 0, 0.8);
  overflow: hidden;
}

/* Color variants */
.neon-frame.cyan {
  --neon-color: #00ffff;
  --neon-glow: rgba(0, 255, 255, 0.6);
}

.neon-frame.magenta {
  --neon-color: #ff00ff;
  --neon-glow: rgba(255, 0, 255, 0.6);
}

.neon-frame.lime {
  --neon-color: #00ff00;
  --neon-glow: rgba(0, 255, 0, 0.6);
}

.neon-frame.orange {
  --neon-color: #ff6600;
  --neon-glow: rgba(255, 102, 0, 0.6);
}

/* Neon borders */
.neon-border-top,
.neon-border-right,
.neon-border-bottom,
.neon-border-left {
  position: absolute;
  background: var(--neon-color);
  box-shadow: 
    0 0 8px var(--neon-glow),
    0 0 16px var(--neon-glow),
    0 0 24px var(--neon-glow);
}

.neon-border-top {
  top: 0;
  left: 10%;
  right: 10%;
  height: 3px;
}

.neon-border-bottom {
  bottom: 0;
  left: 10%;
  right: 10%;
  height: 3px;
}

.neon-border-left {
  left: 0;
  top: 10%;
  bottom: 10%;
  width: 3px;
}

.neon-border-right {
  right: 0;
  top: 10%;
  bottom: 10%;
  width: 3px;
}

/* Corner decorations */
.neon-corner {
  position: absolute;
  width: 20px;
  height: 20px;
  border: 2px solid var(--neon-color);
  box-shadow: 
    0 0 8px var(--neon-glow),
    0 0 16px var(--neon-glow);
}

.neon-corner-tl {
  top: 0;
  left: 0;
  border-right: none;
  border-bottom: none;
}

.neon-corner-tr {
  top: 0;
  right: 0;
  border-left: none;
  border-bottom: none;
}

.neon-corner-bl {
  bottom: 0;
  left: 0;
  border-right: none;
  border-top: none;
}

.neon-corner-br {
  bottom: 0;
  right: 0;
  border-left: none;
  border-top: none;
}

.neon-content {
  position: relative;
  z-index: 1;
  color: var(--neon-color);
  text-shadow: 0 0 8px var(--neon-glow);
}

/* Grid background effect */
.neon-frame::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(var(--neon-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--neon-color) 1px, transparent 1px);
  background-size: 50px 50px;
  opacity: 0.05;
  pointer-events: none;
}

/* Scanline effect */
.neon-frame::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    transparent 50%,
    rgba(0, 0, 0, 0.1) 50%
  );
  background-size: 100% 4px;
  pointer-events: none;
  opacity: 0.3;
}

/* Pulse animation */
@keyframes neon-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.neon-frame.animated .neon-border-top,
.neon-frame.animated .neon-border-right,
.neon-frame.animated .neon-border-bottom,
.neon-frame.animated .neon-border-left,
.neon-frame.animated .neon-corner {
  animation: neon-pulse 2s ease-in-out infinite;
}
</style>
