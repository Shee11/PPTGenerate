<!--
  SlideShell.vue - Editorial Base Layout Wrapper
  
  Props:
    - theme: Theme name (default: editorial)
    - vibe: Style variant (classic, modern, luxe, warm)
    - header: Optional header text
    - footer: Optional footer text
    - dark: Dark mode toggle
-->
<template>
  <div 
    class="slide-shell" 
    :class="[
      `vibe-${vibe}`,
      { 'edit-dark': dark }
    ]"
  >
    <!-- Background layer -->
    <div class="shell-bg"></div>
    
    <!-- Header -->
    <header v-if="header" class="shell-header">
      <span class="header-text">{{ header }}</span>
      <div class="header-line"></div>
    </header>
    
    <!-- Main content -->
    <main class="shell-content">
      <slot />
    </main>
    
    <!-- Footer -->
    <footer v-if="footer || pageNumber" class="shell-footer">
      <div class="footer-line"></div>
      <div class="footer-content">
        <span v-if="footer" class="footer-text">{{ footer }}</span>
        <span v-if="pageNumber" class="page-number">{{ pageNumber }}</span>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  theme?: string
  vibe?: 'classic' | 'modern' | 'luxe' | 'warm'
  header?: string
  footer?: string
  pageNumber?: string | number
  dark?: boolean
}>(), {
  theme: 'editorial',
  vibe: 'classic',
  dark: false
})
</script>

<style scoped>
.slide-shell {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--edit-bg);
  padding: 2.5rem 3rem;
  overflow: hidden;
}

/* Background */
.shell-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

/* Vibe backgrounds */
.vibe-luxe .shell-bg {
  background: var(--edit-black);
}

.vibe-warm .shell-bg {
  background: var(--edit-cream);
}

/* Header */
.shell-header {
  flex-shrink: 0;
  margin-bottom: 1.5rem;
}

.header-text {
  font-family: var(--edit-font-accent);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--edit-text-light);
}

.header-line {
  width: 100%;
  height: 1px;
  background: var(--edit-light);
  margin-top: 0.75rem;
}

.vibe-luxe .header-line {
  background: var(--edit-slate);
}

/* Content */
.shell-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

/* Footer */
.shell-footer {
  flex-shrink: 0;
  margin-top: 1.5rem;
}

.footer-line {
  width: 100%;
  height: 1px;
  background: var(--edit-light);
  margin-bottom: 0.75rem;
}

.vibe-luxe .footer-line {
  background: var(--edit-slate);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-text {
  font-family: var(--edit-font-accent);
  font-size: 0.75rem;
  color: var(--edit-text-light);
}

.page-number {
  font-family: var(--edit-font-display);
  font-size: 0.85rem;
  color: var(--edit-text-light);
}

/* Dark mode */
.edit-dark {
  background: var(--edit-charcoal);
  color: var(--edit-light);
}

.edit-dark .header-text,
.edit-dark .footer-text,
.edit-dark .page-number {
  color: var(--edit-silver);
}

.edit-dark .header-line,
.edit-dark .footer-line {
  background: var(--edit-slate);
}
</style>
