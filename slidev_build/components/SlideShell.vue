<script setup lang="ts">
import { computed } from 'vue'

// Props from frontmatter
const props = defineProps<{
  theme?: 'business' | 'cyber'
  vibe?: 'none' | 'particles' | 'waves' | 'noise' | 'bokeh' | 'mesh'
}>()

// Theme CSS variable mappings
const themeVariables = computed(() => {
  const theme = props.theme || 'business'
  
  if (theme === 'business') {
    return {
      '--c-bg-base': '#ffffff',
      '--c-bg-surface': '#f8fafc',
      '--c-primary': '#2563eb',
      '--c-accent': '#3b82f6',
      '--c-text-main': '#0f172a',
      '--c-text-muted': '#64748b',
      '--font-family': 'Inter, sans-serif',
      '--shadow-theme': '0 1px 3px rgba(0, 0, 0, 0.1)',
      '--c-success': '#10b981',
      '--c-danger': '#ef4444',
      '--border-theme': '#e2e8f0',
    }
  } else if (theme === 'cyber') {
    return {
      '--c-bg-base': '#050505',
      '--c-bg-surface': '#0a0a0a',
      '--c-primary': '#00ffa3',
      '--c-accent': '#00ff6e',
      '--c-text-main': '#e2e8f0',
      '--c-text-muted': '#94a3b8',
      '--font-family': 'Orbitron, monospace',
      '--shadow-theme': '0 0 20px var(--c-primary)',
      '--c-success': '#00ff6e',
      '--c-danger': '#ff006e',
      '--border-theme': '#1e293b',
    }
  }
  
  return {}
})

// Apply grid pattern for cyber theme
const backgroundStyle = computed(() => {
  if (props.theme === 'cyber') {
    return {
      backgroundImage: `
        linear-gradient(rgba(0, 255, 163, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 163, 0.1) 1px, transparent 1px)
      `,
      backgroundSize: '50px 50px',
    }
  }
  return {}
})

// Vibe effect classes
const vibeClass = computed(() => {
  const vibe = props.vibe || 'none'
  return vibe !== 'none' ? `vibe-${vibe}` : ''
})
</script>

<template>
  <div 
    class="slidev-slide-shell" 
    :class="vibeClass"
    :style="{ ...themeVariables, ...backgroundStyle }"
  >
    <!-- Floating particles effect -->
    <div v-if="vibe === 'particles'" class="vibe-particles">
      <div class="particle" v-for="i in 20" :key="i"></div>
    </div>
    
    <!-- Waves effect -->
    <div v-if="vibe === 'waves'" class="vibe-waves">
      <div class="wave wave-1"></div>
      <div class="wave wave-2"></div>
      <div class="wave wave-3"></div>
    </div>
    
    <!-- Noise texture -->
    <div v-if="vibe === 'noise'" class="vibe-noise"></div>
    
    <!-- Bokeh lights -->
    <div v-if="vibe === 'bokeh'" class="vibe-bokeh">
      <div class="bokeh-light" v-for="i in 12" :key="i"></div>
    </div>
    
    <!-- Mesh gradient -->
    <div v-if="vibe === 'mesh'" class="vibe-mesh"></div>
    
    <slot />
  </div>
</template>

<style scoped>
.slidev-slide-shell {
  width: 100%;
  height: 100%;
  background-color: var(--c-bg-base);
  color: var(--c-text-main);
  font-family: var(--font-family);
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

/* === VIBE: PARTICLES === */
.vibe-particles {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: radial-gradient(circle, var(--c-primary), transparent);
  border-radius: 50%;
  opacity: 0.6;
  animation: float-particle 20s infinite ease-in-out;
}

.particle:nth-child(1) { left: 10%; animation-delay: 0s; animation-duration: 18s; }
.particle:nth-child(2) { left: 20%; animation-delay: 2s; animation-duration: 22s; }
.particle:nth-child(3) { left: 30%; animation-delay: 4s; animation-duration: 20s; }
.particle:nth-child(4) { left: 40%; animation-delay: 1s; animation-duration: 24s; }
.particle:nth-child(5) { left: 50%; animation-delay: 3s; animation-duration: 19s; }
.particle:nth-child(6) { left: 60%; animation-delay: 5s; animation-duration: 21s; }
.particle:nth-child(7) { left: 70%; animation-delay: 2s; animation-duration: 23s; }
.particle:nth-child(8) { left: 80%; animation-delay: 4s; animation-duration: 18s; }
.particle:nth-child(9) { left: 90%; animation-delay: 1s; animation-duration: 20s; }
.particle:nth-child(10) { left: 15%; animation-delay: 3s; animation-duration: 22s; }
.particle:nth-child(11) { left: 25%; animation-delay: 5s; animation-duration: 19s; }
.particle:nth-child(12) { left: 35%; animation-delay: 0s; animation-duration: 21s; }
.particle:nth-child(13) { left: 45%; animation-delay: 2s; animation-duration: 24s; }
.particle:nth-child(14) { left: 55%; animation-delay: 4s; animation-duration: 18s; }
.particle:nth-child(15) { left: 65%; animation-delay: 1s; animation-duration: 20s; }
.particle:nth-child(16) { left: 75%; animation-delay: 3s; animation-duration: 22s; }
.particle:nth-child(17) { left: 85%; animation-delay: 5s; animation-duration: 19s; }
.particle:nth-child(18) { left: 95%; animation-delay: 2s; animation-duration: 21s; }
.particle:nth-child(19) { left: 12%; animation-delay: 0s; animation-duration: 23s; }
.particle:nth-child(20) { left: 88%; animation-delay: 4s; animation-duration: 20s; }

@keyframes float-particle {
  0% {
    transform: translateY(100vh) scale(0);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-100px) scale(1.5);
    opacity: 0;
  }
}

