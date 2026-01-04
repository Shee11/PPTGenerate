<!--
  SlideShell - Cyberpunk Base Wrapper Component
  
  Purpose:
  - Futuristic neon-lit visual design with glitch effects
  - HUD-style corners and scan line overlays
  - Consistent dark theme with neon accents
  
  Props:
    - theme: Theme name (default: cyberpunk)
    - vibe: Vibe modifier (minimal, clean, balanced, intense, glitch)
    - header: Header text
    - footer: Footer text
  
  Slots:
    - default: Main content
    - header: Custom header
    - footer: Custom footer
-->
<template>
  <div 
    class="slide-shell"
    :class="[`vibe-${vibe}`, { 'has-header': hasHeader, 'has-footer': hasFooter }]"
    :style="themeVariables"
  >
    <!-- Scan lines overlay -->
    <div class="scanlines-overlay"></div>
    
    <!-- Grid background -->
    <div class="grid-bg"></div>
    
    <!-- HUD corners -->
    <div class="hud-frame">
      <div class="hud-corner hud-tl"></div>
      <div class="hud-corner hud-tr"></div>
      <div class="hud-corner hud-bl"></div>
      <div class="hud-corner hud-br"></div>
    </div>
    
    <!-- Header area -->
    <header v-if="hasHeader" class="shell-header">
      <slot name="header">
        <span class="header-text">{{ header }}</span>
        <span class="header-decoration"></span>
      </slot>
    </header>
    
    <!-- Main content -->
    <main class="shell-content">
      <slot />
    </main>
    
    <!-- Footer area -->
    <footer v-if="hasFooter" class="shell-footer">
      <slot name="footer">
        <span class="footer-decoration"></span>
        <span class="footer-text">{{ footer }}</span>
      </slot>
    </footer>
    
    <!-- Ambient glow effects -->
    <div class="ambient-glow ambient-glow-1"></div>
    <div class="ambient-glow ambient-glow-2"></div>
  </div>
</template>

<script setup lang="ts">
import { computed, provide } from 'vue'

const props = withDefaults(defineProps<{
  theme?: string
  vibe?: string
  header?: string
  footer?: string
}>(), {
  theme: 'cyberpunk',
  vibe: 'balanced'
})

provide('theme', computed(() => props.theme || 'cyberpunk'))
provide('vibe', computed(() => props.vibe || 'balanced'))

// Cyberpunk Theme CSS variables
const themeVariables = computed(() => {
  const neonColors = ['cyan', 'magenta', 'yellow', 'pink', 'green']
  const vibeSettings: Record<string, { primary: string; secondary: string; glowIntensity: number }> = {
    minimal: { primary: 'cyan', secondary: 'cyan', glowIntensity: 0.3 },
    clean: { primary: 'cyan', secondary: 'magenta', glowIntensity: 0.5 },
    balanced: { primary: 'cyan', secondary: 'magenta', glowIntensity: 0.7 },
    intense: { primary: 'magenta', secondary: 'cyan', glowIntensity: 1 },
    glitch: { primary: 'pink', secondary: 'green', glowIntensity: 1 },
  }
  
  const settings = vibeSettings[props.vibe] || vibeSettings.balanced
  
  return {
    // Primary neon colors
    '--cyber-primary': `var(--cyber-${settings.primary})`,
    '--cyber-primary-dark': `var(--cyber-${settings.primary}-dark)`,
    '--cyber-primary-glow': `var(--cyber-${settings.primary}-glow)`,
    '--cyber-secondary': `var(--cyber-${settings.secondary})`,
    '--cyber-secondary-glow': `var(--cyber-${settings.secondary}-glow)`,
    '--glow-intensity': settings.glowIntensity,
    
    // Background
    '--cyber-bg-dark': '#0a0a0f',
    '--cyber-bg-card': '#12121a',
    
    // Text
    '--cyber-text': '#e0e0e0',
    '--cyber-text-dim': '#808090',
    
    // Typography
    '--cyber-font-display': "'Orbitron', 'Rajdhani', sans-serif",
    '--cyber-font-body': "'Rajdhani', sans-serif",
    '--cyber-font-mono': "'Share Tech Mono', monospace",
  }
})

const hasHeader = computed(() => !!props.header || !!props.vibe)
const hasFooter = computed(() => !!props.footer)
</script>

<style scoped>
.slide-shell {
  width: 100%;
  height: 100%;
  background: var(--cyber-bg-dark, #0a0a0f);
  color: var(--cyber-text, #e0e0e0);
  font-family: var(--cyber-font-body);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  padding: 24px;
}

/* Grid background */
.grid-bg {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  z-index: 0;
}

/* Scan lines overlay */
.scanlines-overlay {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 0, 0, 0.15) 2px,
    rgba(0, 0, 0, 0.15) 4px
  );
  pointer-events: none;
  z-index: 50;
  opacity: 0.5;
}

