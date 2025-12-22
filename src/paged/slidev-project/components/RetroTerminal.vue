<template>
  <div class="retro-terminal" :class="color">
    <div class="terminal-header">
      <div class="terminal-buttons">
        <span class="btn btn-close"></span>
        <span class="btn btn-minimize"></span>
        <span class="btn btn-maximize"></span>
      </div>
      <div class="terminal-title">{{ title || 'TERMINAL.EXE' }}</div>
    </div>
    <div class="terminal-screen">
      <div class="scanline"></div>
      <div class="terminal-content">
        <slot />
      </div>
      <div class="terminal-cursor"></div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  color: {
    type: String,
    default: 'green', // green, amber, cyan
  },
})
</script>

<style scoped>
.retro-terminal {
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.5),
    0 0 40px rgba(0, 255, 0, 0.1);
  font-family: 'Courier New', monospace;
  max-width: 800px;
}

/* Color themes */
.retro-terminal.green {
  --term-color: #00ff00;
  --term-glow: rgba(0, 255, 0, 0.5);
}

.retro-terminal.amber {
  --term-color: #ffb000;
  --term-glow: rgba(255, 176, 0, 0.5);
}

.retro-terminal.cyan {
  --term-color: #00ffff;
  --term-glow: rgba(0, 255, 255, 0.5);
}

.terminal-header {
  background: linear-gradient(180deg, #2a2a2a 0%, #1f1f1f 100%);
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #333;
}

.terminal-buttons {
  display: flex;
  gap: 0.5rem;
  margin-right: 1rem;
}

.btn {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.btn-close {
  background: #ff5f56;
}

.btn-minimize {
  background: #ffbd2e;
}

.btn-maximize {
  background: #27c93f;
}

.terminal-title {
  color: #888;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.05em;
}

.terminal-screen {
  background: #0a0a0a;
  padding: 1.5rem;
  min-height: 200px;
  position: relative;
  overflow: hidden;
}

/* CRT scanline effect */
.scanline {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    transparent 50%,
    rgba(0, 0, 0, 0.3) 50%
  );
  background-size: 100% 4px;
  pointer-events: none;
  opacity: 0.1;
}

/* Screen curvature simulation */
.terminal-screen::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at center,
    transparent 60%,
    rgba(0, 0, 0, 0.3) 100%
  );
  pointer-events: none;
}

.terminal-content {
  color: var(--term-color);
  text-shadow: 0 0 8px var(--term-glow);
  line-height: 1.6;
  font-size: 0.95rem;
  position: relative;
  z-index: 1;
}

/* Blinking cursor */
.terminal-cursor {
  position: absolute;
  width: 10px;
  height: 18px;
  background: var(--term-color);
  bottom: 1.5rem;
  left: 1.5rem;
  animation: blink 1s step-end infinite;
  box-shadow: 0 0 8px var(--term-glow);
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}

/* Phosphor glow */
.terminal-screen::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at center,
    var(--term-glow) 0%,
    transparent 70%
  );
  opacity: 0.05;
  pointer-events: none;
}
</style>