/* === VIBE: WAVES === */
.vibe-waves {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.wave {
  position: absolute;
  bottom: -10%;
  left: -10%;
  width: 120%;
  height: 120%;
  background: radial-gradient(
    ellipse at bottom,
    var(--c-primary) 0%,
    transparent 70%
  );
  opacity: 0.1;
  animation: wave-motion 15s ease-in-out infinite;
}

.wave-1 {
  animation-delay: 0s;
}

.wave-2 {
  animation-delay: 5s;
  opacity: 0.07;
}

.wave-3 {
  animation-delay: 10s;
  opacity: 0.05;
}

@keyframes wave-motion {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-20%) scale(1.1);
  }
}

/* === VIBE: NOISE === */
.vibe-noise {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.5'/%3E%3C/svg%3E");
  opacity: 0.15;
  pointer-events: none;
  mix-blend-mode: overlay;
}

/* === VIBE: BOKEH === */
.vibe-bokeh {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.bokeh-light {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.3;
  animation: bokeh-float 25s infinite ease-in-out;
}

.bokeh-light:nth-child(1) {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, var(--c-primary), transparent);
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.bokeh-light:nth-child(2) {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, var(--c-accent), transparent);
  top: 20%;
  right: 15%;
  animation-delay: 3s;
}

.bokeh-light:nth-child(3) {
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, var(--c-success), transparent);
  bottom: 15%;
  left: 20%;
  animation-delay: 6s;
}

.bokeh-light:nth-child(4) {
  width: 180px;
  height: 180px;
  background: radial-gradient(circle, var(--c-primary), transparent);
  bottom: 25%;
  right: 25%;
  animation-delay: 9s;
}

.bokeh-light:nth-child(5) {
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, var(--c-accent), transparent);
  top: 40%;
  left: 5%;
  animation-delay: 2s;
}

.bokeh-light:nth-child(6) {
  width: 280px;
  height: 280px;
  background: radial-gradient(circle, var(--c-primary), transparent);
  top: 50%;
  right: 10%;
  animation-delay: 5s;
}

.bokeh-light:nth-child(7) {
  width: 160px;
  height: 160px;
  background: radial-gradient(circle, var(--c-success), transparent);
  top: 70%;
  left: 40%;
  animation-delay: 8s;
}

.bokeh-light:nth-child(8) {
  width: 240px;
  height: 240px;
  background: radial-gradient(circle, var(--c-accent), transparent);
  bottom: 10%;
  right: 40%;
  animation-delay: 1s;
}

.bokeh-light:nth-child(9) {
  width: 190px;
  height: 190px;
  background: radial-gradient(circle, var(--c-primary), transparent);
  top: 5%;
  left: 50%;
  animation-delay: 4s;
}

.bokeh-light:nth-child(10) {
  width: 270px;
  height: 270px;
  background: radial-gradient(circle, var(--c-success), transparent);
  bottom: 5%;
  left: 60%;
  animation-delay: 7s;
}

.bokeh-light:nth-child(11) {
  width: 210px;
  height: 210px;
  background: radial-gradient(circle, var(--c-accent), transparent);
  top: 30%;
  right: 30%;
  animation-delay: 10s;
}

.bokeh-light:nth-child(12) {
  width: 260px;
  height: 260px;
  background: radial-gradient(circle, var(--c-primary), transparent);
  bottom: 40%;
  left: 30%;
  animation-delay: 3s;
}

@keyframes bokeh-float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.2;
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
    opacity: 0.35;
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
    opacity: 0.25;
  }
}

/* === VIBE: MESH === */
.vibe-mesh {
  position: absolute;
  inset: 0;
  background: radial-gradient(
      circle at 20% 30%,
      var(--c-primary) 0%,
      transparent 50%
    ),
    radial-gradient(
      circle at 80% 20%,
      var(--c-accent) 0%,
      transparent 50%
    ),
    radial-gradient(
      circle at 40% 80%,
      var(--c-success) 0%,
      transparent 50%
    ),
    radial-gradient(
      circle at 90% 70%,
      var(--c-primary) 0%,
      transparent 50%
    );
  opacity: 0.08;
  filter: blur(60px);
  pointer-events: none;
  animation: mesh-shift 20s ease-in-out infinite;
}

@keyframes mesh-shift {
  0%, 100% {
    transform: scale(1) rotate(0deg);
  }
  50% {
    transform: scale(1.1) rotate(5deg);
  }
}
</style>