/* HUD Frame corners */
.hud-frame {
  position: absolute;
  inset: 16px;
  pointer-events: none;
  z-index: 10;
}

.hud-corner {
  position: absolute;
  width: 30px;
  height: 30px;
}

.hud-tl {
  top: 0;
  left: 0;
  border-top: 2px solid var(--cyber-primary, #00FFFF);
  border-left: 2px solid var(--cyber-primary, #00FFFF);
  box-shadow: 
    -2px -2px 10px var(--cyber-primary-glow, rgba(0, 255, 255, 0.5));
}

.hud-tr {
  top: 0;
  right: 0;
  border-top: 2px solid var(--cyber-primary, #00FFFF);
  border-right: 2px solid var(--cyber-primary, #00FFFF);
  box-shadow: 
    2px -2px 10px var(--cyber-primary-glow, rgba(0, 255, 255, 0.5));
}

.hud-bl {
  bottom: 0;
  left: 0;
  border-bottom: 2px solid var(--cyber-secondary, #FF00FF);
  border-left: 2px solid var(--cyber-secondary, #FF00FF);
  box-shadow: 
    -2px 2px 10px var(--cyber-secondary-glow, rgba(255, 0, 255, 0.5));
}

.hud-br {
  bottom: 0;
  right: 0;
  border-bottom: 2px solid var(--cyber-secondary, #FF00FF);
  border-right: 2px solid var(--cyber-secondary, #FF00FF);
  box-shadow: 
    2px 2px 10px var(--cyber-secondary-glow, rgba(255, 0, 255, 0.5));
}

/* Header */
.shell-header {
  position: relative;
  z-index: 20;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.header-text {
  font-family: var(--cyber-font-display);
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--cyber-primary, #00FFFF);
  text-shadow: 0 0 10px var(--cyber-primary-glow, rgba(0, 255, 255, 0.5));
}

.header-decoration {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--cyber-primary, #00FFFF), transparent);
  box-shadow: 0 0 10px var(--cyber-primary-glow, rgba(0, 255, 255, 0.5));
}

/* Main content */
.shell-content {
  flex: 1;
  position: relative;
  z-index: 20;
  min-height: 0;
  overflow: hidden;
}

/* Footer */
.shell-footer {
  position: relative;
  z-index: 20;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.footer-decoration {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--cyber-secondary, #FF00FF));
  box-shadow: 0 0 10px var(--cyber-secondary-glow, rgba(255, 0, 255, 0.5));
}

.footer-text {
  font-family: var(--cyber-font-mono);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--cyber-secondary, #FF00FF);
  text-shadow: 0 0 10px var(--cyber-secondary-glow, rgba(255, 0, 255, 0.5));
}

/* Ambient glow effects */
.ambient-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  z-index: 1;
  opacity: calc(var(--glow-intensity, 0.7) * 0.3);
}

.ambient-glow-1 {
  width: 400px;
  height: 400px;
  background: var(--cyber-primary, #00FFFF);
  top: -150px;
  right: -150px;
}

.ambient-glow-2 {
  width: 300px;
  height: 300px;
  background: var(--cyber-secondary, #FF00FF);
  bottom: -100px;
  left: -100px;
}

/* Vibe modifiers */
.vibe-minimal .scanlines-overlay,
.vibe-minimal .grid-bg {
  display: none;
}

.vibe-minimal .ambient-glow {
  opacity: 0.1;
}

.vibe-minimal .hud-corner {
  opacity: 0.5;
}

.vibe-clean .scanlines-overlay {
  opacity: 0.2;
}

.vibe-clean .ambient-glow {
  opacity: 0.15;
}

.vibe-intense .scanlines-overlay {
  opacity: 0.7;
}

.vibe-intense .ambient-glow {
  opacity: 0.5;
}

.vibe-intense .hud-corner {
  width: 50px;
  height: 50px;
  border-width: 3px;
}

.vibe-glitch .shell-content {
  animation: glitch 0.5s ease-in-out infinite;
}

.vibe-glitch .header-text,
.vibe-glitch .footer-text {
  animation: flicker 1.5s ease-in-out infinite;
}

@keyframes glitch {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-1px, 1px); }
  40% { transform: translate(-1px, -1px); }
  60% { transform: translate(1px, 1px); }
  80% { transform: translate(1px, -1px); }
}

@keyframes flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; }
  52% { opacity: 1; }
  54% { opacity: 0.9; }
}

/* With header/footer adjustments */
.has-header .shell-content {
  padding-top: 0.5rem;
}

.has-footer .shell-content {
  padding-bottom: 0.5rem;
}
</style>
